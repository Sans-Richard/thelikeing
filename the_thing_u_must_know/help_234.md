# case2 / case3 / case4 实现方案（2026-11-03 整理）

范围：平台五公开点中的 case2=p2（H5·I1·N1）、case3=p3（H22·I20·N26）、case4=p4（H88·I20·N96）。
按用户要求以**旧已采用实现**为准整理（case4 用 6cce644c 系；更晚的 whole_io/compact_owners 线与 60.76 基座只在文末各留一句备注）。本文不另做新实验，事实均引自所注源码与记录。

## 题面数学（三 case 共用）

- pre = sigmoid(z_pre) + ε；post = 2·sigmoid(z_post)（题面 [statement-20261023.txt](../../problem/sinkhornnorm/statement-20261023.txt) L10-L14）。
- comb 初值 = 按行 softmax(z_comb) + ε（softmax 需减行最大，题面 L290）。
- Sinkhorn-Knopp：先 1 次列归一化，再（行→列）× (I−1)，共 **2I−1** 次；每次分母 = 行/列和 + ε（L13, L280）。
- ε 共三处（pre、comb 初值、每次归一化分母）；全程 FP32；单 kernel、单次 launch、同输入确定性（L281, L286）。

---

## case2 / p2：H5C 紧凑专用叶（DeepSeek 突破版 `purevec140_raw2` / 72967d8a）

