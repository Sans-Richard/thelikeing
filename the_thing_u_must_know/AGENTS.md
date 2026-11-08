# SinkhornNorm 云端工作入口

## 文档职责与当前状态入口

- `AGENTS.md`：长期协作规则、任务绑定、操作边界和工作顺序。
- `README.md`：目录导航、工具用法和操作说明。
- `RULES.md`：赛题计算合同、竞赛规则及其依据。
- 当前任务父版按工作区读取：A 用 `workspace_control/baseline.json`，B 用 `workspace_control/baseline.B.json`；注册信息、任务及共享预算仍在 `workspace_control/state.json`。`current_baseline.json`、`active_campaign.json` 只供旧轮次兼容。
- `HISTORY/history.md`、`HISTORY/c1_history.md` 至 `HISTORY/c5_history.md`：每轮方案、实现、验证、完整同SHA五项耗时、失败/慢记录、选版和经验。详细原始回执、源码快照、日志和CSV仍保存在已有的独立证据目录，由HISTORY引用，避免复制漂移。
- **优化记录只追加到 `HISTORY/history.md` 和 `HISTORY/c1_history.md` 至 `HISTORY/c5_history.md` 六个固定文件。未知case的方法、编号猜测、证据等级和当前结论写入根目录 `hidden.md`；探测过程、逐笔结果、失败、停止与恢复记录写入根目录 `hidden_history.md`（2026-11-05用户明确指定）。** 不另建轮次、方案、分析、选版、审查、交接或维护Markdown，不在HISTORY新建子目录。AGENTS.md、README.md、RULES.md只维护各自长期规则和说明；当前状态写状态JSON，既有历史原件只归档引用。
- 历史文件及归档中的旧授权、旧STOP和“本块覆盖”等原话均为历史证据，不构成当前执行授权。不得执行会把历史块重新写回入口文档的旧收尾脚本；先审查写入目标，保留既有归档和报告原样。
- 用户最新明确指令优先。STOP、pending、预算或实时源码与状态记录不一致时，先核对；旧额度继续按状态冻结，不从历史记录推导可用额度。

## 当前任务绑定

- 官方赛事名：2026年CANN挑战赛_西南赛区（决赛）。用户所称“复赛”在本工作区指本次新赛题；不可沿用初赛题目配置。
- 算子：SinkhornNorm；slug：`op_challenge_xinan_final/sinkhorn_norm`。
- `problem_id=6adb28021dac5d235bd73b85`；`contest_id=6adac8363ff2fef7e89242fe`。
- 官方工程：`sinkhorn_norm_problem_2360_template`；元数据 `code_template=npu_kernel_dev`，CANN 9.0.0，Vector 实现。
- 截止时间：北京时间 2026-11-07 12:00。每次正式提交前重新检查平台状态和额度。
- 评测硬件已确认为 **Atlas A2（910B4）**。模板 `NPU_ARCH=dav-2201`，公开元数据 `soc_version=null`；模板标识不能替代已确认的评测硬件。云端诊断设备与评测设备分开记录，运行前核实工程实际使用的 CANN 版本、芯片及可用资源。
- 榜单配置 `ranking_submission_mode=latest`，不可假设取历史最优提交。

<!-- generic-workspaces-v1:begin -->
## 通用工作区与共享协调层

