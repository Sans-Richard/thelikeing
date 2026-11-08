# SinkhornNorm 当前 shape 表与核验记录

更新时间：2026-11-04 18:26:15 CST

本文件以用户于2026-11-04上传的同学截图作为 H / iters / N 的当前优先资料；用户明确要求与旧文档冲突时以截图为准。截图补充 H1–H10 十组资料，p1–p5 与本文件原有五个可见 case 的 H、iters、N 全部一致，没有需要替换的公开点数值。图片属于用户提供的选手资料，不标作官方直接公布或我方本次重新探测的结果。

## 0. 用户截图优先表（2026-11-04）

- 图片原件：[shape_peer_20261104.png](/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_help234_exec_4_4_6_merge4_20261104/selection_20261104/input/shape_peer_20261104.png)，SHA256=`509dd5764c3351c1dae01268a25c0143a5216de3e89992a912ec54af506d1123`。
- 逐行转录与核对：[shape_transcription.json](/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_help234_exec_4_4_6_merge4_20261104/selection_20261104/shape_transcription.json)。
- 图片首列“点 / H”中的 `H1 / 100` 表示编号 H1 的 H=100，不能把编号 H1 当成矩阵高度1；第二列“当前I”记录迭代次数，`N=B×S`。
- 截图的“当前N证据”与“manifest本地代表N”在15行逐项相等。这里的manifest数值按截图转录；本次未取得同学原始manifest或共享报告，不能写成已经核验这些原件。

| 图片编号 | H / hc_mult | iters / I | 当前 N=B×S | manifest 本地代表 N | 图片所标来源 |
|---|---:|---:|---:|---:|---|
| H1 | 100 | 20 | 768 | 768 | 共享报告精确 |
| H2 | 2 | 2 | 1048576 | 1048576 | 共享报告精确 |
| H3 | 3 | 3 | 21 | 21 | 共享报告精确 |
| H4 | 7 | 12 | 35 | 35 | 共享报告精确 |
| H5 | 9 | 20 | 899 | 899 | 共享报告精确 |
| H6 | 13 | 2 | 7936 | 7936 | 共享报告精确 |
| H7 | 56 | 10 | 384 | 384 | 共享报告精确 |
| H8 | 64 | 20 | 160 | 160 | 共享报告精确 |
| H9 | 15 | 20 | 192 | 192 | 共享报告精确 |
| H10 | 23 | 32 | 384 | 384 | main共享报告精确 |
| p1 | 128 | 15 | 896 | 896 | 共享报告精确 |
| p2 | 5 | 1 | 1 | 1 | 共享报告精确 |
| p3 | 22 | 20 | 26 | 26 | main共享报告精确 |
| p4 | 88 | 20 | 96 | 96 | main共享报告精确 |
| p5 | 34 | 20 | 256 | 256 | main共享报告精确 |

H1–H10 保留截图原编号，作为当前工作区采用的后十点资料；截图没有给出它们对应的官方 testcase ID，也没有给出与 API 后十项顺序的显式绑定，本次不自行补配。图片未给出这些行的 B/S 拆分、各点实际 eps、数值分布或 dtype。已知 N 只能直接确定展平 token 数；H1–H10 不因此获得完整 `[B,S,D]` 形状。下面保留的 p1–p5 B/S、输出形状和 testcase ID 来自既有探针证据，并非从截图反推。

截图中的 H2 为 H=2、I=2、N=1,048,576；H3 为 H=3、I=3、N=21。两者虽都属于小H，工作量相差很大；因此不能只按H选择本地代表N。所有行的数学宽度仍由 `D=H²+2H` 推导，迭代包含 `2I−1` 个行/列归一化半步；这些是算子关系，不是截图新增测量字段。

此前资料由用户提供的2026-10-24版 `SHAPE.md` 经2026-11-03探针核验更新而来；2026-10-29后 case ID 已更换。下列五个公开点的核验记录保留原有证据范围。member2探针用三个通道读取实际B/S/H/iters，并逐项通过独立校验码；FP32、实际iters、每轮eps、原生Div和全部输出计算均保持，探针仅额外等待，不作为优化版本。

## 1. p1–p5 的 B/S、形状与既有核验参数

| case | B | S | H / hc_mult | 实际 iters | N=B×S | mixes 输入形状 |
|---|---:|---:|---:|---:|---:|---|
| 1 | 7 | 128 | 128 | 15 | 896 | `[7, 128, 16640]` |
| 2 | 1 | 1 | 5 | 1 | 1 | `[1, 1, 35]` |
| 3 | 2 | 13 | 22 | 20 | 26 | `[2, 13, 528]` |
| 4 | 3 | 32 | 88 | 20 | 96 | `[3, 32, 7920]` |
| 5 | 8 | 32 | 34 | 20 | 256 | `[8, 32, 1224]` |

