# Case 5 优化历史

更新日期：2026-10-23（北京时间）。此文件承载 SinkhornNorm 可见测试点 5 的对点观察、试验和经验；共性方法与完整版本 SHA 见 [整体历史](history.md)。

## 身份与证据边界

- 平台：`op_challenge_xinan_final/sinkhorn_norm`，可见结果行 case 5。
- B、S、H、iters、输入分布与当前实现路径：未知，尚无可靠 case→shape 映射。
- 下表是全局版本在本 case 上的观察，不代表此前已完成本 case 的独立定向优化。编号仅用于记录，不允许据编号分派专属实现。
- 云端活动文件在迁移时为 R4（1aa53705），Windows 与最近核对的提交为 R5（17a7d6e0）；本次未切换源码。

## 已确认的平台历史

时间统一为 μs。“下降”为相对上一版本的用时下降百分比，负值表示变慢。结果是平台显示值，有舍入且缺少重复采样。

| 版本 | 提交 | SHA前缀 | 用时 μs | 相邻版本用时下降 | 本项结果 / 显示误差 |
|---|---:|---|---:|---:|---|
| R1（A2 基线） | 928045 | `34db99ae` | 794.24 | — | Pass / 0.00% |
| R2 | 928374 | `49b5f35d` | 568.44 | 28.43% | Pass / 0.00% |
| R3 | 928539 | `7d2ce01c` | 475.05 | 16.43% | Pass / 0.00% |
| R4 | 928794 | `1aa53705` | 455.46 | 4.12% | Pass / 0.00% |
| R5 | 929094 | `17a7d6e0` | 447.69 | 1.71% | Pass / 0.00% |

方法依次为：A2索引基线、R2驻留行归一化合批、R3驻留列累加合批、R4 softmax Exp/分母广播/Div/eps合批、R5 max广播/Sub合批。完整方法、验证层级、版本保留情况见整体历史。

证据：[R1](/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/evidence/windows_20261023/work/sinkhorn_local_20261023/r2_20261023_170335/baseline_ui_results.json)、[R2/R3](/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/evidence/windows_20261023/work/sinkhorn_local_20261023/r4_softmax_20261023/r2_vs_r3_ui.json)、[R4](/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/evidence/windows_20261023/work/sinkhorn_local_20261023/r4_feedback_20261023_184008/comparison.json)、[R5](/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/evidence/r5_feedback_20261023/feedback.json)。R3 使用真实提交928539；18:17旧截图实际为R2。

## 2026-10-23 — 迁移时的观察

- R2→R3 从568.44降至475.05 μs，下降16.43%；R4→R5 从455.46降至447.69 μs，下降1.71%。有持续改善，但页面最优值同步变化，不能据最优分母变化判断本版本回退或提升。
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
- 本项：Pass，precision_ratio=1，447.8 μs；本轮R5基线 447.8 μs，加速 1.0×。
- 共性方法、其他case回退和整体决定见 [总历史](history.md)；单次用时与未知shape不足以确定本case唯一瓶颈。
- 证据：[本轮comparison](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_40/R01/comparison.json)；正式提交 6adb51fd1dac5d235bf35d7f。

## 2026-10-23 — C02（member1，keep）

- 全局候选：WholeReduceSum one-repeat rows；完整SHA 70cd60951e71df30229935d41bf1d4dcf15e3898dacaee77cf6129dd2bd1e8ba。不是按case编号分派。
- 本项：Pass，precision_ratio=1，166.83 μs；本轮R5基线 447.8 μs，加速 2.684169513876401×。
- 共性方法、其他case回退和整体决定见 [总历史](history.md)；单次用时与未知shape不足以确定本case唯一瓶颈。
- 证据：[本轮comparison](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_40/R02/comparison.json)；正式提交 6adb52ba1dac5d235bf3ed76。

## 2026-10-23 — C03（member1，keep）

- 全局候选：WholeReduceSum all rows with original repeat order；完整SHA 91dedc25461bbbb3d1147ab9c4532c3cf8b5cf065ed1336ee6e09bae8b94088f。不是按case编号分派。
- 本项：Pass，precision_ratio=1，165.15 μs；本轮R5基线 447.8 μs，加速 2.711474417196488×。
- 共性方法、其他case回退和整体决定见 [总历史](history.md)；单次用时与未知shape不足以确定本case唯一瓶颈。
- 证据：[本轮comparison](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_40/R03/comparison.json)；正式提交 6adb543a1dac5d235bf4f664。

## 2026-10-23 — C05（member1，keep）

- 全局候选：Retry vector maxima candidate after HTTP 429 cooldown；完整SHA 2d77a04f0d857a80f4d942bd0fa4b75b8690442847524de4f69a876ad692d311。不是按case编号分派。
- 本项：Pass，precision_ratio=1，146.47 μs；本轮R5基线 447.8 μs，加速 3.057281354543593×。
- 共性方法、其他case回退和整体决定见 [总历史](history.md)；单次用时与未知shape不足以确定本case唯一瓶颈。
- 证据：[本轮comparison](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_40/R05/comparison.json)；正式提交 6adb56541dac5d235bf66313。

## 2026-10-23 — C06（member1，confirm）

- 全局候选：Final confirmation of retained best candidate；完整SHA 2d77a04f0d857a80f4d942bd0fa4b75b8690442847524de4f69a876ad692d311。不是按case编号分派。
- 本项：Pass，precision_ratio=1，146.86 μs；本轮R5基线 447.8 μs，加速 3.049162467656271×。
- 共性方法、其他case回退和整体决定见 [总历史](history.md)；单次用时与未知shape不足以确定本case唯一瓶颈。
- 证据：[本轮comparison](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_40/R06/comparison.json)；正式提交 6adb579c1dac5d235bf7631c。

## 2026-10-23 — 五次提交收尾

- 最终同源复测 146.86 μs；本轮R5基线 447.80 μs，加速 3.049×；Pass、precision_ratio=1。
- 全局批量归约/最大值/门控优化，不按case编号分派；shape映射仍未知。
- 最终SHA 2d77a04f0d857a80f4d942bd0fa4b75b8690442847524de4f69a876ad692d311；提交 6adb579c1dac5d235bf7631c。
- [整体结果与验证边界](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_40/final_summary.md)；本轮5/5已停止。

## 2026-10-23 — Q01（member1额度轮次）

- 全局方法：Planes column recurrence，不是按case编号分派。
- 本项：Pass，precision_ratio=1；147.53μs，相对本轮起始146.86μs加速0.9954585508032265×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA ef9466313272825664fac4550d28896201301dac28a67c0016c3bbe7a31c571b；提交6adb60e51dac5d235bfe22ed；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R01/comparison.json)。

## 2026-10-23 — Q02（member1额度轮次）

- 全局方法：Resident input double buffer prefetch，不是按case编号分派。
- 本项：Pass，precision_ratio=1；141.14μs，相对本轮起始146.86μs加速1.0405271361768458×。
- 整体决定：keep；其他case及验证边界见[整体历史](history.md)。
- SHA 0bbf4cd87e76162fcc7fcb39a1c697fd3ed786ab27f92b4e30be40bbcd3a52ff；提交6adb61fa1dac5d235bfee208；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R02/comparison.json)。

## 2026-10-23 — Q03（member1额度轮次）

- 全局方法：Packed column division with retained prefetch，不是按case编号分派。
- 本项：Pass，precision_ratio=1；141μs，相对本轮起始146.86μs加速1.0415602836879434×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA eaffa14b9114c2df57611c01e2ed879e493dc4a91e1c4961a9e36055118a8128；提交6adb63341dac5d235bffb3b4；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R03/comparison.json)。

## 2026-10-23 — Q04（member1额度轮次）

- 全局方法：Resident token batching Q2 with platform UB budget，不是按case编号分派。
- 本项：Pass，precision_ratio=1；138.56μs，相对本轮起始146.86μs加速1.059901847575058×。
- 整体决定：keep；其他case及验证边界见[整体历史](history.md)。
- SHA ba20fab7b1f77f45c38e220ceedf3ec2679b78f505122e88ffc798a08eecbc94；提交6adb658a1dac5d235b013a47；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R04/comparison.json)。

## 2026-10-23 — Q05（member1额度轮次）

- 全局方法：Resident token batching Q4 with platform UB budget，不是按case编号分派。
- 本项：Pass，precision_ratio=1；136.47μs，相对本轮起始146.86μs加速1.076133948853228×。
- 整体决定：keep；其他case及验证边界见[整体历史](history.md)。
- SHA 396102c2330e43208733d32f5c907de495dbf3a8a6adfe1a6cc2a85eb88957a1；提交6adb66711dac5d235b01db52；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R05/comparison.json)。

## 2026-10-23 — Q06（member1额度轮次）

- 全局方法：Resident batching cap 8，不是按case编号分派。
- 本项：Pass，precision_ratio=1；136.54μs，相对本轮起始146.86μs加速1.0755822469605978×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 50d028065d4bfacc4b6b5e3ecc1c09fa8d1f084621780aaa9f38aa7b460451e2；提交6adb67441dac5d235b026a4e；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R06/comparison.json)。

## 2026-10-23 — Q07（member1额度轮次）

- 全局方法：Resident batching cap 16，不是按case编号分派。
- 本项：Pass，precision_ratio=1；140.44μs，相对本轮起始146.86μs加速1.045713471945315×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA a3c2a2db229815bb4d19963737fbced534f6c9c5c4e5c1bc515ff75939e6b286；提交6adb68161dac5d235b031538；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R07/comparison.json)。

## 2026-10-23 — Q08（member1额度轮次）

- 全局方法：Resident batching cap 32，不是按case编号分派。
- 本项：Pass，precision_ratio=1；135.62μs，相对本轮起始146.86μs加速1.0828786314702847×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 21d0ead62d85dabe8951495441aadfabc967132cf471c0426ff2faa0a09a8b42；提交6adb68ea1dac5d235b03bc72；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R08/comparison.json)。

## 2026-10-23 — Q09（member1额度轮次）

- 全局方法：Q4 shared work buffer offset 256B，不是按case编号分派。
- 本项：Pass，precision_ratio=1；136.78μs，相对本轮起始146.86μs加速1.0736949846468782×。
- 整体决定：keep；其他case及验证边界见[整体历史](history.md)。
- SHA cbb15d25acf518b255d0edd0b3ab5e4c921dc245b9507f039267b5c8b4b31593；提交6adb69be1dac5d235b046b42；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R09/comparison.json)。

## 2026-10-23 — Q10（member1额度轮次）

- 全局方法：Q8 batch prefetch while preserving batch size，不是按case编号分派。
- 本项：Pass，precision_ratio=1；141.1μs，相对本轮起始146.86μs加速1.040822111977321×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA f8312d80b9e8829f2d7369a5105b8eff1d3b69c5f65fc4ccde5c5c070a6b31ba；提交6adb6a921dac5d235b050723；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R10/comparison.json)。

## 2026-10-23 — Q11（member1额度轮次）

- 全局方法：Q8 batch prefetch with capacity-driven smaller batches，不是按case编号分派。
- 本项：Pass，precision_ratio=1；142.29μs，相对本轮起始146.86μs加速1.0321175065008084×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 94acb4244a31622add652fd25c11d012a9e5aca35a8ad03bb9fe3c1418d7df5b；提交6adb6b661dac5d235b05b13d；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R11/comparison.json)。

## 2026-10-23 — Q12（member1额度轮次）

- 全局方法：Small-matrix planes batch cap 64，不是按case编号分派。
- 本项：Pass，precision_ratio=1；137.32μs，相对本轮起始146.86μs加速1.069472764346053×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA a3f24b8cf2aad039f206185dace870fd4034dacabcaa4295da234fba3485a5e2；提交6adb6c3a1dac5d235b064c06；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R12/comparison.json)。

## 2026-10-23 — Q13（member1额度轮次）

- 全局方法：Small-matrix planes batch cap 128，不是按case编号分派。
- 本项：Pass，precision_ratio=1；138.09μs，相对本轮起始146.86μs加速1.0635093055253821×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA b4710b1d75d997096aa35b6b4fc34f8bf95cb1416fa0054a690bd49fcbbf9422；提交6adb6d0d1dac5d235b06ea41；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R13/comparison.json)。

## 2026-10-23 — Q14（member1额度轮次）

- 全局方法：Small-matrix planes batch cap 256，不是按case编号分派。
- 本项：Pass，precision_ratio=1；138.76μs，相对本轮起始146.86μs加速1.0583741712309025×。
- 整体决定：keep；其他case及验证边界见[整体历史](history.md)。
- SHA 8dd74dc1752eb792e00217c4325505104051d0e7cc13e128748f70de40216298；提交6adb6de01dac5d235b0787f8；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R14/comparison.json)。

## 2026-10-23 — Q15（member1额度轮次）

- 全局方法：Small-matrix planes batch cap 512，不是按case编号分派。
- 本项：Pass，precision_ratio=1；144.49μs，相对本轮起始146.86μs加速1.0164025192054813×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 308ea9e6be07218d5adbfd97890b47469cf98421237465e5e616faadf9b0d14f；提交6adb6eb31dac5d235b08259e；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R15/comparison.json)。

## 2026-10-23 — Q16（member1额度轮次）

- 全局方法：Small-matrix planes batch cap 1024，不是按case编号分派。
- 本项：Pass，precision_ratio=1；142.35μs，相对本轮起始146.86μs加速1.0316824727783633×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 721a306abc195eb854fd7a3670de0f9a2f987d25f157544424a34e5678dcd3c5；提交6adb6f861dac5d235b08c695；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R16/comparison.json)。

## 2026-10-23 — Q17（member1额度轮次）

- 全局方法：Additional 256B statistics offset，不是按case编号分派。
- 本项：Pass，precision_ratio=1；137.62μs，相对本轮起始146.86μs加速1.0671414038657172×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 9c91baed8d6afaafb5c435235fc10515a9669449c07cc9857d7f2c8eec6ad3eb；提交6adb70591dac5d235b0959a2；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R17/comparison.json)。

## 2026-10-23 — Q18（member1额度轮次）

- 全局方法：Metadata-dependent statistics offset，不是按case编号分派。
- 本项：Pass，precision_ratio=1；135.87μs，相对本轮起始146.86μs加速1.0808861411643484×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA a5b07022660a41acb7dfced56e6c5f2903ed6dab93945cc19767ec779873a3ea；提交6adb712c1dac5d235b09f3de；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R18/comparison.json)。

## 2026-10-23 — Q19（member1额度轮次）

- 全局方法：Three single-path device entries，不是按case编号分派。
- 本项：Pass，precision_ratio=1；137.03μs，相对本轮起始146.86μs加速1.071736116178939×。
- 整体决定：keep；其他case及验证边界见[整体历史](history.md)。
- SHA fa341fa1cc2b7f91a3883292ea6c9782bcff6038c3eb59d13fdd6f01d1d01957；提交6adb71ff1dac5d235b0a93cf；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R19/comparison.json)。

## 2026-10-23 — Q20（member1额度轮次）

- 全局方法：Dense aligned elementwise stages in batched resident，不是按case编号分派。
- 本项：Pass，precision_ratio=1；139.58μs，相对本轮起始146.86μs加速1.0521564694082246×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 198d17d54937a4464cd7351d0cd4d45bcc26e2063ccb5361d55e737594ae48bf；提交6adb72d21dac5d235b0b3714；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R20/comparison.json)。

## 2026-10-23 — Q21（member1额度轮次）

- 全局方法：Dense aligned elementwise stages in both resident paths，不是按case编号分派。
- 本项：Pass，precision_ratio=1；137.46μs，相对本轮起始146.86μs加速1.0683835297541102×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 4dfa4eba61620c1c54ffc26980e3fbdc06b01caaf81920a2fca6dafae3c3a0b5；提交6adb73a51dac5d235b0be066；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R21/comparison.json)。

## 2026-10-23 — Q22（member1额度轮次）

- 全局方法：列求和跨token组块，不是按case编号分派。
- 本项：Pass，precision_ratio=1；136.97μs，相对本轮起始146.86μs加速1.0722055924655034×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA e34c8e461f239dfdd7a1170f5dcf354e54d09c8998f54523908f1931886ce10f；提交6adb74781dac5d235b0c792e；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R22/comparison.json)。

## 2026-10-23 — Q23（member1额度轮次）

- 全局方法：列求和及除法跨token组块，不是按case编号分派。
- 本项：Pass，precision_ratio=1；136.35μs，相对本轮起始146.86μs加速1.0770810414374772×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 19e16a88cc7856f25c821b9fd493c5f4ece6edcde31f6cd02e5043d94f4f2bda；提交6adb754b1dac5d235b0d04fa；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R23/comparison.json)。

## 2026-10-23 — Q24（member1额度轮次）

- 全局方法：Q8列归一化组块，不是按case编号分派。
- 本项：Pass，precision_ratio=1；135.06μs，相对本轮起始146.86μs加速1.0873685769287724×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA dd19d5f2cdba44f118462f841ee50e294e35924230f3ac58b4c5592e32bccd06；提交6adb761e1dac5d235b0d9bc5；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R24/comparison.json)。

## 2026-10-23 — Q25（member1额度轮次）

- 全局方法：守卫式核心数紧凑分配，不是按case编号分派。
- 本项：Pass，precision_ratio=1；133.31μs，相对本轮起始146.86μs加速1.1016427874878105×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 45f4c791f69d70079f1b415352f91f1669af8077e6f006a6ace991f042677f69；提交6adb76f11dac5d235b0e2e72；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R25/comparison.json)。

## 2026-10-23 — Q26（member1额度轮次）

- 全局方法：守卫式批量对齐分配，不是按case编号分派。
- 本项：Pass，precision_ratio=1；135.7μs，相对本轮起始146.86μs加速1.0822402358142964×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 09fe685aba1d0bb42a09bcf6ab13954237ce62a0c91112db6016ac91bbf4981e；提交6adb77c41dac5d235b0ebc17；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R26/comparison.json)。

## 2026-10-23 — Q27（member1额度轮次）

- 全局方法：planes256输出索引前缀扩展，不是按case编号分派。
- 本项：Pass，precision_ratio=1；136.42μs，相对本轮起始146.86μs加速1.0765283682744469×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 53b5d91a58548c4672c11aebcc4fb63013bed40a676b6a47a359d38d741df763；提交6adb78971dac5d235b0f4d11；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R27/comparison.json)。

## 2026-10-23 — Q28（member1额度轮次）

- 全局方法：planes256输入输出索引扩展，不是按case编号分派。
- 本项：Pass，precision_ratio=1；145.95μs，相对本轮起始146.86μs加速1.0062350119904078×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA cd4474bd0e5f8c9080c12e7d47e6d948ef18ba6e5541c76ddead0c75d3a7b669；提交6adb796a1dac5d235b0fe1de；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R28/comparison.json)。

## 2026-10-23 — Q29（member1额度轮次）

- 全局方法：更大planes批次及索引前缀，不是按case编号分派。
- 本项：Pass，precision_ratio=1；145.83μs，相对本轮起始146.86μs加速1.0070630185832818×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 80cb32c1e115648e03ee879ee971c2822c0a68e9566ee072509e97782aba6f4e；提交6adb7a3e1dac5d235b106e20；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R29/comparison.json)。

## 2026-10-23 — Q30（member1额度轮次）

- 全局方法：Case1目标：行与token交错布局 work256，不是按case编号分派。
- 本项：Pass，precision_ratio=1；136.59μs，相对本轮起始146.86μs加速1.0751885203894869×。
- 整体决定：keep；其他case及验证边界见[整体历史](history.md)。
- SHA bb5be613d95c6c1cf6d5f9eacafc6098d908a34dfaa0d48ed0a0b24f331b4353；提交6adb7bc61dac5d235b117f0d；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R30/comparison.json)。

## 2026-10-23 — Q31（member1额度轮次）

- 全局方法：Case1目标：行与token交错布局 work0，不是按case编号分派。
- 本项：Pass，precision_ratio=1；137.12μs，相对本轮起始146.86μs加速1.0710326721120187×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 2c45ef2111bc5e5ef6e562aa0467e13e0b8cfbdb737d7dcfdfa7ebb35090f9a6；提交6adb7c991dac5d235b120d85；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R31/comparison.json)。

## 2026-10-23 — Q32（member1额度轮次）

- 全局方法：Case1目标：行Div分母展开tile64，不是按case编号分派。
- 本项：Pass，precision_ratio=1；136.43μs，相对本轮起始146.86μs加速1.0764494612621858×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 0ab5db162f799f6d1e8e3ec85fecc2c3a011b62704141afafccaca30a66ac826；提交6adb7d6d1dac5d235b12a043；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R32/comparison.json)。

## 2026-10-23 — Q33（member1额度轮次）

- 全局方法：Case1目标：行Div分母展开tile128，不是按case编号分派。
- 本项：Pass，precision_ratio=1；136.47μs，相对本轮起始146.86μs加速1.076133948853228×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 1d4533fe054c86aa75521328ddc32bc7b27055048905aea8e582bbc59ca3ce46；提交6adb7e411dac5d235b133ef6；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R33/comparison.json)。

## 2026-10-23 — Q34（member1额度轮次）

- 全局方法：Case1目标：UB偏移128对照，不是按case编号分派。
- 本项：Pass，precision_ratio=1；140.01μs，相对本轮起始146.86μs加速1.04892507678023×。
- 整体决定：revert；其他case及验证边界见[整体历史](history.md)。
- SHA 9d34e7de50a81abe17baedab04e2b7b21e927d53aea43d8afbd1f524d5ee9289；提交6adb7f151dac5d235b13ce16；[证据](../../others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261023_member1_quota/R34/comparison.json)。


## 2026-10-24T13:48:04.977645+08:00 — 行归约5次轮 R01

- 公共方法：campaign_20261024_rowreduce_member1_5/baseline.asc；完整记录见整体 history 同轮，源码SHA dcd9794f403ebf6a3fba6af26b7b64a1319d59f201b5e37cb94d244f58abb59b。
- A2本项用时 140.29 μs，状态 Pass；相对本轮新基线 1.0。
- 整体决定 baseline；提交 6adc466c1dac5d235b8678f2；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_rowreduce_member1_5/R01/comparison.json。隐藏项不外推。


## 2026-10-24T13:56:40.348251+08:00 — 行归约5次轮 R02

- 公共方法：block_reduce/first64_block_compact_pairs.asc；完整记录见整体 history 同轮，源码SHA 27094f3ffb778a805dc7e62016520351b80f3e6cceb869fb0401dbc4413eb928。
- A2本项用时 144.55 μs，状态 Pass；相对本轮新基线 1.0303656711098441。
- 整体决定 revert；提交 6adc486f1dac5d235b87db4b；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_rowreduce_member1_5/R02/comparison.json。隐藏项不外推。


## 2026-10-24T14:00:12.400207+08:00 — 行归约5次轮 R03

- 公共方法：block_reduce/full_vector_tiles_block_compact_pairs.asc；完整记录见整体 history 同轮，源码SHA 2fd0a4b32bb5af781d3ea5da5b2b40a8f2e9128f0e082fec519055853b33f20c。
- A2本项用时 142.53 μs，状态 Pass；相对本轮新基线 1.0159669256540025。
- 整体决定 keep；提交 6adc49431dac5d235b886ce4；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_rowreduce_member1_5/R03/comparison.json。隐藏项不外推。


## 2026-10-24T14:04:24.941807+08:00 — 行归约5次轮 R04

- 公共方法：block_reduce/composite_full_tiles_and_first64_compact_pairs.asc；完整记录见整体 history 同轮，源码SHA ba47bc0955282436fb48cb8dcc73071d8a5d64245e25f283866d32a0f33023d7。
- A2本项用时 143.5 μs，状态 Pass；相对本轮新基线 1.0228811747095303。
- 整体决定 keep；提交 6adc4a401dac5d235b891e5a；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_rowreduce_member1_5/R04/comparison.json。隐藏项不外推。


## 2026-10-24T14:07:56.163298+08:00 — 行归约5次轮 R05

- 公共方法：campaign_20261024_rowreduce_member1_5/best.asc；完整记录见整体 history 同轮，源码SHA ba47bc0955282436fb48cb8dcc73071d8a5d64245e25f283866d32a0f33023d7。
- A2本项用时 143.82 μs，状态 Pass；相对本轮新基线 1.0251621640886734。
- 整体决定 confirm；提交 6adc4b131dac5d235b898bed；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_rowreduce_member1_5/R05/comparison.json。隐藏项不外推。


## 2026-10-24T14:10:01.940760+08:00 — 行归约5次轮结案

- A2 R01→R05 μs：[140.29, 144.55, 142.53, 143.5, 143.82]；最终相对新基线变化+2.52%，平台各轮本项均Pass。最终提交 6adc4b131dac5d235b898bed。
- 对点经验：本项R02=144.55μs、R03=142.53μs、R04=143.50μs、R05=143.82μs，相对新基线140.29μs最终增加2.52%。本轮整体保留不等于本项优化成功；后续需单独诊断，不能通过改iters/Div/精度容差换性能。
- 正确性与范围：保留源码SHA ba47bc0955282436fb48cb8dcc73071d8a5d64245e25f283866d32a0f33023d7，最终候选4660组A3逐位/guards/input检查通过，原始归约树微测通过；严格iters、原求和树/最终Add与Div。隐藏10项细节未知。
- 决定与证据：保留复合版；今日member1已50/50，本轮5/5停止。整体方法/失败候选见history.md本节；固定证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_rowreduce_member1_5/final_audit.json，逐轮comparison.json与诊断日志保留。


## 2026-10-24T14:28:50.242599+08:00 — 短行归约member2轮 R01

- 公共方法：campaign_20261024_shortrow_member2_limit50/baseline.asc；完整记录见整体 history 同轮，源码SHA ba47bc0955282436fb48cb8dcc73071d8a5d64245e25f283866d32a0f33023d7。
- A2本项用时 143.2 μs，状态 Pass；相对本轮新基线 1.0。
- 整体决定 baseline；提交 6adc4ff91dac5d235b8ccfd3；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_shortrow_member2_limit50/R01/comparison.json。隐藏项不外推。


