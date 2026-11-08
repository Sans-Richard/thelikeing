# SinkhornNorm 规则与计算合同

本文件仅维护规则与计算合同；优化记录写入[HISTORY/history.md](HISTORY/history.md)，当前任务与授权状态读取`current_baseline.json`及`active_campaign.json`。

本文件依据 2026-10-23 在 Chrome 核对的新题页面及用户提供的“规则要求”截图整理。官方阶段名为“2026年CANN挑战赛_西南赛区（决赛）”；本工作区将用户所称“复赛”绑定到 `op_challenge_xinan_final/sinkhorn_norm`，不沿用初赛配置。最新适用的官方题面、模板及公告优先。

来源：[官方赛题](https://competition.gitcode.com/competition/2094722165106008066/publish)、[CANNJudge 题目页](https://cannjudge.cn/public/op_challenge_xinan_final/sinkhorn_norm)、[提交页](https://cannjudge.cn/public/op_challenge_xinan_final/sinkhorn_norm/submit)。`others/migrations/sinkhorn_20261023/*.public.json` 仅作为 2026-10-23 的历史快照，不再代表当前测试点 ID 和下发模板。

## 2026-10-30 当前版本与提交口径

以下内容记录 2026-10-30 对[赛事项目页](https://competition.gitcode.com/competition/2094722165106008066/publish)、[公开题面 `cann.md`](https://raw.gitcode.com/cann-competition/026CANNChallenge_chengdu/raw/main/cann.md)、CANNJudge 题目 API 和实际下发模板的核对结果；不改变下文计算合同。

- **测试点已更新**：当前仍为 15 个测试点、前 5 个公开和后 10 个 `Hidden`，但 testcase ID 已全部更换为 `6ae2fdfb1dac5d235b4b62aa` 至 `6ae2fdfb1dac5d235b4b62e3`。2026-10-23 的旧 ID 结果不能与新测试点按编号或耗时直接横比。
- **新版样例参数**：当前只读 `main.asc` 和 `sample.py` 示例使用 `hc_sinkhorn_iters=15`；`sample.py` 的输入生成范围为 `[-50,50]`。静态题面仍写默认 20 和建议 `[-2,2]`，CANNJudge 元数据 `iterations=5` 也不是 `hc_sinkhorn_iters`。kernel 必须使用运行时传入的迭代数和任意有限实数输入，不能硬编码 15、20 或 5；`15` 与 `[-50,50]` 只是新版样例参数，不是缩窄后的正式输入合同。
- **模板来源**：当前只读模板 `main.asc` SHA-256 为 `6609b3f782b87be34060c65116fa1bbd9f4b3ee0d07259ee5764a65829d3a755`，`sample.py` 为 `a57f032ab81efc1607922df568bbbe1f5b198b3174fddf18dc0a3cd56c0ba3a0`；`reference.py` 未变。模板更新证据见 `sinkhorn_norm_problem_2360_template/parallel_candidates/campaign_20261029_newtests_case35_round2/official_template_update.json`。
- **提交次数与成绩模式**：赛事项目页当前写明每天最多 50 次提交。页面同时出现“取比赛期间最后一次提交”和“以最优成绩作为最终成绩”两种表述；CANNJudge 实际配置仍为 `ranking_submission_mode=latest`。在官方澄清前按“下一次提交覆盖当前成绩”处理，不把旧裁决当成最优模式授权。
- **截止时间冲突**：赛事项目页当前写决赛结束时间为 2026-11-07 11:30（北京时间），CANNJudge 元数据为 2026-11-07 12:00。官方澄清前按更早的 11:30 作为安全截止时间。

## 输入、输出与精度

- 输入 `mixes`：FP32、ND，形状 `[B,S,H²+2H]`，其中 `B∈[1,128]`、`S∈[1,8192]`、`H∈[2,128]`；最后一维依次为 pre 的 H 项、post 的 H 项、comb 的 H² 项，comb 按行展开。
- 输出：pre、post 均为 `[B,S,H]`；comb 为 `[B,S,H,H]`。输入、输出和中间计算均为 FP32。
- `iters∈[1,32]`，eps 默认 `1e-6`。必须使用实际传入属性；题面未明确的 eps 合法范围保留待确认，不自行补写限制。
- 已核对题面精度要求为绝对误差、相对误差小于 `1e-4`；具体判定遵循未修改的官方 reference/校验器。
- 当前公开网页显示 5 个可见测试点，另有 10 个隐藏测试点；不由可见点推定隐藏形状。不把建议输入分布或公开样例当成输入值、隐藏形状或全量验证的保证。

对每个 token，令 zpre、zpost 和 Z 分别为上述三段，sigmoid(x)=1/(1+exp(-x))。计算顺序为：

1. `pre = sigmoid(zpre) + eps`。
2. `post = 2 * sigmoid(zpost)`。
3. Z 按行执行稳定 softmax，再对每个元素加 eps，得到 A。**此处 eps 加在 softmax 输出上，不是 softmax 分母中。**
4. 初始列归一化：`M[i,j] = A[i,j] / (sum_i A[i,j] + eps)`。
5. 再执行 `iters-1` 轮：先逐行除以“本行元素和 + eps”，再逐列除以“本列元素和 + eps”。最终 M 为 comb。

`iters=1` 仍须完成初始 softmax、加 eps 和列归一化；不能跳过。轮次固定，不进行收敛提前退出。

## 官方实现要求

允许向量化、流水、分块、数学等价改写（如缩放向量因子化）等加速手段。等价改写仍须完整实现实际输入及属性对应的运算，并满足 FP32、精度和固定迭代要求。

相同输入与属性组合必须产生完全相同的输出；轮数固定、无数据相关分支。算子执行不得修改输入 `mixes`，workspace 自行管理。

Host 仅负责参数校验、shape 推导、tiling 逻辑和启动配置；Device Kernel 负责完成算子完整计算。按截图所示赛事规则，禁止以下行为，包括但不限于：

1. 在 Host 读取输入张量进行计算。
2. 在 Host 对输入数据进行重排。
3. 在 Host 生成预查表，传入 Kernel 直接取值计算。
4. 在 Host 完成向量、矩阵计算，将结果传入 Kernel 直接用于计算。
5. 硬编码，按测试用例或者数据生成规律跳算。
6. 写入标记跳过计算。
7. 利用旧输出或者未初始化内存跳过计算。
8. 逐条匹配评测用例编号写专属实现。
9. 修改或者干扰判题、精度校验和计时流程。
10. 注入空 kernel、识别预热轮次或把实际计算移出计时范围。
11. 在多轮次判题中加缓存来减少耗时。
12. 一次计算通过多次 kernel 完成。

比赛结束后有最终人工核验，违反适用规则的代码将被作废成绩。平台 Pass、分数、排名或一次未封禁不等于最终合规认定。

## 队内工程约定与证据边界

下列是工作流程约定，不冒称额外官方禁令：保护官方模板/判题文件；为分派说明算法或资源依据；隔离旧题数据；固定快照和显式账号；未确认请求先核对；保留原始结果与源码哈希。

不以名称、关键词或单一写法判断违规；不把“内联汇编”或“精确单轴等式”等另加成官方禁令。若采用更保守的队内标准，应明确标记为队内标准及适用范围。

正确性、性能和规则核对分别报告。离线数值模型或桩语法检查不替代真实 CANN 编译/NPU 运行；官方 sample 不覆盖全部合法输入；正式回执只绑定其实际提交的源码快照。未确认事项必须保留未知，不由榜单、噪声或旧题经验反推。
