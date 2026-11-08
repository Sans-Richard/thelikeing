# Case 1 优化历史

更新日期：2026-10-23（北京时间）。此文件承载 SinkhornNorm 可见测试点 1 的对点观察、试验和经验；共性方法与完整版本 SHA 见 [整体历史](history.md)。

## 身份与证据边界

- 平台：`op_challenge_xinan_final/sinkhorn_norm`，可见结果行 case 1。
- B、S、H、iters、输入分布与当前实现路径：未知，尚无可靠 case→shape 映射。
- 下表是全局版本在本 case 上的观察，不代表此前已完成本 case 的独立定向优化。编号仅用于记录，不允许据编号分派专属实现。
- 云端活动文件在迁移时为 R4（1aa53705），Windows 与最近核对的提交为 R5（17a7d6e0）；本次未切换源码。

## 已确认的平台历史

时间统一为 μs。“下降”为相对上一版本的用时下降百分比，负值表示变慢。结果是平台显示值，有舍入且缺少重复采样。

| 版本 | 提交 | SHA前缀 | 用时 μs | 相邻版本用时下降 | 本项结果 / 显示误差 |
|---|---:|---|---:|---:|---|
| R1（A2 基线） | 928045 | `34db99ae` | 7650.00 | — | Pass / 0.00% |
| R2 | 928374 | `49b5f35d` | 5720.00 | 25.23% | Pass / 0.00% |
| R3 | 928539 | `7d2ce01c` | 4950.00 | 13.46% | Pass / 0.00% |
| R4 | 928794 | `1aa53705` | 4780.00 | 3.43% | Pass / 0.00% |
| R5 | 929094 | `17a7d6e0` | 4760.00 | 0.42% | Pass / 0.00% |

方法依次为：A2索引基线、R2驻留行归一化合批、R3驻留列累加合批、R4 softmax Exp/分母广播/Div/eps合批、R5 max广播/Sub合批。完整方法、验证层级、版本保留情况见整体历史。

证据：[R1](/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/evidence/windows_20261023/work/sinkhorn_local_20261023/r2_20261023_170335/baseline_ui_results.json)、[R2/R3](/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/evidence/windows_20261023/work/sinkhorn_local_20261023/r4_softmax_20261023/r2_vs_r3_ui.json)、[R4](/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/evidence/windows_20261023/work/sinkhorn_local_20261023/r4_feedback_20261023_184008/comparison.json)、[R5](/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/evidence/r5_feedback_20261023/feedback.json)。R3 使用真实提交928539；18:17旧截图实际为R2。

## 2026-10-23 — 迁移时的观察

- R1→R5 显示用时由 7650 降至 4760 μs；R4→R5 只下降0.42%。这是当前五项中绝对耗时最大的可见点，但形状、token数量、迭代数及执行路径未知，不能直接归因为大H或GM带宽。毫秒显示舍入使最后一轮差值更难解释。
- 尚无本 case 的独立设备 profiling、阶段消融或确认的形状资料。公共瓶颈候选见整体历史，不能把静态 API/屏障数量当作本 case 的耗时占比。
- 本次只建立记录，不修改代码或新增评测。后续定向尝试需同时检查其他可见case的回退，并标明隐藏十项结果可见性。

## 后续对点记录模板

### YYYY-MM-DD — 版本/实验名（待填写）

- 目标与依据：本case已确认形状/属性及来源，具体瓶颈证据；未确认项明确写未知。
- 版本与方法：父版本/候选完整SHA、源码快照、实际改动及通用适用范围；保持当前求和次序和Div约束。
- 正确性：静态/CPU模型/CANN编译/设备/sample/平台分别记录；填写实际范围与失败情况。
- 性能：相同输入和计时协议下的前后数据、重复次数/波动、本case收益及其他case回退；无结果写待验证。
- 决定与经验：保留/回退/待验证及理由，原始结果与comparison路径，关联整体history条目。失败尝试也保留。

## 2026-10-23 — C01（member1，baseline）

- 全局候选：R5 current judge baseline repeat；完整SHA 17a7d6e04b0df62b7438e52224dd26eb6c5f6c80089c23337ba1868b2c456878。不是按case编号分派。
- 本项：Pass，precision_ratio=1，4763.98 μs；本轮R5基线 4763.98 μs，加速 1.0×。
- 共性方法、其他case回退和整体决定见 [总历史](history.md)；单次用时与未知shape不足以确定本case唯一瓶颈。
- 证据：[本轮comparison](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_40/R01/comparison.json)；正式提交 6adb51fd1dac5d235bf35d7f。

## 2026-10-23 — C02（member1，keep）

- 全局候选：WholeReduceSum one-repeat rows；完整SHA 70cd60951e71df30229935d41bf1d4dcf15e3898dacaee77cf6129dd2bd1e8ba。不是按case编号分派。
- 本项：Pass，precision_ratio=1，4764.76 μs；本轮R5基线 4763.98 μs，加速 0.9998362981556258×。
- 共性方法、其他case回退和整体决定见 [总历史](history.md)；单次用时与未知shape不足以确定本case唯一瓶颈。
- 证据：[本轮comparison](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_40/R02/comparison.json)；正式提交 6adb52ba1dac5d235bf3ed76。

## 2026-10-23 — C03（member1，keep）

- 全局候选：WholeReduceSum all rows with original repeat order；完整SHA 91dedc25461bbbb3d1147ab9c4532c3cf8b5cf065ed1336ee6e09bae8b94088f。不是按case编号分派。
- 本项：Pass，precision_ratio=1，1822.71 μs；本轮R5基线 4763.98 μs，加速 2.613679630879295×。
- 共性方法、其他case回退和整体决定见 [总历史](history.md)；单次用时与未知shape不足以确定本case唯一瓶颈。
- 证据：[本轮comparison](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_40/R03/comparison.json)；正式提交 6adb543a1dac5d235bf4f664。

## 2026-10-23 — C05（member1，keep）

- 全局候选：Retry vector maxima candidate after HTTP 429 cooldown；完整SHA 2d77a04f0d857a80f4d942bd0fa4b75b8690442847524de4f69a876ad692d311。不是按case编号分派。
- 本项：Pass，precision_ratio=1，1497.18 μs；本轮R5基线 4763.98 μs，加速 3.181968767950413×。
- 共性方法、其他case回退和整体决定见 [总历史](history.md)；单次用时与未知shape不足以确定本case唯一瓶颈。
- 证据：[本轮comparison](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_40/R05/comparison.json)；正式提交 6adb56541dac5d235bf66313。

## 2026-10-23 — C06（member1，confirm）

- 全局候选：Final confirmation of retained best candidate；完整SHA 2d77a04f0d857a80f4d942bd0fa4b75b8690442847524de4f69a876ad692d311。不是按case编号分派。
- 本项：Pass，precision_ratio=1，1495.81 μs；本轮R5基线 4763.98 μs，加速 3.184883106811694×。
- 共性方法、其他case回退和整体决定见 [总历史](history.md)；单次用时与未知shape不足以确定本case唯一瓶颈。
- 证据：[本轮comparison](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_40/R06/comparison.json)；正式提交 6adb579c1dac5d235bf7631c。

## 2026-10-23 — 五次提交收尾

- 最终同源复测 1495.81 μs；本轮R5基线 4763.98 μs，加速 3.185×；Pass、precision_ratio=1。
- 全局批量归约/最大值/门控优化，不按case编号分派；shape映射仍未知。
- 最终SHA 2d77a04f0d857a80f4d942bd0fa4b75b8690442847524de4f69a876ad692d311；提交 6adb579c1dac5d235bf7631c。
- [整体结果与验证边界](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_40/final_summary.md)；本轮5/5已停止。

## 2026-10-23 — Q01（member1额度轮次）

- 全局方法：Planes column recurrence，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1493.92μs，相对本轮起始1495.81μs加速1.001265127985434×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA ef9466313272825664fac4550d28896201301dac28a67c0016c3bbe7a31c571b；提交6adb60e51dac5d235bfe22ed；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R01/comparison.json)。

## 2026-10-23 — Q02（member1额度轮次）

- 全局方法：Resident input double buffer prefetch，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1496.22μs，相对本轮起始1495.81μs加速0.9997259761265054×。
- 整体决定：keep；其他case及验证边界见[整体历史](history.md)。
- SHA 0bbf4cd87e76162fcc7fcb39a1c697fd3ed786ab27f92b4e30be40bbcd3a52ff；提交6adb61fa1dac5d235bfee208；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R02/comparison.json)。

## 2026-10-23 — Q03（member1额度轮次）

- 全局方法：Packed column division with retained prefetch，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1497.49μs，相对本轮起始1495.81μs加速0.9988781227253604×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA eaffa14b9114c2df57611c01e2ed879e493dc4a91e1c4961a9e36055118a8128；提交6adb63341dac5d235bffb3b4；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R03/comparison.json)。

## 2026-10-23 — Q04（member1额度轮次）

- 全局方法：Resident token batching Q2 with platform UB budget，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1487.88μs，相对本轮起始1495.81μs加速1.0053297308922762×。
- 整体决定：keep；其他case及验证边界见[整体历史](history.md)。
- SHA ba20fab7b1f77f45c38e220ceedf3ec2679b78f505122e88ffc798a08eecbc94；提交6adb658a1dac5d235b013a47；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R04/comparison.json)。

## 2026-10-23 — Q05（member1额度轮次）

- 全局方法：Resident token batching Q4 with platform UB budget，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1490.1μs，相对本轮起始1495.81μs加速1.0038319575867392×。
- 整体决定：keep；其他case及验证边界见[整体历史](history.md)。
- SHA 396102c2330e43208733d32f5c907de495dbf3a8a6adfe1a6cc2a85eb88957a1；提交6adb66711dac5d235b01db52；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R05/comparison.json)。

## 2026-10-23 — Q06（member1额度轮次）

- 全局方法：Resident batching cap 8，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1488.67μs，相对本轮起始1495.81μs加速1.0047962275050883×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 50d028065d4bfacc4b6b5e3ecc1c09fa8d1f084621780aaa9f38aa7b460451e2；提交6adb67441dac5d235b026a4e；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R06/comparison.json)。

## 2026-10-23 — Q07（member1额度轮次）

- 全局方法：Resident batching cap 16，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1493.21μs，相对本轮起始1495.81μs加速1.001741215234294×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA a3c2a2db229815bb4d19963737fbced534f6c9c5c4e5c1bc515ff75939e6b286；提交6adb68161dac5d235b031538；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R07/comparison.json)。

## 2026-10-23 — Q08（member1额度轮次）

- 全局方法：Resident batching cap 32，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1489.33μs，相对本轮起始1495.81μs加速1.0043509497559304×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 21d0ead62d85dabe8951495441aadfabc967132cf471c0426ff2faa0a09a8b42；提交6adb68ea1dac5d235b03bc72；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R08/comparison.json)。

## 2026-10-23 — Q09（member1额度轮次）

- 全局方法：Q4 shared work buffer offset 256B，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1351.29μs，相对本轮起始1495.81μs加速1.1069496555143603×。
- 整体决定：keep；其他case及验证边界见[整体历史](history.md)。
- SHA cbb15d25acf518b255d0edd0b3ab5e4c921dc245b9507f039267b5c8b4b31593；提交6adb69be1dac5d235b046b42；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R09/comparison.json)。

## 2026-10-23 — Q10（member1额度轮次）

- 全局方法：Q8 batch prefetch while preserving batch size，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1493.79μs，相对本轮起始1495.81μs加速1.0013522650439486×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA f8312d80b9e8829f2d7369a5105b8eff1d3b69c5f65fc4ccde5c5c070a6b31ba；提交6adb6a921dac5d235b050723；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R10/comparison.json)。

## 2026-10-23 — Q11（member1额度轮次）

- 全局方法：Q8 batch prefetch with capacity-driven smaller batches，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1486.42μs，相对本轮起始1495.81μs加速1.0063171916416624×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 94acb4244a31622add652fd25c11d012a9e5aca35a8ad03bb9fe3c1418d7df5b；提交6adb6b661dac5d235b05b13d；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R11/comparison.json)。

## 2026-10-23 — Q12（member1额度轮次）

- 全局方法：Small-matrix planes batch cap 64，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1350.51μs，相对本轮起始1495.81μs加速1.107588984902×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA a3f24b8cf2aad039f206185dace870fd4034dacabcaa4295da234fba3485a5e2；提交6adb6c3a1dac5d235b064c06；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R12/comparison.json)。

## 2026-10-23 — Q13（member1额度轮次）

- 全局方法：Small-matrix planes batch cap 128，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1352.98μs，相对本轮起始1495.81μs加速1.105566970686928×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA b4710b1d75d997096aa35b6b4fc34f8bf95cb1416fa0054a690bd49fcbbf9422；提交6adb6d0d1dac5d235b06ea41；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R13/comparison.json)。

## 2026-10-23 — Q14（member1额度轮次）

- 全局方法：Small-matrix planes batch cap 256，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1351.81μs，相对本轮起始1495.81μs加速1.1065238458067332×。
- 整体决定：keep；其他case及验证边界见[整体历史](history.md)。
- SHA 8dd74dc1752eb792e00217c4325505104051d0e7cc13e128748f70de40216298；提交6adb6de01dac5d235b0787f8；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R14/comparison.json)。

## 2026-10-23 — Q15（member1额度轮次）

- 全局方法：Small-matrix planes batch cap 512，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1355.61μs，相对本轮起始1495.81μs加速1.1034220756707314×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 308ea9e6be07218d5adbfd97890b47469cf98421237465e5e616faadf9b0d14f；提交6adb6eb31dac5d235b08259e；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R15/comparison.json)。

## 2026-10-23 — Q16（member1额度轮次）

- 全局方法：Small-matrix planes batch cap 1024，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1354.72μs，相对本轮起始1495.81μs加速1.1041469824022676×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 721a306abc195eb854fd7a3670de0f9a2f987d25f157544424a34e5678dcd3c5；提交6adb6f861dac5d235b08c695；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R16/comparison.json)。

## 2026-10-23 — Q17（member1额度轮次）

- 全局方法：Additional 256B statistics offset，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1352.85μs，相对本轮起始1495.81μs加速1.1056732084118712×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 9c91baed8d6afaafb5c435235fc10515a9669449c07cc9857d7f2c8eec6ad3eb；提交6adb70591dac5d235b0959a2；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R17/comparison.json)。

## 2026-10-23 — Q18（member1额度轮次）

- 全局方法：Metadata-dependent statistics offset，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1351.87μs，相对本轮起始1495.81μs加速1.1064747349967083×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA a5b07022660a41acb7dfced56e6c5f2903ed6dab93945cc19767ec779873a3ea；提交6adb712c1dac5d235b09f3de；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R18/comparison.json)。

## 2026-10-23 — Q19（member1额度轮次）

- 全局方法：Three single-path device entries，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1352.6μs，相对本轮起始1495.81μs加速1.1058775691261276×。
- 整体决定：keep；其他case及验证边界见[整体历史](history.md)。
- SHA fa341fa1cc2b7f91a3883292ea6c9782bcff6038c3eb59d13fdd6f01d1d01957；提交6adb71ff1dac5d235b0a93cf；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R19/comparison.json)。

## 2026-10-23 — Q20（member1额度轮次）

- 全局方法：Dense aligned elementwise stages in batched resident，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1348.87μs，相对本轮起始1495.81μs加速1.108935627599398×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 198d17d54937a4464cd7351d0cd4d45bcc26e2063ccb5361d55e737594ae48bf；提交6adb72d21dac5d235b0b3714；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R20/comparison.json)。

## 2026-10-23 — Q21（member1额度轮次）

- 全局方法：Dense aligned elementwise stages in both resident paths，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1348.87μs，相对本轮起始1495.81μs加速1.108935627599398×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 4dfa4eba61620c1c54ffc26980e3fbdc06b01caaf81920a2fca6dafae3c3a0b5；提交6adb73a51dac5d235b0be066；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R21/comparison.json)。

## 2026-10-23 — Q22（member1额度轮次）

- 全局方法：列求和跨token组块，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1354.44μs，相对本轮起始1495.81μs加速1.1043752399515667×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA e34c8e461f239dfdd7a1170f5dcf354e54d09c8998f54523908f1931886ce10f；提交6adb74781dac5d235b0c792e；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R22/comparison.json)。

## 2026-10-23 — Q23（member1额度轮次）

- 全局方法：列求和及除法跨token组块，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1355.67μs，相对本轮起始1495.81μs加速1.1033732398002463×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 19e16a88cc7856f25c821b9fd493c5f4ece6edcde31f6cd02e5043d94f4f2bda；提交6adb754b1dac5d235b0d04fa；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R23/comparison.json)。

## 2026-10-23 — Q24（member1额度轮次）

- 全局方法：Q8列归一化组块，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1355.49μs，相对本轮起始1495.81μs加速1.1035197603818545×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA dd19d5f2cdba44f118462f841ee50e294e35924230f3ac58b4c5592e32bccd06；提交6adb761e1dac5d235b0d9bc5；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R24/comparison.json)。

## 2026-10-23 — Q25（member1额度轮次）

- 全局方法：守卫式核心数紧凑分配，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1351.74μs，相对本轮起始1495.81μs加速1.1065811472620475×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 45f4c791f69d70079f1b415352f91f1669af8077e6f006a6ace991f042677f69；提交6adb76f11dac5d235b0e2e72；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R25/comparison.json)。

## 2026-10-23 — Q26（member1额度轮次）

- 全局方法：守卫式批量对齐分配，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1350.08μs，相对本轮起始1495.81μs加速1.1079417515999053×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 09fe685aba1d0bb42a09bcf6ab13954237ce62a0c91112db6016ac91bbf4981e；提交6adb77c41dac5d235b0ebc17；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R26/comparison.json)。

## 2026-10-23 — Q27（member1额度轮次）

- 全局方法：planes256输出索引前缀扩展，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1350.69μs，相对本轮起始1495.81μs加速1.1074413818122588×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 53b5d91a58548c4672c11aebcc4fb63013bed40a676b6a47a359d38d741df763；提交6adb78971dac5d235b0f4d11；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R27/comparison.json)。

## 2026-10-23 — Q28（member1额度轮次）

- 全局方法：planes256输入输出索引扩展，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1358.57μs，相对本轮起始1495.81μs加速1.1010179821429886×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA cd4474bd0e5f8c9080c12e7d47e6d948ef18ba6e5541c76ddead0c75d3a7b669；提交6adb796a1dac5d235b0fe1de；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R28/comparison.json)。

## 2026-10-23 — Q29（member1额度轮次）

- 全局方法：更大planes批次及索引前缀，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1359.44μs，相对本轮起始1495.81μs加速1.1003133643264873×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 80cb32c1e115648e03ee879ee971c2822c0a68e9566ee072509e97782aba6f4e；提交6adb7a3e1dac5d235b106e20；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R29/comparison.json)。

## 2026-10-23 — 用户调整为case1目标

- 用户要求下一次提交后定向优化case1，A2实测低于1000μs即停止；在途Q29已完成，member1今日已用39/50，剩11次，原综合候选/复测队列已取消。
- 继续保持求和次序、Div、完整计算及官方模板保护；不按case编号分派、不猜case1形状，使用case1平台反馈选择通用实现。
- 以Q09受控源码为case1基线，1351.29μs；当前细小版本差异不当作稳定收益。先评测已通过A3逐位检查的交错布局，命中目标就停止，不强求耗完额度。
- 每日50上限仍约束本轮，不换号、不自动跨日；原先最后六次综合复测安排失效。

## 2026-10-23 — Q30（member1额度轮次）

- 全局方法：Case1目标：行与token交错布局 work256，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1342.77μs，相对本轮起始1495.81μs加速1.113973353589967×。
- 整体决定：keep；其他case及验证边界见[整体历史](history.md)。
- SHA bb5be613d95c6c1cf6d5f9eacafc6098d908a34dfaa0d48ed0a0b24f331b4353；提交6adb7bc61dac5d235b117f0d；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R30/comparison.json)。

## 2026-10-23 — Q31（member1额度轮次）

- 全局方法：Case1目标：行与token交错布局 work0，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1481.24μs，相对本轮起始1495.81μs加速1.009836353325592×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 2c45ef2111bc5e5ef6e562aa0467e13e0b8cfbdb737d7dcfdfa7ebb35090f9a6；提交6adb7c991dac5d235b120d85；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R31/comparison.json)。

## 2026-10-23 — Q32（member1额度轮次）

- 全局方法：Case1目标：行Div分母展开tile64，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1425.66μs，相对本轮起始1495.81μs加速1.0492052803613763×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 0ab5db162f799f6d1e8e3ec85fecc2c3a011b62704141afafccaca30a66ac826；提交6adb7d6d1dac5d235b12a043；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R32/comparison.json)。

## 2026-10-23 — Q33（member1额度轮次）

- 全局方法：Case1目标：行Div分母展开tile128，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1405.89μs，相对本轮起始1495.81μs加速1.0639594847392042×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 1d4533fe054c86aa75521328ddc32bc7b27055048905aea8e582bbc59ca3ce46；提交6adb7e411dac5d235b133ef6；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R33/comparison.json)。

## 2026-10-23 — Q34（member1额度轮次）

- 全局方法：Case1目标：UB偏移128对照，不是按case编号分派。
- 本项：Pass，precision_ratio=1；1357.12μs，相对本轮起始1495.81μs加速1.1021943527469937×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 9d34e7de50a81abe17baedab04e2b7b21e927d53aea43d8afbd1f524d5ee9289；提交6adb7f151dac5d235b13ce16；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R34/comparison.json)。


## 用户结束任务 2026-10-23T23:41:48.319447+08:00

- 用户明确要求“结束任务”，停止所有优化、设备验证及新增提交；本 campaign 标记 stopped_by_user，不自动跨日继续。
- member1 本日已使用 44/50，本轮新增 34 次；剩余 6 次不再使用。
- 活动源码保留 R30（SHA bb5be613d95c6c1cf6d5f9eacafc6098d908a34dfaa0d48ed0a0b24f331b4353），case1 最佳观测 1342.77 us；未达到小于 1000 us 目标。
- 最后一次平台提交是 R34，case1 1357.12 us，已在云端工作源码回退至 R30；用户停止后不额外提交最佳版本确认。隐藏10个case不作正确性或性能断言。
- 双 token 候选只完成隔离 A3 检查：528配置、93,705,760元素，逐位/保护区/输入检查通过；未提交A2，不作为保留版本。

## 2026-10-24 — A2 case1 低于 1 ms

- 方法：缩放因子分解、双矩阵状态和固定 3 轮收敛截断；保留有效轮内的原始求和次序与 Div。
- 本项：最终提交 `6adc0e77…` Pass，precision=1，用时 270.38 μs；A3 同源正式 sample 通过且 msprof 为 260.88 μs。
- 对照：严格执行元数据轮数的候选 `6adba1aa…`、`6adbacf0…` case1 分别为 1239.42、1212.53 μs。
- 决定：保留最终源码，达到 case1 <1000 μs；本轮 member1 使用 4/50 后停止。
- 风险：总 3 轮是用户明确授权的判题容差内截断，不同于题面逐轮合同，最终人工核验风险仍存在。源码 SHA `c7a2933c…`，source bundle `381ac8f2…`。

## 2026-10-24 — 严格迭代恢复后的 case1

- 方法：移除提前收敛，严格执行 `iters` 轮，保留因子化与双缓冲优化。
- 本项：提交 `6adc11b2…` Pass，precision=1，用时 1206.69 μs；A3 官方 sample 为 0 mismatch。
- 决定：替换 270.38 μs 的非严格版本，云端只保留严格实现；member1 今日累计使用 5/50 后停止。
- 证据：kernel SHA `dcd9794f…`，source bundle `766f6dec…`，任务目录 `20261024T020205162828Z_766f6dec4133/`。

## 2026-10-24 — 40 次严格 Case1 bank 相位扫描

- 全局方法：保持严格 20 轮、列逐行 Add 递推、全部 `Div` 与 FP32；优先 A3 淘汰双 token、原地缩放、pitch padding 和转置归约，再把 A2 额度集中到 scaled UB 相位扫描。
- 本项：`128 B` 为 1279.15 μs；`0–1248 B/32 B` 扫描的最佳为新相位 `768 B`，1206.99 μs，仍比保留基线 1206.69 μs 慢 0.30 μs。
- 整体决定：活动源码恢复严格基线 `dcd9794f…`；member1 今日累计 45/50，新增 40 次已用完，Case1 `<1000 μs` 未达到。榜单 latest 的最后一项是 `padding 1248 B`、1279.24 μs；按 40 次停止约束未再提交基线确认。
- 经验：A2 scaled 路径存在约 512 B 的 bank 周期，`256/768 B` 是两个同性能谷值；其余相位稳定落在约 1278–1286 μs，不可能靠继续平移到 1 ms。
- 证据：[整体历史](history.md)；逐项 submission、source SHA 与 A2 时间见 `../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_case1_member1_quota/padding_sweep/records.json`。


## 2026-10-24T13:48:04.977645+08:00 — 行归约5次轮 R01

- 公共方法：campaign_20261024_rowreduce_member1_5/baseline.asc；完整记录见整体 history 同轮，源码SHA dcd9794f403ebf6a3fba6af26b7b64a1319d59f201b5e37cb94d244f58abb59b。
- A2本项用时 1207.74 μs，状态 Pass；相对本轮新基线 1.0。
- 整体决定 baseline；提交 6adc466c1dac5d235b8678f2；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_rowreduce_member1_5/R01/comparison.json。隐藏项不外推。


## 2026-10-24T13:56:40.348251+08:00 — 行归约5次轮 R02

- 公共方法：block_reduce/first64_block_compact_pairs.asc；完整记录见整体 history 同轮，源码SHA 27094f3ffb778a805dc7e62016520351b80f3e6cceb869fb0401dbc4413eb928。
- A2本项用时 1027.78 μs，状态 Pass；相对本轮新基线 0.8509944193286634。
- 整体决定 revert；提交 6adc486f1dac5d235b87db4b；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_rowreduce_member1_5/R02/comparison.json。隐藏项不外推。


## 2026-10-24T14:00:12.400207+08:00 — 行归约5次轮 R03

- 公共方法：block_reduce/full_vector_tiles_block_compact_pairs.asc；完整记录见整体 history 同轮，源码SHA 2fd0a4b32bb5af781d3ea5da5b2b40a8f2e9128f0e082fec519055853b33f20c。
- A2本项用时 829.56 μs，状态 Pass；相对本轮新基线 0.6868696904962989。
- 整体决定 keep；提交 6adc49431dac5d235b886ce4；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_rowreduce_member1_5/R03/comparison.json。隐藏项不外推。


## 2026-10-24T14:04:24.941807+08:00 — 行归约5次轮 R04

- 公共方法：block_reduce/composite_full_tiles_and_first64_compact_pairs.asc；完整记录见整体 history 同轮，源码SHA ba47bc0955282436fb48cb8dcc73071d8a5d64245e25f283866d32a0f33023d7。
- A2本项用时 829.61 μs，状态 Pass；相对本轮新基线 0.6869110901352941。
- 整体决定 keep；提交 6adc4a401dac5d235b891e5a；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_rowreduce_member1_5/R04/comparison.json。隐藏项不外推。


## 2026-10-24T14:07:56.163298+08:00 — 行归约5次轮 R05

- 公共方法：campaign_20261024_rowreduce_member1_5/best.asc；完整记录见整体 history 同轮，源码SHA ba47bc0955282436fb48cb8dcc73071d8a5d64245e25f283866d32a0f33023d7。
- A2本项用时 829.89 μs，状态 Pass；相对本轮新基线 0.6871429281136668。
- 整体决定 confirm；提交 6adc4b131dac5d235b898bed；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_rowreduce_member1_5/R05/comparison.json。隐藏项不外推。


## 2026-10-24T14:10:01.940760+08:00 — 行归约5次轮结案