## 2026-10-24T14:36:43.562193+08:00 — 短行归约member2轮 R02

- 公共方法：candidates/shortrow_v1.asc；完整记录见整体 history 同轮，源码SHA 01f12292d9aaa69a07c880eb9402de0ece6e1c04c52927f7f729a191689720e8。
- A2本项用时 142.32 μs，状态 Pass；相对本轮新基线 0.993854748603352。
- 整体决定 revert；提交 6adc51d31dac5d235b8dd273；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_shortrow_member2_limit50/R02/comparison.json。隐藏项不外推。


## 2026-10-24T14:40:47.186026+08:00 — 短行归约member2轮 R03

- 公共方法：candidates/shortrow_q8_v2.asc；完整记录见整体 history 同轮，源码SHA 2268d38c4c33dd71b313e67334870944a7dd1c406f1f268545444c4775016fd6。
- A2本项用时 147.28 μs，状态 Pass；相对本轮新基线 1.028491620111732。
- 整体决定 revert；提交 6adc52c61dac5d235b8e54e6；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_shortrow_member2_limit50/R03/comparison.json。隐藏项不外推。


## 2026-10-24T14:45:04.619852+08:00 — 短行归约member2轮 R04

- 公共方法：candidates/resident_single_v3.asc；完整记录见整体 history 同轮，源码SHA f748ba3a462a726efea33b7ef60d52fc6452c8245002dedebe5f88394214ff8d。
- A2本项用时 147.09 μs，状态 Pass；相对本轮新基线 1.0271648044692738。
- 整体决定 revert；提交 6adc53c81dac5d235b8eea12；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_shortrow_member2_limit50/R04/comparison.json。隐藏项不外推。


## 2026-10-24T15:12:49.177835+08:00 — 短行归约member2轮 R05

- 公共方法：candidates/planes_sequential_row_add_v4.asc；完整记录见整体 history 同轮，源码SHA 8a82febc5c631ba958251e9b5da7ffcfb088d8e8a0c7dc90990a28bf585feb4a。
- A2本项用时 147.18 μs，状态 Pass；相对本轮新基线 1.0277932960893856。
- 整体决定 revert；提交 6adc5a481dac5d235b9315ce；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_shortrow_member2_limit50/R05/comparison.json。隐藏项不外推。


## 2026-10-24T15:19:10.119951+08:00 — 短行归约member2轮 R06

- 公共方法：candidates/padded_shortrow_oneblock_v5b.asc；完整记录见整体 history 同轮，源码SHA 984810a0b56de8b4482765ae4a7cbcd3e34fed54f7ea7a2dd62ca3ce4b2e2844。
- A2本项用时 147.21 μs，状态 Pass；相对本轮新基线 1.0280027932960896。
- 整体决定 revert；提交 6adc5bc51dac5d235b93d224；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_shortrow_member2_limit50/R06/comparison.json。隐藏项不外推。


## 2026-10-24T15:23:05.581076+08:00 — 短行归约member2轮 R07

- 公共方法：candidates/single_padded_shortrow_v9b.asc；完整记录见整体 history 同轮，源码SHA 87771bfc136ea609d303b189de8c20d5dd66b15e052aeeebfe3982e32a3abff6。
- A2本项用时 147.06 μs，状态 Pass；相对本轮新基线 1.02695530726257。
- 整体决定 revert；提交 6adc5cb11dac5d235b9467cd；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_shortrow_member2_limit50/R07/comparison.json。隐藏项不外推。


## 2026-10-24T15:30:17.298105+08:00 — 短行归约member2轮 R08

- 公共方法：candidates/isolated_padded_batch_entry_v12.asc；完整记录见整体 history 同轮，源码SHA b2a501f0e1656764c77a136a71b7cf5c4729e89fe4455abb35db0735e8389f9f。
- A2本项用时 146.15 μs，状态 Pass；相对本轮新基线 1.020600558659218。
- 整体决定 revert；提交 6adc5e601dac5d235b959931；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_shortrow_member2_limit50/R08/comparison.json。隐藏项不外推。


## 2026-10-24T15:38:57.971946+08:00 — 短行归约member2轮 R09

- 公共方法：candidates/isolated_native_pitch_batch_v14.asc；完整记录见整体 history 同轮，源码SHA 33aa904c4555f8a08da6f5e2817a5f67d5df4925e98d1efd4e09af33ecb036e9。
- A2本项用时 146.27 μs，状态 Pass；相对本轮新基线 1.0214385474860337。
- 整体决定 revert；提交 6adc60651dac5d235b971a50；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_shortrow_member2_limit50/R09/comparison.json。隐藏项不外推。


## 2026-10-24T15:42:30.407273+08:00 — 短行归约member2轮 R10

- 公共方法：campaign_20261024_shortrow_member2_limit50/best.asc；完整记录见整体 history 同轮，源码SHA ba47bc0955282436fb48cb8dcc73071d8a5d64245e25f283866d32a0f33023d7。
- A2本项用时 144.85 μs，状态 Pass；相对本轮新基线 1.011522346368715。
- 整体决定 confirm；提交 6adc613e1dac5d235b97e547；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_shortrow_member2_limit50/R10/comparison.json。隐藏项不外推。


## 2026-10-24T15:42:30.404814+08:00 — member2_shortrow_final_additional5_20261024

- 结果：新基线 143.2 μs；选中版本 R01，最终确认 144.85 μs，提交 6adc613e1dac5d235b97e547。
- 最后五次对照：[('R06', 147.21, 'revert'), ('R07', 147.06, 'revert'), ('R08', 146.15, 'revert'), ('R09', 146.27, 'revert'), ('R10', 144.85, 'confirm')]。整体保留决定见history.md，不以单项最低值冒充当前版本表现。
- 精度覆盖更正：旧 v1 raw 含交替正负零，但没有纯负零整行，旧 PASS 数字真实但覆盖有限；v2 reducer 同源，v1/v2/v6 的短树风险是静态继承判断。直接失败证据仅 v5 literal raw 的480个符号零差异，不是已执行的v1失败。v5b补回P16/P32遗漏的两层/一层加正零，104配置/2496数据集逐位通过；此前 member1 的 reduction_micro、micro_pair 也只覆盖交替正负零，未覆盖纯负零整行；旧 PASS 保留。ba47的H<64原WR不受此结论影响。
- 停止与证据：用户追加5次已完成，member2今日19/50，无后续提交。/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_shortrow_member2_limit50/final_audit.json；本项可见Pass，隐藏项不外推。


## 2026-10-24T16:22:22.417572+08:00 — pipe_interleave_member2_5_R01

- 方法：baseline，SHA ba47bc0955282436fb48cb8dcc73071d8a5d64245e25f283866d32a0f33023d7；公共约束和验证见整体history同轮。
- A2本项 149.54 μs；平台 Pass；当前决定 baseline，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_pipe_interleave_member2_5/R01/comparison.json，提交 6adc6a921dac5d235b9e62de；预算 1/5，隐藏项不外推。


## 2026-10-24T16:27:17.409598+08:00 — pipe_interleave_member2_5_R02

- 方法：tpipe_only，SHA 89d70d5b34175d03fc5b477fab9bc5f4a459eb26b9b632b60bd6684097bd7649；公共约束和验证见整体history同轮。
- A2本项 143.61 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_pipe_interleave_member2_5/R02/comparison.json，提交 6adc6bbc1dac5d235b9f6c8e；预算 2/5，隐藏项不外推。


## 2026-10-24T16:30:56.607213+08:00 — pipe_interleave_member2_5_R03

- 方法：baseline_control，SHA ba47bc0955282436fb48cb8dcc73071d8a5d64245e25f283866d32a0f33023d7；公共约束和验证见整体history同轮。
- A2本项 143.03 μs；平台 Pass；当前决定 baseline_control，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_pipe_interleave_member2_5/R03/comparison.json，提交 6adc6c971dac5d235ba037c0；预算 3/5，隐藏项不外推。


## 2026-10-24T16:34:29.811622+08:00 — pipe_interleave_member2_5_R04

- 方法：interleave_only，SHA 70a206311bc5abdead20442e38e415855e14d36ab0ca818f058e77ec8195192d；公共约束和验证见整体history同轮。
- A2本项 133.33 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_pipe_interleave_member2_5/R04/comparison.json，提交 6adc6d6d1dac5d235ba0ceb8；预算 4/5，隐藏项不外推。


## 2026-10-24T16:38:01.085506+08:00 — pipe_interleave_member2_5_R05

- 方法：confirm，SHA 70a206311bc5abdead20442e38e415855e14d36ab0ca818f058e77ec8195192d；公共约束和验证见整体history同轮。
- A2本项 134.95 μs；平台 Pass；当前决定 confirmation_pending_audit，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_pipe_interleave_member2_5/R05/comparison.json，提交 6adc6e401dac5d235ba155fb；预算 5/5，隐藏项不外推。


## 2026-10-24T16:39:17.431592+08:00 — member2_pipe_interleave_final5_20261024

- 五次独立对照：[('R01', 'baseline', 149.54), ('R02', 'tpipe_only', 143.61), ('R03', 'baseline_control', 143.03), ('R04', 'interleave_only', 133.33), ('R05', 'confirm', 134.95)] us；参照为R01/R03几何均值 146.24878187526897 us。
- 保留决定：R04，SHA 70a206311bc5abdead20442e38e415855e14d36ab0ca818f058e77ec8195192d；R05本项 134.95 us，确认=True。整体选择按预设规则，不能将不同候选单项最低值拼成当前版本。
- 对点经验：交错独立版本R04 133.33us、邻近基线R03 143.03us，需R05再次确认。保留原求和次序/Div后仍有改善，为自然非对齐合批布局提供证据；不靠用时认定官方shape或路径，后续应结合合法静态资源模型。
- 精度与边界：两候选各5323配置逐位通过、官方sample通过、平台可见本项Pass；严格iters/原求和次序/Div保留。纯负零整输入不替代原始归约微测；隐藏项不外推。
- 证据与停止：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_pipe_interleave_member2_5/final_audit.json、selection_before_R05.json、confirmation.json；member2本轮新增5次、今日24/50后停止，不自动续交。


## 2026-10-24T17:02:43.959378+08:00 — three_methods_member2_10_R01

- 方法：baseline，SHA 70a206311bc5abdead20442e38e415855e14d36ab0ca818f058e77ec8195192d；公共约束和验证见整体history同轮。
- A2本项 133.93 μs；平台 Pass；当前决定 baseline，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/R01/comparison.json，提交 6adc740b1dac5d235ba54506；预算 1/10，隐藏项不外推。


## 2026-10-24T17:09:18.128762+08:00 — three_methods_member2_10_R02

- 方法：candidate，SHA f4c42295d086186b4ead5a248759467de32c89ab9755a0667e1137dea0402e75；公共约束和验证见整体history同轮。
- A2本项 0 μs；平台 Fail；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/R02/comparison.json，提交 6adc75a41dac5d235ba6553c；预算 2/10，隐藏项不外推。


## 2026-10-24T17:13:46.297071+08:00 — three_methods_member2_10_R03

- 方法：candidate，SHA bb54a6c7533e76e048ee64363ff196d3c222da87ef1b753711aa0dee03efd848；公共约束和验证见整体history同轮。
- A2本项 135.94 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/R03/comparison.json，提交 6adc76a11dac5d235ba6e265；预算 3/10，隐藏项不外推。


## 2026-10-24T17:17:58.099680+08:00 — three_methods_member2_10_R04

- 方法：candidate，SHA 7dfa7dc0f964d752eebd346537f02a59dbd0b67a641b78c93af3c943d697f9e5；公共约束和验证见整体history同轮。
- A2本项 137.56 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/R04/comparison.json，提交 6adc779d1dac5d235ba7a3d1；预算 4/10，隐藏项不外推。


## 2026-10-24T17:22:17.432152+08:00 — three_methods_member2_10_R05

- 方法：baseline_control，SHA 70a206311bc5abdead20442e38e415855e14d36ab0ca818f058e77ec8195192d；公共约束和验证见整体history同轮。
- A2本项 134.73 μs；平台 Pass；当前决定 baseline_control，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/R05/comparison.json，提交 6adc78a01dac5d235ba86cbe；预算 5/10，隐藏项不外推。


## 2026-10-24T17:27:15.332410+08:00 — three_methods_member2_10_R06

- 方法：candidate，SHA 1242f8042b4abcab0a182352681a877c7b9d3fe463c8d021c541bb756ae5619e；公共约束和验证见整体history同轮。
- A2本项 129.34 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/R06/comparison.json，提交 6adc79ca1dac5d235ba97ade；预算 6/10，隐藏项不外推。


## 2026-10-24T17:30:47.750541+08:00 — three_methods_member2_10_R07

- 方法：candidate，SHA 213549a81aed766f4da5e41b9f979a84acb991966c54ec89621c8f6743fe31f5；公共约束和验证见整体history同轮。
- A2本项 136.32 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/R07/comparison.json，提交 6adc7a9f1dac5d235baa13cc；预算 7/10，隐藏项不外推。


## 2026-10-24T17:36:28.666410+08:00 — three_methods_member2_10_R08

- 方法：candidate，SHA 0af5c23189e8a50e0a148e10d74930a70833a140a53f84789dfc8c4b75eae9d5；公共约束和验证见整体history同轮。
- A2本项 129.81 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/R08/comparison.json，提交 6adc7bf41dac5d235baaf097；预算 8/10，隐藏项不外推。


## 2026-10-24T17:40:00.384210+08:00 — three_methods_member2_10_R09

- 方法：repeat，SHA 0af5c23189e8a50e0a148e10d74930a70833a140a53f84789dfc8c4b75eae9d5；公共约束和验证见整体history同轮。
- A2本项 126.61 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/R09/comparison.json，提交 6adc7cc71dac5d235bab632c；预算 9/10，隐藏项不外推。


## 2026-10-24T17:43:33.134953+08:00 — three_methods_member2_10_R10

- 方法：confirm，SHA 0af5c23189e8a50e0a148e10d74930a70833a140a53f84789dfc8c4b75eae9d5；公共约束和验证见整体history同轮。
- A2本项 128.18 μs；平台 Pass；当前决定 confirmation_pending_audit，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/R10/comparison.json，提交 6adc7d9c1dac5d235babe41b；预算 10/10，隐藏项不外推。


## 2026-10-24T17:44:20.992431+08:00 — member2_three_methods_final10_20261024

- 十次观测：[('R01', 'baseline', 133.93, 'Pass'), ('R02', 'tpipe_interleave', 0, 'Fail'), ('R03', 'rowdiv_panel', 135.94, 'Pass'), ('R04', 'ownership', 137.56, 'Pass'), ('R05', 'baseline control', 134.73, 'Pass'), ('R06', 'metadata', 129.34, 'Pass'), ('R07', 'combined_q1panel', 136.32, 'Pass'), ('R08', 'full_combined_metadata', 129.81, 'Pass'), ('R09', 'repeat selected source', 126.61, 'Pass'), ('R10', 'confirm selected source', 128.18, 'Pass')] us；R01/R05参照 134.3294044504031 us。case编号仅组织记录，形状和路径未由计时反推。
- 保留决定：R08，SHA 0af5c23189e8a50e0a148e10d74930a70833a140a53f84789dfc8c4b75eae9d5；同源码有效观测中位数 128.18 us，相对参照 下降 4.578%。整体采用依据见history同轮，不采用不同源码单点最小值拼接。
- 最终确认：R10本项 128.18 us，源码SHA 0af5c23189e8a50e0a148e10d74930a70833a140a53f84789dfc8c4b75eae9d5；确认通过=True，active_equals_latest_server=True。R10确认的服务器源码与保留源码一致。
- 精度与边界：非父版提交绑定独立strict-bits、编译和A3设备执行manifest，官方sample均通过；本项平台逐轮状态见回执。严格iters/原求和次序/Div及所有权检查的具体覆盖以 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/validation_summary.json 为准，未测范围和隐藏十项不外推。
- 经验与停止：所有权独立R04=137.56us，对照=134.3294044504031us（上升 2.405%）；组合及最终复测同时检查此项，不能只因case3更快就忽略本项退化。 本项变化是整体平台观测，缺少本版本A2阶段profile时不能认定具体阶段占比或因果。证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_three_methods_member2_10/final_audit.json、confirmation.json及各comparison；member2新增10次、今日34/50后停止，禁止第11次POST。


## 2026-10-24T18:13:07.228296+08:00 — colpanel_member2_10_R01

- 方法：candidate，SHA ede5d8c71f8915e211af973cf3d1fc548f337fed7f80c37f88fda714fcb57ca2；公共约束和验证见整体history同轮。
- A2本项 0 μs；平台 Fail；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R01/comparison.json，提交 6adc84991dac5d235bafa3e6；预算 1/10，隐藏项不外推。


## 2026-10-24T18:17:15.463949+08:00 — colpanel_member2_10_R02

- 方法：candidate，SHA 41256f032ffdc525cbbb994a5fa6739bd66f6ab2694dce0868df0b2abb1e0e22；公共约束和验证见整体history同轮。
- A2本项 135.69 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R02/comparison.json，提交 6adc85821dac5d235bb020c5；预算 2/10，隐藏项不外推。


## 2026-10-24T18:21:57.377014+08:00 — colpanel_member2_10_R03

- 方法：candidate，SHA 27676576450024bc6f7fd8d9afdf50150052a0d9ea2d9496d2d4478a63de04d6；公共约束和验证见整体history同轮。
- A2本项 127.21 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
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
- A2本项 134.56 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R06/comparison.json，提交 6adc89ed1dac5d235bb2d71e；预算 6/10，隐藏项不外推。


## 2026-10-24T18:39:38.307793+08:00 — colpanel_member2_10_R07

- 方法：repeat，SHA ede5d8c71f8915e211af973cf3d1fc548f337fed7f80c37f88fda714fcb57ca2；公共约束和验证见整体history同轮。
- A2本项 140.28 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R07/comparison.json，提交 6adc8ac11dac5d235bb35c8d；预算 7/10，隐藏项不外推。


## 2026-10-24T18:51:16.958949+08:00 — colpanel_member2_10_R08

- 方法：candidate，SHA 7245667081bd0341dd614d86b3abc1f48e00ce5c0191da9a3d6c4ec8ef06d161；公共约束和验证见整体history同轮。
- A2本项 136.65 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R08/comparison.json，提交 6adc8d7c1dac5d235bb51919；预算 原始 8/16，有效 5/10，本次平台失败补偿 False，member2 daily50硬上限，隐藏项不外推。


## 2026-10-24T18:54:34.939384+08:00 — colpanel_member2_10_R09

- 方法：repeat，SHA 3256f2a28bdc3a52ff446ce39f6f12f3c1c11a53b768238f5d2c46fe3bee0802；公共约束和验证见整体history同轮。
- A2本项 0 μs；平台 Fail；当前决定 platform_failure_compensated，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R09/comparison.json，提交 6adc8e511dac5d235bb5add2；预算 原始 9/16，有效 5/10，本次平台失败补偿 True，member2 daily50硬上限，隐藏项不外推。


## 2026-10-24T19:00:58.161358+08:00 — colpanel_member2_10_R10

- 方法：candidate，SHA 91b9aee73eec356f845aa36f4c2e1fa36c8dea5e42009b31eba16262783e2555；公共约束和验证见整体history同轮。
- A2本项 126.28 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
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
- A2本项 135.46 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R13/comparison.json，提交 6adc923a1dac5d235bb82221；预算 原始 13/16，有效 7/10，本次平台失败补偿 False，member2 daily50硬上限，隐藏项不外推。


## 2026-10-24T19:14:48.959947+08:00 — colpanel_member2_10_R14

- 方法：repeat，SHA 91b9aee73eec356f845aa36f4c2e1fa36c8dea5e42009b31eba16262783e2555；公共约束和验证见整体history同轮。
- A2本项 0 μs；平台 Fail；当前决定 platform_failure_compensated，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R14/comparison.json，提交 6adc930f1dac5d235bb8ad5a；预算 原始 14/16，有效 7/10，本次平台失败补偿 True，member2 daily50硬上限，隐藏项不外推。


## 2026-10-24T19:18:35.891050+08:00 — colpanel_member2_10_R15

- 方法：repeat，SHA 91b9aee73eec356f845aa36f4c2e1fa36c8dea5e42009b31eba16262783e2555；公共约束和验证见整体history同轮。
- A2本项 126.6 μs；平台 Pass；当前决定 recorded_pending_comparison，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R15/comparison.json，提交 6adc93e31dac5d235bb92d3e；预算 原始 15/16，有效 8/10，本次平台失败补偿 False，member2 daily50硬上限，隐藏项不外推。


## 2026-10-24T19:21:53.867194+08:00 — colpanel_member2_10_R16

- 方法：confirm，SHA 91b9aee73eec356f845aa36f4c2e1fa36c8dea5e42009b31eba16262783e2555；公共约束和验证见整体history同轮。
- A2本项 0 μs；平台 Fail；当前决定 confirmation_pending_audit，不将单项最低值当作最终采用版本。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/R16/comparison.json，提交 6adc94b81dac5d235bb9bf59；预算 原始 16/16，有效 8/10，本次平台失败补偿 True，member2 daily50硬上限，隐藏项不外推。


## 2026-10-24T19:22:52.089402+08:00 — member2_colpanel_final10_20261024

- 原始 16 次回执：[('R01', 'column_panel', 0, 'Fail', 'compensated'), ('R02', 'div_mask', 135.69, 'Pass', 'effective'), ('R03', 'softmax_dense', 127.21, 'Pass', 'effective'), ('R04', 'column_q1_minimal', 0, 'Fail', 'compensated'), ('R05', 'div_full_only', 0, 'Fail', 'compensated'), ('R06', 'softmax_dense_sub', 134.56, 'Pass', 'effective'), ('R07', 'column_panel', 140.28, 'Pass', 'effective'), ('R08', 'column_q1_intcopy', 136.65, 'Pass', 'effective'), ('R09', 'div_full_only', 0, 'Fail', 'compensated'), ('R10', 'softmax_dense_costguard', 126.28, 'Pass', 'effective'), ('R11', 'repeat selected source', 0, 'Fail', 'compensated'), ('R12', 'repeat selected source', 0, 'Fail', 'compensated'), ('R13', 'repeat selected source', 135.46, 'Pass', 'effective'), ('R14', 'repeat selected source', 0, 'Fail', 'compensated'), ('R15', 'repeat selected source', 126.6, 'Pass', 'effective'), ('R16', 'confirm selected source', 0, 'Fail', 'compensated')] us；参考前轮同SHA三次中位数 128.18 us，本轮无新控制；编号不代表shape。平台失败清单 ['R01', 'R04', 'R05', 'R09', 'R11', 'R12', 'R14', 'R16']，共 8 次；来源为用户确认及通用授权“失败请求可以补额度，遇到submission failed就补一次额度”，无独立平台阶段日志佐证。每次仍占每日原始额度并完整审计；精确匹配回执从有效目标和性能统计排除。
- 保留：BASELINE，SHA 0af5c23189e8a50e0a148e10d74930a70833a140a53f84789dfc8c4b75eae9d5；前轮参考中位数 128.18 us，相对 持平 0.000%；整体条件见history，不拼接单点最优。
- 最终确认：成功confirm []，最后原始 R16 本项 0 us，SHA 91b9aee73eec356f845aa36f4c2e1fa36c8dea5e42009b31eba16262783e2555；确认通过=False。最后原始轮次 R16 后回退父版；active与平台latest源码不同，没有为修正latest追加POST。
- 精度边界：非父版绑定0af5 strict-bits/编译/A3设备manifest，全部原始sample通过；A2状态见回执。严格iters/原求和次序/Div/所有权证据见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/validation_summary.json；不外推隐藏十项。
- 经验停止：case3改善须同时看本项；通用资源守卫不按case编号分派。 member2本轮原始 16/16，平台失败补偿 8，有效 8/10，今日 34→50/50；停止原因 daily_hard_cap_reached，有效目标达成=False。STOP已写，无未确认POST，停止后不再提交或自动继续。 证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_colpanel_member2_10/final_audit.json、confirmation.json及全部comparison。 补充已确认的候选观察：91b9成本门槛版R10/R15本项两次Pass为[126.28, 126.6] us，中位数 126.44 us，相对旧参考变化 -1.357%；R16平台失败导致缺少第三次成功及成功confirm，未保留并不表示本项代码失败。完整候选路径和逐版结论见总体history。


## 2026-10-24T20:05:39.846921+08:00 — parallel_member3_R01

- 分支A，SHA c4c07d7fa3fcd1bc99e0b1608db568971970743608f21d7038042102ab464173；约束与验证见整体history同轮。
- 本项 124.54 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R01/comparison.json，提交 6adc9eeb1dac5d235bc07de4。


## 2026-10-24T20:11:55.505707+08:00 — parallel_member3_R02

- 分支C，SHA b4f53e1f5820c25568d73eec67bf2cc93b4d10a4ab0fe37987f57eb1fe548bd2；约束与验证见整体history同轮。
- 本项 125.06 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R02/comparison.json，提交 6adca0631dac5d235bc18e97。


## 2026-10-24T20:16:37.140920+08:00 — parallel_member3_R03

- 分支B，SHA f2eca44b52fb44edc9f0cf31086e250324deb0120eef174acc5daa83f9980b65；约束与验证见整体history同轮。
- 本项 0 μs，A2 Fail；平台失败补偿 True，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R03/comparison.json，提交 6adca18b1dac5d235bc24f99。


## 2026-10-24T20:20:25.034146+08:00 — parallel_member3_R04

- 分支B，SHA f2eca44b52fb44edc9f0cf31086e250324deb0120eef174acc5daa83f9980b65；约束与验证见整体history同轮。
- 本项 125.29 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R04/comparison.json，提交 6adca2601dac5d235bc2cf19。


## 2026-10-24T20:23:58.519175+08:00 — parallel_member3_R05

- 分支A，SHA 19ff0a69a2e644d442b8a40a792c2628bdc4c78fff688d8e7000a0774ee2fdfb；约束与验证见整体history同轮。
- 本项 128.14 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R05/comparison.json，提交 6adca3351dac5d235bc35285。


