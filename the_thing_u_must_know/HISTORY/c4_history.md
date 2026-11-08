# Case 4 优化历史

更新日期：2026-10-23（北京时间）。此文件承载 SinkhornNorm 可见测试点 4 的对点观察、试验和经验；共性方法与完整版本 SHA 见 [整体历史](history.md)。

## 身份与证据边界

- 平台：`op_challenge_xinan_final/sinkhorn_norm`，可见结果行 case 4。
- B、S、H、iters、输入分布与当前实现路径：未知，尚无可靠 case→shape 映射。
- 下表是全局版本在本 case 上的观察，不代表此前已完成本 case 的独立定向优化。编号仅用于记录，不允许据编号分派专属实现。
- 云端活动文件在迁移时为 R4（1aa53705），Windows 与最近核对的提交为 R5（17a7d6e0）；本次未切换源码。

## 已确认的平台历史

时间统一为 μs。“下降”为相对上一版本的用时下降百分比，负值表示变慢。结果是平台显示值，有舍入且缺少重复采样。

| 版本 | 提交 | SHA前缀 | 用时 μs | 相邻版本用时下降 | 本项结果 / 显示误差 |
|---|---:|---|---:|---:|---|
| R1（A2 基线） | 928045 | `34db99ae` | 821.85 | — | Pass / 0.00% |
| R2 | 928374 | `49b5f35d` | 556.09 | 32.34% | Pass / 0.00% |
| R3 | 928539 | `7d2ce01c` | 489.53 | 11.97% | Pass / 0.00% |
| R4 | 928794 | `1aa53705` | 471.38 | 3.71% | Pass / 0.00% |
| R5 | 929094 | `17a7d6e0` | 460.56 | 2.30% | Pass / 0.00% |

方法依次为：A2索引基线、R2驻留行归一化合批、R3驻留列累加合批、R4 softmax Exp/分母广播/Div/eps合批、R5 max广播/Sub合批。完整方法、验证层级、版本保留情况见整体历史。

证据：[R1](/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/evidence/windows_20261023/work/sinkhorn_local_20261023/r2_20261023_170335/baseline_ui_results.json)、[R2/R3](/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/evidence/windows_20261023/work/sinkhorn_local_20261023/r4_softmax_20261023/r2_vs_r3_ui.json)、[R4](/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/evidence/windows_20261023/work/sinkhorn_local_20261023/r4_feedback_20261023_184008/comparison.json)、[R5](/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/evidence/r5_feedback_20261023/feedback.json)。R3 使用真实提交928539；18:17旧截图实际为R2。

## 2026-10-23 — 迁移时的观察

- R2→R3 从556.09降至489.53 μs，下降11.97%；R4→R5 从471.38降至460.56 μs，下降2.30%。最后一轮是可见五项中降幅最大者，仍只有单次显示值，需同条件重复验证。
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
- 本项：Pass，precision_ratio=1，461.58 μs；本轮R5基线 461.58 μs，加速 1.0×。
- 共性方法、其他case回退和整体决定见 [总历史](history.md)；单次用时与未知shape不足以确定本case唯一瓶颈。
- 证据：[本轮comparison](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_40/R01/comparison.json)；正式提交 6adb51fd1dac5d235bf35d7f。

## 2026-10-23 — C02（member1，keep）

- 全局候选：WholeReduceSum one-repeat rows；完整SHA 70cd60951e71df30229935d41bf1d4dcf15e3898dacaee77cf6129dd2bd1e8ba。不是按case编号分派。
- 本项：Pass，precision_ratio=1，461.18 μs；本轮R5基线 461.58 μs，加速 1.0008673403009671×。
- 共性方法、其他case回退和整体决定见 [总历史](history.md)；单次用时与未知shape不足以确定本case唯一瓶颈。
- 证据：[本轮comparison](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_40/R02/comparison.json)；正式提交 6adb52ba1dac5d235bf3ed76。

## 2026-10-23 — C03（member1，keep）

- 全局候选：WholeReduceSum all rows with original repeat order；完整SHA 91dedc25461bbbb3d1147ab9c4532c3cf8b5cf065ed1336ee6e09bae8b94088f。不是按case编号分派。
- 本项：Pass，precision_ratio=1，198.67 μs；本轮R5基线 461.58 μs，加速 2.323350279357729×。
- 共性方法、其他case回退和整体决定见 [总历史](history.md)；单次用时与未知shape不足以确定本case唯一瓶颈。
- 证据：[本轮comparison](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_40/R03/comparison.json)；正式提交 6adb543a1dac5d235bf4f664。

## 2026-10-23 — C05（member1，keep）

- 全局候选：Retry vector maxima candidate after HTTP 429 cooldown；完整SHA 2d77a04f0d857a80f4d942bd0fa4b75b8690442847524de4f69a876ad692d311。不是按case编号分派。
- 本项：Pass，precision_ratio=1，143.03 μs；本轮R5基线 461.58 μs，加速 3.2271551422778435×。
- 共性方法、其他case回退和整体决定见 [总历史](history.md)；单次用时与未知shape不足以确定本case唯一瓶颈。
- 证据：[本轮comparison](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_40/R05/comparison.json)；正式提交 6adb56541dac5d235bf66313。

## 2026-10-23 — C06（member1，confirm）

- 全局候选：Final confirmation of retained best candidate；完整SHA 2d77a04f0d857a80f4d942bd0fa4b75b8690442847524de4f69a876ad692d311。不是按case编号分派。
- 本项：Pass，precision_ratio=1，143.13 μs；本轮R5基线 461.58 μs，加速 3.2249004401592956×。
- 共性方法、其他case回退和整体决定见 [总历史](history.md)；单次用时与未知shape不足以确定本case唯一瓶颈。
- 证据：[本轮comparison](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_40/R06/comparison.json)；正式提交 6adb579c1dac5d235bf7631c。

## 2026-10-23 — 五次提交收尾

- 最终同源复测 143.13 μs；本轮R5基线 461.58 μs，加速 3.225×；Pass、precision_ratio=1。
- 全局批量归约/最大值/门控优化，不按case编号分派；shape映射仍未知。
- 最终SHA 2d77a04f0d857a80f4d942bd0fa4b75b8690442847524de4f69a876ad692d311；提交 6adb579c1dac5d235bf7631c。
- [整体结果与验证边界](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_40/final_summary.md)；本轮5/5已停止。

## 2026-10-23 — Q01（member1额度轮次）

- 全局方法：Planes column recurrence，不是按case编号分派。
- 本项：Pass，precision_ratio=1；143.82μs，相对本轮起始143.13μs加速0.9952023362536504×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA ef9466313272825664fac4550d28896201301dac28a67c0016c3bbe7a31c571b；提交6adb60e51dac5d235bfe22ed；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R01/comparison.json)。

## 2026-10-23 — Q02（member1额度轮次）

- 全局方法：Resident input double buffer prefetch，不是按case编号分派。
- 本项：Pass，precision_ratio=1；136.72μs，相对本轮起始143.13μs加速1.0468841427735518×。
- 整体决定：keep；其他case及验证边界见[整体历史](history.md)。
- SHA 0bbf4cd87e76162fcc7fcb39a1c697fd3ed786ab27f92b4e30be40bbcd3a52ff；提交6adb61fa1dac5d235bfee208；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R02/comparison.json)。

## 2026-10-23 — Q03（member1额度轮次）

- 全局方法：Packed column division with retained prefetch，不是按case编号分派。
- 本项：Pass，precision_ratio=1；147.41μs，相对本轮起始143.13μs加速0.970965334780544×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA eaffa14b9114c2df57611c01e2ed879e493dc4a91e1c4961a9e36055118a8128；提交6adb63341dac5d235bffb3b4；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R03/comparison.json)。

## 2026-10-23 — Q04（member1额度轮次）

- 全局方法：Resident token batching Q2 with platform UB budget，不是按case编号分派。
- 本项：Pass，precision_ratio=1；134.8μs，相对本轮起始143.13μs加速1.0617952522255192×。
- 整体决定：keep；其他case及验证边界见[整体历史](history.md)。
- SHA ba20fab7b1f77f45c38e220ceedf3ec2679b78f505122e88ffc798a08eecbc94；提交6adb658a1dac5d235b013a47；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R04/comparison.json)。

## 2026-10-23 — Q05（member1额度轮次）

- 全局方法：Resident token batching Q4 with platform UB budget，不是按case编号分派。
- 本项：Pass，precision_ratio=1；133.78μs，相对本轮起始143.13μs加速1.069890865600239×。
- 整体决定：keep；其他case及验证边界见[整体历史](history.md)。
- SHA 396102c2330e43208733d32f5c907de495dbf3a8a6adfe1a6cc2a85eb88957a1；提交6adb66711dac5d235b01db52；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R05/comparison.json)。

## 2026-10-23 — Q06（member1额度轮次）

- 全局方法：Resident batching cap 8，不是按case编号分派。
- 本项：Pass，precision_ratio=1；134.9μs，相对本轮起始143.13μs加速1.0610081541882876×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 50d028065d4bfacc4b6b5e3ecc1c09fa8d1f084621780aaa9f38aa7b460451e2；提交6adb67441dac5d235b026a4e；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R06/comparison.json)。

## 2026-10-23 — Q07（member1额度轮次）

- 全局方法：Resident batching cap 16，不是按case编号分派。
- 本项：Pass，precision_ratio=1；139.17μs，相对本轮起始143.13μs加速1.0284544082776461×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA a3c2a2db229815bb4d19963737fbced534f6c9c5c4e5c1bc515ff75939e6b286；提交6adb68161dac5d235b031538；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R07/comparison.json)。

## 2026-10-23 — Q08（member1额度轮次）

- 全局方法：Resident batching cap 32，不是按case编号分派。
- 本项：Pass，precision_ratio=1；134.63μs，相对本轮起始143.13μs加速1.0631360023768848×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 21d0ead62d85dabe8951495441aadfabc967132cf471c0426ff2faa0a09a8b42；提交6adb68ea1dac5d235b03bc72；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R08/comparison.json)。

## 2026-10-23 — Q09（member1额度轮次）

- 全局方法：Q4 shared work buffer offset 256B，不是按case编号分派。
- 本项：Pass，precision_ratio=1；134.89μs，相对本轮起始143.13μs加速1.0610868114760175×。
- 整体决定：keep；其他case及验证边界见[整体历史](history.md)。
- SHA cbb15d25acf518b255d0edd0b3ab5e4c921dc245b9507f039267b5c8b4b31593；提交6adb69be1dac5d235b046b42；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R09/comparison.json)。

## 2026-10-23 — Q10（member1额度轮次）

- 全局方法：Q8 batch prefetch while preserving batch size，不是按case编号分派。
- 本项：Pass，precision_ratio=1；131.69μs，相对本轮起始143.13μs加速1.0868706811451134×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA f8312d80b9e8829f2d7369a5105b8eff1d3b69c5f65fc4ccde5c5c070a6b31ba；提交6adb6a921dac5d235b050723；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R10/comparison.json)。

## 2026-10-23 — Q11（member1额度轮次）

- 全局方法：Q8 batch prefetch with capacity-driven smaller batches，不是按case编号分派。
- 本项：Pass，precision_ratio=1；131.66μs，相对本轮起始143.13μs加速1.0871183351055749×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 94acb4244a31622add652fd25c11d012a9e5aca35a8ad03bb9fe3c1418d7df5b；提交6adb6b661dac5d235b05b13d；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R11/comparison.json)。

## 2026-10-23 — Q12（member1额度轮次）

- 全局方法：Small-matrix planes batch cap 64，不是按case编号分派。
- 本项：Pass，precision_ratio=1；134.6μs，相对本轮起始143.13μs加速1.063372956909361×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA a3f24b8cf2aad039f206185dace870fd4034dacabcaa4295da234fba3485a5e2；提交6adb6c3a1dac5d235b064c06；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R12/comparison.json)。

## 2026-10-23 — Q13（member1额度轮次）

- 全局方法：Small-matrix planes batch cap 128，不是按case编号分派。
- 本项：Pass，precision_ratio=1；134.15μs，相对本轮起始143.13μs加速1.0669399925456577×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA b4710b1d75d997096aa35b6b4fc34f8bf95cb1416fa0054a690bd49fcbbf9422；提交6adb6d0d1dac5d235b06ea41；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R13/comparison.json)。

## 2026-10-23 — Q14（member1额度轮次）

- 全局方法：Small-matrix planes batch cap 256，不是按case编号分派。
- 本项：Pass，precision_ratio=1；133.95μs，相对本轮起始143.13μs加速1.0685330347144457×。
- 整体决定：keep；其他case及验证边界见[整体历史](history.md)。
- SHA 8dd74dc1752eb792e00217c4325505104051d0e7cc13e128748f70de40216298；提交6adb6de01dac5d235b0787f8；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R14/comparison.json)。

## 2026-10-23 — Q15（member1额度轮次）

- 全局方法：Small-matrix planes batch cap 512，不是按case编号分派。
- 本项：Pass，precision_ratio=1；141.55μs，相对本轮起始143.13μs加速1.0111621335217236×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 308ea9e6be07218d5adbfd97890b47469cf98421237465e5e616faadf9b0d14f；提交6adb6eb31dac5d235b08259e；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R15/comparison.json)。

## 2026-10-23 — Q16（member1额度轮次）

- 全局方法：Small-matrix planes batch cap 1024，不是按case编号分派。
- 本项：Pass，precision_ratio=1；139.77μs，相对本轮起始143.13μs加速1.0240394934535306×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 721a306abc195eb854fd7a3670de0f9a2f987d25f157544424a34e5678dcd3c5；提交6adb6f861dac5d235b08c695；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R16/comparison.json)。

## 2026-10-23 — Q17（member1额度轮次）

- 全局方法：Additional 256B statistics offset，不是按case编号分派。
- 本项：Pass，precision_ratio=1；134.53μs，相对本轮起始143.13μs加速1.063926261800342×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 9c91baed8d6afaafb5c435235fc10515a9669449c07cc9857d7f2c8eec6ad3eb；提交6adb70591dac5d235b0959a2；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R17/comparison.json)。

## 2026-10-23 — Q18（member1额度轮次）

- 全局方法：Metadata-dependent statistics offset，不是按case编号分派。
- 本项：Pass，precision_ratio=1；133.83μs，相对本轮起始143.13μs加速1.0694911454830753×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA a5b07022660a41acb7dfced56e6c5f2903ed6dab93945cc19767ec779873a3ea；提交6adb712c1dac5d235b09f3de；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R18/comparison.json)。

## 2026-10-23 — Q19（member1额度轮次）

- 全局方法：Three single-path device entries，不是按case编号分派。
- 本项：Pass，precision_ratio=1；135.11μs，相对本轮起始143.13μs加速1.0593590407815852×。
- 整体决定：keep；其他case及验证边界见[整体历史](history.md)。
- SHA fa341fa1cc2b7f91a3883292ea6c9782bcff6038c3eb59d13fdd6f01d1d01957；提交6adb71ff1dac5d235b0a93cf；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R19/comparison.json)。

## 2026-10-23 — Q20（member1额度轮次）

- 全局方法：Dense aligned elementwise stages in batched resident，不是按case编号分派。
- 本项：Pass，precision_ratio=1；134.68μs，相对本轮起始143.13μs加速1.0627413127413126×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 198d17d54937a4464cd7351d0cd4d45bcc26e2063ccb5361d55e737594ae48bf；提交6adb72d21dac5d235b0b3714；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R20/comparison.json)。

## 2026-10-23 — Q21（member1额度轮次）

- 全局方法：Dense aligned elementwise stages in both resident paths，不是按case编号分派。
- 本项：Pass，precision_ratio=1；134.06μs，相对本轮起始143.13μs加速1.067656273310458×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 4dfa4eba61620c1c54ffc26980e3fbdc06b01caaf81920a2fca6dafae3c3a0b5；提交6adb73a51dac5d235b0be066；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R21/comparison.json)。

## 2026-10-23 — Q22（member1额度轮次）

- 全局方法：列求和跨token组块，不是按case编号分派。
- 本项：Pass，precision_ratio=1；135.3μs，相对本轮起始143.13μs加速1.057871396895787×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA e34c8e461f239dfdd7a1170f5dcf354e54d09c8998f54523908f1931886ce10f；提交6adb74781dac5d235b0c792e；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R22/comparison.json)。

## 2026-10-23 — Q23（member1额度轮次）

- 全局方法：列求和及除法跨token组块，不是按case编号分派。
- 本项：Pass，precision_ratio=1；135.75μs，相对本轮起始143.13μs加速1.054364640883978×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 19e16a88cc7856f25c821b9fd493c5f4ece6edcde31f6cd02e5043d94f4f2bda；提交6adb754b1dac5d235b0d04fa；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R23/comparison.json)。

## 2026-10-23 — Q24（member1额度轮次）

- 全局方法：Q8列归一化组块，不是按case编号分派。
- 本项：Pass，precision_ratio=1；134.66μs，相对本轮起始143.13μs加速1.0628991534234369×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA dd19d5f2cdba44f118462f841ee50e294e35924230f3ac58b4c5592e32bccd06；提交6adb761e1dac5d235b0d9bc5；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R24/comparison.json)。

## 2026-10-23 — Q25（member1额度轮次）

- 全局方法：守卫式核心数紧凑分配，不是按case编号分派。
- 本项：Pass，precision_ratio=1；134.21μs，相对本轮起始143.13μs加速1.0664630057372773×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 45f4c791f69d70079f1b415352f91f1669af8077e6f006a6ace991f042677f69；提交6adb76f11dac5d235b0e2e72；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R25/comparison.json)。

## 2026-10-23 — Q26（member1额度轮次）

- 全局方法：守卫式批量对齐分配，不是按case编号分派。
- 本项：Pass，precision_ratio=1；134.44μs，相对本轮起始143.13μs加速1.0646385004462957×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 09fe685aba1d0bb42a09bcf6ab13954237ce62a0c91112db6016ac91bbf4981e；提交6adb77c41dac5d235b0ebc17；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R26/comparison.json)。

## 2026-10-23 — Q27（member1额度轮次）

- 全局方法：planes256输出索引前缀扩展，不是按case编号分派。
- 本项：Pass，precision_ratio=1；134.88μs，相对本轮起始143.13μs加速1.0611654804270463×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 53b5d91a58548c4672c11aebcc4fb63013bed40a676b6a47a359d38d741df763；提交6adb78971dac5d235b0f4d11；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R27/comparison.json)。

## 2026-10-23 — Q28（member1额度轮次）

- 全局方法：planes256输入输出索引扩展，不是按case编号分派。
- 本项：Pass，precision_ratio=1；143.46μs，相对本轮起始143.13μs加速0.9976997072354662×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA cd4474bd0e5f8c9080c12e7d47e6d948ef18ba6e5541c76ddead0c75d3a7b669；提交6adb796a1dac5d235b0fe1de；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R28/comparison.json)。

## 2026-10-23 — Q29（member1额度轮次）

- 全局方法：更大planes批次及索引前缀，不是按case编号分派。
- 本项：Pass，precision_ratio=1；143.91μs，相对本轮起始143.13μs加速0.994579945799458×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 80cb32c1e115648e03ee879ee971c2822c0a68e9566ee072509e97782aba6f4e；提交6adb7a3e1dac5d235b106e20；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R29/comparison.json)。

## 2026-10-23 — Q30（member1额度轮次）

- 全局方法：Case1目标：行与token交错布局 work256，不是按case编号分派。
- 本项：Pass，precision_ratio=1；132.17μs，相对本轮起始143.13μs加速1.0829235076038437×。
- 整体决定：keep；其他case及验证边界见[整体历史](history.md)。
- SHA bb5be613d95c6c1cf6d5f9eacafc6098d908a34dfaa0d48ed0a0b24f331b4353；提交6adb7bc61dac5d235b117f0d；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R30/comparison.json)。

## 2026-10-23 — Q31（member1额度轮次）

- 全局方法：Case1目标：行与token交错布局 work0，不是按case编号分派。
- 本项：Pass，precision_ratio=1；133.09μs，相对本轮起始143.13μs加速1.075437673754602×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 2c45ef2111bc5e5ef6e562aa0467e13e0b8cfbdb737d7dcfdfa7ebb35090f9a6；提交6adb7c991dac5d235b120d85；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R31/comparison.json)。

## 2026-10-23 — Q32（member1额度轮次）

- 全局方法：Case1目标：行Div分母展开tile64，不是按case编号分派。
- 本项：Pass，precision_ratio=1；143.73μs，相对本轮起始143.13μs加速0.9958255061573784×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 0ab5db162f799f6d1e8e3ec85fecc2c3a011b62704141afafccaca30a66ac826；提交6adb7d6d1dac5d235b12a043；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R32/comparison.json)。

## 2026-10-23 — Q33（member1额度轮次）

- 全局方法：Case1目标：行Div分母展开tile128，不是按case编号分派。
- 本项：Pass，precision_ratio=1；142.88μs，相对本轮起始143.13μs加速1.001749720044793×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 1d4533fe054c86aa75521328ddc32bc7b27055048905aea8e582bbc59ca3ce46；提交6adb7e411dac5d235b133ef6；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R33/comparison.json)。

## 2026-10-23 — Q34（member1额度轮次）

- 全局方法：Case1目标：UB偏移128对照，不是按case编号分派。
- 本项：Pass，precision_ratio=1；139.97μs，相对本轮起始143.13μs加速1.0225762663427878×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 9d34e7de50a81abe17baedab04e2b7b21e927d53aea43d8afbd1f524d5ee9289；提交6adb7f151dac5d235b13ce16；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R34/comparison.json)。


## 2026-10-24T13:48:04.977645+08:00 — 行归约5次轮 R01

- 公共方法：campaign_20261024_rowreduce_member1_5/baseline.asc；完整记录见整体 history 同轮，源码SHA dcd9794f403ebf6a3fba6af26b7b64a1319d59f201b5e37cb94d244f58abb59b。
- A2本项用时 132.38 μs，状态 Pass；相对本轮新基线 1.0。
- 整体决定 baseline；提交 6adc466c1dac5d235b8678f2；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_rowreduce_member1_5/R01/comparison.json。隐藏项不外推。


## 2026-10-24T13:56:40.348251+08:00 — 行归约5次轮 R02

- 公共方法：block_reduce/first64_block_compact_pairs.asc；完整记录见整体 history 同轮，源码SHA 27094f3ffb778a805dc7e62016520351b80f3e6cceb869fb0401dbc4413eb928。
- A2本项用时 124.69 μs，状态 Pass；相对本轮新基线 0.941909654026288。
- 整体决定 revert；提交 6adc486f1dac5d235b87db4b；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_rowreduce_member1_5/R02/comparison.json。隐藏项不外推。


## 2026-10-24T14:00:12.400207+08:00 — 行归约5次轮 R03

- 公共方法：block_reduce/full_vector_tiles_block_compact_pairs.asc；完整记录见整体 history 同轮，源码SHA 2fd0a4b32bb5af781d3ea5da5b2b40a8f2e9128f0e082fec519055853b33f20c。
- A2本项用时 132.9 μs，状态 Pass；相对本轮新基线 1.003928085813567。
- 整体决定 keep；提交 6adc49431dac5d235b886ce4；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_rowreduce_member1_5/R03/comparison.json。隐藏项不外推。


## 2026-10-24T14:04:24.941807+08:00 — 行归约5次轮 R04

- 公共方法：block_reduce/composite_full_tiles_and_first64_compact_pairs.asc；完整记录见整体 history 同轮，源码SHA ba47bc0955282436fb48cb8dcc73071d8a5d64245e25f283866d32a0f33023d7。
- A2本项用时 118.61 μs，状态 Pass；相对本轮新基线 0.8959812660522738。
- 整体决定 keep；提交 6adc4a401dac5d235b891e5a；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_rowreduce_member1_5/R04/comparison.json。隐藏项不外推。


## 2026-10-24T14:07:56.163298+08:00 — 行归约5次轮 R05

- 公共方法：campaign_20261024_rowreduce_member1_5/best.asc；完整记录见整体 history 同轮，源码SHA ba47bc0955282436fb48cb8dcc73071d8a5d64245e25f283866d32a0f33023d7。
- A2本项用时 118.6 μs，状态 Pass；相对本轮新基线 0.8959057259404744。
- 整体决定 confirm；提交 6adc4b131dac5d235b898bed；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_rowreduce_member1_5/R05/comparison.json。隐藏项不外推。


## 2026-10-24T14:10:01.940760+08:00 — 行归约5次轮结案

- A2 R01→R05 μs：[132.38, 124.69, 132.9, 118.61, 118.6]；最终相对新基线变化-10.41%，平台各轮本项均Pass。最终提交 6adc4b131dac5d235b898bed。
- 对点经验：双半完整片版本R03=132.90μs，扩展非完整片首64归约后R04/R05=118.61/118.60μs；提示扩展分支对本项有益。这是性能归因线索，不把case序号或猜测形状写入kernel。
- 正确性与范围：保留源码SHA ba47bc0955282436fb48cb8dcc73071d8a5d64245e25f283866d32a0f33023d7，最终候选4660组A3逐位/guards/input检查通过，原始归约树微测通过；严格iters、原求和树/最终Add与Div。隐藏10项细节未知。
- 决定与证据：保留复合版；今日member1已50/50，本轮5/5停止。整体方法/失败候选见history.md本节；固定证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_rowreduce_member1_5/final_audit.json，逐轮comparison.json与诊断日志保留。


## 2026-10-24T14:28:50.242599+08:00 — 短行归约member2轮 R01

- 公共方法：campaign_20261024_shortrow_member2_limit50/baseline.asc；完整记录见整体 history 同轮，源码SHA ba47bc0955282436fb48cb8dcc73071d8a5d64245e25f283866d32a0f33023d7。
- A2本项用时 117.69 μs，状态 Pass；相对本轮新基线 1.0。
- 整体决定 baseline；提交 6adc4ff91dac5d235b8ccfd3；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_shortrow_member2_limit50/R01/comparison.json。隐藏项不外推。


## 2026-10-24T14:36:43.562193+08:00 — 短行归约member2轮 R02

- 公共方法：candidates/shortrow_v1.asc；完整记录见整体 history 同轮，源码SHA 01f12292d9aaa69a07c880eb9402de0ece6e1c04c52927f7f729a191689720e8。
- A2本项用时 125.83 μs，状态 Pass；相对本轮新基线 1.0691647548644745。
- 整体决定 revert；提交 6adc51d31dac5d235b8dd273；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_shortrow_member2_limit50/R02/comparison.json。隐藏项不外推。


## 2026-10-24T14:40:47.186026+08:00 — 短行归约member2轮 R03

- 公共方法：candidates/shortrow_q8_v2.asc；完整记录见整体 history 同轮，源码SHA 2268d38c4c33dd71b313e67334870944a7dd1c406f1f268545444c4775016fd6。
- A2本项用时 118.81 μs，状态 Pass；相对本轮新基线 1.0095165264678392。
- 整体决定 revert；提交 6adc52c61dac5d235b8e54e6；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_shortrow_member2_limit50/R03/comparison.json。隐藏项不外推。


## 2026-10-24T14:45:04.619852+08:00 — 短行归约member2轮 R04

- 公共方法：candidates/resident_single_v3.asc；完整记录见整体 history 同轮，源码SHA f748ba3a462a726efea33b7ef60d52fc6452c8245002dedebe5f88394214ff8d。
- A2本项用时 119.1 μs，状态 Pass；相对本轮新基线 1.011980627071119。
- 整体决定 revert；提交 6adc53c81dac5d235b8eea12；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_shortrow_member2_limit50/R04/comparison.json。隐藏项不外推。


## 2026-10-24T15:12:49.177835+08:00 — 短行归约member2轮 R05

- 公共方法：candidates/planes_sequential_row_add_v4.asc；完整记录见整体 history 同轮，源码SHA 8a82febc5c631ba958251e9b5da7ffcfb088d8e8a0c7dc90990a28bf585feb4a。
- A2本项用时 118.78 μs，状态 Pass；相对本轮新基线 1.0092616195088793。
- 整体决定 revert；提交 6adc5a481dac5d235b9315ce；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_shortrow_member2_limit50/R05/comparison.json。隐藏项不外推。


## 2026-10-24T15:19:10.119951+08:00 — 短行归约member2轮 R06