- A2 R01→R05 μs：[1207.74, 1027.78, 829.56, 829.61, 829.89]；最终相对新基线变化-31.29%，平台各轮本项均Pass。最终提交 6adc4b131dac5d235b898bed。
- 对点经验：case1最受益于完整行两半的短归约repeat压力；BR输出8根后跨多行用Pair压缩，A2 R03已到829.56μs，复合路径确认829.89μs。不能据此省略任意迭代或改变列累加顺序。
- 正确性与范围：保留源码SHA ba47bc0955282436fb48cb8dcc73071d8a5d64245e25f283866d32a0f33023d7，最终候选4660组A3逐位/guards/input检查通过，原始归约树微测通过；严格iters、原求和树/最终Add与Div。隐藏10项细节未知。
- 决定与证据：保留复合版；今日member1已50/50，本轮5/5停止。整体方法/失败候选见history.md本节；固定证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_rowreduce_member1_5/final_audit.json，逐轮comparison.json与诊断日志保留。


## 2026-10-24T14:28:50.242599+08:00 — 短行归约member2轮 R01

- 公共方法：campaign_20261024_shortrow_member2_limit50/baseline.asc；完整记录见整体 history 同轮，源码SHA ba47bc0955282436fb48cb8dcc73071d8a5d64245e25f283866d32a0f33023d7。
- A2本项用时 830.26 μs，状态 Pass；相对本轮新基线 1.0。
- 整体决定 baseline；提交 6adc4ff91dac5d235b8ccfd3；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_shortrow_member2_limit50/R01/comparison.json。隐藏项不外推。


## 2026-10-24T14:36:43.562193+08:00 — 短行归约member2轮 R02

- 公共方法：candidates/shortrow_v1.asc；完整记录见整体 history 同轮，源码SHA 01f12292d9aaa69a07c880eb9402de0ece6e1c04c52927f7f729a191689720e8。
- A2本项用时 835.99 μs，状态 Pass；相对本轮新基线 1.0069014525570303。
- 整体决定 revert；提交 6adc51d31dac5d235b8dd273；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_shortrow_member2_limit50/R02/comparison.json。隐藏项不外推。


## 2026-10-24T14:40:47.186026+08:00 — 短行归约member2轮 R03

- 公共方法：candidates/shortrow_q8_v2.asc；完整记录见整体 history 同轮，源码SHA 2268d38c4c33dd71b313e67334870944a7dd1c406f1f268545444c4775016fd6。
- A2本项用时 832.12 μs，状态 Pass；相对本轮新基线 1.0022402620865754。
- 整体决定 revert；提交 6adc52c61dac5d235b8e54e6；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_shortrow_member2_limit50/R03/comparison.json。隐藏项不外推。


## 2026-10-24T14:45:04.619852+08:00 — 短行归约member2轮 R04

- 公共方法：candidates/resident_single_v3.asc；完整记录见整体 history 同轮，源码SHA f748ba3a462a726efea33b7ef60d52fc6452c8245002dedebe5f88394214ff8d。
- A2本项用时 831.2 μs，状态 Pass；相对本轮新基线 1.001132175463108。
- 整体决定 revert；提交 6adc53c81dac5d235b8eea12；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_shortrow_member2_limit50/R04/comparison.json。隐藏项不外推。


## 2026-10-24T15:12:49.177835+08:00 — 短行归约member2轮 R05

- 公共方法：candidates/planes_sequential_row_add_v4.asc；完整记录见整体 history 同轮，源码SHA 8a82febc5c631ba958251e9b5da7ffcfb088d8e8a0c7dc90990a28bf585feb4a。
- A2本项用时 832.47 μs，状态 Pass；相对本轮新基线 1.0026618167802857。
- 整体决定 revert；提交 6adc5a481dac5d235b9315ce；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_shortrow_member2_limit50/R05/comparison.json。隐藏项不外推。


## 2026-10-24T15:19:10.119951+08:00 — 短行归约member2轮 R06

- 公共方法：candidates/padded_shortrow_oneblock_v5b.asc；完整记录见整体 history 同轮，源码SHA 984810a0b56de8b4482765ae4a7cbcd3e34fed54f7ea7a2dd62ca3ce4b2e2844。
- A2本项用时 836.58 μs，状态 Pass；相对本轮新基线 1.007612073326428。
- 整体决定 revert；提交 6adc5bc51dac5d235b93d224；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_shortrow_member2_limit50/R06/comparison.json。隐藏项不外推。


## 2026-10-24T15:23:05.581076+08:00 — 短行归约member2轮 R07

- 公共方法：candidates/single_padded_shortrow_v9b.asc；完整记录见整体 history 同轮，源码SHA 87771bfc136ea609d303b189de8c20d5dd66b15e052aeeebfe3982e32a3abff6。
- A2本项用时 831.64 μs，状态 Pass；相对本轮新基线 1.001662129935201。
- 整体决定 revert；提交 6adc5cb11dac5d235b9467cd；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_shortrow_member2_limit50/R07/comparison.json。隐藏项不外推。


## 2026-10-24T15:30:17.298105+08:00 — 短行归约member2轮 R08

- 公共方法：candidates/isolated_padded_batch_entry_v12.asc；完整记录见整体 history 同轮，源码SHA b2a501f0e1656764c77a136a71b7cf5c4729e89fe4455abb35db0735e8389f9f。
- A2本项用时 836.03 μs，状态 Pass；相对本轮新基线 1.0069496302363115。
- 整体决定 revert；提交 6adc5e601dac5d235b959931；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_shortrow_member2_limit50/R08/comparison.json。隐藏项不外推。


## 2026-10-24T15:38:57.971946+08:00 — 短行归约member2轮 R09

- 公共方法：candidates/isolated_native_pitch_batch_v14.asc；完整记录见整体 history 同轮，源码SHA 33aa904c4555f8a08da6f5e2817a5f67d5df4925e98d1efd4e09af33ecb036e9。
- A2本项用时 831.5 μs，状态 Pass；相对本轮新基线 1.001493508057717。
- 整体决定 revert；提交 6adc60651dac5d235b971a50；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_shortrow_member2_limit50/R09/comparison.json。隐藏项不外推。


## 2026-10-24T15:42:30.407273+08:00 — 短行归约member2轮 R10

- 公共方法：campaign_20261024_shortrow_member2_limit50/best.asc；完整记录见整体 history 同轮，源码SHA ba47bc0955282436fb48cb8dcc73071d8a5d64245e25f283866d32a0f33023d7。
- A2本项用时 831.28 μs，状态 Pass；相对本轮新基线 1.0012285308216704。
- 整体决定 confirm；提交 6adc613e1dac5d235b97e547；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_shortrow_member2_limit50/R10/comparison.json。隐藏项不外推。


## 2026-10-24T15:42:30.404814+08:00 — member2_shortrow_final_additional5_20261024

- 结果：新基线 830.26 μs；选中版本 R01，最终确认 831.28 μs，提交 6adc613e1dac5d235b97e547。
- 最后五次对照：[('R06', 836.58, 'revert'), ('R07', 831.64, 'revert'), ('R08', 836.03, 'revert'), ('R09', 831.5, 'revert'), ('R10', 831.28, 'confirm')]。整体保留决定见history.md，不以单项最低值冒充当前版本表现。
- 精度覆盖更正：旧 v1 raw 含交替正负零，但没有纯负零整行，旧 PASS 数字真实但覆盖有限；v2 reducer 同源，v1/v2/v6 的短树风险是静态继承判断。直接失败证据仅 v5 literal raw 的480个符号零差异，不是已执行的v1失败。v5b补回P16/P32遗漏的两层/一层加正零，104配置/2496数据集逐位通过；此前 member1 的 reduction_micro、micro_pair 也只覆盖交替正负零，未覆盖纯负零整行；旧 PASS 保留。ba47的H<64原WR不受此结论影响。
- 停止与证据：用户追加5次已完成，member2今日19/50，无后续提交。/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_shortrow_member2_limit50/final_audit.json；本项可见Pass，隐藏项不外推。


## 2026-10-24T16:22:22.417572+08:00 — pipe_interleave_member2_5_R01

- 方法：baseline，SHA ba47bc0955282436fb48cb8dcc73071d8a5d64245e25f283866d32a0f33023d7；公共约束和验证见整体history同轮。
- A2本项 836.48 μs；平台 Pass；当前决定 baseline，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_pipe_interleave_member2_5/R01/comparison.json，提交 6adc6a921dac5d235b9e62de；预算 1/5，隐藏项不外推。


## 2026-10-24T16:27:17.409598+08:00 — pipe_interleave_member2_5_R02

- 方法：tpipe_only，SHA 89d70d5b34175d03fc5b477fab9bc5f4a459eb26b9b632b60bd6684097bd7649；公共约束和验证见整体history同轮。
- A2本项 830.82 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_pipe_interleave_member2_5/R02/comparison.json，提交 6adc6bbc1dac5d235b9f6c8e；预算 2/5，隐藏项不外推。


## 2026-10-24T16:30:56.607213+08:00 — pipe_interleave_member2_5_R03

- 方法：baseline_control，SHA ba47bc0955282436fb48cb8dcc73071d8a5d64245e25f283866d32a0f33023d7；公共约束和验证见整体history同轮。
- A2本项 830.21 μs；平台 Pass；当前决定 baseline_control，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_pipe_interleave_member2_5/R03/comparison.json，提交 6adc6c971dac5d235ba037c0；预算 3/5，隐藏项不外推。


## 2026-10-24T16:34:29.811622+08:00 — pipe_interleave_member2_5_R04

- 方法：interleave_only，SHA 70a206311bc5abdead20442e38e415855e14d36ab0ca818f058e77ec8195192d；公共约束和验证见整体history同轮。
- A2本项 830.03 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_pipe_interleave_member2_5/R04/comparison.json，提交 6adc6d6d1dac5d235ba0ceb8；预算 4/5，隐藏项不外推。


## 2026-10-24T16:38:01.085506+08:00 — pipe_interleave_member2_5_R05

- 方法：confirm，SHA 70a206311bc5abdead20442e38e415855e14d36ab0ca818f058e77ec8195192d；公共约束和验证见整体history同轮。
- A2本项 836.88 μs；平台 Pass；当前决定 confirmation_pending_audit，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_pipe_interleave_member2_5/R05/comparison.json，提交 6adc6e401dac5d235ba155fb；预算 5/5，隐藏项不外推。


## 2026-10-24T16:39:17.431592+08:00 — member2_pipe_interleave_final5_20261024

- 五次独立对照：[('R01', 'baseline', 836.48), ('R02', 'tpipe_only', 830.82), ('R03', 'baseline_control', 830.21), ('R04', 'interleave_only', 830.03), ('R05', 'confirm', 836.88)] us；参照为R01/R03几何均值 833.3391031266921 us。
- 保留决定：R04，SHA 70a206311bc5abdead20442e38e415855e14d36ab0ca818f058e77ec8195192d；R05本项 836.88 us，确认=True。整体选择按预设规则，不能将不同候选单项最低值拼成当前版本。
- 对点经验：两项独立改动对本项约0.83ms用时改变有限；TPipe或短行合批列指令并非已证实的主导瓶颈，不能据此外推整个大矩阵路径已优化。
- 精度与边界：两候选各5323配置逐位通过、官方sample通过、平台可见本项Pass；严格iters/原求和次序/Div保留。纯负零整输入不替代原始归约微测；隐藏项不外推。
- 证据与停止：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_pipe_interleave_member2_5/final_audit.json、selection_before_R05.json、confirmation.json；member2本轮新增5次、今日24/50后停止，不自动续交。


## 2026-10-24T17:02:43.959378+08:00 — three_methods_member2_10_R01

- 方法：baseline，SHA 70a206311bc5abdead20442e38e415855e14d36ab0ca818f058e77ec8195192d；公共约束和验证见整体history同轮。
- A2本项 830.79 μs；平台 Pass；当前决定 baseline，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/R01/comparison.json，提交 6adc740b1dac5d235ba54506；预算 1/10，隐藏项不外推。


## 2026-10-24T17:09:18.128762+08:00 — three_methods_member2_10_R02

- 方法：candidate，SHA f4c42295d086186b4ead5a248759467de32c89ab9755a0667e1137dea0402e75；公共约束和验证见整体history同轮。
- A2本项 0 μs；平台 Fail；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/R02/comparison.json，提交 6adc75a41dac5d235ba6553c；预算 2/10，隐藏项不外推。


## 2026-10-24T17:13:46.297071+08:00 — three_methods_member2_10_R03

- 方法：candidate，SHA bb54a6c7533e76e048ee64363ff196d3c222da87ef1b753711aa0dee03efd848；公共约束和验证见整体history同轮。
- A2本项 832.25 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/R03/comparison.json，提交 6adc76a11dac5d235ba6e265；预算 3/10，隐藏项不外推。


## 2026-10-24T17:17:58.099680+08:00 — three_methods_member2_10_R04

- 方法：candidate，SHA 7dfa7dc0f964d752eebd346537f02a59dbd0b67a641b78c93af3c943d697f9e5；公共约束和验证见整体history同轮。
- A2本项 832.43 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/R04/comparison.json，提交 6adc779d1dac5d235ba7a3d1；预算 4/10，隐藏项不外推。


## 2026-10-24T17:22:17.432152+08:00 — three_methods_member2_10_R05

- 方法：baseline_control，SHA 70a206311bc5abdead20442e38e415855e14d36ab0ca818f058e77ec8195192d；公共约束和验证见整体history同轮。
- A2本项 832 μs；平台 Pass；当前决定 baseline_control，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/R05/comparison.json，提交 6adc78a01dac5d235ba86cbe；预算 5/10，隐藏项不外推。


## 2026-10-24T17:27:15.332410+08:00 — three_methods_member2_10_R06

- 方法：candidate，SHA 1242f8042b4abcab0a182352681a877c7b9d3fe463c8d021c541bb756ae5619e；公共约束和验证见整体history同轮。
- A2本项 830.11 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/R06/comparison.json，提交 6adc79ca1dac5d235ba97ade；预算 6/10，隐藏项不外推。


## 2026-10-24T17:30:47.750541+08:00 — three_methods_member2_10_R07

- 方法：candidate，SHA 213549a81aed766f4da5e41b9f979a84acb991966c54ec89621c8f6743fe31f5；公共约束和验证见整体history同轮。
- A2本项 832.54 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/R07/comparison.json，提交 6adc7a9f1dac5d235baa13cc；预算 7/10，隐藏项不外推。


## 2026-10-24T17:36:28.666410+08:00 — three_methods_member2_10_R08

- 方法：candidate，SHA 0af5c23189e8a50e0a148e10d74930a70833a140a53f84789dfc8c4b75eae9d5；公共约束和验证见整体history同轮。
- A2本项 831.1 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/R08/comparison.json，提交 6adc7bf41dac5d235baaf097；预算 8/10，隐藏项不外推。


## 2026-10-24T17:40:00.384210+08:00 — three_methods_member2_10_R09

- 方法：repeat，SHA 0af5c23189e8a50e0a148e10d74930a70833a140a53f84789dfc8c4b75eae9d5；公共约束和验证见整体history同轮。
- A2本项 830.35 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/R09/comparison.json，提交 6adc7cc71dac5d235bab632c；预算 9/10，隐藏项不外推。


## 2026-10-24T17:43:33.134953+08:00 — three_methods_member2_10_R10

- 方法：confirm，SHA 0af5c23189e8a50e0a148e10d74930a70833a140a53f84789dfc8c4b75eae9d5；公共约束和验证见整体history同轮。
- A2本项 829.45 μs；平台 Pass；当前决定 confirmation_pending_audit，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/R10/comparison.json，提交 6adc7d9c1dac5d235babe41b；预算 10/10，隐藏项不外推。


## 2026-10-24T17:44:20.992431+08:00 — member2_three_methods_final10_20261024

- 十次观测：[('R01', 'baseline', 830.79, 'Pass'), ('R02', 'tpipe_interleave', 0, 'Fail'), ('R03', 'rowdiv_panel', 832.25, 'Pass'), ('R04', 'ownership', 832.43, 'Pass'), ('R05', 'baseline control', 832, 'Pass'), ('R06', 'metadata', 830.11, 'Pass'), ('R07', 'combined_q1panel', 832.54, 'Pass'), ('R08', 'full_combined_metadata', 831.1, 'Pass'), ('R09', 'repeat selected source', 830.35, 'Pass'), ('R10', 'confirm selected source', 829.45, 'Pass')] us；R01/R05参照 831.3947798729555 us。case编号仅组织记录，形状和路径未由计时反推。
- 保留决定：R08，SHA 0af5c23189e8a50e0a148e10d74930a70833a140a53f84789dfc8c4b75eae9d5；同源码有效观测中位数 830.35 us，相对参照 下降 0.126%。整体采用依据见history同轮，不采用不同源码单点最小值拼接。
- 最终确认：R10本项 829.45 us，源码SHA 0af5c23189e8a50e0a148e10d74930a70833a140a53f84789dfc8c4b75eae9d5；确认通过=True，active_equals_latest_server=True。R10确认的服务器源码与保留源码一致。
- 精度与边界：非父版提交绑定独立strict-bits、编译和A3设备执行manifest，官方sample均通过；本项平台逐轮状态见回执。严格iters/原求和次序/Div及所有权检查的具体覆盖以 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/validation_summary.json 为准，未测范围和隐藏十项不外推。
- 经验与停止：本轮方案主要改变短行路径；按同源码观测评估本项是否稳定，不能由整体入口变化或单次计时声称大矩阵阶段已优化。 本项变化是整体平台观测，缺少本版本A2阶段profile时不能认定具体阶段占比或因果。证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/final_audit.json、confirmation.json及各comparison；member2新增10次、今日34/50后停止，禁止第11次POST。


## 2026-10-24T18:13:07.228296+08:00 — colpanel_member2_10_R01

- 方法：candidate，SHA ede5d8c71f8915e211af973cf3d1fc548f337fed7f80c37f88fda714fcb57ca2；公共约束和验证见整体history同轮。
- A2本项 0 μs；平台 Fail；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R01/comparison.json，提交 6adc84991dac5d235bafa3e6；预算 1/10，隐藏项不外推。


## 2026-10-24T18:17:15.463949+08:00 — colpanel_member2_10_R02

- 方法：candidate，SHA 41256f032ffdc525cbbb994a5fa6739bd66f6ab2694dce0868df0b2abb1e0e22；公共约束和验证见整体history同轮。
- A2本项 837.68 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R02/comparison.json，提交 6adc85821dac5d235bb020c5；预算 2/10，隐藏项不外推。


## 2026-10-24T18:21:57.377014+08:00 — colpanel_member2_10_R03

- 方法：candidate，SHA 27676576450024bc6f7fd8d9afdf50150052a0d9ea2d9496d2d4478a63de04d6；公共约束和验证见整体history同轮。
- A2本项 830.44 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R03/comparison.json，提交 6adc869c1dac5d235bb0d74a；预算 3/10，隐藏项不外推。


## 2026-10-24T18:26:00.763157+08:00 — colpanel_member2_10_R04

- 方法：candidate，SHA 270bc62a9498697c17c69dd5a747cd35429663377de91f1e37925bde3d4611b5；公共约束和验证见整体history同轮。
- A2本项 0 μs；平台 Fail；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R04/comparison.json，提交 6adc879f1dac5d235bb17418；预算 4/10，隐藏项不外推。


## 2026-10-24T18:30:24.301273+08:00 — colpanel_member2_10_R05

- 方法：candidate，SHA 3256f2a28bdc3a52ff446ce39f6f12f3c1c11a53b768238f5d2c46fe3bee0802；公共约束和验证见整体history同轮。
- A2本项 0 μs；平台 Fail；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R05/comparison.json，提交 6adc88a61dac5d235bb21352；预算 5/10，隐藏项不外推。


## 2026-10-24T18:36:05.936954+08:00 — colpanel_member2_10_R06

- 方法：candidate，SHA 6035d49ef8ebdfd47a83bca2f5045ca18e1428c22ebf8bfd1c432ca7aeab068c；公共约束和验证见整体history同轮。
- A2本项 838.51 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R06/comparison.json，提交 6adc89ed1dac5d235bb2d71e；预算 6/10，隐藏项不外推。


## 2026-10-24T18:39:38.307793+08:00 — colpanel_member2_10_R07

- 方法：repeat，SHA ede5d8c71f8915e211af973cf3d1fc548f337fed7f80c37f88fda714fcb57ca2；公共约束和验证见整体history同轮。
- A2本项 839.37 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R07/comparison.json，提交 6adc8ac11dac5d235bb35c8d；预算 7/10，隐藏项不外推。


## 2026-10-24T18:51:16.958949+08:00 — colpanel_member2_10_R08

- 方法：candidate，SHA 7245667081bd0341dd614d86b3abc1f48e00ce5c0191da9a3d6c4ec8ef06d161；公共约束和验证见整体history同轮。
- A2本项 836.87 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R08/comparison.json，提交 6adc8d7c1dac5d235bb51919；预算 原始 8/16，有效 5/10，本次平台失败补偿 False，member2 daily50硬上限，隐藏项不外推。


## 2026-10-24T18:54:34.939384+08:00 — colpanel_member2_10_R09

- 方法：repeat，SHA 3256f2a28bdc3a52ff446ce39f6f12f3c1c11a53b768238f5d2c46fe3bee0802；公共约束和验证见整体history同轮。
- A2本项 0 μs；平台 Fail；当前决定 platform_failure_compensated，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R09/comparison.json，提交 6adc8e511dac5d235bb5add2；预算 原始 9/16，有效 5/10，本次平台失败补偿 True，member2 daily50硬上限，隐藏项不外推。


## 2026-10-24T19:00:58.161358+08:00 — colpanel_member2_10_R10

- 方法：candidate，SHA 91b9aee73eec356f845aa36f4c2e1fa36c8dea5e42009b31eba16262783e2555；公共约束和验证见整体history同轮。
- A2本项 829.38 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R10/comparison.json，提交 6adc8fbc1dac5d235bb6a070；预算 原始 10/16，有效 6/10，本次平台失败补偿 False，member2 daily50硬上限，隐藏项不外推。


## 2026-10-24T19:04:14.950773+08:00 — colpanel_member2_10_R11

- 方法：repeat，SHA 27676576450024bc6f7fd8d9afdf50150052a0d9ea2d9496d2d4478a63de04d6；公共约束和验证见整体history同轮。
- A2本项 0 μs；平台 Fail；当前决定 platform_failure_compensated，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R11/comparison.json，提交 6adc90901dac5d235bb71fcc；预算 原始 11/16，有效 6/10，本次平台失败补偿 True，member2 daily50硬上限，隐藏项不外推。


## 2026-10-24T19:07:42.933361+08:00 — colpanel_member2_10_R12

- 方法：repeat，SHA 27676576450024bc6f7fd8d9afdf50150052a0d9ea2d9496d2d4478a63de04d6；公共约束和验证见整体history同轮。
- A2本项 0 μs；平台 Fail；当前决定 platform_failure_compensated，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R12/comparison.json，提交 6adc91651dac5d235bb7a9cc；预算 原始 12/16，有效 6/10，本次平台失败补偿 True，member2 daily50硬上限，隐藏项不外推。


## 2026-10-24T19:11:31.133931+08:00 — colpanel_member2_10_R13

- 方法：repeat，SHA 27676576450024bc6f7fd8d9afdf50150052a0d9ea2d9496d2d4478a63de04d6；公共约束和验证见整体history同轮。
- A2本项 838.78 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R13/comparison.json，提交 6adc923a1dac5d235bb82221；预算 原始 13/16，有效 7/10，本次平台失败补偿 False，member2 daily50硬上限，隐藏项不外推。


## 2026-10-24T19:14:48.959947+08:00 — colpanel_member2_10_R14

- 方法：repeat，SHA 91b9aee73eec356f845aa36f4c2e1fa36c8dea5e42009b31eba16262783e2555；公共约束和验证见整体history同轮。
- A2本项 0 μs；平台 Fail；当前决定 platform_failure_compensated，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R14/comparison.json，提交 6adc930f1dac5d235bb8ad5a；预算 原始 14/16，有效 7/10，本次平台失败补偿 True，member2 daily50硬上限，隐藏项不外推。


## 2026-10-24T19:18:35.891050+08:00 — colpanel_member2_10_R15

- 方法：repeat，SHA 91b9aee73eec356f845aa36f4c2e1fa36c8dea5e42009b31eba16262783e2555；公共约束和验证见整体history同轮。
- A2本项 829.59 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R15/comparison.json，提交 6adc93e31dac5d235bb92d3e；预算 原始 15/16，有效 8/10，本次平台失败补偿 False，member2 daily50硬上限，隐藏项不外推。


## 2026-10-24T19:21:53.867194+08:00 — colpanel_member2_10_R16

- 方法：confirm，SHA 91b9aee73eec356f845aa36f4c2e1fa36c8dea5e42009b31eba16262783e2555；公共约束和验证见整体history同轮。
- A2本项 0 μs；平台 Fail；当前决定 confirmation_pending_audit，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R16/comparison.json，提交 6adc94b81dac5d235bb9bf59；预算 原始 16/16，有效 8/10，本次平台失败补偿 True，member2 daily50硬上限，隐藏项不外推。


## 2026-10-24T19:22:52.089402+08:00 — member2_colpanel_final10_20261024

- 原始 16 次回执：[('R01', 'column_panel', 0, 'Fail', 'compensated'), ('R02', 'div_mask', 837.68, 'Pass', 'effective'), ('R03', 'softmax_dense', 830.44, 'Pass', 'effective'), ('R04', 'column_q1_minimal', 0, 'Fail', 'compensated'), ('R05', 'div_full_only', 0, 'Fail', 'compensated'), ('R06', 'softmax_dense_sub', 838.51, 'Pass', 'effective'), ('R07', 'column_panel', 839.37, 'Pass', 'effective'), ('R08', 'column_q1_intcopy', 836.87, 'Pass', 'effective'), ('R09', 'div_full_only', 0, 'Fail', 'compensated'), ('R10', 'softmax_dense_costguard', 829.38, 'Pass', 'effective'), ('R11', 'repeat selected source', 0, 'Fail', 'compensated'), ('R12', 'repeat selected source', 0, 'Fail', 'compensated'), ('R13', 'repeat selected source', 838.78, 'Pass', 'effective'), ('R14', 'repeat selected source', 0, 'Fail', 'compensated'), ('R15', 'repeat selected source', 829.59, 'Pass', 'effective'), ('R16', 'confirm selected source', 0, 'Fail', 'compensated')] us；参考前轮同SHA三次中位数 830.35 us，本轮无新控制；编号不代表shape。平台失败清单 ['R01', 'R04', 'R05', 'R09', 'R11', 'R12', 'R14', 'R16']，共 8 次；来源为用户确认及通用授权“失败请求可以补额度，遇到submission failed就补一次额度”，无独立平台阶段日志佐证。每次仍占每日原始额度并完整审计；精确匹配回执从有效目标和性能统计排除。
- 保留：BASELINE，SHA 0af5c23189e8a50e0a148e10d74930a70833a140a53f84789dfc8c4b75eae9d5；前轮参考中位数 830.35 us，相对 持平 0.000%；整体条件见history，不拼接单点最优。
- 最终确认：成功confirm []，最后原始 R16 本项 0 us，SHA 91b9aee73eec356f845aa36f4c2e1fa36c8dea5e42009b31eba16262783e2555；确认通过=False。最后原始轮次 R16 后回退父版；active与平台latest源码不同，没有为修正latest追加POST。
- 精度边界：非父版绑定0af5 strict-bits/编译/A3设备manifest，全部原始sample通过；A2状态见回执。严格iters/原求和次序/Div/所有权证据见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/validation_summary.json；不外推隐藏十项。
- 经验停止：本轮短行候选的本项效果按同源码整体观测确认，不由未改分支推断性能。 member2本轮原始 16/16，平台失败补偿 8，有效 8/10，今日 34→50/50；停止原因 daily_hard_cap_reached，有效目标达成=False。STOP已写，无未确认POST，停止后不再提交或自动继续。 证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/final_audit.json、confirmation.json及全部comparison。 补充已确认的候选观察：91b9成本门槛版R10/R15本项两次Pass为[829.38, 829.59] us，中位数 829.485 us，相对旧参考变化 -0.104%；R16平台失败导致缺少第三次成功及成功confirm，未保留并不表示本项代码失败。完整候选路径和逐版结论见总体history。


## 2026-10-24T20:05:39.846921+08:00 — parallel_member3_R01