## 2026-10-24T20:27:25.305700+08:00 — parallel_member3_R06

- 分支B，SHA d9d09774380da89f4fb9bf918f6f8015f9978f50624af58eaa2f0acaa4302071；约束与验证见整体history同轮。
- 本项 0 μs，A2 Fail；平台失败补偿 True，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R06/comparison.json，提交 6adca4091dac5d235bc3e229。


## 2026-10-24T20:31:03.358069+08:00 — parallel_member3_R07

- 分支B，SHA d9d09774380da89f4fb9bf918f6f8015f9978f50624af58eaa2f0acaa4302071；约束与验证见整体history同轮。
- 本项 132.83 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R07/comparison.json，提交 6adca4de1dac5d235bc46d7a。


## 2026-10-24T20:34:36.526804+08:00 — parallel_member3_R08

- 分支C，SHA 985def93a6fd8953a6a8051d9de8971c48ac0f458b74607dbc813384e019f8ef；约束与验证见整体history同轮。
- 本项 132.42 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R08/comparison.json，提交 6adca5b41dac5d235bc50172。


## 2026-10-24T20:38:09.272308+08:00 — parallel_member3_R09

- 分支A，SHA 924c58ae542c952306af7b6ade561dbe42ebcc6e6fcdc1bcf86d726656ab69e6；约束与验证见整体history同轮。
- 本项 124.42 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R09/comparison.json，提交 6adca6881dac5d235bc5890a。


## 2026-10-24T20:41:41.095574+08:00 — parallel_member3_R10

- 分支B，SHA 3507c71a25a5e204010ecad1bc21a147954614f72ebf805d8fb3b04bfa72ab49；约束与验证见整体history同轮。
- 本项 125.11 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R10/comparison.json，提交 6adca75c1dac5d235bc614d0。


## 2026-10-24T20:45:13.230159+08:00 — parallel_member3_R11

- 分支C，SHA 0d11fbacfa1b7d5bf33af9d0c82f3bcc40db17d07df092bd602ac280d4361775；约束与验证见整体history同轮。
- 本项 126.83 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R11/comparison.json，提交 6adca8301dac5d235bc68c6e。


## 2026-10-24T20:48:45.000914+08:00 — parallel_member3_R12

- 分支A，SHA 924c58ae542c952306af7b6ade561dbe42ebcc6e6fcdc1bcf86d726656ab69e6；约束与验证见整体history同轮。
- 本项 126.69 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R12/comparison.json，提交 6adca9041dac5d235bc71e95。


## 2026-10-24T20:52:01.657790+08:00 — parallel_member3_R13

- 分支B，SHA 3507c71a25a5e204010ecad1bc21a147954614f72ebf805d8fb3b04bfa72ab49；约束与验证见整体history同轮。
- 本项 0 μs，A2 Fail；平台失败补偿 True，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R13/comparison.json，提交 6adca9d81dac5d235bc79984。


## 2026-10-24T20:55:48.789461+08:00 — parallel_member3_R14

- 分支B，SHA 3507c71a25a5e204010ecad1bc21a147954614f72ebf805d8fb3b04bfa72ab49；约束与验证见整体history同轮。
- 本项 125.87 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R14/comparison.json，提交 6adcaaac1dac5d235bc8259a。


## 2026-10-24T20:59:21.593061+08:00 — parallel_member3_R15

- 分支C，SHA b4f53e1f5820c25568d73eec67bf2cc93b4d10a4ab0fe37987f57eb1fe548bd2；约束与验证见整体history同轮。
- 本项 134.1 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R15/comparison.json，提交 6adcab811dac5d235bc8a51e。


## 2026-10-24T21:02:54.363493+08:00 — parallel_member3_R16

- 分支B，SHA 3507c71a25a5e204010ecad1bc21a147954614f72ebf805d8fb3b04bfa72ab49；约束与验证见整体history同轮。
- 本项 127.11 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R16/comparison.json，提交 6adcac551dac5d235bc92c45。


## 2026-10-24T21:06:26.041076+08:00 — parallel_member3_R17

- 分支C，SHA 0d11fbacfa1b7d5bf33af9d0c82f3bcc40db17d07df092bd602ac280d4361775；约束与验证见整体history同轮。
- 本项 125.48 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R17/comparison.json，提交 6adcad291dac5d235bc9b25d。


## 2026-10-24T21:09:58.027296+08:00 — parallel_member3_R18

- 分支A，SHA 924c58ae542c952306af7b6ade561dbe42ebcc6e6fcdc1bcf86d726656ab69e6；约束与验证见整体history同轮。
- 本项 126.91 μs，A2 Pass；平台失败补偿 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/R18/comparison.json，提交 6adcadfd1dac5d235bca32c5。


## 2026-10-24T21:13:09.146962+08:00 — parallel_member3_3x5_FINAL_20261024

- 本轮公共方法/完整SHA/验证见整体history同标记；最终A/v3 `924c58ae542c952306af7b6ade561dbe42ebcc6e6fcdc1bcf86d726656ab69e6`，严格iters、原求和次序和Div。
- 本项同SHA三次中位数 126.690µs；旧父版历史参考 126.440µs，耗时变化 +0.198%。最新确认本项 126.91µs；没有新增同期基线。
- 各路最终候选本项中位数 {'A': 126.69, 'B': 125.29, 'C': 126.155}；不拼接各候选最低值。保留版中位数略高于历史参考但在2%守卫内；未为追逐case3牺牲明显case5回退。
- 决定：保留全局A/v3，三路各5次有效已停；隐藏十项细节未知。证据 `/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/REPORT.md` 和 `/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_parallel_member3_3x5/final_analysis.json`；最新提交 `6adcadfd1dac5d235bca32c5`。



## 2026-10-24T21:28:13.482985+08:00 — local_A3_perf_once_local_perf_20261024T132308Z_924c58ae

- 当前最佳源码SHA `924c58ae542c952306af7b6ade561dbe42ebcc6e6fcdc1bcf86d726656ab69e6`，本地A3单次会话；生产kernel未修改、没有A2提交。
- workload B/S/H/iters=8/32/34/20来自历史探针，eps1e-6和输入uniform[-2,2]为本地假设，不作为生产专用分派依据。
- A2同源码三次历史中位数 126.69µs；A3记录30次中位数 116.88µs，范围115.96–117.94µs，A3耗时变化-7.74%。不能归因纯芯片或当作同期配对结果。
- 五组校验与原始CSV见 `/mnt/workspace/enjoy_ur_time/others/local_perf_20261024T132308Z_924c58ae/REPORT.md` 和comparison.json；本轮只做一次本地测评，NPU锁释放，提交STOP保持。



## 2026-10-24T22:08:04.901153+08:00 — cases345_max_member3_R01

- 分支A，SHA ddec95e49e566a246dab41b1c301ba2c7211cb9c82c6ab5b6be75bf0fd8bfe6c；约束与验证见整体history同轮。
- 本项 132.31 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R01/comparison.json，提交 6adcbb9c1dac5d235bd2ea25。


## 2026-10-24T22:12:27.589595+08:00 — cases345_max_member3_R02

- 分支C，SHA 1bc3e59e4a62f9714669e9a4c092e1397b6e27128b52f07542e311b8fb704366；约束与验证见整体history同轮。
- 本项 0 μs，A2 Fail；平台失败补偿 False，平台失败 True，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R02/comparison.json，提交 6adcbcb21dac5d235bd3a127。


## 2026-10-24T22:17:48.275114+08:00 — cases345_max_member3_R03

- 分支C，SHA 1bc3e59e4a62f9714669e9a4c092e1397b6e27128b52f07542e311b8fb704366；约束与验证见整体history同轮。
- 本项 107.42 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R03/comparison.json，提交 6adcbde31dac5d235bd46196。


## 2026-10-24T22:21:05.068090+08:00 — cases345_max_member3_R04

- 分支A，SHA 44d7468872b70f18b3626d8861f940aafb945a940f984e8f33651dd10bbba722；约束与验证见整体history同轮。
- 本项 0 μs，A2 Fail；平台失败补偿 False，平台失败 True，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R04/comparison.json，提交 6adcbeb71dac5d235bd4e9e1。


## 2026-10-24T22:24:58.110910+08:00 — cases345_max_member3_R05

- 分支A，SHA 44d7468872b70f18b3626d8861f940aafb945a940f984e8f33651dd10bbba722；约束与验证见整体history同轮。
- 本项 134.4 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R05/comparison.json，提交 6adcbf8c1dac5d235bd56f24。


## 2026-10-24T22:29:06.701136+08:00 — cases345_max_member3_R06

- 分支A，SHA 172977f03347d73b5c651020e2a7fd8a5d25450f205b5e62d5e7f5db3f87e8e5；约束与验证见整体history同轮。
- 本项 128 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R06/comparison.json，提交 6adcc08a1dac5d235bd60e6b。


## 2026-10-24T22:34:08.713852+08:00 — cases345_max_member3_R07

- 分支C，SHA 1cbd576d3adbab76ea8c52b6aac43437297819e26ac5b49aa6f85bc4bb6578fe；约束与验证见整体history同轮。
- 本项 110.48 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R07/comparison.json，提交 6adcc1b31dac5d235bd6e585。


## 2026-10-24T22:40:57.379814+08:00 — cases345_max_member3_R08

- 分支B，SHA bf04826db0b6f59abba7460c845e308de95b25bb4462358a3f649ad9ff23861a；约束与验证见整体history同轮。
- 本项 127.26 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R08/comparison.json，提交 6adcc3501dac5d235bd8152d。


## 2026-10-24T22:44:30.189549+08:00 — cases345_max_member3_R09

- 分支A，SHA aebb7faf77b915fa459a7f996606571af9d534fbcd5dc0263306a7cdc26918a1；约束与验证见整体history同轮。
- 本项 137.15 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R09/comparison.json，提交 6adcc4251dac5d235bd8a7b1。


## 2026-10-24T22:50:54.714792+08:00 — cases345_max_member3_R10

- 分支A，SHA aebb7faf77b915fa459a7f996606571af9d534fbcd5dc0263306a7cdc26918a1；约束与验证见整体history同轮。
- 本项 132.29 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R10/comparison.json，提交 6adcc5a61dac5d235bd9bbc4。


## 2026-10-24T22:59:45.324153+08:00 — cases345_max_member3_R11

- 分支C，SHA d117c6ecc8b2ea1b206ccfca0af45a3ac67bf0991204b7854deb32731cce8632；约束与验证见整体history同轮。
- 本项 102.08 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R11/comparison.json，提交 6adcc7b81dac5d235bdb4fc9。


## 2026-10-24T23:03:22.754833+08:00 — cases345_max_member3_R12

- 分支B，SHA adc8b8d677b3c5fa3eb270cc6103efd9e9bfa6665d437b0c538d7d1c165cdfc9；约束与验证见整体history同轮。
- 本项 125.51 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R12/comparison.json，提交 6adcc88d1dac5d235bdc0db8。


## 2026-10-24T23:06:49.482580+08:00 — cases345_max_member3_R13

- 分支C，SHA 680ac58779f099d252beae0a1fc2089c7266bec1fd07f04da830f3dd9053106a；约束与验证见整体history同轮。
- 本项 79.26 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R13/comparison.json，提交 6adcc9611dac5d235bdcc633。


## 2026-10-24T23:10:22.208871+08:00 — cases345_max_member3_R14

- 分支C，SHA 680ac58779f099d252beae0a1fc2089c7266bec1fd07f04da830f3dd9053106a；约束与验证见整体history同轮。
- 本项 79.53 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R14/comparison.json，提交 6adcca351dac5d235bdd5c17。


## 2026-10-24T23:15:15.407819+08:00 — cases345_max_member3_R15

- 分支M，SHA 21dab72f389edddfafc7531de172f86957ae3e5f270be750b31e5dba529ef096；约束与验证见整体history同轮。
- 本项 94.02 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R15/comparison.json，提交 6adccb5a1dac5d235bde897f。


## 2026-10-24T23:18:52.882580+08:00 — cases345_max_member3_R16

- 分支M，SHA 21dab72f389edddfafc7531de172f86957ae3e5f270be750b31e5dba529ef096；约束与验证见整体history同轮。
- 本项 93.4 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R16/comparison.json，提交 6adccc2f1dac5d235bdf2b25。


## 2026-10-24T23:23:30.524029+08:00 — cases345_max_member3_R17

- 分支C，SHA 680ac58779f099d252beae0a1fc2089c7266bec1fd07f04da830f3dd9053106a；约束与验证见整体history同轮。
- 本项 79.01 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/R17/comparison.json，提交 6adccd4a1dac5d235bdfde6a。


## 2026-10-24T23:30:08.945616+08:00 — cases345_max_member3_final_C6

- 方法/经验：Div成本门槛面板、q8、padding独立列lane逐步改善。C6三次A2=79.26/79.53/79.01µs；融合94.02/93.40µs。真实H归约/store隔离padding，零/负eps和NaN逐位与guard通过，最终保留C6。
- A2同源码中位：C6 79.2600µs，融合 93.7100µs，原基线 126.6900µs；最新确认79.01µs。
- 保留：用户选择C6，SHA 680ac58779f099d252beae0a1fc2089c7266bec1fd07f04da830f3dd9053106a；提交6adccd4a1dac5d235bdfde6a。本轮原始17/32，M2/2完成，失败计数，停止续交；隐藏十项未知。
- 证据：C6 10635设备配置执行含1008 holdout全逐位通过，guard/unwritten/input_changes为0；[完整报告](/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/REPORT.md)、[最终选用](/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261024_cases345_member3_max_32/final_selection.json)。


## 2026-10-25T00:10:18.370921+08:00 — cases145_max_member1_20261025_R01

- 分支M，SHA 680ac58779f099d252beae0a1fc2089c7266bec1fd07f04da830f3dd9053106a；约束与验证见整体history同轮。
- 本项 78.99 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R01/comparison.json，提交 6adcd8411dac5d235be77d01。


## 2026-10-25T00:22:59.256150+08:00 — cases145_max_member1_20261025_R02

- 分支D，SHA 57a3f2a87e99c94111e2fbf74da4f382d7a4fe1b147d03278aaa1a2731921245；约束与验证见整体history同轮。
- 本项 79.24 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R02/comparison.json，提交 6adcdb3a1dac5d235be9d4d8。


## 2026-10-25T00:29:37.120625+08:00 — cases145_max_member1_20261025_R03

- 分支C，SHA 17bcdfa9031bab1473eb0508c0756413bd627280a064bd26fe3a1e8ec3a3a07b；约束与验证见整体history同轮。
- 本项 80.14 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R03/comparison.json，提交 6adcdcc31dac5d235bead09f。


## 2026-10-25T00:32:41.852976+08:00 — cases145_max_member1_20261025_R04

- 分支B，SHA 13da845bd6428bd54a221618bedd83cfbea235a797c39b878762abcec78415b3；约束与验证见整体history同轮。
- 本项 82.24 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R04/comparison.json，提交 6adcdd811dac5d235beb583e。


## 2026-10-25T00:37:27.022071+08:00 — cases145_max_member1_20261025_R05

- 分支D，SHA d5e6b51003bd92dd03282e8b799007835110bf397413fa5e9d2113c7ac6e2217；约束与验证见整体history同轮。
- 本项 79.11 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R05/comparison.json，提交 6adcde991dac5d235bec2160。


## 2026-10-25T00:41:44.288049+08:00 — cases145_max_member1_20261025_R06

- 分支B，SHA f3e47ee4a9424579cafb6723c550bba373e4d025cee9591ae3527b66a724e4db；约束与验证见整体history同轮。
- 本项 78.29 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R06/comparison.json，提交 6adcdf9f1dac5d235becda91。


## 2026-10-25T00:51:05.979518+08:00 — cases145_max_member1_20261025_R07

- 分支C，SHA 4e995cb2850a3473d2ce2ea0af5b40199d3fd5675f3d6c79840d07c2fcf135fa；约束与验证见整体history同轮。
- 本项 82.27 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R07/comparison.json，提交 6adce1c71dac5d235bee8021。


## 2026-10-25T00:54:57.725830+08:00 — cases145_max_member1_20261025_R08

- 分支B，SHA f8a672bbcff3400593b795f172fedc290a5d2cec3377c87ac5cc1e960e1f2af4；约束与验证见整体history同轮。
- 本项 80.16 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R08/comparison.json，提交 6adce2b91dac5d235bef5cb8。


## 2026-10-25T01:06:30.198238+08:00 — cases145_max_member1_20261025_R09

- 分支D，SHA f1f310bd2bfcf3906aa898b34096ae9c2524f8c963e3847f177f631d5bc23d93；约束与验证见整体history同轮。
- 本项 79.45 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R09/comparison.json，提交 6adce56d1dac5d235bf1110e。


## 2026-10-25T01:10:49.994077+08:00 — cases145_max_member1_20261025_R10

- 分支B，SHA 12b01f4c87a01c609aa3ae132203bf43a50e3e361b9346f781e8030587e693b9；约束与验证见整体history同轮。
- 本项 86.84 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R10/comparison.json，提交 6adce66c1dac5d235bf1a51b。


## 2026-10-25T01:14:09.247285+08:00 — cases145_max_member1_20261025_R11

- 分支D，SHA 9c87bf37552adfc1c325a99da772fb563ae224e7fc654f88acf40ed75b8f899e；约束与验证见整体history同轮。
- 本项 79.65 μs，A2 Pass；平台失败补偿 False，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R11/comparison.json，提交 6adce7331dac5d235bf226f9。


## 2026-10-25 — cases145_max_member1_R12_HTTP429_HOLD

- C4候选f113a769的fresh19suite/holdout与A3 ABBA通过；POST明确HTTP429拒绝，无SID，不重发、不换账号、不补尝试。
- raw12=accepted11+rejected1；D4/14、B4/14、C3/14、M1/8，三个分支尚未到7次中评。
- 本地doctor原按CST统计本日11，而live UTC当日及滚动24h均50(旧39+新11)；这与429一致，但服务端精确重置算法未公布，不能把CST跨日当额度已重置。
- 已设置本轮SUBMIT_HOLD并修正提交入口拦截；继续CPU及串行A3验证，最终A2融合/保留待额度真正恢复。证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/quota_429_audit.json；/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R12/comparison.json。


## 2026-10-25T01:32:39.557571+08:00 — cases145_max_member1_20261025_R13

- 分支C，SHA f113a769b1cf3d514aa075de4219fdbd955d8898f883cfd6f6b7fe6d4c245880；约束与验证见整体history同轮。
- 本项 83.59 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R13/comparison.json，提交 6adceb8a1dac5d235bf4ef19。


## 2026-10-25T01:35:34.733093+08:00 — cases145_max_member1_20261025_R14

- 分支B，SHA 8efe54ba6cd2c2dd4f77aa1d4873f4d56258ead1618d7f42859d68edd4a8783a；约束与验证见整体history同轮。
- 本项 88.9 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R14/comparison.json，提交 6adcec3e1dac5d235bf561f0。


## 2026-10-25T01:39:30.135164+08:00 — cases145_max_member1_20261025_R15

- 分支D，SHA 06e778648b3fbddacc5720e595a14e51caac8d6ab27f6c39dbe5514a3e3ecb24；约束与验证见整体history同轮。
- 本项 79.42 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R15/comparison.json，提交 6adced291dac5d235bf5f576。


## 2026-10-25T01:46:59.707753+08:00 — cases145_max_member1_20261025_R17

- 分支D，SHA f77cc8fa5461943ab111370f430bb2df715c86b10d63e8d2ad7626e1c682bf4e；约束与验证见整体history同轮。
- 本项 86.64 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R17/comparison.json，提交 6adceeeb1dac5d235bf72397。


## 2026-10-25T01:57:02.170458+08:00 — cases145_max_member1_20261025_R18

- 分支D，SHA 9c87bf37552adfc1c325a99da772fb563ae224e7fc654f88acf40ed75b8f899e；约束与验证见整体history同轮。
- 本项 79.32 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R18/comparison.json，提交 6adcf1451dac5d235bf8ac88。


## 2026-10-25T02:00:29.601221+08:00 — cases145_max_member1_20261025_R19

- 分支B，SHA ae862a6bae960c4be49e12b4f849f9f1675e27fce89c64348d7fbb69aa7b4a43；约束与验证见整体history同轮。
- 本项 86.87 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R19/comparison.json，提交 6adcf2151dac5d235bf93325。


## 2026-10-25T02:04:02.748948+08:00 — cases145_max_member1_20261025_R20

- 分支B，SHA f3e47ee4a9424579cafb6723c550bba373e4d025cee9591ae3527b66a724e4db；约束与验证见整体history同轮。
- 本项 78.33 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R20/comparison.json，提交 6adcf2e51dac5d235bf9ca86。


## 2026-10-25T02:07:30.173349+08:00 — cases145_max_member1_20261025_R21

- 分支D，SHA a0bc1f2d62258843738a0db76351fd73f081b4b2c2d4b014c080ef2051324f1c；约束与验证见整体history同轮。
- 本项 92.78 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R21/comparison.json，提交 6adcf3b41dac5d235bfa551c。


## 2026-10-25T02:11:19.768897+08:00 — cases145_max_member1_20261025_R22

- 分支C，SHA 680ac58779f099d252beae0a1fc2089c7266bec1fd07f04da830f3dd9053106a；约束与验证见整体history同轮。
- 本项 81.05 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R22/comparison.json，提交 6adcf49a1dac5d235bfaf0ff。


## 2026-10-25 面板诊断 — cases145_C_pre_midpoint

- C/v5紧凑分母8列Div虽然减少总repeat，A3完整case5反而约+4.27%，未认定为优化。
- C/v6只移动既有full-row Div分母面板的物理相位，不改q/owner/FP32轨迹/Div；fresh19（含1008holdout）通过，完整A3 case5 ratio0.999712，暂无明确收益。
- 独立UB边界设备诊断9组全部通过，包括实际共同UB上限、阈值-1/0/+1、q/valid/split/tail、eps0/负数/负零和NaN payload。低预算跳过单独计数，不算通过配置；二进制f47b5e5624199d8253cc38e0c2d632ffb867c653c53f991c767947ee75f104f4。
- 在近时原C6控制下做一次A2 ABBA架构假设测量后再复盘。证据：C/ub_boundary_v6/parent_execution.json、中央performance/C_v6_5244c778c747/comparison.json、R22。


## 2026-10-25T02:17:59.689058+08:00 — cases145_max_member1_20261025_R23

- 分支C，SHA 5244c778c74719b0e4f23138a9c46480ef729eb9d5bfe8dfe4925e66577b711a；约束与验证见整体history同轮。
- 本项 87.06 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R23/comparison.json，提交 6adcf62f1dac5d235bfc07ac。


## 2026-10-25T02:21:26.439973+08:00 — cases145_max_member1_20261025_R24

- 分支C，SHA 5244c778c74719b0e4f23138a9c46480ef729eb9d5bfe8dfe4925e66577b711a；约束与验证见整体history同轮。
- 本项 86.96 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R24/comparison.json，提交 6adcf6fe1dac5d235bfc9301。


## 2026-10-25T02:24:53.196004+08:00 — cases145_max_member1_20261025_R25

- 分支C，SHA 680ac58779f099d252beae0a1fc2089c7266bec1fd07f04da830f3dd9053106a；约束与验证见整体history同轮。
- 本项 87.81 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
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
- 本项 93.35 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R27/comparison.json，提交 6adcfa861dac5d235bfeee28。


## 2026-10-25T02:39:57.724663+08:00 — cases145_max_member1_20261025_R28

- 分支B，SHA f3e47ee4a9424579cafb6723c550bba373e4d025cee9591ae3527b66a724e4db；约束与验证见整体history同轮。
- 本项 79.78 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R28/comparison.json，提交 6adcfb551dac5d235bff71af。

### 2026-10-25 C7/C8 parent A3 rejection evidence

- C7 stage source012fa9b4/binary74926429, cores1/40 strict preflight and full protocols Pass. H34q8valid8 at40cores ColumnAccumulate0.574023 to0.704844us (+22.79%), NormalizeColumns1.030586 to1.162266 (+12.78%); E160/E48 unchanged controls near1. Row-major interleaving not advanced to production/A2.
- Same-source row controls: RowDivPanel0.511953, RowDivOnly0.385234, NormalizeRows1.730000 us/proxy call. These are nonadditive contexts, not exact instruction shares; investigate original short WholeReduceSum cost next.
- C8 cost-guarded denominator Copy+dense Div source14133d5f passed fresh19suite including1008holdout, NaN payload/zero signs/guards/input/unwritten all exact. Whole A3 c3 13.90 to14.31us (+2.95%), c5 69.28 to70.84 (+2.25%); denominator copying offsets fewer Div repeats. Not submitted or fused.
- Formal7-effective review read and rootack SHA2c4c51d7; still no demonstrated C donor. Keep native Div, actual iters/FP32 order and every eps.


## 2026-10-25T02:43:30.520861+08:00 — cases145_max_member1_20261025_R29

- 分支M，SHA 26ee0ad7a53014af714da5934985498d1519f86778afb2603c5774e490be4b16；约束与验证见整体history同轮。
- 本项 78.81 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R29/comparison.json，提交 6adcfc251dac5d235bfff258。


## 2026-10-25T02:46:57.864763+08:00 — cases145_max_member1_20261025_R30

- 分支B，SHA f3e47ee4a9424579cafb6723c550bba373e4d025cee9591ae3527b66a724e4db；约束与验证见整体history同轮。
- 本项 86.21 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R30/comparison.json，提交 6adcfcf41dac5d235b007005。


## 2026-10-25T02:51:27.587581+08:00 — cases145_max_member1_20261025_R31

- 分支D，SHA 57a3f2a87e99c94111e2fbf74da4f382d7a4fe1b147d03278aaa1a2731921245；约束与验证见整体history同轮。
- 本项 84.8 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R31/comparison.json，提交 6adcfe071dac5d235b0122d5。


## 2026-10-25T02:55:00.769627+08:00 — cases145_max_member1_20261025_R32