- 公共方法：candidates/padded_shortrow_oneblock_v5b.asc；完整记录见整体 history 同轮，源码SHA 984810a0b56de8b4482765ae4a7cbcd3e34fed54f7ea7a2dd62ca3ce4b2e2844。
- A2本项用时 124.5 μs，状态 Pass；相对本轮新基线 1.0578638796839155。
- 整体决定 revert；提交 6adc5bc51dac5d235b93d224；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_shortrow_member2_limit50/R06/comparison.json。隐藏项不外推。


## 2026-10-24T15:23:05.581076+08:00 — 短行归约member2轮 R07

- 公共方法：candidates/single_padded_shortrow_v9b.asc；完整记录见整体 history 同轮，源码SHA 87771bfc136ea609d303b189de8c20d5dd66b15e052aeeebfe3982e32a3abff6。
- A2本项用时 119.76 μs，状态 Pass；相对本轮新基线 1.0175885801682387。
- 整体决定 revert；提交 6adc5cb11dac5d235b9467cd；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_shortrow_member2_limit50/R07/comparison.json。隐藏项不外推。


## 2026-10-24T15:30:17.298105+08:00 — 短行归约member2轮 R08

- 公共方法：candidates/isolated_padded_batch_entry_v12.asc；完整记录见整体 history 同轮，源码SHA b2a501f0e1656764c77a136a71b7cf5c4729e89fe4455abb35db0735e8389f9f。
- A2本项用时 124.81 μs，状态 Pass；相对本轮新基线 1.0604979182598353。
- 整体决定 revert；提交 6adc5e601dac5d235b959931；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_shortrow_member2_limit50/R08/comparison.json。隐藏项不外推。


## 2026-10-24T15:38:57.971946+08:00 — 短行归约member2轮 R09

- 公共方法：candidates/isolated_native_pitch_batch_v14.asc；完整记录见整体 history 同轮，源码SHA 33aa904c4555f8a08da6f5e2817a5f67d5df4925e98d1efd4e09af33ecb036e9。
- A2本项用时 119.25 μs，状态 Pass；相对本轮新基线 1.013255161865919。
- 整体决定 revert；提交 6adc60651dac5d235b971a50；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_shortrow_member2_limit50/R09/comparison.json。隐藏项不外推。


## 2026-10-24T15:42:30.407273+08:00 — 短行归约member2轮 R10

- 公共方法：campaign_20261024_shortrow_member2_limit50/best.asc；完整记录见整体 history 同轮，源码SHA ba47bc0955282436fb48cb8dcc73071d8a5d64245e25f283866d32a0f33023d7。
- A2本项用时 118.82 μs，状态 Pass；相对本轮新基线 1.0096014954541592。
- 整体决定 confirm；提交 6adc613e1dac5d235b97e547；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_shortrow_member2_limit50/R10/comparison.json。隐藏项不外推。


## 2026-10-24T15:42:30.404814+08:00 — member2_shortrow_final_additional5_20261024

- 结果：新基线 117.69 μs；选中版本 R01，最终确认 118.82 μs，提交 6adc613e1dac5d235b97e547。
- 最后五次对照：[('R06', 124.5, 'revert'), ('R07', 119.76, 'revert'), ('R08', 124.81, 'revert'), ('R09', 119.25, 'revert'), ('R10', 118.82, 'confirm')]。整体保留决定见history.md，不以单项最低值冒充当前版本表现。
- 精度覆盖更正：旧 v1 raw 含交替正负零，但没有纯负零整行，旧 PASS 数字真实但覆盖有限；v2 reducer 同源，v1/v2/v6 的短树风险是静态继承判断。直接失败证据仅 v5 literal raw 的480个符号零差异，不是已执行的v1失败。v5b补回P16/P32遗漏的两层/一层加正零，104配置/2496数据集逐位通过；此前 member1 的 reduction_micro、micro_pair 也只覆盖交替正负零，未覆盖纯负零整行；旧 PASS 保留。ba47的H<64原WR不受此结论影响。
- 停止与证据：用户追加5次已完成，member2今日19/50，无后续提交。/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_shortrow_member2_limit50/final_audit.json；本项可见Pass，隐藏项不外推。


## 2026-10-24T16:22:22.417572+08:00 — pipe_interleave_member2_5_R01

- 方法：baseline，SHA ba47bc0955282436fb48cb8dcc73071d8a5d64245e25f283866d32a0f33023d7；公共约束和验证见整体history同轮。
- A2本项 125.71 μs；平台 Pass；当前决定 baseline，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_pipe_interleave_member2_5/R01/comparison.json，提交 6adc6a921dac5d235b9e62de；预算 1/5，隐藏项不外推。


## 2026-10-24T16:27:17.409598+08:00 — pipe_interleave_member2_5_R02

- 方法：tpipe_only，SHA 89d70d5b34175d03fc5b477fab9bc5f4a459eb26b9b632b60bd6684097bd7649；公共约束和验证见整体history同轮。
- A2本项 118.72 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_pipe_interleave_member2_5/R02/comparison.json，提交 6adc6bbc1dac5d235b9f6c8e；预算 2/5，隐藏项不外推。


## 2026-10-24T16:30:56.607213+08:00 — pipe_interleave_member2_5_R03

- 方法：baseline_control，SHA ba47bc0955282436fb48cb8dcc73071d8a5d64245e25f283866d32a0f33023d7；公共约束和验证见整体history同轮。
- A2本项 118.03 μs；平台 Pass；当前决定 baseline_control，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_pipe_interleave_member2_5/R03/comparison.json，提交 6adc6c971dac5d235ba037c0；预算 3/5，隐藏项不外推。


## 2026-10-24T16:34:29.811622+08:00 — pipe_interleave_member2_5_R04

- 方法：interleave_only，SHA 70a206311bc5abdead20442e38e415855e14d36ab0ca818f058e77ec8195192d；公共约束和验证见整体history同轮。
- A2本项 119.28 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_pipe_interleave_member2_5/R04/comparison.json，提交 6adc6d6d1dac5d235ba0ceb8；预算 4/5，隐藏项不外推。


## 2026-10-24T16:38:01.085506+08:00 — pipe_interleave_member2_5_R05

- 方法：confirm，SHA 70a206311bc5abdead20442e38e415855e14d36ab0ca818f058e77ec8195192d；公共约束和验证见整体history同轮。
- A2本项 124.5 μs；平台 Pass；当前决定 confirmation_pending_audit，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_pipe_interleave_member2_5/R05/comparison.json，提交 6adc6e401dac5d235ba155fb；预算 5/5，隐藏项不外推。


## 2026-10-24T16:39:17.431592+08:00 — member2_pipe_interleave_final5_20261024

- 五次独立对照：[('R01', 'baseline', 125.71), ('R02', 'tpipe_only', 118.72), ('R03', 'baseline_control', 118.03), ('R04', 'interleave_only', 119.28), ('R05', 'confirm', 124.5)] us；参照为R01/R03几何均值 121.80948772571045 us。
- 保留决定：R04，SHA 70a206311bc5abdead20442e38e415855e14d36ab0ca818f058e77ec8195192d；R05本项 124.5 us，确认=True。整体选择按预设规则，不能将不同候选单项最低值拼成当前版本。
- 对点经验：同源码基线R01 125.71us、R03 118.03us，控制组揭示平台波动；不得把R02对R01的下降全部计为TPipe收益。交错未修改Scaled类算术，仍需看实际A2退化守卫，不能直接归因于spill或代码大小。
- 精度与边界：两候选各5323配置逐位通过、官方sample通过、平台可见本项Pass；严格iters/原求和次序/Div保留。纯负零整输入不替代原始归约微测；隐藏项不外推。
- 证据与停止：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_pipe_interleave_member2_5/final_audit.json、selection_before_R05.json、confirmation.json；member2本轮新增5次、今日24/50后停止，不自动续交。


## 2026-10-24T17:02:43.959378+08:00 — three_methods_member2_10_R01

- 方法：baseline，SHA 70a206311bc5abdead20442e38e415855e14d36ab0ca818f058e77ec8195192d；公共约束和验证见整体history同轮。
- A2本项 118.07 μs；平台 Pass；当前决定 baseline，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/R01/comparison.json，提交 6adc740b1dac5d235ba54506；预算 1/10，隐藏项不外推。


## 2026-10-24T17:09:18.128762+08:00 — three_methods_member2_10_R02

- 方法：candidate，SHA f4c42295d086186b4ead5a248759467de32c89ab9755a0667e1137dea0402e75；公共约束和验证见整体history同轮。
- A2本项 0 μs；平台 Fail；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/R02/comparison.json，提交 6adc75a41dac5d235ba6553c；预算 2/10，隐藏项不外推。


## 2026-10-24T17:13:46.297071+08:00 — three_methods_member2_10_R03

- 方法：candidate，SHA bb54a6c7533e76e048ee64363ff196d3c222da87ef1b753711aa0dee03efd848；公共约束和验证见整体history同轮。
- A2本项 119.01 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/R03/comparison.json，提交 6adc76a11dac5d235ba6e265；预算 3/10，隐藏项不外推。


## 2026-10-24T17:17:58.099680+08:00 — three_methods_member2_10_R04

- 方法：candidate，SHA 7dfa7dc0f964d752eebd346537f02a59dbd0b67a641b78c93af3c943d697f9e5；公共约束和验证见整体history同轮。
- A2本项 119.37 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/R04/comparison.json，提交 6adc779d1dac5d235ba7a3d1；预算 4/10，隐藏项不外推。


## 2026-10-24T17:22:17.432152+08:00 — three_methods_member2_10_R05

- 方法：baseline_control，SHA 70a206311bc5abdead20442e38e415855e14d36ab0ca818f058e77ec8195192d；公共约束和验证见整体history同轮。
- A2本项 119.17 μs；平台 Pass；当前决定 baseline_control，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/R05/comparison.json，提交 6adc78a01dac5d235ba86cbe；预算 5/10，隐藏项不外推。


## 2026-10-24T17:27:15.332410+08:00 — three_methods_member2_10_R06

- 方法：candidate，SHA 1242f8042b4abcab0a182352681a877c7b9d3fe463c8d021c541bb756ae5619e；公共约束和验证见整体history同轮。
- A2本项 117.76 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/R06/comparison.json，提交 6adc79ca1dac5d235ba97ade；预算 6/10，隐藏项不外推。


## 2026-10-24T17:30:47.750541+08:00 — three_methods_member2_10_R07

- 方法：candidate，SHA 213549a81aed766f4da5e41b9f979a84acb991966c54ec89621c8f6743fe31f5；公共约束和验证见整体history同轮。
- A2本项 118.72 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/R07/comparison.json，提交 6adc7a9f1dac5d235baa13cc；预算 7/10，隐藏项不外推。


## 2026-10-24T17:36:28.666410+08:00 — three_methods_member2_10_R08

- 方法：candidate，SHA 0af5c23189e8a50e0a148e10d74930a70833a140a53f84789dfc8c4b75eae9d5；公共约束和验证见整体history同轮。
- A2本项 118.45 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/R08/comparison.json，提交 6adc7bf41dac5d235baaf097；预算 8/10，隐藏项不外推。


## 2026-10-24T17:40:00.384210+08:00 — three_methods_member2_10_R09

- 方法：repeat，SHA 0af5c23189e8a50e0a148e10d74930a70833a140a53f84789dfc8c4b75eae9d5；公共约束和验证见整体history同轮。
- A2本项 118.55 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/R09/comparison.json，提交 6adc7cc71dac5d235bab632c；预算 9/10，隐藏项不外推。


## 2026-10-24T17:43:33.134953+08:00 — three_methods_member2_10_R10

- 方法：confirm，SHA 0af5c23189e8a50e0a148e10d74930a70833a140a53f84789dfc8c4b75eae9d5；公共约束和验证见整体history同轮。
- A2本项 117.63 μs；平台 Pass；当前决定 confirmation_pending_audit，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/R10/comparison.json，提交 6adc7d9c1dac5d235babe41b；预算 10/10，隐藏项不外推。


## 2026-10-24T17:44:20.992431+08:00 — member2_three_methods_final10_20261024

- 十次观测：[('R01', 'baseline', 118.07, 'Pass'), ('R02', 'tpipe_interleave', 0, 'Fail'), ('R03', 'rowdiv_panel', 119.01, 'Pass'), ('R04', 'ownership', 119.37, 'Pass'), ('R05', 'baseline control', 119.17, 'Pass'), ('R06', 'metadata', 117.76, 'Pass'), ('R07', 'combined_q1panel', 118.72, 'Pass'), ('R08', 'full_combined_metadata', 118.45, 'Pass'), ('R09', 'repeat selected source', 118.55, 'Pass'), ('R10', 'confirm selected source', 117.63, 'Pass')] us；R01/R05参照 118.61872491305913 us。case编号仅组织记录，形状和路径未由计时反推。
- 保留决定：R08，SHA 0af5c23189e8a50e0a148e10d74930a70833a140a53f84789dfc8c4b75eae9d5；同源码有效观测中位数 118.45 us，相对参照 下降 0.142%。整体采用依据见history同轮，不采用不同源码单点最小值拼接。
- 最终确认：R10本项 117.63 us，源码SHA 0af5c23189e8a50e0a148e10d74930a70833a140a53f84789dfc8c4b75eae9d5；确认通过=True，active_equals_latest_server=True。R10确认的服务器源码与保留源码一致。
- 精度与边界：非父版提交绑定独立strict-bits、编译和A3设备执行manifest，官方sample均通过；本项平台逐轮状态见回执。严格iters/原求和次序/Div及所有权检查的具体覆盖以 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/validation_summary.json 为准，未测范围和隐藏十项不外推。
- 经验与停止：同源码控制R01/R05=[118.07, 119.17]us；比较候选单次和同源码中位数，保留/回退以预设单项守卫为准，不能无profile归因于spill、代码大小或TPipe初始化。 本项变化是整体平台观测，缺少本版本A2阶段profile时不能认定具体阶段占比或因果。证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/final_audit.json、confirmation.json及各comparison；member2新增10次、今日34/50后停止，禁止第11次POST。


## 2026-10-24T18:13:07.228296+08:00 — colpanel_member2_10_R01

- 方法：candidate，SHA ede5d8c71f8915e211af973cf3d1fc548f337fed7f80c37f88fda714fcb57ca2；公共约束和验证见整体history同轮。
- A2本项 0 μs；平台 Fail；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R01/comparison.json，提交 6adc84991dac5d235bafa3e6；预算 1/10，隐藏项不外推。


## 2026-10-24T18:17:15.463949+08:00 — colpanel_member2_10_R02

- 方法：candidate，SHA 41256f032ffdc525cbbb994a5fa6739bd66f6ab2694dce0868df0b2abb1e0e22；公共约束和验证见整体history同轮。
- A2本项 129.59 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R02/comparison.json，提交 6adc85821dac5d235bb020c5；预算 2/10，隐藏项不外推。


## 2026-10-24T18:21:57.377014+08:00 — colpanel_member2_10_R03

- 方法：candidate，SHA 27676576450024bc6f7fd8d9afdf50150052a0d9ea2d9496d2d4478a63de04d6；公共约束和验证见整体history同轮。
- A2本项 117.56 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
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
- A2本项 130.02 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R06/comparison.json，提交 6adc89ed1dac5d235bb2d71e；预算 6/10，隐藏项不外推。


## 2026-10-24T18:39:38.307793+08:00 — colpanel_member2_10_R07

- 方法：repeat，SHA ede5d8c71f8915e211af973cf3d1fc548f337fed7f80c37f88fda714fcb57ca2；公共约束和验证见整体history同轮。
- A2本项 128.79 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R07/comparison.json，提交 6adc8ac11dac5d235bb35c8d；预算 7/10，隐藏项不外推。


## 2026-10-24T18:51:16.958949+08:00 — colpanel_member2_10_R08

- 方法：candidate，SHA 7245667081bd0341dd614d86b3abc1f48e00ce5c0191da9a3d6c4ec8ef06d161；公共约束和验证见整体history同轮。
- A2本项 126.28 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R08/comparison.json，提交 6adc8d7c1dac5d235bb51919；预算 原始 8/16，有效 5/10，本次平台失败补偿 False，member2 daily50硬上限，隐藏项不外推。


## 2026-10-24T18:54:34.939384+08:00 — colpanel_member2_10_R09

- 方法：repeat，SHA 3256f2a28bdc3a52ff446ce39f6f12f3c1c11a53b768238f5d2c46fe3bee0802；公共约束和验证见整体history同轮。
- A2本项 0 μs；平台 Fail；当前决定 platform_failure_compensated，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R09/comparison.json，提交 6adc8e511dac5d235bb5add2；预算 原始 9/16，有效 5/10，本次平台失败补偿 True，member2 daily50硬上限，隐藏项不外推。


## 2026-10-24T19:00:58.161358+08:00 — colpanel_member2_10_R10

- 方法：candidate，SHA 91b9aee73eec356f845aa36f4c2e1fa36c8dea5e42009b31eba16262783e2555；公共约束和验证见整体history同轮。
- A2本项 118.19 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
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
- A2本项 130.43 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R13/comparison.json，提交 6adc923a1dac5d235bb82221；预算 原始 13/16，有效 7/10，本次平台失败补偿 False，member2 daily50硬上限，隐藏项不外推。


## 2026-10-24T19:14:48.959947+08:00 — colpanel_member2_10_R14

- 方法：repeat，SHA 91b9aee73eec356f845aa36f4c2e1fa36c8dea5e42009b31eba16262783e2555；公共约束和验证见整体history同轮。
- A2本项 0 μs；平台 Fail；当前决定 platform_failure_compensated，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R14/comparison.json，提交 6adc930f1dac5d235bb8ad5a；预算 原始 14/16，有效 7/10，本次平台失败补偿 True，member2 daily50硬上限，隐藏项不外推。


## 2026-10-24T19:18:35.891050+08:00 — colpanel_member2_10_R15

- 方法：repeat，SHA 91b9aee73eec356f845aa36f4c2e1fa36c8dea5e42009b31eba16262783e2555；公共约束和验证见整体history同轮。
- A2本项 117.89 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R15/comparison.json，提交 6adc93e31dac5d235bb92d3e；预算 原始 15/16，有效 8/10，本次平台失败补偿 False，member2 daily50硬上限，隐藏项不外推。


## 2026-10-24T19:21:53.867194+08:00 — colpanel_member2_10_R16

- 方法：confirm，SHA 91b9aee73eec356f845aa36f4c2e1fa36c8dea5e42009b31eba16262783e2555；公共约束和验证见整体history同轮。
- A2本项 0 μs；平台 Fail；当前决定 confirmation_pending_audit，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R16/comparison.json，提交 6adc94b81dac5d235bb9bf59；预算 原始 16/16，有效 8/10，本次平台失败补偿 True，member2 daily50硬上限，隐藏项不外推。


## 2026-10-24T19:22:52.089402+08:00 — member2_colpanel_final10_20261024

- 原始 16 次回执：[('R01', 'column_panel', 0, 'Fail', 'compensated'), ('R02', 'div_mask', 129.59, 'Pass', 'effective'), ('R03', 'softmax_dense', 117.56, 'Pass', 'effective'), ('R04', 'column_q1_minimal', 0, 'Fail', 'compensated'), ('R05', 'div_full_only', 0, 'Fail', 'compensated'), ('R06', 'softmax_dense_sub', 130.02, 'Pass', 'effective'), ('R07', 'column_panel', 128.79, 'Pass', 'effective'), ('R08', 'column_q1_intcopy', 126.28, 'Pass', 'effective'), ('R09', 'div_full_only', 0, 'Fail', 'compensated'), ('R10', 'softmax_dense_costguard', 118.19, 'Pass', 'effective'), ('R11', 'repeat selected source', 0, 'Fail', 'compensated'), ('R12', 'repeat selected source', 0, 'Fail', 'compensated'), ('R13', 'repeat selected source', 130.43, 'Pass', 'effective'), ('R14', 'repeat selected source', 0, 'Fail', 'compensated'), ('R15', 'repeat selected source', 117.89, 'Pass', 'effective'), ('R16', 'confirm selected source', 0, 'Fail', 'compensated')] us；参考前轮同SHA三次中位数 118.45 us，本轮无新控制；编号不代表shape。平台失败清单 ['R01', 'R04', 'R05', 'R09', 'R11', 'R12', 'R14', 'R16']，共 8 次；来源为用户确认及通用授权“失败请求可以补额度，遇到submission failed就补一次额度”，无独立平台阶段日志佐证。每次仍占每日原始额度并完整审计；精确匹配回执从有效目标和性能统计排除。
- 保留：BASELINE，SHA 0af5c23189e8a50e0a148e10d74930a70833a140a53f84789dfc8c4b75eae9d5；前轮参考中位数 118.45 us，相对 持平 0.000%；整体条件见history，不拼接单点最优。
- 最终确认：成功confirm []，最后原始 R16 本项 0 us，SHA 91b9aee73eec356f845aa36f4c2e1fa36c8dea5e42009b31eba16262783e2555；确认通过=False。最后原始轮次 R16 后回退父版；active与平台latest源码不同，没有为修正latest追加POST。
- 精度边界：非父版绑定0af5 strict-bits/编译/A3设备manifest，全部原始sample通过；A2状态见回执。严格iters/原求和次序/Div/所有权证据见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/validation_summary.json；不外推隐藏十项。
- 经验停止：保留本项退化守卫；无新控制不能把漂移归因为spill或代码大小。 member2本轮原始 16/16，平台失败补偿 8，有效 8/10，今日 34→50/50；停止原因 daily_hard_cap_reached，有效目标达成=False。STOP已写，无未确认POST，停止后不再提交或自动继续。 证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/final_audit.json、confirmation.json及全部comparison。 补充已确认的候选观察：91b9成本门槛版R10/R15本项两次Pass为[118.19, 117.89] us，中位数 118.04 us，相对旧参考变化 -0.346%；R16平台失败导致缺少第三次成功及成功confirm，未保留并不表示本项代码失败。完整候选路径和逐版结论见总体history。


## 2026-10-24T20:05:39.846921+08:00 — parallel_member3_R01

- 分支A，SHA c4c07d7fa3fcd1bc99e0b1608db568971970743608f21d7038042102ab464173；约束与验证见整体history同轮。
- 本项 118.55 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R01/comparison.json，提交 6adc9eeb1dac5d235bc07de4。


## 2026-10-24T20:11:55.505707+08:00 — parallel_member3_R02

- 分支C，SHA b4f53e1f5820c25568d73eec67bf2cc93b4d10a4ab0fe37987f57eb1fe548bd2；约束与验证见整体history同轮。
- 本项 118.73 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R02/comparison.json，提交 6adca0631dac5d235bc18e97。


## 2026-10-24T20:16:37.140920+08:00 — parallel_member3_R03

- 分支B，SHA f2eca44b52fb44edc9f0cf31086e250324deb0120eef174acc5daa83f9980b65；约束与验证见整体history同轮。
- 本项 0 μs，A2 Fail；平台失败补偿 True，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R03/comparison.json，提交 6adca18b1dac5d235bc24f99。


## 2026-10-24T20:20:25.034146+08:00 — parallel_member3_R04

- 分支B，SHA f2eca44b52fb44edc9f0cf31086e250324deb0120eef174acc5daa83f9980b65；约束与验证见整体history同轮。
- 本项 117.27 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R04/comparison.json，提交 6adca2601dac5d235bc2cf19。


## 2026-10-24T20:23:58.519175+08:00 — parallel_member3_R05

- 分支A，SHA 19ff0a69a2e644d442b8a40a792c2628bdc4c78fff688d8e7000a0774ee2fdfb；约束与验证见整体history同轮。
- 本项 117.83 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R05/comparison.json，提交 6adca3351dac5d235bc35285。


## 2026-10-24T20:27:25.305700+08:00 — parallel_member3_R06

- 分支B，SHA d9d09774380da89f4fb9bf918f6f8015f9978f50624af58eaa2f0acaa4302071；约束与验证见整体history同轮。
- 本项 0 μs，A2 Fail；平台失败补偿 True，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R06/comparison.json，提交 6adca4091dac5d235bc3e229。


## 2026-10-24T20:31:03.358069+08:00 — parallel_member3_R07

- 分支B，SHA d9d09774380da89f4fb9bf918f6f8015f9978f50624af58eaa2f0acaa4302071；约束与验证见整体history同轮。
- 本项 130.28 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R07/comparison.json，提交 6adca4de1dac5d235bc46d7a。


## 2026-10-24T20:34:36.526804+08:00 — parallel_member3_R08

- 分支C，SHA 985def93a6fd8953a6a8051d9de8971c48ac0f458b74607dbc813384e019f8ef；约束与验证见整体history同轮。
- 本项 130.07 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R08/comparison.json，提交 6adca5b41dac5d235bc50172。


## 2026-10-24T20:38:09.272308+08:00 — parallel_member3_R09

- 分支A，SHA 924c58ae542c952306af7b6ade561dbe42ebcc6e6fcdc1bcf86d726656ab69e6；约束与验证见整体history同轮。
- 本项 117.92 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R09/comparison.json，提交 6adca6881dac5d235bc5890a。


## 2026-10-24T20:41:41.095574+08:00 — parallel_member3_R10

- 分支B，SHA 3507c71a25a5e204010ecad1bc21a147954614f72ebf805d8fb3b04bfa72ab49；约束与验证见整体history同轮。
- 本项 118.58 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R10/comparison.json，提交 6adca75c1dac5d235bc614d0。


## 2026-10-24T20:45:13.230159+08:00 — parallel_member3_R11

- 分支C，SHA 0d11fbacfa1b7d5bf33af9d0c82f3bcc40db17d07df092bd602ac280d4361775；约束与验证见整体history同轮。
- 本项 118.61 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R11/comparison.json，提交 6adca8301dac5d235bc68c6e。


## 2026-10-24T20:48:45.000914+08:00 — parallel_member3_R12

- 分支A，SHA 924c58ae542c952306af7b6ade561dbe42ebcc6e6fcdc1bcf86d726656ab69e6；约束与验证见整体history同轮。
- 本项 119.19 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R12/comparison.json，提交 6adca9041dac5d235bc71e95。


## 2026-10-24T20:52:01.657790+08:00 — parallel_member3_R13

- 分支B，SHA 3507c71a25a5e204010ecad1bc21a147954614f72ebf805d8fb3b04bfa72ab49；约束与验证见整体history同轮。
- 本项 0 μs，A2 Fail；平台失败补偿 True，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R13/comparison.json，提交 6adca9d81dac5d235bc79984。


## 2026-10-24T20:55:48.789461+08:00 — parallel_member3_R14

- 分支B，SHA 3507c71a25a5e204010ecad1bc21a147954614f72ebf805d8fb3b04bfa72ab49；约束与验证见整体history同轮。
- 本项 118.83 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R14/comparison.json，提交 6adcaaac1dac5d235bc8259a。


## 2026-10-24T20:59:21.593061+08:00 — parallel_member3_R15

- 分支C，SHA b4f53e1f5820c25568d73eec67bf2cc93b4d10a4ab0fe37987f57eb1fe548bd2；约束与验证见整体history同轮。
- 本项 130.6 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R15/comparison.json，提交 6adcab811dac5d235bc8a51e。


## 2026-10-24T21:02:54.363493+08:00 — parallel_member3_R16

- 分支B，SHA 3507c71a25a5e204010ecad1bc21a147954614f72ebf805d8fb3b04bfa72ab49；约束与验证见整体history同轮。
- 本项 118.57 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R16/comparison.json，提交 6adcac551dac5d235bc92c45。


## 2026-10-24T21:06:26.041076+08:00 — parallel_member3_R17

- 分支C，SHA 0d11fbacfa1b7d5bf33af9d0c82f3bcc40db17d07df092bd602ac280d4361775；约束与验证见整体history同轮。
- 本项 117.61 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R17/comparison.json，提交 6adcad291dac5d235bc9b25d。


## 2026-10-24T21:09:58.027296+08:00 — parallel_member3_R18

- 分支A，SHA 924c58ae542c952306af7b6ade561dbe42ebcc6e6fcdc1bcf86d726656ab69e6；约束与验证见整体history同轮。
- 本项 117.89 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R18/comparison.json，提交 6adcadfd1dac5d235bca32c5。


## 2026-10-24T21:13:09.146962+08:00 — parallel_member3_3x5_FINAL_20261024