通用形状关系：`mixes=[B,S,H²+2H]`；`pre=[B,S,H]`；`post=[B,S,H]`；`comb=[B,S,H,H]`。输出形状由已测 B/S/H 和已核对的算子契约推导。

| case | pre / post | comb | 当前 testcase ID |
|---|---|---|---|
| 1 | `[7, 128, 128]` | `[7, 128, 128, 128]` | `6ae2fdfb1dac5d235b4b62aa` |
| 2 | `[1, 1, 5]` | `[1, 1, 5, 5]` | `6ae2fdfb1dac5d235b4b62af` |
| 3 | `[2, 13, 22]` | `[2, 13, 22, 22]` | `6ae2fdfb1dac5d235b4b62b3` |
| 4 | `[3, 32, 88]` | `[3, 32, 88, 88]` | `6ae2fdfb1dac5d235b4b62b7` |
| 5 | `[8, 32, 34]` | `[8, 32, 34, 34]` | `6ae2fdfb1dac5d235b4b62bb` |

边界：dtype=float32 来自当前算子契约及输入类型校验，本轮没有另做 dtype 编码；eps 的接口默认值为 `1e-6`，但本轮没有测定每个官方 case 实际 eps，不能将默认值写成已探测事实。输入数值分布也未由本轮探针测定。

## 2. 对旧文件的修正

| case | 旧 (B,S,H,iters) | 当前 (B,S,H,iters) | 结论 |
|---|---|---|---|
| 1 | `(7, 128, 128, 20)` | `(7, 128, 128, 15)` | iters: 20→15 |
| 2 | `(1, 1, 5, 1)` | `(1, 1, 5, 1)` | 参数相同；case ID 已更换 |
| 3 | `(2, 13, 22, 20)` | `(2, 13, 22, 20)` | 参数相同；case ID 已更换 |
| 4 | `(3, 32, 88, 20)` | `(3, 32, 88, 20)` | 参数相同；case ID 已更换 |
| 5 | `(8, 32, 34, 20)` | `(8, 32, 34, 20)` | 参数相同；case ID 已更换 |

本次测得 case4 为 B=3、S=32、H=88、iters=20，即 N=96。此前部分本地诊断使用 B=1、S=256、H=88、iters=15，那是代理负载，不能当作该官方 case 的真实参数；也不能把样例默认 iters=15 推广到全部五个 case。
旧表是历史探测结果，不能因当前表不同而断言当年的探测错误。旧官方提交发生在 2026-10-23 UTC；原文件更新时间为 2026-10-24 CST。历史证据：`/mnt/workspace/enjoy_ur_time/others/tools/probes/sinkhorn_shape_value_campaign/state.json`。旧文件部分 HISTORY/evidence 链接已随目录迁移失效，不再作为当前证据入口。

上传原件的云端原样备份：`/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_shape_revalidation_member2_20261103/input/SHAPE.original.txt`，SHA256=`2ae6c1ba652fb07d5ddd7098e62e623ad69611bd4fb08de1cc4f7584fc2ca92d`。原文件中旧预算、旧账号及后续操作建议仅为历史文字，不是本次授权。

## 3. 2026-11-03 探针核验方法与原始结果

主机入口直接读取 `info_mixes.tensors[0].shape[0/1]` 得到 B/S，H 与 iters 分别来自实际 `hc_mult`、`hc_sinkhorn_iters` 参数，而非默认值或本地代理。编码：

```text
P=(B-1) | ((S-1)<<7) | ((H-2)<<20) | ((iters-1)<<27)
D0=P&2047; D1=(P>>11)&2047; D2=(P>>22)&1023
CHECK=(17*B+31*S+13*H+23*iters)&2047
target_ticks=500000+2500*code
```

每个 kernel 入口先记系统计数器，完整执行原始计算及 TPipe 生命周期，然后等待到目标计数。50 ticks/us 对应 10000us 基底、每编码单位 50us；CAL 的 code=0 校准固定开销，逐 case 用 `(Tchannel−TCAL)/50` 四舍五入解码。三个编码通道和独立 CHECK 的残差都必须不超过 7.5us。所有 28 个设备入口被覆盖，27 处实际 launch 追加计数参数；原有未调用入口仍未调用。

