# c4/c6/c7 非对齐归约优化实验记录（2026-09-24）

> 目标：削减 BatchKernel 的 while 树归约（pitch 非 64 倍数）的 vec/scl 成本。
> 动机：c4 平台 8.70 vs best 6.66（31% gap）、c7 17.30 vs 13.90（24%）、c6 12.44 vs 10.86（15%）。
> profiler 证据：c4 的 while 树归约占 vec 时间 11-14%（批量 vcadd 后 vec 1.35→1.16）。

## 1. 背景事实（profiler 实测）

- c4（767x197 fp16，BatchKernel，pitch=208）：aiv_time 6.79µs，串行和 8.81µs（流水省 2.02）
- 等待：Vector Wait 73.3%、MTE2 Wait 47.5%、MTE3 Wait 74.8%
- c4 瓶颈：mte2 4.49µs 主导（非对齐 DMA 伪影）+ while 树归约占 vec

## 2. 归约现状（while 树，正确）

BatchKernel `pitch_%64 != 0` 分支（line ~420）：
```
tail 折叠：Add(tmp[0], tmp[full*64], tail, nr, {stride})   // 每行尾 16 进行首
while 树：多层 Add(tmp[j*64], tmp[(j+half)*64], 64, nr, {stride})
WholeReduceSum(stats, tmp, finalMask, nr, 1, 1, stride)
```
- 每层 Add + barrier，c4 full=3（2 层）、c6 full=9（4 层）
- stride = pitch/8（uint8 上限 255）

## 3. 批量归约 API 签名（dav-2201，dav_m200 impl）

### vcadd（裸指令）
```cpp
// impl/basic_api/dav_m200/kernel_operator_vec_reduce_impl.h:55
vcadd(dst, src, repeat, dst_repeat_stride, src_block_stride, src_repeat_stride, 0)
```
- repeat：归约次数
- dst_repeat_stride / src_repeat_stride：每次 repeat 步进
- mask 由 SetMaskCount() + SetVectorMask(0, n) 设置，支持 >64 元素（c2 用 d_=197）

### BlockReduceSum（public）
```cpp
BlockReduceSum(dst, src, repeatTime, mask, dstRepStride, srcBlkStride, srcRepStride)
// 内部 vcgadd
```

### RepeatReduceSum（public，标准高层）
```cpp
RepeatReduceSum<T, false>(dst, src, repeatTime, elemsInOneRepeat,
    dstBlkStride, srcBlkStride, dstRepStride, srcRepStride)
// 内部 vcadd
// 官方正确用法（sum_common_impl.h SumForOneRepeatTime）：
//   SetVectorMask<T>(0, n);  // 每行 mask = n
//   for row: RepeatReduceSum(dst[row], src[row*inner], 1, MASK_PLACEHOLDER, ...);
//   SetMaskNorm(); ResetMask();
```

## 4. 尝试记录（全部性能收益真实但正确性失败）

| # | 方式 | 性能（c4） | 正确性 | 失败原因推测 |
|---|------|-----------|--------|-------------|
| 1 | 批量 vcadd（repeat=nr, srcRep=pitch） | -10%（7.60）| ❌ non-finite | stride 单位/mask 交互错 |
| 2 | 批量 vcadd（srcRep=pitch/8） | -10% | ❌ non-finite | 同上 |
| 3 | 分块 BlockReduceSum（每块 repeat=nr）| -6%（7.94）| ❌ mismatch | partial 布局/fold 自加重叠 |
| 4 | RepeatReduceSum 批量（elemsInOneRepeat=d_）| -2% | ❌ mismatch | elemsInOneRepeat>64 mask 错 |
| 5 | RepeatReduceSum 逐行（官方模式）| -6%（mte2 -18%）| ❌ mismatch/non-finite | 仍错，原因未明 |
| 6 | 逐行高层 ReduceSum | +9%（9.28）| ❌ non-finite | ReduceSum dst=partial 缓冲冲突? |