- 两个工作区均不绑定 case。A 的工程原位保留在 `sinkhorn_norm_problem_2360_template`，B 的完整工程在 `workspaces/B/project`；登记信息在 `workspaces/A/workspace.json`、`workspaces/B/workspace.json`。只复制官方工程、工程标记和允许的源码，不复制旧构建、测试张量、历史候选或账号密钥。
- 新任务通过 `others/scoreboard_and_submit/workspace task create` 创建，明确 `--workspace A|B`、`--kind analysis|optimize` 和 `--target`。权威任务及预算台账是 `workspace_control/state.json`；任务状态展示副本、构建入口、日志和原始运行记录分别在 `workspaces/<空间>/tasks/<任务ID>/`。同一工作区最多一个优化写任务；旧轮次尚在运行时，不允许在 A 新建优化写任务。分析任务使用独立的基线副本。
- **A、B 独立选择和保留基线，允许相同，也允许不同。** 另一工作区选版、回退或导入旧版，不触发本区同步、重置或重新选版。新分析和优化任务均以本区选中的完整快照为父版；已经开始的任务保留原父版。只有用户明确要求同步时，才在指定目标工作区核对并选用指定版本。完整快照位于 `workspace_control/snapshots/<摘要>/source`。
- `baseline select --workspace A|B` 仅更新指定工作区的指针。用该区旧 kernel SHA 和完整快照 ID 在 `.baseline.lock` 下比对；不部署源码，不改另一工作区或旧状态。工作副本只与本区基线比较；两区版本不同无需 `--adopt-current`，本区有未选改动才需要显式采用。新脚本优先使用 `workspace` 命令；直接使用 Python 时从 `workspace_control/coordinator_v2.py` 导入 Coordinator 并记录其指纹。旧 `coordinator.py` 仅为历史任务复核保留，禁止用旧单指针接口选新版 B。
- 新任务默认 NPU 权限关闭、POST 预算为 0。只有本轮用户新授权才可用唯一授权 ID 执行 `budget grant` 并给任务预留额度；旧轮次或冻结额度不导入、不借用。分析任务始终不能取得 NPU/POST 权限；构建协调层本身不启动优化、设备验证、正式提交或周期 worker。
- 编辑、只读分析和普通 CPU 工作可跨空间并行。受管理命令使用 `workspace run --workspace ... --task ... --resource cpu|compile|npu|compile-npu -- <命令>`，从固定源码快照建立独立 `/tmp/sinkhorn_workspaces/<空间>/<任务>/<运行>/project`。临时构建和大张量放该运行目录，日志、命令与源码指纹留在任务目录。持久盘不足 1 GiB 或临时盘不足 1 GiB 时拒绝启动新受管理运行；不自动删除证据。资源标签是协作约定，不是操作系统沙箱，不得以 cpu 标签运行设备或提交命令绕过协调。
- 编译继续共用 `/tmp/sinkhorn_case5_four_routes_compile.lock`；NPU 共用 `/tmp/npu.lock`，统一先编译锁后设备锁。新提交使用同一个旧提交后端和固定的 `.submission.lock`、pending 扫描、全局时钟、去重、账号/日策略及结果库；不得为 B 复制另一套看不见彼此状态的提交系统。
- `submit --workspace <空间> --task <任务ID>` 或 `workspace submit ...` 从指定任务快照打包，参数贯穿校验、快照、官方 sample 构建和上传。未带工作区参数的旧 submit 命令保持原行为。新提交只使用既有缓存会话，不自动登录续期；会话失效时先由现有账号工具显式恢复。每个新记账请求默认按三个账号轮换，账号对该请求及其续查/对账保持固定。所有新旧 STOP、至少 60 秒共享间隔、约 195 秒账号观察冷却及更严格的 Retry-After 均保留，429 不换号重投。
- 可用 `queue enqueue` 固定提交候选，`queue dispatch --job <队列ID>` 显式派发一项；没有后台 worker，也没有自动重试。队列放在 `workspace_control/submit_queue`。不确定请求只用原任务、原账号 `--reconcile` / `--resume`，再 `queue refresh` 更新本地状态；派发进程已退出且确认未记账、无 POST 证据时才可显式 `queue abandon`。失败/不确定尝试保留记账，不自动返还额度。
- 两个工作区向平台提交的仍是完整算子，不能分别上传单个 case 的局部实现。各路成果需按冻结父版合并并复测完整结果；`latest` 不会自动合并两个版本的收益。新流程不更改官方模板、算法合同、精度或计时边界。
- HISTORY 继续只含六个固定文件，写入共用 `.history.lock`，记录任务 ID、工作区、完整 SHA 和证据路径。只把目标 case 的优化写入其 cN_history；未知 case 假设及结论写 hidden.md，探测过程写 hidden_history.md。新协调层的 JSON、测试、备份和运行证据放 HISTORY 之外。
<!-- generic-workspaces-v1:end -->