- 分支M，SHA 7c3275dd848553fa06334508f4f4ac3b2918aa0fd0e9046f0e78b4122478f55a；约束与验证见整体history同轮。
- 本项 78.37 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R32/comparison.json，提交 6adcfed71dac5d235b019dd5。


## 2026-10-25T02:58:28.888350+08:00 — cases145_max_member1_20261025_R33

- 分支D，SHA d5e6b51003bd92dd03282e8b799007835110bf397413fa5e9d2113c7ac6e2217；约束与验证见整体history同轮。
- 本项 91.76 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R33/comparison.json，提交 6adcffa71dac5d235b021c36。


## 2026-10-25T03:01:56.709644+08:00 — cases145_max_member1_20261025_R34

- 分支M，SHA 26ee0ad7a53014af714da5934985498d1519f86778afb2603c5774e490be4b16；约束与验证见整体history同轮。
- 本项 79.27 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R34/comparison.json，提交 6add00771dac5d235b02984b。


## 2026-10-25T03:05:24.114680+08:00 — cases145_max_member1_20261025_R35

- 分支D，SHA 9c87bf37552adfc1c325a99da772fb563ae224e7fc654f88acf40ed75b8f899e；约束与验证见整体history同轮。
- 本项 80.78 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R35/comparison.json，提交 6add01461dac5d235b033068。


## 2026-10-25T03:09:07.836377+08:00 — cases145_max_member1_20261025_R36

- 分支M，SHA 7c3275dd848553fa06334508f4f4ac3b2918aa0fd0e9046f0e78b4122478f55a；约束与验证见整体history同轮。
- 本项 87.68 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R36/comparison.json，提交 6add022b1dac5d235b03f77e。


## 2026-10-24T19:12:31.641903+00:00 — cases145_final_diagnostic_gates_20261025

- 方法：C10仅把native WR输入位复制到既有broadcast scratch pitch64，实际矩阵pitch40/Div/树/eps不变；H22不适用则回退。
- 验证：1/40核各840launch strict/guard/input检查通过，source e4eaad15、stage binary 387eee72固定。
- 结果/决定：40核H34 q8v8 ReduceRows1.285195→2.461719μs(+91.54%)，NormalizeRows1.728359→2.905938(+68.13%)；v4+65.11%，H22控制相同。Copy/barrier全成本显著负面，不做完整生产fresh、不A2。
- 证据/经验：C/stage_micro_row_pitch64_v10/parent_profile_cores40/comparison.json；保持C6短行路径。代理不可相加，未改变源顺序但对齐搬运仍不值；未实测A2此机制。


## 2026-10-25T03:14:04.232978+08:00 — cases145_max_member1_20261025_R37

- 分支M，SHA 06fb13aefcd79b8bef105479e11a0d5e7e880056b1ac8187ea2d0cc5aad369c8；约束与验证见整体history同轮。
- 本项 78.94 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R37/comparison.json，提交 6add03531dac5d235b04a006。


## 2026-10-25T03:17:30.930966+08:00 — cases145_max_member1_20261025_R38

- 分支D，SHA 57a3f2a87e99c94111e2fbf74da4f382d7a4fe1b147d03278aaa1a2731921245；约束与验证见整体history同轮。
- 本项 79.51 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R38/comparison.json，提交 6add04221dac5d235b050829。


## 2026-10-25T03:21:04.462882+08:00 — cases145_max_member1_20261025_R39

- 分支M，SHA 06fb13aefcd79b8bef105479e11a0d5e7e880056b1ac8187ea2d0cc5aad369c8；约束与验证见整体history同轮。
- 本项 78.05 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R39/comparison.json，提交 6add04f21dac5d235b058cc7。


## 2026-10-25T03:24:27.312691+08:00 — cases145_max_member1_20261025_R40

- 分支D，SHA 57a3f2a87e99c94111e2fbf74da4f382d7a4fe1b147d03278aaa1a2731921245；约束与验证见整体history同轮。
- 本项 78.36 μs，A2 Pass；平台失败补偿依2026-10-25新授权，平台失败 False，单项最低不代表最终采用。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/R40/comparison.json，提交 6add05c21dac5d235b061370。


## 2026-10-25T03:24:42.209435+08:00 — cases145_member1_20261025_completed

- 采用：D1（最高观测官方分版本），SHA 57a3f2a87e99c94111e2fbf74da4f382d7a4fe1b147d03278aaa1a2731921245；严格iters、原树/eps/Div、单launch与32B owner保持。正式kernel、冻结快照、服务端源码一致。
- 验证/成绩：A3完整逐位/边界与holdout通过；A2 Pass，本项/整体 78.36μs；官方 30.6分/r18，观察2026-10-25T03:24:27.373097+08:00，隐藏10项详情未知。
- 决定/经验：M3 R37/39为30.68/29.93未证明稳定总分优势；按排名优先恢复D1（历史最高30.80，三次中位30.52高于M3的30.305）。融合公开收益保留为候选；D15/C10/尾WR压缩淘汰。跨时段波动不作编译因果。
- 停止与证据：原始尝试40，接收38，有效37；member2未用，剩余额度不自动继续。最终SID 6add05c21dac5d235b061370；/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/REPORT.md、/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_cases145_member1_max_50/final_selection.json。


## 2026-10-25 — m1m2_batch_member1_20261025_comparison_complete

- 方法/范围：四个已冻结版本复测；严格真实iters1..32、FP32原求和次序、原Div和eps、单launch、输入只读与32B owner均不改。用户已取消用完剩余额度及B2选批优化提交。
- A2结果：M2 78.97 us；C6 78.81 us；D1 79.77 us；M1 78.83 us；均Pass，数值来自各自精确SID，隐藏10项详情未知。
- 官方观察：M2 29.67分/r19 SID 6add70571dac5d235b3c49fd；C6 28.67分/r20 SID 6add72051dac5d235b3d8ee4；D1 29.63分/r19 SID 6add72de1dac5d235b3e363c；M1 29.71分/r18 SID 6add73b81dac5d235b3ed41b；观察时间与完整SHA见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_m1m2_batch_member1_remaining/REPORT.md；R01初始M1仅附录，无分数。
- 决定：未自动选版；生产源码暂保持M1 SHA 26ee0ad7a53014af714da5934985498d1519f86778afb2603c5774e490be4b16，等待用户选择，不把动态分数当作源码稳定属性。
- 停止/证据：原始尝试6，接受5、有效5；member1当日43/50，剩余7次不自动使用。STOP保留，B2选批草稿未执行或提交；/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_m1m2_batch_member1_remaining/comparison.json。


## 2026-10-25T11:20:16.264081+08:00 — m1m2_member1_20261025_user_selected_M1

- 选择：用户明确指示“保留M1”；正式kernel已是M1，核对哈希一致，无需覆盖源码。
- 证据：SHA 26ee0ad7a53014af714da5934985498d1519f86778afb2603c5774e490be4b16；member1提交 6add73b81dac5d235b3ed41b，A2 Pass；本项/五项耗时 78.83 µs。
- 观察：该次官方29.71分/第18，观察时间 2026-10-25T11:13:42.506903+08:00；仅作历史榜单参考，不声明当前排名；隐藏十项详情未知。
- 状态：已确认M1并保持STOP，不再提交、不续用余量；选择记录 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_m1m2_batch_member1_remaining/final_selection.json。


## 2026-10-25T12:39:46.981439+08:00 — m1_cases345_3x5_merge5_20261025_completed

- 方法：q8改q4、原生WR行间步长8/2/4和带尾组保护的q8 wave packing5版；原树/eps/Div、真实iters、单launch和32B owner保持。
- A3：−6.550%、−4.291%、−0.185%、−1.352%、+0.215%；末版69.77→69.62us，改善小于约0.472%基线漂移；未达>5%，0/5 A2请求。
- 验证：5版fresh编译/逐位/guard与holdout通过；wave packing额外8套件/894配置的完整组、部分尾组、r1回退、core8/40和eps/负零检查全部通过。
- 经验：q8仍保留；仅行间调度未减少每轮WR→eps→广播→Div与原列归约依赖；更多calls/更大stride可能抵消收益，停止同类扫描，不声称不存在bank问题。
- A2/停止：仅M1额外确认本项78.41us，SID 6add871c1dac5d235b4c9e53；M1保持。/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_m1_cases345_3x5_merge5/REPORT.md、candidate_comparison.json，分路C/FINAL_C_REPORT.md。


## 2026-10-25 M1 八行BR、尾部WR与分母表示独立优化（已停止，待选择）

- C/v1仅改K5..8短行八行BR、完整三层根树保留；C/v2紧凑分母省Brcb但Div repeats未减且调用增加；C/v3同路组合。
- A2：R03 795.49/2.62/16.30/104.89/62.25 us; R10 796.61/2.56/16.11/105.44/62.34 us; R07 799.63/2.65/17.94/104.91/74.71 us；归约首版优于组合版的当前观测，不按官方分数决定取舍。
- C/v2 A3 69.36→72.31us退化4.25%，不送A2；C/v3 A3 56.44us慢于v1的53.19us。跨行Div的控制和地址访问改变已知，bank冲突仅假设。
- 原始归约465配置/16M words全逐位通过；原始Div3768配置/543M有效words全逐位，尾行未操作padding保持原位，预期padding差异单列；guard/input/所有权均无错误。
- 本路3/5请求，未对fail补交。候选冻结，正式M1、用户选择待定；RAW与REPORT提供精确SHA证据。


## 2026-10-25 M1融合A1+B2+C1验证完成（已停止，待选择）

- 融合F1 SHA fd52c080d686134fa389a3930d6f922adf19cd4d5a5fd462ee6a65d9e5f6a798，A1+B2+C1 literal union；原iters/树/eps/Div/输出所有权不改，正式M1保持。
- 本项A2：F1 62.46/72.16 us；本轮M1 93.49 us。独立版上轮 A1:80.23/78.78 us, B2:81.00/78.35 us, C1:62.25/62.34 us；跨时段明确标注。
- 检查/经验：A3严格9222配置执行含1008holdout与边界检查通过；mask/UB/dead scratch/树静态审查无问题。F1同SHA case3/5复测变慢，case4较稳定，不能确认三项独立收益同时稳定保留。保留全部记录，不外推A2机制。
- 停止/证据：member2 3/5 POST后停止，fail不补，无自动换基线；用户选择待定。完整五项/SID/分数排名观察时间见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_m1_merge_a1b2c1_5/REPORT.md、final_comparison.json。


## 2026-10-25T14:18:07.365489+08:00 — user_selected_F1_as_baseline

- 用户明确选择F1作为新基线；正式云端kernel.asc已部署冻结F1，SHA fd52c080d686134fa389a3930d6f922adf19cd4d5a5fd462ee6a65d9e5f6a798。原M1快照继续保留。
- 本项既有A2两次Pass耗时 62.46/72.16 us；完整同次五项、SID、观察时间见整体记录；case3/5波动结论保持，隐藏细节未知。
- 生产/冻结/服务端源码哈希一致，原iters/求和次序/eps/Div与输出所有权不变。此次只部署已验证字节，不重新编译或运行NPU。
- 用户要求不再提交；新增POST=0、本轮计数3/3及STOP保持。选择及部署证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_m1_merge_a1b2c1_5/final_selection.json、post_selection_audit.json。


## 2026-10-25T14:25:12.568665+08:00 — f1_single_confirmation_once_completed

- F1同SHA追加一次member2 A2测评，正式源码未改；保持原iters/树/eps/native Div与输出所有权。
- 本项Pass耗时 71.59 us；此前同F1为 62.46/72.16 us，完整同次五项见整体记录。SID 6adda02d1dac5d235b5f7783。
- 同SHA三次实测全部保留，复测不是源码优化收益；分数排名为观察快照，隐藏细节未知。
- 本范围1/1完成并STOP，无pending，不再提交；正式基线继续F1。证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_f1_confirmation_once/REPORT.md、comparison.json、final_audit.json。


<!-- f1_entry_tail_layout_20261025_history -->
## 2026-10-25 F1 三路短行入口/尾部ApplyRows/布局（已停止，待用户选择）

- 方法：C/v1/v2的gap增加列分片/mask，A3退化未交；v3跳过gap列后A3持平，A2无case5收益。A/v1同SHA 74.53→62.55，F1也73.75→62.84，不能归因源码。
- 本项A2实测（us，按提交顺序；均平台整体Pass/公开项Pass）：R01 F1_control_open:73.75; R02 B_v1_tail_apply:73.62; R03 A_v1_short_entry:74.53; R04 F1_control_middle:71.86; R05 A_v1_short_entry_repeat:62.55; R06 F1_control_after_A_repeat:62.84; R07 A_v2_fixed_q:62.72; R08 C_v3_row_gap_active_columns:63.07; R09 B_v1_tail_apply_repeat:64.05; R10 F1_control_close:61.13; R11 A_v2_fixed_q_repeat:63.43。
- 严格iters1..32、原树/+0/eps/native Div、输入/guard/未写输出、32B owner及边界通过；A3诊断与官方case形状映射未知，隐藏十项未知。
- 状态：生产F1未改；member2 A/B/C=5/3/3含对照，全11次已完成并STOP，fail不补、不自动融合，等待用户选择。[完整报告](/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_f1_entry_tail_layout_3x5/REPORT.md)、[源码/SID/分数排名](/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_f1_entry_tail_layout_3x5/final_comparison.json)。


<!-- user_selected_B1_20261025_history -->
## 2026-10-25T15:52:05.284092+08:00 — user_selected_B1_as_baseline

- 用户选择本轮B1为基线，云端kernel已部署冻结B/v1，SHA 7f9a5c0ac91fb990eb7ce9ffd0b5494ad42e509043e32cf62eb1136259dfb8d8；原F1快照保留。
- 本项既有A2 Pass两次为73.62/64.05 us，分别来自R02 SID6adda89e1dac5d235b66d48a和R09 SID6addb00b1dac5d235b6c763b；完整同次五项见整体历史。
- 沿用同SHA A3严格/边界/所有权检查及A2记录；保持真实iters、原树/+0/eps/native Div。不把用户选择等同于全项稳定提升，公开case形状映射及隐藏十项详情仍未知。
- 此次仅部署已验证字节和记录，新增POST/编译/NPU均0，本轮11/11及STOP保持，无pending、不再提交。[选择](/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_f1_entry_tail_layout_3x5/final_selection.json)、[审计](/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_f1_entry_tail_layout_3x5/post_selection_audit.json)。


<!-- b1_tail_exp_gate_20261025_history -->
## 2026-10-25 B1 三路优化（已停止，待用户选择）

- C1批gate搬运/后处理/输出；C2进一步valid>2两次跨tokenDMA，valid<=2保留pair。有效字节/块数不减，减少的是调用与描述符；raw全H、尾批和分核所有权检查通过。
- 本项A2实际耗时(us，顺序不删)：R01 B1_control_open:62.52; R02 A1_tail_BR:62.77; R04 C1_gate_merge:71.18; R05 B1_control_middle:63.24; R06 Bv1_contiguous_Exp_eps:62.88; R07 C2_gate_batchload:61.14; R08 A1_tail_BR_repeat:62.14; R09 Bv1_contiguous_Exp_eps_repeat:62.66; R10 B1_control_close:62.16; R11 C2_gate_batchload_repeat:63.08。
- 每个候选独立SHA与完整同次五项见整体history及REPORT；真实iters1..32、原树/+0/eps/native Div、输入/guard/未写/32B owner检查通过。A3与A2证据分开，官方case形状及隐藏十项详情未知。
- 状态：生产仍B1；本轮member2 A/B/C=3/3/4，共10次请求且全部Pass，fail不补、无pending并STOP，用户选择前不部署。完整证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_b1_tail_exp_gate_3x5/REPORT.md、final_comparison.json、final_audit.json。
- 判断：C1单次71.18us不支持保留；C2首61.14us、复测63.08us，后一次慢于收尾B1 62.16us，首次收益未复现。减少调用而有效字节/块数不减，不能直接认定MTE2延迟按比例降低。


<!-- a1_interleave_tailmul_stripe_20261025_history -->
## 2026-10-25T18:59:01.391315+08:00 A1 三路优化完成（已停止，待用户选择）

- 方法：8列块驻留减少行分母Brcb，新增列API/转换；C2 active斜率更慢且I1/I2 fallback同样慢约3.2us，不能只归转换。eps合并单独消融，结果按完整SHA记录。
- 本项A2实测(us，顺序完整)：R01 A1_control_open:63.55 us; R02 B1_tailMul_pack:70.57 us; R03 A1_control_mid:62.47 us; R04 B1_tailMul_pack_repeat:62.69 us; R05 A1_control_after_B:62.77 us。完整同次五项/SID/分数排名观察时间见整体记录及REPORT。
- 验证：所有实测候选各35套/9222配置、input/guard/未写输出与owner尾批检查通过，原iters/树/eps/Div保持。专项raw与容量修复证据分开，prepared-only版本不称设备通过。
- 停止/决定：member2原始/接受5/5，每路最多5且对照计入、fail不补；STOP、pending空，正式A1保持，等待用户选择。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_a1_interleave_tailmul_stripe_3x5/REPORT.md、final_comparison.json、excluded_candidates.json、final_audit.json；A3与A2独立，官方shape/隐藏详情未知。


<!-- a1_compact_prezero_rootpair_20261025_history -->
## 2026-10-25T20:42:32.678705+08:00 A1 紧凑Div与正零/根平面三路完成（停止，待用户选择）

- 方法/结论：短行预零、BR根平面配对、缓存tile+mask复用三版独立A1父版；proxy5退化2.15%/3.61%/2.46%，故C无A2。C raw2960/2290/2960套通过。B/v2在A2本项62.19/62.02有小幅重复优势，来源机制和官方形状未知，不能据此确认C路线收益。
- 本项A2实际耗时(us，全部顺序保留)：R01 A1_control_open:62.89; R02 B_v1_prezero:62.69; R03 A1_control_middle:62.74; R04 B_v2_prezero_sum:62.19; R05 A1_control_close:71.80; R06 B_v2_prezero_sum_repeat:62.02。完整同次五项/SID/分数排名时间见整体记录及REPORT。
- 验证：7个候选各35套/9222配置A3逐位通过；原生A两版各12960配置/207360批次，B两版各48几何/6720对，C三版2960/2290/2960套均通过，容量跳过不是设备Pass；NaN全编码专项及CSV/源码/binary绑定分开保存。
- 停止/证据：member2原始/接受6/6，无fail补交；A/B/C=1/5/0且对照计入，今日41/50。STOP、pending空、无自动续交。详见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_a1_compact_prezero_rootpair_3x5/REPORT.md、final_comparison.json、final_audit.json；BAAB漂移标签单独补正，原始计时和所有中位数不变。
- 保留决定：正式仍A1、用户选择待定，不自动融合或部署；A3代理与A2官方case映射未证实，隐藏十项未知。详见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_a1_compact_prezero_rootpair_3x5/REPORT.md、final_comparison.json、excluded_candidates.json。


<!-- a1_cases12_member3_20261025_history -->
## 2026-10-25T23:08:54.797215+08:00 A1 case1/case2 两路与融合（本项完整观察）

- 方法/结论：本轮无case5专属数值改动，A1同源61.81/71.50/62.82us存在明显波动。F2为62.20/62.80us，接近近时A1；不声称稳定收益，保留E1/E2/F1/D2所有有效慢记录。
- 本项A2实际耗时(us，全部顺序保留)：R01 A1_control_open:61.81; R02 E1_packed_input:72.15; R03 D1_br8_roots:62.65; R04 E2_compact_pitch8_entry:71.67; R05 A1_control_mid:71.5; R06 D1_br8_roots_repeat:61.71; R07 E2_compact_pitch8_entry_repeat:62.25; R08 F1_D1_E2:70.87; R09 E2_compact_pitch8_entry_third:63.4; R10 F1_D1_E2_repeat:69.89; R11 D2_isolated_entry:69.73; R12 D2_isolated_entry_repeat:63.05; R13 A1_control_late:62.82; R14 F2_D2_E2:62.2; R15 F2_D2_E2_repeat:62.8。每次完整五项与SID见REPORT，不拼跨版本最小值。
- 分层验证：D1/D2 fresh 35套/9222配置，E1/E2/F1/F2 fresh 45套/23131配置，含holdout，FP32全位、NaN payload/符号、零符号、guard/input/漏写检查通过。D2/F2各432组UB阈值回退通过。D1 raw 192数据集/73728 uint32为D1表达式专项；融合复用边界单列，不称融合raw binary运行或动态race检查。
- 证据边界：完整同次五项/SID/SHA/分数排名观察时间、慢记录与分层证据见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_a1_cases12_member3_2x5_merge5/REPORT.md、final_comparison.json、candidate_registry.json、final_audit.json。A3代理不是A2官方shape，隐藏十项未知。 case编号仅组织观察，不代表已知shape或专属路由；静态/设备/A2结论分开。
- 决定：member3原始/接受15/15，D/E/M=5/5/5（对照和复测计入），无补交/换号/跨日。STOP、pending空、全部root任务完成；两个GPT-6.1-sol Max子agent已关闭。 正式继续A1，用户选择前不替换；整体完整SHA与经验见history.md本轮条目。


<!-- cases12_F2_selected_20261025_history -->
## 2026-10-25T23:28:52.996269+08:00 F2已由用户选择并部署

- 正式F2 SHA b23f7c906666d2ce734812e6ab4b9c59faa5aca2eed17c5fd419cb32815ac149，原A1保存，完整源与部署审计见整体history本轮条目。
- 本项两次A2记录 62.2/62.8us，完整同次五项及SID保留于 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_a1_cases12_member3_2x5_merge5/REPORT.md；隐藏十项未知。
- 此次部署新增POST/编译/NPU均0，复用同SHA验证；不将此项或其他项跨版本最小值拼接。
- 用户选择及源审计：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_a1_cases12_member3_2x5_merge5/final_selection.json、post_selection_audit.json。旧轮STOP与15次预算已结束，不自动续交。


<!-- f2_targets600_23_member3_20261025_history -->
## 2026-10-26T03:42:12.027034+08:00 F2 case1/2轮次的case5完整观察

- 本轮没有case5专属新路由承诺；case编号是官方观察项，不能据耗时反推隐藏shape或实际分支命中。严格iters/FP32节点顺序/eps/Div及32B owner保持。
- 本项关键A2观察us（完整同次五项见REPORT，其他所有轮次同样保留）：F2_control_open:63.28；F2_control_mid:61.73；F2_control_late:62.85；F2_control_close:62.84；M1_D10_E23:71.6；M1_D10_E23_repeat:61.53；M3_D26_E23:71.28；M3_D26_E23_repeat:62.7。不剔除慢记录，不拼跨源码最小值，不宣称稳定全项改善。
- 源/二进制/输入及服务端快照绑定、A3严格whole/holdout与专项raw/资源检查分层保存；25次平台整体Pass，隐藏十项耗时仍未知。
- 正式F2不变，用户候选选择权保留；member3 25/30，D/E/M=9/10/6，STOP、无pending或后台运行。证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_f2_targets600_23_member3_2x10_merge10/REPORT.md、final_comparison.json、candidate_registry.json、final_audit.json。


<!-- m3_repeat_two_20261026T074934_history -->
## 2026-10-26T07:55:55.595891+08:00 M3追加两次：case5稳定性观察

- 同一冻结M3 SHA e5ad93b67d0e7f6ddf6f23a60ccacb186bee6d401d5bfd9451af100edc745943，仅复测，正式F2不变，原实际iters/求和/eps/native Div保持。
- 本项四次A2 us（按顺序、包含慢值）：71.28 / 62.70 / 63.44 / 62.28；新增两次为63.44 / 62.28。完整同次五项与SID见追加REPORT。
- 四次范围62.28–71.28us、范围/中位数14.270%；样本数4、新旧相隔数小时且无新增F2对照，仅描述观察，不宣称后续稳定或跨版本因果收益。
- 请求追加2/2完成；累计member3 27/30、融合M8/10，STOP恢复、无pending；证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_f2_targets600_23_member3_2x10_merge10/m3_repeat_two_20261026T074934/REPORT.md、stability_analysis.json，累计final_audit绑定27次。


<!-- M3_selected_20261026_history -->
## 2026-10-26T08:06:10.176111+08:00 用户选择M3作为新正式基线

- 用户明确选择M3为正式基线；正式kernel.asc复制冻结原字节，SHA e5ad93b67d0e7f6ddf6f23a60ccacb186bee6d401d5bfd9451af100edc745943。父F2 SHA b23f7c906666d2ce734812e6ab4b9c59faa5aca2eed17c5fd419cb32815ac149保存在本轮selection目录。
- 复用同SHA既有A3分层验证及四次A2 Pass，快照/服务端回显逐一一致；本项记录：71.28 / 62.70 / 63.44 / 62.28 us；同次五项/SID见selection.json。保留慢值，不拼接最小值或声称全部case稳定提高。
- 此次新增POST/编译/NPU均0；原iters/求和次序/eps/native Div不变，官方七文件不变。
- 累计member3 27/30，D9/E10/M8；剩余D1/M2共3次明确冻结，STOP保持、无pending和后台任务；后续仅分析600us/2.3us目标。
- 选择、父版、全向量及部署审计：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261025_f2_targets600_23_member3_2x10_merge10/selection_M3_20261026/selection.json、post_selection_audit.json；当前指针 /mnt/workspace/enjoy_ur_time/the_thing_u_must_know/current_baseline.json。


<!-- m3_cumulative_coeffshare_20261026_history -->
## 2026-10-26T11:43:15.103892+08:00 数学优化轮case5观察（正式M3保持）