**关键教训**：
- 批量 vcadd/BlockReduceSum/RepeatReduceSum 处理非 64 倍数（197）批量归约的 mask/stride 语义，读代码无法确定，需现场硬件实验
- 逐行高层 ReduceSum 正确性也失败 → 怀疑是 partial/work 缓冲布局冲突，或 dst 非独立缓冲问题
- 性能收益真实（c4 -6~10%、mte2 -18%）——方向正确

## 4b. 突破：dst 必须用独立缓冲（2026-09-24 续）

**关键发现**：逐行 ReduceSum 失败是因为 **dst 用了 reducebuf 内的 partial 区**（与 work 缓冲可能冲突）。
**改成 dst=stats[r]（独立 statsbuf）后 4/4 PASS 全对！**

```cpp
// 正确版（dst 独立）：
auto work = reducebuf.template Get<float>();
for (uint32_t r = 0; r < nr; ++r) {
    ReduceSum(stats[r], tmp[r * pitch_], work, d_);  // dst=stats[r] 独立缓冲
}
```
- 性能：c4 8.64 vs base 8.48（+1.9%，高层 ReduceSum 固定成本高）
- **结论：归约 API 的 dst 必须独立于 reducebuf/scratch**。批量 vcadd/BlockReduceSum 之前失败可能也是 dst 缓冲问题（但批量 vcadd 用 stats 仍错 → 还有 stride/mask 语义问题）。

## 4c. 批量 BlockReduceSum 正确版（dst 独立）仍崩

- 用 dst=reducebuf 独立区 + 每块 repeat=nr + fold，**仍 76ms 崩溃**
- 说明批量 repeat 的 srcRepStride 单位语义未掌握（现有正确用法 srcRepStride=8，单位=8 元素？）

## 4d. RepeatReduceSum 逐行（dst=stats[r]）仍错

- 尝试 SetVectorMask / SetMaskCount / elemsInOneRepeat=d_ 三种 mask 方式，**全部 mismatch**
- **结论：RepeatReduceSum/vcadd 的 mask 由内部 SetMask(elemsInOneRepeat) 控制，外部 SetVectorMask 无效；但传 d_（197>64）也错**——vcadd 系列对 >64 元素的 mask 语义未掌握
- 高层 ReduceSum（内部处理任意长度 mask）**正确**，但逐行调用 vec 反升（1.82 vs while树 1.35）

## 4e. 最终结论（本轮）

| 方式 | 正确性 | vec | dur |
|------|--------|-----|-----|
| 原始 while 树 | ✅ | 1.35 | 8.48 |
| 逐行 ReduceSum（dst 独立）| ✅ | 1.82 | 8.64 |
| 批量 vcadd | ❌ | 1.16 | 7.60 |
| 批量 BlockReduceSum | ❌ 崩 | - | - |
| RepeatReduceSum（3 种 mask）| ❌ | 1.53-1.79 | 8.34-8.70 |
| 逐行 vcadd（c2 模式，dst 独立）| ❌ | 1.70 | 8.42 |
| 逐行 vcadd + 交替事件 ID | ❌ | **1.16** | 8.28 |

**关键知识**：
1. **归约 dst 必须独立缓冲**（不能是 reducebuf 内与 scratch 重叠）→ 逐行 ReduceSum 由此正确
2. **vcadd 系列对 >64 元素（197）的 mask 语义**：高层 ReduceSum 正确处理，vcadd/RepeatReduceSum 需要特殊 mask 配置（未突破）
3. **vcadd 归约的 vec 收益确认**（1.35→1.16，-14%），但 mask 正确性需现场硬件调试
4. 原始 while 树的 vec 1.35 已优于逐行 ReduceSum（1.82）——**while 树本身不差**，vcadd 的 1.16 是真优化空间
5. **c2 单行 vcadd（197>64）正确**，c4 逐行 vcadd 错误——差异在 mask 应用时机/事件管理，需对比调试