- 分支A，SHA c4c07d7fa3fcd1bc99e0b1608db568971970743608f21d7038042102ab464173；约束与验证见整体history同轮。
- 本项 830.11 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R01/comparison.json，提交 6adc9eeb1dac5d235bc07de4。


## 2026-10-24T20:11:55.505707+08:00 — parallel_member3_R02

- 分支C，SHA b4f53e1f5820c25568d73eec67bf2cc93b4d10a4ab0fe37987f57eb1fe548bd2；约束与验证见整体history同轮。
- 本项 830.77 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R02/comparison.json，提交 6adca0631dac5d235bc18e97。


## 2026-10-24T20:16:37.140920+08:00 — parallel_member3_R03

- 分支B，SHA f2eca44b52fb44edc9f0cf31086e250324deb0120eef174acc5daa83f9980b65；约束与验证见整体history同轮。
- 本项 0 μs，A2 Fail；平台失败补偿 True，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R03/comparison.json，提交 6adca18b1dac5d235bc24f99。


## 2026-10-24T20:20:25.034146+08:00 — parallel_member3_R04

- 分支B，SHA f2eca44b52fb44edc9f0cf31086e250324deb0120eef174acc5daa83f9980b65；约束与验证见整体history同轮。
- 本项 830.71 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R04/comparison.json，提交 6adca2601dac5d235bc2cf19。


## 2026-10-24T20:23:58.519175+08:00 — parallel_member3_R05

- 分支A，SHA 19ff0a69a2e644d442b8a40a792c2628bdc4c78fff688d8e7000a0774ee2fdfb；约束与验证见整体history同轮。
- 本项 829.24 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R05/comparison.json，提交 6adca3351dac5d235bc35285。


## 2026-10-24T20:27:25.305700+08:00 — parallel_member3_R06

- 分支B，SHA d9d09774380da89f4fb9bf918f6f8015f9978f50624af58eaa2f0acaa4302071；约束与验证见整体history同轮。
- 本项 0 μs，A2 Fail；平台失败补偿 True，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R06/comparison.json，提交 6adca4091dac5d235bc3e229。


## 2026-10-24T20:31:03.358069+08:00 — parallel_member3_R07

- 分支B，SHA d9d09774380da89f4fb9bf918f6f8015f9978f50624af58eaa2f0acaa4302071；约束与验证见整体history同轮。
- 本项 840.42 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R07/comparison.json，提交 6adca4de1dac5d235bc46d7a。


## 2026-10-24T20:34:36.526804+08:00 — parallel_member3_R08

- 分支C，SHA 985def93a6fd8953a6a8051d9de8971c48ac0f458b74607dbc813384e019f8ef；约束与验证见整体history同轮。
- 本项 838.65 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R08/comparison.json，提交 6adca5b41dac5d235bc50172。


## 2026-10-24T20:38:09.272308+08:00 — parallel_member3_R09

- 分支A，SHA 924c58ae542c952306af7b6ade561dbe42ebcc6e6fcdc1bcf86d726656ab69e6；约束与验证见整体history同轮。
- 本项 830.64 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R09/comparison.json，提交 6adca6881dac5d235bc5890a。


## 2026-10-24T20:41:41.095574+08:00 — parallel_member3_R10

- 分支B，SHA 3507c71a25a5e204010ecad1bc21a147954614f72ebf805d8fb3b04bfa72ab49；约束与验证见整体history同轮。
- 本项 831.45 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R10/comparison.json，提交 6adca75c1dac5d235bc614d0。


## 2026-10-24T20:45:13.230159+08:00 — parallel_member3_R11

- 分支C，SHA 0d11fbacfa1b7d5bf33af9d0c82f3bcc40db17d07df092bd602ac280d4361775；约束与验证见整体history同轮。
- 本项 831.18 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R11/comparison.json，提交 6adca8301dac5d235bc68c6e。


## 2026-10-24T20:48:45.000914+08:00 — parallel_member3_R12

- 分支A，SHA 924c58ae542c952306af7b6ade561dbe42ebcc6e6fcdc1bcf86d726656ab69e6；约束与验证见整体history同轮。
- 本项 830.61 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R12/comparison.json，提交 6adca9041dac5d235bc71e95。


## 2026-10-24T20:52:01.657790+08:00 — parallel_member3_R13

- 分支B，SHA 3507c71a25a5e204010ecad1bc21a147954614f72ebf805d8fb3b04bfa72ab49；约束与验证见整体history同轮。
- 本项 0 μs，A2 Fail；平台失败补偿 True，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R13/comparison.json，提交 6adca9d81dac5d235bc79984。


## 2026-10-24T20:55:48.789461+08:00 — parallel_member3_R14

- 分支B，SHA 3507c71a25a5e204010ecad1bc21a147954614f72ebf805d8fb3b04bfa72ab49；约束与验证见整体history同轮。
- 本项 831.51 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R14/comparison.json，提交 6adcaaac1dac5d235bc8259a。


## 2026-10-24T20:59:21.593061+08:00 — parallel_member3_R15

- 分支C，SHA b4f53e1f5820c25568d73eec67bf2cc93b4d10a4ab0fe37987f57eb1fe548bd2；约束与验证见整体history同轮。
- 本项 840.65 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R15/comparison.json，提交 6adcab811dac5d235bc8a51e。


## 2026-10-24T21:02:54.363493+08:00 — parallel_member3_R16

- 分支B，SHA 3507c71a25a5e204010ecad1bc21a147954614f72ebf805d8fb3b04bfa72ab49；约束与验证见整体history同轮。
- 本项 831.2 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R16/comparison.json，提交 6adcac551dac5d235bc92c45。


## 2026-10-24T21:06:26.041076+08:00 — parallel_member3_R17

- 分支C，SHA 0d11fbacfa1b7d5bf33af9d0c82f3bcc40db17d07df092bd602ac280d4361775；约束与验证见整体history同轮。
- 本项 829.88 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R17/comparison.json，提交 6adcad291dac5d235bc9b25d。


## 2026-10-24T21:09:58.027296+08:00 — parallel_member3_R18

- 分支A，SHA 924c58ae542c952306af7b6ade561dbe42ebcc6e6fcdc1bcf86d726656ab69e6；约束与验证见整体history同轮。
- 本项 830.18 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R18/comparison.json，提交 6adcadfd1dac5d235bca32c5。


## 2026-10-24T21:13:09.146962+08:00 — parallel_member3_3x5_FINAL_20261024

- 本轮公共方法/完整SHA/验证见整体history同标记；最终A/v3 `924c58ae542c952306af7b6ade561dbe42ebcc6e6fcdc1bcf86d726656ab69e6`，严格iters、原求和次序和Div。
- 本项同SHA三次中位数 830.610µs；旧父版历史参考 829.485µs，耗时变化 +0.136%。最新确认本项 830.18µs；没有新增同期基线。
- 各路最终候选本项中位数 {'A': 830.61, 'B': 830.71, 'C': 830.53}；不拼接各候选最低值。本轮case1变化很小，未把它解释为定向收益。
- 决定：保留全局A/v3，三路各5次有效已停；隐藏十项细节未知。证据 `/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/REPORT.md` 和 `/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/final_analysis.json`；最新提交 `6adcadfd1dac5d235bca32c5`。



## 2026-10-24T21:28:13.482985+08:00 — local_A3_perf_once_local_perf_20261024T132308Z_924c58ae

- 当前最佳源码SHA `924c58ae542c952306af7b6ade561dbe42ebcc6e6fcdc1bcf86d726656ab69e6`，本地A3单次会话；生产kernel未修改、没有A2提交。
- workload B/S/H/iters=7/128/128/20来自历史探针，eps1e-6和输入uniform[-2,2]为本地假设，不作为生产专用分派依据。
- A2同源码三次历史中位数 830.61µs；A3记录30次中位数 818.24µs，范围817.18–819.42µs，A3耗时变化-1.49%。不能归因纯芯片或当作同期配对结果。
- 五组校验与原始CSV见 `/mnt/workspace/enjoy_ur_time/others/local_perf_20261024T132308Z_924c58ae/REPORT.md` 和comparison.json；本轮只做一次本地测评，NPU锁释放，提交STOP保持。



## 2026-10-24T22:08:04.901153+08:00 — cases345_max_member3_R01

- 分支A，SHA ddec95e49e566a246dab41b1c301ba2c7211cb9c82c6ab5b6be75bf0fd8bfe6c；约束与验证见整体history同轮。
- 本项 830.42 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R01/comparison.json，提交 6adcbb9c1dac5d235bd2ea25。


## 2026-10-24T22:12:27.589595+08:00 — cases345_max_member3_R02

- 分支C，SHA 1bc3e59e4a62f9714669e9a4c092e1397b6e27128b52f07542e311b8fb704366；约束与验证见整体history同轮。
- 本项 0 μs，A2 Fail；平台失败补偿 False，平台失败 True，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R02/comparison.json，提交 6adcbcb21dac5d235bd3a127。


## 2026-10-24T22:17:48.275114+08:00 — cases345_max_member3_R03

- 分支C，SHA 1bc3e59e4a62f9714669e9a4c092e1397b6e27128b52f07542e311b8fb704366；约束与验证见整体history同轮。
- 本项 830.68 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R03/comparison.json，提交 6adcbde31dac5d235bd46196。


## 2026-10-24T22:21:05.068090+08:00 — cases345_max_member3_R04

- 分支A，SHA 44d7468872b70f18b3626d8861f940aafb945a940f984e8f33651dd10bbba722；约束与验证见整体history同轮。
- 本项 0 μs，A2 Fail；平台失败补偿 False，平台失败 True，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R04/comparison.json，提交 6adcbeb71dac5d235bd4e9e1。


## 2026-10-24T22:24:58.110910+08:00 — cases345_max_member3_R05

- 分支A，SHA 44d7468872b70f18b3626d8861f940aafb945a940f984e8f33651dd10bbba722；约束与验证见整体history同轮。
- 本项 840.07 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R05/comparison.json，提交 6adcbf8c1dac5d235bd56f24。


## 2026-10-24T22:29:06.701136+08:00 — cases345_max_member3_R06

- 分支A，SHA 172977f03347d73b5c651020e2a7fd8a5d25450f205b5e62d5e7f5db3f87e8e5；约束与验证见整体history同轮。
- 本项 830.55 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R06/comparison.json，提交 6adcc08a1dac5d235bd60e6b。


## 2026-10-24T22:34:08.713852+08:00 — cases345_max_member3_R07

- 分支C，SHA 1cbd576d3adbab76ea8c52b6aac43437297819e26ac5b49aa6f85bc4bb6578fe；约束与验证见整体history同轮。
- 本项 838.8 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R07/comparison.json，提交 6adcc1b31dac5d235bd6e585。


## 2026-10-24T22:40:57.379814+08:00 — cases345_max_member3_R08

- 分支B，SHA bf04826db0b6f59abba7460c845e308de95b25bb4462358a3f649ad9ff23861a；约束与验证见整体history同轮。
- 本项 834.6 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R08/comparison.json，提交 6adcc3501dac5d235bd8152d。


## 2026-10-24T22:44:30.189549+08:00 — cases345_max_member3_R09

- 分支A，SHA aebb7faf77b915fa459a7f996606571af9d534fbcd5dc0263306a7cdc26918a1；约束与验证见整体history同轮。
- 本项 839.18 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R09/comparison.json，提交 6adcc4251dac5d235bd8a7b1。


## 2026-10-24T22:50:54.714792+08:00 — cases345_max_member3_R10

- 分支A，SHA aebb7faf77b915fa459a7f996606571af9d534fbcd5dc0263306a7cdc26918a1；约束与验证见整体history同轮。
- 本项 839.01 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R10/comparison.json，提交 6adcc5a61dac5d235bd9bbc4。


## 2026-10-24T22:59:45.324153+08:00 — cases345_max_member3_R11

- 分支C，SHA d117c6ecc8b2ea1b206ccfca0af45a3ac67bf0991204b7854deb32731cce8632；约束与验证见整体history同轮。
- 本项 828.95 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R11/comparison.json，提交 6adcc7b81dac5d235bdb4fc9。


## 2026-10-24T23:03:22.754833+08:00 — cases345_max_member3_R12

- 分支B，SHA adc8b8d677b3c5fa3eb270cc6103efd9e9bfa6665d437b0c538d7d1c165cdfc9；约束与验证见整体history同轮。
- 本项 830.95 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R12/comparison.json，提交 6adcc88d1dac5d235bdc0db8。


## 2026-10-24T23:06:49.482580+08:00 — cases345_max_member3_R13

- 分支C，SHA 680ac58779f099d252beae0a1fc2089c7266bec1fd07f04da830f3dd9053106a；约束与验证见整体history同轮。
- 本项 829.67 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R13/comparison.json，提交 6adcc9611dac5d235bdcc633。


## 2026-10-24T23:10:22.208871+08:00 — cases345_max_member3_R14

- 分支C，SHA 680ac58779f099d252beae0a1fc2089c7266bec1fd07f04da830f3dd9053106a；约束与验证见整体history同轮。
- 本项 831.01 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R14/comparison.json，提交 6adcca351dac5d235bdd5c17。


## 2026-10-24T23:15:15.407819+08:00 — cases345_max_member3_R15

- 分支M，SHA 21dab72f389edddfafc7531de172f86957ae3e5f270be750b31e5dba529ef096；约束与验证见整体history同轮。
- 本项 835.39 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R15/comparison.json，提交 6adccb5a1dac5d235bde897f。


## 2026-10-24T23:18:52.882580+08:00 — cases345_max_member3_R16

- 分支M，SHA 21dab72f389edddfafc7531de172f86957ae3e5f270be750b31e5dba529ef096；约束与验证见整体history同轮。
- 本项 836.17 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R16/comparison.json，提交 6adccc2f1dac5d235bdf2b25。


## 2026-10-24T23:23:30.524029+08:00 — cases345_max_member3_R17

- 分支C，SHA 680ac58779f099d252beae0a1fc2089c7266bec1fd07f04da830f3dd9053106a；约束与验证见整体history同轮。
- 本项 830.36 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R17/comparison.json，提交 6adccd4a1dac5d235bdfde6a。


## 2026-10-24T23:30:08.945616+08:00 — cases345_max_member3_final_C6

- 方法/经验：未定向修改大矩阵路径，A3成对测量基本不变。A2约830–839µs波动，不能把所有变化归于代码或假定固定机器模式。
- A2同源码中位：C6 830.3600µs，融合 835.7800µs，原基线 830.6100µs；最新确认830.36µs。
- 保留：用户选择C6，SHA 680ac58779f099d252beae0a1fc2089c7266bec1fd07f04da830f3dd9053106a；提交6adccd4a1dac5d235bdfde6a。本轮原始17/32，M2/2完成，失败计数，停止续交；隐藏十项未知。
- 证据：C6 10635设备配置执行含1008 holdout全逐位通过，guard/unwritten/input_changes为0；[完整报告](/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/REPORT.md)、[最终选用](/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/final_selection.json)。


## 2026-10-25T00:10:18.370921+08:00 — cases145_max_member1_20261025_R01

- 分支M，SHA 680ac58779f099d252beae0a1fc2089c7266bec1fd07f04da830f3dd9053106a；约束与验证见整体history同轮。
- 本项 829.54 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R01/comparison.json，提交 6adcd8411dac5d235be77d01。


## 2026-10-25T00:22:59.256150+08:00 — cases145_max_member1_20261025_R02

- 分支D，SHA 57a3f2a87e99c94111e2fbf74da4f382d7a4fe1b147d03278aaa1a2731921245；约束与验证见整体history同轮。
- 本项 804.25 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R02/comparison.json，提交 6adcdb3a1dac5d235be9d4d8。


## 2026-10-25T00:29:37.120625+08:00 — cases145_max_member1_20261025_R03

- 分支C，SHA 17bcdfa9031bab1473eb0508c0756413bd627280a064bd26fe3a1e8ec3a3a07b；约束与验证见整体history同轮。
- 本项 830.17 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R03/comparison.json，提交 6adcdcc31dac5d235bead09f。


## 2026-10-25T00:32:41.852976+08:00 — cases145_max_member1_20261025_R04

- 分支B，SHA 13da845bd6428bd54a221618bedd83cfbea235a797c39b878762abcec78415b3；约束与验证见整体history同轮。
- 本项 834.25 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R04/comparison.json，提交 6adcdd811dac5d235beb583e。


## 2026-10-25T00:37:27.022071+08:00 — cases145_max_member1_20261025_R05

- 分支D，SHA d5e6b51003bd92dd03282e8b799007835110bf397413fa5e9d2113c7ac6e2217；约束与验证见整体history同轮。
- 本项 801.55 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R05/comparison.json，提交 6adcde991dac5d235bec2160。


## 2026-10-25T00:41:44.288049+08:00 — cases145_max_member1_20261025_R06

- 分支B，SHA f3e47ee4a9424579cafb6723c550bba373e4d025cee9591ae3527b66a724e4db；约束与验证见整体history同轮。
- 本项 830.57 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R06/comparison.json，提交 6adcdf9f1dac5d235becda91。


## 2026-10-25T00:51:05.979518+08:00 — cases145_max_member1_20261025_R07

- 分支C，SHA 4e995cb2850a3473d2ce2ea0af5b40199d3fd5675f3d6c79840d07c2fcf135fa；约束与验证见整体history同轮。
- 本项 831.28 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R07/comparison.json，提交 6adce1c71dac5d235bee8021。


## 2026-10-25T00:54:57.725830+08:00 — cases145_max_member1_20261025_R08

- 分支B，SHA f8a672bbcff3400593b795f172fedc290a5d2cec3377c87ac5cc1e960e1f2af4；约束与验证见整体history同轮。
- 本项 833.07 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R08/comparison.json，提交 6adce2b91dac5d235bef5cb8。


## 2026-10-25T01:06:30.198238+08:00 — cases145_max_member1_20261025_R09

- 分支D，SHA f1f310bd2bfcf3906aa898b34096ae9c2524f8c963e3847f177f631d5bc23d93；约束与验证见整体history同轮。
- 本项 806.27 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R09/comparison.json，提交 6adce56d1dac5d235bf1110e。


## 2026-10-25T01:10:49.994077+08:00 — cases145_max_member1_20261025_R10

- 分支B，SHA 12b01f4c87a01c609aa3ae132203bf43a50e3e361b9346f781e8030587e693b9；约束与验证见整体history同轮。
- 本项 837.93 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R10/comparison.json，提交 6adce66c1dac5d235bf1a51b。


## 2026-10-25T01:14:09.247285+08:00 — cases145_max_member1_20261025_R11

- 分支D，SHA 9c87bf37552adfc1c325a99da772fb563ae224e7fc654f88acf40ed75b8f899e；约束与验证见整体history同轮。
- 本项 796.14 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R11/comparison.json，提交 6adce7331dac5d235bf226f9。


## 2026-10-25T01:32:39.557571+08:00 — cases145_max_member1_20261025_R13

- 分支C，SHA f113a769b1cf3d514aa075de4219fdbd955d8898f883cfd6f6b7fe6d4c245880；约束与验证见整体history同轮。
- 本项 829.41 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R13/comparison.json，提交 6adceb8a1dac5d235bf4ef19。


## 2026-10-25T01:35:34.733093+08:00 — cases145_max_member1_20261025_R14

- 分支B，SHA 8efe54ba6cd2c2dd4f77aa1d4873f4d56258ead1618d7f42859d68edd4a8783a；约束与验证见整体history同轮。
- 本项 838.88 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R14/comparison.json，提交 6adcec3e1dac5d235bf561f0。


## 2026-10-25T01:39:30.135164+08:00 — cases145_max_member1_20261025_R15

- 分支D，SHA 06e778648b3fbddacc5720e595a14e51caac8d6ab27f6c39dbe5514a3e3ecb24；约束与验证见整体history同轮。
- 本项 799.19 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R15/comparison.json，提交 6adced291dac5d235bf5f576。


## 2026-10-25T01:46:59.707753+08:00 — cases145_max_member1_20261025_R17

- 分支D，SHA f77cc8fa5461943ab111370f430bb2df715c86b10d63e8d2ad7626e1c682bf4e；约束与验证见整体history同轮。
- 本项 800.13 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R17/comparison.json，提交 6adceeeb1dac5d235bf72397。


## 2026-10-25T01:57:02.170458+08:00 — cases145_max_member1_20261025_R18

- 分支D，SHA 9c87bf37552adfc1c325a99da772fb563ae224e7fc654f88acf40ed75b8f899e；约束与验证见整体history同轮。
- 本项 797.65 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R18/comparison.json，提交 6adcf1451dac5d235bf8ac88。


## 2026-10-25T02:00:29.601221+08:00 — cases145_max_member1_20261025_R19

- 分支B，SHA ae862a6bae960c4be49e12b4f849f9f1675e27fce89c64348d7fbb69aa7b4a43；约束与验证见整体history同轮。
- 本项 838.18 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R19/comparison.json，提交 6adcf2151dac5d235bf93325。


## 2026-10-25T02:04:02.748948+08:00 — cases145_max_member1_20261025_R20

- 分支B，SHA f3e47ee4a9424579cafb6723c550bba373e4d025cee9591ae3527b66a724e4db；约束与验证见整体history同轮。
- 本项 830.59 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R20/comparison.json，提交 6adcf2e51dac5d235bf9ca86。


## 2026-10-25T02:07:30.173349+08:00 — cases145_max_member1_20261025_R21

- 分支D，SHA a0bc1f2d62258843738a0db76351fd73f081b4b2c2d4b014c080ef2051324f1c；约束与验证见整体history同轮。
- 本项 799.88 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R21/comparison.json，提交 6adcf3b41dac5d235bfa551c。


## 2026-10-25T02:11:19.768897+08:00 — cases145_max_member1_20261025_R22

- 分支C，SHA 680ac58779f099d252beae0a1fc2089c7266bec1fd07f04da830f3dd9053106a；约束与验证见整体history同轮。
- 本项 829.82 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R22/comparison.json，提交 6adcf49a1dac5d235bfaf0ff。


## 2026-10-25 中点诊断 — cases145_stage_D

- A2 D6两次case1为796.14/797.65µs；D8退化的case3/4/5在D6邻近控制中恢复，暂以D6作性能donor，不据此断言A2缓存/寄存器原因。
- A3 40核432任务阶段ABBA：H64 Softmax D2→D6为0.833594→0.855391µs/次（+2.615%）；H128为3.019453→2.862852（-5.186%）。相同方法控制约1.0，漂移小；阶段proxy不是生产时间占比。
- 列链D2→D7 H64约-0.88%、H128约-0.40%；两独立机制不能按百分比相加。D11 A2跨项退化，暂不融合；D12只给至少两完整向量片保留连续Exp/eps，H64精确回到D2。
- strict/guard/input/unwritten检查通过；D12新源码仍须fresh22+全kernel/H64配对。证据：D/stage_pair_d2_d6_d7_d11/parent_profile/comparison.json、中央R18/R21、D/MIDPOINT.md。


## 2026-10-25T02:17:59.689058+08:00 — cases145_max_member1_20261025_R23

- 分支C，SHA 5244c778c74719b0e4f23138a9c46480ef729eb9d5bfe8dfe4925e66577b711a；约束与验证见整体history同轮。
- 本项 837.3 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R23/comparison.json，提交 6adcf62f1dac5d235bfc07ac。


## 2026-10-25T02:21:26.439973+08:00 — cases145_max_member1_20261025_R24

- 分支C，SHA 5244c778c74719b0e4f23138a9c46480ef729eb9d5bfe8dfe4925e66577b711a；约束与验证见整体history同轮。
- 本项 836.73 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R24/comparison.json，提交 6adcf6fe1dac5d235bfc9301。


## 2026-10-25T02:24:53.196004+08:00 — cases145_max_member1_20261025_R25

- 分支C，SHA 680ac58779f099d252beae0a1fc2089c7266bec1fd07f04da830f3dd9053106a；约束与验证见整体history同轮。
- 本项 839.06 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R25/comparison.json，提交 6adcf7cc1dac5d235bfd13ec。


## 2026-10-25T02:35:26.624217+08:00 — cases145_max_member1_20261025_R26

- 分支B，SHA f3e47ee4a9424579cafb6723c550bba373e4d025cee9591ae3527b66a724e4db；约束与验证见整体history同轮。
- 本项 0 μs，A2 Time Limit Exceeded；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R26/comparison.json，提交 6adcf8d31dac5d235bfdcaca。


## 2026-10-25T02:36:35.519788+08:00 — cases145_max_member1_20261025_R27

- 分支M，SHA 26ee0ad7a53014af714da5934985498d1519f86778afb2603c5774e490be4b16；约束与验证见整体history同轮。
- 本项 801.14 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R27/comparison.json，提交 6adcfa861dac5d235bfeee28。


## 2026-10-25T02:39:57.724663+08:00 — cases145_max_member1_20261025_R28

- 分支B，SHA f3e47ee4a9424579cafb6723c550bba373e4d025cee9591ae3527b66a724e4db；约束与验证见整体history同轮。
- 本项 829.51 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R28/comparison.json，提交 6adcfb551dac5d235bff71af。


## 2026-10-25T02:43:30.520861+08:00 — cases145_max_member1_20261025_R29

- 分支M，SHA 26ee0ad7a53014af714da5934985498d1519f86778afb2603c5774e490be4b16；约束与验证见整体history同轮。
- 本项 797.1 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R29/comparison.json，提交 6adcfc251dac5d235bfff258。


## 2026-10-25T02:46:57.864763+08:00 — cases145_max_member1_20261025_R30

- 分支B，SHA f3e47ee4a9424579cafb6723c550bba373e4d025cee9591ae3527b66a724e4db；约束与验证见整体history同轮。
- 本项 838.67 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R30/comparison.json，提交 6adcfcf41dac5d235b007005。


## 2026-10-25T02:51:27.587581+08:00 — cases145_max_member1_20261025_R31

- 分支D，SHA 57a3f2a87e99c94111e2fbf74da4f382d7a4fe1b147d03278aaa1a2731921245；约束与验证见整体history同轮。
- 本项 807.91 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R31/comparison.json，提交 6adcfe071dac5d235b0122d5。


## 2026-10-25T02:55:00.769627+08:00 — cases145_max_member1_20261025_R32

- 分支M，SHA 7c3275dd848553fa06334508f4f4ac3b2918aa0fd0e9046f0e78b4122478f55a；约束与验证见整体history同轮。
- 本项 795.79 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R32/comparison.json，提交 6adcfed71dac5d235b019dd5。


## 2026-10-25T02:58:28.888350+08:00 — cases145_max_member1_20261025_R33

- 分支D，SHA d5e6b51003bd92dd03282e8b799007835110bf397413fa5e9d2113c7ac6e2217；约束与验证见整体history同轮。
- 本项 806.39 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R33/comparison.json，提交 6adcffa71dac5d235b021c36。


## 2026-10-25T03:01:56.709644+08:00 — cases145_max_member1_20261025_R34

- 分支M，SHA 26ee0ad7a53014af714da5934985498d1519f86778afb2603c5774e490be4b16；约束与验证见整体history同轮。
- 本项 797.53 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R34/comparison.json，提交 6add00771dac5d235b02984b。


## 2026-10-25T03:05:24.114680+08:00 — cases145_max_member1_20261025_R35

- 分支D，SHA 9c87bf37552adfc1c325a99da772fb563ae224e7fc654f88acf40ed75b8f899e；约束与验证见整体history同轮。
- 本项 797.31 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R35/comparison.json，提交 6add01461dac5d235b033068。


## 2026-10-25T03:09:07.836377+08:00 — cases145_max_member1_20261025_R36

- 分支M，SHA 7c3275dd848553fa06334508f4f4ac3b2918aa0fd0e9046f0e78b4122478f55a；约束与验证见整体history同轮。
- 本项 794.37 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R36/comparison.json，提交 6add022b1dac5d235b03f77e。


## 2026-10-24T19:12:31.639915+00:00 — cases145_final_diagnostic_gates_20261025