## 技术问题查询与硬件适用性（2026-10-24）

评测硬件已确认为 **Atlas A2（910B4）**。所有技术结论必须核对是否适用于该硬件，不能直接套用 Atlas A3、910C、Atlas 350 或其他产品的支持范围、精度和性能结论。同时核实工程实际使用的 CANN 版本；下面提供的 9.0.0 文档仅在版本匹配时作为直接依据。

遇到 API 签名、硬件支持、dtype、对齐、mask、归约、同步、精度、编译或性能问题时，主动查询下列官方文档及竞赛答疑，并结合实际安装的头文件、实现和编译路径核对：

- 确认取得正文及相关回复，不把网页导航或搜索摘要当作已查证结论。区分官方说明、维护者答复和参赛者推测，注明来源链接、版本、日期及硬件适用范围。
- 分别核对接口的具体重载、数据类型与硬件支持表；商业版和社区版页面须注明各自版本及适用范围，不能仅凭 API 同名或签名一致认定硬件支持相同。
- A3 等其他设备上的本地诊断必须明确标注设备，只作为问题线索，不能冒充 A2（910B4）的编译、正确性、精度或性能验证。接口支持、数值精度和性能收益分别给出证据。
- `CreateVecIndex` 的 9.0.0 官方实现用于核查 API 内部行为；源码分支标签不能替代当前安装 SDK 的实现核对，也不能单独证明 A2 适用性。

### 主要入口

1. 昇腾官方文档中心  
   https://www.hiascend.com/document/

2. CANN 9.0.0 文档  
   https://www.hiascend.com/document/detail/zh/canncommercial/900/index/index.html

3. CANN 算子竞赛问题与答疑列表  
   https://gitcode.com/cann/cann-ops-competitions/issues

4. 集中答疑帖 #36  
   https://gitcode.com/cann/cann-ops-competitions/issues/36

### 可按需要查阅的具体页面

5. Gather  
   https://www.hiascend.com/document/detail/en/CANNCommunityEdition/900/API/ascendcopapi/atlasascendc_api_07_0092.html

6. PipeBarrier  
   https://www.hiascend.com/document/detail/en/CANNCommunityEdition/900/API/ascendcopapi/atlasascendc_api_07_0271.html

7. InitSocState  
   https://www.hiascend.com/document/detail/en/CANNCommunityEdition/900/API/ascendcopapi/atlasascendc_api_07_00094.html

8. CreateVecIndex 官方 9.0.0 实现，作为核查 API 内部行为的示例  
   https://gitcode.com/cann/asc-devkit/blob/9.0.0/impl/basic_api/dav_c220/kernel_operator_vec_createvecindex_impl.h

## 优化参考文档（references）

参考目录：`/mnt/workspace/enjoy_ur_time/the_thing_u_must_know/references`。当前包含以下 5 份优化参考文档，链接均相对于本文件：

| 阶段 | 参考文档 | 主要内容 |
|---|---|---|
| 1. Tiling 优化 | [tiling-prof.md](references/tiling-prof.md) | 多核切分、L2Cache 切分和核间负载均衡 |
| 2. 搬运优化 | [data-copy-prof.md](references/data-copy-prof.md) | 搬运粒度、GM 地址对齐和 stride 搬运 |
| 3. API 使用优化 | [api-usage-prof.md](references/api-usage-prof.md) | TPipe、TQueBind、Counter 模式、Matmul AtomicAdd 和归约指令组合 |
| 4. 内存优化 | [memory-prof.md](references/memory-prof.md) | 存储层级、UB 融合、L0C 累加、L1 常驻及 BT/FP Buffer 示例 |
| 5. 流水优化 | [pipeline-prof.md](references/pipeline-prof.md) | CopyIn/Compute/CopyOut、Double Buffer 和异步 Iterate 示例 |

进行瓶颈分析、候选设计或遇到相关技术问题时，按上表查阅对应文档；具体 API 与实现问题同时结合上一节的官方文档、答疑和实际 SDK 头文件核对。