- 本轮公共方法/完整SHA/验证见整体history同标记；最终A/v3 `924c58ae542c952306af7b6ade561dbe42ebcc6e6fcdc1bcf86d726656ab69e6`，严格iters、原求和次序和Div。
- 本项同SHA三次中位数 117.920µs；旧父版历史参考 118.040µs，耗时变化 -0.102%。最新确认本项 117.89µs；没有新增同期基线。
- 各路最终候选本项中位数 {'A': 117.92, 'B': 117.27, 'C': 118.11}；不拼接各候选最低值。C/v1同SHA R02→R15从118.73升到130.60µs，说明运行波动参与，不能把所有回退归因源码。
- 决定：保留全局A/v3，三路各5次有效已停；隐藏十项细节未知。证据 `/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/REPORT.md` 和 `/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/final_analysis.json`；最新提交 `6adcadfd1dac5d235bca32c5`。



## 2026-10-24T21:28:13.482985+08:00 — local_A3_perf_once_local_perf_20261024T132308Z_924c58ae

- 当前最佳源码SHA `924c58ae542c952306af7b6ade561dbe42ebcc6e6fcdc1bcf86d726656ab69e6`，本地A3单次会话；生产kernel未修改、没有A2提交。
- workload B/S/H/iters=3/32/88/20来自历史探针，eps1e-6和输入uniform[-2,2]为本地假设，不作为生产专用分派依据。
- A2同源码三次历史中位数 117.92µs；A3记录30次中位数 110.74µs，范围110.22–110.94µs，A3耗时变化-6.09%。不能归因纯芯片或当作同期配对结果。
- 五组校验与原始CSV见 `/mnt/workspace/enjoy_ur_time/others/local_perf_20261024T132308Z_924c58ae/REPORT.md` 和comparison.json；本轮只做一次本地测评，NPU锁释放，提交STOP保持。



## 2026-10-24T22:08:04.901153+08:00 — cases345_max_member3_R01

- 分支A，SHA ddec95e49e566a246dab41b1c301ba2c7211cb9c82c6ab5b6be75bf0fd8bfe6c；约束与验证见整体history同轮。
- 本项 118.49 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R01/comparison.json，提交 6adcbb9c1dac5d235bd2ea25。


## 2026-10-24T22:12:27.589595+08:00 — cases345_max_member3_R02

- 分支C，SHA 1bc3e59e4a62f9714669e9a4c092e1397b6e27128b52f07542e311b8fb704366；约束与验证见整体history同轮。
- 本项 0 μs，A2 Fail；平台失败补偿 False，平台失败 True，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R02/comparison.json，提交 6adcbcb21dac5d235bd3a127。


## 2026-10-24T22:17:48.275114+08:00 — cases345_max_member3_R03

- 分支C，SHA 1bc3e59e4a62f9714669e9a4c092e1397b6e27128b52f07542e311b8fb704366；约束与验证见整体history同轮。
- 本项 118.47 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R03/comparison.json，提交 6adcbde31dac5d235bd46196。


## 2026-10-24T22:21:05.068090+08:00 — cases345_max_member3_R04

- 分支A，SHA 44d7468872b70f18b3626d8861f940aafb945a940f984e8f33651dd10bbba722；约束与验证见整体history同轮。
- 本项 0 μs，A2 Fail；平台失败补偿 False，平台失败 True，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R04/comparison.json，提交 6adcbeb71dac5d235bd4e9e1。


## 2026-10-24T22:24:58.110910+08:00 — cases345_max_member3_R05

- 分支A，SHA 44d7468872b70f18b3626d8861f940aafb945a940f984e8f33651dd10bbba722；约束与验证见整体history同轮。
- 本项 130.98 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R05/comparison.json，提交 6adcbf8c1dac5d235bd56f24。


## 2026-10-24T22:29:06.701136+08:00 — cases345_max_member3_R06

- 分支A，SHA 172977f03347d73b5c651020e2a7fd8a5d25450f205b5e62d5e7f5db3f87e8e5；约束与验证见整体history同轮。
- 本项 118.08 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R06/comparison.json，提交 6adcc08a1dac5d235bd60e6b。


## 2026-10-24T22:34:08.713852+08:00 — cases345_max_member3_R07

- 分支C，SHA 1cbd576d3adbab76ea8c52b6aac43437297819e26ac5b49aa6f85bc4bb6578fe；约束与验证见整体history同轮。
- 本项 130.82 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R07/comparison.json，提交 6adcc1b31dac5d235bd6e585。


## 2026-10-24T22:40:57.379814+08:00 — cases345_max_member3_R08

- 分支B，SHA bf04826db0b6f59abba7460c845e308de95b25bb4462358a3f649ad9ff23861a；约束与验证见整体history同轮。
- 本项 103.69 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R08/comparison.json，提交 6adcc3501dac5d235bd8152d。


## 2026-10-24T22:44:30.189549+08:00 — cases345_max_member3_R09

- 分支A，SHA aebb7faf77b915fa459a7f996606571af9d534fbcd5dc0263306a7cdc26918a1；约束与验证见整体history同轮。
- 本项 129.88 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R09/comparison.json，提交 6adcc4251dac5d235bd8a7b1。


## 2026-10-24T22:50:54.714792+08:00 — cases345_max_member3_R10

- 分支A，SHA aebb7faf77b915fa459a7f996606571af9d534fbcd5dc0263306a7cdc26918a1；约束与验证见整体history同轮。
- 本项 130.02 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R10/comparison.json，提交 6adcc5a61dac5d235bd9bbc4。


## 2026-10-24T22:59:45.324153+08:00 — cases345_max_member3_R11

- 分支C，SHA d117c6ecc8b2ea1b206ccfca0af45a3ac67bf0991204b7854deb32731cce8632；约束与验证见整体history同轮。
- 本项 116.99 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R11/comparison.json，提交 6adcc7b81dac5d235bdb4fc9。


## 2026-10-24T23:03:22.754833+08:00 — cases345_max_member3_R12

- 分支B，SHA adc8b8d677b3c5fa3eb270cc6103efd9e9bfa6665d437b0c538d7d1c165cdfc9；约束与验证见整体history同轮。
- 本项 101.47 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R12/comparison.json，提交 6adcc88d1dac5d235bdc0db8。


## 2026-10-24T23:06:49.482580+08:00 — cases345_max_member3_R13

- 分支C，SHA 680ac58779f099d252beae0a1fc2089c7266bec1fd07f04da830f3dd9053106a；约束与验证见整体history同轮。
- 本项 118.44 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R13/comparison.json，提交 6adcc9611dac5d235bdcc633。


## 2026-10-24T23:10:22.208871+08:00 — cases345_max_member3_R14

- 分支C，SHA 680ac58779f099d252beae0a1fc2089c7266bec1fd07f04da830f3dd9053106a；约束与验证见整体history同轮。
- 本项 118.59 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R14/comparison.json，提交 6adcca351dac5d235bdd5c17。


## 2026-10-24T23:15:15.407819+08:00 — cases345_max_member3_R15

- 分支M，SHA 21dab72f389edddfafc7531de172f86957ae3e5f270be750b31e5dba529ef096；约束与验证见整体history同轮。
- 本项 111.67 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R15/comparison.json，提交 6adccb5a1dac5d235bde897f。


## 2026-10-24T23:18:52.882580+08:00 — cases345_max_member3_R16

- 分支M，SHA 21dab72f389edddfafc7531de172f86957ae3e5f270be750b31e5dba529ef096；约束与验证见整体history同轮。
- 本项 112.38 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R16/comparison.json，提交 6adccc2f1dac5d235bdf2b25。


## 2026-10-24T23:23:30.524029+08:00 — cases345_max_member3_R17

- 分支C，SHA 680ac58779f099d252beae0a1fc2089c7266bec1fd07f04da830f3dd9053106a；约束与验证见整体history同轮。
- 本项 118.32 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R17/comparison.json，提交 6adccd4a1dac5d235bdfde6a。


## 2026-10-24T23:30:08.945616+08:00 — cases345_max_member3_final_C6

- 方法/经验：B1/B2 A3仅2–4%未上A2；B3合批=103.69µs，B5 compact BR8与mask复用=101.47µs。融合111.67/112.38µs。按用户公开五项整体优先恢复C6，本项回到原scaled路径；B5为独立已验证候选。
- A2同源码中位：C6 118.4400µs，融合 112.0250µs，原基线 117.9200µs；最新确认118.32µs。
- 保留：用户选择C6，SHA 680ac58779f099d252beae0a1fc2089c7266bec1fd07f04da830f3dd9053106a；提交6adccd4a1dac5d235bdfde6a。本轮原始17/32，M2/2完成，失败计数，停止续交；隐藏十项未知。
- 证据：C6 10635设备配置执行含1008 holdout全逐位通过，guard/unwritten/input_changes为0；[完整报告](/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/REPORT.md)、[最终选用](/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/final_selection.json)。


## 2026-10-25T00:10:18.370921+08:00 — cases145_max_member1_20261025_R01

- 分支M，SHA 680ac58779f099d252beae0a1fc2089c7266bec1fd07f04da830f3dd9053106a；约束与验证见整体history同轮。
- 本项 118.7 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R01/comparison.json，提交 6adcd8411dac5d235be77d01。


## 2026-10-25T00:22:59.256150+08:00 — cases145_max_member1_20261025_R02

- 分支D，SHA 57a3f2a87e99c94111e2fbf74da4f382d7a4fe1b147d03278aaa1a2731921245；约束与验证见整体history同轮。
- 本项 117.78 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R02/comparison.json，提交 6adcdb3a1dac5d235be9d4d8。


## 2026-10-25T00:29:37.120625+08:00 — cases145_max_member1_20261025_R03

- 分支C，SHA 17bcdfa9031bab1473eb0508c0756413bd627280a064bd26fe3a1e8ec3a3a07b；约束与验证见整体history同轮。
- 本项 118.87 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R03/comparison.json，提交 6adcdcc31dac5d235bead09f。


## 2026-10-25T00:32:41.852976+08:00 — cases145_max_member1_20261025_R04

- 分支B，SHA 13da845bd6428bd54a221618bedd83cfbea235a797c39b878762abcec78415b3；约束与验证见整体history同轮。
- 本项 105.75 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R04/comparison.json，提交 6adcdd811dac5d235beb583e。


## 2026-10-25T00:37:27.022071+08:00 — cases145_max_member1_20261025_R05

- 分支D，SHA d5e6b51003bd92dd03282e8b799007835110bf397413fa5e9d2113c7ac6e2217；约束与验证见整体history同轮。
- 本项 119.09 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R05/comparison.json，提交 6adcde991dac5d235bec2160。


## 2026-10-25T00:41:44.288049+08:00 — cases145_max_member1_20261025_R06

- 分支B，SHA f3e47ee4a9424579cafb6723c550bba373e4d025cee9591ae3527b66a724e4db；约束与验证见整体history同轮。
- 本项 105.26 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R06/comparison.json，提交 6adcdf9f1dac5d235becda91。


## 2026-10-25T00:51:05.979518+08:00 — cases145_max_member1_20261025_R07

- 分支C，SHA 4e995cb2850a3473d2ce2ea0af5b40199d3fd5675f3d6c79840d07c2fcf135fa；约束与验证见整体history同轮。
- 本项 117.85 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R07/comparison.json，提交 6adce1c71dac5d235bee8021。


## 2026-10-25T00:54:57.725830+08:00 — cases145_max_member1_20261025_R08

- 分支B，SHA f8a672bbcff3400593b795f172fedc290a5d2cec3377c87ac5cc1e960e1f2af4；约束与验证见整体history同轮。
- 本项 106.19 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R08/comparison.json，提交 6adce2b91dac5d235bef5cb8。


## 2026-10-25T01:06:30.198238+08:00 — cases145_max_member1_20261025_R09

- 分支D，SHA f1f310bd2bfcf3906aa898b34096ae9c2524f8c963e3847f177f631d5bc23d93；约束与验证见整体history同轮。
- 本项 120.11 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R09/comparison.json，提交 6adce56d1dac5d235bf1110e。


## 2026-10-25T01:10:49.994077+08:00 — cases145_max_member1_20261025_R10

- 分支B，SHA 12b01f4c87a01c609aa3ae132203bf43a50e3e361b9346f781e8030587e693b9；约束与验证见整体history同轮。
- 本项 109.38 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R10/comparison.json，提交 6adce66c1dac5d235bf1a51b。


## 2026-10-25T01:14:09.247285+08:00 — cases145_max_member1_20261025_R11

- 分支D，SHA 9c87bf37552adfc1c325a99da772fb563ae224e7fc654f88acf40ed75b8f899e；约束与验证见整体history同轮。
- 本项 119.38 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R11/comparison.json，提交 6adce7331dac5d235bf226f9。


## 2026-10-25T01:32:39.557571+08:00 — cases145_max_member1_20261025_R13

- 分支C，SHA f113a769b1cf3d514aa075de4219fdbd955d8898f883cfd6f6b7fe6d4c245880；约束与验证见整体history同轮。
- 本项 118.37 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R13/comparison.json，提交 6adceb8a1dac5d235bf4ef19。


## 2026-10-25T01:35:34.733093+08:00 — cases145_max_member1_20261025_R14

- 分支B，SHA 8efe54ba6cd2c2dd4f77aa1d4873f4d56258ead1618d7f42859d68edd4a8783a；约束与验证见整体history同轮。
- 本项 116.56 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R14/comparison.json，提交 6adcec3e1dac5d235bf561f0。


## 2026-10-25T01:39:30.135164+08:00 — cases145_max_member1_20261025_R15

- 分支D，SHA 06e778648b3fbddacc5720e595a14e51caac8d6ab27f6c39dbe5514a3e3ecb24；约束与验证见整体history同轮。
- 本项 119.4 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R15/comparison.json，提交 6adced291dac5d235bf5f576。


## 2026-10-25T01:46:59.707753+08:00 — cases145_max_member1_20261025_R17

- 分支D，SHA f77cc8fa5461943ab111370f430bb2df715c86b10d63e8d2ad7626e1c682bf4e；约束与验证见整体history同轮。
- 本项 129.11 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R17/comparison.json，提交 6adceeeb1dac5d235bf72397。


## 2026-10-25T01:57:02.170458+08:00 — cases145_max_member1_20261025_R18

- 分支D，SHA 9c87bf37552adfc1c325a99da772fb563ae224e7fc654f88acf40ed75b8f899e；约束与验证见整体history同轮。
- 本项 120.2 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R18/comparison.json，提交 6adcf1451dac5d235bf8ac88。


## 2026-10-25T02:00:29.601221+08:00 — cases145_max_member1_20261025_R19

- 分支B，SHA ae862a6bae960c4be49e12b4f849f9f1675e27fce89c64348d7fbb69aa7b4a43；约束与验证见整体history同轮。
- 本项 106.71 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R19/comparison.json，提交 6adcf2151dac5d235bf93325。


## 2026-10-25T02:04:02.748948+08:00 — cases145_max_member1_20261025_R20

- 分支B，SHA f3e47ee4a9424579cafb6723c550bba373e4d025cee9591ae3527b66a724e4db；约束与验证见整体history同轮。
- 本项 105.02 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R20/comparison.json，提交 6adcf2e51dac5d235bf9ca86。


## 2026-10-25T02:07:30.173349+08:00 — cases145_max_member1_20261025_R21

- 分支D，SHA a0bc1f2d62258843738a0db76351fd73f081b4b2c2d4b014c080ef2051324f1c；约束与验证见整体history同轮。
- 本项 127.5 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R21/comparison.json，提交 6adcf3b41dac5d235bfa551c。


## 2026-10-25T02:11:19.768897+08:00 — cases145_max_member1_20261025_R22

- 分支C，SHA 680ac58779f099d252beae0a1fc2089c7266bec1fd07f04da830f3dd9053106a；约束与验证见整体history同轮。
- 本项 117.47 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R22/comparison.json，提交 6adcf49a1dac5d235bfaf0ff。


## 2026-10-25 中点诊断 — cases145_stage_B

- B2两次A2 case4为105.26/105.02µs，case5为78.29/78.33；保留稳定donor。B6虽缩减UB且A3保持收益，A2短行退化，在切回B2后恢复，不保留为全局最佳。
- A3独立阶段core1和40均逐位/guard/input通过。H88/q3/valid3，B5行Mul从0.660312到0.982461µs/次（1.488倍）、行Div从0.822812到1.552773（1.887倍）；未改阶段约1.0。
- B5行ApplyRows repeat528→363，但API4→33，真实阶段更慢；不能只数repeat或以小FUNC解释收益。B2/B5 scaled FUNC7984/7148B，机器指令解码不可用，A2编译物未知。
- 下一步独立B7控制/地址展开及ReduceRows子阶段诊断；新源码fresh43+holdout和B2增量ABBA。证据：B/stage_micro_b2_b5/parent_profile_cores40/comparison.json、中央R19/R20、B/MIDPOINT.md。


## 2026-10-25T02:17:59.689058+08:00 — cases145_max_member1_20261025_R23

- 分支C，SHA 5244c778c74719b0e4f23138a9c46480ef729eb9d5bfe8dfe4925e66577b711a；约束与验证见整体history同轮。
- 本项 126.26 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R23/comparison.json，提交 6adcf62f1dac5d235bfc07ac。


## 2026-10-25T02:21:26.439973+08:00 — cases145_max_member1_20261025_R24

- 分支C，SHA 5244c778c74719b0e4f23138a9c46480ef729eb9d5bfe8dfe4925e66577b711a；约束与验证见整体history同轮。
- 本项 126.59 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R24/comparison.json，提交 6adcf6fe1dac5d235bfc9301。


## 2026-10-25T02:24:53.196004+08:00 — cases145_max_member1_20261025_R25

- 分支C，SHA 680ac58779f099d252beae0a1fc2089c7266bec1fd07f04da830f3dd9053106a；约束与验证见整体history同轮。
- 本项 129.44 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R25/comparison.json，提交 6adcf7cc1dac5d235bfd13ec。

### 2026-10-25 cases145 R22-R25 A2 control drift correction

- C6/phase/phase/C6: c3 16.76/17.69/17.79/18.35, c4 117.47/126.26/126.59/129.44, c5 81.05/87.06/86.96/87.81 us; all Pass, source/server bindings match.
- End control C6 itself c3/4/5 +9.5/+10.2/+8.34% versus start. This pair cannot establish bank-phase harm or benefit; time/device drift is a live confounder, not a proven cause. Earlier short-case regressions also cannot be assigned to A2 compiler layout from source equality.
- C phase not selected as a donor without demonstrable gain; follow-up candidates need nearby controls. Stage proxy effects are not additive whole-kernel shares.
- Evidence campaign_20261025_cases145_member1_max_50 R22-R25, SID6adcf49a1dac5d235bfaf0ff /6adcf62f1dac5d235bfc07ac /6adcf6fe1dac5d235bfc9301 /6adcf7cc1dac5d235bfd13ec.


## 2026-10-25T02:35:26.624217+08:00 — cases145_max_member1_20261025_R26

- 分支B，SHA f3e47ee4a9424579cafb6723c550bba373e4d025cee9591ae3527b66a724e4db；约束与验证见整体history同轮。
- 本项 0 μs，A2 Time Limit Exceeded；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R26/comparison.json，提交 6adcf8d31dac5d235bfdcaca。


## 2026-10-25T02:36:35.519788+08:00 — cases145_max_member1_20261025_R27

- 分支M，SHA 26ee0ad7a53014af714da5934985498d1519f86778afb2603c5774e490be4b16；约束与验证见整体history同轮。
- 本项 105.64 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R27/comparison.json，提交 6adcfa861dac5d235bfeee28。


## 2026-10-25T02:39:57.724663+08:00 — cases145_max_member1_20261025_R28

- 分支B，SHA f3e47ee4a9424579cafb6723c550bba373e4d025cee9591ae3527b66a724e4db；约束与验证见整体history同轮。
- 本项 106.43 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R28/comparison.json，提交 6adcfb551dac5d235bff71af。

### 2026-10-25 B8 split-stage diagnostic (parent A3 actual)

- Bound binary413aa0e7, cores1/40,1176 launches each. Initial parser only matched B2 because compiled B8 entry retained the name _b5; exact symbol-to-class mapping repaired in analyze_opnames_v2.py,17 negative checks, original CSV/binary unchanged. No repeated NPU run for parsing.
- At40cores H88q3valid3: First64BR0.271953, MaskedTailWR1.226641, Compact8BR0.105859, FinalAdd0.093086, full ReduceRows1.504609 us/proxy call. Different proxies include distinct setup/drains; never sum them into a full-kernel fraction.
- B8 fullReduceRows1.511641 (+0.47%); H96 also no gain, valid2 original control unchanged. Mask caching not selected for A2. Target the original masked WR path only with exact tree/bit-copy/alias proof.
- R26 unchanged B2 returned terminal Time Limit Exceeded, no valid timing, SID6adcf8d31dac5d235bfdcaca. Raw accepted/day consumes1, effective0. Cause unknown, despite prior two Pass results; do not call it a proven platform defect.


## 2026-10-25T02:43:30.520861+08:00 — cases145_max_member1_20261025_R29

- 分支M，SHA 26ee0ad7a53014af714da5934985498d1519f86778afb2603c5774e490be4b16；约束与验证见整体history同轮。
- 本项 106.14 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R29/comparison.json，提交 6adcfc251dac5d235bfff258。


## 2026-10-25T02:46:57.864763+08:00 — cases145_max_member1_20261025_R30

- 分支B，SHA f3e47ee4a9424579cafb6723c550bba373e4d025cee9591ae3527b66a724e4db；约束与验证见整体history同轮。
- 本项 105.2 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R30/comparison.json，提交 6adcfcf41dac5d235b007005。


## 2026-10-25T02:51:27.587581+08:00 — cases145_max_member1_20261025_R31

- 分支D，SHA 57a3f2a87e99c94111e2fbf74da4f382d7a4fe1b147d03278aaa1a2731921245；约束与验证见整体history同轮。
- 本项 124.47 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R31/comparison.json，提交 6adcfe071dac5d235b0122d5。


## 2026-10-25T02:55:00.769627+08:00 — cases145_max_member1_20261025_R32

- 分支M，SHA 7c3275dd848553fa06334508f4f4ac3b2918aa0fd0e9046f0e78b4122478f55a；约束与验证见整体history同轮。
- 本项 106.29 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R32/comparison.json，提交 6adcfed71dac5d235b019dd5。


## 2026-10-25T02:58:28.888350+08:00 — cases145_max_member1_20261025_R33

- 分支D，SHA d5e6b51003bd92dd03282e8b799007835110bf397413fa5e9d2113c7ac6e2217；约束与验证见整体history同轮。
- 本项 128.52 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R33/comparison.json，提交 6adcffa71dac5d235b021c36。


## 2026-10-25T03:01:56.709644+08:00 — cases145_max_member1_20261025_R34

- 分支M，SHA 26ee0ad7a53014af714da5934985498d1519f86778afb2603c5774e490be4b16；约束与验证见整体history同轮。
- 本项 106.37 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R34/comparison.json，提交 6add00771dac5d235b02984b。


## 2026-10-25T03:05:24.114680+08:00 — cases145_max_member1_20261025_R35

- 分支D，SHA 9c87bf37552adfc1c325a99da772fb563ae224e7fc654f88acf40ed75b8f899e；约束与验证见整体history同轮。
- 本项 119.68 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R35/comparison.json，提交 6add01461dac5d235b033068。


## 2026-10-25T03:09:07.836377+08:00 — cases145_max_member1_20261025_R36

- 分支M，SHA 7c3275dd848553fa06334508f4f4ac3b2918aa0fd0e9046f0e78b4122478f55a；约束与验证见整体history同轮。
- 本项 106.69 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R36/comparison.json，提交 6add022b1dac5d235b03f77e。


## 2026-10-24T19:12:31.640926+00:00 — cases145_final_diagnostic_gates_20261025

- 方法：保持原生masked WR源树，独立测试dst stride1→8、uint32 Gather压缩，未用+0或Mul复制。
- 验证：h88cores1、allcores1/allcores40原始NaN/±0/消去位型与所有guard/input检查通过；各完整CSV均匹配已冻结binary/source。
- 结果/决定：40核H88 q3v3纯尾WR1.233516→1.233750μs(无收益)，含压缩1.233125→1.287188(+4.38%)；其他宽尾也更慢3.70~4.61%。不建立生产候选、不A2；B2继续donor。
- 证据/经验：B/tail_sparse_bitpack_diag/parent_profile_all_cores40/comparison.json；稀疏dst并未改善本代理，Gather增加成本；此实验不证明所有bank冲突不存在，也不代表A2生产。


## 2026-10-25T03:14:04.232978+08:00 — cases145_max_member1_20261025_R37

- 分支M，SHA 06fb13aefcd79b8bef105479e11a0d5e7e880056b1ac8187ea2d0cc5aad369c8；约束与验证见整体history同轮。
- 本项 107.54 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R37/comparison.json，提交 6add03531dac5d235b04a006。


## 2026-10-25T03:17:30.930966+08:00 — cases145_max_member1_20261025_R38

- 分支D，SHA 57a3f2a87e99c94111e2fbf74da4f382d7a4fe1b147d03278aaa1a2731921245；约束与验证见整体history同轮。
- 本项 117.63 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R38/comparison.json，提交 6add04221dac5d235b050829。


## 2026-10-25T03:21:04.462882+08:00 — cases145_max_member1_20261025_R39

- 分支M，SHA 06fb13aefcd79b8bef105479e11a0d5e7e880056b1ac8187ea2d0cc5aad369c8；约束与验证见整体history同轮。
- 本项 108.09 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R39/comparison.json，提交 6add04f21dac5d235b058cc7。


## 2026-10-25T03:24:27.312691+08:00 — cases145_max_member1_20261025_R40

- 分支D，SHA 57a3f2a87e99c94111e2fbf74da4f382d7a4fe1b147d03278aaa1a2731921245；约束与验证见整体history同轮。
- 本项 118.85 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R40/comparison.json，提交 6add05c21dac5d235b061370。


## 2026-10-25T03:24:42.209435+08:00 — cases145_member1_20261025_completed

- 采用：D1（最高观测官方分版本），SHA 57a3f2a87e99c94111e2fbf74da4f382d7a4fe1b147d03278aaa1a2731921245；严格iters、原树/eps/Div、单launch与32B owner保持。正式kernel、冻结快照、服务端源码一致。
- 验证/成绩：A3完整逐位/边界与holdout通过；A2 Pass，本项/整体 118.85μs；官方 30.6分/r18，观察2026-10-25T03:24:27.373097+08:00，隐藏10项详情未知。
- 决定/经验：M3 R37/39为30.68/29.93未证明稳定总分优势；按排名优先恢复D1（历史最高30.80，三次中位30.52高于M3的30.305）。融合公开收益保留为候选；D15/C10/尾WR压缩淘汰。跨时段波动不作编译因果。
- 停止与证据：原始尝试40，接收38，有效37；member2未用，剩余额度不自动继续。最终SID 6add05c21dac5d235b061370；/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/REPORT.md、/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/final_selection.json。


## 2026-10-25 — m1m2_batch_member1_20261025_comparison_complete

- 方法/范围：四个已冻结版本复测；严格真实iters1..32、FP32原求和次序、原Div和eps、单launch、输入只读与32B owner均不改。用户已取消用完剩余额度及B2选批优化提交。
- A2结果：M2 107.08 us；C6 119.01 us；D1 118.95 us；M1 105.40 us；均Pass，数值来自各自精确SID，隐藏10项详情未知。
- 官方观察：M2 29.67分/r19 SID 6add70571dac5d235b3c49fd；C6 28.67分/r20 SID 6add72051dac5d235b3d8ee4；D1 29.63分/r19 SID 6add72de1dac5d235b3e363c；M1 29.71分/r18 SID 6add73b81dac5d235b3ed41b；观察时间与完整SHA见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_m1m2_batch_member1_remaining/REPORT.md；R01初始M1仅附录，无分数。
- 决定：未自动选版；生产源码暂保持M1 SHA 26ee0ad7a53014af714da5934985498d1519f86778afb2603c5774e490be4b16，等待用户选择，不把动态分数当作源码稳定属性。
- 停止/证据：原始尝试6，接受5、有效5；member1当日43/50，剩余7次不自动使用。STOP保留，B2选批草稿未执行或提交；/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_m1m2_batch_member1_remaining/comparison.json。