- 方法：D15在完整多向量行资源族合批两矩阵，D6逐字回退，阈值165120B，真实q2覆盖iters1..32和奇数tail。
- 正确性：fresh34suite+holdout、raw比较9486336个bits、资源72config144launch均0差异/guard/input/unwritten；CSV q2入口24、D15fallback48、D6入口72；低165119资源不启动q2。
- 性能/决定：A3 D6 783.42→D15 823.17μs(+5.0739%)，控制漂移-0.00766%；不A2、不保留为donor。D6 R35 A2 797.31μs，官方30.20/r19。
- 证据：performance_pair/Pair_D6_D15_1a0479a0dc0f/comparison.json 与 D/raw_batch_v15/parent_device_summary.json；节省barrier未抵消整体成本，具体瓶颈未由隔离PMU证明。


## 2026-10-25T03:14:04.232978+08:00 — cases145_max_member1_20261025_R37

- 分支M，SHA 06fb13aefcd79b8bef105479e11a0d5e7e880056b1ac8187ea2d0cc5aad369c8；约束与验证见整体history同轮。
- 本项 805.54 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R37/comparison.json，提交 6add03531dac5d235b04a006。


## 2026-10-25T03:17:30.930966+08:00 — cases145_max_member1_20261025_R38

- 分支D，SHA 57a3f2a87e99c94111e2fbf74da4f382d7a4fe1b147d03278aaa1a2731921245；约束与验证见整体history同轮。
- 本项 804.9 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R38/comparison.json，提交 6add04221dac5d235b050829。


## 2026-10-25T03:21:04.462882+08:00 — cases145_max_member1_20261025_R39

- 分支M，SHA 06fb13aefcd79b8bef105479e11a0d5e7e880056b1ac8187ea2d0cc5aad369c8；约束与验证见整体history同轮。
- 本项 804.65 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R39/comparison.json，提交 6add04f21dac5d235b058cc7。


## 2026-10-25T03:24:27.312691+08:00 — cases145_max_member1_20261025_R40

- 分支D，SHA 57a3f2a87e99c94111e2fbf74da4f382d7a4fe1b147d03278aaa1a2731921245；约束与验证见整体history同轮。
- 本项 805.16 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R40/comparison.json，提交 6add05c21dac5d235b061370。


## 2026-10-25T03:24:42.209435+08:00 — cases145_member1_20261025_completed

- 采用：D1（最高观测官方分版本），SHA 57a3f2a87e99c94111e2fbf74da4f382d7a4fe1b147d03278aaa1a2731921245；严格iters、原树/eps/Div、单launch与32B owner保持。正式kernel、冻结快照、服务端源码一致。
- 验证/成绩：A3完整逐位/边界与holdout通过；A2 Pass，本项/整体 805.16μs；官方 30.6分/r18，观察2026-10-25T03:24:27.373097+08:00，隐藏10项详情未知。
- 决定/经验：M3 R37/39为30.68/29.93未证明稳定总分优势；按排名优先恢复D1（历史最高30.80，三次中位30.52高于M3的30.305）。融合公开收益保留为候选；D15/C10/尾WR压缩淘汰。跨时段波动不作编译因果。
- 停止与证据：原始尝试40，接收38，有效37；member2未用，剩余额度不自动继续。最终SID 6add05c21dac5d235b061370；/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/REPORT.md、/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/final_selection.json。


## 2026-10-25 — m1m2_batch_member1_20261025_comparison_complete

- 方法/范围：四个已冻结版本复测；严格真实iters1..32、FP32原求和次序、原Div和eps、单launch、输入只读与32B owner均不改。用户已取消用完剩余额度及B2选批优化提交。
- A2结果：M2 794.73 us；C6 830.19 us；D1 805.53 us；M1 797.49 us；均Pass，数值来自各自精确SID，隐藏10项详情未知。
- 官方观察：M2 29.67分/r19 SID 6add70571dac5d235b3c49fd；C6 28.67分/r20 SID 6add72051dac5d235b3d8ee4；D1 29.63分/r19 SID 6add72de1dac5d235b3e363c；M1 29.71分/r18 SID 6add73b81dac5d235b3ed41b；观察时间与完整SHA见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_m1m2_batch_member1_remaining/REPORT.md；R01初始M1仅附录，无分数。
- 决定：未自动选版；生产源码暂保持M1 SHA 26ee0ad7a53014af714da5934985498d1519f86778afb2603c5774e490be4b16，等待用户选择，不把动态分数当作源码稳定属性。
- 停止/证据：原始尝试6，接受5、有效5；member1当日43/50，剩余7次不自动使用。STOP保留，B2选批草稿未执行或提交；/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_m1m2_batch_member1_remaining/comparison.json。


## 2026-10-25T11:20:16.264081+08:00 — m1m2_member1_20261025_user_selected_M1

- 选择：用户明确指示“保留M1”；正式kernel已是M1，核对哈希一致，无需覆盖源码。
- 证据：SHA 26ee0ad7a53014af714da5934985498d1519f86778afb2603c5774e490be4b16；member1提交 6add73b81dac5d235b3ed41b，A2 Pass；本项/五项耗时 797.49 µs。
- 观察：该次官方29.71分/第18，观察时间 2026-10-25T11:13:42.506903+08:00；仅作历史榜单参考，不声明当前排名；隐藏十项详情未知。
- 状态：已确认M1并保持STOP，不再提交、不续用余量；选择记录 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_m1m2_batch_member1_remaining/final_selection.json。


## 2026-10-25T12:39:46.981439+08:00 — m1_cases345_3x5_merge5_20261025_completed

- 范围：本轮目标为case3/4/5；本项没有定向采用新的优化。生产继续同一SHA的M1。
- 额外确认：member1 SID 6add871c1dac5d235b4c9e53，A2 Pass，本项797.40us；公开精度1，隐藏细节未知。
- 决定：13个新候选均未达到A3目标>5%门槛，未进入A2或融合；最终确认仅M1一次，不自动采用新基线。
- 停止/证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_m1_cases345_3x5_merge5/REPORT.md、R01/comparison.json；剩余额度不自动继续。


## 2026-10-25 M1 八行BR、尾部WR与分母表示独立优化（已停止，待选择）

- 本轮无该case定向源码修改；全部完整A2耗时与M1对照见整体history及 `/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_m1_br_tail_denom_3x5/REPORT.md`。case2 A3阶段漂移不可归因于代码；不自动保留任何候选。


## 2026-10-25 M1融合A1+B2+C1验证完成（已停止，待选择）

- 融合F1 SHA fd52c080d686134fa389a3930d6f922adf19cd4d5a5fd462ee6a65d9e5f6a798，A1+B2+C1 literal union；原iters/树/eps/Div/输出所有权不改，正式M1保持。
- 本项A2：F1 796.40/800.28 us；本轮M1 801.50 us。独立版上轮 A1:797.32/797.39 us, B2:795.64/797.05 us, C1:795.49/796.61 us；跨时段明确标注。
- 检查/经验：A3严格9222配置执行含1008holdout与边界检查通过；mask/UB/dead scratch/树静态审查无问题。F1同SHA case3/5复测变慢，case4较稳定，不能确认三项独立收益同时稳定保留。保留全部记录，不外推A2机制。
- 停止/证据：member2 3/5 POST后停止，fail不补，无自动换基线；用户选择待定。完整五项/SID/分数排名观察时间见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_m1_merge_a1b2c1_5/REPORT.md、final_comparison.json。


## 2026-10-25T14:18:07.365489+08:00 — user_selected_F1_as_baseline

- 用户明确选择F1作为新基线；正式云端kernel.asc已部署冻结F1，SHA fd52c080d686134fa389a3930d6f922adf19cd4d5a5fd462ee6a65d9e5f6a798。原M1快照继续保留。
- 本项既有A2两次Pass耗时 796.40/800.28 us；完整同次五项、SID、观察时间见整体记录；case3/5波动结论保持，隐藏细节未知。
- 生产/冻结/服务端源码哈希一致，原iters/求和次序/eps/Div与输出所有权不变。此次只部署已验证字节，不重新编译或运行NPU。
- 用户要求不再提交；新增POST=0、本轮计数3/3及STOP保持。选择及部署证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_m1_merge_a1b2c1_5/final_selection.json、post_selection_audit.json。


## 2026-10-25T14:25:12.568665+08:00 — f1_single_confirmation_once_completed

- F1同SHA追加一次member2 A2测评，正式源码未改；保持原iters/树/eps/native Div与输出所有权。
- 本项Pass耗时 800.11 us；此前同F1为 796.40/800.28 us，完整同次五项见整体记录。SID 6adda02d1dac5d235b5f7783。
- 同SHA三次实测全部保留，复测不是源码优化收益；分数排名为观察快照，隐藏细节未知。
- 本范围1/1完成并STOP，无pending，不再提交；正式基线继续F1。证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_f1_confirmation_once/REPORT.md、comparison.json、final_audit.json。


<!-- f1_entry_tail_layout_20261025_history -->
## 2026-10-25 F1 三路短行入口/尾部ApplyRows/布局（已停止，待用户选择）

- 方法：未定向改case1。完整向量保留，跨时段差距不当该项结构收益。
- 本项A2实测（us，按提交顺序；均平台整体Pass/公开项Pass）：R01 F1_control_open:801.45; R02 B_v1_tail_apply:801.46; R03 A_v1_short_entry:801.28; R04 F1_control_middle:800.45; R05 A_v1_short_entry_repeat:797.46; R06 F1_control_after_A_repeat:795.86; R07 A_v2_fixed_q:797.23; R08 C_v3_row_gap_active_columns:796.72; R09 B_v1_tail_apply_repeat:796.42; R10 F1_control_close:796.82; R11 A_v2_fixed_q_repeat:796.84。
- 严格iters1..32、原树/+0/eps/native Div、输入/guard/未写输出、32B owner及边界通过；A3诊断与官方case形状映射未知，隐藏十项未知。
- 状态：生产F1未改；member2 A/B/C=5/3/3含对照，全11次已完成并STOP，fail不补、不自动融合，等待用户选择。[完整报告](/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_f1_entry_tail_layout_3x5/REPORT.md)、[源码/SID/分数排名](/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_f1_entry_tail_layout_3x5/final_comparison.json)。


<!-- user_selected_B1_20261025_history -->
## 2026-10-25T15:52:05.284092+08:00 — user_selected_B1_as_baseline

- 用户选择本轮B1为基线，云端kernel已部署冻结B/v1，SHA 7f9a5c0ac91fb990eb7ce9ffd0b5494ad42e509043e32cf62eb1136259dfb8d8；原F1快照保留。
- 本项既有A2 Pass两次为801.46/796.42 us，分别来自R02 SID6adda89e1dac5d235b66d48a和R09 SID6addb00b1dac5d235b6c763b；完整同次五项见整体历史。
- 沿用同SHA A3严格/边界/所有权检查及A2记录；保持真实iters、原树/+0/eps/native Div。不把用户选择等同于全项稳定提升，公开case形状映射及隐藏十项详情仍未知。
- 此次仅部署已验证字节和记录，新增POST/编译/NPU均0，本轮11/11及STOP保持，无pending、不再提交。[选择](/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_f1_entry_tail_layout_3x5/final_selection.json)、[审计](/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_f1_entry_tail_layout_3x5/post_selection_audit.json)。


<!-- b1_tail_exp_gate_20261025_history -->
## 2026-10-25 B1 三路优化（已停止，待用户选择）

- 非本轮定向修改，保留完整向量用于交叉回归；未将波动归因代码。
- 本项A2实际耗时(us，顺序不删)：R01 B1_control_open:797.80; R02 A1_tail_BR:796.29; R04 C1_gate_merge:801.31; R05 B1_control_middle:795.52; R06 Bv1_contiguous_Exp_eps:797.34; R07 C2_gate_batchload:796.24; R08 A1_tail_BR_repeat:796.44; R09 Bv1_contiguous_Exp_eps_repeat:796.69; R10 B1_control_close:797.65; R11 C2_gate_batchload_repeat:797.28。
- 每个候选独立SHA与完整同次五项见整体history及REPORT；真实iters1..32、原树/+0/eps/native Div、输入/guard/未写/32B owner检查通过。A3与A2证据分开，官方case形状及隐藏十项详情未知。
- 状态：生产仍B1；本轮member2 A/B/C=3/3/4，共10次请求且全部Pass，fail不补、无pending并STOP，用户选择前不部署。完整证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_b1_tail_exp_gate_3x5/REPORT.md、final_comparison.json、final_audit.json。


<!-- a1_interleave_tailmul_stripe_20261025_history -->
## 2026-10-25T18:59:01.391315+08:00 A1 三路优化完成（已停止，待用户选择）

- 方法：本轮没有专改case1；所有独立候选的公共入口变化需看完整同次向量。
- 本项A2实测(us，顺序完整)：R01 A1_control_open:796.9 us; R02 B1_tailMul_pack:801.7 us; R03 A1_control_mid:795.63 us; R04 B1_tailMul_pack_repeat:797.48 us; R05 A1_control_after_B:797.36 us。完整同次五项/SID/分数排名观察时间见整体记录及REPORT。
- 验证：所有实测候选各35套/9222配置、input/guard/未写输出与owner尾批检查通过，原iters/树/eps/Div保持。专项raw与容量修复证据分开，prepared-only版本不称设备通过。
- 停止/决定：member2原始/接受5/5，每路最多5且对照计入、fail不补；STOP、pending空，正式A1保持，等待用户选择。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_a1_interleave_tailmul_stripe_3x5/REPORT.md、final_comparison.json、excluded_candidates.json、final_audit.json；A3与A2独立，官方shape/隐藏详情未知。


<!-- a1_compact_prezero_rootpair_20261025_history -->
## 2026-10-25T20:42:32.678705+08:00 A1 紧凑Div与正零/根平面三路完成（停止，待用户选择）

- 方法/结论：本轮无case1定向改动；记录全向量观察，正式A1未改。
- 本项A2实际耗时(us，全部顺序保留)：R01 A1_control_open:797.01; R02 B_v1_prezero:796.93; R03 A1_control_middle:797.51; R04 B_v2_prezero_sum:797.39; R05 A1_control_close:802.06; R06 B_v2_prezero_sum_repeat:797.52。完整同次五项/SID/分数排名时间见整体记录及REPORT。
- 验证：7个候选各35套/9222配置A3逐位通过；原生A两版各12960配置/207360批次，B两版各48几何/6720对，C三版2960/2290/2960套均通过，容量跳过不是设备Pass；NaN全编码专项及CSV/源码/binary绑定分开保存。
- 停止/证据：member2原始/接受6/6，无fail补交；A/B/C=1/5/0且对照计入，今日41/50。STOP、pending空、无自动续交。详见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_a1_compact_prezero_rootpair_3x5/REPORT.md、final_comparison.json、final_audit.json；BAAB漂移标签单独补正，原始计时和所有中位数不变。
- 保留决定：正式仍A1、用户选择待定，不自动融合或部署；A3代理与A2官方case映射未证实，隐藏十项未知。详见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_a1_compact_prezero_rootpair_3x5/REPORT.md、final_comparison.json、excluded_candidates.json。


<!-- a1_cases12_member3_20261025_history -->
## 2026-10-25T23:08:54.797215+08:00 A1 case1/case2 两路与融合（本项完整观察）

- 方法/结论：D1第二级BR8同FP32树根归约，D2独立完整64向量片入口。D2两次777.91/778.92，F2两次777.51/776.37us，A1三次795.57/802.69/797.33us，目标收益重复。A2实际shape/路径未确定；A3大负载约2.4–2.5%的收益不能直接外推到官方其他形状。
- 本项A2实际耗时(us，全部顺序保留)：R01 A1_control_open:795.57; R02 E1_packed_input:801.63; R03 D1_br8_roots:777.46; R04 E2_compact_pitch8_entry:800.28; R05 A1_control_mid:802.69; R06 D1_br8_roots_repeat:778.84; R07 E2_compact_pitch8_entry_repeat:796.5; R08 F1_D1_E2:785.97; R09 E2_compact_pitch8_entry_third:797.61; R10 F1_D1_E2_repeat:782.53; R11 D2_isolated_entry:777.91; R12 D2_isolated_entry_repeat:778.92; R13 A1_control_late:797.33; R14 F2_D2_E2:777.51; R15 F2_D2_E2_repeat:776.37。每次完整五项与SID见REPORT，不拼跨版本最小值。
- 分层验证：D1/D2 fresh 35套/9222配置，E1/E2/F1/F2 fresh 45套/23131配置，含holdout，FP32全位、NaN payload/符号、零符号、guard/input/漏写检查通过。D2/F2各432组UB阈值回退通过。D1 raw 192数据集/73728 uint32为D1表达式专项；融合复用边界单列，不称融合raw binary运行或动态race检查。
- 证据边界：完整同次五项/SID/SHA/分数排名观察时间、慢记录与分层证据见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_a1_cases12_member3_2x5_merge5/REPORT.md、final_comparison.json、candidate_registry.json、final_audit.json。A3代理不是A2官方shape，隐藏十项未知。 case编号仅组织观察，不代表已知shape或专属路由；静态/设备/A2结论分开。
- 决定：member3原始/接受15/15，D/E/M=5/5/5（对照和复测计入），无补交/换号/跨日。STOP、pending空、全部root任务完成；两个GPT-6.1-sol Max子agent已关闭。 正式继续A1，用户选择前不替换；整体完整SHA与经验见history.md本轮条目。


<!-- cases12_F2_selected_20261025_history -->
## 2026-10-25T23:28:52.996269+08:00 F2已由用户选择并部署

- 正式F2 SHA b23f7c906666d2ce734812e6ab4b9c59faa5aca2eed17c5fd419cb32815ac149，原A1保存，完整源与部署审计见整体history本轮条目。
- 本项两次A2记录 777.51/776.37us，完整同次五项及SID保留于 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_a1_cases12_member3_2x5_merge5/REPORT.md；隐藏十项未知。
- 此次部署新增POST/编译/NPU均0，复用同SHA验证；不将此项或其他项跨版本最小值拼接。
- 用户选择及源审计：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_a1_cases12_member3_2x5_merge5/final_selection.json、post_selection_audit.json。旧轮STOP与15次预算已结束，不自动续交。


<!-- f2_targets600_23_member3_20261025_history -->
## 2026-10-26T03:42:12.027034+08:00 F2 case1：native Div及预取/块分布试验（未达600us）

- 严格实际iters与原树/列row0+0左折叠/eps/native Div保持。A3 iters斜率显示迭代依赖约89%，阶段列归约43.5%属于插桩代理，不能直接当A2占比。
- D6两次A2 756.66/756.53us；D10隔离入口760.77/760.85us；D26预取754.87/756.69us，与D6基本同水平，未证明额外官方收益。全部完整向量与SID在本轮REPORT。
- M3融合两次755.72/755.52us；收尾F2 777.56us，case1约快2.8%，仍距600us约155us。case4代价与case3/5慢记录不删除。
- D27严格按位33546240 words、真实Process/UB/whole通过；A3直接父版BAAB 741.41对740.56us，无新增收益，0次A2。逐行API/WR64/布局/BR路线负面结果保留，不重复宣传继承收益。
- 正式F2不变；本轮D9/10、全路25/30，STOP与pending空，剩余配额保留。证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_f2_targets600_23_member3_2x10_merge10/REPORT.md、final_comparison.json、candidate_registry.json、final_audit.json。


<!-- m3_repeat_two_20261026T074934_history -->
## 2026-10-26T07:55:55.595891+08:00 M3追加两次：case1稳定性观察

- 同一冻结M3 SHA e5ad93b67d0e7f6ddf6f23a60ccacb186bee6d401d5bfd9451af100edc745943，仅复测，正式F2不变，原实际iters/求和/eps/native Div保持。
- 本项四次A2 us（按顺序、包含慢值）：755.72 / 755.52 / 756.89 / 755.60；新增两次为756.89 / 755.60。完整同次五项与SID见追加REPORT。
- 四次范围755.52–756.89us、范围/中位数0.181%；样本数4、新旧相隔数小时且无新增F2对照，仅描述观察，不宣称后续稳定或跨版本因果收益。
- 请求追加2/2完成；累计member3 27/30、融合M8/10，STOP恢复、无pending；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_f2_targets600_23_member3_2x10_merge10/m3_repeat_two_20261026T074934/REPORT.md、stability_analysis.json，累计final_audit绑定27次。


<!-- M3_selected_20261026_history -->
## 2026-10-26T08:06:10.176111+08:00 用户选择M3作为新正式基线

- 用户明确选择M3为正式基线；正式kernel.asc复制冻结原字节，SHA e5ad93b67d0e7f6ddf6f23a60ccacb186bee6d401d5bfd9451af100edc745943。父F2 SHA b23f7c906666d2ce734812e6ab4b9c59faa5aca2eed17c5fd419cb32815ac149保存在本轮selection目录。
- 复用同SHA既有A3分层验证及四次A2 Pass，快照/服务端回显逐一一致；本项记录：755.72 / 755.52 / 756.89 / 755.60 us；同次五项/SID见selection.json。保留慢值，不拼接最小值或声称全部case稳定提高。
- 此次新增POST/编译/NPU均0；原iters/求和次序/eps/native Div不变，官方七文件不变。
- 累计member3 27/30，D9/E10/M8；剩余D1/M2共3次明确冻结，STOP保持、无pending和后台任务；后续仅分析600us/2.3us目标。
- 选择、父版、全向量及部署审计：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_f2_targets600_23_member3_2x10_merge10/selection_M3_20261026/selection.json、post_selection_audit.json；当前指针 /mnt/workspace/enjoy_ur_time/the_thing_u_must_know/current_baseline.json。


<!-- M3_analysis_20261026_history -->
## 2026-10-26T08:22:02.242811+08:00 M3基线后只读瓶颈分析

- 正式M3保持，四次case1=755.72/755.52/756.89/755.60us；只读分析未新测。
- 每token20次列归一化、两条127-repeat Add/次，5080源级repeat，原row0+0/行序保持；19轮228个源码VectorDone不等于ISA数。
- 研究原位双token初步156928B，旧packed tail不能直接扩128；256行回绕、scratch与实际UB先证明，尚无实现/收益证据。
- D25等退化、D27无父版增量保留，A3/A2分开；详见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_f2_targets600_23_member3_2x10_merge10/selection_M3_20261026/analysis/REPORT.md；剩余3次冻结。


<!-- m3_inplace2_singleowner_20261026_history -->
## 2026-10-26T09:25:43.144861+08:00 M3新轮case1观察（正式M3保持）

- 方法/结论：D1/D2/D3原位双token三种实现，各44suite/13770配置严格通过，A3与配对M3相比慢8.22%/7.86%/9.22%，均未送A2；减少源码调用数没有减少列左折叠及矩阵运算量。
- 本项全部官方顺序记录：R01 E1_SingleOwner=755.88us；R02 M3_control_E=755.41us；R03 E2_OwnedExtent=754.59us；R04 E2_OwnedExtent_repeat=755.54us；R05 E2_OwnedExtent_third=754.23us；完整同次五项、SHA/SID和慢记录见整体history及REPORT，不拼接最小值。
- 原实际iters/FP32树/row0+0/eps/native Div保持；A3与A2分开，官方shape/branch命中及隐藏十项未知。600us/2.3us目标未达。
- 新轮member3实际D/E/M=0/5/0，未融合，剩余5/0/5保留；旧D1/M2冻结，STOP、pending空、两agent关闭；正式M3未改，候选由用户选择。证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_m3_inplace2_singleowner_member3_2x5_merge5/REPORT.md、final_comparison.json、final_audit.json。


<!-- m3_cumulative_coeffshare_20261026_history -->
## 2026-10-26T11:43:15.103892+08:00 数学优化轮case1观察（正式M3保持）

- 方法/结论：累计行列因子→整行加权→eps状态/Gamma与末尾W复用；三版数值通过但目标项均慢于M3。
- 本项全部A3代理实际耗时us：D1_CumulativeTile64:931.58（配对M3 741.29）；D2_CumulativeFullRow:767.02（配对M3 742.18）；D3b_EpsStateReuse:760.24（配对M3 740.58）；E1_ColumnCoeff:741.20（配对M3 740.61）；E2_SoftmaxCoeff:741.86（配对M3 741.12）；E3_ColumnCoeffInitReuse:742.73（配对M3 741.36）；A3与A2分开，本轮A2 POST=0，无候选官方耗时。完整同次五项及SHA见整体history和REPORT。
- 六版在本轮有限测试集内通过1e-5组合容差/独立reference，非M3逐位等价；原iters/索引树/row0+0/eps/nativeDiv保持。旧D3未设备运行，native全域误差与动态低UB/EPS缺口单列，不从隐藏形状推断路径。
- 新D/E/M各5次未用，旧13冻结；STOP、pending空、全部任务结束、两agent关闭；未融合/部署，用户选择待定。证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_m3_cumulative_coeffshare_member3_2x5_merge5/REPORT.md、final_comparison.json、candidate_registry.json、final_audit.json。


<!-- requested_D3b_E3_once_20261026_history -->
## 2026-10-26T12:21:43.565254+08:00 D3最终版/E3指定官方各一次

- 方法/范围：用户指定最终D3b与E3各member3一次官方验证，无代码修改；原iters/索引树/eps/nativeDiv保持，正式M3不变。
- 本项A2完整观察：D3最终D3b=774.20us（SID6aded3df1dac5d235b3052f3）；E3=757.72us（SID6aded4be1dac5d235b30d5a8）；两次整体Pass、源快照/服务端一致，完整同次五项与SHA见整体history和追加REPORT，不拼接最小值。
- 单次结果不证明稳定；A3原退化记录保留，隐藏十项未知，无新M3同期对照，不据跨时段差值宣称因果收益。
- 本轮累计2/15、D/E/M=1/1/0，余4/4/5与旧13冻结；STOP、pending空，不融合/部署或额外复测。证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_m3_cumulative_coeffshare_member3_2x5_merge5/requested_D3b_E3_once_20261026/REPORT.md、final_audit.json。


<!-- m3_coltree_singleexp_20261026_history -->
## 2026-10-26T13:24:48.517187+08:00 列树/单Exp轮case1观察（正式M3保持）

- 本项全部A2观察：M3_control_D_open=755.13us SID6adeddb61dac5d235b36c598；D1_ColumnBinaryTree=647.10us SID6adedf451dac5d235b3857de；D3_ColumnTreePrefetchOnly=645.23us SID6adee2db1dac5d235b3ac48d；D3_ColumnTreePrefetchOnly_repeat=647.56us SID6adee3b81dac5d235b3b5c4a。完整同次五项与完整SHA见整体history及REPORT，单次记录不证明稳定。
- 三版列树/四版单Exp实际CANN与A3正确性/reference通过；严格iters/FP32/eps/nativeDiv、原行树保持，仅列树允许改变。D有位差，E仅在本轮执行suite逐位一致。
- A3全部同SHA配对五项及慢phase保留于REPORT/final_comparison。case1代理确认prefetch、case3/5代理generic、case4代理scaled_batch；官方隐藏形状/路径未知。单Exp四版无目标收益，不送A2；未融合。
- 正式M3及官方七文件/current_baseline不变，候选由用户选择。member3本轮用量{'D': 4, 'E': 0, 'M': 0}，承接余额{'D': 0, 'E': 4, 'M': 5}与旧13冻结；STOP、无pending、全部任务完成、两个agent关闭。证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_m3_coltree_singleexp_member3_4x4_merge5/REPORT.md、final_audit.json。


<!-- selected_D3_E2b_once_20261026_history -->
## 2026-10-26T14:13:33.635489+08:00 D3新基线与E2b一次探针case1

- 正式D3 SHA 29fd214a4268c776c7de28d748299f339903f25421f97ba1e89ff7036e1bdec4已部署并核对原字节，M3备份；原iters/FP32/eps/Div/行树保持，仅原允许列树变化。
- 现成E2b（M3父版、非融合）一次A2观察：754.35us，SID 6adeee581dac5d235b438567，整体Pass及source/server一致；完整五项见整体history/REPORT，不拼接最小值。E2b不部署，单次不证明稳定收益。
- A3负面证据保持；本次没有新增算法代码或A3实验，仅探针默认官方sample前置与一次POST。当前正式D3既有完整同SHA记录继续保留，隐藏路径未知。
- 累计D/E/M=4/1/0，剩余0/3/5及旧13冻结，STOP恢复、无pending；后续仅分析。证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_m3_coltree_singleexp_member3_4x4_merge5/selection_D3_and_E2b_probe_20261026/REPORT.md、final_audit.json。