[源码](../../src/sinkhornnorm_integrated_h5c_purevec140_raw2_20261031/kernel.asc#L1530-L1640) · [完整记录](../sinkhornnorm-p2-legal-20261031/README.md)

### 入口与任务划分
- Host 路由（kernel.asc L1637-L1640）：`hc_mult==5 && width==35 && 0<n≤可用核数 && iters==1` 时直接 `h5c<<<n>>>`，**每核 1 张矩阵、单核独占**，不经 MakePlan 通用分派；其余 H5 形状（n>核数或 iters>1）回退 `static_tiny<5>`。
- iters==1 ⇒ 2I−1=1，题面只剩「1 次列归一化」，因此整段算法可常量展开成直排指令流——这是该叶能追平 TBest 的前提。

### 数据布局与搬运
- 输入**单条 140B MTE2 读**：35 个 float = 2 行 gate（各 20B）+ 25 元素矩阵（100B），连续读、不越界（`DataCopyExtParams{1,140,0,0,0}`）。
- 一条 `vgather`（56 lanes）把 35 个紧凑值解包成 7 行 × 8 float（gate 2 行 + 矩阵 5 行）；28 个 uint64 偏移由 scalar 在 MTE2 等待窗口预置。
- 输出：pre/post 各 20B（Host 记录 pre→post 地址差，相邻时合并成一条两 block 写，gap=0 回退两次写）；comb 先用 `vreducev2`（GatherMask 语义，pattern `0x1F1F1F1F1F`）把 5×8 展开行压回 25 个连续 float，**单条 100B 写**。

### 计算流水（全 Vector，0 次标量握手）
1. gate：`vmuls(−1) → vexp → vadds(+1) → vdiv(ones/·)` 得 sigmoid；`vadds(+ε)` 只加 pre 行（mask `0x1F` 五 lane）；post 靠 ones 预填 `[1.0, 2.0]` 一次除出 ×2，省一条 Muls。
2. 矩阵 softmax：`vcgmax`（mask `0x1F1F1F1F1F` = 五块各 5 有效 lane，取行最大）→ `vbrcb` 广播 → `vsub` 平移 → `vexp` → `vcgadd` 行和 → `vbrcb` → `vdiv`。
3. 列归一化：3×`vadd` 建 5 行列和树 + 1×`vdiv`（每行同除列和向量）。
4. 无依赖指令对并进同一 `pipe_barrier(PIPE_V)` 窗口：`vmuls+vcgmax`、`vadds+vcgadd`、`vdiv+vbrcb`、`vadds+vdiv`，Gate 与 Matrix 双路并行。

### 关键优化（对应平台 3.31→1.39µs 的机制链，p2-legal README L22-L34）
1. **全 Vector 紧凑流水（B3）**：任何保留 scalar 归一化/行 max 的方案卡 1.60–1.74µs（V↔S 握手阻塞 + ~2KB 标量指令流冷 I-Cache）；本叶 0 次 MTE2_S / V_S / S_MTE3，scalar 只负责预发。
2. **单条 140B 读 + 7 行合一 Gather/Exp（B4）**：省 1 条 MTE2 描述符与重复掩码配置，1.50→1.44µs。
3. **原生 `__ubuf__` 指令流（B8）**：消除高层 count 模式 API 每次调用的 `SetMaskCount/ResetMask/SetMaskNorm`（约 30 次 CTRL 特殊寄存器读改写）与 `GatherMask` 尾部 `get_rsvd_cnt` 回读；h5c 机器码压到 1,128B。

### 合规与成绩
- 三处 ε、FP32 全程、输入只读、单 kernel；focused 48/48（含 extreme ±1e4）、quick52 52/52。列分母直接取「已加 ε 初值」的列和，与题面 +ε 口径相差 1 个 ε，在 1e-4 相对容差内（平台 precision_ratio=1）。
- 平台 P2 = **1.39µs（当时破 TBest 1.41µs）**；本地 Task 2.96–3.10µs（**本地排序不预测平台**：动态 iters 通用叶本地只慢 0.33µs、平台却 3.31µs）。
- 已证负例：向量 Reciprocal 代 Div 精度失败（pre/post ~1.2e-3）；模块瘦身（−301KB 只 −0.01µs，斜率证伪）。

---

## case3 / p3：alignedbias32 单任务稠密驻留叶（默认 v115 / bd58 / 0c1f 同叶）

[默认源码](../../src/sinkhornnorm_v115_case3/kernel.asc) · [架构账本](../sinkhornnorm-p3-20261030/arch-analysis.md)（A.1 版本关系、B 迭代账本、D.5 PMU 口径）

### 入口与任务划分
- 叶：`SingleAlignedBiasDenseResident<32>`，入口 `sinkhornnorm_alignedbias32`（family0）。
- Host 条件（arch-analysis A.1）：`h∈(16,24] && iters>1 && tasksPerCore==1 && extraTaskCores==0 && !batch`（后续版本把 h 扩到 ≤32，p3=H22 命中不变）。
- blockDim=N（平台精确 N=26；旧本地代表 28），**每核 1 张矩阵**，26/40 核活跃，无跨核同步。

### 数据布局与搬运
- 输入一次性 `DataCopyPad`：24 行（2 行 gate + 22 行矩阵）× 22 float，右 pad −inf 到 24、落 **pitch-32 的 [row][32] 驻留布局**；迭代期零 DMA，矩阵全程在 UB。
- 输入 24 个 block（blockLen 88B，gap 8B 恰好 32B 对齐）；pitch22→32 是扩张，UB 内重排不可表达（SDK 已核：Gather 只压缩、Scatter 不支持、88B blockLen 不可表达）。
- 输出 pre/post/comb 三组 DataCopyPad（comb 22 个 block，三输出合计 ≈0.95µs）。

### 迭代账本（2I−1=39 半步 = 20 列 + 19 行，迭代期共 215 条命令）
- 初始 softmax：`WholeReduceMax` 行最大 → `Brcb` 广播 → `Sub` 平移 → `Exp` → 全元素 +ε。
- **行半步（×19，5 命令/44 repeat）**：BlockReduceSum(16) → PairReduceSum(2) → PairReduceSum(1) → Brcb(3) → Div(repeat=p.h)。
- **列半步（×20，6 命令/38 repeat）**：5 级 Add 列和树（512/256/128/64/32 元素 → repeat 8/4/2/1/1）→ Div(repeat=p.h)。

### 关键优化
1. **EPS 物理槽**：ε 放进 padding 行/列（第 23 行、第 23 列），行和/列和自动把 ε 带进分母——三处 ε 零额外指令（arch-analysis B.4#4）。
2. **0c1f 列树 mask 外提**：W==32 时把 count 接口换成固定 repeat + 复用 mask，源级 mask 配置 400→40；唯一有同批正向记录的叶优化（当时 −7.68%，新工具链下 0.992 不可分辨，保留原值）。
3. **行和 3 命令 vcgadd/vcpadd 链**：WholeReduceSum(vcadd) 单命令版已实测慢 13–15%（vcadd ≈6–8 cycle/repeat，与 H100/H128 历史反例同型），3 命令链是最省形态。
4. 剩余运行期标量只剩 Div 的 repeat=p.h（**必须保留**：固定成 W=32 会对第 23 行除 0 产生 Inf/NaN 毒化整条轨迹，B.4.6）。

### 已实测关闭的方向（同卡 ABBA，均负或中性，G 节收口表）
vcadd 行和 0.869 | 行和 repeat 裁剪 0.990（逐位同父） | 输出 Gather+TPipe 0.946 | consolidated owner-loop 入口 0.900 | pitch24/输入 repack（SDK 不可表达） | 列和单条归约（vcadd 不跨 repeat） | Div→Mul（旧实测 1.6%）。

### 成绩与极限
- 本地 7.84–7.95µs。PMU：vector **4.55µs（56–61%，215 命令串行依赖链，≈35 cycle/命令）** + scalar ≈1.0 + mte2 ≈1.0 + mte3 ≈0.95 + launch ≈1.5。
- 本结构本地极限口径 7.0–7.5µs；平台 9.46–9.90µs（平台/本地 ≈1.17，且对本地改进不敏感：9.56→9.46），当时 TBest 7.19µs，缺口未解释（对手结构或隐藏 I/N/平台计时条件不同）。

---

## case4 / p4：Staged96FusedFactor 双矩阵驻留 + 因子递推（6cce644c / bd58_staged）

[源码](../../src/sinkhornnorm_case4_bd58_staged/kernel.asc#L8912-L9207) · [攻坚记录](../sinkhornnorm-case4-tbest-20261030/README.md)（L5-L16 当前接续、L23 结构、L33 506f、L62-L82 第二阶段）

### 入口与任务划分
- Host（kernel.asc L436-L437）：`80<h≤96 && 原 family18 域 && 实际 UB≥156928B` → family37 / paddedH=128 / UB156928B，入口 `sinkhornnorm_staged96_fused_factor`。
- P40 满核，每核 3–4 张矩阵（本地 N128；平台 N96 时 2–3 张）；每 token 在 matrix↔transposed 双缓冲间互换，无跨核同步。

### 数据布局
- pitch=128、hp=128（状态/因子空间），**计算域 96 物理行**（88 真实 + 8 dummy）：padding 为块对角——第 88..95 行只有对角元 1.0、其余 0，且真实输入 DMA 与输出缩放都不碰 dummy（Init 用 scalar SetValue 一次置好，L8966-L8969）。
- UB 三区共 156,928B = storage 58,368（因子/分母/广播/矩阵 C）＋ transpose 49,152（Cᵀ）＋ work 49,408（工作区 + 4096 预取尾），与记录口径 58368+49152+49408 一致。

### 算法流水
1. gate：`Muls(−1)→Exp→Adds(+1)→Div(1/·)`，pre +ε、post ×2，即算即出（L9142-L9148）。
2. 初始 softmax（L9155-L9184）：RowStatistic 两段——前 64 列整块拷贝 + 真尾 24 列折叠 Max → 两级 BlockReduceMax → Brcb → Sub 平移 → Exp → RowStatistic(false) 行和 S → 预除 1/S → `Muls(ε·S)` → `Add(E, ε·S)` 得 C=E+εS。
3. **因子递推主循环**（L9080-L9117，`Padded96SyncIterationLoop<88/96>`，与已资格 H128 叶同一编译前缀）：行/列因子沿 C、Cᵀ 两个常量方向交替做 vmla 加权行和（64 宽 + 24 真尾两段），分母 = dot + ε·旧分母（Axpy），因子 = 1/分母（Div）；三个 128B 不相交的分母向量轮换角色，零张量拷贝。
4. 收尾：Brcb 广播行因子 → Mul(matrix, rowFactor) → Mul(matrix, colFactor) 物化 comb → DataCopyPad 输出。

### IO 流水
- 首 token：gate + 矩阵各一条 DataCopyPad；后续 token：前 32 行预取进「已死」的 Cᵀ（4096 float 单 DataCopy）＋后 56 行 DataCopyPad，与当前计算重叠；gate 预取进 storage 别名区。
- 输出等待全部延后到别名区真正被覆盖前；上一张的 comb store 由下一张 softmax 的延后 fence 兜底（L9186-L9189）。

### 关键优化
1. **compact_fused（506f98e0，本地 −9.3%）**：尾乘法只读真实补齐后的 24/32 列；计算行按 8 行容量域选 88/96；两个常量方向都裁到 96 物理行（pitch 仍 128）。
2. **transpose_stage（12bd2c6e，本地 −2.5%）**：初始转置改为 16 行 × 136 float 暂存 + `TransDataTo5HD` 硬件转置 + 回拷，6 段完成 96 行（32 个 VA 指针预置，L8952-L8956、L9022-L9032）。
3. **bank 相位旋转**：rowFactor/colFactor 起始地址按 `((desired+16−group)%16)*8` 错开，避免因子流与矩阵流的 bank 组冲突（L8944-L8949）。
4. **ε 折进分母递推**：M=A/(u·v) 表示下，分母更新 = dot + ε·旧分母，且旧分母向量直接复用为下一次 dot 缓冲（UpdateFactor，L9042-L9051）。
5. ReuseReciprocal：先除一次得 1/分母再乘（省每行重复 Div）；输入预取 + 输出延后等待自父版继承。

### 成绩与瓶颈
- 本地 N128/I20 完整 Task 65.12µs（1.1328×）；平台 P4 = **57.31µs / TBest 40.94µs**（本地 N128 比真实 N96 高估 ≈28%）。
- PMU/仿真：Vector 43.3µs，其中**主循环 40.6µs 占 Vector 区间 75.9%**——瓶颈是矩阵读取与反馈依赖的串行链，不是 DMA；因此后续结构筛选都冲着「改矩阵读取/反馈安排」去，而不是继续压表面 repeat/API 数。
- 后续版本备注（本文不展开）：h88-resident 线的 whole_io→eps_ready→feedback_drain→compact_owners（平台 P4 45.81µs）；最新 60.76 基座 b23502a5（平台 P4 44.96µs，H88 叶未改自 C5）。

---

## 三 case 速查

| case | 形状 | 实现方案 | 平台成绩（历史窗口） | 当时 TBest |
|---|---|---|---|---|
| case2 / p2 | H5·I1·N1 | H5C 紧凑叶 `purevec140_raw2`（72967d8a） | 1.39µs（破榜） | 1.41µs |
| case3 / p3 | H22·I20·N26 | alignedbias32 稠密驻留（v115 默认同叶） | 9.46–9.90µs | 7.19µs |
| case4 / p4 | H88·I20·N96 | Staged96FusedFactor（6cce644c） | 57.31µs | 40.94µs |

跨时分数/时间不能直接互比（平台与本地均如此）；本地 Task 排序也不预测平台（p2 已有反例）。