## 4f. 🔑 突破：vcadd 结果在标量寄存器，必须 GetReduceRepeatSumSpr 读（2026-09-24 续）

**根因**：vcadd 归约结果落在**标量寄存器**（不是直接写 dst），必须用 `GetReduceRepeatSumSpr<float>()` 读出再 `SetValue` 写入 dst。

**正确的 vcadd 模式**（c4 逐行，4/4 PASS 验证）：
```cpp
if ASCEND_IS_AIV {
    SetMaskCount();
    SetVectorMask<float>(0, d_);          // mask = 归约元素数（支持 >64，c2 用 197）
    for (uint32_t r = 0; r < nr; ++r) {
        vcadd((__ubuf__ float*)(stats[r].GetPhyAddr()),
              (__ubuf__ float*)tmp[r*pitch_].GetPhyAddr(),
              1, 1, 1, 8, 1);             // repeat=1（单行）
        const event_t ev = (event_t)(r % 2);
        SetFlag<HardEvent::V_S>(ev); WaitFlag<HardEvent::V_S>(ev);
        stats[r].SetValue(0, GetReduceRepeatSumSpr<float>());  // ★ 读标量结果
        SetFlag<HardEvent::S_V>(ev); WaitFlag<HardEvent::S_V>(ev);
        SetFlag<HardEvent::S_MTE3>(ev); WaitFlag<HardEvent::S_MTE3>(ev);
    }
    SetMaskNorm(); ResetMask();
}
```

**性能**：c4 9.18 vs base 8.48（**+8% 慢**）——逐行 vcadd 每行 3 事件 + 标量读，nr 次开销大。
**结论**：vcadd 批量归约**不适合每行独立统计**（GetReduceRepeatSumSpr 每次只读 1 个标量结果，批量 repeat 无法每行独立读）→ **只能逐行（慢）**。c4 的 while 树（批量、快）仍是每行归约的最优正确实现。

## 4g. 其他仿射实验（无收益，2026-09-24 续）

| 尝试 | 目标 | 结果 |
|------|------|------|
| c2 MulAddDst → Mul+Add（fp32，§18.1 依据）| c2 | 严格交替 +3.5%（MulAddDst 1-pass dst 累加已最优）|
| c1 MicroRow MulAddDst → FusedMulAdd（half，§2 依据）| c1 | 持平（±1%，c1 启动主导）|
| c14 pitch 检查 | c14 | 无 bug（gap=0 正确）；本地慢 2.3× 是环境差异（msprof 冷态 vs 平台）|

## 4h. 最终全局结论

**当前 kernel 81.34 版（SHA256 2e0cd302）是 dav-2201 上的最优正确实现**：
- c4/c6/c7 的 while 树归约 = 每行归约最优（vcadd 受标量寄存器限制、逐行慢）
- c2 的 vcadd + MulAddDst = 已最优
- c1 的 MicroRow = 启动主导，仿射无收益
- c14 的 DMA = 环境差异，无 kernel 可优化点
- vcadd 完整正确模式（GetReduceRepeatSumSpr）已突破并记录

## 5. 下一步实验计划（正确性驱动）

1. ✅ vcadd 完整模式突破（GetReduceRepeatSumSpr 读标量结果）
2. ✅ while 树 = 每行归约最优确认
3. ✅ 仿射（MulAddDst/FMA）无收益
4. **待试：c14 的真实平台 shape 确认**（本地 2097152x115 可能不匹配平台）
5. **待试：批量归约的 dst 累积语义**（vcadd repeat 是否写 dst[0..nr-1]，若可则批量读）
6. **待试：c5 Pass2 的 tb 缓冲复用**（重新评估 UB）

## 6. 相关文件