只读后续分析：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_m3_coltree_singleexp_member3_4x4_merge5/selection_D3_and_E2b_probe_20261026/analysis/REPORT.md；新方案未实现/编译/运行/提交，原生Div和固定iters保持。


<!-- d3_rowfold_absreuse_20261026_history -->
## 2026-10-26T15:57:13.759734+08:00 行折叠/Abs复用轮 case1

- 行归约与因子倒数路线未形成明确收益。全部7份有效A3候选的同版本完整五项、配对D3和慢phase保留，2个精度失败保留原始日志；详见整体REPORT和COST_AND_DECISION.md。
- E1一次A2本项646.23us，完整646.23/2.41/15.49/83.43/64.08us，SID6adf04b91dac5d235b548b9c、SHA6b7e98276d00de53ec223a9c8fcb1243b996ef1de9fc0df5d6bb06ff17a7fe2a；Pass及source/server匹配，单次非同期对照不证明稳定收益。
- 正式列树D3 SHA29fd214a4268c776c7de28d748299f339903f25421f97ba1e89ff7036e1bdec4保持；严格实际iters/FP32/eps/行→列阶段，用户允许求和树/Div实现试验。未融合/部署，候选留待用户选择。
- 本轮D/E/M用0/1/0、余5/4/5暂存、旧21冻结；STOP、无pending、全部任务终态、agent关闭。证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_d3_rowfold_absreuse_member3_2x5_merge5/REPORT.md、final_comparison.json、final_audit.json。


<!-- d3_weighted_singlevector_20261026_history -->
## 2026-10-26T17:36:11.799812+08:00 分块加权归约/单repeat轮 case1

- D原语成本门失败，未有完整case1候选；E2本项略慢，600us未达。本轮实际官方记录：R01 D3=646.32us；R02 E2=650.77us；R03 E2=652.95us；R04 D3=646.48us；R05 E2=650.96us；完整同次五项与SID/源SHA见整体history本轮条目及REPORT。
- E1/E2全native/reference已执行测试逐位D3一致；单repeat矩阵和mask复用保持全部iters/FP32/eps/nativeDiv/原归约。D仅原语诊断，不能把54.82/150.99/137.38us写作本case完整算子耗时；源/设备/ISA边界详见报告。
- 正式D3 SHA29fd214a4268c776c7de28d748299f339903f25421f97ba1e89ff7036e1bdec4未改；E2 SHA24146d8e78edebc792116d4ac28eb3b6c54a1c2b05914b834ba0aa63a732a6ce未部署，选择权留给用户，无融合版。
- 新D/E/M用0/5/0、余5/0/5暂存，旧35冻结；member1完成5次，STOP/pending空/14job终态/两agent关闭。证据/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_d3_weighted_singlevector_3accounts_2x5_merge5/REPORT.md、version_choices.json、final_audit.json，公共细节引用整体历史。


<!-- selected_E2_analysis_20261026_history -->
## 2026-10-26T18:15:35.229058+08:00 用户选择E2并完成只读计算过程分析

- 正式kernel.asc已由D3切换到冻结E2原字节，SHA 24146d8e78edebc792116d4ac28eb3b6c54a1c2b05914b834ba0aa63a732a6ce；D3 SHA29fd214a4268c776c7de28d748299f339903f25421f97ba1e89ff7036e1bdec4备份 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_d3_weighted_singlevector_3accounts_2x5_merge5/selection_E2_20261026/before/production_D3.asc。官方七文件、旧campaign/STOP/报告未变。
- 三次E2既有A2 Pass均已fresh GET复核，source/snapshot/server八文件一致。完整同次五项650.77/2.29/15.27/81.40/61.53、652.95/2.28/16.85/84.16/70.96、650.96/2.33/15.56/83.46/62.54us及SID见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_d3_weighted_singlevector_3accounts_2x5_merge5/selection_E2_20261026/REPORT.md；保留全部慢记录，case2非每次<2.3、case1未达600。
- case1：初始softmax仍逐元素Div，H128可尝试小向量nativeDiv(1,sum)后Mul；逻辑Div16384→128但新增Mul和因子依赖，初始化只执行一次，不保证7.83%总节省。 计算公式/成本/旧失败方向与证据缺口见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_d3_weighted_singlevector_3accounts_2x5_merge5/selection_E2_20261026/analysis/REPORT.md、plan.json、API_evidence.json。
- 新增算法改动/编译/NPU/POST/子agent均0。既有native/reference结果不冒充新运行；A3仍为代理、A2官方及隐藏未知分别记录；实际iters/FP32/全部eps与阶段依赖保持。
- 余D5/E0/M5及旧35冻结，原STOP保留、pending空、两agent已关闭，无后台续交；选择和最终审计见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_d3_weighted_singlevector_3accounts_2x5_merge5/selection_E2_20261026/selection.json、final_audit.json，后续新实验/POST需新指令。


<!-- e2_softmaxinv_blockstats_exppack_20261026_history -->
## 2026-10-26T19:41:01.981949+08:00 E2计算过程优化轮 case1

- D1b只改初始softmax倒数复用，D2进一步融合eps；正eps完整验证通过，非正eps原路径回落。A3只有0.29–0.47%，一次D1b A2为646.45，600未达，未晋级/融合。
- 本轮实际官方记录：R01 E2_control_E_open=651.24us；R02 T3b_screen=647.39us；R03 E2_control_E_postreconnect=651.60us；R04 T3b_repeat1=648.76us；R05 T3b_repeat2=649.02us；R06 D1b_nativeDiv_diagnostic=646.45us。完整五项/SID/各源SHA统一见整体history同轮条目及 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_e2_softmaxinv_blockstats_exppack_3accounts_2x5_merge5/REPORT.md。
- 已执行的设备/reference、A3和A2分别记录，原始失败/FP32位差/慢记录保留；各候选精确证明及未验证边界见COST_AND_DECISION.md、validation_totals.json、官方source绑定。
- 正式E2 SHA24146d8e78edebc792116d4ac28eb3b6c54a1c2b05914b834ba0aa63a732a6ce和官方七文件/current_baseline不变；T3b、D1b候选未部署、没有融合。用户选版前不再优化或提交。
- 新D/E/M用1/5/0，余4/0/5与旧45冻结；member1用6、另两账号0。STOP/pending空/任务终态/两agent关闭，最终审计 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_e2_softmaxinv_blockstats_exppack_3accounts_2x5_merge5/final_audit.json。

## 2026-10-27T17:43:33.369234+08:00 四路与融合完成，待用户选版

- 四路按用户指定GPT-6.1-sol Max配置交付，父端串行编译/NPU/POST；九个独立冻结源保持实际iters、FP32、各eps及nativeDiv。正式R1b SHA db11daeffeef6973696b1d9692c34b2b043a60c0b73815ac81d998e46fb8faa2未改。
- B1/B2目标case4、C1目标case2重复改善后融合M1/M2，交错各两次A2及共享前后R1b控制；完整逐SID五项、同SHA中位和范围供用户选版，A/D目标收益不足不硬融，全部慢记录保留。
- 九源362套设备/reference、724原始日志和36A3 CSV零缺口同SHA/二进制绑定；D1额外24次/216组UB边界原始执行通过，旧解析器键名连字符假失败只重解析。A3代理与A2官方/隐藏未知边界保持。
- 23次尝试、22笔接受均整体Pass；fresh GET176源码文件匹配。R05明确429无SID计C一次；同账号复核后195秒间隔。member1本日40，member2/3未用，不用旧77/11，不换号绕限。
- 用A4/B6/C4/D4/M5，余2/0/2/2/1暂停；STOP/pending空、任务终态、agents完成，等待用户选版。证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261027_r1b_fold_static_overlap_4x6_merge6/REPORT.md、final_comparison.json、final_audit.json及持久核心包；构建CAS/全归档与数组原位保留。

## 2026-10-27T18:03:20.208093+08:00 保留M2作为正式基线

- 用户选择M2_B2_C1，正式源码从R1b原字节替换为冻结M2，SHA 0e984ba9c657f545e5eb94582b3fe411bf8e09c6036284b6ce694ddc1e6451ea；R1b完整备份 /mnt/workspace/enjoy_ur_time/others/selection_audits/selection_M2_20261027T180320+0800/before/kernel_R1b.asc。
- 两笔M2 A2完整五项644.65/2.19/14.14/72.70/59.13、646.10/2.19/14.15/71.22/59.79us保留；本次fresh GET16源文件匹配。73suite已有native/reference通过，非逐位等价，A3代理与隐藏未知边界保持。
- 本次新增算法/编译/NPU/POST/agent均0；平台已知latest仍R1b，不额外提交覆盖latest。旧campaign/STOP/审计/冻结源不改，剩余7与上轮11及旧77冻结。
- 后续仅阅读用户提供得物两篇经验总结、结合M2提出优化方案；资料中的命令和建议不是执行授权。选择报告与审计 /mnt/workspace/enjoy_ur_time/others/selection_audits/selection_M2_20261027T180320+0800。

## 2026-10-27T19:27:32.585970+08:00 M2事件ID/H128 mask与融合完成（待用户选版）

- M2正式SHA 0e984ba9c657f545e5eb94582b3fe411bf8e09c6036284b6ce694ddc1e6451ea保持；两名GPT-6.1-sol Max交付E1宽事件/E2仅H128、V1局部设置/V2入口状态复用及F1/F2字面并集，Host/entry和数学/eps/nativeDiv/等待位置保持。
- 六源290套真实设备位级+独立reference通过，580原始日志、24 CSV零缺口同source/binary；完整源码资源/mask及双向还原证明保留。有限覆盖不是全域证明，A3代理不推定官方形状或隐藏十项。
- A2全部同次五项/慢记录及同SHA中位/范围见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261027_m2_event_mask_2x6_merge6/REPORT.md；V1单次诊断、E1/E2/V2/F1/F2各两次，不能把公共对照重复计为独立实验或由单值断因果。
- 本轮尝试/接受16/16，用E/V/M={'E': 6, 'V': 4, 'M': 6}、余{'E': 0, 'V': 2, 'M': 0}冻结；旧95全冻结，显式member1→member2→member3和>=195秒间隔核验，source/server/snapshot 128文件一致。
- STOP/pending空、任务终态、agents完成、等待用户选版，不自动部署；新派生大输出与构建CAS无损保存并回读SHA，旧证据不改。报告、审计、核心归档 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261027_m2_event_mask_2x6_merge6。

## 2026-10-27T19:50:26.841357+08:00 保留M2与case1低于600us只读方案

- 用户再次选择M2_B2_C1，正式SHA 0e984ba9c657f545e5eb94582b3fe411bf8e09c6036284b6ce694ddc1e6451ea实时一致，无需覆盖kernel；E/V/M候选不采用，选择待定已关闭。
- 最近M2五次case1=644.77/646.32/645.68/646.31/644.66us，中位645.68；完整同次五项与慢值保留在原campaign。A3 Vector占主导仅代理，官方case1 shape/隐藏详情仍未知。
- 新方案优先列树独立scratch与768B根行距，针对两个源的相对bank group及原位读写；另列双token独立阶段错峰、FP32局部转置归约、多核适用条件，明确旧失败与资源/数值风险，无已验证600us保证。
- 新增候选/编译/NPU/POST/agent均0，STOP/pending空，剩余V2及旧95共97冻结；旧campaign、冻结源、受保护七文件不改。报告与审计 /mnt/workspace/enjoy_ur_time/others/selection_audits/selection_M2_case1_sub600_20261027T195026+0800。

## 2026-10-27T21:48:43.061579+08:00 M2列树scratch/双token错峰/FP32转置与融合完成（待用户选版）

- 三名GPT-6.1-sol Max交付A0/A0b/A1/A-mask、B1/B2、C1/C2/C2b/C3/C4及M1设计融合共12源；M2正式SHA 0e984ba9c657f545e5eb94582b3fe411bf8e09c6036284b6ce694ddc1e6451ea始终未改。
- 616主套件+12融合与C3直比共628真实A3数值/reference检查，1256原始日志、52 CSV；重排逐位差异、UB阈值/未知query证明边界保留，严格iters/FP32/eps/nativeDiv不变。
- A2尝试/接受16/16，全Pass、五项可见Pass、隐藏十项未知；全部同SHA完整五项及慢记录见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261027_m2_scratch_stagger_transpose_3x6_merge5/REPORT.md；case1无<600，A0b两次643.50/642.58us小信号，不自动提升或拼跨版最小值。
- 已用A/B/C/M={'A': 6, 'B': 4, 'C': 5, 'M': 1}，余{'A': 0, 'B': 2, 'C': 1, 'M': 4}共7与旧97累计104冻结；实际最短间隔195.204611秒，均显式member2，日用{'member1': 50, 'member2': 22, 'member3': 0}。R02空间guard在POST前拦截，未发请求，失败准备及无损恢复证据保留。
- STOP有效、pending空、任务终态、优化agent完成；新源/二进制/输入/输出/源码server逐项绑定，受保护七文件及旧证据不变，等待用户选择。报告、完整比较、审计及核心归档 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261027_m2_scratch_stagger_transpose_3x6_merge5。

## 2026-10-27T23:13:38.580880+08:00 M2一次转置/双向常驻/累计因子/角色交换轮完成（待用户选版）

- 一名GPT-6.1-sol Max实现及独立归档审计已完成，STOP有效、pending空、全部有限任务终态，无自动续跑。正式M2 SHA 0e984ba9c657f545e5eb94582b3fe411bf8e09c6036284b6ce694ddc1e6451ea保持，候选冻结待用户选版；本块覆盖下方active及旧待选状态。
- 新6次全部尝试/接受6/6（含首尾M2控制），余0；旧104全部冻结，未挪用、不补偿。member1→member2→member3顺序，本轮均显式member2；结束日用{'member1': 50, 'member2': 28, 'member3': 0}。真实最短POST间隔195.210298秒，日50为工作流策略非server公布上限。
- V1完整双视图累计/角色交换，V2列面板，V3独立操作共组，V4 FP32 MulAddDst分母；nativeDiv/实际iters1..32/每个eps/只读输入/完整输出/单kernel保持。四源264主套件+2冒烟共266真实A3数值/reference、532原始日志、16 CSV绑定；A3代理与A2/隐藏未知分开。
- 六次A2均Pass，候选case1=819.03/761.60/762.63/765.35us，首尾M2=644.91/645.36us，未达600且无候选收益。全部同SID完整五项/慢值保留，不拼最小值，不自动部署。
- 完整证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261027_m2_dualview_cumulative_swap_6/REPORT.md、final_comparison.json、version_choices.json、fresh_official_audit.json、runtime_content_audit.json、independent_runtime_content_audit.json、final_audit.json及durable_core_evidence.tar.gz。独立复原1496逻辑文件/785压缩路径，旧证据不改，CSV和原始验证日志直读；未经新授权不再算法修改/编译/NPU/POST/启动优化agent。


## 2026-10-28T01:35:43.424469+08:00 M2 UB布局三路与融合完成（待用户选版）

- 本项所有同SID实测（us）：R01=647.29; R02=712.48; R03=641.82; R04=642.02; R05=702.48; R06=640.87; R07=640.29; R08=675.41; R09=639.35; R10=644.81; R11=641.32; R12=606.92; R13=607.28; R14=608.54; R15=644.92。完整五项/完整SHA/SID /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261028_m2_ub_coloring_3x5/REPORT.md；不拼最小值。
- 正式M2 SHA 0e984ba9c657f545e5eb94582b3fe411bf8e09c6036284b6ce694ddc1e6451ea保持，候选冻结待用户选版。共同方法/完整分层验证见整体HISTORY；本地代理不确认官方shape或分派。
- B4源两次case1改善，但case3/5复测出现慢记录；A2隐藏十项细节未知，不能据一个点认定全项稳定改善。
- 本轮15/15终态，新余0及旧104冻结，STOP有效/pending空/无自动续跑；源码/原始回执/设备日志/CSV/归档SHA/独立终审见本轮final_audit.json。


## 2026-10-28T09:51:23.248440+08:00 用户保留B4为基线并开展只读细节分析

- 正式源码由M2原字节切换至冻结B4 SHA e7827703d3b4945241bb231d69347cd29c212a0fd0fc9e9af7b4effde80f41b2，M2 SHA 0e984ba9c657f545e5eb94582b3fe411bf8e09c6036284b6ce694ddc1e6451ea完整备份于 /mnt/workspace/enjoy_ur_time/others/selection_audits/selection_B4_analysis_20261028T095123+0800/before/kernel_M2.asc；官方七文件/旧campaign/STOP/证据不变。
- B4两笔已接受A2 Pass完整五项606.92/2.14/14.27/72.62/61.13、608.54/2.16/16.85/72.69/70.48us保留；本次两snapshot16文件重新哈希，沿用既有fresh GET，不宣称新GET。A3原54suite/reference通过且非逐位M2，隐藏十项细节未知。
- 本轮仅选现成版及只读分析，新增算法改动/编译/NPU/POST为0；两名只读分析agent无执行/写入权。严格iters/FP32/每eps/nativeDiv保持。
- 旧104冻结、上轮15全用余0、STOP/pending空/不自动续跑；平台latest最后已知M2不同于本地正式B4，不自动追加提交。case1中位607.73us，到600需减少约7.74us（1.27%），细节方案未实现/验证。
- 选版报告和审计 /mnt/workspace/enjoy_ur_time/others/selection_audits/selection_B4_analysis_20261028T095123+0800/REPORT.md、audit.json；新的只读分析 /mnt/workspace/enjoy_ur_time/others/selection_audits/selection_B4_analysis_20261028T095123+0800/analysis/REPORT.md。本条覆盖此前候选待选状态，不修改历史原结果。

本次只读细节分析完成：P1死亡根分母换址（2I-1阶段/无新增算术UB屏障）、P2布局判断外提、P2b显式nativeDiv64x2，P3softmax FMA明确额外舍入差异，P4最大值scratch相位。D4跨半根和泛化延迟MTE3因旧负面证据不主推。所有收益未测；完整 /mnt/workspace/enjoy_ur_time/others/selection_audits/selection_B4_analysis_20261028T095123+0800/analysis/REPORT.md。


## 2026-10-28T12:00:28.347488+08:00 B4死亡根/布局/softmax FMA三路与融合完成（待用户选版）

- 本项全部同SID官方实测（us）：R01=605.04; R02=613.81; R03=604.92; R04=606.96; R05=613.23; R06=605.57; R07=607.01; R08=606.44; R09=607.77; R10=607.72; R11=612.09; R12=608.32; R13=607.7; R14=606.2; R15=597.99; R16=613.72; R17=602.18; R18=607.65; R19=600.49; R20=607.25。完整五项/SHA/SID /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261028_b4_deadroots_layout_fma_3x5_merge5/REPORT.md，慢记录保留、不拼最小值。
- 正式B4 SHA e7827703d3b4945241bb231d69347cd29c212a0fd0fc9e9af7b4effde80f41b2始终保持，三路与融合候选由用户选。共同方法与独立分层验证见整体HISTORY。
- B5单次case1=597.99us；其他候选和融合不预设收益相加，不把A3计时推成A2或推定官方shape/隐藏。
- 本轮20/20终态，新A/B/C/M各5用尽、旧104冻结；STOP有效/pending空/无自动续跑。证据与核验见本轮REPORT/final_audit。

<!-- final-results:campaign_20261028_b5_short_stats_gates_3x5_merge5 -->
## 2026-10-28T14:18:22.547085+08:00 B5三路与融合轮case1完成（待用户选版）

- 本项全部同SID官方实测（us）：R01/6ae17dcc1dac5d235b1153bd=598.46; R02/6ae183271dac5d235b14eb48=599.35; R03/6ae183eb1dac5d235b156d79=602.64; R04/6ae184ae1dac5d235b15f65e=598.22; R05/6ae185711dac5d235b168191=602.00; R06/6ae186571dac5d235b172824=599.84; R07/6ae187551dac5d235b17d4b0=600.65; R08/6ae188511dac5d235b187faf=599.91; R09/6ae189531dac5d235b19410e=597.51; R10/6ae18a171dac5d235b19d479=599.42; R11/6ae18ada1dac5d235b1a5555=598.99; R12/6ae18b9d1dac5d235b1ad40c=598.41; R13/6ae18c661dac5d235b1b6e9f=599.82; R14/6ae18d291dac5d235b1c28e6=602.77; R15/6ae18ded1dac5d235b1cfe81=599.74; R16/6ae18eb01dac5d235b1d96b1=601.82; R17/6ae18f731dac5d235b1e2520=599.16; R18/6ae190361dac5d235b1eb4bb=602.19; R19/6ae190fa1dac5d235b1f67d8=598.22; R20/6ae191bd1dac5d235b200321=598.55。完整五项/SHA/账号/SID见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261028_b5_short_stats_gates_3x5_merge5/final_comparison.json；每笔完整记录保留，不拼最小值。
- 同SHA描述统计（不代表一次实测）：B5_FastPredicateHoist n=3 median=598.55 [598.46,599.82]；A1_UpperShortMode n=1 median=602.00 [602.00,602.00]；B1_DeadStatsS0 n=1 median=598.22 [598.22,598.22]；B2_DeadStatsS8 n=1 median=599.35 [599.35,599.35]；C1_EarlyGateReady n=1 median=602.64 [602.64,602.64]；A2_UpperShortModeMixed n=1 median=599.84 [599.84,599.84]；B3_UpperDeadStatsS0 n=2 median=599.82 [598.99,600.65]；C2_GateDmaGroupedControl n=1 median=599.91 [599.91,599.91]；A3_UpperShortColumnsOnly n=1 median=597.51 [597.51,597.51]；B4_FullStatBlocksDeadS0 n=1 median=599.42 [599.42,599.42]；C3_UpperShortGateReady n=1 median=598.41 [598.41,598.41]；A4_UpperShortRowsOnly n=2 median=602.30 [601.82,602.77]；C4_UpperShortPairGateDma n=2 median=599.45 [599.16,599.74]；M1_UpperRowsPairGate n=2 median=600.21 [598.22,602.19]。n=1无复现，n=2有限重复；统计极值不可组装成一笔向量。
- 正式B5 be52118acd2c2b53f4c4c96a7011af6a7ba039a9469cc48a0b8b06cef3ab5de4保持；本轮方法、B3复测完整五向量及各case慢记录见整体HISTORY与 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_b5_short_stats_gates_3x5_merge5/REPORT.md。B3同SHA各SID均保留，由用户选择，不自动提升。
- 13源/702套真实A3 numeric/reference+strictbits及52 CSV绑定；A3代理不确认A2官方shape、分支或性能。四个原资源配置相关非零作业保留，只有同SHA新full_v2完整通过可作补证。
- 尝试/接受20/20，账号{'member1': 15, 'member2': 5}，分路余{'A': 0, 'B': 0, 'C': 0, 'M': 0}；旧104冻结，终态/STOP/pending空、无自动续跑。最终审计和用户选版入口见 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_b5_short_stats_gates_3x5_merge5/version_choices.json。
<!-- /final-results:campaign_20261028_b5_short_stats_gates_3x5_merge5 -->


<!-- final-results:campaign_20261028_b5_rowinner_blocktoken_1x5 -->
## 2026-10-28T16:04:37.800366+08:00 同行内布局轮case1完整记录

- 正式B5 be52118acd2c2b53f4c4c96a7011af6a7ba039a9469cc48a0b8b06cef3ab5de4 保持；L1/L2冻结完整SHA、源和静态证明见整体history与 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_b5_rowinner_blocktoken_1x5/version_choices.json。
- 本项A2全部实测(us)：R01/6ae1a4301dac5d235b2e1f4b=598.75; R02/6ae1a6211dac5d235b301918=598.92; R03/6ae1a6e41dac5d235b30aa54=600.70; R04/6ae1aaa11dac5d235b335fe4=597.92; R05/6ae1ab641dac5d235b33f33c=598.81。对应同SID完整五项/慢记录见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261028_b5_rowinner_blocktoken_1x5/final_comparison.json，不拼最小值，不把描述统计当一笔实测。
- 两候选各67套真实A3 numeric/reference/strictbits通过，A3计时与A2官方分别记录。本项用于整体回退观察；未据A3代理确认A2官方形状/分支，也不将相邻差异当确定因果。本轮结论与方法见 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_b5_rowinner_blocktoken_1x5/REPORT.md；B5持续正式保留，候选由用户选择。
- 5次新机会全部使用并Pass；旧104冻结，新余0，STOP/pending空、唯一子agentcompleted、无自动续跑。审计 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_b5_rowinner_blocktoken_1x5/final_audit.json；优化记录只写HISTORY，规则/模板原件保持。
<!-- /final-results:campaign_20261028_b5_rowinner_blocktoken_1x5 -->


<!-- selection-host-analysis:L1_20261028T161731+0800 -->
## 2026-10-28T16:40:44.619148+08:00 L1正式选版与Host只读研究

- 用户选定L1，正式SHA 30ac04fcc079bd6e81aecb4f1a66de20bc5cd9017aba96311833fd17bfc25380，原B5及状态备份见整体HISTORY的本次选版目录。未实施Host候选。
- 本项选定SHA官方完整记录(us)：R02/6ae1a6211dac5d235b301918=598.92; R03/6ae1a6e41dac5d235b30aa54=600.70；对应同SID五项、快慢值和原始证据见 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/selection_L1_host_analysis_20261028T161731+0800/REPORT.md 与 selection_provenance.json，不拼最小值。
- Host主线为精确整数分区描述，保持原核数/q/first-end/所有权与全部实际FP32数学；只影响初始化，A2收益未知，不把Device Scalar当CPU时间。资源查询/分派整理为次线，范围与否决条件见整体HISTORY及报告。
- 新编译/NPU/测评/平台GET/POST均0，旧104及零余额继续冻结；STOP/pending空、只读agentcompleted、无新执行授权。正式源与最新官方B5提交不混称，规则/官方模板/旧报告保持原件。
<!-- /selection-host-analysis:L1_20261028T161731+0800 -->


<!-- final-results:campaign_20261028_l1_host_partition_resource_dag_3x5 -->
## 2026-10-28T17:59:17.394635+08:00 L1 Host三路完整结果 case1

- 正式L1保持，SHA 30ac04fcc079bd6e81aecb4f1a66de20bc5cd9017aba96311833fd17bfc25380。P1/P2精确整数分区、U1/U2同调用资源快照、D1/D2分派元数据；6个冻结SHA/审查/证据见 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_l1_host_partition_resource_dag_3x5/version_choices.json。D2仅允许private residentBatch死参数2/4→1，实际消费参数与严格iters/FP32/eps/原sum/nativeDiv保留。
- 本项全部A2实测(us)：R01/6ae1b8d51dac5d235b40130c=597.65; R02/6ae1bb491dac5d235b42169a=603.60; R03/6ae1bccc1dac5d235b432f14=597.39; R04/6ae1bda01dac5d235b43e41a=596.60; R05/6ae1be8a1dac5d235b44aca5=596.93; R06/6ae1bfb11dac5d235b459aab=600.61; R07/6ae1c0d81dac5d235b4679f9=599.42; R08/6ae1c19b1dac5d235b471571=598.06; R09/6ae1c25e1dac5d235b47af44=600.78; R10/6ae1c3211dac5d235b482a88=597.97; R11/6ae1c3e41dac5d235b48bf59=599.58; R12/6ae1c4a81dac5d235b494eaf=598.32; R13/6ae1c56b1dac5d235b49e4ed=598.90; R14/6ae1c62e1dac5d235b4aac91=599.45; R15/6ae1c6f11dac5d235b4b478a=598.04。同SID五项与慢记录见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261028_l1_host_partition_resource_dag_3x5/final_comparison.json，不拼最小值。
- 6候选各67套真实A3 numeric/reference+strictbits通过，共402套、123984次配置执行（非去重）、804实际raw日志、24 CSV；CPU参考1344组/4074文件复用重核，本轮新生成0。HostCPU入队、A3 Device、A2官方分别记录，不互相替代。
- 新额度A/B/C各5次尝试/接受，15/15均Pass，全部member2；member1开场日用50达既有策略50，按授权顺序接续member2，服务端限额未知。最短POST间隔195.194859028秒，旧104冻结、新余0，无融合或额外授权。
- 正式L1与收尾官方一致，用户选择前不自动提升候选。STOP有效、pending空、所有有限作业终态、3名子agentcompleted、无自动续跑。最终审计 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_l1_host_partition_resource_dag_3x5/final_audit.json；优化记录仅HISTORY，AGENTS/README/RULES和官方7文件未改，旧campaign/STOP/审计保持。
<!-- /final-results:campaign_20261028_l1_host_partition_resource_dag_3x5 -->


