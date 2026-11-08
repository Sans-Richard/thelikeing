# SinkhornNorm 工作区说明

## 入口文件分工

| 内容 | 读取位置 |
|---|---|
| 协作规则、授权边界、工作顺序 | [AGENTS.md](AGENTS.md) |
| 计算合同与竞赛规则 | [RULES.md](RULES.md) |
| 新通用任务的基线、空间状态和预算 | A：`../workspace_control/baseline.json`；B：`../workspace_control/baseline.B.json`；共享 `../workspace_control/state.json` 及各自任务目录 |
| 未迁移旧轮次的兼容状态 | [current_baseline.json](current_baseline.json)、[active_campaign.json](active_campaign.json) |
| 优化方案、验证、完整耗时、失败、选版与经验 | [HISTORY/history.md](HISTORY/history.md)及c1–c5五个history文件 |
| 未知case的方法、编号猜测、当前结论及反例 | [hidden.md](hidden.md) |
| 隐藏点探测的计划、过程、逐笔结果、失败与恢复 | [hidden_history.md](hidden_history.md) |

本文件仅维护导航和操作说明。优化记录只写HISTORY中的六个固定history文件；未知case的方法和编号猜测写根目录hidden.md，探测过程与工作记录写根目录hidden_history.md（2026-11-05用户指定）。HISTORY不建子目录或其他md，不向本文件或AGENTS/RULES追加轮次履历。历史授权不自动生效，实际操作服从用户当前指令和实时状态。

<!-- generic-workspaces-v1:begin -->
## 两个通用工作区的使用

两个空间均可执行任意 case 优化或未知 case 分析。A 保留现有工程路径，B 使用 `workspaces/B/project`。两区独立选版，不要求基线同步。选版仅影响本区以后创建的任务；工作区注册、独立任务和不可变快照由 `workspace_control` 协调；账号、提交锁、pending 和结果库仍只有一套。

```text
enjoy_ur_time/
  sinkhorn_norm_problem_2360_template/   # A 工程，兼容现有轮次
  workspaces/A/workspace.json
  workspaces/A/tasks/<任务ID>/           # A 的状态展示、运行与证据
  workspaces/B/workspace.json
  workspaces/B/project/                  # B 工程，只复制源码与官方文件
  workspaces/B/tasks/<任务ID>/
  workspace_control/state.json           # 新任务与预算权威台账
  workspace_control/baseline.json        # A 的已选基线（保留旧路径）
  workspace_control/baseline.B.json      # B 的已选基线
  workspace_control/snapshots/<摘要>/source/
  workspace_control/submit_queue/        # 按需派发，无后台 worker
  others/scoreboard_and_submit/           # 共享旧提交后端、账号、锁、回执
```

以下命令在 `/mnt/workspace/enjoy_ur_time` 执行。先检查 `status`，不要从历史记录推导本轮授权：

```bash
./others/scoreboard_and_submit/workspace status
./others/scoreboard_and_submit/workspace baseline show --workspace A
./others/scoreboard_and_submit/workspace baseline show --workspace B
```

创建一个无 NPU、无 POST 权限的分析任务：

```bash
./others/scoreboard_and_submit/workspace task create --workspace B --kind analysis --target hidden --id B_hidden_analysis
./others/scoreboard_and_submit/workspace snapshot --workspace B --task B_hidden_analysis
./others/scoreboard_and_submit/submit --workspace B --task B_hidden_analysis --dry-run
./others/scoreboard_and_submit/workspace task close --workspace B --task B_hidden_analysis
```

`--dry-run` 只检查固定快照打包，不登录、不触网、不编译、不运行 NPU、不 POST。分析任务的源码保持与父版一致；分析脚本和输出存任务目录。可用 `workspace run --workspace B --task <ID> --resource cpu -- <命令>` 做已授权 CPU 工作，从独立 runtime 副本运行并留日志。