五个探针各通过 149 组本地正确性、readonly、越界保护和重复确定性验证；其中 100 组与缓存 M1_A1_C2 输出逐位一致，另 49 组通过原参考容差。未重新运行基线诊断/性能套件；最终原快照恢复提交仍执行现有流程要求的官方样例门禁。五个探针的 28 个设备函数机器码逐一相同，差异仅在主机侧选择编码值。A3 本地结果只用于探针计算保持检查；下表来自 A2 官方提交。

下列时间均为 us，包含人为诊断延时，不可用于评判优化性能。每行保持同一 SID 的完整五项向量。

| 版本 | case1 | case2 | case3 | case4 | case5 | 状态 | SID |
|---|---:|---:|---:|---:|---:|---|---|
| CAL | 10008.22 | 10000.81 | 10002.54 | 10004.66 | 10003.30 | Pass | `6ae9e57f1dac5d235b235667` |
| D0 | 106310.80 | 10000.97 | 86856.08 | 106108.84 | 106357.48 | Pass | `6ae9e6a31dac5d235b25d0ea` |
| D1 | 61557.98 | 86802.34 | 10002.84 | 61257.01 | 10054.15 | Pass | `6ae9e7b71dac5d235b281e11` |
| D2 | 33957.76 | 10000.64 | 40652.45 | 41454.50 | 40803.16 | Pass | `6ae9e8be1dac5d235b2a8b4c` |
| CHECK | 110006.62 | 16800.58 | 69152.32 | 39955.53 | 111504.14 | Pass | `6ae9e9eb1dac5d235b2d260a` |

| case | D0 / D1 / D2 | 最大通道残差(us) | CHECK 实测/预期 | CHECK 残差(us) |
|---|---|---:|---|---:|
| 1 | `[1926, 1031, 479]` | 2.580 | 2000 / 2000 | -1.600 |
| 2 | `[0, 1536, 0]` | 1.530 | 136 / 136 | -0.230 |
| 3 | `[1537, 0, 613]` | 3.540 | 1183 / 1183 | -0.220 |
| 4 | `[1922, 1025, 629]` | 4.180 | 599 / 599 | 0.870 |
| 5 | `[1927, 1, 616]` | 4.180 | 2030 / 2030 | 0.840 |

探针均获整体 Pass；五个可见 case 各项 Pass，后十个 case 的 API 状态为 Hidden，该轮探针没有识别其形状。本文件第0节的H1–H10来自2026-11-04用户截图，不是上述探针的解码结果。每笔服务端全部源码文件与冻结快照逐项校验一致。

## 4. 探针任务当时的保留状态与证据入口

以下是2026-11-03形状探针任务的历史收尾：该任务期间工作区A的正式版本始终为 **M1_A1_C2**，九个源码文件及baseline.json的开始/结束哈希一致，未选择新优化版本。这不代表当前基线；2026-11-04用户已选择 **A3_T2b_compact_output**（kernel SHA `c01e3f2c6fc54a7d1fd29a058c8486dcf7891fa626e65ae7d2ae0328f89e798d`），当前权威指针为 [workspace_control/baseline.json](../workspace_control/baseline.json)。

- kernel SHA256：`50440a3b8468f91f44c6212a2ed6a6d88566c5c58a068d6dafe0f7072cd57a38`。
- 完整工程快照：`092767eaf982ac9231b84edb59b2b4f4b4fbacc1385fc4903617ec57f03ce4a6`。
- 本次共 6 次 member2 POST，其中 5 次诊断、1 次原快照恢复提交；最短实际 POST 间隔 258.038 秒。
- 收尾恢复 SID：`6ae9eaed1dac5d235b2f61d4`，状态 Pass；只用于将 member2 最新提交恢复为无探针的 M1_A1_C2，不用于优化比较。
- 任务与原始证据：`/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_shape_revalidation_member2_20261103`。
- 当前解码及五个 case ID：`/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_shape_revalidation_member2_20261103/analysis/current_shapes.json`。
- 预注册编码协议：`/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_shape_revalidation_member2_20261103/analysis/protocol.json`。
- 逐笔提交、实际 POST 时刻及源码绑定：`/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_shape_revalidation_member2_20261103/control/submission_ledger.json`。
- 原算法保留审计：`/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_shape_revalidation_member2_20261103/analysis/static_probe_audit.json`；设备代码比较：`/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_shape_revalidation_member2_20261103/analysis/device_functions_identical.json`。
- 本地验证：`/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_shape_revalidation_member2_20261103/validation/{CAL,D0,D1,D2,CHECK}/result.json`。

本文件第1–4节的探针结论绑定上述testcase ID、源码和SID；第0节新增H1–H10绑定用户截图及其编号，二者证据来源分开记录。测试集或接口再次变化时需重新核验，不能仅凭 H 相同、耗时相近或本地代理 N 相近沿用。