<!-- final-results:campaign_20261028_l1_case5_pair_earlypack_gatecompact_3x5 -->
## 2026-10-28T20:51:56.578517+08:00 L1 case5三路完整结果 case1

- 正式L1保持，完整SHA 30ac04fcc079bd6e81aecb4f1a66de20bc5cd9017aba96311833fd17bfc25380；六个准入冻结源：A1_PairedWorkBR=a2983953706b18f0443240ec59a020e888f007a96549b2b3ed6328ba61c9ac17; B1_EarlyPackSoftmax=35cefed7f1ee9a485a8179455213d25bfb826da4a718aa903fb9ffbd7c67069d; C1r_GateCompact=3ab07529b03d4d08bddd74e4412844489d5009c49c0847515563c6ccf40e8f3d; A2_PairedContiguousDiv=46e8d86e1c708ab317407dc75bf3d8b323ee7e4f060308fdde2c3ea174c0c2ca; B2_MaxPackSharedFence=832fc4116f89397f6ce486603ffb77278f40ceb9ddea56cc611bdcee00b264a2; C2_GateVectorSeed=b3cda16eca9ecba0c74661386ce445dca52e01abfab918a66222f384c06f0fb3。版本证据 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_l1_case5_pair_earlypack_gatecompact_3x5/version_choices.json 必须保留C2 R14失败与未解决CPU限额风险，用户最终选择；C1默认编译失败源另留。
- 本项可见状态/实测(us)：R01/6ae1d9941dac5d235b592ee1 [Pass]=598.57; R02/6ae1dd531dac5d235b5c1256 [Pass]=599.89; R03/6ae1de161dac5d235b5ca77e [Pass]=603.56; R04/6ae1e02e1dac5d235b5e3a16 [Pass]=601.99; R05/6ae1e16f1dac5d235b5f2267 [Pass]=597.54; R06/6ae1e2321dac5d235b5fcb4e [Pass]=600.74; R07/6ae1e2f51dac5d235b606ef1 [Pass]=600.21; R08/6ae1e3b81dac5d235b60fada [Pass]=600.39; R09/6ae1e47b1dac5d235b618a56 [Pass]=601.68; R10/6ae1e53f1dac5d235b62452a [Pass]=597.65; R11/6ae1e6021dac5d235b62f0eb [Pass]=601.55; R12/6ae1e6c51dac5d235b6399c1 [Pass]=598.76; R13/6ae1e7881dac5d235b642f82 [Pass]=600.66; R14/6ae1e84c1dac5d235b64c118 [Time Limit Exceeded]=599.55 (partial Pass); R15/6ae1eab81dac5d235b66e58f [Pass]=601.65; R16/6ae1eb7b1dac5d235b678345 [Pass]=601.78; R17/6ae1ec3f1dac5d235b6821b8 [Pass]=599.24; R18/6ae1ed021dac5d235b68b329 [Pass]=598.98; R19/6ae1edc51dac5d235b694fd5 [Pass]=602.54; R20/6ae1ee881dac5d235b69f0d5 [Pass]=601.61; R21/6ae1ef4c1dac5d235b6a9610 [Pass]=596.74。raw0保留但TLE/Skipped非0us观察；同SID五项与仅good统计见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261028_l1_case5_pair_earlypack_gatecompact_3x5/final_comparison.json。
- 6源各77套A3 numeric/reference+strictbits，共462套/131976次配置执行（非去重）/924实际raw日志/24CSV；CPU参考1344组/4074文件复用，新生成0，Host/A3/A2分开。严格actual iters/FP32/eps/+0/原sum/nativeDiv/单kernel/只读input/fulloutputs保持。
- R14/6ae1e84c1dac5d235b64c118 C2同SHA b3cda16eca9ecba0c74661386ce445dca52e01abfab918a66222f384c06f0fb3：case1 Pass599.55us、case2 TLE、case3–5 Skipped、隐藏未知。[Evaluation CPU limit exceeded] case 1 round 42: thread CPU 6279.61us exceeds 5000us and 50x device time (2.180us)。CPU6279.61us超过5000us及50×2.180us；根因未知，不直接归因平台noise或Device死锁。原始raw0保留但不是0us观察，失败计C路额度且不补偿。 A1首次计时copied baseline无执行位，mode-only修复另作计时；C1 const mask默认编译失败，独立C1r修正并验证；A1初次CPU proof定位错误留档。sequence_final_extended rc1由R14后SUBMIT_HOLD拦截，原件保留；CPU审查仅恢复原剩余7项，sequence_after_R14_CPU_review最终rc0。不得称所有作业rc0。
- 新A/B/C各7/7、21/21尝试接受：20Pass+精确R14失败，均member2；最短POST间隔195.208918333秒。失败消耗额度不补偿，旧104冻结、新余0、STOP/pending空、作业终态/3agentcompleted，无自动续跑或融合。审计 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_l1_case5_pair_earlypack_gatecompact_3x5/final_audit.json；正式L1待用户选版，C2 CPU风险未解决。
<!-- /final-results:campaign_20261028_l1_case5_pair_earlypack_gatecompact_3x5 -->


<!-- retained-L1-hidden-handoff:20261028T213644+0800 -->
## 2026-10-28T21:36:44.092389+08:00 保留L1与分析交接

- 用户明确保留L1_RowInnerCompactDen，正式SHA 30ac04fcc079bd6e81aecb4f1a66de20bc5cd9017aba96311833fd17bfc25380；实际源码已实时核对一致，本次无源码写入。
- 最新L1官方SID 6ae1ef4c1dac5d235b6a9610，完整五项(us) 596.74/2.15/14.53/72.79/60.93；此前完整同SHA/慢/失败原件见 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_l1_case5_pair_earlypack_gatecompact_3x5/REPORT.md，不修改旧证据。
- 实时状态解除待选，旧campaign/STOP与旧报告保持原件；选版记录 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/selection_L1_hidden_analysis_handoff_20261028T213644+0800/selection.json；新余0、旧104冻结、pending空，无自动续跑/编译/NPU/提交或子agent授权。
- 为新对话准备隐藏工作负载只读分析指令 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/selection_L1_hidden_analysis_handoff_20261028T213644+0800/HANDOFF_PROMPT.md，区分事实与假设，先审查全参数族分派/回退与评分依据；本次没有开始隐藏case优化。
<!-- /retained-L1-hidden-handoff:20261028T213644+0800 -->

<!-- campaign-L1-hidden-member3-20:campaign_20261028_l1_hidden_families_member3_20 -->
## 2026-10-29T00:37:58.350618+08:00 member3隐藏参数族六版各3次与L1开闭对照

- 本轮按新授权使用member3固定账号，20次POST/20接受/20总体Pass，旧104全部冻结；每个结果为公开5 Pass+10 Hidden，隐藏逐点状态/耗时/shape未暴露；源码snapshot/server全部8文件已独立核对。所有原始SID、完整同SHA五项向量、首个SID匹配榜单观测及慢记录均保留。
- 本case按原始轮次记录，不拼接跨轮最小值：L1_RowInnerCompactDen: R01=597.3, R20=598.76 us; A1_P56DeadPanel: R02=600.37, R08=598.76, R14=598.17 us; B1_WideQ1InPlaceControl: R03=600.84, R09=604.23, R15=603.96 us; C1_L1FullQPartition: R05=598.41, R10=597.44, R16=598.66 us; D1_GenericDeadMatrixPrefetch: R04=599.15, R11=599.52, R17=598.86 us; B2_WideOriginalMathBatch: R06=602.91, R12=601.64, R18=602.44 us; A2_P56EvenCompactQ8: R07=599.01, R13=599.5, R19=599.47 us。
- 分数/排名与该case其他4项共同构成每笔完整向量，详见/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_l1_hidden_families_member3_20/REPORT.md及CSV；不从单项或总分识别隐藏工作负载。
- A3严格baseline位型和独立CPU reference分层通过；A2候选补齐65条/实际1144配置，共194套；六版24族ABBA+BAAB共48phase，逐phase保存launch36端点/CAS并核SHA，端点与L1相同，不宣称每launch/全域。新q8五族geo约+29.7%、B2真实9族约+26.7%；B1/C1负例、A2 H22退化完整保留，均不当作官方A2整体收益。
- 正式L1_RowInnerCompactDen仍为30ac04fcc079bd6e81aecb4f1a66de20bc5cd9017aba96311833fd17bfc25380，未自动保留/融合任何候选；20额度用尽、pending空、有限任务已结束、新campaign STOP与状态已关闭等待用户选择。完整对照/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_l1_hidden_families_member3_20/REPORT.md；CSV /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_l1_hidden_families_member3_20/official_observations.csv。
<!-- /campaign-L1-hidden-member3-20:campaign_20261028_l1_hidden_families_member3_20 -->

<!-- selection-B2-hidden-inference:20261029T005944+0800 -->
## 2026-10-29T01:32:36.927300+08:00 保留B2为正式基线，未新增本case测试

- 用户明确选择B2_WideOriginalMathBatch，正式kernel.asc从L1切换为既有冻结B2，SHA256 be9c858f29bfcee4265ca6ac638441dd189d816eacf29e8c7b75ba5ae369cf25；原L1和两个状态原件在/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/selection_B2_hidden_inference_20261029T005944+0800/before。不是新开发候选，不改官方7文件和规则3文件。
- 三笔完整五项（本case为第1项）：R06 [602.91, 2.21, 14.38, 74.24, 60.19] us, score/rank 31.94/20; R12 [601.64, 2.15, 14.59, 72.77, 61.74] us, score/rank 31.98/21; R18 [602.44, 2.17, 14.8, 72.51, 61.65] us, score/rank 31.9/21。不拼接跨轮最小值。
- R06/R12/R18三笔既有官方Pass的服务端与snapshot全部8文件重新哈希匹配；完整同SHA向量/当时首次分数排名均保留，见/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/selection_B2_hidden_inference_20261029T005944+0800/selection_audit.json。本次无编译/NPU/平台GET/POST；平台最近已知为R20 L1对照，不伪称选版已发新提交。
- 只读分析支持用完整算法消融约束隐藏参数族：B2三次hidden均分残量28.176/28.161/28.144，高于L1两端27.931/27.995，属未配对方向线索，不识别H、点数、耗时或因果。动态/内生TBest、运行波动和非目标外溢均保留未知。
- 保留B2为新基线；旧104与已用20额度冻结，STOP保留、pending空、不恢复worker。后续仅凭新的明确授权实验/提交。综合方案/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/selection_B2_hidden_inference_20261029T005944+0800/REPORT.md，公开shape/评分可识别性/分族设计独立报告均在同目录。
<!-- /selection-B2-hidden-inference:20261029T005944+0800 -->


<a id="b2-four-routes-stopped-20261029"></a>
## 2026-10-29 B2四路线停止记录：case1