## 2026-10-25T11:20:16.264081+08:00 — m1m2_member1_20261025_user_selected_M1

- 选择：用户明确指示“保留M1”；正式kernel已是M1，核对哈希一致，无需覆盖源码。
- 证据：SHA 26ee0ad7a53014af714da5934985498d1519f86778afb2603c5774e490be4b16；member1提交 6add73b81dac5d235b3ed41b，A2 Pass；本项/五项耗时 105.40 µs。
- 观察：该次官方29.71分/第18，观察时间 2026-10-25T11:13:42.506903+08:00；仅作历史榜单参考，不声明当前排名；隐藏十项详情未知。
- 状态：已确认M1并保持STOP，不再提交、不续用余量；选择记录 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_m1m2_batch_member1_remaining/final_selection.json。


## 2026-10-25T12:39:46.981439+08:00 — m1_cases345_3x5_merge5_20261025_completed

- 方法：ApplyRows COUNTER、full64 BR COUNTER、native tailWR交错、单batch owner wave packing4版；原生树/eps/Div和真实iters保持。
- A3：+0.301%、+0.021%、−0.011%、−2.925%；全部未达>5%，0/5 A2请求；最后一版93.32→96.05us。
- 经验/验证：4版逐位/边界/guard与holdout通过。API减少但native repeats和依赖未减；已有UB驻留无整面板冗余Copy；40→32核在本地代理增加row chunks和column slices。
- A2：仅同源M1额外确认本项106.44us，旧M1 105.40us；同源波动不当优化结论，隐藏细节未知。
- 停止/证据：不采用B路、不融合；M1不变。/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_m1_cases345_3x5_merge5/candidate_comparison.json、REPORT.md；分路B/AFTER_V2_ANALYSIS.md。


## 2026-10-25 M1 八行BR、尾部WR与分母表示独立优化（已停止，待选择）

- B/v1八行BR替代尾部WR，B/v2独立root scratch、屏障7→5，B/v3仅改尾部Mul/Div八行发射；first64树、原eps/Div/iters与q/UB保持。
- A2已接收实测：R02 796.82/2.58/16.36/88.39/80.93 us; R06 795.64/2.65/16.20/86.60/81.00 us; R11 797.05/2.59/16.15/86.16/78.35 us；M1范围见整体历史，B/v2确认收益以逐项时间为依据。
- B/v3 A3 c4 93.02→72.58us，严格/原始MulDiv全Pass；R09 HTTP429频率拒绝，无SID、没有A2成绩，不按A3外推A2。
- raw v1/v2各41自然容量配置，v3 Mul/Div head/tail逐位及guard/input/未写全0；容量跳过项显式记录，不假装设备全覆盖。
- 本路5/5尝试，429已计入且未补交B3；候选未自动部署，正式仍M1。


## 2026-10-25 M1融合A1+B2+C1验证完成（已停止，待选择）

- 融合F1 SHA fd52c080d686134fa389a3930d6f922adf19cd4d5a5fd462ee6a65d9e5f6a798，A1+B2+C1 literal union；原iters/树/eps/Div/输出所有权不改，正式M1保持。
- 本项A2：F1 82.41/83.15 us；本轮M1 105.94 us。独立版上轮 A1:101.94/101.82 us, B2:86.60/86.16 us, C1:104.89/105.44 us；跨时段明确标注。
- 检查/经验：A3严格9222配置执行含1008holdout与边界检查通过；mask/UB/dead scratch/树静态审查无问题。F1同SHA case3/5复测变慢，case4较稳定，不能确认三项独立收益同时稳定保留。保留全部记录，不外推A2机制。
- 停止/证据：member2 3/5 POST后停止，fail不补，无自动换基线；用户选择待定。完整五项/SID/分数排名观察时间见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_m1_merge_a1b2c1_5/REPORT.md、final_comparison.json。


## 2026-10-25T14:18:07.365489+08:00 — user_selected_F1_as_baseline

- 用户明确选择F1作为新基线；正式云端kernel.asc已部署冻结F1，SHA fd52c080d686134fa389a3930d6f922adf19cd4d5a5fd462ee6a65d9e5f6a798。原M1快照继续保留。
- 本项既有A2两次Pass耗时 82.41/83.15 us；完整同次五项、SID、观察时间见整体记录；case3/5波动结论保持，隐藏细节未知。
- 生产/冻结/服务端源码哈希一致，原iters/求和次序/eps/Div与输出所有权不变。此次只部署已验证字节，不重新编译或运行NPU。
- 用户要求不再提交；新增POST=0、本轮计数3/3及STOP保持。选择及部署证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_m1_merge_a1b2c1_5/final_selection.json、post_selection_audit.json。


## 2026-10-25T14:25:12.568665+08:00 — f1_single_confirmation_once_completed

- F1同SHA追加一次member2 A2测评，正式源码未改；保持原iters/树/eps/native Div与输出所有权。
- 本项Pass耗时 83.50 us；此前同F1为 82.41/83.15 us，完整同次五项见整体记录。SID 6adda02d1dac5d235b5f7783。
- 同SHA三次实测全部保留，复测不是源码优化收益；分数排名为观察快照，隐藏细节未知。
- 本范围1/1完成并STOP，无pending，不再提交；正式基线继续F1。证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_f1_confirmation_once/REPORT.md、comparison.json、final_audit.json。


<!-- f1_entry_tail_layout_20261025_history -->
## 2026-10-25 F1 三路短行入口/尾部ApplyRows/布局（已停止，待用户选择）

- 方法：B/v1沿用B3尾部八行ApplyRows，first64及B2归约不改。B/v2 switch未减真实指令量，直接ABBA无收益且proxy5回退，不送A2。
- 本项A2实测（us，按提交顺序；均平台整体Pass/公开项Pass）：R01 F1_control_open:83.69; R02 B_v1_tail_apply:81.98; R03 A_v1_short_entry:83.42; R04 F1_control_middle:83.23; R05 A_v1_short_entry_repeat:82.29; R06 F1_control_after_A_repeat:83.24; R07 A_v2_fixed_q:82.28; R08 C_v3_row_gap_active_columns:86.40; R09 B_v1_tail_apply_repeat:80.71; R10 F1_control_close:83.32; R11 A_v2_fixed_q_repeat:83.21。
- 严格iters1..32、原树/+0/eps/native Div、输入/guard/未写输出、32B owner及边界通过；A3诊断与官方case形状映射未知，隐藏十项未知。
- 状态：生产F1未改；member2 A/B/C=5/3/3含对照，全11次已完成并STOP，fail不补、不自动融合，等待用户选择。[完整报告](/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_f1_entry_tail_layout_3x5/REPORT.md)、[源码/SID/分数排名](/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_f1_entry_tail_layout_3x5/final_comparison.json)。


<!-- user_selected_B1_20261025_history -->
## 2026-10-25T15:52:05.284092+08:00 — user_selected_B1_as_baseline

- 用户选择本轮B1为基线，云端kernel已部署冻结B/v1，SHA 7f9a5c0ac91fb990eb7ce9ffd0b5494ad42e509043e32cf62eb1136259dfb8d8；原F1快照保留。
- 本项既有A2 Pass两次为81.98/80.71 us，分别来自R02 SID6adda89e1dac5d235b66d48a和R09 SID6addb00b1dac5d235b6c763b；完整同次五项见整体历史。
- 沿用同SHA A3严格/边界/所有权检查及A2记录；保持真实iters、原树/+0/eps/native Div。不把用户选择等同于全项稳定提升，公开case形状映射及隐藏十项详情仍未知。
- 此次仅部署已验证字节和记录，新增POST/编译/NPU均0，本轮11/11及STOP保持，无pending、不再提交。[选择](/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_f1_entry_tail_layout_3x5/final_selection.json)、[审计](/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_f1_entry_tail_layout_3x5/post_selection_audit.json)。


<!-- b1_tail_exp_gate_20261025_history -->
## 2026-10-25 B1 三路优化（已停止，待用户选择）

- B/v1仅连续Exp与eps Adds，wide归约、五道barrier及Div(1,sum)再Mul保持。A3 raw1815对通过；8超UB布局明确跳过，未算设备通过。
- 本项A2实际耗时(us，顺序不删)：R01 B1_control_open:82.05; R02 A1_tail_BR:83.01; R04 C1_gate_merge:81.18; R05 B1_control_middle:80.51; R06 Bv1_contiguous_Exp_eps:81.45; R07 C2_gate_batchload:82.15; R08 A1_tail_BR_repeat:81.51; R09 Bv1_contiguous_Exp_eps_repeat:81.19; R10 B1_control_close:82.08; R11 C2_gate_batchload_repeat:83.00。
- 每个候选独立SHA与完整同次五项见整体history及REPORT；真实iters1..32、原树/+0/eps/native Div、输入/guard/未写/32B owner检查通过。A3与A2证据分开，官方case形状及隐藏十项详情未知。
- 状态：生产仍B1；本轮member2 A/B/C=3/3/4，共10次请求且全部Pass，fail不补、无pending并STOP，用户选择前不部署。完整证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_b1_tail_exp_gate_3x5/REPORT.md、final_comparison.json、final_audit.json。
- 判断：B-Exp两次81.45/81.19us落在B1的80.51–82.08us内，未确认稳定收益。A1/C2并未同时改善本项；原迭代主体保持不变。


<!-- a1_interleave_tailmul_stripe_20261025_history -->
## 2026-10-25T18:59:01.391315+08:00 A1 三路优化完成（已停止，待用户选择）

- 方法：列尾Mul打包减少尾部native repeats，完整sum/eps/Div1-Mul不变；16行独立列链调度保持每列顺序但API5→25，A3回退6.83%未交A2；两次Mul A2收益未稳定复现。
- 本项A2实测(us，顺序完整)：R01 A1_control_open:84.06 us; R02 B1_tailMul_pack:81.89 us; R03 A1_control_mid:81.49 us; R04 B1_tailMul_pack_repeat:84.03 us; R05 A1_control_after_B:84.57 us。完整同次五项/SID/分数排名观察时间见整体记录及REPORT。
- 验证：所有实测候选各35套/9222配置、input/guard/未写输出与owner尾批检查通过，原iters/树/eps/Div保持。专项raw与容量修复证据分开，prepared-only版本不称设备通过。
- 停止/决定：member2原始/接受5/5，每路最多5且对照计入、fail不补；STOP、pending空，正式A1保持，等待用户选择。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_a1_interleave_tailmul_stripe_3x5/REPORT.md、final_comparison.json、excluded_candidates.json、final_audit.json；A3与A2独立，官方shape/隐藏详情未知。


<!-- a1_compact_prezero_rootpair_20261025_history -->
## 2026-10-25T20:42:32.678705+08:00 A1 紧凑Div与正零/根平面三路完成（停止，待用户选择）

- 方法/结论：提前准备正零：B/v1 tailSum与B/v2原sum地址。A3基本持平，各6720对raw逐位通过后A2对照；case4 B/v1=84.37，B/v2=84.60/82.81，A1=83.47/83.01/84.33us，尚无稳定收益，保留两次而不取单次最小。
- 本项A2实际耗时(us，全部顺序保留)：R01 A1_control_open:83.47; R02 B_v1_prezero:84.37; R03 A1_control_middle:83.01; R04 B_v2_prezero_sum:84.60; R05 A1_control_close:84.33; R06 B_v2_prezero_sum_repeat:82.81。完整同次五项/SID/分数排名时间见整体记录及REPORT。
- 验证：7个候选各35套/9222配置A3逐位通过；原生A两版各12960配置/207360批次，B两版各48几何/6720对，C三版2960/2290/2960套均通过，容量跳过不是设备Pass；NaN全编码专项及CSV/源码/binary绑定分开保存。
- 停止/证据：member2原始/接受6/6，无fail补交；A/B/C=1/5/0且对照计入，今日41/50。STOP、pending空、无自动续交。详见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_a1_compact_prezero_rootpair_3x5/REPORT.md、final_comparison.json、final_audit.json；BAAB漂移标签单独补正，原始计时和所有中位数不变。
- 保留决定：正式仍A1、用户选择待定，不自动融合或部署；A3代理与A2官方case映射未证实，隐藏十项未知。详见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_a1_compact_prezero_rootpair_3x5/REPORT.md、final_comparison.json、excluded_candidates.json。


<!-- a1_cases12_member3_20261025_history -->
## 2026-10-25T23:08:54.797215+08:00 A1 case1/case2 两路与融合（本项完整观察）

- 方法/结论：D1两次87.15/89.17及F1两次88.09/88.58us代价复现。D2独立入口后81.12/83.73，F2为81.43/81.13us；A1三次81.73/83.32/84.29us。观测支持代价收窄，未证明ICache或某编译器机制是唯一原因。
- 本项A2实际耗时(us，全部顺序保留)：R01 A1_control_open:81.73; R02 E1_packed_input:84.67; R03 D1_br8_roots:87.15; R04 E2_compact_pitch8_entry:84.65; R05 A1_control_mid:83.32; R06 D1_br8_roots_repeat:89.17; R07 E2_compact_pitch8_entry_repeat:81.5; R08 F1_D1_E2:88.09; R09 E2_compact_pitch8_entry_third:83.74; R10 F1_D1_E2_repeat:88.58; R11 D2_isolated_entry:81.12; R12 D2_isolated_entry_repeat:83.73; R13 A1_control_late:84.29; R14 F2_D2_E2:81.43; R15 F2_D2_E2_repeat:81.13。每次完整五项与SID见REPORT，不拼跨版本最小值。
- 分层验证：D1/D2 fresh 35套/9222配置，E1/E2/F1/F2 fresh 45套/23131配置，含holdout，FP32全位、NaN payload/符号、零符号、guard/input/漏写检查通过。D2/F2各432组UB阈值回退通过。D1 raw 192数据集/73728 uint32为D1表达式专项；融合复用边界单列，不称融合raw binary运行或动态race检查。
- 证据边界：完整同次五项/SID/SHA/分数排名观察时间、慢记录与分层证据见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_a1_cases12_member3_2x5_merge5/REPORT.md、final_comparison.json、candidate_registry.json、final_audit.json。A3代理不是A2官方shape，隐藏十项未知。 case编号仅组织观察，不代表已知shape或专属路由；静态/设备/A2结论分开。
- 决定：member3原始/接受15/15，D/E/M=5/5/5（对照和复测计入），无补交/换号/跨日。STOP、pending空、全部root任务完成；两个GPT-6.1-sol Max子agent已关闭。 正式继续A1，用户选择前不替换；整体完整SHA与经验见history.md本轮条目。


<!-- cases12_F2_selected_20261025_history -->
## 2026-10-25T23:28:52.996269+08:00 F2已由用户选择并部署

- 正式F2 SHA b23f7c906666d2ce734812e6ab4b9c59faa5aca2eed17c5fd419cb32815ac149，原A1保存，完整源与部署审计见整体history本轮条目。
- 本项两次A2记录 81.43/81.13us，完整同次五项及SID保留于 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_a1_cases12_member3_2x5_merge5/REPORT.md；隐藏十项未知。
- 此次部署新增POST/编译/NPU均0，复用同SHA验证；不将此项或其他项跨版本最小值拼接。
- 用户选择及源审计：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_a1_cases12_member3_2x5_merge5/final_selection.json、post_selection_audit.json。旧轮STOP与15次预算已结束，不自动续交。


<!-- f2_targets600_23_member3_20261025_history -->
## 2026-10-26T03:42:12.027034+08:00 F2 case1/2轮次的case4完整观察

- 本轮没有case4专属新路由承诺；case编号是官方观察项，不能据耗时反推隐藏shape或实际分支命中。严格iters/FP32节点顺序/eps/Div及32B owner保持。
- 本项关键A2观察us（完整同次五项见REPORT，其他所有轮次同样保留）：F2_control_open:81.3；F2_control_mid:81.3；F2_control_late:84.56；F2_control_close:81.77；M1_D10_E23:82.94；M1_D10_E23_repeat:81.39；M3_D26_E23:84.43；M3_D26_E23_repeat:84.43。不剔除慢记录，不拼跨源码最小值，不宣称稳定全项改善。
- 源/二进制/输入及服务端快照绑定、A3严格whole/holdout与专项raw/资源检查分层保存；25次平台整体Pass，隐藏十项耗时仍未知。
- 正式F2不变，用户候选选择权保留；member3 25/30，D/E/M=9/10/6，STOP、无pending或后台运行。证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_f2_targets600_23_member3_2x10_merge10/REPORT.md、final_comparison.json、candidate_registry.json、final_audit.json。


<!-- m3_repeat_two_20261026T074934_history -->
## 2026-10-26T07:55:55.595891+08:00 M3追加两次：case4稳定性观察

- 同一冻结M3 SHA e5ad93b67d0e7f6ddf6f23a60ccacb186bee6d401d5bfd9451af100edc745943，仅复测，正式F2不变，原实际iters/求和/eps/native Div保持。
- 本项四次A2 us（按顺序、包含慢值）：84.43 / 84.43 / 82.62 / 83.57；新增两次为82.62 / 83.57。完整同次五项与SID见追加REPORT。
- 四次范围82.62–84.43us、范围/中位数2.155%；样本数4、新旧相隔数小时且无新增F2对照，仅描述观察，不宣称后续稳定或跨版本因果收益。
- 请求追加2/2完成；累计member3 27/30、融合M8/10，STOP恢复、无pending；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_f2_targets600_23_member3_2x10_merge10/m3_repeat_two_20261026T074934/REPORT.md、stability_analysis.json，累计final_audit绑定27次。


<!-- M3_selected_20261026_history -->
## 2026-10-26T08:06:10.176111+08:00 用户选择M3作为新正式基线

- 用户明确选择M3为正式基线；正式kernel.asc复制冻结原字节，SHA e5ad93b67d0e7f6ddf6f23a60ccacb186bee6d401d5bfd9451af100edc745943。父F2 SHA b23f7c906666d2ce734812e6ab4b9c59faa5aca2eed17c5fd419cb32815ac149保存在本轮selection目录。
- 复用同SHA既有A3分层验证及四次A2 Pass，快照/服务端回显逐一一致；本项记录：84.43 / 84.43 / 82.62 / 83.57 us；同次五项/SID见selection.json。保留慢值，不拼接最小值或声称全部case稳定提高。
- 此次新增POST/编译/NPU均0；原iters/求和次序/eps/native Div不变，官方七文件不变。
- 累计member3 27/30，D9/E10/M8；剩余D1/M2共3次明确冻结，STOP保持、无pending和后台任务；后续仅分析600us/2.3us目标。
- 选择、父版、全向量及部署审计：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_f2_targets600_23_member3_2x10_merge10/selection_M3_20261026/selection.json、post_selection_audit.json；当前指针 /mnt/workspace/enjoy_ur_time/the_thing_u_must_know/current_baseline.json。


<!-- m3_cumulative_coeffshare_20261026_history -->
## 2026-10-26T11:43:15.103892+08:00 数学优化轮case4观察（正式M3保持）

- 方法/结论：非本轮定向优化；仅记录完整同版本交叉观察，不把波动归因候选数学路线。
- 本项全部A3代理实际耗时us：D1_CumulativeTile64:72.66（配对M3 72.97）；D2_CumulativeFullRow:72.74（配对M3 72.72）；D3b_EpsStateReuse:72.77（配对M3 72.88）；E1_ColumnCoeff:72.87（配对M3 72.70）；E2_SoftmaxCoeff:72.81（配对M3 72.48）；E3_ColumnCoeffInitReuse:72.87（配对M3 72.70）；A3与A2分开，本轮A2 POST=0，无候选官方耗时。完整同次五项及SHA见整体history和REPORT。
- 六版在本轮有限测试集内通过1e-5组合容差/独立reference，非M3逐位等价；原iters/索引树/row0+0/eps/nativeDiv保持。旧D3未设备运行，native全域误差与动态低UB/EPS缺口单列，不从隐藏形状推断路径。
- 新D/E/M各5次未用，旧13冻结；STOP、pending空、全部任务结束、两agent关闭；未融合/部署，用户选择待定。证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_m3_cumulative_coeffshare_member3_2x5_merge5/REPORT.md、final_comparison.json、candidate_registry.json、final_audit.json。


<!-- requested_D3b_E3_once_20261026_history -->
## 2026-10-26T12:21:43.565254+08:00 D3最终版/E3指定官方各一次

- 方法/范围：用户指定最终D3b与E3各member3一次官方验证，无代码修改；原iters/索引树/eps/nativeDiv保持，正式M3不变。
- 本项A2完整观察：D3最终D3b=81.60us（SID6aded3df1dac5d235b3052f3）；E3=83.94us（SID6aded4be1dac5d235b30d5a8）；两次整体Pass、源快照/服务端一致，完整同次五项与SHA见整体history和追加REPORT，不拼接最小值。
- 单次结果不证明稳定；A3原退化记录保留，隐藏十项未知，无新M3同期对照，不据跨时段差值宣称因果收益。
- 本轮累计2/15、D/E/M=1/1/0，余4/4/5与旧13冻结；STOP、pending空，不融合/部署或额外复测。证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_m3_cumulative_coeffshare_member3_2x5_merge5/requested_D3b_E3_once_20261026/REPORT.md、final_audit.json。


<!-- m3_coltree_singleexp_20261026_history -->
## 2026-10-26T13:24:48.517187+08:00 列树/单Exp轮case4观察（正式M3保持）

- 本项全部A2观察：M3_control_D_open=82.91us SID6adeddb61dac5d235b36c598；D1_ColumnBinaryTree=89.62us SID6adedf451dac5d235b3857de；D3_ColumnTreePrefetchOnly=84.10us SID6adee2db1dac5d235b3ac48d；D3_ColumnTreePrefetchOnly_repeat=81.90us SID6adee3b81dac5d235b3b5c4a。完整同次五项与完整SHA见整体history及REPORT，单次记录不证明稳定。
- 三版列树/四版单Exp实际CANN与A3正确性/reference通过；严格iters/FP32/eps/nativeDiv、原行树保持，仅列树允许改变。D有位差，E仅在本轮执行suite逐位一致。
- A3全部同SHA配对五项及慢phase保留于REPORT/final_comparison。case1代理确认prefetch、case3/5代理generic、case4代理scaled_batch；官方隐藏形状/路径未知。单Exp四版无目标收益，不送A2；未融合。
- 正式M3及官方七文件/current_baseline不变，候选由用户选择。member3本轮用量{'D': 4, 'E': 0, 'M': 0}，承接余额{'D': 0, 'E': 4, 'M': 5}与旧13冻结；STOP、无pending、全部任务完成、两个agent关闭。证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_m3_coltree_singleexp_member3_4x4_merge5/REPORT.md、final_audit.json。


<!-- selected_D3_E2b_once_20261026_history -->
## 2026-10-26T14:13:33.635489+08:00 D3新基线与E2b一次探针case4

- 正式D3 SHA 29fd214a4268c776c7de28d748299f339903f25421f97ba1e89ff7036e1bdec4已部署并核对原字节，M3备份；原iters/FP32/eps/Div/行树保持，仅原允许列树变化。
- 现成E2b（M3父版、非融合）一次A2观察：84.37us，SID 6adeee581dac5d235b438567，整体Pass及source/server一致；完整五项见整体history/REPORT，不拼接最小值。E2b不部署，单次不证明稳定收益。
- A3负面证据保持；本次没有新增算法代码或A3实验，仅探针默认官方sample前置与一次POST。当前正式D3既有完整同SHA记录继续保留，隐藏路径未知。
- 累计D/E/M=4/1/0，剩余0/3/5及旧13冻结，STOP恢复、无pending；后续仅分析。证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_m3_coltree_singleexp_member3_4x4_merge5/selection_D3_and_E2b_probe_20261026/REPORT.md、final_audit.json。


<!-- d3_rowfold_absreuse_20261026_history -->
## 2026-10-26T15:57:13.759734+08:00 行折叠/Abs复用轮 case4

- 目标分支之外保留完整回归记录，不从时间变化推断隐藏路径。全部7份有效A3候选的同版本完整五项、配对D3和慢phase保留，2个精度失败保留原始日志；详见整体REPORT和COST_AND_DECISION.md。
- E1一次A2本项83.43us，完整646.23/2.41/15.49/83.43/64.08us，SID6adf04b91dac5d235b548b9c、SHA6b7e98276d00de53ec223a9c8fcb1243b996ef1de9fc0df5d6bb06ff17a7fe2a；Pass及source/server匹配，单次非同期对照不证明稳定收益。
- 正式列树D3 SHA29fd214a4268c776c7de28d748299f339903f25421f97ba1e89ff7036e1bdec4保持；严格实际iters/FP32/eps/行→列阶段，用户允许求和树/Div实现试验。未融合/部署，候选留待用户选择。
- 本轮D/E/M用0/1/0、余5/4/5暂存、旧21冻结；STOP、无pending、全部任务终态、agent关闭。证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_d3_rowfold_absreuse_member3_2x5_merge5/REPORT.md、final_comparison.json、final_audit.json。


<!-- d3_weighted_singlevector_20261026_history -->
## 2026-10-26T17:36:11.799812+08:00 分块加权归约/单repeat轮 case4

- 保留全部可见耗时与慢记录，不由单项波动推断隐藏路径或整体收益。本轮实际官方记录：R01 D3=82.99us；R02 E2=81.40us；R03 E2=84.16us；R04 D3=81.66us；R05 E2=83.46us；完整同次五项与SID/源SHA见整体history本轮条目及REPORT。
- E1/E2全native/reference已执行测试逐位D3一致；单repeat矩阵和mask复用保持全部iters/FP32/eps/nativeDiv/原归约。D仅原语诊断，不能把54.82/150.99/137.38us写作本case完整算子耗时；源/设备/ISA边界详见报告。
- 正式D3 SHA29fd214a4268c776c7de28d748299f339903f25421f97ba1e89ff7036e1bdec4未改；E2 SHA24146d8e78edebc792116d4ac28eb3b6c54a1c2b05914b834ba0aa63a732a6ce未部署，选择权留给用户，无融合版。
- 新D/E/M用0/5/0、余5/0/5暂存，旧35冻结；member1完成5次，STOP/pending空/14job终态/两agent关闭。证据/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_d3_weighted_singlevector_3accounts_2x5_merge5/REPORT.md、version_choices.json、final_audit.json，公共细节引用整体历史。


<!-- selected_E2_analysis_20261026_history -->
## 2026-10-26T18:15:35.229058+08:00 用户选择E2并完成只读计算过程分析

- 正式kernel.asc已由D3切换到冻结E2原字节，SHA 24146d8e78edebc792116d4ac28eb3b6c54a1c2b05914b834ba0aa63a732a6ce；D3 SHA29fd214a4268c776c7de28d748299f339903f25421f97ba1e89ff7036e1bdec4备份 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_d3_weighted_singlevector_3accounts_2x5_merge5/selection_E2_20261026/before/production_D3.asc。官方七文件、旧campaign/STOP/报告未变。
- 三次E2既有A2 Pass均已fresh GET复核，source/snapshot/server八文件一致。完整同次五项650.77/2.29/15.27/81.40/61.53、652.95/2.28/16.85/84.16/70.96、650.96/2.33/15.56/83.46/62.54us及SID见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_d3_weighted_singlevector_3accounts_2x5_merge5/selection_E2_20261026/REPORT.md；保留全部慢记录，case2非每次<2.3、case1未达600。
- 完整计算分析区分源级repeat/已有A3管线计数/A2结果；仅提出后续独立验证方案，case3/4/5不因静态方案宣称有收益。 计算公式/成本/旧失败方向与证据缺口见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_d3_weighted_singlevector_3accounts_2x5_merge5/selection_E2_20261026/analysis/REPORT.md、plan.json、API_evidence.json。
- 新增算法改动/编译/NPU/POST/子agent均0。既有native/reference结果不冒充新运行；A3仍为代理、A2官方及隐藏未知分别记录；实际iters/FP32/全部eps与阶段依赖保持。
- 余D5/E0/M5及旧35冻结，原STOP保留、pending空、两agent已关闭，无后台续交；选择和最终审计见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_d3_weighted_singlevector_3accounts_2x5_merge5/selection_E2_20261026/selection.json、final_audit.json，后续新实验/POST需新指令。


<!-- e2_softmaxinv_blockstats_exppack_20261026_history -->
## 2026-10-26T19:41:01.981949+08:00 E2计算过程优化轮 case4