- 方法/结论：非本轮定向优化；仅记录完整同版本交叉观察，不把波动归因候选数学路线。
- 本项全部A3代理实际耗时us：D1_CumulativeTile64:53.58（配对M3 53.27）；D2_CumulativeFullRow:53.54（配对M3 53.43）；D3b_EpsStateReuse:53.16（配对M3 53.43）；E1_ColumnCoeff:53.54（配对M3 53.78）；E2_SoftmaxCoeff:53.48（配对M3 53.17）；E3_ColumnCoeffInitReuse:53.77（配对M3 53.48）；A3与A2分开，本轮A2 POST=0，无候选官方耗时。完整同次五项及SHA见整体history和REPORT。
- 六版在本轮有限测试集内通过1e-5组合容差/独立reference，非M3逐位等价；原iters/索引树/row0+0/eps/nativeDiv保持。旧D3未设备运行，native全域误差与动态低UB/EPS缺口单列，不从隐藏形状推断路径。
- 新D/E/M各5次未用，旧13冻结；STOP、pending空、全部任务结束、两agent关闭；未融合/部署，用户选择待定。证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_m3_cumulative_coeffshare_member3_2x5_merge5/REPORT.md、final_comparison.json、candidate_registry.json、final_audit.json。


<!-- requested_D3b_E3_once_20261026_history -->
## 2026-10-26T12:21:43.565254+08:00 D3最终版/E3指定官方各一次

- 方法/范围：用户指定最终D3b与E3各member3一次官方验证，无代码修改；原iters/索引树/eps/nativeDiv保持，正式M3不变。
- 本项A2完整观察：D3最终D3b=62.55us（SID6aded3df1dac5d235b3052f3）；E3=64.26us（SID6aded4be1dac5d235b30d5a8）；两次整体Pass、源快照/服务端一致，完整同次五项与SHA见整体history和追加REPORT，不拼接最小值。
- 单次结果不证明稳定；A3原退化记录保留，隐藏十项未知，无新M3同期对照，不据跨时段差值宣称因果收益。
- 本轮累计2/15、D/E/M=1/1/0，余4/4/5与旧13冻结；STOP、pending空，不融合/部署或额外复测。证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_m3_cumulative_coeffshare_member3_2x5_merge5/requested_D3b_E3_once_20261026/REPORT.md、final_audit.json。


<!-- m3_coltree_singleexp_20261026_history -->
## 2026-10-26T13:24:48.517187+08:00 列树/单Exp轮case5观察（正式M3保持）

- 本项全部A2观察：M3_control_D_open=72.09us SID6adeddb61dac5d235b36c598；D1_ColumnBinaryTree=63.00us SID6adedf451dac5d235b3857de；D3_ColumnTreePrefetchOnly=63.17us SID6adee2db1dac5d235b3ac48d；D3_ColumnTreePrefetchOnly_repeat=70.31us SID6adee3b81dac5d235b3b5c4a。完整同次五项与完整SHA见整体history及REPORT，单次记录不证明稳定。
- 三版列树/四版单Exp实际CANN与A3正确性/reference通过；严格iters/FP32/eps/nativeDiv、原行树保持，仅列树允许改变。D有位差，E仅在本轮执行suite逐位一致。
- A3全部同SHA配对五项及慢phase保留于REPORT/final_comparison。case1代理确认prefetch、case3/5代理generic、case4代理scaled_batch；官方隐藏形状/路径未知。单Exp四版无目标收益，不送A2；未融合。
- 正式M3及官方七文件/current_baseline不变，候选由用户选择。member3本轮用量{'D': 4, 'E': 0, 'M': 0}，承接余额{'D': 0, 'E': 4, 'M': 5}与旧13冻结；STOP、无pending、全部任务完成、两个agent关闭。证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_m3_coltree_singleexp_member3_4x4_merge5/REPORT.md、final_audit.json。


<!-- selected_D3_E2b_once_20261026_history -->
## 2026-10-26T14:13:33.635489+08:00 D3新基线与E2b一次探针case5

- 正式D3 SHA 29fd214a4268c776c7de28d748299f339903f25421f97ba1e89ff7036e1bdec4已部署并核对原字节，M3备份；原iters/FP32/eps/Div/行树保持，仅原允许列树变化。
- 现成E2b（M3父版、非融合）一次A2观察：63.67us，SID 6adeee581dac5d235b438567，整体Pass及source/server一致；完整五项见整体history/REPORT，不拼接最小值。E2b不部署，单次不证明稳定收益。
- A3负面证据保持；本次没有新增算法代码或A3实验，仅探针默认官方sample前置与一次POST。当前正式D3既有完整同SHA记录继续保留，隐藏路径未知。
- 累计D/E/M=4/1/0，剩余0/3/5及旧13冻结，STOP恢复、无pending；后续仅分析。证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_m3_coltree_singleexp_member3_4x4_merge5/selection_D3_and_E2b_probe_20261026/REPORT.md、final_audit.json。


<!-- d3_rowfold_absreuse_20261026_history -->
## 2026-10-26T15:57:13.759734+08:00 行折叠/Abs复用轮 case5

- 目标分支之外保留完整回归记录，不从时间变化推断隐藏路径。全部7份有效A3候选的同版本完整五项、配对D3和慢phase保留，2个精度失败保留原始日志；详见整体REPORT和COST_AND_DECISION.md。
- E1一次A2本项64.08us，完整646.23/2.41/15.49/83.43/64.08us，SID6adf04b91dac5d235b548b9c、SHA6b7e98276d00de53ec223a9c8fcb1243b996ef1de9fc0df5d6bb06ff17a7fe2a；Pass及source/server匹配，单次非同期对照不证明稳定收益。
- 正式列树D3 SHA29fd214a4268c776c7de28d748299f339903f25421f97ba1e89ff7036e1bdec4保持；严格实际iters/FP32/eps/行→列阶段，用户允许求和树/Div实现试验。未融合/部署，候选留待用户选择。
- 本轮D/E/M用0/1/0、余5/4/5暂存、旧21冻结；STOP、无pending、全部任务终态、agent关闭。证据 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_d3_rowfold_absreuse_member3_2x5_merge5/REPORT.md、final_comparison.json、final_audit.json。


<!-- d3_weighted_singlevector_20261026_history -->
## 2026-10-26T17:36:11.799812+08:00 分块加权归约/单repeat轮 case5

- 保留全部可见耗时与慢记录，不由单项波动推断隐藏路径或整体收益。本轮实际官方记录：R01 D3=62.79us；R02 E2=61.53us；R03 E2=70.96us；R04 D3=69.73us；R05 E2=62.54us；完整同次五项与SID/源SHA见整体history本轮条目及REPORT。
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
## 2026-10-26T19:41:01.981949+08:00 E2计算过程优化轮 case5

- 本项完整慢记录保留，不由单点波动推定隐藏路由或归因为未改的计算路径。E2/T3b/D1b按各自完整同次五项评价，不拼接最小值。
- 本轮实际官方记录：R01 E2_control_E_open=63.13us；R02 T3b_screen=62.22us；R03 E2_control_E_postreconnect=63.51us；R04 T3b_repeat1=70.50us；R05 T3b_repeat2=61.83us；R06 D1b_nativeDiv_diagnostic=61.98us。完整五项/SID/各源SHA统一见整体history同轮条目及 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_e2_softmaxinv_blockstats_exppack_3accounts_2x5_merge5/REPORT.md。
- 已执行的设备/reference、A3和A2分别记录，原始失败/FP32位差/慢记录保留；各候选精确证明及未验证边界见COST_AND_DECISION.md、validation_totals.json、官方source绑定。
- 正式E2 SHA24146d8e78edebc792116d4ac28eb3b6c54a1c2b05914b834ba0aa63a732a6ce和官方七文件/current_baseline不变；T3b、D1b候选未部署、没有融合。用户选版前不再优化或提交。
- 新D/E/M用1/5/0，余4/0/5与旧45冻结；member1用6、另两账号0。STOP/pending空/任务终态/两agent关闭，最终审计 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_e2_softmaxinv_blockstats_exppack_3accounts_2x5_merge5/final_audit.json。


<!-- selected_D1b_analysis345_20261026_history -->
## 2026-10-26T20:45:57.524877+08:00 选择D1b并完成case3/4/5计算过程分析

- 用户选择D1b作为正式基线，复制已冻结原字节SHA 84a28f39b95d031947796266e2e0a6bac817905922e06bf5d4af0d9a7cfec9a9；SID6adf3ba21dac5d235b8123f8一次A2 Pass已fresh GET核对八文件，完整五项646.45/2.26/15.59/84.56/61.98us。E2原字节备份 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_e2_softmaxinv_blockstats_exppack_3accounts_2x5_merge5/selection_D1b_analysis345_20261026/before/kernel_E2.asc；不将单次称稳定。
- 本次仅基线部署与只读计算过程分析，新算法改动/编译/NPU/POST/子agent均0；源七官方文件、旧STOP/campaign/REPORT/comparison/choices/audit指纹保持，余D4/E0/M5与旧45冻结。
- 已有A3 ABBA/BAAB八CSV及实际binary SHA复核、60样本同角色汇总与原comparison一致；完整五项和慢记录保留，A3代理映射/官方隐藏形状仍未确认，不从A2单项漂移归因。
- case5代理H34/q8/valid4或8/pitch40已是五块strided BR，仍逐元素Div；优先共享列native倒数、再行倒数，I20活跃元素Div45084→factor1326加原矩阵Mul，非总耗时34倍。work尾320floats可存ones，eps/零节点合并抵消新增依赖；E160混合mask须单列。无新候选/结果。
- 证据：/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_e2_softmaxinv_blockstats_exppack_3accounts_2x5_merge5/selection_D1b_analysis345_20261026/REPORT.md；/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_e2_softmaxinv_blockstats_exppack_3accounts_2x5_merge5/selection_D1b_analysis345_20261026/analysis/REPORT.md、route_projection.json、existing_profile345.json、optimization_plan.json；最终审计 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_e2_softmaxinv_blockstats_exppack_3accounts_2x5_merge5/selection_D1b_analysis345_20261026/final_audit.json。


## 2026-10-26 D1b cases345 math campaign completed

- 方法：C1仅列阶段native FP32 Div1共享Mul，行阶段保留逐元素Div；七版消融比较RC/eps叶子等，保持实际iters/FP32/eps语义。
- 效果：C1 A3四次混合，普通门false保持；预先声明一次A2硬件诊断后最多两次正向复测，本路预算内，A2=59.56/59.46/59.58us。其余弱收益/退化未A2。
- 决定：C1纳入M1，M1自身case4/5 A3普通门均通过，五次A2 case5=59.36/59.77/60.79/60.09/59.69us；正式D1b不变，C5用3余2冻结。
- 版本：C1 SHA2627c32980d55bc6fc872a2ed0edeff2ca52cb4b1fe51ef1f33000da10f19d5c；平台latest M1 SID6adf6d5f1dac5d235ba91dcb未部署。慢记录/全5项/日志缺口 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_d1b_cases345_math_3accounts_3x5_merge5/REPORT.md


## 2026-10-26 用户选择M1并完成case3计算过程分析

- 用户选择融合M1并部署冻结原字节SHAf407ecbd467b5d8389a28a18842d4f23808daa0e2c8a30b71dc6c7488897e083，C1原始负/混合A3记录保持；D1b已备份。
- 本项五次既有A2=59.36/59.77/60.79/60.09/59.69us，fresh GET及同次完整五项见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_d1b_cases345_math_3accounts_3x5_merge5/selection_M1_analysisC3_20261026/selection.json；不称本次新测评。
- 本次仅基线选择与case3分析，新增优化源码/编译/NPU/POST均0；本路余2与旧54继续冻结，后10项Hidden。
- 选择及最终审计 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261026_d1b_cases345_math_3accounts_3x5_merge5/selection_M1_analysisC3_20261026/REPORT.md、final_audit.json；已披露上轮部分重复suite日志原字节缺口，官方A2与CSV记录完整。


## 2026-10-27 保留R1b并只读分析P1非目标退化

- 保留R1b SHA db11daeffeef6973696b1d9692c34b2b043a60c0b73815ac81d998e46fb8faa2；P1不采用，余额冻结。
- 既有A2 case5退化及完整同次五项保留；仅2候选/2对照，不把全部差值判为代码因果。
- A3代理分派/机器码及ICache字段与A2分层；共同入口膨胀不是A2 ICache/spill/bank根因证明。
- 后续仅设计编译隔离和阶段特化，未改实现/编译/NPU验证/提交。
- 公共证据见HISTORY/history.md本日保留条目及 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261027_r1b_case3_padzero_maxfold_3accounts_2x5_merge5/selection_R1b_P1_regression_analysis_20261027/REPORT.md、analysis.json、audit.json。


## 2026-10-27 独立入口/编译期阶段化：用户停止，R1b保留

- 用户停止本轮并保留R1b SHA db11daeffeef6973696b1d9692c34b2b043a60c0b73815ac81d998e46fb8faa2，正式与R04计划内末轮对照一致。
- I1两次A2完整五项与同期两次R1b见整体history本日条目；原始快慢记录均保留、n=2仅描述统计。
- case5描述中位R1b60.81、I1 63.725us，候选慢4.79%，不采用I1。
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

- 本项所有同SID实测（us）：R01=69.49; R02=60.64; R03=59.6; R04=61.16; R05=60.76; R06=59.89; R07=61.64; R08=60.22; R09=61.49; R10=69.33; R11=60; R12=61.13; R13=60.53; R14=70.48; R15=60.28。完整五项/完整SHA/SID /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261028_m2_ub_coloring_3x5/REPORT.md；不拼最小值。
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

- 本项全部同SID官方实测（us）：R01=61.81; R02=70.73; R03=60.04; R04=60.08; R05=68.83; R06=60.62; R07=70.42; R08=60.88; R09=70.04; R10=59.36; R11=60.8; R12=60.89; R13=60.1; R14=60.42; R15=59.6; R16=61.13; R17=68.06; R18=60.81; R19=61.38; R20=61.48。完整五项/SHA/SID /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261028_b4_deadroots_layout_fma_3x5_merge5/REPORT.md，慢记录保留、不拼最小值。
- 正式B4 SHA e7827703d3b4945241bb231d69347cd29c212a0fd0fc9e9af7b4effde80f41b2始终保持，三路与融合候选由用户选。共同方法与独立分层验证见整体HISTORY。
- B5单次case1=597.99us；其他候选和融合不预设收益相加，不把A3计时推成A2或推定官方shape/隐藏。
- 本轮20/20终态，新A/B/C/M各5用尽、旧104冻结；STOP有效/pending空/无自动续跑。证据与核验见本轮REPORT/final_audit。


## 2026-10-28T12:35:45.142931+08:00 用户保留B5并完成case5只读方案分析

- 正式kernel由B4原字节切换至冻结B5_FastPredicateHoist，SHA be52118acd2c2b53f4c4c96a7011af6a7ba039a9469cc48a0b8b06cef3ab5de4；B4完整备份和选版证据[本次选版](/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/selection_B5_case5_analysis_20261028T122057+0800/REPORT.md)。这是用户选择现成版本，新增算法改动0。
- B5仅既有R15一笔A2整体Pass，完整同SHA五项597.99/2.19/14.21/71.36/59.60us；本次仅重验snapshot与缓存服务器八文件，未新平台GET或测评。官方最后已知R20仍B4，不自动提交对齐latest。
- 新方案：[只读分析](/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/selection_B5_case5_analysis_20261028T122057+0800/analysis/REPORT.md)：短行批次私有模式外提、仅stats换址至死亡work、单批gate早ready；整token输入包独立比较，compact八行Sub为一次性低预期备选。保持实际iters/FP32/每eps/nativeDiv及原求和次序；所有收益未验证。
- 已排除旧compact Div、32核wave、行倒数共享等复刻；已有H34/T256/20iters只是A3代理。B5旧CSV两phase case5=52.78/53.30us、Vector27.767us，重叠字段不相加，不能据此确认A2瓶颈或官方shape。
- 本次未新增候选/编译/NPU/平台GET/POST，三名只读分析agent均结束；旧104全部冻结、STOP保留、pending空、无新执行授权。优化记录只写HISTORY，规则入口和旧campaign报告/快照/归档未改。

<!-- final-results:campaign_20261028_b5_short_stats_gates_3x5_merge5 -->
## 2026-10-28T14:18:22.547085+08:00 B5三路与融合轮case5完成（待用户选版）

- 本项全部同SID官方实测（us）：R01/6ae17dcc1dac5d235b1153bd=59.45; R02/6ae183271dac5d235b14eb48=61.84; R03/6ae183eb1dac5d235b156d79=61.92; R04/6ae184ae1dac5d235b15f65e=61.17; R05/6ae185711dac5d235b168191=58.84; R06/6ae186571dac5d235b172824=59.07; R07/6ae187551dac5d235b17d4b0=73.98; R08/6ae188511dac5d235b187faf=61.51; R09/6ae189531dac5d235b19410e=59.70; R10/6ae18a171dac5d235b19d479=61.23; R11/6ae18ada1dac5d235b1a5555=61.02; R12/6ae18b9d1dac5d235b1ad40c=61.68; R13/6ae18c661dac5d235b1b6e9f=70.81; R14/6ae18d291dac5d235b1c28e6=71.52; R15/6ae18ded1dac5d235b1cfe81=61.81; R16/6ae18eb01dac5d235b1d96b1=59.00; R17/6ae18f731dac5d235b1e2520=63.24; R18/6ae190361dac5d235b1eb4bb=75.35; R19/6ae190fa1dac5d235b1f67d8=70.87; R20/6ae191bd1dac5d235b200321=61.47。完整五项/SHA/账号/SID见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261028_b5_short_stats_gates_3x5_merge5/final_comparison.json；每笔完整记录保留，不拼最小值。
- 同SHA描述统计（不代表一次实测）：B5_FastPredicateHoist n=3 median=61.47 [59.45,70.81]；A1_UpperShortMode n=1 median=58.84 [58.84,58.84]；B1_DeadStatsS0 n=1 median=61.17 [61.17,61.17]；B2_DeadStatsS8 n=1 median=61.84 [61.84,61.84]；C1_EarlyGateReady n=1 median=61.92 [61.92,61.92]；A2_UpperShortModeMixed n=1 median=59.07 [59.07,59.07]；B3_UpperDeadStatsS0 n=2 median=67.50 [61.02,73.98]；C2_GateDmaGroupedControl n=1 median=61.51 [61.51,61.51]；A3_UpperShortColumnsOnly n=1 median=59.70 [59.70,59.70]；B4_FullStatBlocksDeadS0 n=1 median=61.23 [61.23,61.23]；C3_UpperShortGateReady n=1 median=61.68 [61.68,61.68]；A4_UpperShortRowsOnly n=2 median=65.26 [59.00,71.52]；C4_UpperShortPairGateDma n=2 median=62.53 [61.81,63.24]；M1_UpperRowsPairGate n=2 median=73.11 [70.87,75.35]。n=1无复现，n=2有限重复；统计极值不可组装成一笔向量。
- 正式B5 be52118acd2c2b53f4c4c96a7011af6a7ba039a9469cc48a0b8b06cef3ab5de4保持；本轮方法、B3复测完整五向量及各case慢记录见整体HISTORY与 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_b5_short_stats_gates_3x5_merge5/REPORT.md。B3同SHA各SID均保留，由用户选择，不自动提升。
- 13源/702套真实A3 numeric/reference+strictbits及52 CSV绑定；A3代理不确认A2官方shape、分支或性能。四个原资源配置相关非零作业保留，只有同SHA新full_v2完整通过可作补证。
- 尝试/接受20/20，账号{'member1': 15, 'member2': 5}，分路余{'A': 0, 'B': 0, 'C': 0, 'M': 0}；旧104冻结，终态/STOP/pending空、无自动续跑。最终审计和用户选版入口见 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_b5_short_stats_gates_3x5_merge5/version_choices.json。
<!-- /final-results:campaign_20261028_b5_short_stats_gates_3x5_merge5 -->


<!-- analysis-only:B5_case5_postcampaign_20261028T143030+0800 -->
## 2026-10-28T15:18:32.178749+08:00 B5保留：case5新布局优先，仍仅分析

- 正式B5 SHA be52118acd2c2b53f4c4c96a7011af6a7ba039a9469cc48a0b8b06cef3ab5de4 保留。上一轮全部逐SID五项、同SHA慢记录及负结果原件仍见 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_b5_short_stats_gates_3x5_merge5/REPORT.md；本项B5三笔59.45/70.81/61.47us不是拼接最小值。
- 当前榜单完整GET保存在 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/analysis_B5_case5_postcampaign_20261028T143030+0800/ranking_live.json，29条Pass中14条case5<50us，当前最低同SID完整五项545.78/1.79/13.19/64.04/35.49us。只能证明公开性能空间，官方case形状、核数和他人实现未知。
- 新首选把8token和8列块轴只在同一H行内交换，保持原softmax、FP32、strict iters、每eps、原sum树和native Div；列阶段仍整行E连续，避免旧stripe列API增加。代理Brcb170→34/row，19轮减2584repeat，Copy初末搬移340repeat；净热段13.07%为静态工作量，不是时延预测。完整地址/存储生命周期、CopyRepeatParams与回退条件见 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/analysis_B5_case5_postcampaign_20261028T143030+0800/REPORT.md。
- 计算次线只优化mixed-E尾向量；并行次线只交接跨核32B边界四行，代理scratch9216B/额外逻辑GM17408B，但7.59%最重核单位仍须付同步/DMA，且A2为32核时无均衡收益。主布局与valid7均衡路径互斥，不当作可相加的融合收益。失败路线与原SDK证据见compute.md/ub.md/schedule.md及JSON。
- 本次未实现、编译、运行NPU、测评或提交；三名既有只读agent已completed。STOP/pending空/旧104冻结及本轮零余额保持，不启动后续执行；完整性审计和新方案均只在HISTORY，当前任务指针按规则更新两个状态JSON。
<!-- /analysis-only:B5_case5_postcampaign_20261028T143030+0800 -->


<!-- final-results:campaign_20261028_b5_rowinner_blocktoken_1x5 -->
## 2026-10-28T16:04:37.800366+08:00 同行内布局轮case5完整记录

- 正式B5 be52118acd2c2b53f4c4c96a7011af6a7ba039a9469cc48a0b8b06cef3ab5de4 保持；L1/L2冻结完整SHA、源和静态证明见整体history与 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_b5_rowinner_blocktoken_1x5/version_choices.json。
- 本项A2全部实测(us)：R01/6ae1a4301dac5d235b2e1f4b=61.39; R02/6ae1a6211dac5d235b301918=59.96; R03/6ae1a6e41dac5d235b30aa54=59.40; R04/6ae1aaa11dac5d235b335fe4=60.63; R05/6ae1ab641dac5d235b33f33c=59.97。对应同SID完整五项/慢记录见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261028_b5_rowinner_blocktoken_1x5/final_comparison.json，不拼最小值，不把描述统计当一笔实测。
- 两候选各67套真实A3 numeric/reference/strictbits通过，A3计时与A2官方分别记录。本项为目标：L1/B5开收控制对照未证明稳定整体优势，所有候选均未达50us。本轮结论与方法见 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_b5_rowinner_blocktoken_1x5/REPORT.md；B5持续正式保留，候选由用户选择。
- 5次新机会全部使用并Pass；旧104冻结，新余0，STOP/pending空、唯一子agentcompleted、无自动续跑。审计 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_b5_rowinner_blocktoken_1x5/final_audit.json；优化记录只写HISTORY，规则/模板原件保持。
<!-- /final-results:campaign_20261028_b5_rowinner_blocktoken_1x5 -->


<!-- selection-host-analysis:L1_20261028T161731+0800 -->
## 2026-10-28T16:40:44.619148+08:00 L1正式选版与Host只读研究

- 用户选定L1，正式SHA 30ac04fcc079bd6e81aecb4f1a66de20bc5cd9017aba96311833fd17bfc25380，原B5及状态备份见整体HISTORY的本次选版目录。未实施Host候选。
- 本项选定SHA官方完整记录(us)：R02/6ae1a6211dac5d235b301918=59.96; R03/6ae1a6e41dac5d235b30aa54=59.40；对应同SID五项、快慢值和原始证据见 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/selection_L1_host_analysis_20261028T161731+0800/REPORT.md 与 selection_provenance.json，不拼最小值。
- Host主线为精确整数分区描述，保持原核数/q/first-end/所有权与全部实际FP32数学；只影响初始化，A2收益未知，不把Device Scalar当CPU时间。资源查询/分派整理为次线，范围与否决条件见整体HISTORY及报告。
- 新编译/NPU/测评/平台GET/POST均0，旧104及零余额继续冻结；STOP/pending空、只读agentcompleted、无新执行授权。正式源与最新官方B5提交不混称，规则/官方模板/旧报告保持原件。
<!-- /selection-host-analysis:L1_20261028T161731+0800 -->


<!-- final-results:campaign_20261028_l1_host_partition_resource_dag_3x5 -->
## 2026-10-28T17:59:17.394635+08:00 L1 Host三路完整结果 case5

- 正式L1保持，SHA 30ac04fcc079bd6e81aecb4f1a66de20bc5cd9017aba96311833fd17bfc25380。P1/P2精确整数分区、U1/U2同调用资源快照、D1/D2分派元数据；6个冻结SHA/审查/证据见 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_l1_host_partition_resource_dag_3x5/version_choices.json。D2仅允许private residentBatch死参数2/4→1，实际消费参数与严格iters/FP32/eps/原sum/nativeDiv保留。
- 本项全部A2实测(us)：R01/6ae1b8d51dac5d235b40130c=59.86; R02/6ae1bb491dac5d235b42169a=62.38; R03/6ae1bccc1dac5d235b432f14=61.18; R04/6ae1bda01dac5d235b43e41a=72.86; R05/6ae1be8a1dac5d235b44aca5=70.74; R06/6ae1bfb11dac5d235b459aab=61.59; R07/6ae1c0d81dac5d235b4679f9=60.88; R08/6ae1c19b1dac5d235b471571=60.71; R09/6ae1c25e1dac5d235b47af44=61.15; R10/6ae1c3211dac5d235b482a88=60.20; R11/6ae1c3e41dac5d235b48bf59=60.76; R12/6ae1c4a81dac5d235b494eaf=60.93; R13/6ae1c56b1dac5d235b49e4ed=60.81; R14/6ae1c62e1dac5d235b4aac91=60.92; R15/6ae1c6f11dac5d235b4b478a=73.59。同SID五项与慢记录见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261028_l1_host_partition_resource_dag_3x5/final_comparison.json，不拼最小值。
- 6候选各67套真实A3 numeric/reference+strictbits通过，共402套、123984次配置执行（非去重）、804实际raw日志、24 CSV；CPU参考1344组/4074文件复用重核，本轮新生成0。HostCPU入队、A3 Device、A2官方分别记录，不互相替代。
- 新额度A/B/C各5次尝试/接受，15/15均Pass，全部member2；member1开场日用50达既有策略50，按授权顺序接续member2，服务端限额未知。最短POST间隔195.194859028秒，旧104冻结、新余0，无融合或额外授权。
- 正式L1与收尾官方一致，用户选择前不自动提升候选。STOP有效、pending空、所有有限作业终态、3名子agentcompleted、无自动续跑。最终审计 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_l1_host_partition_resource_dag_3x5/final_audit.json；优化记录仅HISTORY，AGENTS/README/RULES和官方7文件未改，旧campaign/STOP/审计保持。
<!-- /final-results:campaign_20261028_l1_host_partition_resource_dag_3x5 -->