- 保留B2，SHA `be9c858f29bfcee4265ca6ac638441dd189d816eacf29e8c7b75ba5ae369cf25`；唯一进入A2的候选C01 SHA `2c2c249310bbdd36fc2c442ce9ded657413934071179a7c3edac5d3c713c5953`。A/B/D仅有本地A3检查，不冒充此case的A2验证。
- 以下只摘同SID的本case值；完整五项、所有候选、方案及A3限制在 [总history](history.md#b2-four-routes-stopped-20261029)。配对确认在完成前被用户停止，不据这些单次值宣称收益或无回退。
- R04与R10没有收尾数据，保留未知，不填0；R04长期Running不等于算子错误。E01是用户手动旧代码检查，不纳入候选对照。
- 14:42:41 +08已按用户要求停止，剩余额度冻结；此处补齐历史记录不构成新实验或重试授权。

|轮次|版本|case1耗时(us)|SID|
|---|---|---:|---|
|R01|B2|604.71|6ae2d4691dac5d235b204572|
|R02|B2|600.90|6ae2d4c31dac5d235b20a509|
|R03|B2|603.84|6ae2d51e1dac5d235b21007b|
|R05|C01|604.42|6ae2de861dac5d235b2a7114|
|R06|C01|604.77|6ae2e7541dac5d235b339f94|
|R07|C01|603.14|6ae2e9851dac5d235b370293|
|R08|C01|603.15|6ae2e9e21dac5d235b377117|
|R09|C01|602.46|6ae2ea3f1dac5d235b37d626|


<!-- case5-four-routes-ccs-max-20261030-final -->
## 2026-10-30T15:22:18.162178+08:00 case5 四路线 CCS DeepSeek Flash Max 完整结果（待用户选版）

- 父版与正式源保持 case5_compact `2a3e946715f9bb380b55b61a6e68b2113084998e5bfa17723a6a5bef8a5b9a39`，本轮四路各5次、20次A2已结束，等待用户选版。
- 四路线方法、A3范围、失败、完整五项和预算审计见总history本轮条目；本文件按同SID摘取本case，不将代理形状当官方映射。
- 本case所有真实快慢值如下，未拼接跨版本最小值：1/6ae438161dac5d235b4cccff A0_baseline_control_v2=477.54us; 2/6ae43a141dac5d235b4e9e17 A1_softmax_eps_direct_packed=475.98us; 3/6ae43a751dac5d235b4ef578 C1_compact_prefetch=475.94us; 4/6ae43bb01dac5d235b5000f1 B1_blockmajor_flat_br=476.83us; 5/6ae43c1c1dac5d235b5059ee A2_softmax_eps_mask_reuse=474.72us; 6/6ae43c7b1dac5d235b50a63a C2_lookahead_admission=476.28us; 7/6ae43d7c1dac5d235b51800d D1_q8_singlewave_partition=478.08us; 8/6ae43e6b1dac5d235b526575 A1_softmax_eps_direct_packed_repeat=474.76us; 9/6ae43ec31dac5d235b52b77b A2_softmax_eps_mask_reuse_repeat=474.26us; 10/6ae43f5d1dac5d235b5350c3 B2_blockmajor_mask_reuse=479.3us; 11/6ae43fbc1dac5d235b53aff1 C3_post_dequeue_lookahead=476.85us; 12/6ae4401c1dac5d235b540582 D2_q8_multiwave_partition=477.41us; 13/6ae441891dac5d235b559c71 B1_blockmajor_flat_br_repeat=476.29us; 14/6ae441e61dac5d235b55e98c C2_lookahead_admission_repeat=477.21us; 15/6ae442471dac5d235b56359f D1_q8_singlewave_partition_repeat=479.86us; 16/6ae4429f1dac5d235b56825c B2_blockmajor_mask_reuse_repeat=477.68us; 17/6ae442fd1dac5d235b56dbe7 C1_compact_prefetch_repeat=477.33us; 18/6ae4435c1dac5d235b572e31 D2_q8_multiwave_partition_repeat=478.07us; 19/6ae443b51dac5d235b5771b6 B2_blockmajor_mask_reuse_repeat2=476.97us; 20/6ae4440e1dac5d235b57bf42 D0_closing_baseline_control=478.37us.
- 分数是完整15项官方总分的首次成功观测，10项Hidden逐点耗时未知；A3诊断、官方样例、A2总体Pass及最终人工规则核验分层。
- 原始逐SID回执、源码SHA、完整比较见 `/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261030_case5_four_routes_deepseek_4x5/final_comparison.json`；生产不自动覆盖，本轮STOP、pending空、无自动续跑。


<!-- user-retains-case5-compact-after-four-routes-20261030 -->
## 2026-10-30T15:36:51.370142+08:00 用户选择保留 case5_compact 基线

- 用户确认保留原基线 case5_compact，活动源码SHA `2a3e946715f9bb380b55b61a6e68b2113084998e5bfa17723a6a5bef8a5b9a39`，无需源码复制。
- 本case最近已知收尾基线观察为 478.37us（SID `6ae4440e1dac5d235b57bf42`）；完整同SID五项、全部同源快慢与选版依据见总history本次条目及上轮原始比较。
- 本次没有新增正确性或性能实验；选版不将既有观测扩大为稳定性能收益，也不改写旧失败与慢记录。
- 待选标记已解除，STOP保留、pending空、各路剩余0、无自动续跑；本次编译/NPU/平台GET/POST均0。


## 2026-10-30 tree_tail_deepseek_3x7 complete

- 父版与完整SHA、逐SID五项、算法及分层验证见同轮总history；正式版本未自动替换。
- 本case全部实际观察：R01 A0_opening_baseline SID=6ae4593d1dac5d235b69ab44 477.18us score=34.84; R02 A1_dense_column_tree SID=6ae45b0f1dac5d235b6b5eeb 480.59us score=33.9; R03 C1_q8_singlewave SID=6ae45c1e1dac5d235b6c30a0 478.71us score=34.88; R04 A1_dense_column_tree_repeat SID=6ae45c761dac5d235b6c8128 482.22us score=34.64; R05 A2_layered_column_tree SID=6ae45d8f1dac5d235b6d78e3 478.58us score=33.59; R06 C2_tree_singlewave SID=6ae45de81dac5d235b6dbf60 478.56us score=34.82; R07 A2_layered_column_tree_repeat SID=6ae45fa71dac5d235b6f4061 476.18us score=33.54; R08 C1_q8_singlewave_repeat SID=6ae460001dac5d235b6f84ae 480.08us score=34.71; R09 M1_tree_singlewave_repeat SID=6ae460581dac5d235b6fc900 480.74us score=33.59; R10 B1_compact_tail2 SID=6ae460b31dac5d235b7019fd 477.98us score=33.63; R11 A3_fixed32_early_tail SID=6ae462721dac5d235b71a9b0 474.86us score=34.2; R12 M2_fixed32_singlewave SID=6ae462d31dac5d235b720b1d 476.86us score=34.24; R13 B1_compact_tail2_repeat SID=6ae463321dac5d235b726926 478.86us score=33.43; R14 A3_fixed32_early_tail_repeat SID=6ae465431dac5d235b7455dd 477.9us score=34.07; R15 M2_fixed32_singlewave_repeat SID=6ae4659b1dac5d235b74a28d 476.72us score=33.94; R16 C1_q8_singlewave_repeat2 SID=6ae465f31dac5d235b74eed0 481.18us score=34.26; R17 B2_safe_shared_column_gather SID=6ae468b21dac5d235b773716 479.65us score=33.9; R18 C4_latepack_softmax SID=6ae4690b1dac5d235b778648 477.48us score=34.57; R19 B2_safe_shared_column_gather_repeat SID=6ae469651dac5d235b77cd3c 483.02us score=33.97; R20 C4_latepack_softmax_repeat SID=6ae469c01dac5d235b78226f 482.55us score=34.53; R21 M4_unrolled_row_fixed32_singlewave SID=6ae46f2d1dac5d235b7d1d01 476.69us score=34.12; R22 M3_latepack_fixed32_singlewave SID=6ae46f851dac5d235b7d61fe 484.54us score=32.87; R23 M3_latepack_fixed32_singlewave_repeat SID=6ae4703c1dac5d235b7e0105 483.56us score=33.33; R24 M4_unrolled_row_fixed32_singlewave_repeat SID=6ae470941dac5d235b7e4adc 476.77us score=34; R25 C0_closing_baseline SID=6ae470ed1dac5d235b7ea777 478.12us score=34.38。
- 分数是对应SID评测后首次观测，包含隐藏项，不能由公开五项重算。保留同SHA慢记录，不因单次最好值判定稳定收益。
- STOP已设，未用额度冻结，待用户选版；原始JSON/CSV：`/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261030_case5_tree_tail_deepseek_3x7`。


## 2026-10-30 用户选定 M2 为正式基线

- 选定完整M2源码 `5b87987c98156bbba80ab73665e71a5e593a8e8f849eb6dc4e7ab2f8fec16676`；本case两次官方耗时为 476.86 / 476.72 us。
- 两次完整五项、SID、分数与选版审计见总history同节；本次没有新增设备验证或提交。
- 正式源码已切换，STOP与旧额度冻结；平台最新成绩仍对应旧基线最后回执。


## 2026-10-30 M2_bank_counter_deepseek_3x7 complete

- 父版与完整SHA、逐SID五项、算法及分层验证见同轮总history；正式版本未自动替换。
- 本case全部实际观察：R01 A0_M2_open SID=6ae482fd1dac5d235b8fc3f5 474.44us score=33.71; R02 I0_isolated_M2 SID=6ae4852e1dac5d235b91eca9 477.45us score=33.68; R03 A1_dual_phase_den SID=6ae485881dac5d235b924719 479.69us score=33.65; R04 C1_counter_windows SID=6ae485f51dac5d235b92a9ce 479.5us score=33.41; R05 B2_colored_row_roots_fixed SID=6ae486691dac5d235b931d92 484.14us score=34.14; R06 A2_dual_phase_isolated SID=6ae486cc1dac5d235b937da7 475.54us score=33.79; R07 A2_dual_phase_isolated_repeat SID=6ae487de1dac5d235b947240 479.98us score=33.62; R08 A1_dual_phase_den_repeat SID=6ae488361dac5d235b94bee6 478.65us score=33.43; R09 B2_colored_row_roots_fixed_repeat SID=6ae4888f1dac5d235b950ebb 484.52us score=34.02; R10 C1_counter_windows_repeat SID=6ae488e71dac5d235b957189 478.74us score=33.38; R11 B0_M2_mid SID=6ae4894b1dac5d235b95d358 478.17us score=33.83; R12 F1_AB_direct SID=6ae489a51dac5d235b963353 478.34us score=33.85; R13 F2_AB_isolated SID=6ae48a041dac5d235b9691a7 481.14us score=33.95; R14 C2_counter_isolated SID=6ae48a631dac5d235b96e983 482.54us score=33.92; R15 B3_colored_roots_isolated SID=6ae48ac61dac5d235b9749cc 477.27us score=32.98; R16 A3_single_phase_den SID=6ae48b211dac5d235b97a463 475.68us score=33.44; R17 F3_ABC_isolated SID=6ae48b7c1dac5d235b98013d 479.41us score=34.35; R18 A3_single_phase_den_repeat SID=6ae48c191dac5d235b98b107 476.85us score=33.89; R19 B3_colored_roots_isolated_repeat SID=6ae48c7c1dac5d235b9917f4 476.71us score=33.45; R20 F1_AB_direct_repeat SID=6ae48ce51dac5d235b9993aa 478.22us score=33.98; R21 F2_AB_isolated_repeat SID=6ae48d3f1dac5d235b9a0140 477.82us score=33.17; R22 F3_ABC_isolated_repeat SID=6ae48d9b1dac5d235b9a623d 477.39us score=33.72; R23 C3_column_counter_isolated SID=6ae48dfb1dac5d235b9ad33e 476.48us score=32.86; R24 C3_column_counter_isolated_repeat SID=6ae48e571dac5d235b9b7566 478.63us score=32.38; R25 F3_ABC_isolated_repeat2 SID=6ae48f081dac5d235b9c98b9 477.58us score=34.08; R26 C0_M2_close SID=6ae48fa21dac5d235b9d53aa 476.24us score=33.73。
- 分数是对应SID评测后首次观测，包含隐藏项，不能由公开五项重算。保留同SHA慢记录，不因单次最好值判定稳定收益。
- STOP已设，未用额度冻结，待用户选版；原始JSON/CSV：`/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261030_M2_bank_counter_deepseek_3x7`。


<!-- F1-selected-case5-next-plan-20261030 -->
## 2026-10-30T21:41:45.711488+08:00 用户选择 F1 为正式基线

- 用户明确选择 F1_AB_direct，正式源码由 M2 `5b87987c98156bbba80ab73665e71a5e593a8e8f849eb6dc4e7ab2f8fec16676` 切换为 `4e74fab52bdf7226d628b04e768c8d171d6ecd3cf62c48a5092481b0eeb74659`；复用不可变官方提交快照。
- 既有官方证据：SID 6ae489a51dac5d235b963353 case1=478.34us 首次分数=33.85；SID 6ae48ce51dac5d235b9993aa case1=478.22us 首次分数=33.98。分数为评测后首次采集，非提交瞬间值。
- 核对两次Pass、服务端全8文件绑定、候选175组设备验证与M2逐位一致；本次仅复制已验证源码，新增编译/NPU/POST均0。七个保护文件不变。
- 旧STOP与剩余额度维持冻结；平台最新记录仍是M2收尾SID，未冒称已重新提交F1。接下来只做方案分析，选版审计与下一轮JSON见 `/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_F1_case5_next_20261030`。


## 2026-10-30 F1_col_q4_io_deepseek_3x7 complete

- 父版与完整SHA、逐SID五项、算法及分层验证见同轮总history；正式版本未自动替换。
- 本case全部实际观察：R01 A0_F1_open SID=6ae4a8cb1dac5d235bb86ba9 477us score=34.03; R02 C1_gate_pair SID=6ae4a9451dac5d235bb8dfe1 479.04us score=33.71; R03 A1b_colscratch SID=6ae4aa711dac5d235bba11c7 474.74us score=34.54; R04 C2_early_gate_store SID=6ae4ab301dac5d235bbaefe4 480.23us score=33.91; R05 A1b_colscratch_repeat SID=6ae4ab8a1dac5d235bbb7054 477.33us score=34.35; R06 C3b_softmax_eps_pack SID=6ae4accb1dac5d235bbd5546 482.73us score=33.63; R07 A2_cachedlayout SID=6ae4ad251dac5d235bbdb675 476.09us score=33.52; R08 C4_io_pack SID=6ae4ae861dac5d235bbf3780 477.21us score=33.5; R09 M1_A1b_C2 SID=6ae4aee21dac5d235bbf9b5b 480.03us score=34.03; R10 C2_early_gate_store_repeat SID=6ae4af3f1dac5d235bbffc04 484.77us score=32.99; R11 C6_F1_drift SID=6ae4afd61dac5d235bc0aa7f 478.66us score=33.88; R12 A3_constpitch SID=6ae4b1f61dac5d235bc2ecbc 476.9us score=33.22; R13 A4_ones_phase SID=6ae4b38a1dac5d235bc4f445 478.74us score=33.07; R14 A1b_colscratch_third SID=6ae4b45e1dac5d235bc5da0e 476.47us score=33.78; R15 C7_F1_close SID=6ae4b6971dac5d235bc82cdd 476.17us score=33.51。
- 分数是对应SID评测后首次观测，包含隐藏项，不能由公开五项重算。保留同SHA慢记录，不因单次最好值判定稳定收益。
- STOP已设，未用额度冻结，待用户选版；原始JSON/CSV：`/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261030_F1_col_q4_io_deepseek_3x7`。

<!-- F1-selected-post-colq4io-analysis-complete -->
## 2026-10-31T00:20:41.482734+08:00 F1选定与case5下一轮分析（仅方案）

- 用户选择并保留F1，完整SHA `4e74fab52bdf7226d628b04e768c8d171d6ecd3cf62c48a5092481b0eeb74659`；正式源码原本已匹配，无需复制；SID `6ae4b6971dac5d235bc82cdd`，评测后首次同SID分数33.51。该case最近F1同SID耗时476.17us；本轮未新增测试。
- case5当前3次F1为53.90/53.27/53.90us，中位数53.90；进入50需再省>3.90us（>7.2356%），工程目标49us。A1b/C2单次最好值不稳定，旧q4占核前提不成立，不重扫同类相位/搬运方案。
- 新主线A：列归约前3级不动，8根按[0,4,2,6,1,5,3,7]转置后BR，6→5调用与屏障，但每列阶段多5120/6144B逻辑UB流量；地址表可复用原死matrix末段256B。次线B：packed按token做8条strided WR，9/11→8调用、4→1屏障；短WR吞吐可能反向变慢。只融合独立获益者；16根WR因320/384短repeat降级候补。
- 验证仅CPU：16个H的有序树、48组地址、135168转置搬运、212672行元素、4096组地址表phase检查通过；这是源码分支域分析，不认定官方shape。masked FP32树/符号零仍需设备逐位核验；A3计数器只作诊断。计划与API/SDK原文证据：`/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_F1_case5_after_colq4io_20261030/next_round_plan.json`。
- 本次候选实现/编译/NPU/POST/新子代理均0；8个正式文件与F1快照一致，STOP不变，旧A7/B0/C7/M1共15次及剩余B7/M6冻结，pending为空。选版已确认；下一轮未启动，当前基线仍F1。


<!-- F1-treefusion-deepseek-3x7-complete -->
## 2026-10-31T01:39:54.415354+08:00 F1_treefusion_deepseek_3x7 完成，待用户选版

- 本轮正式case1逐提交耗时（us，序号对应history.md完整SID表）：1:A0_F1_open=475.87；2:A1_col8_scalar_addr=480.83；3:C0_F1_mid=476.90；4:A3_normal64_tree=480.67；5:A1_col8_scalar_addr_repeat=479.19；6:A3_normal64_tree_repeat=480.35；7:A4_normal64_full_column=479.43；8:C4_row_normal_mask_reuse=477.25；9:M1_A4_C4=477.52；10:A4_normal64_full_column_repeat=477.20；11:C4_row_normal_mask_reuse_repeat=474.87；12:M1_A4_C4_repeat=476.98；13:M2_row_count_reuse=477.49；14:C1_F1_late_control=477.01；15:M3_A3_row_counter=476.70；16:M3_A3_row_counter_repeat=477.95；17:C2_F1_close=477.23。
- 当前正式F1收尾case1=477.23us，SID `6ae4d6091dac5d235beb9e30`；代码SHA `4e74fab52bdf7226d628b04e768c8d171d6ecd3cf62c48a5092481b0eeb74659`。
- 所有正式记录均保留，包括同源码慢测；A3代理形状不是已确认官方形状，十隐藏项不可见。
- 建议继续保留F1作为正式基线。A3是本轮最值得保留研究的case5候选，两次为52.35/51.95us，但case4升至76.11/77.68us，未证明整体稳定改善；M3复测虽到52.07us，两次分数32.86/32.84，融合没有形成更好的综合版本。本轮未实现case5低于50us。；正式源码未切换，等待用户选择。
- 证据 `/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261031_F1_treefusion_deepseek_3x7/final_comparison.json` 与 `results.csv`；配额、间隔、源码及STOP审计通过。


<!-- F1-issue-bulk-deepseek-3x7-complete -->
## 2026-10-31T03:54:53.345490+08:00 F1_issue_bulk_deepseek_3x7 完成，待用户选版

- 本轮正式case1逐提交耗时（us，序号对应history.md完整SID表）：1:C0_F1_open=475.73；2:A1_column_mul_unroll=476.46；3:A1_repeat2=476.19；4:A2_row_loops_unroll=478.71；5:B2_bulk_input_gather_lifecycle=477.39；6:C1_idle_gate_cores=479.83；7:B2_repeat2=476.42；8:M1_A1_B2=477.81；9:C0_F1_mid=477.03；10:M1_repeat2=476.75；11:B4_seed8_fanout=477.58；12:B4_repeat2=478.14；13:C3_balanced_idle_gates=477.63；14:M3_A1_B4=478.78；15:B2_repeat3=478.95；16:A1_repeat3=473.94；17:C0_F1_late=476.99；18:M1_repeat3=477.26；19:C0_F1_close=476.85。
- 当前正式F1收尾case1=476.85us，SID `6ae4f51f1dac5d235b059860`；代码SHA `4e74fab52bdf7226d628b04e768c8d171d6ecd3cf62c48a5092481b0eeb74659`。
- 所有正式记录均保留，包括同源码慢测；A3代理形状不是已确认官方形状，十隐藏项不可见。
- 建议本轮B2连续输入搬运版：三个固定轮换账号的case5均低于50us，分别47.99/47.81/46.82us，中位数47.81us；包含全部慢测的F1中位数53.545us，case5中位数改善10.71%，case4中位数改善5.51%。B2分数中位数33.01，F1为33.07；这是面向case5目标与公开case4收益的推荐，并非总分最优保证。正式基线继续F1，最终保留版本由用户决定；正式源码未切换，等待用户选择。
- 证据 `/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261031_F1_issue_bulk_deepseek_3x7/final_comparison.json` 与 `results.csv`；配额、间隔、源码及STOP审计通过。


## 2026-10-31 B2 baseline selected; under40 analysis
- 用户明确保留本轮 B2_bulk_input_gather_lifecycle；正式 kernel.asc 已切换至 SHA 870259fd7968eb6842f47ac6a9ac93d768558abf875358863030cf57c1dc4f67，其余七个正式文件哈希不变。
- 本轮B2该case正式观测为 477.39/476.42/478.95 us；保留全部观测，未拼接跨提交最小值。
- 三次B2官方Pass及337项本地A3验证沿用精确同SHA证据；本次为源码选定，未新增编译、NPU验证或POST。平台latest仍是上一轮F1收尾提交，不能写成已更新排行榜。
- 上轮19次POST账本、STOP与剩余9次冻结额度保持不变；本轮仅分析，记录 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261031_B2_under40/selection.json。


## 2026-10-31 B2 under40 bottleneck analysis complete
- 本轮仅保留B2并分析case5，未修改其他case算法、未新增正式耗时或分数。
- 新A3诊断只支持合成H34的瓶颈定位，不将其映射为本case或任何隐藏case。
- 待执行方案须报告完整五case及官方分数，尤其防止重现M1/B4对case4的退化。
- 分析与原始证据：/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261031_B2_under40/analysis.json；旧轮19次POST及未用9次预算冻结，analysis STOP保留。


## 2026-10-31 B2 output-bank-pack campaign completed
- 三个 ccs-deepseek/deepseek-flash High 子代理完成输出批量写回、列归约UB着色、softmax与pack融合；父端审查并正式POST 18 次，全部Pass。A/B/C/M用量 5/4/4/5，各上限5；仅member1/member2交替，member3为0。
- case1全部同提交官方观测（us）：C0_B2_open=479.28; B1_column_colored=477.50; A1_tokenmajor_3dma=476.75; C1b_eps_pack_fixed=475.72; C1b_repeat2=474.64; A2_dense_output=478.09; B0_B2_mid=477.82; M1_AC=481.86; A3_dense_fast_pattern=477.12; A3_repeat2=476.56; B1_repeat2=477.05; M2_A3C=478.06; A3_repeat3=475.81; M2_repeat2=477.93; M1_repeat2=483.20; B0_B2_late=477.94; M2_repeat3=475.83; C0_B2_close=476.64。保留慢测；分数为完成后首次成功读取，完整五项/分数/提交ID见results.csv。
- 所有正式新候选先通过111+162+64项本地A3逐位/输入只读检查，再经固定快照官方样例与服务端8文件SHA绑定。C1首版本地失败未POST；B路线只着色首层变体无诊断收益未晋级。A3诊断不是A2官方或隐藏shape证据。
- 父端建议：推荐 A3_dense_fast_pattern 作为继续压低case5的下一轮版本，等待用户选择，当前生产仍保留B2；A3三次case5为44.44/44.40/45.54us，中位44.44us，相对本轮B2全部四次中位49.965us降低11.06%；B2慢测保留，A3三次也均快于B2最快的47.24us。主要代价是case4中位74.00us（B2为70.395us），首次观测分数中位32.60（B2为32.745）。本轮未达到40us，不宣称总分收益。正式源码始终B2(870259fd7968eb6842f47ac6a9ac93d768558abf875358863030cf57c1dc4f67)，本轮收尾也提交精确B2，最终版本由用户选择。
- 当前STOP已设置，pending为空，未用2次冻结、不自动续跑；旧轮STOP及未用9次保持。证据 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261031_B2_output_bank_pack_deepseek_3x5/final_comparison.json、control/final_audit.json 和 results.csv。


## 2026-10-31 A3 baseline selected; under40 analysis
- 用户明确保留A3_dense_fast_pattern；正式kernel.asc已切换到SHA b35e7a8a3f52d856243c2e3ed518636d7aa83dc077de7e3a95d89cf9751fd508，其他七个正式文件哈希不变。
- case1三次官方同SHA观测为477.12/476.56/475.81us，中位476.56us；完整五项与分数沿用上轮固定回执，不拼接最小值。
- 复用精确A3的337项本地验证及三次A2 Pass证据；本次选择未新增POST，平台latest仍是B2收尾，不能说排行榜已切换A3。
- 旧轮18次POST、STOP与未用2次保持冻结，更早9次也不恢复；本轮仅分析/原样诊断，选版证据 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261031_A3_under40/selection.json。


## 2026-10-31 A3 under40 diagnosis completed
- A3正式源码SHA b35e7a8a3f52d856243c2e3ed518636d7aa83dc077de7e3a95d89cf9751fd508及其他七文件核验未变；本轮仅分析，0次新POST、0个优化候选。
- case1沿用三次同SHA官方观测；本次没有新增该case的官方耗时或分数，不将代理负载数据写成官方改善。
- 下一轮方案集中compact迭代与门控路径；仍需全量正确性、前五项和总分复查后由用户选择保留版本。
- 分析已完成，旧STOP及未用2次/更早9次保持冻结；下一轮未启动。完整量化证据与方案：/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261031_A3_under40/analysis.json。


## 2026-10-31 B2 retained; mask-row-column campaign started
- 用户最新指令保持B2，生产恢复精确SHA 870259fd7968eb6842f47ac6a9ac93d768558abf875358863030cf57c1dc4f67；A3 b35e7a8a3f52d856243c2e3ed518636d7aa83dc077de7e3a95d89cf9751fd508仅作为隔离候选父版本，七个保护文件不变。
- DeepSeek Flash High三路：A mask驻留、B单条行BR、C两级列BR；父端审核及POST。A/B/C/M各最多5次，含重复/失败/控制，总上限20；只member1/member2交替，member3禁用。
- 旧轮STOP与未用2次及更早9次保持冻结；复用精确B2/A3既有337项验证，新候选须独立核验后提交。
- 新轮状态与固定证据目录 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261031_B2_mask_row_col_deepseek_3x5；本条为开轮记录，尚无新官方结果，最终由用户选版。


## 2026-10-31 mask/row/column轮结束：B2保留，等待用户选版
- 完成13次正式POST，A/B/C/M用量5/2/1/5（每路上限5），全部Pass且服务端八文件绑定匹配；member1/member2严格交替，未用member3；余下7次冻结。
- A2行列Counter-mask合并三次case5为43.22/43.81/43.97us，中位43.81us；B单条BR/间隔根分别46.87/46.83us，停止扩展；C正确版本337项通过但本地耗时数倍上升，Max复核后停止，0次候选POST。
- 融合版和每次提交的case1–5、分数、SID详见下表及/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261031_B2_mask_row_col_deepseek_3x5/final_comparison.json；推荐A2_column_row_counter_fusion，理由：面向case5目标推荐A2：三次43.22/43.81/43.97us，中位43.81us，波动范围0.75us；M1三次中位43.97us且范围2.71us，M2两次中位44.515us。A2的case4中位69.12us也较低。A2得分32.46–32.99，M2为32.81/32.86，尚不能证明A2有稳定总分优势。生产保留B2，由用户最终选择。；该推荐尚未采用，本轮未实现case5<40us。
- 生产仍为B2 SHA 870259fd7968eb6842f47ac6a9ac93d768558abf875358863030cf57c1dc4f67；最后精确B2对照SID 6ae58e601dac5d235b825890，case5=53.90us，分数32.30；七个保护文件及旧轮STOP/账本/分析均未变。
- 本地337项逐位一致/输入只读验证与A3代理profile不等于官方A2性能；分数为完成后首次成功读取的同SID分数，十个隐藏用例不可见；所有重复保留，STOP已写入，停止自动继续，最终由用户选择。

| 版本 | 本case耗时(us) | 分数 | SID |
|---|---:|---:|---|
| A0_A3_open | 475.64 | 32.75 | 6ae57f5e1dac5d235b70dab3 |
| A1_column_counter_mask | 475.68 | 32.52 | 6ae580cc1dac5d235b7268ff |
| A2_column_row_counter_fusion | 480.00 | 32.73 | 6ae5836f1dac5d235b74f218 |
| A2_repeat2 | 476.35 | 32.99 | 6ae584cb1dac5d235b766a57 |
| B1_dense_flat_br_h33_42_v4 | 482.85 | 32.36 | 6ae586391dac5d235b788359 |
| A2_repeat3 | 479.51 | 32.46 | 6ae587b41dac5d235b7a1e04 |
| M1_A2_B | 476.01 | 32.87 | 6ae588a61dac5d235b7b6555 |
| B2_spaced_roots_gap6_5_v1 | 476.80 | 32.04 | 6ae58afa1dac5d235b7e5584 |
| M2_A2_gate | 478.92 | 32.81 | 6ae58bff1dac5d235b7f919d |
| M1_repeat2 | 477.25 | 32.60 | 6ae58c9a1dac5d235b804726 |
| M1_repeat3 | 477.15 | 32.74 | 6ae58d401dac5d235b80fbf7 |
| M2_repeat2 | 478.01 | 32.86 | 6ae58dd01dac5d235b81adf5 |
| C0_B2_close | 478.65 | 32.30 | 6ae58e601dac5d235b825890 |


## 2026-10-31 用户选择A2为基线，启动剩余瓶颈分析
- 用户明确选择A2_column_row_counter_fusion，正式源码从B2恢复为精确SHA 82e983326ae960963ac7365aca88f43672e051f3e3ed92ee0b431fac1c7a4b24，七个保护文件不变。
- 本case同SHA三次耗时：480.00/476.35/479.51us；完整五项与SID见总history本次选版记录。
- 复用该SHA的337项本地逐位一致性、输入只读和三次官方Pass证据；本次选版0次POST，最新平台提交仍为上一轮B2收尾，不冒充已上传A2。
- 旧STOP、账本、比较报告及未用7次保持冻结；本次只分析与原样源码诊断，不启动候选开发或正式提交。选版审计：/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261031_A2_under40/selection.json。


## 2026-10-31 A2缓冲/索引/布局轮结束：保持A2，等待用户选版
- 三个DeepSeek Flash High子代理，父端审核决策；共15次正式POST，A/B/C/M用量2/5/5/3（各上限5）。全部Pass且服务端八文件绑定匹配；member1/member2严格交替，member3未用；本轮剩余5次冻结，旧7次仍冻结。
- 三路实现、失败、止损和融合决定详见/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261031_A2_reuse_index_layout_deepseek_3x5/final_comparison.json的route_decisions及candidate_inventory；本地337项逐位一致/输入只读与完整A3 ABBA不冒充官方A2性能。
- 推荐M1_RC3_RB2_index_doubling，理由：综合表现推荐M1融合版，但不把它称为case5优化成功：本轮同SHA三次中位数，M1的case1/2/3/4为475.57/2.20/15.75/68.53us，A2三次对照为478.40/2.22/15.81/70.58us；M1的case5中位43.93us，反而比A2的43.63us慢0.30us，均未低于40us。M1后段首次观测分数31.79/31.97/32.17，邻近A2对照31.74/31.71，显示综合成绩的正向信号；但TBest在轮内变化，不能保证固定幅度的总分收益。若用户只以case5为取舍标准，A2仍更合适。生产保持A2，M1仅推荐，最终由用户选择。；推荐不自动采用，最终由用户选择。全部同SID五项耗时、分数和复测慢记录见下表；case5目标是否达成以final_comparison为准。
- 生产仍为A2 SHA 82e983326ae960963ac7365aca88f43672e051f3e3ed92ee0b431fac1c7a4b24；末次A2对照SID 6ae5a9781dac5d235ba48acd，case5=43.63us，首次观测分数31.71。七个保护文件及旧轮STOP/账本/分析均未变。
- 分数为完成后首次成功读取的同SID官方值，并非提交瞬间分数；本轮TBest发生变化，尤其case1从334.85降至262.27us，分数变化不能全部归因于候选。STOP已写入，停止自动继续，保留所有失败和慢记录。

| 版本 | 本case耗时(us) | 分数 | SID |
|---|---:|---:|---|
| A0_A2_open | 478.27 | 33.04 | 6ae59d941dac5d235b95a05b |
| RB1_row_prefix | 478.87 | 32.93 | 6ae59f971dac5d235b982564 |
| RA1_index_reuse_mul_pingpong | 475.86 | 32.43 | 6ae5a0851dac5d235b993b59 |
| RB2_full_doubling | 478.44 | 33.19 | 6ae5a1bf1dac5d235b9aa70f |
| RB2_repeat2 | 479.93 | 32.50 | 6ae5a26b1dac5d235b9b709f |
| RB3_hybrid_flat8 | 485.46 | 31.51 | 6ae5a3191dac5d235b9c41ab |
| RC3_compact_helpers_only | 475.35 | 32.06 | 6ae5a3fe1dac5d235b9d5b4c |
| RB2_repeat3 | 482.08 | 31.65 | 6ae5a45c1dac5d235b9dd7ee |
| RC3_repeat2 | 475.97 | 32.01 | 6ae5a50a1dac5d235b9eaba3 |
| RC3_repeat3 | 476.37 | 31.98 | 6ae5a5ce1dac5d235b9f8f2b |
| M1_RC3_RB2_index_doubling | 475.02 | 31.79 | 6ae5a6fd1dac5d235ba1055a |
| C0_A2_mid | 478.40 | 31.74 | 6ae5a79e1dac5d235ba1f145 |
| M1_repeat2 | 476.23 | 31.97 | 6ae5a8731dac5d235ba33b58 |
| M1_repeat3 | 475.57 | 32.17 | 6ae5a8cd1dac5d235ba3b120 |
| C0_A2_close | 481.08 | 31.71 | 6ae5a9781dac5d235ba48acd |


## 2026-10-31 用户选择M1为基线并分析剩余瓶颈
- 生产源码由A2切换为用户选定M1 SHA 3c8f646d971e4a4750eaa68e7ddc1e5bb5f706bc060376221559d94aa4722075，七个保护文件不变。
- 本case同SHA三次耗时：475.02/476.23/475.57us；完整五项与SID见总history本次选版记录。
- 复用337项本地逐位/只读验证与三次官方Pass；本次选版0次POST，最新平台提交仍为上一轮A2收尾。
- 旧轮STOP、账本及未用5次冻结；本次分析和原样诊断，不开发优化候选或正式提交。选版审计：/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261031_M1_under40/selection.json。


## 2026-10-31 M1重复BR/首层错相/交替布局轮结束：保持M1，等待用户选版
- 三个DeepSeek Flash High子代理启动，C路升级为同模型Max接替；父端审核与提交。共10次正式POST，A/B/C/M用量5/2/3/0（各上限5）；仅member2/member1严格交替，未使用member3。本轮未用10次及旧5次均冻结。
- 三路正确性失败、性能负结果、版本筛选和融合决定保存在/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261031_M1_br_skew_alternate_deepseek_3x5/final_comparison.json及candidate_inventory.json；本地A3验证与诊断不代替官方A2性能。
- 推荐RA1_remove_redundant_br，理由：以case5为优先目标推荐RA1：四次正式Pass的case5为42.26/43.05/41.99/42.37us，中位数42.315us；同轮三次M1对照中位数44.26us，约降低4.39%。B/C正式退化，不融合。RA1的case1/case4中位数略慢，且后段分数31.63与M1收尾31.64接近，因此不宣称稳定总分领先；本轮未达到40us。生产M1不变，等待用户选择。；尚未采用，由用户选择。全部同SID正式耗时和分数见表，慢记录不删。是否达到40us目标见final_comparison.json。
- 生产仍为M1 SHA 3c8f646d971e4a4750eaa68e7ddc1e5bb5f706bc060376221559d94aa4722075，末次本轮M1对照SID 6ae5c3971dac5d235bc57dfe，case5=44.26us；正式八文件和七个保护文件、旧轮不可变记录均核验一致。STOP已写入，不自动继续。
- 分数为完成后首次成功观测的同SID官方值；榜单被队内其他提交覆盖而未采集到的分数记为缺失，不填入其他版本分数，也不从公开五项推算隐藏总分。

| 版本 | 本case耗时(us) | 分数 | SID |
|---|---:|---:|---|
| A0_M1_open | 474.79 | 31.71 | 6ae5b6281dac5d235bb4e306 |
| RA1_remove_redundant_br | 478.41 | 32.04 | 6ae5b8eb1dac5d235bb8ad34 |
| RA1_repeat2 | 477.49 | 32.09 | 6ae5ba231dac5d235bba3893 |
| B0_M1_mid | 474.56 | 未采集 | 6ae5bbb91dac5d235bbc3b75 |
| RA1_repeat3 | 475.74 | 32.04 | 6ae5bc7d1dac5d235bbd1780 |
| RB1_first_level_input_skew_v3 | 478.02 | 31.35 | 6ae5be4d1dac5d235bbf3f40 |
| RC2_correct_block_offsets | 476.64 | 31.24 | 6ae5c01e1dac5d235bc1651e |
| RA1_repeat4_late | 478.14 | 31.63 | 6ae5c1471dac5d235bc2d446 |
| RC4_combined_first4_br | 478.05 | 30.89 | 6ae5c3001dac5d235bc4c8d8 |
| C0_M1_close | 475.90 | 31.64 | 6ae5c3971dac5d235bc57dfe |


## 2026-10-31 用户选择RA1基线，开始剩余瓶颈分析
- 已按用户明确选择将生产源码由M1 3c8f646d971e4a4750eaa68e7ddc1e5bb5f706bc060376221559d94aa4722075切换到RA1 84948804f38c5f0a17541e4138f1186bda0ad0432484bb014e0ccc27fe112a05，生产只读，七个保护文件未变。
- 同SHA四次官方Pass，case5=42.26/43.05/41.99/42.37us，中位42.315us；完整五项和分数沿用上一轮原始记录，不重写为新成绩。
- 复用337项逐位/输入只读验证和四次官方源码绑定；本次选版0次POST。最新已知平台提交仍是M1收尾，已与当前生产RA1区分。
- 旧轮STOP、账本、报告及剩余10次保持冻结，旧5次仍冻结。本次只分析并给出下轮方案。选版审计：/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261031_RA1_under40/selection.json。



## 2026-10-31 RA1三路stride/gap/roots轮次完成，待用户选版
- 本轮保持RA1基线84948804f38c5f0a17541e4138f1186bda0ad0432484bb014e0ccc27fe112a05；完整方法、负结果、预算及五项对照见history.md本轮条目。
- 下表为本case所有正式同SID观测，不择优拼接；A3配对profile只作诊断。
- 生产及官方保护文件未变；全部正式候选经337项逐位/输入只读验证和父端复核，SC2仅111项并因本地退步未提交。
- 推荐及选版状态：面向本轮case5目标，推荐SA1v2_col_scratch_stride9作为候选：两次官方41.97/41.87us，中位41.92us，本轮RA1三次中位43.16us，改善约2.87%；但case4中位70.355us对RA1的68.90us有回退，且分数31.44/31.67未证明稳定总分领先。本轮未达40us，RA1生产保持不变，由用户最终选择。；待用户选择。
- 原始证据：/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261031_RA1_stride_gap_roots_deepseek_3x5/final_comparison.json；STOP，剩余冻结，无自动继续。

|版本|耗时(us)|分数*|SID|
|---|---:|---:|---|
|A0_RA1_open|476.58|31.61|6ae5d3561dac5d235bd7bd49|
|SB1_single_gap256|479.01|30.80|6ae5d6051dac5d235bdb045a|
|SA1v2_col_scratch_stride9|478.87|31.44|6ae5d6f01dac5d235bdc0fee|
|SA2_col_scratch_stride15|481.73|31.08|6ae5d8bc1dac5d235bde347a|
|B0_RA1_mid|477.15|31.67|6ae5d9ea1dac5d235bdfb8e0|
|SA3_stride9_compiletime|481.25|31.49|6ae5dce41dac5d235be3258b|
|SA1v2_repeat2|476.34|31.67|6ae5ddfc1dac5d235be46e77|
|C0_RA1_close|477.39|31.15|6ae5de6b1dac5d235be4fad6|


## 2026-10-31 用户选择SA1v2基线并分析剩余瓶颈
- 生产源码由RA1切换为SA1v2 17c145dd6fb8b788b64e7f316e25b83eb36b6cc5d0d40a36caf8013c4efea51d；七个保护文件不变，保留只读。
- 同SHA两次官方Pass，五项分别478.87/2.17/16.01/70.50/41.97us（31.44分）及476.34/2.13/15.82/70.21/41.87us（31.67分）；case5中位41.92us，尚未低于40。
- 复用337项逐位/输入只读证据及两次官方源码绑定；本次选版0次POST。最新已知平台提交仍为RA1收尾，与当前生产SA1v2区分。
- 旧轮STOP/账本/报告及剩余12次、较早15次保持冻结；本次仅分析和原样源码诊断。选版审计：/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261031_SA1v2_under40/selection.json。


## 2026-10-31 SA1v2三路layer/buffer/tail轮次完成，待用户选版
- 本轮保持SA1v2基线17c145dd6fb8b788b64e7f316e25b83eb36b6cc5d0d40a36caf8013c4efea51d；完整方法、负结果、预算及五项对照见history.md本轮条目。
- 下表为本case所有正式同SID观测，不择优拼接；A3配对profile只作诊断。
- TA1、TB1v2、TC1均通过111+162+64共337项A3设备验证，输出逐位匹配SA1v2且输入只读；父端独立复核源码SHA及输出哈希。初版TB1因split路径漏传新参数而编译失败，修复后的fix1与TB1v2源码SHA相同；失败证据保留。
- 推荐及选版状态：建议继续保留SA1v2。TA1可保留为备选源码，但其case5三次为43.03/43.03/43.11us，中位43.03us，相对本轮SA1v2四次中位43.105us只快0.075us（约0.17%），小于基线41.40至44.35us的观测波动，尚不足以支持更换基线。本轮没有版本突破40us。；待用户选择。
- 原始证据：/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261031_SA1v2_layer_buffer_tail_deepseek_3x5/final_comparison.json；STOP，剩余冻结，无自动继续。

|版本|耗时(us)|分数*|SID|
|---|---:|---:|---|
|A0_SA1v2_open|477.82|31.39|6ae5f22c1dac5d235bfba124|
|TA1_layer_stride_9_10_12_8|478.86|31.28|6ae5f51a1dac5d235bfed21c|
|TB1v2_column_index_pingpong|477.35|30.78|6ae5f6c11dac5d235b00668e|
|TA1r2_layer_stride_9_10_12_8|479.84|31.51|6ae5f7351dac5d235b00f685|
|C0_SA1v2_close|479.25|30.95|6ae5f7c21dac5d235b018e8b|
|C1_SA1v2_cross_account|479.19|31.23|6ae5f8851dac5d235b02552a|
|TA1r3_layer_stride_9_10_12_8|477.75|31.34|6ae5f92a1dac5d235b0308b9|
|C0_SA1v2_close|475.02|31.91|6ae5f9be1dac5d235b03ace8|


## 2026-10-31 用户确认继续保留SA1v2，分析下一轮方案
- 用户选择保留SA1v2，生产SHA 17c145dd6fb8b788b64e7f316e25b83eb36b6cc5d0d40a36caf8013c4efea51d 已匹配，无需复制源码，七个保护文件不变。
- 上轮8次官方结果及原始报告保持；最新同SHA基线case5=41.40us、分数31.91，SID 6ae5f9be1dac5d235b03ace8，不冒称稳定耗时。
- 待选标记全部关闭；上轮剩余12次及更早27次合计39次仍冻结，STOP保持，无自动继续和新POST授权。
- 本次仅瓶颈/方案分析及三个账号GET额度核验；选版审计 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261031_SA1v2_post_layer_under40/selection.json。


## 2026-10-31 SA1v2本轮结果复盘与下一轮方案
- 继续保留SA1v2 SHA 17c145dd6fb8b788b64e7f316e25b83eb36b6cc5d0d40a36caf8013c4efea51d；本次0新候选、0编译、0NPU、0POST、0子代理，旧39次额度冻结。
- 本轮基线case5四次中位43.105us、范围41.40至44.35；TA1中位43.03，差0.075us不足以证明稳定收益。低于40需再省超过3.105us（约7.20%）。
- 主攻统一紧凑尾部且共用原六级列树；区别于旧双平面串行列归约。CPU验证H33/H34的536条列有序表达式及地址通过，H34列Add repeat165→142、UB源码计168256B；不是设备性能证明，索引/Gather/恢复成本与真实物理地址尚待测。
- 辅助审计固定helper的Normal-mask驻留，先对照旧C4负结果；先行诊断实际阶段/地址，保留原树/native Div/eps/iters/输入只读，禁止把插桩或A3计时当官方收益。
- 三账号GET快照已用50/47/36，按当前每日50策略剩0/3/14；API未公布限额。现有member1/member2严格交替下今日不可续交。完整方案与证据 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261031_SA1v2_post_layer_under40/analysis.json；STOP，不自动执行。


<!-- A_case12_gate_tail_3dirs_20261104_C1_FINAL -->
## 2026-11-04 case1 H128 gate/CopyOut重叠候选

- D1在既有MatrixPrefetch/half-swap路径末尾追加1KiB下一token gate bank和2KiB独立sigmoid scratch，保持原matrix/product/factors起点与归约、Div/eps/iters不变；通过容量和物理地址guard回退。D3仅在该D1源码上增加tiny尾部生命周期改动。
- 本机CANN9/A2官方case1 sample编译运行全Pass；D3同样通过。D1 kernel SHA c8c234ebbdab7e0313b157ee7f82aff323cdd5b918ab051f82f2a4b7fe217ff2，D3 SHA e290e415c6da10b80b3acfa6eaf21453a8e02e04eb9ee077f86963ae180cbb21。
- 官方D1/member1 SID 6aea0f471dac5d235b7addca case1=472.75us，较同SHA基线五次中位475.75us低3.00us；完整五项[472.75,2.20,9.72,68.75,34.01]us，Pass。D3 case1=476.01us，未复现收益。
- D1为可见五项总和最优候选，但只有单次官方观测，不能外推为稳定加速；隐藏十项未知。平台latest为D3，D1未自动选为基线。
- 原始证据：/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case12_gate_tail_3dirs_20261104/performance/oj_results.json、runs/20261103T163636210869Z（D1）、runs/20261103T164126144591Z（D3）。


<!-- A_case12_D1_select_submit_20261104_FINAL -->
## 2026-11-04 用户选择D1并提交一次

- 用户明确同意D1作为基线并授权一次D1重复提交；任务A_case12_D1_select_submit_20261104，授权user_20261104_A_D1_select_submit1，预算1/1已用，task closed、pending空。
- D1/member1重复提交SID 6aea12ec1dac5d235b82dc60，整体Pass，五项[476.85,2.16,9.70,68.11,33.37]us；平台latest现为D1。去重守卫在POST前要求--repeat，首次未提交未计费，第二次为唯一实际POST。
- 同SHA既有观测6aea0f471dac5d235b7addca五项[472.75,2.20,9.72,68.75,34.01]us继续保留；两次D1观测并存，不取跨版本最小值冒充单次成绩。
- 已用workspace baseline select将D1冻结快照c20423055d770d8d6624639630de361de0107ab89a9bef68af6feb370f67084e选为新流程正式基线，kernel SHA c8c234ebbdab7e0313b157ee7f82aff323cdd5b918ab051f82f2a4b7fe217ff2；正式工程该SHA一致。旧兼容current_baseline.json未重写。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/20261103T165845258447Z_2ef210740698、workspace_control/baseline.json、任务目录/attempt记录。


<!-- A_style7_refactor_20261104_FINAL -->
## 2026-11-04 七条Scalar编码原则整体风格重构：OJ变慢，回退D1

- 用户授权按Scalar 7原则整体重构一次并提交一次；任务A_style7_refactor_20261104，授权user_20261104_A_style7_refactor_submit1，预算1/1已用，member2，task closed、pending空。
- 候选SHA af0d8ff071f254c4e3137bb9207541ed500cad7ba9c86c9dc84c55e89b6c95ac：MatrixPrefetch/Tiny固定维度改constexpr并去成员、case1主循环与末尾token拆分、删除ResidentTokenBatch两个动态mask数组及未用colScale_、一个while改for。官方sample、H5连续3次、3094组/6188 launch多shape回归全部Pass。
- OJ SID 6aea17471dac5d235b8c436e整体Pass，五项[484.17,2.18,9.75,77.47,32.83]us，总和606.40us；预注册D1基线逐case中位[474.8,2.18,9.71,68.43,33.69]us、总和588.81us。候选慢17.59us，case1 +9.37、case4 +9.04，未达保留门槛。
- 按用户约定已恢复D1 kernel SHA c8c234ebbdab7e0313b157ee7f82aff323cdd5b918ab051f82f2a4b7fe217ff2，baseline指针仍为D1快照c20423055d770d8d6624639630de361de0107ab89a9bef68af6feb370f67084e；不采用风格重构版本。
- 平台latest当前是该慢候选SID；恢复平台latest到D1需要另行授权的额外POST，本轮未使用。证据：任务control/decision_plan.json、control/final_summary.json、performance/oj_result.json及runs。

## A_N3_case1_under400_ABC_pair_20261105 — H128 三路优化与双账号正式对照

父版 N3，A 基线指针与正式九文件不变；三名 DeepSeek Flash high 分别实现 A 双视图半宽点积、B 延迟列缩放、C 单视图 8×8。表内是正式 A2 同 SID 观测，分数为完成后首次精确绑定 SID 的榜单观测。

| 版本 | 账号 | SID | p1 | p2 | p3 | p4 | p5 (μs) | 分数 |
|---|---|---|---:|---:|---:|---:|---:|---:|
| A | member1 | 6aec58631dac5d235bda4b7c | 649.89 | 1.54 | 9.7 | 60.01 | 33.31 | 33.24 |
| A | member2 | 6aec58e51dac5d235bdb6da1 | 649.84 | 1.62 | 9.64 | 60.46 | 34.47 | 32.71 |
| B | member1 | 6aec5a101dac5d235bddd61e | 814.32 | 1.56 | 9.75 | 56.46 | 34.49 | 32.85 |
| B | member2 | 6aec5a911dac5d235bdeeff9 | 812.44 | 1.6 | 9.7 | 56.97 | 35.86 | 32.44 |
| C | member1 | 6aec5bf51dac5d235be1e1a8 | 1169.75 | 1.57 | 9.83 | 62.44 | 36.08 | 31.72 |
| C | member2 | 6aec5c771dac5d235be2eab8 | 1170.52 | 1.55 | 9.62 | 63.43 | 33.11 | 32.22 |
- A: 326 组设备参考/越界/确定性通过，A3 p1=682.486 μs；SHA 6778ca7798512d071b37d955ca967ee9e197e5a7d1350fd3d45df323c9b45891。
- B: 326 组设备参考/越界/确定性通过，A3 p1=879.152 μs；SHA de9b2325813ad5feaa7df08aa719e5603938f1b9a259be4c7fa7d44197909a57。
- C: 326 组设备参考/越界/确定性通过，A3 p1=1195.356 μs；SHA 22c4ba64c9fc862775a6df300cbaf59592c03ba6bc0c6e1d836bd51291ef095f。
- 融合触发路线：[]；建议 N3。三路均双次通过但比N3的case1更慢，平均总分也更低；无独立收益可融合。；等待用户选版。
- 原始提交回执、两账号实测和完整快照：/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_N3_case1_under400_ABC_pair_20261105/analysis/official_comparison.csv、/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_N3_case1_under400_ABC_pair_20261105/analysis/selection_options.json。

<!-- A_N3_case1_under400_ABC_pair_20261105:user_retained_N3 -->
- 用户在三路 A/B/C 双账号正式对照后明确保留工作区 A 的 N3。现有基线指针与正式九文件一致，不替换源码、不复交；选版回执：/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_N3_case1_under400_ABC_pair_20261105/analysis/user_retained_N3.json。

## A_N3_projection3_pair_20261105 — H128 三路优化与双账号正式对照

父版 N3，A 基线指针与正式九文件不变；三名 DeepSeek Flash high 分别实现 P2 双视图按输出并行累加、P1 地址错位对照、P3 单视图行列分开算。表内是正式 A2 同 SID 观测，分数为完成后首次精确绑定 SID 的榜单观测。

| 版本 | 账号 | SID | p1 | p2 | p3 | p4 | p5 (μs) | 分数 |
|---|---|---|---:|---:|---:|---:|---:|---:|
| P1 | member1 | 6aec6eec1dac5d235b0b9e62 | 552.33 | 1.6 | 9.85 | 60.84 | 34.17 | 32.98 |
| P1 | member2 | 6aec6f681dac5d235b0cb7c7 | 550.24 | 1.52 | 9.69 | 60.71 | 34.11 | 33.57 |
| P3 | member1 | 6aec701d1dac5d235b0e49d8 | 742.69 | 1.59 | 9.68 | 59.53 | 33.16 | 32.86 |
| P3 | member2 | 6aec70991dac5d235b0f581f | 743.2 | 1.59 | 9.74 | 59.63 | 33.2 | 32.8 |
| P2 | member1 | 6aec714f1dac5d235b10e2c4 | 900.23 | 1.52 | 9.75 | 60.86 | 34.04 | 32.85 |
| P2 | member2 | 6aec71d31dac5d235b120b71 | 898.94 | 1.58 | 9.64 | 60.38 | 33.36 | 32.7 |
| F | member1 | 6aec72a51dac5d235b13e8a2 | 628.53 | 1.55 | 9.8 | 60.23 | 33.39 | 33.13 |
| F | member2 | 6aec73271dac5d235b14fc4c | 630.88 | 1.58 | 9.82 | 60.88 | 34.04 | 32.93 |
- P1: 326 组设备参考/越界/确定性通过，A3 p1=582.028 μs；SHA 10626bdd03b2fd3f4bbc7f0dea2c7bf53238c94bf89a5fc0f9b2f4f39394d775。
- P3: 326 组设备参考/越界/确定性通过，A3 p1=769.974 μs；SHA 654d6459b2bdd3bb6a894094f95d433907905a046d64b1138855c5b7480f5eaf。
- P2: 326 组设备参考/越界/确定性通过，A3 p1=930.181 μs；SHA 772f6c6e2d913976e34cdf8171bee01e5c5ee641ca604792007037cb7edbd525。
- F: 326 组设备参考/越界/确定性通过，A3 p1=663.606 μs；SHA 7092723f0291fe69d5521f388e87043f8a0851970f5ca023026d939008c84097。
- 融合触发路线：['P1', 'P3']；建议 N3。N3 历史两测 case1 均值 479.22 µs；本轮三路和融合版双测均慢于 N3，无一低于 400 µs。仅作推荐，未选择或部署。；等待用户选版。
- 原始提交回执、两账号实测和完整快照：/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_N3_projection3_pair_20261105/analysis/official_comparison.csv、/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_N3_projection3_pair_20261105/analysis/selection_options.json。
- A3 隔离对照：保持 P3 计算不变恢复转置，I15 增加 43.45 µs；P1 相比旧 A1 的 I15 布局收益 96.43 µs。融合作同一单视图，错位放置倒数向量及纵向广播/partials。详见 analysis/fusion_decision.json。

<!-- A_N3_projection3_pair_20261105:selected_N3 -->
- 用户在八次正式对照后选择保留工作区 A 的 N3。指针及正式 9 文件已核对，没有部署或复交。证据：/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_N3_projection3_pair_20261105/analysis/user_retained_N3.json。

## A_N3_rowdelay_dma_panel_20261105 — H128 三路优化与融合版正式对照

父版 N3，A 基线指针与正式九文件不变；三名 DeepSeek Flash high 分别实现 A 延迟行缩放、B 连续 DMA、C 行面板双半步。A/B/C 各用 member1、member2 提交一次；F 两次均按用户指示使用 member3。表内是正式 A2 同 SID 观测，分数为完成后首次精确绑定 SID 的榜单观测。

| 版本 | 账号 | SID | 状态 | p1 | p2 | p3 | p4 | p5 (μs) | 分数 |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| A | member1 | 6aec7c7d1dac5d235b2aa76b | Pass | 640.24 | 1.6 | 9.61 | 62.13 | 36.08 | 32.23 |
| A | member2 | 6aec7cff1dac5d235b2bc57e | Pass | 635.42 | 1.56 | 9.73 | 62.5 | 35.82 | 32.39 |
| B | member1 | 6aec7e291dac5d235b2e7a36 | Pass | 507.29 | 1.57 | 9.82 | 58.25 | 33.17 | 33.24 |
| B | member2 | 6aec7eb21dac5d235b2fa1a5 | Pass | 507.67 | 1.53 | 9.6 | 58.01 | 33.22 | 33.45 |
| C | member1 | 6aec802e1dac5d235b32fbc8 | Pass | 865.42 | 1.55 | 9.51 | 61.32 | 35.63 | 32.44 |
| C | member2 | 6aec80af1dac5d235b340a62 | Pass | 866.04 | 1.55 | 9.64 | 61.1 | 35.89 | 32.29 |
| F | member3 | 6aec84921dac5d235b3caea8 | Pass | 483.29 | 1.54 | 9.69 | 59.53 | 34.46 | 33.28 |
| F | member3 | 6aec85831dac5d235b3eba35 | Time Limit Exceeded | — | — | — | — | — | 0 |
- A: 346 组设备参考/越界/确定性通过，A3 p1=735.495 μs；SHA 9b36cfe92f011a6887a6827bee9009524d90b3eceac43471c0d356a12c6e7d41。
- B: 346 组设备参考/越界/确定性通过，A3 p1=495.830 μs；SHA cae09117c26842c2907a7972b857c13c8b779e4d4c515d5cabf9597ba1e14123。
- C: 346 组设备参考/越界/确定性通过，A3 p1=895.562 μs；SHA 84deda10ad3f795b7dce912a1daa5f6b5b486c8e78c909c675a15223dcdd51b9。
- F: 346 组设备参考/越界/确定性通过，A3 p1=466.330 μs；SHA 96741bc56737b54f2b1e954513186a24a376eaa6e8f3a1e03e976347164f6930。
- 融合触发路线：['B', 'C']；建议 N3。正式 A2：F 第一笔 case1 483.29 μs、33.28 分；同 SHA 第二笔 case1 超时、case2–5 跳过，同 SID 榜单 0 分。N3 两次通过，case1 历史均值 479.22 μs、平均分 33.69。本轮未达到 400 μs，建议保留 N3，基线未切换。；等待用户选版。
- 原始提交回执、逐次实测和完整快照：/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_N3_rowdelay_dma_panel_20261105/analysis/official_comparison.csv、/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_N3_rowdelay_dma_panel_20261105/analysis/selection_options.json。
- 云端独立对照：B 仅输入/仅输出及 C 关闭预取/分成全扫的同源诊断见 analysis/local_conclusions.json。F 沿用 B 的算术与连续 I/O，借用 C 的下一 token 预取和矩阵角色轮换；未把 C 的递推合并进 B。

## A_N3_panel_slots_L2_m3_20261105 — N3 H128 双 panel、双矩阵 slot 和输出 L2 旁路

正式A2逐SID结果（μs，分数来自同SID榜单）：

|路线|账号|SID|状态|case1|case2|case3|case4|case5|分数|
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| C | member3 | 6aec9cae1dac5d235b718bd2 | Pass | 485.2 | 1.52 | 9.69 | 62.56 | 35.87 | 33.26 |
| C | member3 | 6aec9dd21dac5d235b741c8f | Pass | 494.87 | 1.59 | 9.7 | 62.02 | 33.23 | 33.23 |
| A | member3 | 6aec9f001dac5d235b76d050 | Pass | 740.03 | 1.61 | 9.71 | 58.99 | 33.31 | 32.52 |
| A | member3 | 6aeca0481dac5d235b79b30f | Pass | 741.38 | 1.63 | 9.75 | 58.67 | 33.36 | 32.42 |
| B | member3 | 6aeca1821dac5d235b7c455f | Pass | 557.47 | 1.55 | 9.63 | 58.97 | 34.07 | 32.9 |
| B | member3 | 6aeca2a71dac5d235b7ebe82 | Pass | 560.14 | 1.56 | 9.71 | 58.06 | 33.4 | 33.02 |
| F | member3 | 6aeca3cb1dac5d235b81633b | Pass | 462.26 | 1.55 | 9.75 | 59.23 | 36.03 | 33.28 |
| F | member3 | 6aeca4ef1dac5d235b83fb0a | Pass | 463.88 | 1.54 | 9.58 | 57.92 | 34.49 | 33.48 |
- F: SHA d50e6d4234c276149b7be44f371b4ac4a679a1dadfbc82a155eda1fb2b85e07f; A3 346 组，case1 509.43 μs。
- B: SHA d173b2f72ac475170124a142ecda8627d8249e505cba27f0f37edc7fdf752241; A3 346 组，case1 547.59 μs。
- A: SHA ae9a25780d8a76faed82e2b02746516d629340437d72df6ed1022a7ba01ad455; A3 346 组，case1 855.67 μs。
- C: SHA da9d42802e7995c27561eba5724d4d45ffab01e79078749b30a3585ae7aa7330; A3 346 组，case1 540.51 μs。
- 融合判定：选择 F10：A 的双 panel 大描述符和 B 的倒数乘法、双 slot 在受控对照中互补。候选 A3 case1 汇总 509.43 μs，N3 交错基线 537.90/537.26 μs；只给选中的完整融合源码两次 member3 正式机会。
- 推荐 F；本轮未替用户切换N3。完整证据 /mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_N3_panel_slots_L2_m3_20261105/analysis/official_comparison_with_N3.csv。

- 用户选定 F10 为工作区 A 基线（A_N3_panel_slots_L2_m3_20261105）；两次正式 case1 462.26/463.88 µs，分数 33.28/33.48。原 N3 快照保留；正式源码及基线指针已核验，SHA d50e6d4234c276149b7be44f371b4ac4a679a1dadfbc82a155eda1fb2b85e07f，证据 /mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_N3_panel_slots_L2_m3_20261105/analysis/selected_F10.json；本次新增 POST 为 0。

## A_F10_compact_whole_early_20261106 — F10 行列归约与提前预取

|版本|账号|提交 ID|case1|case2|case3|case4|case5|分数|状态|
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| F10 | member3 | 6aeca3cb1dac5d235b81633b | 462.26 | 1.55 | 9.75 | 59.23 | 36.03 | 33.28 | Pass |
| F10 | member3 | 6aeca4ef1dac5d235b83fb0a | 463.88 | 1.54 | 9.58 | 57.92 | 34.49 | 33.48 | Pass |
| A | member1 | 6aecacdb1dac5d235b95befc | 445.12 | 1.6 | 9.78 | 61.98 | 33.32 | 33.11 | Pass |
| A | member3 | 6aecae001dac5d235b982093 | 445.34 | 1.62 | 9.61 | 62.02 | 33.27 | 33.11 | Pass |
| B | member1 | 6aecaf6a1dac5d235b9b146e | 755.86 | 1.57 | 9.79 | 62.12 | 34.42 | 32.08 | Pass |
| B | member3 | 6aecb0e01dac5d235b9dec27 | 755.67 | 1.55 | 9.72 | 62.72 | 34.51 | 32.2 | Pass |
| C | member1 | 6aecb205c9ce2e3de4e9af58 | 455.16133333333335 | 1.5633333333333332 | 9.556666666666667 | 59.79866666666667 | 35.894333333333336 | 33.06 | Pass |
| C | member3 | 6aecb329c9ce2e3de4ecdfd3 | 456.719 | 1.56 | 9.606666666666667 | 61.561 | 33.984 | 33.2 | Pass |
| F | member1 | 6aecb44dc9ce2e3de4eff338 | — | — | — | — | — | — | Preparation Interrupted |
| F | member3 | 6aecb9293ea55e2ce825a634 | — | — | — | — | — | — | Preparation Interrupted |
- 来源：A 紧凑列归约，B 半行直接求和，C 提前预取；各版本独立真机校验，正式成绩按提交 ID 绑定。
- A/A2：a407fbcc208dff4d31ba68dae54f5bcd2d33dcb763b12881e72db6a1dd0e91e5，A3 case1 493.45 µs。
- B/B1：fabd5369fef357378a432b2fc7524bda834c94a2c96d0f0762feebd910781fe2，A3 case1 803.68 µs。
- C/C2：4c41caf201deecc2dc37458ed698e255045bffcedc5033b9101702e91e68b357，A3 case1 448.25 µs。
- F/F1：db7beeb7089aa702fd58005d219874621f7aa29fbf2777e645fb6cbabf831f43，A3 case1 431.69 µs。
- 融合：A2 与 C2 分别改善迭代耗时和矩阵间等待。完整验证后的 F1 本地 case1 431.69 µs；通过反序复测筛选，同一源码交两次。
- 推荐 A；用户未选新版，F10 保持基线。证据 /mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_F10_compact_whole_early_20261106/analysis/official_with_F10.csv

## A_F1_repeat_m1_m2_20261106 — 用户指定 F1 原样复投

- 账号 member1/member2 各 1 次，完整源码 SHA db7beeb7089aa702fd58005d219874621f7aa29fbf2777e645fb6cbabf831f43，基线未变。正式数据（case1–5 µs、当次同 SID 分数）：
- member1，6aecbdc4a5348dcef5c4bcce，Pass：441.63 / 1.61 / 9.73 / 61.01 / 34.49 / 33.00
- member2，6aecbee9a5348dcef5c767c7，Pass：441.33 / 1.64 / 9.77 / 60.68 / 36.19 / 32.75
- 完整核对记录 /mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_F1_repeat_m1_m2_20261106/analysis/official.csv，未做自动保留或替换。

- 用户选定 F1 为工作区 A 基线；正式 case1 441.626 / 441.325333 µs，分数 33.00 / 32.75。父版 F10 快照保留，正式工程 9 个文件与 F1 快照一致。SHA db7beeb7089aa702fd58005d219874621f7aa29fbf2777e645fb6cbabf831f43；证据 /mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_F1_repeat_m1_m2_20261106/analysis/selected_F1.json；选版新增 POST 0。

## A_F1_factor_group8_recip_20261106 — F1 延迟列缩放、分组布局与倒数

|版本|账号|提交 ID|case1|case2|case3|case4|case5|分数|状态|
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| F1 baseline | member1 | 6aecbdc4a5348dcef5c4bcce | 441.626 | 1.6133333333333333 | 9.728666666666667 | 61.010666666666665 | 34.49466666666667 | 33 | Pass |
| F1 baseline | member2 | 6aecbee9a5348dcef5c767c7 | 441.32533333333333 | 1.6366666666666667 | 9.77 | 60.684333333333335 | 36.19416666666667 | 32.75 | Pass |
| A | member1 | 6aecc6a7a5348dcef5d87721 | 488.2903333333333 | 1.5766666666666667 | 9.612 | 59.294 | 33.1545 | 33.07 | Pass |
| A | member3 | 6aecc7dfa5348dcef5db1602 | 487.8326666666667 | 1.5666666666666667 | 9.723333333333333 | 59.001 | 33.207 | 33.04 | Pass |
| C | member1 | 6aecc922a5348dcef5dddeae | 466.11566666666664 | 1.5966666666666667 | 9.556666666666667 | 63.06433333333333 | 34.083666666666666 | 32.8 | Pass |
| C | member3 | 6aecca5ca5348dcef5e0973b | 466.119 | 1.6433333333333333 | 9.636666666666667 | 63.147666666666666 | 33.126666666666665 | 32.71 | Pass |
| B | member1 | 6aeccc53a5348dcef5e45e2a | 612.4606666666666 | 1.5466666666666666 | 9.59 | 59.66866666666667 | 35.724333333333334 | 32.55 | Pass |
| B | member3 | 6aeccd77a5348dcef5e6a993 | 608.9886666666666 | 1.5566666666666666 | 9.7 | 59.644333333333336 | 35.45733333333333 | 32.48 | Pass |
- 来源：A 延迟列缩放，B 八行分组，C 矢量倒数；各版本独立真机校验，正式成绩按提交 ID 绑定。
- A/A3：8350651ef45496c9b748c5354c81cec9285a139119afdad419eb79ba3ebb8086，A3 case1 480.12 µs。
- C/C5：16c9d2b4b0b768de2414f038d32b7c3c23b35e74ad460babcbe1ac78007d8c0f，A3 case1 458.15 µs。
- B/B8：50b29c262cd0052b09b063cff3fa4d84fc8b2512ccae990071f505de2636ae49，A3 case1 647.47 µs。
- 融合：云端 A+C 行倒数融合验证通过，但 case1 为 492.82 µs，慢于 A 480.12、C 458.15 及 F1 431.84；分组 B 647.47 也没有缩短迭代。无跨路线互补收益，未申请两次正式融合机会。
- 推荐 F1；用户未选新版，F1 保持基线。证据 /mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_F1_factor_group8_recip_20261106/analysis/official_with_F1.csv

## A_F1_row_tree_pairroots_20261106_exec — F1 行归约、七级列树与双 token

|版本|账号|提交 ID|case1|case2|case3|case4|case5|分数|状态|
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| F1 baseline | member1 | 6aecbdc4a5348dcef5c4bcce | 441.626 | 1.6133333333333333 | 9.728666666666667 | 61.010666666666665 | 34.49466666666667 | 33 | Pass |
| F1 baseline | member2 | 6aecbee9a5348dcef5c767c7 | 441.32533333333333 | 1.6366666666666667 | 9.77 | 60.684333333333335 | 36.19416666666667 | 32.75 | Pass |
| A | member1 | 6aed2892a5348dcef588c04a | 442.89733333333334 | 1.5533333333333332 | 9.673333333333334 | 61.232 | 34.48766666666667 | 33.17 | Pass |
| A | member3 | 6aed29e9a5348dcef58be88b | 441.61533333333335 | 1.5566666666666666 | 9.733333333333333 | 60.931 | 34.127 | 33.12 | Pass |
| B | member1 | 6aed2d35a5348dcef593da03 | 459.11566666666664 | 1.5633333333333332 | 9.76 | 56.381 | 34.01683333333333 | 33.35 | Pass |
| B | member3 | 6aed2e59a5348dcef596b015 | 459.04 | 1.5466666666666666 | 9.81 | 56.60333333333333 | 33.22666666666667 | 33.49 | Pass |
| C | member1 | 6aed2fe0a5348dcef59a8d34 | 470.3625 | 1.5266666666666666 | 9.795333333333334 | 60.70733333333333 | 33.388 | 33.27 | Pass |
| C | member3 | 6aed3136a5348dcef59e0680 | 469.309 | 1.5866666666666667 | 9.703333333333333 | 60.62766666666667 | 33.29683333333333 | 33.05 | Pass |
| F | member1 | 6aed3742a5348dcef5ad3b63 | 436.9103333333333 | 1.5833333333333333 | 9.596666666666666 | 56.14533333333333 | 34.451 | 33.55 | Pass |
| F | member3 | 6aed3866a5348dcef5b03f67 | 436.6585 | 1.62 | 9.576666666666666 | 56.70433333333333 | 35.770833333333336 | 33.15 | Pass |
- 来源：A 先合行，B 分段预取与列树，C 双 token 合并根；各版本独立真机校验，正式成绩按提交 ID 绑定。
- A/A3：f558cc524f789741361ee6272e0da516d9b648e3ca46d5fc359577de811cb426，A3 case1 433.99 µs。
- B/B3：2f44491149050775563a9cd44e44245f82b15620254a0d400479fb455e3e922b，A3 case1 451.02 µs。
- C/C7：766566d9a661d150c1ac9e5e741eebc6f3d3f5fbfdfbe4387354d614b4863640，A3 case1 567.15 µs。
- F/F12：a098e2b54ef06fcdf5b9c7a7e86a628202993a937748788fd1354a33cb09684a，A3 case1 429.71 µs。
- 融合：B+C：每核末 token 借空闲 slot 做七级列树，其他 token 用错开八轮的双 token 调度。云端 case1 429.711/430.421 µs，F1 432.081/431.881；同调度旧树 429.801/430.271，两种末端树接近，列树独立净收益未证实。整体复测稳定快于基线及两单路，提交两次正式验证。
- 推荐 F；用户未选新版，F1 保持基线。证据 /mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_F1_row_tree_pairroots_20261106_exec/analysis/official_with_F1.csv

- Workspace A: user selected F12 (previous baseline F1). Production verified against all 9 official files; case1 436.910 / 436.659 us; no new POST. Evidence: /mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_F1_row_tree_pairroots_20261106_exec/analysis/selected_F12.json