- 本项完整慢记录保留，不由单点波动推定隐藏路由或归因为未改的计算路径。E2/T3b/D1b按各自完整同次五项评价，不拼接最小值。
- 本轮实际官方记录：R01 E2_control_E_open=83.09us；R02 T3b_screen=82.44us；R03 E2_control_E_postreconnect=83.51us；R04 T3b_repeat1=81.76us；R05 T3b_repeat2=81.05us；R06 D1b_nativeDiv_diagnostic=84.56us。完整五项/SID/各源SHA统一见整体history同轮条目及 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_e2_softmaxinv_blockstats_exppack_3accounts_2x5_merge5/REPORT.md。
- 已执行的设备/reference、A3和A2分别记录，原始失败/FP32位差/慢记录保留；各候选精确证明及未验证边界见COST_AND_DECISION.md、validation_totals.json、官方source绑定。
- 正式E2 SHA24146d8e78edebc792116d4ac28eb3b6c54a1c2b05914b834ba0aa63a732a6ce和官方七文件/current_baseline不变；T3b、D1b候选未部署、没有融合。用户选版前不再优化或提交。
- 新D/E/M用1/5/0，余4/0/5与旧45冻结；member1用6、另两账号0。STOP/pending空/任务终态/两agent关闭，最终审计 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_e2_softmaxinv_blockstats_exppack_3accounts_2x5_merge5/final_audit.json。


<!-- selected_D1b_analysis345_20261026_history -->
## 2026-10-26T20:45:57.524877+08:00 选择D1b并完成case3/4/5计算过程分析

- 用户选择D1b作为正式基线，复制已冻结原字节SHA 84a28f39b95d031947796266e2e0a6bac817905922e06bf5d4af0d9a7cfec9a9；SID6adf3ba21dac5d235b8123f8一次A2 Pass已fresh GET核对八文件，完整五项646.45/2.26/15.59/84.56/61.98us。E2原字节备份 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_e2_softmaxinv_blockstats_exppack_3accounts_2x5_merge5/selection_D1b_analysis345_20261026/before/kernel_E2.asc；不将单次称稳定。
- 本次仅基线部署与只读计算过程分析，新算法改动/编译/NPU/POST/子agent均0；源七官方文件、旧STOP/campaign/REPORT/comparison/choices/audit指纹保持，余D4/E0/M5与旧45冻结。
- 已有A3 ABBA/BAAB八CSV及实际binary SHA复核、60样本同角色汇总与原comparison一致；完整五项和慢记录保留，A3代理映射/官方隐藏形状仍未确认，不从A2单项漂移归因。
- case4代理H88/q3/valid2或3已共享native因子；优先三块尾根去+0/eps叶子与列eps seed。再评估scratch复用的纯Add P2/P4，真实依赖87→44/23，E264时API5→10/20，P8 stride264排除。旧stripe16与带权FMA失败保留，不原样重试；旧列树未改ScaledTokenBatch。无新候选/结果。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_e2_softmaxinv_blockstats_exppack_3accounts_2x5_merge5/selection_D1b_analysis345_20261026/REPORT.md；/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_e2_softmaxinv_blockstats_exppack_3accounts_2x5_merge5/selection_D1b_analysis345_20261026/analysis/REPORT.md、route_projection.json、existing_profile345.json、optimization_plan.json；最终审计 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_e2_softmaxinv_blockstats_exppack_3accounts_2x5_merge5/selection_D1b_analysis345_20261026/final_audit.json。


## 2026-10-26 D1b cases345 math campaign completed

- 方法：T5独立scratch平衡半折列树，奇数尾保留，查询真实UB、预留16KiB、不降低q，原矩阵与eps/iters保持；不够空间回退。
- 效果：A3两轮约15.5%～15.9%；A2 case4=72.15/72.24/70.64us。P2/P4约慢2.8%/7.3%，Z0/R1弱收益，失败/慢记录保留。
- 决定：T5纳入M1，正式D1b待选不变；C4用5次（3候选+2控制）。M1 case4五次73.84/72.30/73.17/73.30/73.04us。
- 版本：T5 SHA35ba0fde4526cf8da5bcefbd621d6b8a20da38db1e48674bdae494a1f6da80f1，M1 SHA f407ecbd467b5d8389a28a18842d4f23808daa0e2c8a30b71dc6c7488897e083；八文件GET绑定及完整向量 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_d1b_cases345_math_3accounts_3x5_merge5/REPORT.md


## 2026-10-26 用户选择M1并完成case3计算过程分析

- 用户选择融合M1并部署冻结原字节SHAf407ecbd467b5d8389a28a18842d4f23808daa0e2c8a30b71dc6c7488897e083，T5来源保留；D1b已备份。
- 本项五次既有A2=73.84/72.30/73.17/73.30/73.04us，fresh GET及同次完整五项见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_d1b_cases345_math_3accounts_3x5_merge5/selection_M1_analysisC3_20261026/selection.json；不称本次新测评。
- 本次仅基线选择与case3分析，不新改T5算法/编译/NPU/POST，旧STOP/额度冻结；后10项Hidden。
- 选择及最终审计 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_d1b_cases345_math_3accounts_3x5_merge5/selection_M1_analysisC3_20261026/REPORT.md、final_audit.json；case3下一步仅方案，收益未验证。


## 2026-10-27 保留R1b并只读分析P1非目标退化

- 保留R1b SHA db11daeffeef6973696b1d9692c34b2b043a60c0b73815ac81d998e46fb8faa2；P1不采用，余额冻结。
- 既有A2 case4退化及完整同次五项保留；仅2候选/2对照，不把全部差值判为代码因果。
- A3代理分派/机器码及ICache字段与A2分层；共同入口膨胀不是A2 ICache/spill/bank根因证明。
- 后续仅设计编译隔离和阶段特化，未改实现/编译/NPU验证/提交。
- 公共证据见HISTORY/history.md本日保留条目及 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261027_r1b_case3_padzero_maxfold_3accounts_2x5_merge5/selection_R1b_P1_regression_analysis_20261027/REPORT.md、analysis.json、audit.json。


## 2026-10-27 独立入口/编译期阶段化：用户停止，R1b保留

- 用户停止本轮并保留R1b SHA db11daeffeef6973696b1d9692c34b2b043a60c0b73815ac81d998e46fb8faa2，正式与R04计划内末轮对照一致。
- I1两次A2完整五项与同期两次R1b见整体history本日条目；原始快慢记录均保留、n=2仅描述统计。
- case4描述中位R1b75.86、I1 74.53us，不能单项改善掩盖case3/5成本。
- T1未运行A2、M1 A3负未提交，M2未创建；代理/官方及未知shape边界保持。
- 本轮I4/T0/M0、余1/5/5与旧77冻结，STOP/pending空/agents关闭。证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261027_r1b_case3_isolate_phase_3accounts_2x5_merge5/REPORT.md、final_comparison.json、final_audit.json。

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

- 本项所有同SID实测（us）：R01=71.28; R02=73.63; R03=71.03; R04=74.47; R05=73.69; R06=73.04; R07=72.59; R08=73.53; R09=72.69; R10=72.34; R11=70.92; R12=72.62; R13=72.35; R14=72.69; R15=72.55。完整五项/完整SHA/SID /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261028_m2_ub_coloring_3x5/REPORT.md；不拼最小值。
- 正式M2 SHA 0e984ba9c657f545e5eb94582b3fe411bf8e09c6036284b6ce694ddc1e6451ea保持，候选冻结待用户选版。共同方法/完整分层验证见整体HISTORY；本地代理不确认官方shape或分派。
- B4源两次case1改善，但case3/5复测出现慢记录；A2隐藏十项细节未知，不能据一个点认定全项稳定改善。
- 本轮15/15终态，新余0及旧104冻结，STOP有效/pending空/无自动续跑；源码/原始回执/设备日志/CSV/归档SHA/独立终审见本轮final_audit.json。


## 2026-10-28T09:51:23.248440+08:00 用户保留B4为基线并开展只读细节分析

- 正式源码由M2原字节切换至冻结B4 SHA e7827703d3b4945241bb231d69347cd29c212a0fd0fc9e9af7b4effde80f41b2，M2 SHA 0e984ba9c657f545e5eb94582b3fe411bf8e09c6036284b6ce694ddc1e6451ea完整备份于 /mnt/workspace/enjoy_ur_time/others/selection_audits/selection_B4_analysis_20261028T095123+0800/before/kernel_M2.asc；官方七文件/旧campaign/STOP/证据不变。
- B4两笔已接受A2 Pass完整五项606.92/2.14/14.27/72.62/61.13、608.54/2.16/16.85/72.69/70.48us保留；本次两snapshot16文件重新哈希，沿用既有fresh GET，不宣称新GET。A3原54suite/reference通过且非逐位M2，隐藏十项细节未知。
- 本轮仅选现成版及只读分析，新增算法改动/编译/NPU/POST为0；两名只读分析agent无执行/写入权。严格iters/FP32/每eps/nativeDiv保持。
- 旧104冻结、上轮15全用余0、STOP/pending空/不自动续跑；平台latest最后已知M2不同于本地正式B4，不自动追加提交。case1中位607.73us，到600需减少约7.74us（1.27%），细节方案未实现/验证。
- 选版报告和审计 /mnt/workspace/enjoy_ur_time/others/selection_audits/selection_B4_analysis_20261028T095123+0800/REPORT.md、audit.json；新的只读分析 /mnt/workspace/enjoy_ur_time/others/selection_audits/selection_B4_analysis_20261028T095123+0800/analysis/REPORT.md。本条覆盖此前候选待选状态，不修改历史原结果。


## 2026-10-28T12:00:28.347488+08:00 B4死亡根/布局/softmax FMA三路与融合完成（待用户选版）

- 本项全部同SID官方实测（us）：R01=73.39; R02=74.06; R03=72.6; R04=71.51; R05=72.27; R06=72.2; R07=72.34; R08=73.47; R09=74.18; R10=72.27; R11=72.49; R12=73.9; R13=72.18; R14=74.25; R15=71.36; R16=72.29; R17=72.24; R18=73.5; R19=72.64; R20=73.52。完整五项/SHA/SID /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261028_b4_deadroots_layout_fma_3x5_merge5/REPORT.md，慢记录保留、不拼最小值。
- 正式B4 SHA e7827703d3b4945241bb231d69347cd29c212a0fd0fc9e9af7b4effde80f41b2始终保持，三路与融合候选由用户选。共同方法与独立分层验证见整体HISTORY。
- B5单次case1=597.99us；其他候选和融合不预设收益相加，不把A3计时推成A2或推定官方shape/隐藏。
- 本轮20/20终态，新A/B/C/M各5用尽、旧104冻结；STOP有效/pending空/无自动续跑。证据与核验见本轮REPORT/final_audit。

<!-- final-results:campaign_20261028_b5_short_stats_gates_3x5_merge5 -->
## 2026-10-28T14:18:22.547085+08:00 B5三路与融合轮case4完成（待用户选版）

- 本项全部同SID官方实测（us）：R01/6ae17dcc1dac5d235b1153bd=72.84; R02/6ae183271dac5d235b14eb48=69.44; R03/6ae183eb1dac5d235b156d79=70.34; R04/6ae184ae1dac5d235b15f65e=67.69; R05/6ae185711dac5d235b168191=76.21; R06/6ae186571dac5d235b172824=74.19; R07/6ae187551dac5d235b17d4b0=68.37; R08/6ae188511dac5d235b187faf=71.06; R09/6ae189531dac5d235b19410e=74.10; R10/6ae18a171dac5d235b19d479=77.92; R11/6ae18ada1dac5d235b1a5555=68.02; R12/6ae18b9d1dac5d235b1ad40c=77.08; R13/6ae18c661dac5d235b1b6e9f=72.48; R14/6ae18d291dac5d235b1c28e6=72.08; R15/6ae18ded1dac5d235b1cfe81=68.59; R16/6ae18eb01dac5d235b1d96b1=71.08; R17/6ae18f731dac5d235b1e2520=78.30; R18/6ae190361dac5d235b1eb4bb=73.46; R19/6ae190fa1dac5d235b1f67d8=73.70; R20/6ae191bd1dac5d235b200321=72.50。完整五项/SHA/账号/SID见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261028_b5_short_stats_gates_3x5_merge5/final_comparison.json；每笔完整记录保留，不拼最小值。
- 同SHA描述统计（不代表一次实测）：B5_FastPredicateHoist n=3 median=72.50 [72.48,72.84]；A1_UpperShortMode n=1 median=76.21 [76.21,76.21]；B1_DeadStatsS0 n=1 median=67.69 [67.69,67.69]；B2_DeadStatsS8 n=1 median=69.44 [69.44,69.44]；C1_EarlyGateReady n=1 median=70.34 [70.34,70.34]；A2_UpperShortModeMixed n=1 median=74.19 [74.19,74.19]；B3_UpperDeadStatsS0 n=2 median=68.19 [68.02,68.37]；C2_GateDmaGroupedControl n=1 median=71.06 [71.06,71.06]；A3_UpperShortColumnsOnly n=1 median=74.10 [74.10,74.10]；B4_FullStatBlocksDeadS0 n=1 median=77.92 [77.92,77.92]；C3_UpperShortGateReady n=1 median=77.08 [77.08,77.08]；A4_UpperShortRowsOnly n=2 median=71.58 [71.08,72.08]；C4_UpperShortPairGateDma n=2 median=73.44 [68.59,78.30]；M1_UpperRowsPairGate n=2 median=73.58 [73.46,73.70]。n=1无复现，n=2有限重复；统计极值不可组装成一笔向量。
- 正式B5 be52118acd2c2b53f4c4c96a7011af6a7ba039a9469cc48a0b8b06cef3ab5de4保持；本轮方法、B3复测完整五向量及各case慢记录见整体HISTORY与 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_b5_short_stats_gates_3x5_merge5/REPORT.md。B3同SHA各SID均保留，由用户选择，不自动提升。
- 13源/702套真实A3 numeric/reference+strictbits及52 CSV绑定；A3代理不确认A2官方shape、分支或性能。四个原资源配置相关非零作业保留，只有同SHA新full_v2完整通过可作补证。
- 尝试/接受20/20，账号{'member1': 15, 'member2': 5}，分路余{'A': 0, 'B': 0, 'C': 0, 'M': 0}；旧104冻结，终态/STOP/pending空、无自动续跑。最终审计和用户选版入口见 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_b5_short_stats_gates_3x5_merge5/version_choices.json。
<!-- /final-results:campaign_20261028_b5_short_stats_gates_3x5_merge5 -->


<!-- final-results:campaign_20261028_b5_rowinner_blocktoken_1x5 -->
## 2026-10-28T16:04:37.800366+08:00 同行内布局轮case4完整记录

- 正式B5 be52118acd2c2b53f4c4c96a7011af6a7ba039a9469cc48a0b8b06cef3ab5de4 保持；L1/L2冻结完整SHA、源和静态证明见整体history与 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_b5_rowinner_blocktoken_1x5/version_choices.json。
- 本项A2全部实测(us)：R01/6ae1a4301dac5d235b2e1f4b=72.69; R02/6ae1a6211dac5d235b301918=74.25; R03/6ae1a6e41dac5d235b30aa54=74.02; R04/6ae1aaa11dac5d235b335fe4=73.22; R05/6ae1ab641dac5d235b33f33c=73.82。对应同SID完整五项/慢记录见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261028_b5_rowinner_blocktoken_1x5/final_comparison.json，不拼最小值，不把描述统计当一笔实测。
- 两候选各67套真实A3 numeric/reference/strictbits通过，A3计时与A2官方分别记录。本项用于整体回退观察；未据A3代理确认A2官方形状/分支，也不将相邻差异当确定因果。本轮结论与方法见 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_b5_rowinner_blocktoken_1x5/REPORT.md；B5持续正式保留，候选由用户选择。
- 5次新机会全部使用并Pass；旧104冻结，新余0，STOP/pending空、唯一子agentcompleted、无自动续跑。审计 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_b5_rowinner_blocktoken_1x5/final_audit.json；优化记录只写HISTORY，规则/模板原件保持。
<!-- /final-results:campaign_20261028_b5_rowinner_blocktoken_1x5 -->


<!-- selection-host-analysis:L1_20261028T161731+0800 -->
## 2026-10-28T16:40:44.619148+08:00 L1正式选版与Host只读研究

- 用户选定L1，正式SHA 30ac04fcc079bd6e81aecb4f1a66de20bc5cd9017aba96311833fd17bfc25380，原B5及状态备份见整体HISTORY的本次选版目录。未实施Host候选。
- 本项选定SHA官方完整记录(us)：R02/6ae1a6211dac5d235b301918=74.25; R03/6ae1a6e41dac5d235b30aa54=74.02；对应同SID五项、快慢值和原始证据见 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/selection_L1_host_analysis_20261028T161731+0800/REPORT.md 与 selection_provenance.json，不拼最小值。
- Host主线为精确整数分区描述，保持原核数/q/first-end/所有权与全部实际FP32数学；只影响初始化，A2收益未知，不把Device Scalar当CPU时间。资源查询/分派整理为次线，范围与否决条件见整体HISTORY及报告。
- 新编译/NPU/测评/平台GET/POST均0，旧104及零余额继续冻结；STOP/pending空、只读agentcompleted、无新执行授权。正式源与最新官方B5提交不混称，规则/官方模板/旧报告保持原件。
<!-- /selection-host-analysis:L1_20261028T161731+0800 -->


<!-- final-results:campaign_20261028_l1_host_partition_resource_dag_3x5 -->
## 2026-10-28T17:59:17.394635+08:00 L1 Host三路完整结果 case4

- 正式L1保持，SHA 30ac04fcc079bd6e81aecb4f1a66de20bc5cd9017aba96311833fd17bfc25380。P1/P2精确整数分区、U1/U2同调用资源快照、D1/D2分派元数据；6个冻结SHA/审查/证据见 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_l1_host_partition_resource_dag_3x5/version_choices.json。D2仅允许private residentBatch死参数2/4→1，实际消费参数与严格iters/FP32/eps/原sum/nativeDiv保留。
- 本项全部A2实测(us)：R01/6ae1b8d51dac5d235b40130c=74.26; R02/6ae1bb491dac5d235b42169a=77.95; R03/6ae1bccc1dac5d235b432f14=72.70; R04/6ae1bda01dac5d235b43e41a=72.66; R05/6ae1be8a1dac5d235b44aca5=74.38; R06/6ae1bfb11dac5d235b459aab=76.31; R07/6ae1c0d81dac5d235b4679f9=73.95; R08/6ae1c19b1dac5d235b471571=73.14; R09/6ae1c25e1dac5d235b47af44=75.96; R10/6ae1c3211dac5d235b482a88=72.74; R11/6ae1c3e41dac5d235b48bf59=74.17; R12/6ae1c4a81dac5d235b494eaf=74.90; R13/6ae1c56b1dac5d235b49e4ed=74.07; R14/6ae1c62e1dac5d235b4aac91=73.02; R15/6ae1c6f11dac5d235b4b478a=72.54。同SID五项与慢记录见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261028_l1_host_partition_resource_dag_3x5/final_comparison.json，不拼最小值。
- 6候选各67套真实A3 numeric/reference+strictbits通过，共402套、123984次配置执行（非去重）、804实际raw日志、24 CSV；CPU参考1344组/4074文件复用重核，本轮新生成0。HostCPU入队、A3 Device、A2官方分别记录，不互相替代。
- 新额度A/B/C各5次尝试/接受，15/15均Pass，全部member2；member1开场日用50达既有策略50，按授权顺序接续member2，服务端限额未知。最短POST间隔195.194859028秒，旧104冻结、新余0，无融合或额外授权。
- 正式L1与收尾官方一致，用户选择前不自动提升候选。STOP有效、pending空、所有有限作业终态、3名子agentcompleted、无自动续跑。最终审计 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_l1_host_partition_resource_dag_3x5/final_audit.json；优化记录仅HISTORY，AGENTS/README/RULES和官方7文件未改，旧campaign/STOP/审计保持。
<!-- /final-results:campaign_20261028_l1_host_partition_resource_dag_3x5 -->


<!-- final-results:campaign_20261028_l1_case5_pair_earlypack_gatecompact_3x5 -->
## 2026-10-28T20:51:56.578517+08:00 L1 case5三路完整结果 case4

- 正式L1保持，完整SHA 30ac04fcc079bd6e81aecb4f1a66de20bc5cd9017aba96311833fd17bfc25380；六个准入冻结源：A1_PairedWorkBR=a2983953706b18f0443240ec59a020e888f007a96549b2b3ed6328ba61c9ac17; B1_EarlyPackSoftmax=35cefed7f1ee9a485a8179455213d25bfb826da4a718aa903fb9ffbd7c67069d; C1r_GateCompact=3ab07529b03d4d08bddd74e4412844489d5009c49c0847515563c6ccf40e8f3d; A2_PairedContiguousDiv=46e8d86e1c708ab317407dc75bf3d8b323ee7e4f060308fdde2c3ea174c0c2ca; B2_MaxPackSharedFence=832fc4116f89397f6ce486603ffb77278f40ceb9ddea56cc611bdcee00b264a2; C2_GateVectorSeed=b3cda16eca9ecba0c74661386ce445dca52e01abfab918a66222f384c06f0fb3。版本证据 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_l1_case5_pair_earlypack_gatecompact_3x5/version_choices.json 必须保留C2 R14失败与未解决CPU限额风险，用户最终选择；C1默认编译失败源另留。
- 本项可见状态/实测(us)：R01/6ae1d9941dac5d235b592ee1 [Pass]=74.04; R02/6ae1dd531dac5d235b5c1256 [Pass]=73.88; R03/6ae1de161dac5d235b5ca77e [Pass]=72.70; R04/6ae1e02e1dac5d235b5e3a16 [Pass]=68.84; R05/6ae1e16f1dac5d235b5f2267 [Pass]=72.70; R06/6ae1e2321dac5d235b5fcb4e [Pass]=72.66; R07/6ae1e2f51dac5d235b606ef1 [Pass]=73.19; R08/6ae1e3b81dac5d235b60fada [Pass]=73.96; R09/6ae1e47b1dac5d235b618a56 [Pass]=72.59; R10/6ae1e53f1dac5d235b62452a [Pass]=73.37; R11/6ae1e6021dac5d235b62f0eb [Pass]=69.26; R12/6ae1e6c51dac5d235b6399c1 [Pass]=72.09; R13/6ae1e7881dac5d235b642f82 [Pass]=74.01; R14/6ae1e84c1dac5d235b64c118 [Time Limit Exceeded]=Skipped; R15/6ae1eab81dac5d235b66e58f [Pass]=72.23; R16/6ae1eb7b1dac5d235b678345 [Pass]=72.49; R17/6ae1ec3f1dac5d235b6821b8 [Pass]=68.64; R18/6ae1ed021dac5d235b68b329 [Pass]=74.40; R19/6ae1edc51dac5d235b694fd5 [Pass]=72.38; R20/6ae1ee881dac5d235b69f0d5 [Pass]=74.26; R21/6ae1ef4c1dac5d235b6a9610 [Pass]=72.79。raw0保留但TLE/Skipped非0us观察；同SID五项与仅good统计见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261028_l1_case5_pair_earlypack_gatecompact_3x5/final_comparison.json。
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
- 本case按原始轮次记录，不拼接跨轮最小值：L1_RowInnerCompactDen: R01=72.83, R20=74.25 us; A1_P56DeadPanel: R02=74.38, R08=74.04, R14=72.58 us; B1_WideQ1InPlaceControl: R03=74.18, R09=74.17, R15=72.59 us; C1_L1FullQPartition: R05=74.72, R10=73.88, R16=73.57 us; D1_GenericDeadMatrixPrefetch: R04=72.85, R11=74.27, R17=74.65 us; B2_WideOriginalMathBatch: R06=74.24, R12=72.77, R18=72.51 us; A2_P56EvenCompactQ8: R07=77.54, R13=77.48, R19=76.66 us。
- 分数/排名与该case其他4项共同构成每笔完整向量，详见/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_l1_hidden_families_member3_20/REPORT.md及CSV；不从单项或总分识别隐藏工作负载。
- A3严格baseline位型和独立CPU reference分层通过；A2候选补齐65条/实际1144配置，共194套；六版24族ABBA+BAAB共48phase，逐phase保存launch36端点/CAS并核SHA，端点与L1相同，不宣称每launch/全域。新q8五族geo约+29.7%、B2真实9族约+26.7%；B1/C1负例、A2 H22退化完整保留，均不当作官方A2整体收益。
- 正式L1_RowInnerCompactDen仍为30ac04fcc079bd6e81aecb4f1a66de20bc5cd9017aba96311833fd17bfc25380，未自动保留/融合任何候选；20额度用尽、pending空、有限任务已结束、新campaign STOP与状态已关闭等待用户选择。完整对照/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_l1_hidden_families_member3_20/REPORT.md；CSV /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_l1_hidden_families_member3_20/official_observations.csv。
<!-- /campaign-L1-hidden-member3-20:campaign_20261028_l1_hidden_families_member3_20 -->

<!-- selection-B2-hidden-inference:20261029T005944+0800 -->
## 2026-10-29T01:32:36.927300+08:00 保留B2为正式基线，未新增本case测试

- 用户明确选择B2_WideOriginalMathBatch，正式kernel.asc从L1切换为既有冻结B2，SHA256 be9c858f29bfcee4265ca6ac638441dd189d816eacf29e8c7b75ba5ae369cf25；原L1和两个状态原件在/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/selection_B2_hidden_inference_20261029T005944+0800/before。不是新开发候选，不改官方7文件和规则3文件。
- 三笔完整五项（本case为第4项）：R06 [602.91, 2.21, 14.38, 74.24, 60.19] us, score/rank 31.94/20; R12 [601.64, 2.15, 14.59, 72.77, 61.74] us, score/rank 31.98/21; R18 [602.44, 2.17, 14.8, 72.51, 61.65] us, score/rank 31.9/21。不拼接跨轮最小值。
- R06/R12/R18三笔既有官方Pass的服务端与snapshot全部8文件重新哈希匹配；完整同SHA向量/当时首次分数排名均保留，见/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/selection_B2_hidden_inference_20261029T005944+0800/selection_audit.json。本次无编译/NPU/平台GET/POST；平台最近已知为R20 L1对照，不伪称选版已发新提交。
- 只读分析支持用完整算法消融约束隐藏参数族：B2三次hidden均分残量28.176/28.161/28.144，高于L1两端27.931/27.995，属未配对方向线索，不识别H、点数、耗时或因果。动态/内生TBest、运行波动和非目标外溢均保留未知。
- 保留B2为新基线；旧104与已用20额度冻结，STOP保留、pending空、不恢复worker。后续仅凭新的明确授权实验/提交。综合方案/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/selection_B2_hidden_inference_20261029T005944+0800/REPORT.md，公开shape/评分可识别性/分族设计独立报告均在同目录。
<!-- /selection-B2-hidden-inference:20261029T005944+0800 -->


<a id="b2-four-routes-stopped-20261029"></a>
## 2026-10-29 B2四路线停止记录：case4