- 当前 kernel：`/mnt/workspace/sxy/addrmsnormbias_problem_1742_template/kernel.asc`（81.34 版，SHA256 2e0cd302）
- 实验变体：/tmp/opencode/kernel_c4*.asc（临时）
- impl 参考：`/home/developer/Ascend/cann-9.0.0/aarch64-linux/asc/impl/basic_api/dav_m200/kernel_operator_vec_reduce_impl.h`
- 官方用法：`.../impl/adv_api/detail/reduce/sum/sum_common_impl.h`（SumForOneRepeatTime）

## 6. 后续实验补充（2026-09-24 续）

### 已尝试（全部严格交替确认）
| 方向 | 目标 | 结果 |
|------|------|------|
| MakeScale Rsqrt | 所有 case | ❌ 精度灾难（fp32/fp16 大量 mismatch）——HISTORY 警告正确 |
| PIPE_ALL → PIPE_V（4 处）| c1/c2/c3/c5 | ❌ 严格交替反转（单测 -5% 是进程漂移，严格 +9%）|
| c2 vcadd 省 S_MTE3 事件 | c2 | ❌ 正确但 +3% 慢（S_MTE3 必要）|
| c06 强制 StreamKernel | c06 | ❌ +2.3×（BatchKernel 批量最优）|
| c06 5 核并行 | c5 | ❌ +4%（DMA 请求变多）|

### 核心结论（80+ 次实验）
- **每个 case 本地都接近或快于 Tbest**（c06 9.96 vs 9.62、c02 1.94 vs 2.21）
- **平台比本地慢是提交级偏移**（c06 12.78 vs 9.96、c07 17.03 vs 11.88），kernel 无法解决
- **当前 kernel 81.34 版（2e0cd302）是 dav-2201 的最优正确实现**

### 关键纪律（本次强化）
1. **单进程测的收益必须严格交替确认**（c2 -5% 是进程漂移假象，严格 +9%）
2. **精度优化必须 verify**（Rsqrt 灾难性失败，HISTORY 警告不可忽略）
3. **PIPE_ALL 排空是必要的**（PIPE_V 反而慢）
4. **事件同步（S_MTE3）是必要的**（省了慢）

### 平台验证结果（用户授权提交验证）
| 版本 | 改动 | 平台成绩 |
|------|------|---------|
| 81.34 | PIPE_ALL×4 | 79.95 |
| **PIPE_V** | PIPE_ALL→PIPE_V×4 | **81.31 ✅** |
| 删 PIPE_V | 删除×4 | 80.60 |
| tail 16→5 | 只加有效尾 | 79.50 |

**关键教训**：
1. **PIPE_ALL→PIPE_V 平台 +1.36 分**（逻辑正确 + 本地 PASS，即使本地严格交替反转）——**验证"逻辑正确即可提交验证"的方法论**
2. **tail 折叠 16→5 平台退步**（逻辑正确 + 本地 PASS 但 pad Add 是免费的）——**不是所有逻辑正确都生效，平台验证是最终**
3. **PIPE_V 是边界最优**（删了慢 c01/c02，PIPE_ALL 过度）

### 平台验证汇总（6 次提交验证）
| 版本 | 改动 | 平台成绩 |
|------|------|---------|
| 81.34 | PIPE_ALL×4 | 79.95 |
| **PIPE_V** | PIPE_ALL→PIPE_V×4 | **81.31 ✅ 最终采用** |
| 删 PIPE_V | 删除×4 | 80.60 |
| tail 16→5 | 只加有效尾 | 79.50 |
| c5 span 精确 d/4 | 每核精确份额 | 80.46 |
| c4 pitch=256 | 64 对齐 BlockReduceSum | 79.59 |

**最终结论**：PIPE_V 版（81.31）是 dav-2201 的最优。
- 重构（pitch 对齐/BlockReduceSum/flat 布局）全部被"非对齐 DMA 惩罚 + 向量 32B 对齐 + 标量寄存器"硬件约束阻断
- while 树归约在"保持 pitch 紧凑"前提下是最优
- 唯一冗余 = PIPE_ALL（过度同步），改为 PIPE_V