<!-- analysis-only:L1_case5_rethink_20261028T180557+0800 -->
## 2026-10-28T18:38:12.699176+08:00 保留L1并重新分析case5

- 用户确认保留正式L1，实时SHA 30ac04fcc079bd6e81aecb4f1a66de20bc5cd9017aba96311833fd17bfc25380，当前已是该原字节，无源码复制/回滚。已结束Host轮待选状态由本次人工选择收束，旧campaign/STOP/审计原件不改；详细新方案 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/analysis_L1_case5_rethink_20261028T180557+0800/REPORT.md。
- 选定L1五笔同SHA完整五项(us)：6ae1a6211dac5d235b301918=598.92/2.11/14.38/74.25/59.96; 6ae1a6e41dac5d235b30aa54=600.70/2.19/14.26/74.02/59.40; 6ae1b8d51dac5d235b40130c=597.65/2.18/14.40/74.26/59.86; 6ae1be8a1dac5d235b44aca5=596.93/2.17/16.11/74.38/70.74; 6ae1c6f11dac5d235b4b478a=598.04/2.20/16.68/72.54/73.59。本次重验snapshot/server8文件，未新平台GET；70.74/73.59慢记录保留，原因未确认，不拼最小值。
- 首选矩阵[K,H,T,L]配列因子[T,K,L]并合并BR：H34/I20源数学API564→507，等效repeat14581→14641，UB96064B不变；块主序旧Cstripe已失败，新增差异为单seed配对work/连续eps原生inverse/BR聚合，不能把布局本身当新发现。EarlyPack只将已有转换提前至原max后，一次性少238repeat但净多3数学API，softmax仍输出加eps、分母不加eps。
- 搬运线只改gate输出：L1的16短块→2连续大块，Gather9repeat、索引约10Adds/16repeat/8屏障和2176B额外UB均计成本；旧C1已是2描述符16短块且A2负样本保留，不能称16→2描述符首次创新。无Brcb token最内布局须先证原BR精确树；raw整包及轻核接管gate为更低优先研究，不预加收益。
- 本次仅只读分析，新增候选/编译/NPU/测评/平台GET/POST均0；3名GPT-6.1-sol Max分析agent均completed，STOP/pending空、旧104与零余额继续冻结、无自动续跑或下一轮执行授权。规则/官方7文件保持，记录仅HISTORY；终态审计 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/analysis_L1_case5_rethink_20261028T180557+0800/final_audit.json。
<!-- /analysis-only:L1_case5_rethink_20261028T180557+0800 -->


<!-- final-results:campaign_20261028_l1_case5_pair_earlypack_gatecompact_3x5 -->
## 2026-10-28T20:51:56.578517+08:00 L1 case5三路完整结果 case5

- 正式L1保持，完整SHA 30ac04fcc079bd6e81aecb4f1a66de20bc5cd9017aba96311833fd17bfc25380；六个准入冻结源：A1_PairedWorkBR=a2983953706b18f0443240ec59a020e888f007a96549b2b3ed6328ba61c9ac17; B1_EarlyPackSoftmax=35cefed7f1ee9a485a8179455213d25bfb826da4a718aa903fb9ffbd7c67069d; C1r_GateCompact=3ab07529b03d4d08bddd74e4412844489d5009c49c0847515563c6ccf40e8f3d; A2_PairedContiguousDiv=46e8d86e1c708ab317407dc75bf3d8b323ee7e4f060308fdde2c3ea174c0c2ca; B2_MaxPackSharedFence=832fc4116f89397f6ce486603ffb77278f40ceb9ddea56cc611bdcee00b264a2; C2_GateVectorSeed=b3cda16eca9ecba0c74661386ce445dca52e01abfab918a66222f384c06f0fb3。版本证据 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_l1_case5_pair_earlypack_gatecompact_3x5/version_choices.json 必须保留C2 R14失败与未解决CPU限额风险，用户最终选择；C1默认编译失败源另留。
- 本项可见状态/实测(us)：R01/6ae1d9941dac5d235b592ee1 [Pass]=59.71; R02/6ae1dd531dac5d235b5c1256 [Pass]=71.70; R03/6ae1de161dac5d235b5ca77e [Pass]=61.33; R04/6ae1e02e1dac5d235b5e3a16 [Pass]=71.01; R05/6ae1e16f1dac5d235b5f2267 [Pass]=72.14; R06/6ae1e2321dac5d235b5fcb4e [Pass]=63.61; R07/6ae1e2f51dac5d235b606ef1 [Pass]=72.55; R08/6ae1e3b81dac5d235b60fada [Pass]=59.36; R09/6ae1e47b1dac5d235b618a56 [Pass]=60.27; R10/6ae1e53f1dac5d235b62452a [Pass]=60.73; R11/6ae1e6021dac5d235b62f0eb [Pass]=61.24; R12/6ae1e6c51dac5d235b6399c1 [Pass]=67.22; R13/6ae1e7881dac5d235b642f82 [Pass]=59.99; R14/6ae1e84c1dac5d235b64c118 [Time Limit Exceeded]=Skipped; R15/6ae1eab81dac5d235b66e58f [Pass]=69.34; R16/6ae1eb7b1dac5d235b678345 [Pass]=60.44; R17/6ae1ec3f1dac5d235b6821b8 [Pass]=61.33; R18/6ae1ed021dac5d235b68b329 [Pass]=62.58; R19/6ae1edc51dac5d235b694fd5 [Pass]=61.24; R20/6ae1ee881dac5d235b69f0d5 [Pass]=60.61; R21/6ae1ef4c1dac5d235b6a9610 [Pass]=60.93。raw0保留但TLE/Skipped非0us观察；同SID五项与仅good统计见 /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard/runs_sinkhorn/campaign_20261028_l1_case5_pair_earlypack_gatecompact_3x5/final_comparison.json。
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
- 本case按原始轮次记录，不拼接跨轮最小值：L1_RowInnerCompactDen: R01=59.94, R20=70.99 us; A1_P56DeadPanel: R02=71.91, R08=60.65, R14=72.74 us; B1_WideQ1InPlaceControl: R03=65.29, R09=67.07, R15=65 us; C1_L1FullQPartition: R05=58.98, R10=59.33, R16=59 us; D1_GenericDeadMatrixPrefetch: R04=67.11, R11=71.97, R17=71.63 us; B2_WideOriginalMathBatch: R06=60.19, R12=61.74, R18=61.65 us; A2_P56EvenCompactQ8: R07=60.98, R13=61, R19=60.6 us。
- 分数/排名与该case其他4项共同构成每笔完整向量，详见/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_l1_hidden_families_member3_20/REPORT.md及CSV；不从单项或总分识别隐藏工作负载。
- A3严格baseline位型和独立CPU reference分层通过；A2候选补齐65条/实际1144配置，共194套；六版24族ABBA+BAAB共48phase，逐phase保存launch36端点/CAS并核SHA，端点与L1相同，不宣称每launch/全域。新q8五族geo约+29.7%、B2真实9族约+26.7%；B1/C1负例、A2 H22退化完整保留，均不当作官方A2整体收益。
- 正式L1_RowInnerCompactDen仍为30ac04fcc079bd6e81aecb4f1a66de20bc5cd9017aba96311833fd17bfc25380，未自动保留/融合任何候选；20额度用尽、pending空、有限任务已结束、新campaign STOP与状态已关闭等待用户选择。完整对照/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_l1_hidden_families_member3_20/REPORT.md；CSV /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/campaign_20261028_l1_hidden_families_member3_20/official_observations.csv。
<!-- /campaign-L1-hidden-member3-20:campaign_20261028_l1_hidden_families_member3_20 -->

<!-- selection-B2-hidden-inference:20261029T005944+0800 -->
## 2026-10-29T01:32:36.927300+08:00 保留B2为正式基线，未新增本case测试

- 用户明确选择B2_WideOriginalMathBatch，正式kernel.asc从L1切换为既有冻结B2，SHA256 be9c858f29bfcee4265ca6ac638441dd189d816eacf29e8c7b75ba5ae369cf25；原L1和两个状态原件在/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/selection_B2_hidden_inference_20261029T005944+0800/before。不是新开发候选，不改官方7文件和规则3文件。
- 三笔完整五项（本case为第5项）：R06 [602.91, 2.21, 14.38, 74.24, 60.19] us, score/rank 31.94/20; R12 [601.64, 2.15, 14.59, 72.77, 61.74] us, score/rank 31.98/21; R18 [602.44, 2.17, 14.8, 72.51, 61.65] us, score/rank 31.9/21。不拼接跨轮最小值。
- R06/R12/R18三笔既有官方Pass的服务端与snapshot全部8文件重新哈希匹配；完整同SHA向量/当时首次分数排名均保留，见/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/selection_B2_hidden_inference_20261029T005944+0800/selection_audit.json。本次无编译/NPU/平台GET/POST；平台最近已知为R20 L1对照，不伪称选版已发新提交。
- 只读分析支持用完整算法消融约束隐藏参数族：B2三次hidden均分残量28.176/28.161/28.144，高于L1两端27.931/27.995，属未配对方向线索，不识别H、点数、耗时或因果。动态/内生TBest、运行波动和非目标外溢均保留未知。
- 保留B2为新基线；旧104与已用20额度冻结，STOP保留、pending空、不恢复worker。后续仅凭新的明确授权实验/提交。综合方案/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/selection_B2_hidden_inference_20261029T005944+0800/REPORT.md，公开shape/评分可识别性/分族设计独立报告均在同目录。
<!-- /selection-B2-hidden-inference:20261029T005944+0800 -->


<a id="b2-four-routes-stopped-20261029"></a>
## 2026-10-29 B2四路线停止记录：case5