这些材料用于提供优化思路。文档中的示例核数、缓存容量、搬运阈值、API 用法和性能收益数字，必须核对 **Atlas A2（910B4）** 与工程实际 CANN 版本的适用性；不能直接视为本题已验证的支持范围、精度或性能结论。候选效果仍须由对应环境和源码版本的实际验证确认。

## 源码及修改边界

1. 旧轮次的活动源码仍为 `/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/kernel.asc`；新通用任务从任务记录的 `project_dir` 读取源码并绑定冻结快照。新基线读取本工作区的指针，任务授权读取共享任务台账，旧轮次继续使用两个兼容状态 JSON。每轮核对路径、构建入口、SHA-256和ABI，不因选版或迁移自动覆盖其他工作区。
2. 按新模板允许范围只修改 `kernel.asc` 及允许的工程根目录 `.asc/.h` 源文件。`main.asc`、`CMakeLists.txt`、reference、sample、run 等官方文件均保持原件；不得修改判题、容差或计时流程。
3. Host 只处理参数校验、shape、tiling 和启动配置；Device 完成本次真实输入的完整计算。全程 FP32，固定迭代，单次 kernel 启动，输入 `mixes` 不可写。完整规则见 `RULES.md`。
4. 形状分派应有算法、容量、对齐或调度依据，并覆盖相应真实输入和尾部。不得由已知样例、评测编号或生成规律推断答案或省略计算。
5. 不读取初赛资料来替代新题合同；不运行旧 `perf_verify`、`verify_harness` 或旧题提交链。需要额外设备验证时，先核对其适用性及当前授权。

## 账号与提交

共享入口：`others/scoreboard_and_submit/submit`；新通用任务必须带 `--workspace`、`--task`，管理入口为 `others/scoreboard_and_submit/workspace`，不带工作区参数时保持旧模式。三个配置名为 `member1`（ruinward）、`member2`（琉暝）、`member3`（孙新尧爱提交）。凭据位置和内容保持不变，不把会话、Cookie 或令牌写进文档、源码及日志。

- **在用户已授权的任务范围和总提交预算内，新提交任务默认按 `member1 → member2 → member3 → member1` 循环选择账号，无需用户逐次指定。** 用户本轮另行明确指定固定账号或顺序时，以最新指令为准。由主agent或本轮调度器在创建新任务、冻结提交快照前选定账号；底层提交入口仍显式传入 `--account`，不依赖隐式默认账号。
- 每个新提交任务选定账号后，全程固定使用该账号，记录账号、用户ID、源码SHA及提交SID；验证、提交、续查和reconcile均沿用原账号。doctor、dry-run、续查和reconcile不推进轮换顺序。重复验证或失败请求按实际记录保留，不通过新任务或换号重投未确认请求。
- **三个账号分别核对最近POST和自身冷却时间；当前用户观察同一账号两次提交约需间隔195秒。** 该数值为当前观察值，实际等待以实时服务端反馈和更严格的本轮约定为准。现有提交器仍执行跨账号共享至少60秒的提交间隔，两类间隔须同时满足；可用账号均未满足条件时等待，不连续试探。
- 三个账号共用提交流程锁、pending拦截和本轮授权总预算，正式提交串行执行。各账号可用额度与适用的团队或全局限制分别核对，轮换不增加总预算、不自动恢复冻结额度，也不自动启动优化、提交或后台worker。
- 收到429时保留回执及Retry-After等字段，并按实际适用范围更新冷却；不能把团队或全局限制当成单账号限制。不得用换号绕过未确认POST、停止状态、共享间隔或总额度。
- 默认使用上述三账号轮换；用户明确指定的账号范围或顺序优先。预算、最短提交间隔和日策略上限以当前授权及本轮状态为准，不视为平台公布限额。控制、复测和实际失败请求计入本轮总账及适用的分路额度，不补偿、不转借、不因轮换或跨日重置，也不为耗尽上限而机械提交。
- 保持实际iters、FP32、每个eps及原生Div；求和次序等额外约束按用户当前指令执行。保留所有同SHA/同SID完整五项耗时和慢记录，禁止拼接跨版本最小值。
- 并行agent按独立候选目录隔离；父端统一协调编译、NPU和提交锁，避免共享状态冲突。子agent不自行扩大授权或消耗提交预算。
- `--dry-run` 只做离线检查，不登录、不 POST；`--doctor` 仅 GET；`--resume <sid>` 只续查现有提交，不 POST。
- 默认正式提交在固定源码快照的隔离目录运行新题官方 sample 验证；样例通过才可进入提交。保护官方验证文件，不把该样例当作全量正确性证明。
- 新题使用 `data.sinkhorn_norm.json`，与初赛 `data.json` 隔离；不自动推送 GitHub。
- 同一工程的源码写入、NPU 使用和提交应串行，避免协作者冲突。未确认 POST 先核对请求和服务端状态；有提交 ID 只续查，不通过新任务、重复请求或换号绕过。