- 保留B2，SHA `be9c858f29bfcee4265ca6ac638441dd189d816eacf29e8c7b75ba5ae369cf25`；唯一进入A2的候选C01 SHA `2c2c249310bbdd36fc2c442ce9ded657413934071179a7c3edac5d3c713c5953`。A/B/D仅有本地A3检查，不冒充此case的A2验证。
- 以下只摘同SID的本case值；完整五项、所有候选、方案及A3限制在 [总history](history.md#b2-four-routes-stopped-20261029)。配对确认在完成前被用户停止，不据这些单次值宣称收益或无回退。
- R04与R10没有收尾数据，保留未知，不填0；R04长期Running不等于算子错误。E01是用户手动旧代码检查，不纳入候选对照。
- 14:42:41 +08已按用户要求停止，剩余额度冻结；此处补齐历史记录不构成新实验或重试授权。

|轮次|版本|case4耗时(us)|SID|
|---|---|---:|---|
|R01|B2|72.75|6ae2d4691dac5d235b204572|
|R02|B2|73.78|6ae2d4c31dac5d235b20a509|
|R03|B2|73.06|6ae2d51e1dac5d235b21007b|
|R05|C01|72.82|6ae2de861dac5d235b2a7114|
|R06|C01|72.87|6ae2e7541dac5d235b339f94|
|R07|C01|73.99|6ae2e9851dac5d235b370293|
|R08|C01|74.20|6ae2e9e21dac5d235b377117|
|R09|C01|74.13|6ae2ea3f1dac5d235b37d626|


<!-- case5-four-routes-ccs-max-20261030-final -->
## 2026-10-30T15:22:18.162178+08:00 case5 四路线 CCS DeepSeek Flash Max 完整结果（待用户选版）

- 父版与正式源保持 case5_compact `2a3e946715f9bb380b55b61a6e68b2113084998e5bfa17723a6a5bef8a5b9a39`，本轮四路各5次、20次A2已结束，等待用户选版。
- 四路线方法、A3范围、失败、完整五项和预算审计见总history本轮条目；本文件按同SID摘取本case，不将代理形状当官方映射。
- 本case所有真实快慢值如下，未拼接跨版本最小值：1/6ae438161dac5d235b4cccff A0_baseline_control_v2=73.5us; 2/6ae43a141dac5d235b4e9e17 A1_softmax_eps_direct_packed=68.52us; 3/6ae43a751dac5d235b4ef578 C1_compact_prefetch=72.94us; 4/6ae43bb01dac5d235b5000f1 B1_blockmajor_flat_br=75.25us; 5/6ae43c1c1dac5d235b5059ee A2_softmax_eps_mask_reuse=68.63us; 6/6ae43c7b1dac5d235b50a63a C2_lookahead_admission=70.3us; 7/6ae43d7c1dac5d235b51800d D1_q8_singlewave_partition=72.07us; 8/6ae43e6b1dac5d235b526575 A1_softmax_eps_direct_packed_repeat=68.24us; 9/6ae43ec31dac5d235b52b77b A2_softmax_eps_mask_reuse_repeat=68.01us; 10/6ae43f5d1dac5d235b5350c3 B2_blockmajor_mask_reuse=68.66us; 11/6ae43fbc1dac5d235b53aff1 C3_post_dequeue_lookahead=72.38us; 12/6ae4401c1dac5d235b540582 D2_q8_multiwave_partition=73.34us; 13/6ae441891dac5d235b559c71 B1_blockmajor_flat_br_repeat=68.51us; 14/6ae441e61dac5d235b55e98c C2_lookahead_admission_repeat=73.59us; 15/6ae442471dac5d235b56359f D1_q8_singlewave_partition_repeat=73.62us; 16/6ae4429f1dac5d235b56825c B2_blockmajor_mask_reuse_repeat=68.56us; 17/6ae442fd1dac5d235b56dbe7 C1_compact_prefetch_repeat=69.58us; 18/6ae4435c1dac5d235b572e31 D2_q8_multiwave_partition_repeat=72.05us; 19/6ae443b51dac5d235b5771b6 B2_blockmajor_mask_reuse_repeat2=68.32us; 20/6ae4440e1dac5d235b57bf42 D0_closing_baseline_control=72.26us.
- 分数是完整15项官方总分的首次成功观测，10项Hidden逐点耗时未知；A3诊断、官方样例、A2总体Pass及最终人工规则核验分层。
- 原始逐SID回执、源码SHA、完整比较见 `/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261030_case5_four_routes_deepseek_4x5/final_comparison.json`；生产不自动覆盖，本轮STOP、pending空、无自动续跑。


<!-- user-retains-case5-compact-after-four-routes-20261030 -->
## 2026-10-30T15:36:51.370142+08:00 用户选择保留 case5_compact 基线

- 用户确认保留原基线 case5_compact，活动源码SHA `2a3e946715f9bb380b55b61a6e68b2113084998e5bfa17723a6a5bef8a5b9a39`，无需源码复制。
- 本case最近已知收尾基线观察为 72.26us（SID `6ae4440e1dac5d235b57bf42`）；完整同SID五项、全部同源快慢与选版依据见总history本次条目及上轮原始比较。
- 本次没有新增正确性或性能实验；选版不将既有观测扩大为稳定性能收益，也不改写旧失败与慢记录。
- 待选标记已解除，STOP保留、pending空、各路剩余0、无自动续跑；本次编译/NPU/平台GET/POST均0。


## 2026-10-30 tree_tail_deepseek_3x7 complete

- 父版与完整SHA、逐SID五项、算法及分层验证见同轮总history；正式版本未自动替换。
- 本case全部实际观察：R01 A0_opening_baseline SID=6ae4593d1dac5d235b69ab44 72.15us score=34.84; R02 A1_dense_column_tree SID=6ae45b0f1dac5d235b6b5eeb 72.16us score=33.9; R03 C1_q8_singlewave SID=6ae45c1e1dac5d235b6c30a0 73.38us score=34.88; R04 A1_dense_column_tree_repeat SID=6ae45c761dac5d235b6c8128 72.12us score=34.64; R05 A2_layered_column_tree SID=6ae45d8f1dac5d235b6d78e3 70.27us score=33.59; R06 C2_tree_singlewave SID=6ae45de81dac5d235b6dbf60 71.51us score=34.82; R07 A2_layered_column_tree_repeat SID=6ae45fa71dac5d235b6f4061 72.63us score=33.54; R08 C1_q8_singlewave_repeat SID=6ae460001dac5d235b6f84ae 73.93us score=34.71; R09 M1_tree_singlewave_repeat SID=6ae460581dac5d235b6fc900 73.1us score=33.59; R10 B1_compact_tail2 SID=6ae460b31dac5d235b7019fd 73us score=33.63; R11 A3_fixed32_early_tail SID=6ae462721dac5d235b71a9b0 71.57us score=34.2; R12 M2_fixed32_singlewave SID=6ae462d31dac5d235b720b1d 73.36us score=34.24; R13 B1_compact_tail2_repeat SID=6ae463321dac5d235b726926 73.11us score=33.43; R14 A3_fixed32_early_tail_repeat SID=6ae465431dac5d235b7455dd 72.09us score=34.07; R15 M2_fixed32_singlewave_repeat SID=6ae4659b1dac5d235b74a28d 73.36us score=33.94; R16 C1_q8_singlewave_repeat2 SID=6ae465f31dac5d235b74eed0 73.71us score=34.26; R17 B2_safe_shared_column_gather SID=6ae468b21dac5d235b773716 70.65us score=33.9; R18 C4_latepack_softmax SID=6ae4690b1dac5d235b778648 73.14us score=34.57; R19 B2_safe_shared_column_gather_repeat SID=6ae469651dac5d235b77cd3c 68.57us score=33.97; R20 C4_latepack_softmax_repeat SID=6ae469c01dac5d235b78226f 73.12us score=34.53; R21 M4_unrolled_row_fixed32_singlewave SID=6ae46f2d1dac5d235b7d1d01 74.96us score=34.12; R22 M3_latepack_fixed32_singlewave SID=6ae46f851dac5d235b7d61fe 77.06us score=32.87; R23 M3_latepack_fixed32_singlewave_repeat SID=6ae4703c1dac5d235b7e0105 77.78us score=33.33; R24 M4_unrolled_row_fixed32_singlewave_repeat SID=6ae470941dac5d235b7e4adc 78.35us score=34; R25 C0_closing_baseline SID=6ae470ed1dac5d235b7ea777 74.66us score=34.38。
- 分数是对应SID评测后首次观测，包含隐藏项，不能由公开五项重算。保留同SHA慢记录，不因单次最好值判定稳定收益。
- STOP已设，未用额度冻结，待用户选版；原始JSON/CSV：`/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261030_case5_tree_tail_deepseek_3x7`。


## 2026-10-30 用户选定 M2 为正式基线

- 选定完整M2源码 `5b87987c98156bbba80ab73665e71a5e593a8e8f849eb6dc4e7ab2f8fec16676`；本case两次官方耗时为 73.36 / 73.36 us。
- 两次完整五项、SID、分数与选版审计见总history同节；本次没有新增设备验证或提交。
- 正式源码已切换，STOP与旧额度冻结；平台最新成绩仍对应旧基线最后回执。


## 2026-10-30 M2_bank_counter_deepseek_3x7 complete

- 父版与完整SHA、逐SID五项、算法及分层验证见同轮总history；正式版本未自动替换。
- 本case全部实际观察：R01 A0_M2_open SID=6ae482fd1dac5d235b8fc3f5 71.94us score=33.71; R02 I0_isolated_M2 SID=6ae4852e1dac5d235b91eca9 73.51us score=33.68; R03 A1_dual_phase_den SID=6ae485881dac5d235b924719 76.69us score=33.65; R04 C1_counter_windows SID=6ae485f51dac5d235b92a9ce 76.83us score=33.41; R05 B2_colored_row_roots_fixed SID=6ae486691dac5d235b931d92 79.42us score=34.14; R06 A2_dual_phase_isolated SID=6ae486cc1dac5d235b937da7 69.03us score=33.79; R07 A2_dual_phase_isolated_repeat SID=6ae487de1dac5d235b947240 70.57us score=33.62; R08 A1_dual_phase_den_repeat SID=6ae488361dac5d235b94bee6 77.02us score=33.43; R09 B2_colored_row_roots_fixed_repeat SID=6ae4888f1dac5d235b950ebb 74.07us score=34.02; R10 C1_counter_windows_repeat SID=6ae488e71dac5d235b957189 75.72us score=33.38; R11 B0_M2_mid SID=6ae4894b1dac5d235b95d358 73.12us score=33.83; R12 F1_AB_direct SID=6ae489a51dac5d235b963353 72.2us score=33.85; R13 F2_AB_isolated SID=6ae48a041dac5d235b9691a7 68.89us score=33.95; R14 C2_counter_isolated SID=6ae48a631dac5d235b96e983 75.37us score=33.92; R15 B3_colored_roots_isolated SID=6ae48ac61dac5d235b9749cc 74.94us score=32.98; R16 A3_single_phase_den SID=6ae48b211dac5d235b97a463 71.71us score=33.44; R17 F3_ABC_isolated SID=6ae48b7c1dac5d235b98013d 72.3us score=34.35; R18 A3_single_phase_den_repeat SID=6ae48c191dac5d235b98b107 73.43us score=33.89; R19 B3_colored_roots_isolated_repeat SID=6ae48c7c1dac5d235b9917f4 76.64us score=33.45; R20 F1_AB_direct_repeat SID=6ae48ce51dac5d235b9993aa 73.05us score=33.98; R21 F2_AB_isolated_repeat SID=6ae48d3f1dac5d235b9a0140 68.86us score=33.17; R22 F3_ABC_isolated_repeat SID=6ae48d9b1dac5d235b9a623d 73.46us score=33.72; R23 C3_column_counter_isolated SID=6ae48dfb1dac5d235b9ad33e 75.96us score=32.86; R24 C3_column_counter_isolated_repeat SID=6ae48e571dac5d235b9b7566 75.4us score=32.38; R25 F3_ABC_isolated_repeat2 SID=6ae48f081dac5d235b9c98b9 73.34us score=34.08; R26 C0_M2_close SID=6ae48fa21dac5d235b9d53aa 73.14us score=33.73。
- 分数是对应SID评测后首次观测，包含隐藏项，不能由公开五项重算。保留同SHA慢记录，不因单次最好值判定稳定收益。
- STOP已设，未用额度冻结，待用户选版；原始JSON/CSV：`/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261030_M2_bank_counter_deepseek_3x7`。


<!-- F1-selected-case5-next-plan-20261030 -->
## 2026-10-30T21:41:45.711488+08:00 用户选择 F1 为正式基线

- 用户明确选择 F1_AB_direct，正式源码由 M2 `5b87987c98156bbba80ab73665e71a5e593a8e8f849eb6dc4e7ab2f8fec16676` 切换为 `4e74fab52bdf7226d628b04e768c8d171d6ecd3cf62c48a5092481b0eeb74659`；复用不可变官方提交快照。
- 既有官方证据：SID 6ae489a51dac5d235b963353 case4=72.2us 首次分数=33.85；SID 6ae48ce51dac5d235b9993aa case4=73.05us 首次分数=33.98。分数为评测后首次采集，非提交瞬间值。
- 核对两次Pass、服务端全8文件绑定、候选175组设备验证与M2逐位一致；本次仅复制已验证源码，新增编译/NPU/POST均0。七个保护文件不变。
- 旧STOP与剩余额度维持冻结；平台最新记录仍是M2收尾SID，未冒称已重新提交F1。接下来只做方案分析，选版审计与下一轮JSON见 `/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_F1_case5_next_20261030`。


## 2026-10-30 F1_col_q4_io_deepseek_3x7 complete

- 父版与完整SHA、逐SID五项、算法及分层验证见同轮总history；正式版本未自动替换。
- 本case全部实际观察：R01 A0_F1_open SID=6ae4a8cb1dac5d235bb86ba9 71.67us score=34.03; R02 C1_gate_pair SID=6ae4a9451dac5d235bb8dfe1 75.6us score=33.71; R03 A1b_colscratch SID=6ae4aa711dac5d235bba11c7 67.7us score=34.54; R04 C2_early_gate_store SID=6ae4ab301dac5d235bbaefe4 72.12us score=33.91; R05 A1b_colscratch_repeat SID=6ae4ab8a1dac5d235bbb7054 71.05us score=34.35; R06 C3b_softmax_eps_pack SID=6ae4accb1dac5d235bbd5546 73.7us score=33.63; R07 A2_cachedlayout SID=6ae4ad251dac5d235bbdb675 72.09us score=33.52; R08 C4_io_pack SID=6ae4ae861dac5d235bbf3780 72.94us score=33.5; R09 M1_A1b_C2 SID=6ae4aee21dac5d235bbf9b5b 73.73us score=34.03; R10 C2_early_gate_store_repeat SID=6ae4af3f1dac5d235bbffc04 73.87us score=32.99; R11 C6_F1_drift SID=6ae4afd61dac5d235bc0aa7f 72.82us score=33.88; R12 A3_constpitch SID=6ae4b1f61dac5d235bc2ecbc 73.4us score=33.22; R13 A4_ones_phase SID=6ae4b38a1dac5d235bc4f445 77.03us score=33.07; R14 A1b_colscratch_third SID=6ae4b45e1dac5d235bc5da0e 69.87us score=33.78; R15 C7_F1_close SID=6ae4b6971dac5d235bc82cdd 72.08us score=33.51。
- 分数是对应SID评测后首次观测，包含隐藏项，不能由公开五项重算。保留同SHA慢记录，不因单次最好值判定稳定收益。
- STOP已设，未用额度冻结，待用户选版；原始JSON/CSV：`/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261030_F1_col_q4_io_deepseek_3x7`。

<!-- F1-selected-post-colq4io-analysis-complete -->
## 2026-10-31T00:20:41.482734+08:00 F1选定与case5下一轮分析（仅方案）

- 用户选择并保留F1，完整SHA `4e74fab52bdf7226d628b04e768c8d171d6ecd3cf62c48a5092481b0eeb74659`；正式源码原本已匹配，无需复制；SID `6ae4b6971dac5d235bc82cdd`，评测后首次同SID分数33.51。该case最近F1同SID耗时72.08us；本轮未新增测试。
- case5当前3次F1为53.90/53.27/53.90us，中位数53.90；进入50需再省>3.90us（>7.2356%），工程目标49us。A1b/C2单次最好值不稳定，旧q4占核前提不成立，不重扫同类相位/搬运方案。
- 新主线A：列归约前3级不动，8根按[0,4,2,6,1,5,3,7]转置后BR，6→5调用与屏障，但每列阶段多5120/6144B逻辑UB流量；地址表可复用原死matrix末段256B。次线B：packed按token做8条strided WR，9/11→8调用、4→1屏障；短WR吞吐可能反向变慢。只融合独立获益者；16根WR因320/384短repeat降级候补。
- 验证仅CPU：16个H的有序树、48组地址、135168转置搬运、212672行元素、4096组地址表phase检查通过；这是源码分支域分析，不认定官方shape。masked FP32树/符号零仍需设备逐位核验；A3计数器只作诊断。计划与API/SDK原文证据：`/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_F1_case5_after_colq4io_20261030/next_round_plan.json`。
- 本次候选实现/编译/NPU/POST/新子代理均0；8个正式文件与F1快照一致，STOP不变，旧A7/B0/C7/M1共15次及剩余B7/M6冻结，pending为空。选版已确认；下一轮未启动，当前基线仍F1。


<!-- F1-treefusion-deepseek-3x7-complete -->
## 2026-10-31T01:39:54.415354+08:00 F1_treefusion_deepseek_3x7 完成，待用户选版

- 本轮正式case4逐提交耗时（us，序号对应history.md完整SID表）：1:A0_F1_open=73.30；2:A1_col8_scalar_addr=73.85；3:C0_F1_mid=71.91；4:A3_normal64_tree=76.11；5:A1_col8_scalar_addr_repeat=74.32；6:A3_normal64_tree_repeat=77.68；7:A4_normal64_full_column=73.46；8:C4_row_normal_mask_reuse=73.10；9:M1_A4_C4=75.83；10:A4_normal64_full_column_repeat=73.53；11:C4_row_normal_mask_reuse_repeat=72.43；12:M1_A4_C4_repeat=72.64；13:M2_row_count_reuse=74.32；14:C1_F1_late_control=71.50；15:M3_A3_row_counter=74.46；16:M3_A3_row_counter_repeat=74.92；17:C2_F1_close=71.73。
- 当前正式F1收尾case4=71.73us，SID `6ae4d6091dac5d235beb9e30`；代码SHA `4e74fab52bdf7226d628b04e768c8d171d6ecd3cf62c48a5092481b0eeb74659`。
- 所有正式记录均保留，包括同源码慢测；A3代理形状不是已确认官方形状，十隐藏项不可见。
- 建议继续保留F1作为正式基线。A3是本轮最值得保留研究的case5候选，两次为52.35/51.95us，但case4升至76.11/77.68us，未证明整体稳定改善；M3复测虽到52.07us，两次分数32.86/32.84，融合没有形成更好的综合版本。本轮未实现case5低于50us。；正式源码未切换，等待用户选择。
- 证据 `/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261031_F1_treefusion_deepseek_3x7/final_comparison.json` 与 `results.csv`；配额、间隔、源码及STOP审计通过。


<!-- F1-issue-bulk-deepseek-3x7-complete -->
## 2026-10-31T03:54:53.345490+08:00 F1_issue_bulk_deepseek_3x7 完成，待用户选版

- 本轮正式case4逐提交耗时（us，序号对应history.md完整SID表）：1:C0_F1_open=73.18；2:A1_column_mul_unroll=68.34；3:A1_repeat2=68.49；4:A2_row_loops_unroll=75.14；5:B2_bulk_input_gather_lifecycle=69.63；6:C1_idle_gate_cores=75.16；7:B2_repeat2=68.97；8:M1_A1_B2=72.81；9:C0_F1_mid=72.80；10:M1_repeat2=72.58；11:B4_seed8_fanout=74.95；12:B4_repeat2=74.49；13:C3_balanced_idle_gates=76.56；14:M3_A1_B4=78.03；15:B2_repeat3=68.57；16:A1_repeat3=69.37；17:C0_F1_late=73.57；18:M1_repeat3=74.03；19:C0_F1_close=72.75。
- 当前正式F1收尾case4=72.75us，SID `6ae4f51f1dac5d235b059860`；代码SHA `4e74fab52bdf7226d628b04e768c8d171d6ecd3cf62c48a5092481b0eeb74659`。
- 所有正式记录均保留，包括同源码慢测；A3代理形状不是已确认官方形状，十隐藏项不可见。
- 建议本轮B2连续输入搬运版：三个固定轮换账号的case5均低于50us，分别47.99/47.81/46.82us，中位数47.81us；包含全部慢测的F1中位数53.545us，case5中位数改善10.71%，case4中位数改善5.51%。B2分数中位数33.01，F1为33.07；这是面向case5目标与公开case4收益的推荐，并非总分最优保证。正式基线继续F1，最终保留版本由用户决定；正式源码未切换，等待用户选择。
- 证据 `/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261031_F1_issue_bulk_deepseek_3x7/final_comparison.json` 与 `results.csv`；配额、间隔、源码及STOP审计通过。


## 2026-10-31 B2 baseline selected; under40 analysis
- 用户明确保留本轮 B2_bulk_input_gather_lifecycle；正式 kernel.asc 已切换至 SHA 870259fd7968eb6842f47ac6a9ac93d768558abf875358863030cf57c1dc4f67，其余七个正式文件哈希不变。
- 本轮B2该case正式观测为 69.63/68.97/68.57 us；保留全部观测，未拼接跨提交最小值。
- 三次B2官方Pass及337项本地A3验证沿用精确同SHA证据；本次为源码选定，未新增编译、NPU验证或POST。平台latest仍是上一轮F1收尾提交，不能写成已更新排行榜。
- 上轮19次POST账本、STOP与剩余9次冻结额度保持不变；本轮仅分析，记录 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261031_B2_under40/selection.json。


## 2026-10-31 B2 under40 bottleneck analysis complete
- 本轮仅保留B2并分析case5，未修改其他case算法、未新增正式耗时或分数。
- 新A3诊断只支持合成H34的瓶颈定位，不将其映射为本case或任何隐藏case。
- 待执行方案须报告完整五case及官方分数，尤其防止重现M1/B4对case4的退化。
- 分析与原始证据：/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261031_B2_under40/analysis.json；旧轮19次POST及未用9次预算冻结，analysis STOP保留。


## 2026-10-31 B2 output-bank-pack campaign completed
- 三个 ccs-deepseek/deepseek-flash High 子代理完成输出批量写回、列归约UB着色、softmax与pack融合；父端审查并正式POST 18 次，全部Pass。A/B/C/M用量 5/4/4/5，各上限5；仅member1/member2交替，member3为0。
- case4全部同提交官方观测（us）：C0_B2_open=70.08; B1_column_colored=72.66; A1_tokenmajor_3dma=70.71; C1b_eps_pack_fixed=70.89; C1b_repeat2=68.05; A2_dense_output=69.16; B0_B2_mid=71.07; M1_AC=75.08; A3_dense_fast_pattern=71.46; A3_repeat2=74.23; B1_repeat2=73.88; M2_A3C=69.50; A3_repeat3=74.00; M2_repeat2=73.17; M1_repeat2=75.02; B0_B2_late=70.71; M2_repeat3=72.29; C0_B2_close=68.52。保留慢测；分数为完成后首次成功读取，完整五项/分数/提交ID见results.csv。
- 所有正式新候选先通过111+162+64项本地A3逐位/输入只读检查，再经固定快照官方样例与服务端8文件SHA绑定。C1首版本地失败未POST；B路线只着色首层变体无诊断收益未晋级。A3诊断不是A2官方或隐藏shape证据。
- 父端建议：推荐 A3_dense_fast_pattern 作为继续压低case5的下一轮版本，等待用户选择，当前生产仍保留B2；A3三次case5为44.44/44.40/45.54us，中位44.44us，相对本轮B2全部四次中位49.965us降低11.06%；B2慢测保留，A3三次也均快于B2最快的47.24us。主要代价是case4中位74.00us（B2为70.395us），首次观测分数中位32.60（B2为32.745）。本轮未达到40us，不宣称总分收益。正式源码始终B2(870259fd7968eb6842f47ac6a9ac93d768558abf875358863030cf57c1dc4f67)，本轮收尾也提交精确B2，最终版本由用户选择。
- 当前STOP已设置，pending为空，未用2次冻结、不自动续跑；旧轮STOP及未用9次保持。证据 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261031_B2_output_bank_pack_deepseek_3x5/final_comparison.json、control/final_audit.json 和 results.csv。


## 2026-10-31 A3 baseline selected; under40 analysis
- 用户明确保留A3_dense_fast_pattern；正式kernel.asc已切换到SHA b35e7a8a3f52d856243c2e3ed518636d7aa83dc077de7e3a95d89cf9751fd508，其他七个正式文件哈希不变。
- case4三次官方同SHA观测为71.46/74.23/74us，中位74us；完整五项与分数沿用上轮固定回执，不拼接最小值。
- 复用精确A3的337项本地验证及三次A2 Pass证据；本次选择未新增POST，平台latest仍是B2收尾，不能说排行榜已切换A3。
- 旧轮18次POST、STOP与未用2次保持冻结，更早9次也不恢复；本轮仅分析/原样诊断，选版证据 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261031_A3_under40/selection.json。


## 2026-10-31 A3 under40 diagnosis completed
- A3正式源码SHA b35e7a8a3f52d856243c2e3ed518636d7aa83dc077de7e3a95d89cf9751fd508及其他七文件核验未变；本轮仅分析，0次新POST、0个优化候选。
- case4沿用三次同SHA官方观测；本次没有新增该case的官方耗时或分数，不将代理负载数据写成官方改善。
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
| A0_A3_open | 71.30 | 32.75 | 6ae57f5e1dac5d235b70dab3 |
| A1_column_counter_mask | 73.03 | 32.52 | 6ae580cc1dac5d235b7268ff |
| A2_column_row_counter_fusion | 69.12 | 32.73 | 6ae5836f1dac5d235b74f218 |
| A2_repeat2 | 69.09 | 32.99 | 6ae584cb1dac5d235b766a57 |
| B1_dense_flat_br_h33_42_v4 | 74.03 | 32.36 | 6ae586391dac5d235b788359 |
| A2_repeat3 | 71.11 | 32.46 | 6ae587b41dac5d235b7a1e04 |
| M1_A2_B | 70.10 | 32.87 | 6ae588a61dac5d235b7b6555 |
| B2_spaced_roots_gap6_5_v1 | 75.52 | 32.04 | 6ae58afa1dac5d235b7e5584 |
| M2_A2_gate | 73.26 | 32.81 | 6ae58bff1dac5d235b7f919d |
| M1_repeat2 | 71.15 | 32.60 | 6ae58c9a1dac5d235b804726 |
| M1_repeat3 | 73.02 | 32.74 | 6ae58d401dac5d235b80fbf7 |
| M2_repeat2 | 74.47 | 32.86 | 6ae58dd01dac5d235b81adf5 |
| C0_B2_close | 70.89 | 32.30 | 6ae58e601dac5d235b825890 |


## 2026-10-31 用户选择A2为基线，启动剩余瓶颈分析
- 用户明确选择A2_column_row_counter_fusion，正式源码从B2恢复为精确SHA 82e983326ae960963ac7365aca88f43672e051f3e3ed92ee0b431fac1c7a4b24，七个保护文件不变。
- 本case同SHA三次耗时：69.12/69.09/71.11us；完整五项与SID见总history本次选版记录。
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
| A0_A2_open | 69.38 | 33.04 | 6ae59d941dac5d235b95a05b |
| RB1_row_prefix | 70.22 | 32.93 | 6ae59f971dac5d235b982564 |
| RA1_index_reuse_mul_pingpong | 68.82 | 32.43 | 6ae5a0851dac5d235b993b59 |
| RB2_full_doubling | 71.22 | 33.19 | 6ae5a1bf1dac5d235b9aa70f |
| RB2_repeat2 | 76.90 | 32.50 | 6ae5a26b1dac5d235b9b709f |
| RB3_hybrid_flat8 | 73.01 | 31.51 | 6ae5a3191dac5d235b9c41ab |
| RC3_compact_helpers_only | 68.00 | 32.06 | 6ae5a3fe1dac5d235b9d5b4c |
| RB2_repeat3 | 72.88 | 31.65 | 6ae5a45c1dac5d235b9dd7ee |
| RC3_repeat2 | 68.87 | 32.01 | 6ae5a50a1dac5d235b9eaba3 |
| RC3_repeat3 | 68.87 | 31.98 | 6ae5a5ce1dac5d235b9f8f2b |
| M1_RC3_RB2_index_doubling | 68.53 | 31.79 | 6ae5a6fd1dac5d235ba1055a |
| C0_A2_mid | 70.58 | 31.74 | 6ae5a79e1dac5d235ba1f145 |
| M1_repeat2 | 68.11 | 31.97 | 6ae5a8731dac5d235ba33b58 |
| M1_repeat3 | 68.69 | 32.17 | 6ae5a8cd1dac5d235ba3b120 |
| C0_A2_close | 71.15 | 31.71 | 6ae5a9781dac5d235ba48acd |


## 2026-10-31 用户选择M1为基线并分析剩余瓶颈
- 生产源码由A2切换为用户选定M1 SHA 3c8f646d971e4a4750eaa68e7ddc1e5bb5f706bc060376221559d94aa4722075，七个保护文件不变。
- 本case同SHA三次耗时：68.53/68.11/68.69us；完整五项与SID见总history本次选版记录。
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
| A0_M1_open | 68.20 | 31.71 | 6ae5b6281dac5d235bb4e306 |
| RA1_remove_redundant_br | 68.54 | 32.04 | 6ae5b8eb1dac5d235bb8ad34 |
| RA1_repeat2 | 69.84 | 32.09 | 6ae5ba231dac5d235bba3893 |
| B0_M1_mid | 68.52 | 未采集 | 6ae5bbb91dac5d235bbc3b75 |
| RA1_repeat3 | 68.47 | 32.04 | 6ae5bc7d1dac5d235bbd1780 |
| RB1_first_level_input_skew_v3 | 74.64 | 31.35 | 6ae5be4d1dac5d235bbf3f40 |
| RC2_correct_block_offsets | 68.41 | 31.24 | 6ae5c01e1dac5d235bc1651e |
| RA1_repeat4_late | 70.04 | 31.63 | 6ae5c1471dac5d235bc2d446 |
| RC4_combined_first4_br | 68.20 | 30.89 | 6ae5c3001dac5d235bc4c8d8 |
| C0_M1_close | 68.87 | 31.64 | 6ae5c3971dac5d235bc57dfe |


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
|A0_RA1_open|68.90|31.61|6ae5d3561dac5d235bd7bd49|
|SB1_single_gap256|73.86|30.80|6ae5d6051dac5d235bdb045a|
|SA1v2_col_scratch_stride9|70.50|31.44|6ae5d6f01dac5d235bdc0fee|
|SA2_col_scratch_stride15|69.16|31.08|6ae5d8bc1dac5d235bde347a|
|B0_RA1_mid|68.24|31.67|6ae5d9ea1dac5d235bdfb8e0|
|SA3_stride9_compiletime|76.98|31.49|6ae5dce41dac5d235be3258b|
|SA1v2_repeat2|70.21|31.67|6ae5ddfc1dac5d235be46e77|
|C0_RA1_close|71.78|31.15|6ae5de6b1dac5d235be4fad6|


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
|A0_SA1v2_open|70.91|31.39|6ae5f22c1dac5d235bfba124|
|TA1_layer_stride_9_10_12_8|69.33|31.28|6ae5f51a1dac5d235bfed21c|
|TB1v2_column_index_pingpong|73.81|30.78|6ae5f6c11dac5d235b00668e|
|TA1r2_layer_stride_9_10_12_8|69.56|31.51|6ae5f7351dac5d235b00f685|
|C0_SA1v2_close|69.98|30.95|6ae5f7c21dac5d235b018e8b|
|C1_SA1v2_cross_account|70.96|31.23|6ae5f8851dac5d235b02552a|
|TA1r3_layer_stride_9_10_12_8|69.37|31.34|6ae5f92a1dac5d235b0308b9|
|C0_SA1v2_close|67.77|31.91|6ae5f9be1dac5d235b03ace8|


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


## 2026-11-02 F3基线case3剩余瓶颈与case4修复方案完成
- 本次明确以修复case4回退为分析目标。F3同SHA官方case4为74.44/75.58us，M3本轮首尾68.70/68.45us，中位回退6.435us（9.38%）；完整向量和选版见总history，正式版本保持F3。
- 同465配方本地编译产物核验：F3的26个旧入口与M3重定位归一化机器码全同，新静态入口插入使部分旧入口移动；少量原始字节差异均处于重定位字。工具不能解码真实汇编，未把not available占位当等价证据。
- C布局诊断仅将新入口移到全部旧入口之后：26个旧地址全部恢复，F3新入口自身4180字节完全不变；诊断SHA3c9e7aa106c4b021da1c4a440ed7e4f9b048ae48b72fb38af85c9351c8846f82。465组A3 reference/逐位/输入只读通过，副本未成为正式基线。
- 八组A3 ABBA变化约-0.964%至+0.415%，未复现官方约9.4%的回退；布局/I-cache机制仍待A2验证，未确认case4形状或实际入口。下一轮优先M3/F3/布局版近时对照及同SHA复测，目标case4回到同期M3中位+2%以内（历史约70us）。
- 本次0新POST，已有预算冻结。证据 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261102_F3_case3_case4_under10/diagnostics/entry_layout_audit.json、/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261102_F3_case3_case4_under10/diagnostics/F3_entry_last/runtime_result.json、/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261102_F3_case3_case4_under10/profiles/F3_vs_entry_last/paired_summary.json；完整方案 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261102_F3_case3_case4_under10/analysis.json。


## 2026-11-02 F3 static/mask/layout three-route campaign

- 保持正式F3；本轮C及融合版本针对case4回退，完整五项向量与SHA见总history同名轮次。
- C1仅移动447字节相同入口，M2仅移动M1两个相同入口；父端验证移除入口块后其余源码字节完全相等，所有数值/UB/同步不变。
- C1两次68.93/68.79；M1两次68.32/68.67；M2三次68.82/68.43/68.80。F3开场75.71、收尾70.47，M2与收尾F3相比仍更快，但样本有限且不能作唯一布局因果证明。A1慢值79.19、B1慢值77.22全部保留；最后相邻B1/F3为74.49/70.47，B1没有稳定修复证据。M2 case5慢值36.25是实际取舍。
- A1/B1相同SHA均保留case4慢记录；不能由少量快样本断言布局为唯一原因、I-cache瓶颈或反推case形状。A3 ELF地址/字节审计不等于官方A2二进制或PMU证据。
- 按本轮case4稳定修复优先，推荐本轮M2_M1_entry_last（SHA c816bfcc0096b61cf0f2881d455dad2a528867c139567976a8cb225eac420895），仅作推荐不采用；case3中位10.86us未改善，case5有36.25us慢值，整体无回退未证明。B1总分更高但case4波动明显，作为偏重总分的备选。 本轮停止、基线F3未变、等待用户选版；原始回执和数值证据保存在 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261102_F3_static_mask_layout_gpt61sol_3x5。


## 2026-11-02 用户选择本轮M2并重启case3多角度分析

- 用户明确选择M2_M1_entry_last；正式kernel原样切换为SHA c816bfcc0096b61cf0f2881d455dad2a528867c139567976a8cb225eac420895，父F3 SHA 9f65416d73aca967751ac9c54da40ceea029f93d8c60d4373a97ca44658e3a6d及两个状态原件保存于/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261102_M2_case3_broader_design/before。
- 复用该SHA三次官方Pass：case3=10.96/10.86/10.84us，case4=68.82/68.43/68.80us；case5慢记录36.25us继续保留，未宣称整体无回退。
- 所选冻结源与正式源哈希一致，七个官方保护文件不变，既有465项regular/native-bit/readonly及GM-guard证据绑定保留。
- 此次选版不提交；最近已知官方SID仍为F3收尾6ae81de11dac5d235b8b4cc1，选版不代表排行榜latest已切换。旧20/20额度和STOP保持。
- 本次授权为多角度分析，使用现有证据、源码、CPU推导和官方资料；新候选/编译/NPU/POST为0。分析目录/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261102_M2_case3_broader_design，新的数值改写只作条件化方案，不自动放宽原约束。


<!-- A_case4_under50_analysis_20261103 -->
## 2026-11-03 工作区A case4突破50us方案
- 基线M1_A1_C2完整SHA 50440a3b8468f91f44c6212a2ed6a6d88566c5c58a068d6dafe0f7072cd57a38；同SHA五次case4=68.51/68.35/68.02/69.46/68.73us，中位68.51；完整向量及SID见总history同名任务与analysis.json。距离50需要18.51us、27.02%降低。
- 当前宽矩阵UB驻留、native倒数因子和半折列树已存在；ResidentScaledTokenBatchKernel类与20261027 M2_B2_C1完全同哈希。优先保留同一FP32归约树，验证分层相位错开与交替scratch布局；再评估宽热循环专门化、完整容量/尾批成本联合选q，先做阶段占比和实际bank计数器剖析。
- CPU抽象布局420组/80640值逐位通过，硬件mask/复制/同步尚未验证；组地址重叠不是stall cycles。列连续Mul的合成成本模型363加80复制=443，高于原440，需靠实际冲突下降才能获益；既有B5阶段回退、counter弱收益及stripe16负结果列入止损依据。
- q先按基础空间选大、后因完整树容量不足退回串行链的边界已在CPU表中验证；其是否命中官方case4没有证明。改变串行链为树不属于同树默认路线；所有当前eps/iters/native Div和输入只读规则保持。只加速一个阶段2倍，需其原占比至少54.04%才够到50，不能承诺布局单项达标。
- 仅分析并留方案，新增kernel修改/编译/NPU/POST均0，正式A保持。证据根：/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_under50_analysis_20261103；详见next_round_plan.json、analysis/capacity_grid.json、analysis/same_tree_layout_proof.json。后续目标为同SHA五次完整Pass、case4均<50且中位48–49，完整五项与总分共同判定。


<!-- A_case4_under50_3x4_merge4_20261103 -->
## 2026-11-03 工作区A case4三路实验结果

- 父版M1_A1_C2 SHA 50440a3b8468f91f44c6212a2ed6a6d88566c5c58a068d6dafe0f7072cd57a38；本轮A/B/C/M额度使用4/2/4/0，10次官方全部Pass。完整SHA/5项耗时/分数/SID及慢记录见总history同名轮次与 /mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_under50_3x4_merge4_20261103/performance/comparison.json。
- 新基线case4控制68.04/68.65/68.71us；A2首输出half-gap 68.72/68.49/69.25us；B1热循环展开73.02us；C1尾批重排68.38/68.19/68.67us。未突破50us；C1中位比控制低0.27us但落在基线波动内，不判定稳定收益。
- A3 1108项原生位一致性/输入只读/guard全部通过；A1 bankgroup计数比值降低但整算子变慢，A2基本持平。B1局部约3%–4%代理收益未迁移至官方A2。B2两种顺序负收益，B3顺序变化与控制漂移相近，均无官方POST。C1本地特定尾批改善不能认定官方case4命中该形状。
- A2分数32.73/32.80/32.29，C1 32.49/32.58/32.19，基线32.20/32.42/31.64；保留全部观测，不能用高分样本替换低分样本或反推隐藏用例。独立稳定收益门槛未达，不做融合；静态兼容审查仅保留为审计。
- 推荐继续保留M1_A1_C2，尚未替用户选版；正式A九文件及baseline指针未变，任务关闭、无本任务pending。余6次不自动使用。所有原始本地/官方证据及最终审核：/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_under50_3x4_merge4_20261103。


<!-- A_case4_bottleneck_replan_20261103 -->
## 2026-11-03 case4无收益原因与结构路线复核

- 父版M1_A1_C2 SHA 50440a3b8468f91f44c6212a2ed6a6d88566c5c58a068d6dafe0f7072cd57a38不变。上一轮case4完整观测与同SID五项向量保留在总history及/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_under50_3x4_merge4_20261103/performance/comparison.json；基线68.04/68.65/68.71us，A2 68.72/68.49/69.25us，C1 68.38/68.19/68.67us，B1 73.02us。0.27us中位差不足以证明稳定收益，距离50仍需27.17%总体降低。
- A1/A2的PMU比值改善不是临界路径收益；C1仅改尾批而未解决q/完整容量决策。B1 A3代理正收益、官方A2负收益，当前缺少官方机器码/阶段证据，原因不冒充确定。旧masked-tail WholeReduceSum阶段已不代表当前baseline。
- 新候选一是完整容量与最慢owner成本选q；二是头部归约结果落入既有sum_后复用scratch给尾部，增加局部屏障但可能合并批次；三是每列保持原half-fold顺序的列分片，腾出UB支持更大q。全部只作CPU成本/依赖推导；columnTreeEnabled同时影响部分行尾树，不能默认切换来省时间。
- 累计列抽象模型4074组/1337280值、行复用140组/41888输出逐位一致，3个受管理CPU运行完成。实际NPU地址/mask/自动同步/UB/partial batch仍需验证；不把源级屏障减少换算成官方提速。先分派定位，命中路径后早做A2验证；无可省批次或无主阶段证据即止损，不为用完预算提交。
- 本轮仅分析、正式基线不变。完整方案和止损/14次建议预算见/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_bottleneck_replan_20261103/next_round_plan.json，未经新授权未执行。未知映射见hidden.md，不外推具体H/N/iters；不修改其他case历史或B任务。


<!-- A_case4_structural_3x4_merge4_20261103 -->
## 2026-11-03 工作区A case4结构优化三路执行完成

- 目标case4，父版M1_A1_C2 SHA 50440a3b8468f91f44c6212a2ed6a6d88566c5c58a068d6dafe0f7072cd57a38；复用旧基线68.04/68.65/68.71us，本轮0次基线执行/POST。
- 六次官方case4：A1_complete_q67.91、B1_lifetime_q5 67.96、C1_column_panels68.61、B2_static67.76、B3_pair_br8 68.99、A3_gate_softmax_schedule68.55us；全部整体Pass。未达独立重复获益条件，未突破50us，不融合。
- 十个冻结候选完成对应设备正确性、原生缓存或独立reference验证、只读/guard/确定性及源码/二进制/输入/报告绑定。四版本因本地退化或无明确整算子收益不POST；本地改善不得替代官方case4结论。
- 用量A2/B3/C1/M0，总6/16；剩余10保留不转借。建议保持现有基线，用户尚未选择新候选，所有候选保留冻结。
- 完整五项、分数、SHA、SID及慢记录见总history和 /mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_structural_3x4_merge4_20261103/analysis/final_report.json；未知映射仅见 ../hidden.md。正式九文件与baseline指针不变，任务closed。

<!-- A_case4_representation_replan_20261103 -->
### 2026-11-03 case4：保留基线后的结构性重新规划
- 用户保留M1_A1_C2，SHA 50440a3b8468f91f44c6212a2ed6a6d88566c5c58a068d6dafe0f7072cd57a38；case4复用68.04/68.65/68.71us，不重测。中位68.65到50需要降低18.65us（27.17%）；到40需要降低41.73%。
- 源码先q后树的资源决策是具体检查点；三路分别检验联合tiling、静态双布局因子状态、显式矩阵的转置分块列归约。不以mask/API数量下降替代全算子收益。
- CPU筛查和反例见总history同轮条目及/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_representation_replan_20261103/analysis/factor_cpu_summary.json，不构成设备正确性或官方收益证明。
- 方案与停止条件：/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_representation_replan_20261103/analysis/next_round_plan.json。本轮无编译/NPU/POST，正式源码和基线指针不变。


<!-- A_case4_reassoc_3x4_merge4_20261103 -->
## 2026-11-03 工作区A case4求和重排实验完成

- 父版M1_A1_C2 SHA50440a3b8468f91f44c6212a2ed6a6d88566c5c58a068d6dafe0f7072cd57a38保持；用户允许FP32求和重排但实际iters/每eps/nativeDiv不变，复用旧基线case4=68.04/68.65/68.71us，不重测。
- 10个冻结候选覆盖q/tree、双布局因子、归约BR8、转置及独立列链；9版通过对应1917/2365诊断，B3初版mask数组高低位错在本地拦截并另SHA修复。全部失败/慢记录保留，A3收益本地不当作A2收益。
- 仅3次官方完整Pass：A1 case4=68.96，A2=69.08，A3=68.50us；分数32.04/32.23/31.93，完整5项/SHA/SID/观测时间见总history同轮及/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_reassoc_3x4_merge4_20261103/performance/comparison.json。
- 未达到50us及独立稳定收益，不融合。额度A/B/C/M使用3/0/0/0，剩余13次不自动使用；B/C完整性能筛查无益，不为耗尽额度提交。
- 推荐保留M1_A1_C2，最终用户选择；正式九文件和baseline指针未变、0基线执行/POST。完整报告/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_reassoc_3x4_merge4_20261103/analysis/final_report.json，未知分派边界只记hidden.md。


<!-- A_case4_evidence_first_replan_20261103 -->
## 2026-11-03 case4覆盖缺口复盘
- 保留M1_A1_C2 SHA 50440a3b8468f91f44c6212a2ed6a6d88566c5c58a068d6dafe0f7072cd57a38；本轮只读分析与记录，无编译/NPU/POST。
- 三轮候选case4分别68.19..73.02us（3SHA/7观测）、67.76..68.99（6SHA/6观测）、68.50..69.08（3SHA/3观测）；复用基线68.04/68.65/68.71。到50需较中位减少18.65us/27.17%，小幅单条变化不认定稳定改善。
- 12候选两I1通用类源码完全相同，scaled门槛iters>1与splitOwnership的H<64条件均保持；非对齐packed列归约仍串行，旧q1列树受更早入口优先级排除。此为源码覆盖事实，不从官方无响应倒推出shape或入口。
- 旧A3 H88/N96四phase I1=26.279..27.679us、I2=20.520..20.8295；I>=2拟合残差最大0.06283us。它支持检查分派断点，不能替代官方case4阶段占比。公开榜单差距、历史完整五项、源绑定与原始路径见总history及 /mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_evidence_first_replan_20261103/analysis/summary.json。
- 提案优先补I1、非对齐packed、H128批处理覆盖；分核只在最长owner工作量下降时考虑，例H70/N96/C40虽核数24到40、最长仍4tokens，无改善证明。详细准入/精度/UB/止损/8次预算提案见 /mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_evidence_first_replan_20261103/analysis/next_round_plan.json；未知路径登记hidden.md。

## 2026-11-03 A_case4_coverage_deepseek_3x4_merge4_20261103

- 范围：工作区A，三个 ccs-deepseek/deepseek-flash high 子代理并行实现/审阅，父端统一审核、设备调度和POST；FP32、实际iters、每次eps、native Div、单launch与输入只读保持，允许重排求和。M1_A1_C2源码和基线指针不变，不重测、不POST基线，最终选版仍由用户决定。
- 固定候选与源码SHA：A1_i1_wide_scaled_safe_v1=63037401430ddbdc3f874a0c742076aed6a199ddddd7fcc1ae0df6ac1350c866; B1_wide_half_fold_v3=f9c2e50cd3d49b375efdaf0e85a980685ab33e9e23f58843255b50297bcce04f; B2_wide_gate_matrix_ownership_v1=0a7ed4e77101e9b4e03e15d8c1679a0e637ea63690a6ca5f78930e570fa53e05; C1_h128_q2col16_v3=ede6d076eb002a411d9fbad5375d09857c4c28c9d7cdfb32c45929606d341823; C2_h128_q2col16_count_v1=16f055a868bf1dd3e56d216be7c017677ef6625a1a5c6217c5da060b34df6464; C3_h128_q2_serial_v1=d64aba08397fa21fc6caf1e7b2b7e3b727f9ce34d2100ca8dd24e60d038b26be; C4_h128_q2col16_colored_v1=86631e4a1437d361b3ba6d21d0a203b264dda48af6e9758b8a31d075712fb2e0。完整快照、binary/input绑定、失败尝试和审核修正保存在 /mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_coverage_deepseek_3x4_merge4_20261103；只冻结并验证7个候选，草稿保留不提交。
- 验证：A1/B1/C1–C4各3094组、B2为3403组独立参考/readonly/guards/两次确定性全部通过，每版完成两轮候选性能采集。C1/C2/C3/C4在相同H128大样本的两次A3耗时分别为1382.2625/1380.332、1255.0345/1255.225、1378.372/1375.4825、1370.562/1375.582us，旧同输入中位552.104us；故未POST。C2与C1全部9282输出文件SHA相同，API签名/未初始化/不可达分支问题在冻结前修复。
- 正式A2完整五项同SID记录：A1_i1_wide_scaled_safe_v1 / member1 / 6ae9aab21dac5d235ba08460: [475.46, 2.17, 9.83, 67.87, 33.36] us, score 31.96; B1_wide_half_fold_v3 / member2 / 6ae9afc81dac5d235bab8772: [479.46, 2.15, 9.77, 69.37, 34.5] us, score 32.25; B2_wide_gate_matrix_ownership_v1 / member1 / 6ae9b0fb1dac5d235bae18a1: [476.07, 2.15, 9.78, 68.75, 34.22] us, score 32.36。全部Pass；分数为完成后首次成功取得的同SID榜单分数，不是保证提交瞬间分数。旧同SHA三向量及分数完整复用在 /mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_coverage_deepseek_3x4_merge4_20261103/baseline/prior_comparison.json，旧case4中位68.65us；新最小单次67.87us仅低0.78us，无>=3us实质信号。
- 决策：A1/4、B2/4、C0/4、融合0/4，实际3次按member1→member2→member1；13次未用，不机械消耗。无独立A2实质收益，未融合；推荐继续保留M1_A1_C2，未替用户选版。正式源码9文件和baseline.json哈希复核一致；平台本轮最后提交为B2，并非正式工作副本。完整对照：/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_coverage_deepseek_3x4_merge4_20261103/performance/all_versions.csv；结论：/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_coverage_deepseek_3x4_merge4_20261103/analysis/final_campaign.json。


<!-- A_case4_softmax_frontend_factor_3x3_merge3_20261103 -->
## 2026-11-03 A_case4_softmax_frontend_factor_3x3_merge3_20261103

- 范围：工作区A，三个 ccs-deepseek/deepseek-flash high 子代理并行，父端冻结/审核/POST；仅member2，195秒冷却，A/B/C各最多3次、独立获益后融合最多3次。保持FP32、实际iters、每次eps、native Div、单launch、输入只读；允许求和重排。基线M1_A1_C2不改、不重测，旧三组正式向量完整复用。
- 版本与实现：A为初始softmax逆数因子化及尾部独立入口，B为q1/q2/q4 I1与q1 I2..32精简入口，C为单A行列因子及32/128行乘积块。冻结源码：A1b_softmax_divfactor_v1=d83ff8f8d7c798516962f2a7ca31ff1a5387d3275f06b5145d7ed0596e137e33; A2_softmax_divfactor_isolated_entry_v1=f866c7cf15b7ea1b214b85fea17f51284152289b059b8c2a8ffdd2c0e7fe2b2f; A2b_softmax_divfactor_isolated_entry_v1=bd3bfcd20b9e7ea756c6d52713c419097452859e2266b60cf27770b2d44a853b; B1_wide_lean_entry_v1=e0a0c9c46aca29ae60ccbdd6eb4d0d8a15e3834f88760e588952e23fed514930; B2_repeat1=1cc5bd62b45a13b449cfd761499f50c18b4600f925cc77848f287122136385fa; B3_wide_scaled_i2_32_v1=e4c3b97c3bd43fe2d7ad3d96578619277f154d4e3280f34e7ccdfbc1c72cbbc8; C1b_single_matrix_factor_v1=bbc6b501a1aa881c0540e8759d80c005ecbf95f4d3c0483c78873af346227370; C2_single_matrix_factor_v2=546410a55f58848deaa4585169cf9e22e3879ee245cd2b755e25068fb091c185; C2b_single_matrix_factor_v2=379b234538837819660b6858ff4c7ec2579410c11423d398a228f5f00e9e0b54; C3_factor_tile128_v3=00b58e234479a20956fccd90f7827c3c5be67013bd136acab31486f3916ac60d。8个不同候选完成3094例精度/readonly/guards/确定性检查及两轮候选A3计时；A2 host/device调用、C2 Copy重载编译失败证据保留，A1/C1静态错误在POST前拦下。
- 正式同SID完整五项：A1b_softmax_divfactor_v1 / 6ae9ceb61dac5d235beec89c: [474.85, 2.13, 9.55, 73.08, 33.65] us, score 32.71; B2_wide_resident_once_v1 / 6ae9d0101dac5d235bf1b14d: [475.06, 2.23, 9.66, 67.79, 33.4] us, score 32.15; B3_wide_scaled_i2_32_v1 / 6ae9d1b51dac5d235bf5715c: [475.25, 2.16, 9.69, 68.79, 34.24] us, score 32.15; B2_repeat1 / 6ae9d51b1dac5d235bfd1088: [474.68, 2.24, 9.77, 68.39, 33.18] us, score 32.05; A2b_softmax_divfactor_isolated_entry_v1 / 6ae9d8761dac5d235b056569: [476.06, 2.21, 9.65, 68.24, 33.29] us, score 32.20。全部Pass，服务端所有源码文件绑定一致，case ID顺序一致；分数是完成后首次成功捕获的对应SID榜单分数，不保证提交瞬间分数，旧分数非同期。
- 证据与结论：B2同SHA case4为67.79/68.39us，与旧68.04..68.71us重叠；A1b为73.08us退化，A2b旧28入口不移址后为68.24us，仍无实质收益。四个旧入口raw bytes差异保留未知，不能断言重定位或布局单因素因果。C1b/C2b/C3在同H128 N896 I15本地两轮分别1241.385/1237.045、1311.564/1303.724、986.63/991.49us，对旧中位552.104us均退化，故C未POST。A3代理不用于断言官方case4形状。
- 决策与收尾：A2/3、B3/3、C0/3、融合0/3，实际5次全member2，最小POST间隔346.8016秒，未用7次已释放，任务closed。无两路独立正式收益，未融合；推荐继续保留M1_A1_C2，最终选版仍由用户决定。正式9文件和baseline.json哈希不变；本轮最后平台提交是A2b，正式工作副本仍M1_A1_C2。完整记录 /mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_softmax_frontend_factor_3x3_merge3_20261103/performance/all_versions.csv；审计 /mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_softmax_frontend_factor_3x3_merge3_20261103/analysis/final_campaign.json。

<!-- A_case4_verified_shape_replan_20261104 -->
## 2026-11-04 case4已确认shape后的性能复盘与方案（仅分析）

- 实时基线已由用户在A_case12_D1_select_submit_20261104选为D1，kernel SHA c8c234ebbdab7e0313b157ee7f82aff323cdd5b918ab051f82f2a4b7fe217ff2；本轮不回退到旧M1。D1与M1的ResidentScaledTokenBatchKernel源码区间相同，但不据此声称binary相同；正式9文件和baseline.json哈希未变。复用D1完整Pass向量：6aea0f471dac5d235b7addca=[472.75,2.20,9.72,68.75,34.01]us；6aea12ec1dac5d235b82dc60=[476.85,2.16,9.70,68.11,33.37]us；6aea18e11dac5d235b8fad53=[475.27,2.14,9.68,68.37,33.38]us；另保留6aea183d1dac5d235b8e5a9f CPU TLE，不纳入成功耗时中位。
- SHAPE.md确认case4 B3/S32/H88/I20/N96。39次行列归一化、约2899万元素缩放；旧匹配H88/N96 A3迭代扫描拟合T=16.2974+2.19259*I us，只支持迭代成本假设，不是A2阶段占比。按已有40 AIV/179968B可用UB模型，q3完整列树145984B可容纳；旧N256代理q4树194560B不容纳，不能混用路径结论；官方eps与实时资源准入仍未直接确认。
- 覆盖审计：上一轮B2只改I1、B3只改q1、C单A因子只准入H128/q1；更早双布局因子确实准入H88，但token++逐个执行。因此不能称因子化从未覆盖H88，也不能称已否定q3批处理单A方案。实时只读aclrtGetSocName返回Ascend910_9362（A3），正式评测A2；兼容编译目标不能当作A2实机计时。
- 下一轮主攻A=q3单A+有界加权归约+延迟物化，严格保留u/(u*Av+eps)、v/(v*A^Tu+eps)、实际iters/nativeDiv；不能把O(H^2)算术伪称降成O(H)。B=真正命中q2/q3的精简入口与常量tiling，迭代循环不全展开；C=按64/gcd(qH,64)复制因子的8行/4行列缩放面板，q3理论440 repeats变403（含40复制），额外标量发令可能抵消，不能据此承诺50us。当前68.37us中位到50需26.87%，单纯理想负载均衡线性上限20%仍不足。
- 详细证据、风险、覆盖和止损条件：/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_verified_shape_replan_20261104/analysis/next_round_plan.json；本轮0编译、0张量/NPU计算、0POST、0基线重测，仅源码/历史/设备身份只读查询与CPU静态计数。后续提交仍需新一轮执行授权；无候选收益或他人算法的确定性承诺。


<!-- A_case4_q3_factor_entry_panel_4x4_20261104 -->
## 2026-11-04 A_case4_q3_factor_entry_panel_4x4_20261104

- 范围：工作区A，三个 ccs-deepseek/deepseek-flash high 子代理实现，父代理审核/冻结/提交；实时正式基线D1（由 A_case12_D1_select_submit_20261104 用户选定），SHA c8c234ebbdab7e0313b157ee7f82aff323cdd5b918ab051f82f2a4b7fe217ff2。本轮不回退旧M1、不重测基线；FP32、实际iters、每次eps、native Div、单launch、输入只读和确定性保持，允许求和重排。
- 实现与验证：8个不同SHA候选各3261组完整本地验证通过、每版两轮A3性能采集。A1四FMA链、A2加权BR8与44行配对树、A3收缩Div设置/屏障/临时复制；B1命中q2/q3精简入口、B2按q拆分；C1复制面板、C2跨行尾块、C3固定q3尾块展开。A/C均未POST。A1内部alias只算一次；Copy步长、因子越界、软max行步长、临时区、API实参问题在POST前修正，失败草稿与锁竞争/脚本路径失败记录保留。完整SHA及快照 /mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_q3_factor_entry_panel_4x4_20261104/analysis/final_campaign.json。
- 本轮case4正式结果：[66, 65.88, 66.41]us（B1三次）与67.10us（B2）；case5风险、完整同SID五项、分数、源码SHA与未提交慢版本见总history同任务块及 /mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_q3_factor_entry_panel_4x4_20261104/analysis/final_campaign.json。
- case4结论：仅B1有重复小幅收益，未突破50us；A因子化三版/C尾块三版均未建立独立收益，不做融合，不自动选版。


<!-- A_case4_B1_pipeline_replan_20261104 -->
## 2026-11-04 case4：保留B1后的归约流水方案
- 用户选定B1，SHA 9b417483dde77c15b131adde937073f274a8a7ada9595dc423f6cb2da7628791；正式A与完整快照匹配。复用官方case4 66.00/65.88/66.41us，无新增计时；完整五项与case5风险见总history同任务及analysis/next_round_plan.json。
- 关键计数：H88/q3行缩放363repeat已经满利用；39归一化共352源级PIPE_V屏障和237计数API封装。A3迭代斜率约2.177us不能当A2阶段时间；bankgroup0.219为21.9%计数比率，旧冲突更低候选仍慢，不能断言唯一瓶颈。两轮旧Counter的39份宽类同SHA且无区域复用，实际覆盖范围已审计。
- 两条主线：先列Counter共域，再行末Add/eps/Div共域；独立eps分支调度把行/列8/10层降7/9层，共少39屏障。440组符号行列检查证明每输入/eps恰一次，不证明FP32设备误差；必须保护初始softmax的共享ReduceRows不注入denominator eps。完整融合的mask动作模型332而非A单独256，优先测A+仅列eps的选择性融合。
- 本轮仅选版与分析：1次管理CPU证明、0编译/NPU/POST/基线复测。后续先完整候选与逐核/pipe证据，再决定UB相位布局；不复扫尾块/全双矩阵/非法去RAW同步。详细审查、CPU证明、旧记录与停止标准 /mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_B1_pipeline_replan_20261104/analysis/next_round_plan.json。


<!-- A_case4_B1_counter_eps_4x4_20261104_FINAL -->
## 2026-11-04 A case4：本轮执行结果

- 任务A_case4_B1_counter_eps_4x4_20261104，父版B1 SHA 9b417483dde77c15b131adde937073f274a8a7ada9595dc423f6cb2da7628791。历史case4 66.00/65.88/66.41us复用；本轮0基线执行、0正式源码/指针改动。
- A列/行Counter官方67.71/66.73us；合并A3本地59.639/59.6785us慢于旧B1 58.519/58.399，未POST。B列/行/合并eps官方66.79/67.59/66.93us；352->313源级屏障没有带来官方收益。
- 计数器启用C：H88/q3第一层配对40+4，C1 SHA 5d14b038e6f0392f238a9de5448fc81cd31d7c5bf19a36a105d57a003b58d55b；本地bankgroup0.204、vec36.275us与完整case4 57.279/56.979us，官方同SHA65.67/65.64/66.86us；慢第三次保留，中位小幅改善不认定稳定收益。C2尾先写CPU模型错误经审核发现，真实尾源80E/84E，纠正RW192->226，未送测；不把集合交集当cycle。
- 7版各3261组验证通过，8次member2官方Pass；A2/4、B3/4、C3/4、M0/4，195秒要求已满足（最短235.207秒）。无两路独立收益，不做融合，不追加基线恢复POST；推荐保留B1，由用户决定。
- 完整五项/分数/SID与SHA见总history同任务块及[final_campaign.json](/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_B1_counter_eps_4x4_20261104/analysis/final_campaign.json)、[official_comparison.csv](/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_B1_counter_eps_4x4_20261104/performance/official_comparison.csv)；A3本地证据与A2官方分开，当前未到50us，标量/屏障方向被本轮结果削弱，后续若继续需比首层配对更大幅降低向量归约/UB访问代价的机制证据。


<!-- A_help234_analysis_20261104 -->
## 2026-11-04 help_234文档审查与下一轮方案（仅分析）

- 父版B1_q3_compact_entry SHA 9b417483dde77c15b131adde937073f274a8a7ada9595dc423f6cb2da7628791；本轮只读源码/SDK/官方正文及2次受管理CPU检查，0候选源码修改、0编译、0NPU、0POST，A九文件和正式基线未变。
- 旧B2_dual_factor_br8_q1确有A/AT和FP32硬转置，但WeightedRows先物化乘积后归约、更新scale/(scale*dot+eps)，逐token完整排空；旧H88/N96/I15 A3两次124.9575/124.8375us，不能当I20官方负例。近期q3单A候选也未实现分母状态递推。
- 主线F0/F1采用完整eps分母递推及64lane加权行累加器：先64列Mul，再24列MulAddDst折入，再归约；两方向C/CT共用。目标减少乘积/尾部roots往返与反馈依赖，仍是每半步O(H²)，不宣称O(H)。C=E+eps*S、r=S保留softmax语义。
- F2在独立收益后比较16x136分段转置、分母角色轮换与死区预取。容量草案153600B须核运行时可用UB；q3双96x128矩阵仅常量区即294912B不可套入当前预算。N96/40核例16owner3token、24owner2token，串行新叶必须胜过当前q3批处理；核数从availableCoreNum取。
- 12组精确代数、H88子集160组及H81..96边界/FMA代理960组CPU通过；H128两组严格相对误差失败保留，不能全域扩展。先争取<=60us再<50；45.81/44.96缺源码不承诺。完整准入/验证/失败对照 /mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_help234_analysis_20261104/analysis/next_round_plan.json。


## 2026-11-04 工作区A help234 执行轮：A_help234_exec_4_4_6_merge4_20261104

- 父版B1 SHA `9b417483dde77c15b131adde937073f274a8a7ada9595dc423f6cb2da7628791`；实施7个隔离候选：F0双矩阵分母状态、folded乘加、BR8两级归约、静态H88/H96、scaled-E初始化、96x128矩形布局、factorPitch144相位调整；完整运行时iters/eps/nativeDiv与资源回退均保留。
- C1验证3261组，其余C2-C7各4205组通过参考精度/只读/GM守卫/确定性。A3目标耗时中位约[160.8815,101.993,70.81375,69.88875,67.58375,74.89875,76.3135]us，B1历史58.459us；没有本地收益，地址相位推断不当作性能证明。
- 最优本地C5 SHA `176a2e741c6ead8b072c92a8c1ee3a982a17c57278d9f676e34a146b2bb94858` 首笔SID `6aeaff8f1dac5d235b3ac0c6` 为TLE：case1 returncode=-9/cpu_timeout、case2-5跳过，未取得case4耗时；原SID续查0新增POST，失败照计。
- 同SHA C5_R2 SID `6aeb02901dac5d235b40f8a4` 全部Pass，完整[475.92,2.24,9.66,81.58,33.47]us、同SIDscore31.18；case4比B1历史66.00us慢23.61%。首笔超时未复现，根因未知，不宣称平台故障已证实。
- case4用2/6后停止，C6/C7不提交，保留B1分支；没有第二独立收益，融合0/4。详细全部SHA和原始证据 `/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_help234_exec_4_4_6_merge4_20261104/C/final_evidence.json`、`/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_help234_exec_4_4_6_merge4_20261104/analysis/final_report.json`。


<!-- A_case4_S3_peer4433_analysis_20261104 -->
## 2026-11-04 S3基线下case4对标44.33us：q3紧凑分母递推方案（仅分析）

- 当前S3 case4两次65.57/66.05us、均65.81；到用户提供同学44.33需降低21.48us/32.64%。help_234主体为旧57.31实现及45.81/44.96后续标签，没有44.33源码；不能把文档PMU比例或A3诊断当A2分阶段耗时。当前ResidentScaledTokenBatchKernel类与B1同字节：H88批处理仍是每核2/3token、39半步及约352个源码V屏障。
- 审核旧C5完整eps分母版：已具备64+24折叠、三分母句柄轮换、scaled-E，正式81.58us；q1每owner串行2/3矩阵，缺下一token预取与延后输出等待。旧q3 A3_trim保留批处理但用u/(u*dot+eps)，行乘积仍为88列和48+40行两块；A3测62.6285/62.339us，旧B1 58.519/58.399us。四FMA链160.9us、pitch128/144及减少屏障的失败一并保留，不重复包装为新方法。
- 新主线D1：单份C[row,token,88]、r/c完整eps分母递推、全q3的64列head+24尾折叠乘积，BR8 roots原位放每64lane行的前8lane，再跨8行归约；列向复用44行加权半折树，保持批处理、不转置。显式UB预算178720B（矩阵92928+scratch67584+gates2112+7state7392+broadcast8448+pad256），对历史179968仅余1248B，必须重新检查真实资源准入；不能将横向BR8直接替换纵向列树。
- 后续建议D0先隔离q3 scaled-E/分母变化，D1再折叠全批次乘积；D2独立验证whole-token搬入/repack及输出等待寿命；D3仅备用q2紧凑C/CT，175552B且3token owner要q2+q1，必须比较完整owner。每次实际eps/iters/nativeDiv/FP32保留；先过原参考、守卫及确定性，再看A3机制与A2正式收益，阶段目标<60再<50，不承诺44.33。未来若授权执行建议每版最多2次、四槽最多8次、member1/member2交替及历史基线复用；本轮未新增执行额度。
- 本轮仅1次受管理CPU检查：q1/q2/q3布局地址、BR8未读源覆盖及9组精确有理数递推均通过；未编译候选、未跑NPU、未POST。DeepSeek Flash high完成旧C1-C7取证并已关闭，父端审核修正其“列树直接BR8”和peer2/3owner等于q3resident的不充分推论。计划与所有来源 `/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_S3_peer4433_analysis_20261104/analysis/next_round_plan.json`，地址证据同目录static_layout.json；S3正式源码保留。


<!-- A_case4_S3_denfold_pipeline_exec12_20261104 -->
## 2026-11-05 S3下case4四候选执行结果（工作区A）

- 父版S3 SHA `3aa61d27815f908890c49b0e1b8d25e877442ab05e3950f7dca88ce26fda4696`；D0验证q3 scaled-E/完整eps分母状态，D1增加全batch64lane乘积折叠及原位BR8、三句柄轮换，D2独立优化whole-token搬入/UB重排与输出等待寿命，D3验证q2紧凑C/CT及同launch q1尾部。全部候选SHA、完整五项耗时与SID见总history同任务块和[报告](/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_S3_denfold_pipeline_exec12_20261104/analysis/final_report.json)。各4297组诊断通过，均保持运行时iters/eps、FP32、nativeDiv及输入只读。
- D1行乘积head写完再tail MulAddDst，第一BR8 dstRepStride8原位roots，第二mask64/srcBlkStride8/srcRepStride64；审查发现并在冻结前修正缺V依赖与mask8错误。D3原子代理稿的转置/折叠模型不成立，父端改为FP32 16x8->8x16分块、96stride阶段缓冲、定义零行及88x88压紧，修正Brcb repeat11与尾乘积位置后才冻结并完整设备验证；旧稿与纠错清单保留，不能引用旧静态模型为正确性证据。
- A3 case4形状两阶段中位D0 61.799/61.899、D1 58.759/58.6585、D2 55.099/55.059、D3 63.7885/63.839us；旧B1同协议58.519/58.399us。D0/D3本地退步停止，D1官方A2 72.96/72.74us（均72.85，慢10.697%），说明本地近中性不能推出A2收益；D2官方62.96/62.95us（均62.955，快4.338%）。本轮未达到60或44.33us。
- D2只改搬运/缓冲寿命，算术helpers不变，全部本地12891输出文件与S3逐位相等。q3 UB162880B，两个31680B raw槽可与后续tree/temp复用；token2覆盖槽0前保留V->MTE2，gate缓冲保留至最终MTE3->V排空。D1 UB178720B，完整分母并未消除每半步O(H^2)加权点积；A3描述性迭代斜率D1约2.1434、D2约2.1762、D3约2.4980us/iter，不能当A2逐阶段耗时；下一大步需要新的减少迭代归约/UB访问证据，不重复包装已失败双矩阵路线。
- D1/D2各2次有效机会全部Pass，另2次评测机不可用按用户规则豁免并补额；D0/D3零正式机会，融合条件不满足。物理6/有效4，余8释放并关闭任务。D2 case4改善但观测总分及其他公开case未证明整版收益，推荐保留S3待用户决定；正式A未切版，所有候选与原始证据保留。


<!-- A_case4_S3_help234_rethink_analysis_20261105 -->
## 2026-11-05 help234重审：因子算法与实际执行数据流分开验证

- 当前正式基线继续S3，完整SHA及选版收据见总history同任务块。help234详述57.31us旧Staged96FusedFactor；45.81/44.96仅有whole_io/eps_ready/feedback_drain/compact_owners标签，44.33为用户额外提供，缺peer源码，不能声称复现最新叶。文档40.6/43.3与75.9%、128B分母向量、32行4096floats存在摘要口径疑点，不能机械照搬容量/预取长度。
- S3每半步已经Div倒数+Mul，因子化不能再重复记这份收益。D1 row product67584B/column product46464B仍是O(H²)临时流；D1第一BR8 dstRepStride8原位roots、第二srcBlkStride8使8个32B块集中2个group。CANN9官方220x文档给出该步长读冲突；可改用该阶段闲置broadcastBuf8448B写连续roots，第二srcBlkStride1/srcRepStride8，不增UB且归约树不变。先作本地因果反例诊断，不预分正式提交机会；静态冲突不是整段性能归因。
- C5源码6946-6968把最终comb写at_(CT)，并立即MTE3_V等待，因而未实现文档的CT死亡区预取/矩阵角色交换；C7仅把factor间距128改144floats，不等同实际group/desired相位选择。拟F0把两个96x128常量矩阵安排在相隔65536B的区间、work放第三bank层，matrix/weight/product目标group0/8/4；连续roots在其他空隙，工作区复用whole-input/raw、乘积和16x136转置stage。168832B只是草案，真实物理基址、UB占用及生成指令需核验。
- 拟F1缓存epsR/epsC；新分母完成后nativeDiv与epsilon Muls写独立目的，下一dot+预备eps用Add。所有真实依赖屏障保留，禁止靠删fence制造假快；FP32舍入会变，须全量精度。拟F2输出原位写C，下一raw预取/重排进CT，上一comb MTE3与下一softmax并行，到下一transpose首次覆盖旧C前才drain，最终token全部排空；双gate槽、token<end守卫和实际owner范围不可省略。F1/F2均相对F0独立验证后才融合。
- 下一轮先验证热循环和完整2/3-token owner，再给通过候选4297组全验证及官方每版2机会；优先证明迭代斜率下降，不能再只看API数或整体A3时间。目标先官方<60再<50，44.33不是承诺。本次只有CPU数学/地址证明，无新kernel/编译/NPU/POST；计划、736组地址检查和18组代数证明见[任务报告](/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_S3_help234_rethink_analysis_20261105/analysis/next_round_plan.json)、[static_proofs.json](/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_S3_help234_rethink_analysis_20261105/analysis/static_proofs.json)、[planned_bank_layout.json](/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_S3_help234_rethink_analysis_20261105/analysis/planned_bank_layout.json)。


<!-- A_case4_S3_peerflow_member3_exec8_20261105_CLOSED_PENDING_SELECTION -->
## 2026-11-05 A：按help234重做case4，推荐F2c待选择

- DR诊断仅改变D1第一层BR8 roots布局，558例与D1逐位一致，本机case4约57.94us；该局部变化没有成为正式候选。F0以q1、96x128 C/CT、物理地址相位选择、连续roots、16x136转置暂存与完整三分母递推实现新叶。初稿审查纠正C=E+eps*S/r0=S及转置步长；首个本地F0因第二BR8目标步长越界失败，修正后才通过4297例并正式提交。
- F0b正式75.46us；F0c补上文档的真实tail24折叠+两级BR8 max，替代WholeReduceMax，正式73.53us；F0两机会耗尽且均劣于S3。A3迭代斜率从S3约2.177降至F0c约1.668us/iter，但固定项较大，A2结果否定了仅凭本机斜率选版。
- F1/F1b先本地筛选，F1c为early-epsilon+固定128-lane Div/Muls/Add，两次正式[73.93, 73.71]us。多发向量命令并未显示相对F0c的稳定独立收益，不能把提前Muls等同于实际流水并行；因此不做M1融合、不花融合2机会。
- F2c在最后CT dot后将work用于next raw预取，当前输出写C、下一C占用旧CT、双gate slot、下一softmax后且transpose首次覆盖旧C前才Wait MTE3_V，尾token完整drain。两次正式[61.42, 60.78]us、均值61.10us，A3约50.959us；4297例与F0c逐位一致，收益支持这组IO生命周期改动。推荐完整SHA `b696db680ea9497fdd7e7a55fcf481ca8c3bb3522313dfab41c556b5c8f89895`，尚未替换S3；目标44.33us未达到，总分优势仍受跨时参考/采样波动限制。
- F0b/F0c/F1c/F2c完整SHA、五case耗时、分数与SID以[official_comparison.csv](/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_S3_peerflow_member3_exec8_20261105/performance/official_comparison.csv)和[final_report.json](/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_S3_peerflow_member3_exec8_20261105/analysis/final_report.json)为准。F0/F1/F2各2有效、member3固定、全部有效Pass；M1=0；选版由用户决定。非H88正式源码及输出语义未改，未推断隐藏单项性能。


<!-- A_case4_F2c_break60_analysis_20261105_SELECTED_AND_ANALYZED -->
## 2026-11-05 F2c正式基线与突破60us的四个独立候选

- 用户选定F2c，正式A SHA `b696db680ea9497fdd7e7a55fcf481ca8c3bb3522313dfab41c556b5c8f89895`；选版与完整五case/SID见总history本任务块及[selection.json](/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_S3_peerflow_member3_exec8_20261105/selection_F2c_20261105/selection.json)。case4两次61.42/60.78us，均值61.10；突破60需从均值降低超过1.10us，尚非性能极限证明。
- 明确源码开销：最终invR已在最后CT dot前算好，行分母未再改变；初始c0=1可用Adds(eps)替代reset+Axpy。当前转置6段x128列、只回写96行，真实计算仅88；拟16->11 repeats、tail64->24、回写96->88，保留pitch128、stage136及dummy初始化，转置载荷少31.25%不等于整核少31.25%。
- 主循环仍39个串行weighted-dot；I20源码41次Div+39次Axpy。SDK dav_c220 count实现确认COUNT/NORMAL切换；G2只改Div固定NORMAL128lane且保留分母padding，不夹带F1提前Muls。既有A3对象无法可靠反汇编，实际CTRL指令数及VA提升仍未知，不伪造周期分解。
- G4拟在最后CT MulAddDst读取完成后V_MTE2直接加载next矩阵到旧CT、两gate到inactive槽；与work归约/eps/收尾并行，省去raw->matrix/gates共4条Adds与约63360B逻辑UB读写/transition。代价是1条连续DMA变2条strided描述符；必须实测净收益，保留MTE2_V、输出别名延后drain、最后排空及owner-end守卫。compact-owners仅条件候补，公式B=ceil(N/ceil(N/min(N,C)))，不硬编码32/40核，旧M1减核负例不可忽略。
- 静态证明、证据限制、四版独立筛选/验证和条件融合见[next_round_plan.json](/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_F2c_break60_analysis_20261105/analysis/next_round_plan.json)。本轮无新候选/编译/NPU/POST，不把A3约50.959us当A2<60证据；G1/G2/G3/G4都尚未实测。保留F2c，分析任务收口，执行另待用户开始。


<!-- A_case4_F2c_break60_G1234_m12_exec10_20261105_CLOSED_PENDING_SELECTION -->
## 2026-11-05 F2c四路与M1融合：官方两次结果收口

- G1删最终重复invR、以Adds(eps)替代初始c0填充/Axpy；G2单独试固定NORMAL128-lane nativeDiv，保留padding与原生除法；G3转置16→11 repeats、尾部64→24、回写96→88，保留pitch128/stage136/dummy初始化和依赖屏障；G4最后CT读取后直接strided预取next矩阵/gates并省raw重排。完整SHA：G1 `8b21b43e5ffa29dbec148a3f1993112eda7008df3324a5a5cb0ab7de8e007173`；G2 `905b481893c2f2b3d7fc56bf2fac54f44f1cd8995fe9437d3d87253b8e3591d3`；G3 `050f0ae851ce6262e6037256a8ab902c9a6e58bd476042779055ffd9fa7e4ee7`；G4 `10dc6229431bce5ee7486fb44f636747ef72028140fe82a70338e6a703b9b3dd`；M1 `fc27b164f8c76f62bb9c621934f094cfac9d6bc711ff9e47af713f5ba6088f6f`。
- 四独立结果与融合结果：G1=59.90/60.91 us，均值60.405；G2=62.27/59.54 us，均值60.905；G3=60.64/59.02 us，均值59.830；G4=61.55/63.46 us，均值62.505；M1=60.63/58.54 us，均值59.585。G2仅均值微小改善且两次跨度大、A3更慢；G4官方两次均回退，均不纳入融合。保留所有慢结果，不以最小值拼版。
- G1和G3有独立正向信号，故按授权生成M1=G1+G3；父端验证9个非重叠编辑精确并集，保护文件无改动。五版各4297项通过且对F2c逐位一致；M1全部12891个输出文件通过哈希确认后引用完整F2c原始输出，不丢失可恢复证据。
- A3两阶段case4：G1 51.099/51.179、G2 52.099/52.039、G3 50.499/50.559、G4 52.399/52.239、M1 50.259/50.399 us，对照F2c旧50.919/50.999。M1本机更快不能替代A2结论；G4额外strided DMA/地址控制可能抵消重排收益，但未取得A2周期归因，不能写成已证实瓶颈。
- 推荐M1，两次均值59.585 us，相对F2c 61.10改善2.48%；仍只有2次、不得断言稳定突破60。正式保留F2c等待用户选择；本轮10次全部Pass，无额外POST。完整五case/分数/账号/SID与源码绑定见[final_report.json](/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_F2c_break60_G1234_m12_exec10_20261105/analysis/final_report.json)和总history同任务块。


<!-- A_case4_M1_toward44_analysis_20261105_M1_SELECTED_PLAN -->
## 2026-11-05 M1已选定：下一轮应改反馈依赖与内部布局

- 正式基线M1 SHA `fc27b164f8c76f62bb9c621934f094cfac9d6bc711ff9e47af713f5ba6088f6f`，case4复用60.63/58.54us均值59.585；全五项/SID/选版收据见总history同任务块。到44.33需再降低25.602%；不把peer旧57.31描述等同于最新44.33源码。
- R1保留88真lane，将每次Axpy/Add分母修正及nativeDiv共用COUNTER域，I20从79个包装区间降40，保留原vaxpy/vdiv树。R2在末级BR8后分头64/尾24，依次同窗口放Axpy头+BR8尾、Div头+Axpy尾、下轮Mul头+Div尾；原pitch128不改，源级仍6个窗口而非减少屏障，每半步多3调用，必须以完整owner和官方两次结果裁决。
- R3作为有边界的大改动诊断：q2四个C/CT各33792B改head[88,64]+tail[88,32]，单product22528B、双roots、独立三分母和四个1024B inverse ring，总pool178688B，按实际资源准入。ring偏移headOdd0/headEven256/tailOdd512/tailEven640；两条nativeDiv生成相位视图，避免Div→Copy新依赖。跨token BR2/Axpy/Div与对方Mul/Mla/BR1交错，双半步窗口12→6但每half调用6→9、Div有效lane88→176；所有数学与求和树保留。
- 审核否决连续pitch96简单压紧：row stride12块令相位按0/12/8/4变化，固定factor的8组与矩阵8组平均重合4组（静态集合，不是PMU占比）；分离面板按偶/奇行调用可消去这一读组重合，但不能证明零读写冲突或零等待。旧D3已是q2+q1且A3斜率2.498，不能包装为新试验；新R3必须证明真实窗口机制与完整owner3净收益，尾部8行转置、raw不适配product、额外输出DMA均纳入。
- R4按C0=min(N,C),L=ceil(N/C0),B=ceil(N/L)选owner；N96/C40示例40混合2/3→32全3，最长仍3，不能声称少20%计算。建议R1→R2→R4，R3仅本地诊断准入后使用两次正式机会；独立收益才融合，R2/R3互为反馈结构备选而非直接相加。无新编译/NPU/POST，M1保持；详细机制、旧负例、全部CPU证明与官方API/SDK来源见[方案](/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_M1_toward44_analysis_20261105/analysis/next_round_plan.json)。


<!-- A_case4_M1_feedback_R1243_m12_exec10_20261105_CLOSED_PENDING_SELECTION -->
## 2026-11-05 工作区 A：M1 上的 case4 反馈与分核实验

- R1 合并 COUNT88 mask 窗口；R2 在 64+24 反馈上分段调度；R4 仅改变 H88 F2 路径核数。R3b 实现双 token 分面板、共享单 product 及 q1 尾 token，已在真实设备验证命中新入口。
- case4 官方两次与均值（μs）：R1 60.25/60.01（均值60.130）；R2 62.87/63.08（均值62.975）；R4 56.49/57.19（均值56.840）。每组仅两次，对照跨时复用；未测隐藏单项，不按单笔最低值拼接。
- R3 原草稿 N256 的 pre 7040 项错误；诊断 token 0/2 的门控输出与下一对 token 2/4 原始输入完全匹配。R3b 增设 MTE3→MTE2 依赖后 4297 组与 M1 逐位相等；实际双 token 入口 A3 完整 case4 两阶段 68.138/67.219 μs（M1 50.259/50.399），未达准入条件，未 POST。仅 R4 有独立官方正收益，未做融合。
- 推荐 R4，官方 case4 均值 56.840 μs，相比 M1 59.585 μs 降低 2.745 μs（4.61%）。仍比同学 44.33 μs 高 12.51 μs。 正式源码九文件及基线指针已核验；未切换基线，等待用户选择。 完整验证、评测机豁免及逐笔结果见 [final_report.json](/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_M1_feedback_R1243_m12_exec10_20261105/analysis/final_report.json)。


<!-- A_case4_M1_feedback_R1243_m12_exec10_20261105_SELECTED_R4 -->
## 2026-11-05 工作区 A：R4 正式选版

- 用户选择 R4 为工作区 A 正式基线，替换 M1；完整 kernel SHA-256：`0fded51730b6eb75aa27477c54647f3f69c359af514097744d76577582c98943`，任务 `A_case4_M1_feedback_R1243_m12_exec10_20261105`。
- R4 仅改变 H88 F2 路径分核。复用 member1 / member2 的两笔官方 Pass：case4 56.49 / 57.19 μs，均值 56.840 μs；旧 M1 均值 59.585 μs。
- 两笔同源码五项耗时（μs）：member1 6aec005a1dac5d235b1d416d [477.23, 1.57, 9.64, 56.49, 34.43]；member2 6aec00cf1dac5d235b1e18fa [474.85, 1.53, 9.67, 57.19, 35.39]。4297 组设备验证与 M1 逐位一致。
- 正式工程全部 9 文件、冻结快照及共享基线指针已核验；原 M1 与回退副本保留，本次未编译、未用 NPU、未新增提交。[选版回执](/mnt/workspace/enjoy_ur_time/workspaces/A/tasks/A_case4_M1_feedback_R1243_m12_exec10_20261105/selection_R4_20261105/selection.json)。