创建优化任务时用 `--kind optimize --target case1`（或其他目标）；未额外授权时也只有源码编辑与 CPU 权限。设备任务需要明确 `--allow-npu --authorization <本轮授权ID>`。有新的正式提交授权后，先以唯一 ID 执行 `workspace budget grant --posts <新增次数> --authorization <唯一ID> --reason <用户授权说明>`，创建任务时再用 `--submit-budget <次数>` 原子预留。建设工作区不预先授予这些权限或额度，不复用旧轮次预算。

任务创建成功会返回真实 `project_dir`、父基线和证据目录，应在该路径修改允许的 `kernel.asc` / `.asc/.h`。同一空间最多一个优化写任务；A 的旧轮次仍在运行时拒绝新 A 写任务。仅当工作副本偏离本区已选快照时才需处理；A、B版本相异无需额外参数。工作副本已有改动时默认拒绝覆盖，可显式 `--adopt-current` 保留并登记这些改动；此时实际起点和正式父基线分别记录。

正式提交必须显式绑定工作区和任务：`./others/scoreboard_and_submit/submit --workspace B --task <ID>`。可另传 `--account member1|member2|member3` 指定本次请求，默认在已授权账号中按新请求轮换。续查和对账必须用原账号：`--resume <SID>` / `--reconcile <JOB>`。新入口直接使用既有缓存会话；不会为恢复登录额外 POST。旧的、不带工作区参数的 submit 命令保持兼容。

需要先排队时，执行 `workspace queue enqueue --workspace B --task <ID>`，再 `workspace queue list`，最后用 `workspace queue dispatch --job <队列ID>` 显式派发一项。派发使用排队时的冻结源码，不读取后来编辑的工作副本；没有后台自动提交或自动重试。不确定请求先续查/对账，再 `workspace queue refresh --job <队列ID>`；确认派发进程已退出且没有记账或 POST 证据时，才可用 `workspace queue abandon --job <队列ID> --reason <原因>` 取消未发出的队列项。

选版示例：`workspace baseline select --workspace B --task <ID> --snapshot <候选快照ID> --expected-sha <B当前kernelSHA> --expected-snapshot <B当前完整快照ID> --reason <原因>`。只比较和更新目标工作区指针，不部署源码，不影响另一空间。`status` 的 `selected_baselines` 列出两区父版，`matches_selected_baseline` 比较各自工作副本；旧顶层 `selected_baseline` 和不带空间的 `baseline show` 仅代表 A。`baseline import-legacy --workspace A --expected-sha <旧系统选中kernelSHA>` 仅导入 A，既有任务均保持原父版。新 Python 调用使用 `from coordinator_v2 import Coordinator`（模块目录 `workspace_control/`）；旧单指针版本仅用于历史证据。

编译和 NPU 验证共用既有锁并统一排队，正式提交共用旧流程锁、pending、间隔、去重和账号策略；不能通过另复制一套提交器获得独立通道。每笔提交仍是完整算子，两个空间的收益必须合并后再验证。临时运行产物在 `/tmp/sinkhorn_workspaces`，关键源码、快照和日志在持久工作区；旧日期临时目录可能仍被当前任务引用，不按日期整删。
<!-- generic-workspaces-v1:end -->

## 工程与记录位置

- `sinkhorn_norm_problem_2360_template`：工作区 A 的现有工程和旧轮次兼容路径；B 的完整工程在 `workspaces/B/project`。新任务以自身记录的 `project_dir` 和冻结 SHA 为准，新基线由本区独立指针指向不可变快照；旧轮次仍按原状态核对源码。
- `others/scoreboard_and_submit/workspace`：通用工作区、任务、预算、快照和队列管理入口；`others/scoreboard_and_submit/submit --workspace <空间> --task <ID>`：任务绑定的检查、提交与续查入口。省略工作区参数时保留旧模式。
- `others/scoreboard_and_submit/scoreboard/runs_sinkhorn/`：每次源码快照、manifest、验证/提交结果与 comparison。
- `data.sinkhorn_norm.json`：提交工具的新题数据文件，与旧 `data.json` 隔离。