## 每轮流程与证据

1. 固定本轮父版本；记录题目、账号、源码路径、SHA-256、时间与授权范围。已有完全匹配快照时可复用，不修改既有快照。
2. 按当前授权在隔离候选目录开发，再冻结候选快照及 manifest；正式验证和提交均绑定该快照，期间工作文件的新修改不能混入。
3. 执行所授权的检查。正式提交前用 `--doctor` 核对身份、题目、截止时间、停止状态和预算；只有获得提交授权且已按默认轮换或用户指定规则选定账号时才正式提交。
4. 原始回执、结果与 comparison 存入 `others/scoreboard_and_submit/scoreboard/runs_sinkhorn/` 的本轮目录，保留父版、候选及版本绑定。比较完整正确性和整体性能后决定保留或回退；回退前确认不覆盖他人的新改动。
5. 静态审查、离线模型、普通 C++ 桩检查、CANN 编译、设备运行、官方 sample、正式平台结果和最终人工核验分别记录。不能将一个层次的通过扩大成另一个层次的结论。

## 历史维护与归档

- 用户2026-11-01明确：只有实际针对某个case开展优化，才写该case对应的cN_history.md。优化case5时只写总history.md和c5_history.md；其他case的完整耗时及回退检查留在总history和原始证据，不向c1–c4复制case5优化经验。历史原件保留，新记录严格按目标case归属。


### 固定记录入口与代码归档规则（用户明确要求）

- **HISTORY目录只能直接包含六个文件：`history.md`、`c1_history.md`、`c2_history.md`、`c3_history.md`、`c4_history.md`、`c5_history.md`。禁止子目录、其他Markdown、软链接和其他文件。** “只放md”不能解释为允许任意md或campaign/analysis/selection目录。
- 整体方案、共性实现/审查结论、版本选择、跨case完整耗时、失败/慢记录、交接和维护摘要合并到 `HISTORY/history.md`；单case事实与结论写相应 `cN_history.md`。共同内容由case文件引用总history，不复制多套持续更新的报告。
- 未知case的方法、编号猜测、推断依据、置信度和反例在 `/mnt/workspace/enjoy_ur_time/the_thing_u_must_know/hidden.md` 维护；逐轮探测过程及工作记录在同目录 `hidden_history.md` 维护。history可记录已做验证及指向hidden的链接，不另开预测报告或复制一套假设登记。A3代理、旧探针映射和评分残量不得写成官方shape事实。
- 旧轮次继续使用 `sinkhorn_norm_problem_2360_template/parallel_candidates/`。新通用任务的可写工程、任务状态和证据按注册信息分别放在 A/B 工程与 `workspaces/<空间>/tasks/<任务ID>/`；不可变源码快照、基线索引、预算和队列放 `workspace_control/`。正式提交回执继续共用 `others/scoreboard_and_submit/scoreboard/runs_sinkhorn/` 并标注空间/任务/快照。JSON/CSV/日志/图片/HTML/patch/manifest/状态备份均不得放HISTORY。
- 历史散落Markdown的原件可归档在HISTORY外以保全证据，必须在六个history或hidden中收束其结论和归属；原件不再作为持续更新入口，也不能以“详细报告”“agent交付”“临时计划”为由继续创建独立优化记录md。
- 写入锁使用 `/mnt/workspace/enjoy_ur_time/the_thing_u_must_know/.history.lock`；临时文件、迁移清单、备份和维护审计放HISTORY外。文档修改前后检查HISTORY的直接条目集合恰好为上述六个普通文件，不能只检查扩展名。
- 旧脚本与子agent必须遵守同一六文件/hidden分工；运行前检查写入路径，发现要创建HISTORY子目录或额外md则先修正，不能执行后再整理。保存原始证据字节和SHA，迁移时同步现行引用并留外部映射；核对正式源码SHA和停止状态不被文档维护改变。