- 保留B2，SHA `be9c858f29bfcee4265ca6ac638441dd189d816eacf29e8c7b75ba5ae369cf25`；唯一进入A2的候选C01 SHA `2c2c249310bbdd36fc2c442ce9ded657413934071179a7c3edac5d3c713c5953`。A/B/D仅有本地A3检查，不冒充此case的A2验证。
- 以下只摘同SID的本case值；完整五项、所有候选、方案及A3限制在 [总history](history.md#b2-four-routes-stopped-20261029)。C01含R09=72.00us，未证实稳定改善；真实shape/iters/eps仍未知，见hidden.md。
- R04与R10没有收尾数据，保留未知，不填0；R04长期Running不等于算子错误。E01是用户手动旧代码检查，不纳入候选对照。
- 14:42:41 +08已按用户要求停止，剩余额度冻结；此处补齐历史记录不构成新实验或重试授权。

|轮次|版本|case5耗时(us)|SID|
|---|---|---:|---|
|R01|B2|61.87|6ae2d4691dac5d235b204572|
|R02|B2|59.64|6ae2d4c31dac5d235b20a509|
|R03|B2|60.17|6ae2d51e1dac5d235b21007b|
|R05|C01|60.58|6ae2de861dac5d235b2a7114|
|R06|C01|61.30|6ae2e7541dac5d235b339f94|
|R07|C01|61.51|6ae2e9851dac5d235b370293|
|R08|C01|60.05|6ae2e9e21dac5d235b377117|
|R09|C01|72.00|6ae2ea3f1dac5d235b37d626|

## 2026-10-29T20:30:00+08:00 C6_PackedRowReciprocalMul case5 官方对照

- B2 最新官方 case5=71.15us（SID 6ae31b861dac5d235b662617，member1）；C6_PackedRowReciprocalMul 官方 case5=59.25us（SID 6ae338e11dac5d235b7e95c8，member2），-16.7%。A3 代理 round2/3 对应 case5(H34) 46.14→43.27 / 45.85→43.12 us。
- 同官方测试点更新批次内比较；hidden 逐点仍未公开。C6 紧凑路径行倒数 Mul 收益在 A2 官方复现，未含 C7 劣化项。完整证据见 total history 与 runs_sinkhorn/20261029T121459482672Z_978aed619a15。


<!-- case5-four-routes-ccs-max-20261030-final -->
## 2026-10-30T15:22:18.162178+08:00 case5 四路线 CCS DeepSeek Flash Max 完整结果（待用户选版）

- 父版与正式源保持 case5_compact `2a3e946715f9bb380b55b61a6e68b2113084998e5bfa17723a6a5bef8a5b9a39`，本轮四路各5次、20次A2已结束，等待用户选版。
- 四路线方法、A3范围、失败、完整五项和预算审计见总history本轮条目；本文件按同SID摘取本case，不将代理形状当官方映射。
- 本case所有真实快慢值如下，未拼接跨版本最小值：1/6ae438161dac5d235b4cccff A0_baseline_control_v2=59.67us; 2/6ae43a141dac5d235b4e9e17 A1_softmax_eps_direct_packed=59.74us; 3/6ae43a751dac5d235b4ef578 C1_compact_prefetch=59.23us; 4/6ae43bb01dac5d235b5000f1 B1_blockmajor_flat_br=60.49us; 5/6ae43c1c1dac5d235b5059ee A2_softmax_eps_mask_reuse=60.33us; 6/6ae43c7b1dac5d235b50a63a C2_lookahead_admission=69.68us; 7/6ae43d7c1dac5d235b51800d D1_q8_singlewave_partition=58.83us; 8/6ae43e6b1dac5d235b526575 A1_softmax_eps_direct_packed_repeat=58.9us; 9/6ae43ec31dac5d235b52b77b A2_softmax_eps_mask_reuse_repeat=59.6us; 10/6ae43f5d1dac5d235b5350c3 B2_blockmajor_mask_reuse=59.35us; 11/6ae43fbc1dac5d235b53aff1 C3_post_dequeue_lookahead=59.48us; 12/6ae4401c1dac5d235b540582 D2_q8_multiwave_partition=57.81us; 13/6ae441891dac5d235b559c71 B1_blockmajor_flat_br_repeat=72.53us; 14/6ae441e61dac5d235b55e98c C2_lookahead_admission_repeat=60.55us; 15/6ae442471dac5d235b56359f D1_q8_singlewave_partition_repeat=57.78us; 16/6ae4429f1dac5d235b56825c B2_blockmajor_mask_reuse_repeat=70.97us; 17/6ae442fd1dac5d235b56dbe7 C1_compact_prefetch_repeat=59.14us; 18/6ae4435c1dac5d235b572e31 D2_q8_multiwave_partition_repeat=63.05us; 19/6ae443b51dac5d235b5771b6 B2_blockmajor_mask_reuse_repeat2=70.93us; 20/6ae4440e1dac5d235b57bf42 D0_closing_baseline_control=60.56us.
- 分数是完整15项官方总分的首次成功观测，10项Hidden逐点耗时未知；A3诊断、官方样例、A2总体Pass及最终人工规则核验分层。
- 原始逐SID回执、源码SHA、完整比较见 `/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261030_case5_four_routes_deepseek_4x5/final_comparison.json`；生产不自动覆盖，本轮STOP、pending空、无自动续跑。


<!-- user-retains-case5-compact-after-four-routes-20261030 -->
## 2026-10-30T15:36:51.370142+08:00 用户选择保留 case5_compact 基线

- 用户确认保留原基线 case5_compact，活动源码SHA `2a3e946715f9bb380b55b61a6e68b2113084998e5bfa17723a6a5bef8a5b9a39`，无需源码复制。
- 本case最近已知收尾基线观察为 60.56us（SID `6ae4440e1dac5d235b57bf42`）；完整同SID五项、全部同源快慢与选版依据见总history本次条目及上轮原始比较。
- 本次没有新增正确性或性能实验；选版不将既有观测扩大为稳定性能收益，也不改写旧失败与慢记录。
- 待选标记已解除，STOP保留、pending空、各路剩余0、无自动续跑；本次编译/NPU/平台GET/POST均0。


## 2026-10-30 tree_tail_deepseek_3x7 complete

- 父版与完整SHA、逐SID五项、算法及分层验证见同轮总history；正式版本未自动替换。
- 本case全部实际观察：R01 A0_opening_baseline SID=6ae4593d1dac5d235b69ab44 59.28us score=34.84; R02 A1_dense_column_tree SID=6ae45b0f1dac5d235b6b5eeb 71.1us score=33.9; R03 C1_q8_singlewave SID=6ae45c1e1dac5d235b6c30a0 57.75us score=34.88; R04 A1_dense_column_tree_repeat SID=6ae45c761dac5d235b6c8128 57.32us score=34.64; R05 A2_layered_column_tree SID=6ae45d8f1dac5d235b6d78e3 73.77us score=33.59; R06 C2_tree_singlewave SID=6ae45de81dac5d235b6dbf60 54.78us score=34.82; R07 A2_layered_column_tree_repeat SID=6ae45fa71dac5d235b6f4061 60.77us score=33.54; R08 C1_q8_singlewave_repeat SID=6ae460001dac5d235b6f84ae 61.41us score=34.71; R09 M1_tree_singlewave_repeat SID=6ae460581dac5d235b6fc900 55.7us score=33.59; R10 B1_compact_tail2 SID=6ae460b31dac5d235b7019fd 70.52us score=33.63; R11 A3_fixed32_early_tail SID=6ae462721dac5d235b71a9b0 59.67us score=34.2; R12 M2_fixed32_singlewave SID=6ae462d31dac5d235b720b1d 55.26us score=34.24; R13 B1_compact_tail2_repeat SID=6ae463321dac5d235b726926 72.09us score=33.43; R14 A3_fixed32_early_tail_repeat SID=6ae465431dac5d235b7455dd 59.53us score=34.07; R15 M2_fixed32_singlewave_repeat SID=6ae4659b1dac5d235b74a28d 55.28us score=33.94; R16 C1_q8_singlewave_repeat2 SID=6ae465f31dac5d235b74eed0 58.45us score=34.26; R17 B2_safe_shared_column_gather SID=6ae468b21dac5d235b773716 71.02us score=33.9; R18 C4_latepack_softmax SID=6ae4690b1dac5d235b778648 58.95us score=34.57; R19 B2_safe_shared_column_gather_repeat SID=6ae469651dac5d235b77cd3c 70.98us score=33.97; R20 C4_latepack_softmax_repeat SID=6ae469c01dac5d235b78226f 59.87us score=34.53; R21 M4_unrolled_row_fixed32_singlewave SID=6ae46f2d1dac5d235b7d1d01 55.71us score=34.12; R22 M3_latepack_fixed32_singlewave SID=6ae46f851dac5d235b7d61fe 60.98us score=32.87; R23 M3_latepack_fixed32_singlewave_repeat SID=6ae4703c1dac5d235b7e0105 55.68us score=33.33; R24 M4_unrolled_row_fixed32_singlewave_repeat SID=6ae470941dac5d235b7e4adc 55.31us score=34; R25 C0_closing_baseline SID=6ae470ed1dac5d235b7ea777 59.62us score=34.38。
- 分数是对应SID评测后首次观测，包含隐藏项，不能由公开五项重算。保留同SHA慢记录，不因单次最好值判定稳定收益。
- STOP已设，未用额度冻结，待用户选版；原始JSON/CSV：`/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261030_case5_tree_tail_deepseek_3x7`。


## 2026-10-30 用户选定 M2 为正式基线

- 选定完整M2源码 `5b87987c98156bbba80ab73665e71a5e593a8e8f849eb6dc4e7ab2f8fec16676`；本case两次官方耗时为 55.26 / 55.28 us。
- 两次完整五项、SID、分数与选版审计见总history同节；本次没有新增设备验证或提交。
- 正式源码已切换，STOP与旧额度冻结；平台最新成绩仍对应旧基线最后回执。


<!-- M2-next-case5-plan-20261030-complete -->
## 2026-10-30T19:29:58.613858+08:00 M2基线下一轮case5方案完成（未执行）

- 正式基线维持 M2 `5b87987c98156bbba80ab73665e71a5e593a8e8f849eb6dc4e7ab2f8fec16676`；两次官方case5=55.26/55.28us，进入50us需再减少大于5.27us、约9.54%。本次只读/CPU分析，新增候选/编译/NPU/平台GET/POST均0，既有三路分析agent已结束并关闭。
- 父端决策：P1双相位行分母为主攻，P3行归约根地址重排次之，P2连续Counter窗口辅助。P1两份相同分母错开256B、行跨度768/512B，仅多一次Brcb；P3保持原Add树且无新增BR/Add/barrier；均复用失活scratch。P2明确Brcb前SetMaskNorm，保留依赖屏障。
- 证据边界：P1/P3已对H33..48、所有32B基址相位做地址模型，峰值30944/10976B均在原scratch内；这不是设备速度证据。官方case5形状未知，A3代理不代表A2。因子化仍需两次H平方加权归约；完整列树着色缺完整映射/UB证明，暂不进入首轮。
- 下一轮建议先I0等算术独立入口控制，再P1/P3/P2独立和有效融合；保留实际iters、FP32、每次eps、nativeDiv、单kernel、输入只读，要求参考与M2逐位检查、配对全核计时及官方复测。建议上限12次（对照2、I0 2、三组件各2、融合2）仅为计划，原STOP和旧未用额度继续冻结，无自动执行授权。
- 完整方案与三个审查结果：`/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_M2_case5_next_20261030/next_round_plan.json`；地址模型、源码/SDK依据与淘汰条件同目录。当前状态中遗留的旧B2验证/SID字段已按M2证据纠正，旧值保存在`superseded_current_metadata.json`，不改写既有提交回执。


## 2026-10-30 M2_bank_counter_deepseek_3x7 complete

- 父版与完整SHA、逐SID五项、算法及分层验证见同轮总history；正式版本未自动替换。
- 本case全部实际观察：R01 A0_M2_open SID=6ae482fd1dac5d235b8fc3f5 55.19us score=33.71; R02 I0_isolated_M2 SID=6ae4852e1dac5d235b91eca9 56.27us score=33.68; R03 A1_dual_phase_den SID=6ae485881dac5d235b924719 54.31us score=33.65; R04 C1_counter_windows SID=6ae485f51dac5d235b92a9ce 56.11us score=33.41; R05 B2_colored_row_roots_fixed SID=6ae486691dac5d235b931d92 55.46us score=34.14; R06 A2_dual_phase_isolated SID=6ae486cc1dac5d235b937da7 54.45us score=33.79; R07 A2_dual_phase_isolated_repeat SID=6ae487de1dac5d235b947240 54.11us score=33.62; R08 A1_dual_phase_den_repeat SID=6ae488361dac5d235b94bee6 54.24us score=33.43; R09 B2_colored_row_roots_fixed_repeat SID=6ae4888f1dac5d235b950ebb 54.8us score=34.02; R10 C1_counter_windows_repeat SID=6ae488e71dac5d235b957189 56.04us score=33.38; R11 B0_M2_mid SID=6ae4894b1dac5d235b95d358 55.6us score=33.83; R12 F1_AB_direct SID=6ae489a51dac5d235b963353 53.65us score=33.85; R13 F2_AB_isolated SID=6ae48a041dac5d235b9691a7 54.85us score=33.95; R14 C2_counter_isolated SID=6ae48a631dac5d235b96e983 56.9us score=33.92; R15 B3_colored_roots_isolated SID=6ae48ac61dac5d235b9749cc 55.68us score=32.98; R16 A3_single_phase_den SID=6ae48b211dac5d235b97a463 59.9us score=33.44; R17 F3_ABC_isolated SID=6ae48b7c1dac5d235b98013d 54.32us score=34.35; R18 A3_single_phase_den_repeat SID=6ae48c191dac5d235b98b107 53.8us score=33.89; R19 B3_colored_roots_isolated_repeat SID=6ae48c7c1dac5d235b9917f4 55.43us score=33.45; R20 F1_AB_direct_repeat SID=6ae48ce51dac5d235b9993aa 53.27us score=33.98; R21 F2_AB_isolated_repeat SID=6ae48d3f1dac5d235b9a0140 54.02us score=33.17; R22 F3_ABC_isolated_repeat SID=6ae48d9b1dac5d235b9a623d 54.1us score=33.72; R23 C3_column_counter_isolated SID=6ae48dfb1dac5d235b9ad33e 56.97us score=32.86; R24 C3_column_counter_isolated_repeat SID=6ae48e571dac5d235b9b7566 57.33us score=32.38; R25 F3_ABC_isolated_repeat2 SID=6ae48f081dac5d235b9c98b9 54.7us score=34.08; R26 C0_M2_close SID=6ae48fa21dac5d235b9d53aa 55.32us score=33.73。
- 分数是对应SID评测后首次观测，包含隐藏项，不能由公开五项重算。保留同SHA慢记录，不因单次最好值判定稳定收益。
- STOP已设，未用额度冻结，待用户选版；原始JSON/CSV：`/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261030_M2_bank_counter_deepseek_3x7`。


<!-- F1-selected-case5-next-plan-20261030 -->
## 2026-10-30T21:41:45.711488+08:00 用户选择 F1 为正式基线

- 用户明确选择 F1_AB_direct，正式源码由 M2 `5b87987c98156bbba80ab73665e71a5e593a8e8f849eb6dc4e7ab2f8fec16676` 切换为 `4e74fab52bdf7226d628b04e768c8d171d6ecd3cf62c48a5092481b0eeb74659`；复用不可变官方提交快照。
- 既有官方证据：SID 6ae489a51dac5d235b963353 case5=53.65us 首次分数=33.85；SID 6ae48ce51dac5d235b9993aa case5=53.27us 首次分数=33.98。分数为评测后首次采集，非提交瞬间值。
- 核对两次Pass、服务端全8文件绑定、候选175组设备验证与M2逐位一致；本次仅复制已验证源码，新增编译/NPU/POST均0。七个保护文件不变。
- 旧STOP与剩余额度维持冻结；平台最新记录仍是M2收尾SID，未冒称已重新提交F1。接下来只做方案分析，选版审计与下一轮JSON见 `/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_F1_case5_next_20261030`。


<!-- F1-next-case5-plan-20261030-complete -->
## 2026-10-30T22:05:48.548204+08:00 F1下一轮case5方案完成（未执行新候选）

- 正式基线F1 `4e74fab52bdf7226d628b04e768c8d171d6ecd3cf62c48a5092481b0eeb74659`，两次官方case5=53.65/53.27us，中位数53.46us。进入50us需减少6.47%，到35us需减少34.53%。21:59榜单剔除失败/零耗时后29队有效，其中14队case5<40us，最快当前Pass为30.57us；排行榜不能揭示对手实现或官方shape。
- 主攻P1列树scratch按层错位：保留原六级算术和屏障，无额外逐元素Add/Copy/UB；337920个CPU向量窗口检查通过，峰值38624B，后四级读group不重叠。代价为每列阶段多4/5条API，首级冲突仍在，必须测整核净收益。
- P2 q4双行compact已对8个偶数H证明布局和原树，BR/Brcb重复数由H到H/2，但列倒数需2Copy+1屏障；只在输出对齐与核数/波数成本满足时考虑。P3分别合并pre/post输入、提前gate输出重叠、将softmax最后+eps直接写packed，先单独归因再融合。P4 lane重排+硬件归约仅候补，尚无完整实现与速度证据。
- 当前数值约束继续保持F1运算树、实际iters、所有eps、FP32/nativeDiv、单kernel、输入只读。Counter/仅入口拆分/简单Gather不重试；因子化仍需两个H平方加权归约，不承诺自然进入30多us。详细API、地址模型、负证据和准入门槛见 `/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_F1_case5_next_20261030/next_round_plan.json`。
- 本次仅选版、只读API/文档/源码与CPU符号分析，新增候选/编译/NPU/POST均0；STOP、26次原账及剩余B2次冻结不变。建议下一轮初始上限14次仅为计划，不启动worker或复用旧授权；未知参数仅在hidden.md管理。


## 2026-10-30 F1_col_q4_io_deepseek_3x7 complete

- 父版与完整SHA、逐SID五项、算法及分层验证见同轮总history；正式版本未自动替换。
- 本case全部实际观察：R01 A0_F1_open SID=6ae4a8cb1dac5d235bb86ba9 53.9us score=34.03; R02 C1_gate_pair SID=6ae4a9451dac5d235bb8dfe1 53.72us score=33.71; R03 A1b_colscratch SID=6ae4aa711dac5d235bba11c7 52.39us score=34.54; R04 C2_early_gate_store SID=6ae4ab301dac5d235bbaefe4 53.08us score=33.91; R05 A1b_colscratch_repeat SID=6ae4ab8a1dac5d235bbb7054 54.66us score=34.35; R06 C3b_softmax_eps_pack SID=6ae4accb1dac5d235bbd5546 54.22us score=33.63; R07 A2_cachedlayout SID=6ae4ad251dac5d235bbdb675 60.72us score=33.52; R08 C4_io_pack SID=6ae4ae861dac5d235bbf3780 54.88us score=33.5; R09 M1_A1b_C2 SID=6ae4aee21dac5d235bbf9b5b 53.69us score=34.03; R10 C2_early_gate_store_repeat SID=6ae4af3f1dac5d235bbffc04 59.53us score=32.99; R11 C6_F1_drift SID=6ae4afd61dac5d235bc0aa7f 53.27us score=33.88; R12 A3_constpitch SID=6ae4b1f61dac5d235bc2ecbc 59.92us score=33.22; R13 A4_ones_phase SID=6ae4b38a1dac5d235bc4f445 54.13us score=33.07; R14 A1b_colscratch_third SID=6ae4b45e1dac5d235bc5da0e 58.94us score=33.78; R15 C7_F1_close SID=6ae4b6971dac5d235bc82cdd 53.9us score=33.51。
- 分数是对应SID评测后首次观测，包含隐藏项，不能由公开五项重算。保留同SHA慢记录，不因单次最好值判定稳定收益。
- STOP已设，未用额度冻结，待用户选版；原始JSON/CSV：`/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261030_F1_col_q4_io_deepseek_3x7`。

<!-- F1-selected-post-colq4io-analysis-complete -->
## 2026-10-31T00:20:41.482734+08:00 F1选定与case5下一轮分析（仅方案）

- 用户选择并保留F1，完整SHA `4e74fab52bdf7226d628b04e768c8d171d6ecd3cf62c48a5092481b0eeb74659`；正式源码原本已匹配，无需复制；SID `6ae4b6971dac5d235bc82cdd`，评测后首次同SID分数33.51。该case最近F1同SID耗时53.90us；本轮未新增测试。
- case5当前3次F1为53.90/53.27/53.90us，中位数53.90；进入50需再省>3.90us（>7.2356%），工程目标49us。A1b/C2单次最好值不稳定，旧q4占核前提不成立，不重扫同类相位/搬运方案。
- 新主线A：列归约前3级不动，8根按[0,4,2,6,1,5,3,7]转置后BR，6→5调用与屏障，但每列阶段多5120/6144B逻辑UB流量；地址表可复用原死matrix末段256B。次线B：packed按token做8条strided WR，9/11→8调用、4→1屏障；短WR吞吐可能反向变慢。只融合独立获益者；16根WR因320/384短repeat降级候补。
- 验证仅CPU：16个H的有序树、48组地址、135168转置搬运、212672行元素、4096组地址表phase检查通过；这是源码分支域分析，不认定官方shape。masked FP32树/符号零仍需设备逐位核验；A3计数器只作诊断。计划与API/SDK原文证据：`/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_F1_case5_after_colq4io_20261030/next_round_plan.json`。
- 本次候选实现/编译/NPU/POST/新子代理均0；8个正式文件与F1快照一致，STOP不变，旧A7/B0/C7/M1共15次及剩余B7/M6冻结，pending为空。选版已确认；下一轮未启动，当前基线仍F1。


<!-- F1-treefusion-deepseek-3x7-complete -->
## 2026-10-31T01:39:54.415354+08:00 F1_treefusion_deepseek_3x7 完成，待用户选版

- 本轮正式case5逐提交耗时（us，序号对应history.md完整SID表）：1:A0_F1_open=53.85；2:A1_col8_scalar_addr=53.65；3:C0_F1_mid=59.20；4:A3_normal64_tree=52.35；5:A1_col8_scalar_addr_repeat=53.27；6:A3_normal64_tree_repeat=51.95；7:A4_normal64_full_column=58.58；8:C4_row_normal_mask_reuse=53.51；9:M1_A4_C4=53.45；10:A4_normal64_full_column_repeat=53.41；11:C4_row_normal_mask_reuse_repeat=53.95；12:M1_A4_C4_repeat=53.35；13:M2_row_count_reuse=53.80；14:C1_F1_late_control=53.46；15:M3_A3_row_counter=57.43；16:M3_A3_row_counter_repeat=52.07；17:C2_F1_close=53.87。
- 当前正式F1收尾case5=53.87us，SID `6ae4d6091dac5d235beb9e30`；代码SHA `4e74fab52bdf7226d628b04e768c8d171d6ecd3cf62c48a5092481b0eeb74659`。
- 所有正式记录均保留，包括同源码慢测；A3代理形状不是已确认官方形状，十隐藏项不可见。
- 建议继续保留F1作为正式基线。A3是本轮最值得保留研究的case5候选，两次为52.35/51.95us，但case4升至76.11/77.68us，未证明整体稳定改善；M3复测虽到52.07us，两次分数32.86/32.84，融合没有形成更好的综合版本。本轮未实现case5低于50us。；正式源码未切换，等待用户选择。
- 证据 `/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261031_F1_treefusion_deepseek_3x7/final_comparison.json` 与 `results.csv`；配额、间隔、源码及STOP审计通过。


<!-- F1-issue-bulk-deepseek-3x7-complete -->
## 2026-10-31T03:54:53.345490+08:00 F1_issue_bulk_deepseek_3x7 完成，待用户选版

- 本轮正式case5逐提交耗时（us，序号对应history.md完整SID表）：1:C0_F1_open=53.21；2:A1_column_mul_unroll=51.79；3:A1_repeat2=57.92；4:A2_row_loops_unroll=53.16；5:B2_bulk_input_gather_lifecycle=47.99；6:C1_idle_gate_cores=57.22；7:B2_repeat2=47.81；8:M1_A1_B2=51.96；9:C0_F1_mid=53.78；10:M1_repeat2=46.37；11:B4_seed8_fanout=46.82；12:B4_repeat2=52.56；13:C3_balanced_idle_gates=56.44；14:M3_A1_B4=53.98；15:B2_repeat3=46.82；16:A1_repeat3=53.32；17:C0_F1_late=59.06；18:M1_repeat3=47.27；19:C0_F1_close=53.31。
- 当前正式F1收尾case5=53.31us，SID `6ae4f51f1dac5d235b059860`；代码SHA `4e74fab52bdf7226d628b04e768c8d171d6ecd3cf62c48a5092481b0eeb74659`。
- 所有正式记录均保留，包括同源码慢测；A3代理形状不是已确认官方形状，十隐藏项不可见。
- 建议本轮B2连续输入搬运版：三个固定轮换账号的case5均低于50us，分别47.99/47.81/46.82us，中位数47.81us；包含全部慢测的F1中位数53.545us，case5中位数改善10.71%，case4中位数改善5.51%。B2分数中位数33.01，F1为33.07；这是面向case5目标与公开case4收益的推荐，并非总分最优保证。正式基线继续F1，最终保留版本由用户决定；正式源码未切换，等待用户选择。
- 证据 `/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261031_F1_issue_bulk_deepseek_3x7/final_comparison.json` 与 `results.csv`；配额、间隔、源码及STOP审计通过。


## 2026-10-31 B2 baseline selected; under40 analysis
- 用户明确保留本轮 B2_bulk_input_gather_lifecycle；正式 kernel.asc 已切换至 SHA 870259fd7968eb6842f47ac6a9ac93d768558abf875358863030cf57c1dc4f67，其余七个正式文件哈希不变。
- B2 三次正式 case5 为 47.99/47.81/46.82 us，中位数47.81 us；对应提交完成后首次可见分数32.95/33.60/33.01。进入40 us还需相对中位数减少7.81 us以上。
- 三次B2官方Pass及337项本地A3验证沿用精确同SHA证据；本次为源码选定，未新增编译、NPU验证或POST。平台latest仍是上一轮F1收尾提交，不能写成已更新排行榜。
- 上轮19次POST账本、STOP与剩余9次冻结额度保持不变；本轮仅分析，记录 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261031_B2_under40/selection.json。


## 2026-10-31 B2 under40 bottleneck analysis complete
- B2基线SHA870259fd7968保持；官方case5中位47.81us，进入40us需再省7.81us以上/16.34%以上。本次0 POST，0新算法候选。
- 完成原样B2/F1的10组合成A3迭代斜率ABBA及B2两类PMU采集，共6次profiling/2160次完整调用；输出容差与input只读全部通过。B2 I7–32约1.23us/轮、Vector约1.1485us/轮；H34I15 bank-group约9.9%多核/11.7%单核，指标不可相加或外推A2。
- 下一轮优先：末列Mul直接输出token-major使24条DMA变3条；再比较GatherMask去padding后的连续写回；初始softmax最后eps与pack融合；列归约scratch分半着色但保持有序加法树。地址和表达式证明已做，尚无设备候选性能证据，不宣称已达40us。
- 分析与原始证据：/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261031_B2_under40/analysis.json；旧轮19次POST及未用9次预算冻结，analysis STOP保留。


## 2026-10-31 B2 output-bank-pack campaign completed
- 三个 ccs-deepseek/deepseek-flash High 子代理完成输出批量写回、列归约UB着色、softmax与pack融合；父端审查并正式POST 18 次，全部Pass。A/B/C/M用量 5/4/4/5，各上限5；仅member1/member2交替，member3为0。
- case5全部同提交官方观测（us）：C0_B2_open=53.82; B1_column_colored=47.51; A1_tokenmajor_3dma=47.60; C1b_eps_pack_fixed=53.92; C1b_repeat2=53.14; A2_dense_output=47.20; B0_B2_mid=47.92; M1_AC=46.98; A3_dense_fast_pattern=44.44; A3_repeat2=44.40; B1_repeat2=47.70; M2_A3C=47.60; A3_repeat3=45.54; M2_repeat2=45.88; M1_repeat2=46.98; B0_B2_late=47.24; M2_repeat3=46.63; C0_B2_close=52.01。保留慢测；分数为完成后首次成功读取，完整五项/分数/提交ID见results.csv。
- 所有正式新候选先通过111+162+64项本地A3逐位/输入只读检查，再经固定快照官方样例与服务端8文件SHA绑定。C1首版本地失败未POST；B路线只着色首层变体无诊断收益未晋级。A3诊断不是A2官方或隐藏shape证据。
- 父端建议：推荐 A3_dense_fast_pattern 作为继续压低case5的下一轮版本，等待用户选择，当前生产仍保留B2；A3三次case5为44.44/44.40/45.54us，中位44.44us，相对本轮B2全部四次中位49.965us降低11.06%；B2慢测保留，A3三次也均快于B2最快的47.24us。主要代价是case4中位74.00us（B2为70.395us），首次观测分数中位32.60（B2为32.745）。本轮未达到40us，不宣称总分收益。正式源码始终B2(870259fd7968eb6842f47ac6a9ac93d768558abf875358863030cf57c1dc4f67)，本轮收尾也提交精确B2，最终版本由用户选择。
- 当前STOP已设置，pending为空，未用2次冻结、不自动续跑；旧轮STOP及未用9次保持。证据 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261031_B2_output_bank_pack_deepseek_3x5/final_comparison.json、control/final_audit.json 和 results.csv。


## 2026-10-31 A3 baseline selected; under40 analysis
- 用户明确保留A3_dense_fast_pattern；正式kernel.asc已切换到SHA b35e7a8a3f52d856243c2e3ed518636d7aa83dc077de7e3a95d89cf9751fd508，其他七个正式文件哈希不变。
- case5三次官方同SHA观测为44.44/44.4/45.54us，中位44.44us；完整五项与分数沿用上轮固定回执，不拼接最小值。
- 复用精确A3的337项本地验证及三次A2 Pass证据；本次选择未新增POST，平台latest仍是B2收尾，不能说排行榜已切换A3。
- 旧轮18次POST、STOP与未用2次保持冻结，更早9次也不恢复；本轮仅分析/原样诊断，选版证据 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261031_A3_under40/selection.json。


## 2026-10-31 A3 under40 diagnosis completed
- A3正式源码SHA b35e7a8a3f52d856243c2e3ed518636d7aa83dc077de7e3a95d89cf9751fd508及其他七文件核验未变；本轮仅分析，0次新POST、0个优化候选。
- 原样B2/A3 ABBA：H34/I15/N256代理MTE3由约5us降至0.52~0.72us，迭代I7..32斜率仍约1.23us/轮；主攻迭代归约和mask控制，非继续押注输出尾部。
- 6次本地A3 profiler、2个原样源码二进制、2160次完整kernel调用；输出/输入只读检查通过。PMU冲突比例不可等同耗时损失，MemoryUB多核耗时受采集影响；不能推断官方case5形状或40us已达成。
- 下一轮优先mask驻留、单条批量行BR；另探索保持原树的两级列BR（需先筛Gather/UB成本），门控批量/提前写回作补充；保留原FP32树、native Div、每次eps和实际iters。静态地址枚举H33..42通过，尚无候选设备正确性或性能证据。
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
| A0_A3_open | 44.88 | 32.75 | 6ae57f5e1dac5d235b70dab3 |
| A1_column_counter_mask | 44.00 | 32.52 | 6ae580cc1dac5d235b7268ff |
| A2_column_row_counter_fusion | 43.22 | 32.73 | 6ae5836f1dac5d235b74f218 |
| A2_repeat2 | 43.81 | 32.99 | 6ae584cb1dac5d235b766a57 |
| B1_dense_flat_br_h33_42_v4 | 46.87 | 32.36 | 6ae586391dac5d235b788359 |
| A2_repeat3 | 43.97 | 32.46 | 6ae587b41dac5d235b7a1e04 |
| M1_A2_B | 43.97 | 32.87 | 6ae588a61dac5d235b7b6555 |
| B2_spaced_roots_gap6_5_v1 | 46.83 | 32.04 | 6ae58afa1dac5d235b7e5584 |
| M2_A2_gate | 44.82 | 32.81 | 6ae58bff1dac5d235b7f919d |
| M1_repeat2 | 42.22 | 32.60 | 6ae58c9a1dac5d235b804726 |
| M1_repeat3 | 44.93 | 32.74 | 6ae58d401dac5d235b80fbf7 |
| M2_repeat2 | 44.21 | 32.86 | 6ae58dd01dac5d235b81adf5 |
| C0_B2_close | 53.90 | 32.30 | 6ae58e601dac5d235b825890 |


## 2026-10-31 用户选择A2为基线，启动剩余瓶颈分析
- 用户明确选择A2_column_row_counter_fusion，正式源码从B2恢复为精确SHA 82e983326ae960963ac7365aca88f43672e051f3e3ed92ee0b431fac1c7a4b24，七个保护文件不变。
- 本case同SHA三次耗时：43.22/43.81/43.97us；完整五项与SID见总history本次选版记录。
- 复用该SHA的337项本地逐位一致性、输入只读和三次官方Pass证据；本次选版0次POST，最新平台提交仍为上一轮B2收尾，不冒充已上传A2。
- 旧STOP、账本、比较报告及未用7次保持冻结；本次只分析与原样源码诊断，不启动候选开发或正式提交。选版审计：/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261031_A2_under40/selection.json。


## 2026-10-31 A2剩余瓶颈分析完成
- A2正式case5三次43.22/43.81/43.97us，中位43.81；本次未新提交。
- 原样源码本地A3诊断并未识别官方shape；统计与瓶颈边界见总history同名记录。
- 下一轮主攻失活index缓冲复用与设备索引倍增；CPU表达式/地址证明已保存，候选实现和设备收益待验证。
- 生产A2保持，旧STOP/未用7次冻结；完整方案和证据：/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261031_A2_under40/analysis.json。


## 2026-10-31 A2缓冲/索引/布局轮结束：保持A2，等待用户选版
- 三个DeepSeek Flash High子代理，父端审核决策；共15次正式POST，A/B/C/M用量2/5/5/3（各上限5）。全部Pass且服务端八文件绑定匹配；member1/member2严格交替，member3未用；本轮剩余5次冻结，旧7次仍冻结。
- 三路实现、失败、止损和融合决定详见/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261031_A2_reuse_index_layout_deepseek_3x5/final_comparison.json的route_decisions及candidate_inventory；本地337项逐位一致/输入只读与完整A3 ABBA不冒充官方A2性能。
- 推荐M1_RC3_RB2_index_doubling，理由：综合表现推荐M1融合版，但不把它称为case5优化成功：本轮同SHA三次中位数，M1的case1/2/3/4为475.57/2.20/15.75/68.53us，A2三次对照为478.40/2.22/15.81/70.58us；M1的case5中位43.93us，反而比A2的43.63us慢0.30us，均未低于40us。M1后段首次观测分数31.79/31.97/32.17，邻近A2对照31.74/31.71，显示综合成绩的正向信号；但TBest在轮内变化，不能保证固定幅度的总分收益。若用户只以case5为取舍标准，A2仍更合适。生产保持A2，M1仅推荐，最终由用户选择。；推荐不自动采用，最终由用户选择。全部同SID五项耗时、分数和复测慢记录见下表；case5目标是否达成以final_comparison为准。
- 生产仍为A2 SHA 82e983326ae960963ac7365aca88f43672e051f3e3ed92ee0b431fac1c7a4b24；末次A2对照SID 6ae5a9781dac5d235ba48acd，case5=43.63us，首次观测分数31.71。七个保护文件及旧轮STOP/账本/分析均未变。
- 分数为完成后首次成功读取的同SID官方值，并非提交瞬间分数；本轮TBest发生变化，尤其case1从334.85降至262.27us，分数变化不能全部归因于候选。STOP已写入，停止自动继续，保留所有失败和慢记录。

| 版本 | 本case耗时(us) | 分数 | SID |
|---|---:|---:|---|
| A0_A2_open | 43.16 | 33.04 | 6ae59d941dac5d235b95a05b |
| RB1_row_prefix | 44.16 | 32.93 | 6ae59f971dac5d235b982564 |
| RA1_index_reuse_mul_pingpong | 45.80 | 32.43 | 6ae5a0851dac5d235b993b59 |
| RB2_full_doubling | 43.71 | 33.19 | 6ae5a1bf1dac5d235b9aa70f |
| RB2_repeat2 | 43.07 | 32.50 | 6ae5a26b1dac5d235b9b709f |
| RB3_hybrid_flat8 | 45.78 | 31.51 | 6ae5a3191dac5d235b9c41ab |
| RC3_compact_helpers_only | 43.24 | 32.06 | 6ae5a3fe1dac5d235b9d5b4c |
| RB2_repeat3 | 45.09 | 31.65 | 6ae5a45c1dac5d235b9dd7ee |
| RC3_repeat2 | 44.61 | 32.01 | 6ae5a50a1dac5d235b9eaba3 |
| RC3_repeat3 | 46.40 | 31.98 | 6ae5a5ce1dac5d235b9f8f2b |
| M1_RC3_RB2_index_doubling | 43.97 | 31.79 | 6ae5a6fd1dac5d235ba1055a |
| C0_A2_mid | 44.26 | 31.74 | 6ae5a79e1dac5d235ba1f145 |
| M1_repeat2 | 42.83 | 31.97 | 6ae5a8731dac5d235ba33b58 |
| M1_repeat3 | 43.93 | 32.17 | 6ae5a8cd1dac5d235ba3b120 |
| C0_A2_close | 43.63 | 31.71 | 6ae5a9781dac5d235ba48acd |


## 2026-10-31 用户选择M1为基线并分析剩余瓶颈
- 生产源码由A2切换为用户选定M1 SHA 3c8f646d971e4a4750eaa68e7ddc1e5bb5f706bc060376221559d94aa4722075，七个保护文件不变。
- 本case同SHA三次耗时：43.97/42.83/43.93us；完整五项与SID见总history本次选版记录。
- 复用337项本地逐位/只读验证与三次官方Pass；本次选版0次POST，最新平台提交仍为上一轮A2收尾。
- 旧轮STOP、账本及未用5次冻结；本次分析和原样诊断，不开发优化候选或正式提交。选版审计：/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261031_M1_under40/selection.json。


## 2026-10-31 M1剩余瓶颈分析完成（无新优化提交）
- M1 SHA 3c8f646d971e4a4750eaa68e7ddc1e5bb5f706bc060376221559d94aa4722075 保持，正式case5三次43.97/42.83/43.93us，中位43.93us；距40us需再省3.93us（8.95%），本轮没有达标候选。
- 原样A2/M1完整kernel ABBA和M1冲突计数器共1800次A3合成代理调用；各组前后校验/输入只读通过。I7..32单批M1 task斜率1.2323~1.2351us/轮、Vector1.1521，对照A2约1.23/1.1485；Scalar由约0.289降至0.117~0.118。改善主要在控制/固定成本，未降低主循环斜率。I4的task异常保留，原因未定，不称分派切换。
- 新线索：P40/H33..39专门化full尾BR被masked尾BR覆盖；仅源码层结论，ISA解码为not available。下一轮先做最小消融，再研究行Mul直接写列树首层两个输入错相的布局；交替block-major仅备选，必须解决根着色回退和额外Mul发射成本。H33..48地址双射/22528组phase检查为CPU证明，不是候选性能。
- 本轮0子agent、0优化候选、0正式POST；生产及七个保护文件核验不变，旧STOP/账本/冻结5次不变，不自动继续。完整分析、计时、限制及计划：/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261031_M1_under40/analysis.json。


## 2026-10-31 M1重复BR/首层错相/交替布局轮结束：保持M1，等待用户选版
- 三个DeepSeek Flash High子代理启动，C路升级为同模型Max接替；父端审核与提交。共10次正式POST，A/B/C/M用量5/2/3/0（各上限5）；仅member2/member1严格交替，未使用member3。本轮未用10次及旧5次均冻结。
- 三路正确性失败、性能负结果、版本筛选和融合决定保存在/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261031_M1_br_skew_alternate_deepseek_3x5/final_comparison.json及candidate_inventory.json；本地A3验证与诊断不代替官方A2性能。
- 推荐RA1_remove_redundant_br，理由：以case5为优先目标推荐RA1：四次正式Pass的case5为42.26/43.05/41.99/42.37us，中位数42.315us；同轮三次M1对照中位数44.26us，约降低4.39%。B/C正式退化，不融合。RA1的case1/case4中位数略慢，且后段分数31.63与M1收尾31.64接近，因此不宣称稳定总分领先；本轮未达到40us。生产M1不变，等待用户选择。；尚未采用，由用户选择。全部同SID正式耗时和分数见表，慢记录不删。是否达到40us目标见final_comparison.json。
- 生产仍为M1 SHA 3c8f646d971e4a4750eaa68e7ddc1e5bb5f706bc060376221559d94aa4722075，末次本轮M1对照SID 6ae5c3971dac5d235bc57dfe，case5=44.26us；正式八文件和七个保护文件、旧轮不可变记录均核验一致。STOP已写入，不自动继续。
- 分数为完成后首次成功观测的同SID官方值；榜单被队内其他提交覆盖而未采集到的分数记为缺失，不填入其他版本分数，也不从公开五项推算隐藏总分。

| 版本 | 本case耗时(us) | 分数 | SID |
|---|---:|---:|---|
| A0_M1_open | 45.05 | 31.71 | 6ae5b6281dac5d235bb4e306 |
| RA1_remove_redundant_br | 42.26 | 32.04 | 6ae5b8eb1dac5d235bb8ad34 |
| RA1_repeat2 | 43.05 | 32.09 | 6ae5ba231dac5d235bba3893 |
| B0_M1_mid | 43.01 | 未采集 | 6ae5bbb91dac5d235bbc3b75 |
| RA1_repeat3 | 41.99 | 32.04 | 6ae5bc7d1dac5d235bbd1780 |
| RB1_first_level_input_skew_v3 | 50.13 | 31.35 | 6ae5be4d1dac5d235bbf3f40 |
| RC2_correct_block_offsets | 47.94 | 31.24 | 6ae5c01e1dac5d235bc1651e |
| RA1_repeat4_late | 42.37 | 31.63 | 6ae5c1471dac5d235bc2d446 |
| RC4_combined_first4_br | 49.02 | 30.89 | 6ae5c3001dac5d235bc4c8d8 |
| C0_M1_close | 44.26 | 31.64 | 6ae5c3971dac5d235bc57dfe |


## 2026-10-31 用户选择RA1基线，开始剩余瓶颈分析
- 已按用户明确选择将生产源码由M1 3c8f646d971e4a4750eaa68e7ddc1e5bb5f706bc060376221559d94aa4722075切换到RA1 84948804f38c5f0a17541e4138f1186bda0ad0432484bb014e0ccc27fe112a05，生产只读，七个保护文件未变。
- 同SHA四次官方Pass，case5=42.26/43.05/41.99/42.37us，中位42.315us；完整五项和分数沿用上一轮原始记录，不重写为新成绩。
- 复用337项逐位/输入只读验证和四次官方源码绑定；本次选版0次POST。最新已知平台提交仍是M1收尾，已与当前生产RA1区分。
- 旧轮STOP、账本、报告及剩余10次保持冻结，旧5次仍冻结。本次只分析并给出下轮方案。选版审计：/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261031_RA1_under40/selection.json。


## 2026-10-31 RA1剩余瓶颈分析完成（无新提交）
- RA1生产SHA84948804f38c5f0a17541e4138f1186bda0ad0432484bb014e0ccc27fe112a05不变；四次历史case5中位42.315us，低于40需再省超过2.315us，按慢样本留余量约3.1us。
- 复查旧A3斜率：task约1.196–1.201us/iter，vector约1.117us/iter；优先降低循环内向量归约成本，同时补查多核/首样固定开销。未取得指令级冲突或I-cache证据，不据此认定成因。
- 下轮主线A将列树scratch每64个float按72跨度存储，保持6个Add/6层屏障且无额外Copy/Mul；B用单个256B间隔作对照（6→7个Add）；C仅Gather前四块归约根并保留RA1着色合并，先证明额外成本净收益。A/B择优后才考虑与C融合。
- CPU符号树/边界/16相位校验覆盖H33..40，非设备正确性与性能证据；完整归约错相、密集根布局、交替整矩阵、gate批处理等旧负结果已核对。保持原FP32树/eps/Div/迭代和输入只读。
- 分析报告及证据：/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261031_RA1_under40/analysis.json；本轮0候选、0编译、0NPU、0POST，STOP，旧10+5次仍冻结，未授权自动进入下一轮。



## 2026-10-31 RA1三路stride/gap/roots轮次完成，待用户选版
- 本轮保持RA1基线84948804f38c5f0a17541e4138f1186bda0ad0432484bb014e0ccc27fe112a05；完整方法、负结果、预算及五项对照见history.md本轮条目。
- 下表为本case所有正式同SID观测，不择优拼接；A3配对profile只作诊断。
- 生产及官方保护文件未变；全部正式候选经337项逐位/输入只读验证和父端复核，SC2仅111项并因本地退步未提交。
- 推荐及选版状态：面向本轮case5目标，推荐SA1v2_col_scratch_stride9作为候选：两次官方41.97/41.87us，中位41.92us，本轮RA1三次中位43.16us，改善约2.87%；但case4中位70.355us对RA1的68.90us有回退，且分数31.44/31.67未证明稳定总分领先。本轮未达40us，RA1生产保持不变，由用户最终选择。；待用户选择。
- 原始证据：/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261031_RA1_stride_gap_roots_deepseek_3x5/final_comparison.json；STOP，剩余冻结，无自动继续。

|版本|耗时(us)|分数*|SID|
|---|---:|---:|---|
|A0_RA1_open|43.16|31.61|6ae5d3561dac5d235bd7bd49|
|SB1_single_gap256|45.72|30.80|6ae5d6051dac5d235bdb045a|
|SA1v2_col_scratch_stride9|41.97|31.44|6ae5d6f01dac5d235bdc0fee|
|SA2_col_scratch_stride15|44.23|31.08|6ae5d8bc1dac5d235bde347a|
|B0_RA1_mid|42.31|31.67|6ae5d9ea1dac5d235bdfb8e0|
|SA3_stride9_compiletime|45.01|31.49|6ae5dce41dac5d235be3258b|
|SA1v2_repeat2|41.87|31.67|6ae5ddfc1dac5d235be46e77|
|C0_RA1_close|44.47|31.15|6ae5de6b1dac5d235be4fad6|


## 2026-10-31 用户选择SA1v2基线并分析剩余瓶颈
- 生产源码由RA1切换为SA1v2 17c145dd6fb8b788b64e7f316e25b83eb36b6cc5d0d40a36caf8013c4efea51d；七个保护文件不变，保留只读。
- 同SHA两次官方Pass，五项分别478.87/2.17/16.01/70.50/41.97us（31.44分）及476.34/2.13/15.82/70.21/41.87us（31.67分）；case5中位41.92us，尚未低于40。
- 复用337项逐位/输入只读证据及两次官方源码绑定；本次选版0次POST。最新已知平台提交仍为RA1收尾，与当前生产SA1v2区分。
- 旧轮STOP/账本/报告及剩余12次、较早15次保持冻结；本次仅分析和原样源码诊断。选版审计：/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261031_SA1v2_under40/selection.json。


## 2026-10-31 SA1v2剩余瓶颈分析完成
- 生产SA1v2 SHA 17c145dd6fb8b788b64e7f316e25b83eb36b6cc5d0d40a36caf8013c4efea51d不变，case5官方两次41.97/41.87us、中位41.92us；本次0优化候选、0正式POST、0子代理。
- 两份原样源码独立编译，A3合成10组完整kernel配对ABBA共4次profile/1440次调用；前后数值与输入只读检查通过，最终30输出逐位一致。SA1v2单批I7..32斜率1.1762~1.1773us/轮、Vector1.1000；RA1约1.1960、Vector1.11664，不能外推A2。
- 主线A逐层stride9/10/12/8，保持6Add/6屏障，现有matrix内两片区交换；CPU8个H、每H320lane的原树/地址检查及16种基址相位通过，峰值35776B小于最小matrix42240B。区别于旧10Add分半着色，仍无候选设备性能证据。
- 次线B只将列树中间层写到单批owner失活索引缓冲，先核对实际bank与生命周期；C尾依赖优先调度为低优先备选，7Add/6屏障，必须测量额外发射代价。有独立收益才融合；保持原FP32树/eps/Div/实际iters及输入只读。
- 旧STOP/账本/报告及12+15次冻结额度不变；本次STOP，不自动执行下一轮。完整剖析、CPU证明和准入计划：/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261031_SA1v2_under40/analysis.json。


## 2026-10-31 SA1v2三路layer/buffer/tail轮次完成，待用户选版
- 本轮保持SA1v2基线17c145dd6fb8b788b64e7f316e25b83eb36b6cc5d0d40a36caf8013c4efea51d；完整方法、负结果、预算及五项对照见history.md本轮条目。
- 下表为本case所有正式同SID观测，不择优拼接；A3配对profile只作诊断。
- TA1、TB1v2、TC1均通过111+162+64共337项A3设备验证，输出逐位匹配SA1v2且输入只读；父端独立复核源码SHA及输出哈希。初版TB1因split路径漏传新参数而编译失败，修复后的fix1与TB1v2源码SHA相同；失败证据保留。
- 推荐及选版状态：建议继续保留SA1v2。TA1可保留为备选源码，但其case5三次为43.03/43.03/43.11us，中位43.03us，相对本轮SA1v2四次中位43.105us只快0.075us（约0.17%），小于基线41.40至44.35us的观测波动，尚不足以支持更换基线。本轮没有版本突破40us。；待用户选择。
- 原始证据：/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261031_SA1v2_layer_buffer_tail_deepseek_3x5/final_comparison.json；STOP，剩余冻结，无自动继续。

|版本|耗时(us)|分数*|SID|
|---|---:|---:|---|
|A0_SA1v2_open|42.44|31.39|6ae5f22c1dac5d235bfba124|
|TA1_layer_stride_9_10_12_8|43.03|31.28|6ae5f51a1dac5d235bfed21c|
|TB1v2_column_index_pingpong|45.11|30.78|6ae5f6c11dac5d235b00668e|
|TA1r2_layer_stride_9_10_12_8|43.03|31.51|6ae5f7351dac5d235b00f685|
|C0_SA1v2_close|44.35|30.95|6ae5f7c21dac5d235b018e8b|
|C1_SA1v2_cross_account|43.77|31.23|6ae5f8851dac5d235b02552a|
|TA1r3_layer_stride_9_10_12_8|43.11|31.34|6ae5f92a1dac5d235b0308b9|
|C0_SA1v2_close|41.40|31.91|6ae5f9be1dac5d235b03ace8|


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


## 2026-11-01 SA1v2紧凑尾部与mask驻留轮次启动
- 保持SA1v2源码 17c145dd6fb8b788b64e7f316e25b83eb36b6cc5d0d40a36caf8013c4efea51d，保护文件不变。
- A统一紧凑尾部共用六级列树，B固定helper mask驻留，C独立诊断与成本审核；DeepSeek Flash High，父端审核与提交。
- A/B/C/M各最多5次；member1→member2→member3轮换，控制及复测计入预算，不使用旧冻结额度。
- 保持FP32原有顺序、eps、native Div和实际iters；结果由用户选版。本轮只更新总history与c5_history。
- 证据：/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261101_SA1v2_dense_mask_deepseek_3x5。


## 2026-11-01 SA1v2紧凑尾部/mask轮次完成，待用户选版
- 保持生产SA1v2 17c145dd6fb8b788b64e7f316e25b83eb36b6cc5d0d40a36caf8013c4efea51d，七个保护文件不变；三个DeepSeek Flash High子代理分别执行统一紧凑尾部、mask驻留、诊断审核。
- UA1v3、UA2、UA3v1、UA3v2均通过497项逐位/输入只读检查，B1通过337项；初版类型、Gather重载、分母/恢复索引错误及C旧地址视图错误均保留并更正。
- 本地完整kernel配对未显示净收益：紧凑列树虽改善循环斜率，索引与恢复成本抵消收益；B1没有重复收益。只对最终UA3v2做一次A2迁移探测，官方Pass但case5=48.32us、首次分数30.33；不融合。
- member1→member2→member3共3次POST（开场SA1v2、UA3v2、收尾SA1v2）；A/B/C/M用1/0/2/0，剩4/5/3/5合计17冻结，旧冻结额度不借用。推荐继续保留SA1v2，未突破40us；最终用户选择。
- 本轮仅写总history和c5_history，c1–c4哈希未变。完整同SID向量、所有失败/慢记录、诊断纠正与证据：/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261101_SA1v2_dense_mask_deepseek_3x5/final_comparison.json。*分数为完成后首次匹配SID观测，不是提交瞬间分数。

|版本|case5(us)|分数*|SID|
|---|---:|---:|---|
|C0_SA1v2_open|41.86|31.12|6ae6b2f71dac5d235bbbdb8c|
|UA3v2_dense_sparse_seed_first64_zero|48.32|30.33|6ae6bc531dac5d235bc55519|
|C0_SA1v2_close|41.85|31.37|6ae6bd031dac5d235bc60291|


## 2026-11-01 用户保留SA1v2：紧凑尾部轮后瓶颈与下一轮方案
- 保留SA1v2 SHA 17c145dd6fb8b788b64e7f316e25b83eb36b6cc5d0d40a36caf8013c4efea51d；本case最近同SHA两次官方41.86/41.85us，中位41.855us，严格低于40还需净省超过1.855us；完整五项与分数见总history本条。
- 紧凑尾部官方48.32us，mask驻留无完整核净收益；不继续追加索引/布局转换。A3合成迭代斜率约1.1784us/轮，仍缺归约/广播/Div分阶段可靠归因，不以代理确认官方参数。
- 主攻Exp直接写入原packed布局，取消独立pack；保留max/Sub、原归约树、softmax原生Div与后置eps、实际iters。区别于旧early-pack仍有Copy及late-pack倒数乘法；无新增索引表或UB。风险是strided Exp及五次Div调用抵消搬运收益。
- 辅线仅首8字索引种子扇出，保留既有行/token倍增；TBuf生命周期与stats覆盖初始化分别消融。先阶段差分及完整核配对，再决定后续热点路线；CPU地址/有序表达式证明已通过，收益未知。
- 本次0新候选/0编译/0NPU/0POST，选版完成，旧额度与STOP冻结；方案 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261101_SA1v2_post_dense_under40/analysis.json，CPU证明 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261101_SA1v2_post_dense_under40/cpu_proof.json。


## 2026-11-01 SA1v2 Exp-pack与固定开销轮次启动
- 保持SA1v2源码 17c145dd6fb8b788b64e7f316e25b83eb36b6cc5d0d40a36caf8013c4efea51d及七个保护文件。
- A Exp直接写入packed布局，B首8字索引种子/固定开销独立消融，C阶段诊断与审查；使用GPT6.1sol high，必要时xhigh接替，父端审核提交。
- A/B/C/M各最多5次；member1→member2→member3轮换，控制/复测/失败计预算，旧冻结额度不复用；结果由用户选版。
- 复用并重新核验基线111+162+64+160项证据与输出哈希，保持原FP32树、每次eps、原生Div、实际iters及输入只读。
- 证据 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261101_SA1v2_exp_seed_gpt61sol_3x5；只写总history及c5_history。


## 2026-11-01 SA1v2 Exp-pack/索引与固定开销轮完成，待用户选版
- 三个GPT6.1sol High子代理执行A融合、B索引/固定开销和C独立阶段诊断，父端审核全部POST；生产SA1v2 17c145dd6fb8b788b64e7f316e25b83eb36b6cc5d0d40a36caf8013c4efea51d及七个保护文件未改，最终选版由用户决定。
- EA1与EA2各569项逐位/输入只读通过；EB1v2、EB1v3、EB3各497项通过。TBuf首版跨批错算，恢复V_MTE2后12项定向及111项通过、24组实际地址一致，但完整核变慢而不提交；全部失败和慢值保留。
- 正式候选未证明case5优于同SHA基线；EB1v3分数观察值较高但需结合完整复测，不据单次分数推断隐藏用例。不做无独立收益依据的融合，推荐保留SA1v2，未突破40us。
- member3一次HTTP429明确拒绝无SID；用户随后指定仅member1/member2交替。A/B/C/M已用2/4/3/0，合计9/20；余量全部冻结，旧额度与STOP未改。
- C阶段诊断修复了探针自身V_MTE2初始化竞态，140份输出父端重验；A3 H34行归约/行归一化/列树/列归一化差分约0.267/0.305/0.290/0.348us，非可加和全核成本，也非A2时长。仅写本总history及c5_history，c1–c4哈希不变。

|版本|case5(us)|分数*|SID|
|---|---:|---:|---|
|C0_SA1v2_open|42.29|31.13|6ae6c81f1dac5d235bd0850c|
|EA1|43.34|31.08|6ae6cb5f1dac5d235bd3f354|
|EB3_stats_init_v1|44.14|31.13|6ae6cec41dac5d235bd74966|
|EB1_seed8_v3|43.33|31.44|6ae6cf611dac5d235bd7eac9|
|EA2|42.85|30.89|6ae6d0061dac5d235bd8838e|
|C0_SA1v2_mid|41.57|31.38|6ae6d0bb1dac5d235bd9293d|
|EB1_seed8_v3_repeat|43.41|31.20|6ae6d1851dac5d235bd9ed6c|
|C0_SA1v2_close|42.63|31.12|6ae6d2de1dac5d235bdb4d76|

*分数为完成后首次匹配SID观测；同SHA慢值与拒绝请求详见 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261101_SA1v2_exp_seed_gpt61sol_3x5/final_comparison.json。


## 2026-11-01 SA1v2保留：本轮结果与下一轮列缩放方案
- 用户选择SA1v2（17c145dd6fb8b788b64e7f316e25b83eb36b6cc5d0d40a36caf8013c4efea51d）。同SHA正式case5为42.29/41.57/42.63us，中位42.29；严格低于40还需>2.29us、>5.415%整体收益。EA1 43.34、EA2 42.85、EB1v3 43.33/43.41、EB3 44.14均无正式收益。
- 修正竞态后的A3代理阶段差分H34：行归约0.2669、行归一化0.3047、列树0.2899、列归一化0.3479us；归一化与树同量级，优先处理反复执行部分。阶段数不可直接加和为全核时间，H33–40代理不是官方case5元数据，列归一化差分也不是独立bank冲突耗时。
- 主攻新方案：保留原生Div的两个输入与元素数，将输出直接落在A=work[320+delta]，仅一次Copy到B=work[delta]，奇偶行分别Mul A/B；delta=((packed-work)&511)/4，固定E320。相比旧双Copy提案减半复制流量为2560B并少一次同步，无新增UB；初版只动初始/中间列缩放。2048组静态地址/高度组合、373760对窗口及符号数据流检查通过，仍须实际编译和完整阶段测量，不能宣布性能已改善。
- 条件路线：先看生成代码是否存在循环内重复标量工作，再做受限专门化；rowRootViews/denominatorOffset/TPipe等已外提，不重复宣称新优化。独立诊断复用v5，检查Copy的NORMAL mask语义、实际UB地址、逐位/只读、多批与实际iters；A2正式重复<40且相对同期基线稳定，才认定突破。
- 目前仅分析，未实现/编译/运行NPU/POST；不融合本轮负收益版本。完整方案与限制见/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261101_SA1v2_post_exp_seed_under40/analysis.json；CPU证明见cpu_address_proof.json。原始报告、慢值与失败保留。


## 2026-11-01 SA1v2单Copy/生成代码轮完成，待用户选版
- A0改变native Div输出落点；A1在此基础上单Copy倒数并拆奇偶行Mul。保留原FP32运算顺序、归约树、eps、运行时iters及原分派条件，未更改UB分配和正式输出路径。
- C路在原分配顺序与实际UB地址下测列缩放阶段，含Div/Copy/所有屏障并扣配对reset控制：H33至36时A0局部改善12.07%至16.55%，A1局部改善9.96%至13.39%；1656导出均独立CPU校验通过，但阶段斜率不能累加推算完整case5。
- 完整kernel及正式反馈否定局部收益外推：A1多核代理退化约8.23%/9.81%；A0虽A3代理改善，正式A2两次case5为44.80/44.57us，慢于三次SA1v2对照43.19/42.00/43.09us，停止A0提交。
- B审计发现中间IR中Copy已留NORMAL64、Mul<true>仍调用有副作用MOVEMASK；实施A2仅两处Mul<float,false>。111项逐位通过，对象text比A1小864B，但H34/S256与S320完整代理分别退化12.292%/12.273%，单核近持平；不能宣称最终ISA减少了多少mask指令或已消除硬件冲突。
- 本轮判断：SA1v2仍最佳保留建议，case5未突破40us；无独立获益路线可融合。保留全部同SHA慢值和失败工具输出，不从正式case耗时反推隐藏形状。后续若再推进应先取得完整kernel/A2可复现收益证据，避免继续用局部列缩放收益替代端到端效果。

|版本|case5(us)|分数*|SID|
|---|---:|---:|---|
|C0_SA1v2_open|43.19|31.09|6ae6dcb61dac5d235be528bc|
|SC_A0_DivPlace|44.80|30.17|6ae6e0541dac5d235be8c742|
|SC_A0_DivPlace_repeat|44.57|30.17|6ae6e10f1dac5d235be97560|
|C0_SA1v2_mid|42.00|30.97|6ae6e2c41dac5d235beb3182|
|C0_SA1v2_close|43.09|30.85|6ae6e4581dac5d235becb971|

*分数为完成后首次匹配SID的正式观测；失败、慢记录与完整证据见 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261101_SA1v2_singlecopy_codegen_gpt61sol_3x5/final_comparison.json。


## 2026-11-01 SA1v2确认保留与多角度重新分析
- 保留SA1v2，沿用总history所列上一轮完整正式向量；本轮没有新case5设备耗时。榜单证实40us不是已达到的统一硬件下限，但不能反推竞争者实现或官方输入参数。
- 原序主线：隔离自然compact家族的精简device类，审查循环内基址/stride/视图生成与原生指令调用；保留原UB地址与运算顺序，以标量和完整kernel证据判定，不把代码体积减小当收益。
- 条件性新行归约：由每块先BR再合并改为列块逐元素合并后一次BR。合成H34成本9→5个API、190→170个repeat，但四组屏障不减，逻辑UB字节62016→94656；不同于历史单平铺BR，增加流量可能使其变慢。
- CPU FP32示意模型覆盖H33至40、iters1至32、8类输入、4种eps，共8192组，每组8矩阵；相对原序模型最大绝对误差2.3841858e-7、相对7.0488765e-6。仅为数值筛查，不是官方reference/NPU/逐位证据；实施须先明确变更额外原求和树约束，padding必须mask排除。
- 第三方向按公开元数据与完整关键核成本检查分派、多波q8尾批及条件性搬运重叠；单波q8已在生产。详细来源、历史负证据与停止条件见 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261101_SA1v2_multiaxis_rethink/analysis.json；本轮只分析，不消耗提交。


## 2026-11-01 SA1v2多角度轮完成，待用户选版
- A1抽出自然compact资源家族的独立入口，保持原UB分配、FP32树、Div、eps及实际iters；group8且N整除8的host证明覆盖所有owner完整批次，其他元数据回退。497+785项逐位/只读验证通过。
- A1两轮A3完整ABBA在H34/N256改善18.98%/22.32%、N320改善25.49%/26.06%，单核约5.5%；这些是合成代理，不是官方case5参数。独立入口7684B；通用回退符号尺寸相同但字节hash不同，保留P48小幅慢记录，不宣称原因已证实。
- B1v2交换列块与块内求和层级，1282项独立数值审计通过，但正式case5=44.74us；B2错开两个fold面板相位仅局部小幅改善，完整代理相对SA仍退化，不提交。B的首次mask const编译失败保留，未消耗正式次数。
- C的52项成本诊断中q8+tail4均快于两批q8，停止强制多波q8方案；无独立第二路收益可融合。A第二阶段低层循环的结果和正式版本比较见同轮final_comparison.json及A2报告。
- 推荐 A2_native_loop40；A2两次正式Pass的case5为35.25/35.29us，中位35.27us，较本轮SA1v2三次中位42.24us改善约16.5%；首次观测总分31.27/31.52。代价是case4两次73.55/73.95us，较SA1v2中位69.74us约慢5.75%。建议按case5目标保留A2_native_loop40，完整列明权衡，由用户决定；不宣称所有case都提升。。完整五case、分数、SID见本轮总history，下方只保留case5观测；保持SA1v2生产，等待用户选择。

|版本|case5(us)|分数*|SID|
|---|---:|---:|---|
|C0_SA1v2_open|42.55|31.08|6ae6f9811dac5d235b021aa0|
|B1v2_BlockFoldBeforeBR|44.74|30.52|6ae6fc851dac5d235b05162b|
|A1_slim_compact40|40.57|30.93|6ae6fd851dac5d235b061ddb|
|C0_SA1v2_mid|42.24|30.82|6ae6fe921dac5d235b072c1d|
|A1_slim_compact40_repeat|40.65|30.81|6ae6ff191dac5d235b07b871|
|A2_native_loop40|35.25|31.27|6ae702501dac5d235b0b2a7a|
|A2_native_loop40_repeat|35.29|31.52|6ae703341dac5d235b0c111e|
|C0_SA1v2_close|42.04|31.25|6ae703f51dac5d235b0cd7d7|

*分数为完成后首次匹配SID的正式榜单观测，不冒称提交瞬间分数；完整同SHA结果、慢记录及原始路径见 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261101_SA1v2_multiaxis_gpt61sol_3x5/final_comparison.json。


## 2026-11-01 用户选择A2_native_loop40基线及突破30us分析
- 采用本轮A2_native_loop40（非历史同名A2），SHA 148e391fc54ab461df505384785f045777a8f0677d2719ca49e404f8fc2b01cc；case5正式35.25/35.29us，中位35.27，突破30还需超过14.94%整核收益；完整五项/SID/分数见总history本条。
- 原生热循环仍有行归约/eps/Div/广播/Mul及列树/eps/Div/Mul依赖链。每轮17个显式V屏障是源码计数，不是可删除开销；A3 Vector19.93us不是正式case5分阶段计时。
- 先建立A2迭代斜率/冲突证据；主线为有限H静态化和一次配对行布局，补充门控-softmax共组。B只改物理行顺序，原运算树和每轮10Mul保留，CPU有序表达式/索引/输出/相位证明已通过，实际收益未知。
- 旧错相RB1的额外20Mul/轮、block-fold的额外UB流量等负证据纳入止损；不重复将mask/API减少等同速度改善。不凭代理或榜单推测官方参数。
- 生产A2已固定；0候选/编译/NPU/POST，旧12次冻结，不自动执行。详细分析 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261101_A2_native_under30/analysis.json；CPU证明 /mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/analysis_20261101_A2_native_under30/paired_rows_static_proof.json。