官方 `main.asc`、`CMakeLists.txt`、reference、sample、run 等文件保持原件，只在允许范围修改 `kernel.asc` 及工程根目录允许的 `.asc/.h`。默认不运行初赛 `perf_verify` 或 `verify_harness`，不自动 GitHub 推送。

## 旧轮次兼容检查入口

以下不带工作区参数的命令仅用于未迁移的旧轮次；新通用任务使用上节带 `--workspace`、`--task` 的入口。

在工作区根目录调用工具；以下为命令格式。已授权的新提交任务默认由主agent或轮次调度器按 `member1 → member2 → member3` 循环选账号，无需用户逐次指定；底层命令仍显式传入 `--account`：

`./others/scoreboard_and_submit/submit --dry-run --account <member1|member2|member3>`

离线检查目标题目、路径与配置，不登录、不 POST，也不运行 NPU。

`./others/scoreboard_and_submit/submit --doctor --account <member1|member2|member3>`

仅 GET，核对所选账号、题目、平台截止时间、停止状态及当前预算；不会创建提交。

本次平台用户历史接口实测会返回混合题目记录，即使传入 problemId 也未过滤；新工具还会在本地按题目和账号校验、过滤后再归档。CANNJudge API 未公开服务端额度；[赛事项目页](https://gitcode.com/cann-competition/026CANNChallenge_chengdu)当前写明每天最多 50 次、比赛期间取最后一次提交。可用 `--daily-limit <次数>` 设置更保守的本地日上限，服务端限制仍优先。

`./others/scoreboard_and_submit/submit --resume <sid> --account <原提交账号>`

仅续查现有提交，不 POST。不得跨账号续查旧任务或把已有结果挂到新源码。

账号配置：`member1` 为 ruinward，`member2` 为琉暝，`member3` 为孙新尧爱提交。已授权任务默认轮换三个账号，用户本轮另行指定时按其指令；每个任务选定后，提交、续查和reconcile始终使用原账号并显式传入 `--account`。各账号分别核对约195秒的当前观察冷却，同时满足现有提交器跨账号共享至少60秒间隔；三账号共享锁、pending拦截和授权总预算。具体冷却、429及轮换约定见 [AGENTS.md](AGENTS.md)。凭据不改动、不输出。

## 正式开发与提交流程

1. 读取规则，核对新工程、SDK/芯片、题目 ID 和账号；固定父版本及 SHA-256。
2. 修改候选，冻结独立源码快照和 manifest。后续验证、上传和结果均绑定该快照，不直接上传验证后仍在变化的工作文件。
3. 在隔离快照内运行未修改的官方 sample；这是正式提交的默认前置检查。记录结果与环境，失败不自动提交。
4. 获得正式提交授权后，实时检查题目、账号、截止时间、停止状态和预算，再通过同一入口显式带 `--account` 提交。出现未确认 POST 时先核对状态；取得 sid 后只使用续查。
5. 保存原始结果与 comparison，分别评价正确性和整体性能。决定保留或回退前检查活动源码是否被他人修改。

## 优化历史的维护位置

- 用户2026-11-01明确：只有实际针对某个case开展优化，才写该case对应的cN_history.md。优化case5时只写总history.md和c5_history.md；其他case的完整耗时及回退检查留在总history和原始证据，不向c1–c4复制case5优化经验。历史原件保留，新记录严格按目标case归属。


以下路径均相对本说明目录 `/mnt/workspace/enjoy_ur_time/the_thing_u_must_know`：

| 文件/目录 | 用途 |
|---|---|
| [HISTORY/history.md](HISTORY/history.md) | 整体优化历史、通用经验、版本对照和保留/回退 |
| [HISTORY/c1_history.md](HISTORY/c1_history.md) | case 1 对点记录 |
| [HISTORY/c2_history.md](HISTORY/c2_history.md) | case 2 对点记录 |
| [HISTORY/c3_history.md](HISTORY/c3_history.md) | case 3 对点记录 |
| [HISTORY/c4_history.md](HISTORY/c4_history.md) | case 4 对点记录 |
| [HISTORY/c5_history.md](HISTORY/c5_history.md) | case 5 对点记录 |
| [hidden.md](hidden.md) | 未知case与未确认参数的预测、证据、置信度和反例 |
| [/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/evidence/windows_20261023](/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/evidence/windows_20261023) | Windows原文、源码快照、脚本、验证报告与截图档案 |
| [/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/migration_manifest.json](/mnt/workspace/enjoy_ur_time/sinkhorn_norm_problem_2360_template/parallel_candidates/history_assets_migrated_20261029T150327+0800/migration_manifest.json) | 迁移来源、目标、SHA-256及排除项 |

工作顺序：读规则和整体history，对点任务再读对应cN_history；核对活动源码哈希后开展已授权工作。每轮结束在整体history记录共性结论，在实际影响的case文件中追加对点观察、验证、性能和决定，并链接同一份原始证据。未确认的case形状/属性映射保持未知，不将全局改动伪装成单case定向优化。

HISTORY的直接条目必须恰好是上述六个history文件，不允许子目录或额外Markdown。已有归档是原始证据，新的分析、方案、审查、交接和维护结论都归入固定文件。

新的原始结果仍由 `others/scoreboard_and_submit/scoreboard/runs_sinkhorn/` 承载；HISTORY存摘要和经验，避免重复维护漂移数据。失败和回退也保留，每轮4–5条；具体字段见AGENTS和case模板。

## 2026-10-29 官方评测数据更新

- CANNJudge 实时元数据确认 15 个测试点 ID 已全部更换，当前为 `6ae2fdfb1dac5d235b4b62aa` 至 `6ae2fdfb1dac5d235b4b62e3`；仍然公开前 5 项、隐藏后 10 项。旧 `6adb28021dac5d235bd73b8a` 至 `...bc2` 的耗时和分数不能与新数据直接横比。
- 平台只读模板 `main.asc` 更新为 `6609b3f782b87be34060c65116fa1bbd9f4b3ee0d07259ee5764a65829d3a755`，默认 `hc_sinkhorn_iters` 从 20 改为 15；`sample.py` 更新为 `a57f032ab81efc1607922df568bbbe1f5b198b3174fddf18dc0a3cd56c0ba3a0`，输入生成范围从 `[-2,2]` 改为 `[-50,50]`，迭代数从 20 改为 15。其余官方文件哈希未变。
- 题目正文合同没有变化：仍要求 float32、`H∈[2,128]`、`hc_sinkhorn_iters∈[1,32]`，eps 作用于每轮归一化，迭代轨迹不能提前停止，也不能用近似结果替代完整计算。静态 `cann.md` 仍写默认 20，但新版官方 sample 实际传入 15；kernel 必须使用运行时属性，不能固定默认值。题目元数据中的 `iterations=5` 在更新前后均为 5，不是算子迭代数。
- 当前正式 B2 源码 `be9c858f29bfcee4265ca6ac638441dd189d816eacf29e8c7b75ba5ae369cf25` 已在新版官方 sample 上编译、运行并通过精度校验。2026-10-29 member1 提交 `6ae31b861dac5d235b662617` 总体 Pass，公开五项为 `479.79 / 2.17 / 16.55 / 74.03 / 71.15 μs`；首次榜单观测为 35.12 分、第 20 名。
- 赛事项目页同时出现“每天最大提交次数 50 次、取比赛期间最后一次提交”和“以最优成绩作为最终成绩”两种表述；CANNJudge 实际配置仍为 `ranking_submission_mode=latest`。该冲突未获官方澄清。赛事页决赛结束写 11/07 11:30，而 CANNJudge 元数据为 12:00，应按更早的 11:30 保守处理。
- 提交前仍须执行 `doctor`。平台若更新只读模板，应先核对活动文件没有协作者新改动，再从实时模板同步；只允许保留自有的 `kernel.asc`。隐藏十项的逐点耗时、shape、精度和测试顺序仍未公开。

## 面板的手动使用方法

面板目录为 `/mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard`。面板保留原 UI，只读取当前 SinkhornNorm 题目及其复赛记录。以下命令用于更新和查看数据，不发起算子提交，不编译或运行 NPU。

### 1. 选定账号并更新数据

在 VS Code 的云端终端执行：

```bash
cd /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard
python3 track.py --account member1
```

按实际需要将 `member1` 换成 `member2` 或 `member3`，面板采集始终显式选择账号，不推进正式提交的轮换顺序。该命令仅以 GET 读取平台记录、榜单和提交详情，再更新云端面板缓存；浏览器刷新继续使用最近选定的账号。

若提示会话失效，使用已有账号工具检查并恢复所选账号的会话，然后重新执行 `track.py`：

```bash
cd /mnt/workspace/enjoy_ur_time
python3 others/tools/accounts.py check --account member1
```

不要把账号配置、密码或 Cookie 粘贴到聊天、写进 README 或提交到仓库。

### 2. 启动云端面板服务

若云端 `8000` 端口已有面板服务，直接使用，不要重复启动。没有运行时，在云端终端前台启动：

```bash
cd /mnt/workspace/enjoy_ur_time/others/scoreboard_and_submit/scoreboard
python3 server.py 8000
```

服务只监听云端 `127.0.0.1:8000`。保持该终端运行；在这个终端按 `Ctrl+C` 停止本次前台启动的服务。若提示 `Address already in use`，先确认已有服务，避免重复启动或直接结束不明进程。

### 3. 将端口转发到 Windows 并打开面板

可以在 VS Code 底部“端口 / Ports”面板中转发云端 `8000`，然后打开显示的本地地址。

也可以在 Windows PowerShell 中运行下列命令。先将最后的占位符替换为当前 VS Code Remote-SSH 实际使用的主机别名，不要照抄尖括号，也不要沿用已失效实例的别名：

```powershell
ssh -o ExitOnForwardFailure=yes -N -L 127.0.0.1:18080:127.0.0.1:8000 <当前SSH别名>
```

保持 PowerShell 窗口运行，浏览器打开 <http://127.0.0.1:18080/>。在这个窗口按 `Ctrl+C` 只停止本次端口转发。若本机 `18080` 已占用，先确认是否已有可用转发，或换用另一个空闲的本地端口；浏览器地址相应调整。

### 4. 刷新、查看记录与停止

浏览器重新加载页面会请求平台刷新，再读取面板缓存。连续刷新在 10 秒内可能使用缓存；平台刷新仍在进行、会话失效或网络失败时，页面保留已保存的数据，并在原更新时间位置提示状态。慢刷新结束后可以再次重新加载。`/data.json` 只读取缓存，本身不请求 CANNJudge。

原 UI 的 Pass 筛选、提交明细、源码详情和成绩曲线继续使用原来的入口。三个原曲线按钮仍保留；复赛曲线按真实采集时间展示成绩观测，“全部提交”按钮展示全部已采集观测，“最近 50 次”展示最近 50 个观测，按天使用北京时间聚合。云环境停止或 SSH 断开后，需要重新确认云端服务和端口转发是否仍在运行。不要仅因浏览器能打开旧页面就认定平台数据已经更新。

### 分数、排名和历史曲线的口径

本题当前官方榜单接口为：

```text
GET https://cannjudge.cn/api/problems/6adb28021dac5d235bd73b85/ranking?page=1&size=100
```

这是本题的分页排行榜，不使用初赛时期的赛事统计接口代替。榜单 `rows[].score` 是包含隐藏测试点的官方完整总分，`rank` 是该榜单的实际队伍排名，必须按题目、队伍和具体 `submission_id` 对应，不能只靠同分匹配。

2026-10-23 核对的题目配置为 `score_mode=1`、`ranking_submission_mode=latest`：全部 15 个测试点通过才计分，榜单采用最新提交，不能把个人历史最高分当成当前队伍榜单分。当前官方评分说明的单点公式为 `100 / (1 + ln(t / TBest) / ln(1.5))`，总分为 15 个点的平均值，其中 `t` 为该提交耗时、`TBest` 为当前单点最优耗时。依据为[本题元数据](https://cannjudge.cn/api/problems/6adb28021dac5d235bd73b85)和[官方当前评分说明源码](https://cannjudge.cn/js/pages/scoring-rules-content.js)。

接口只公开 5 个测试点的耗时，其余 10 个点为 `Hidden`。完整官方总分可以直接显示；缺少隐藏点耗时时，不能据 5 个公开点推算其余点、重算完整历史总分或“我们理论最优”的完整得分。

旧提交接口没有返回其提交瞬间的完整总分，因此真实历史“提交时成绩”无法追溯恢复。为保持原 UI，原“提交时成绩”列保留列名，首次采集到的官方分数加 `*`，悬停显示“首次采集官方成绩”和采集时间，不能声称它就是提交瞬间成绩。首次观测冻结保留，后续刷新不会覆盖；未采集到的历史记录仍为 `-`。首次观测与后续观测用于对比时，也不能当成历史榜单的还原。

“当前成绩”仅填入当前官方榜单所代表的那次提交的分数；不能把队伍当前分数复制给所有历史提交。虚拟排名也仅在有对应当前完整得分和完整榜单依据时显示。历史记录最后一次确实采集到的分数可以用于曲线，并保留其观测时间和来源；没有历史观测的记录保持未知，不补零，不拿当前分数倒填过去。切换曲线模式只改变展示范围，不改变这些数据口径。

以后若官方接口、题目配置或评分说明改变，应先重新核实数据适配逻辑。维护面板时保持原 UI；不要手改缓存中的分数、账号配置或活动 `kernel.asc` 来修正显示。

原始分页榜单证据保存在面板目录的 `ranking_observations/<采集时间>.json`；曲线观测和首次采集值随 `data.sinkhorn_norm.json` 保存。相同提交、分数和排名未变化时只更新最近确认时间，避免重复刷新产生重复曲线点。数据证据目录不是 HTTP 静态下载目录。


<!-- probe-turn-taking-v2 -->
### B探针轮流提交入口

B十次探针的现行可复用控制器由 /mnt/workspace/enjoy_ur_time/workspace_control/probe_scheduler/current.json 指定，当前revision为turn_taking_v2。给已经创建、已授权并已冻结证据的新B任务使用：

    python3 /mnt/workspace/enjoy_ur_time/workspace_control/probe_scheduler/turn_taking_v2/run_block_v2.py --task-dir /mnt/workspace/enjoy_ur_time/workspaces/B/tasks/<本轮任务ID> <起始序号> <结束序号>

本任务的analysis/prepost_evidence_registration.json须设置scheduler_revision为turn_taking_v2，formal_POST_approval保持本轮真实授权，frozen_files须包含当前revision的run_block_v2.py、submit_variant_v2.py、scheduling_guard.py和submission_window.py完整路径及SHA；其余源码、统计、账号、预算和模式审查仍必需。新入口不提供授权、不重开closed任务、不补交缺失观测。

此版本允许其他工作区active，实际pending/锁占用/冷却进入有界等待；B前一观测已完整保存后，队伍latest变成A的另一SID可正常继续。当前同SID分数、公共参考和本次采集完整性检查保持。维护证据在workspaces/B/tasks/B_submission_scheduling_fix_20261103；旧实验全部冻结文件未改。