- 整体优化、公共经验、版本保留/回退与整体性能对照写入 [HISTORY/history.md](HISTORY/history.md)。
- 可见case 1–5的对点分析、试验、失败与经验分别写入 [c1](HISTORY/c1_history.md)、[c2](HISTORY/c2_history.md)、[c3](HISTORY/c3_history.md)、[c4](HISTORY/c4_history.md)、[c5](HISTORY/c5_history.md)。每轮按实际影响更新相关case，公共内容由case文件引用整体历史，避免复制后漂移。
- 每轮4–5条：父版/候选与完整SHA、方法及范围、分层验证、同协议性能及其他case回退、决定与原始证据链接。待验证、失败、无收益和回退都记录，不覆盖旧结论；后续反馈用追加条目纠正。
- 原始回执、快照、manifest和comparison继续存入 `others/scoreboard_and_submit/scoreboard/runs_sinkhorn/` 的独立目录；HISTORY是摘要与经验入口，两者相互链接。
- Windows历史已迁入 `/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/evidence/windows_20261023/`，原文/快照保持原样；其中“待提交”等旧状态仅为历史记录，当前状态读取两个状态 JSON 及其指向的证据。
- case编号只用于组织记录。未证实的形状、路径和瓶颈写未知；隐藏测试点不可由可见点或旧版本结果外推。沿用用户当前“保持现有求和次序和Div”约束，后续明确指示优先。
- 文档整理、历史维护和只读查阅不自动授权算法修改、编译、NPU、提交或持续优化；具体行动按用户当前授权执行。

## 面板 UI 维护约定（用户 2026-10-23 明确要求）

- 保留迁移前的原完整深色 UI，包括布局、CSS、图表、筛选、最优行和详情弹窗；切换赛题时只清理旧题数据、接入新题数据并做必要的数据适配。除非用户明确要求，不重做或替换 UI。
- 原 UI 基线存于 `others/migrations/sinkhorn_20261023/original_ui_restore/original.index.html`（相对工作区根目录）；维护时按该基线核对布局。数据严格绑定 SinkhornNorm 题目，不恢复初赛记录。


<!-- probe-turn-taking-v2 -->
### A/B提交轮流调度（2026-11-03用户纠正）

A/B可以同时存在有提交额度的active优化任务；任务存在本身不能作为停止另一个任务的条件。真正的POST与成绩采集窗口串行：等待共享锁、pending请求和对应账号冷却，上一笔实际提交的终态及同SID成绩采集完成后，另一工作区可继续。原有STOP、预算、身份/源码、未确认POST续查与去重守卫继续生效，已计费异常不得用新POST重试。

一笔B观测的同SID总分与完整耗时保存并校验后，允许A后续提交更新队伍latest；不得要求队伍最新SID永久等于B上一笔。相同SID重现时仍核对身份/结果/总分，跨SID仍检查公共参考；本笔尚未采集到有效总分就被覆盖、参考漂移或证据不完整仍停止。只使用本工作区实际序号维护账号轮换和预算，不把A的提交计为B提交。

后续B的10次探针控制器使用 workspace_control/probe_scheduler/current.json 指定的turn_taking_v2入口，并在本任务首次POST前将revision与四个运行文件SHA纳入预注册。旧已关闭实验的冻结脚本保留原样作为历史证据，不作为下一轮模板。此规则和修复不会自动重开任务、增加额度或启动POST。
