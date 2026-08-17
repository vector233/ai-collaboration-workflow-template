# Repo Continuity

**一个仓库，多种 Coding Agent，一套持续演进的项目知识。**

[![分发验证](https://github.com/vector233/repo-continuity/actions/workflows/validate.yml/badge.svg)](https://github.com/vector233/repo-continuity/actions/workflows/validate.yml)

Coding Agent 很强，但它们的上下文是暂时的：会话会结束，上下文会被压缩，执行任务的 Agent 会变化，重要的项目知识也会被反复重新发现。

Repo Continuity 让仓库成为所有 Agent 共享的可信上下文：

- **接着做，而不是重新开始。** 新 Agent 不依赖聊天历史，也能恢复当前目标、决策、验证、风险和下一步。
- **只读取真正需要的知识。** 链接式知识和按需 Project Skills 避免每次加载完整项目历史。
- **小任务保持轻量。** Direct、Tracked、Governed 只在持续时间、协作或风险需要时增加流程。
- **大型需求保持有界。** 已有 Epic 继续作为权威父级；没有外部父级时，只用一个轻量本地 Initiative 协调独立子 WORK，不建立递归任务树。
- **让项目从开发中持续学习。** 已验证的修复和重复流程会固化为规则、笔记、runbook 或 Project Skills，而不是遗失在会话里。
- **让并行 Agent 安全协作。** Task branch、worktree、owned paths 和稳定 WORK 避免不同任务静默覆盖彼此。

所有必要状态都保存在可 Review 的 Markdown 和 Git 中。Companion Skill 可以自动完成初始化与检查，但项目不依赖服务、数据库、隐藏记忆或自主执行 runtime。

## 快速开始

以下命令固定到当前版本 `v4.4.1`。已经初始化的项目不会被自动修改，需要升级时使用三方协调流程采用新版改进。

> [!TIP]
> **从 `v4.1.1` 或更早版本升级：** Companion Skill 已从 `ai-collaboration-workflow` 更名为 `repo-continuity`。
>
> 先执行 `npx skills remove ai-collaboration-workflow -g -y` 移除全局旧 Skill，再安装并调用 `$repo-continuity`。已经完整执行过 `INIT.md` 的仓库不需要重新初始化；如果上次初始化中断，继续完成 `INIT.md` 即可，Doctor 仍能识别旧 payload marker。

### 推荐：安装 Companion Skill

为 Claude Code 安装固定版本：

```bash
npx skills add \
  https://github.com/vector233/repo-continuity/tree/v4.4.1/skills/repo-continuity \
  --skill repo-continuity \
  -a claude-code \
  -g -y
```

为 Codex 安装固定版本：

```bash
npx skills add \
  https://github.com/vector233/repo-continuity/tree/v4.4.1/skills/repo-continuity \
  --skill repo-continuity \
  -a codex \
  -g -y
```

然后进入目标项目，让 Agent 执行：

```text
使用 $repo-continuity 初始化当前仓库。
先检查已有项目规则，保留更严格的本地策略，并完整执行 INIT.md。
```

`npx skills add` 只会安装 Companion Skill，不会在这一步把完整仓库 payload 复制到目标项目。调用 Skill 后，它才会运行内置 bootstrap，获取同一个固定版本，并预览或复制缺失的核心文件，不会覆盖内容不同的仓库文件。默认安装只包含核心，不会加入模型路由配置。如果 `AGENTS.md`、`CLAUDE.md` 或其他文件发生冲突，Agent 必须保留原文件并有意识地合并适用的共享规则。

### 只安装核心模板

Companion Skill 不是必需项。如果是一个尚不存在 Agent 指令或知识目录冲突的新仓库，可以复制固定版本的 payload：

```bash
git clone --branch v4.4.1 --depth 1 \
  https://github.com/vector233/repo-continuity.git

cp -R repo-continuity/template/. /path/to/your-project/
```

然后让 Agent 执行：

```text
完整执行 INIT.md。只写入已经验证的项目事实，检查知识链接，
所有验证通过后再删除初始化文件。
```

如果目标仓库已经有 `AGENTS.md`、`CLAUDE.md`、`zettelkasten/` 或 `project-skills/`，不要直接执行覆盖式复制；应使用 Companion Skill，或者显式合并这些文件。

## 初始化完成标准

- 已有仓库指令和更严格的 Git 策略得到保留；
- 项目目的、技术栈、架构、命令和验证流程来自已确认事实；
- 模板占位符已经清理；
- Wiki 链接和知识必填字段验证通过；
- `INIT.md`、`.repo-continuity-template` 和可能存在的旧 `.ai-collaboration-workflow-template` marker 已删除；
- 没有创建空 WORK，也没有凭空发明项目 Skill；
- 只有项目策略或用户要求时才提交初始化变更。

初始化后，项目只依赖 Markdown、Git 和项目自身的验证系统。移除 Companion Skill 不会丢失项目知识或工作状态。

## 安全协调升级

已经初始化的项目不是可随时覆盖的模板副本，而是“旧上游基线 + 项目事实、规则和持续沉淀的 Skill”。安装目标版本 Skill 后，进入项目告诉 Agent：

```text
使用 $repo-continuity 把这个已初始化仓库升级到 Skill 固定的目标版本。
创建隔离的升级任务分支，预览三方协调，只应用安全变更，保留本地定制，
解决剩余冲突，完成验证，最后再推进模板基线。
```

Companion Skill 会真正比较旧版上游、当前项目和目标上游。可以先生成只读报告和 dry-run。执行应用后，它会自动加入上游新增文件、采用纯上游修改并完成无冲突的文本三方合并，同时保留纯本地修改；真实冲突和上游删除仍留给显式检查。

应用过程要求干净的任务分支，并以事务方式写入；不会在 `main` 或 `master` 上执行，不会跟随目标 symlink，也不会自行修改 `Template baseline`。解决剩余路径后，运行项目验证、检查最终 Git Diff，最后才推进基线。详见[升级指南](../upgrading.zh-CN.md)和 [Companion Skill](../../skills/repo-continuity/SKILL.md#reconcile-an-upgrade)。

## 日常使用

开始普通开发任务时描述结果，不要要求固定文档链：

```text
按照 AGENTS.md 和 zettelkasten/AI.md 处理这个任务：
<任务描述>
选择最轻但安全的路径，并保持长期项目知识为最新状态。
```

Agent 自行选择：

| 路径 | 使用场景 | 流程状态 |
|---|---|---|
| Direct | 本地、可逆、低风险、一个上下文 | 无 WORK，验证后提交 |
| Tracked | 行为改动、调试连续性、多上下文 | 一个稳定 `WORK-*` |
| Governed | 高风险、重要不确定性、独立审批、迁移、发布、多人协调 | 同一个 `WORK-*`，增加明确门禁和证据 |

## 大型需求不等于大型 WORK

不要让一个 WORK 变成无限增长的 Epic 日志。如果结果仍然只有一个紧密耦合的验收和回滚边界，就继续使用一个 WORK；如果多个结果可以分别验收、路由、分配、验证、回滚或发布，则拆成独立 WORK。

只允许下面这种有界层级：

```text
已有外部 Epic / Issue / Milestone（优先）
└── 多个独立 WORK

或者，在没有合适外部父级时：

一个可选的本地 INITIATIVE
├── 独立 WORK-A
├── 独立 WORK-B
└── 独立 WORK-C
```

不存在第三层。WORK 不能成为另一个 WORK 或 Initiative 的父级。每个子 WORK 保留自己的路径选择、task branch 或 worktree、验收、`depends_on` 依赖、验证、checkpoint、Learning Check 和关闭状态。`depends_on` 是严格前置条件：所有依赖完成前，子 WORK 必须保持 backlog 或 blocked；如果只是最终集成顺序不同，应使用协调说明而不是 `depends_on`。Initiative 只保存总体目标、共享门禁、集成顺序、派生汇总和下一项协调动作。长期事实仍写入链接的 Zettel、Decision、Runbook 或项目 Skill。

如果 Jira、GitHub、GitLab 或其他项目原生系统已经管理父级生命周期，则在每个子 WORK 中设置 `external_parent`，不要在仓库内镜像 Epic。确实需要仓库内协调时，可以复制 `zettelkasten/templates/initiative.md`，或使用可选 helper：

```bash
python3 skills/repo-continuity/scripts/workflow_task.py initiative-new <slug>
python3 skills/repo-continuity/scripts/workflow_task.py new <child-slug> \
  --initiative <INITIATIVE-ID> --depends-on <WORK-ID>
```

外部记录是权威父级时，使用 `--external-parent <tracker-ref>` 代替 `--initiative`。恢复任务时从子分支和子 WORK 开始；只有共享门禁、依赖或集成约束影响当前切片时才加载 Initiative，默认不加载兄弟 WORK。

恢复长任务：

```text
根据当前 Git 分支找到对应 WORK，读取 checkpoint 和 next_action，
只加载其中链接的知识和匹配的项目 Skill，然后继续执行。
```

暂停或交接长任务：

```text
更新现有 WORK，使一个全新的 Agent 能恢复路径、验收状态、已完成步骤和提交、
准确验证结果、未解决风险、下一步动作和经验候选。提交 checkpoint，不创建新的交接文件。
```

只在有意义的边界记录 checkpoint：每个 Tracked 或 Governed 有限切片完成后，以及未完成任务将要交接、长时间暂停、切换 Agent 或会话、发生可检测的上下文压缩之前，或者继续依赖聊天会丢失决策时。能在当前上下文完成、验证并提交的 Direct 工作仍然不需要 WORK；否则升级为 Tracked。运行时上下文遥测始终是可选能力，不是核心依赖。

验证完成后，每条路径都执行一次轻量 Learning Check。Direct 工作没有已验证的可复用经验时不创建任何产物；如果发现应该改变共享项目知识的经验，则先升级为 Tracked，再进行固化，使证据和决策可恢复。

启动并行任务：

```text
将这个任务作为隔离的并行任务执行。使用 task branch 和独立 worktree，
声明 owned paths，并在修改前检查是否与活跃 WORK 重叠。
```

关闭 Tracked 或 Governed 工作：

```text
验证验收行为，记录最终提交和证据，关闭所有 Governed 门禁，
执行 Learning Check，决定所有候选，验证长期知识写回，然后关闭 WORK。
```

没有安装 Skill 时，仅在 Tracked 或 Governed 路径下手工创建 WORK：

```bash
cp zettelkasten/templates/work-item.md \
  zettelkasten/work/WORK-$(date +%Y%m%d%H%M%S)-<slug>.md
```

直接更新 frontmatter 和 checkpoint。WORK 不会因为状态变化而移动。

启用 Companion Skill 后，可以让 Agent 调用其内置 WORK helper；实际绝对路径由宿主安装位置决定。在 Repo Continuity 源码 checkout 中，对应命令如下：

```bash
python3 skills/repo-continuity/scripts/workflow_task.py learn-add <WORK-ID> \
  --candidate "<经验>" --shape project-skill --evidence "<已验证证据>"
python3 skills/repo-continuity/scripts/workflow_task.py learn-decide <WORK-ID> \
  --candidate "<经验>" --decision promoted \
  --destination "project-skills/<name>/SKILL.md; project-skills/INDEX.md" \
  --reason "<写回和验证结果>"
python3 skills/repo-continuity/scripts/workflow_task.py learn-status <WORK-ID> --require-complete
```

Tracked 或 Governed 任务没有候选时，使用 `learn-none <WORK-ID> --reason "<没有已验证可复用经验的原因>"`。辅助命令只管理 Markdown 行和关闭检查；经验价值判断、目标写入和检索验证仍由 Agent 完成。

## 可选的 Codex 模型路由

仓库在 `adapters/codex/` 下提供独立的 Codex overlay。默认 bootstrap 和直接复制 `template/` 都不会安装它。需要时显式启用：

```bash
python3 skills/repo-continuity/scripts/bootstrap_template.py \
  --source . \
  --target /path/to/your-project \
  --with-model-routing codex \
  --dry-run

python3 skills/repo-continuity/scripts/bootstrap_template.py \
  --source . \
  --target /path/to/your-project \
  --with-model-routing codex
```

对于没有冲突的新项目，也可以在复制 `template/.` 后再手工复制 `adapters/codex/.`。流程路由与模型路由相互独立：先选择 Direct、Tracked 或 Governed，再判断是否由专业 Agent 提高结果质量或效率。root 继续使用用户或当前 Codex 会话选择的模型。

| Agent | 适用任务 | 默认模型策略 |
|---|---|---|
| root | 任务路由和普通工作 | 用户或当前会话选择；overlay 不覆盖 |
| `explorer` | 只读代码定位、调用路径追踪和证据收集 | `gpt-5.6-terra`，低推理强度 |
| `implementer` | 已确认路径的单个局部改动与定向验证 | `gpt-5.6-terra`，中等推理强度 |
| `reviewer` | 只读正确性、安全性、回归和测试覆盖审查 | `gpt-5.6-sol`，高推理强度 |
| `architect` | 只读高影响架构决策或疑难根因分析 | `gpt-5.6-sol`，超高推理强度 |

适配层将 Codex 限制为最多三个线程和一层委派。作用域独立时，多个只读 Agent 可以并行；`implementer` 有写入权限，必须与同一任务 worktree 中的其他写入 Agent 串行执行。并发写入任务必须使用各自的 task branch 和 worktree。

表中的模型需要目标账户实际可用。如果某个模型不可用，只替换对应 `.codex/agents/*.toml` 的 `model` 配置为账户支持的等价模型。

## 可选的 Claude Code 模型路由

`adapters/claude/` 下的独立 overlay 同样需要显式启用：

```bash
python3 skills/repo-continuity/scripts/bootstrap_template.py \
  --source . \
  --target /path/to/your-project \
  --with-model-routing claude \
  --dry-run

python3 skills/repo-continuity/scripts/bootstrap_template.py \
  --source . \
  --target /path/to/your-project \
  --with-model-routing claude
```

使用 `--with-model-routing all` 可以同时安装两个 overlay。对于没有冲突的新项目，也可以在核心模板之后手工复制 `adapters/claude/.`。该 overlay 只安装 `.claude/agents/`，不会安装 `.claude/settings.json`，所以 root 继续使用用户当前选择的 Claude Code 模型，专业 Agent 使用固定的模型和工具策略。

| Agent | 适用任务 | 默认模型策略 |
|---|---|---|
| root | 任务路由、规划和普通工作 | 用户或当前客户端选择；overlay 不覆盖 |
| `explorer` | 只读代码定位、调用路径追踪和证据收集 | Haiku；仅 `Read`、`Grep`、`Glob` |
| `implementer` | 已确认路径的单个局部改动与定向验证 | Sonnet；可写 |
| `reviewer` | 只读正确性、安全性、回归和测试覆盖审查 | Opus |
| `architect` | 只读高影响架构决策或疑难根因分析 | Opus |

Claude Code 根据 Agent 的描述和当前上下文自动选择。需要固定角色时，使用 `@explorer`、`@implementer`、`@reviewer` 或 `@architect`。`implementer` 必须与同一任务 worktree 中的其他写入 Agent 串行执行；作用域独立的只读角色可以并行。如果模型不可用或被组织策略限制，Claude Code 会回退到继承或允许的模型，仓库工作流仍然保持不变。

## 评估模型路由

不能仅凭配置推断额度节省。[模型路由 A/B 评估](../model-routing-evaluation.md) 定义了六类成对任务、全新会话来源、独立验收结果、高风险漏检检查、专业角色检查、耗时和可选的可比额度单位。评估器会明确区分合成测试夹具与真实 Agent 证据；无法获得可比额度数据时，成本结论会保持为“不确定”。

## 核心模型

```text
任务
  -> 路由：Direct | Tracked | Governed
  -> 只加载当前 WORK 和匹配知识
  -> 按需实现、验证和 Review
  -> 在有意义的上下文边界保存可恢复状态
  -> 每个产生持久变更的上下文或完整切片形成提交
  -> 将可复用经验升级为规则、知识笔记、runbook 或项目 Skill
```

Router 不只看代码量，还判断影响范围、不确定性、风险与可逆性、持续时间、协作方式和验证要求。小型权限或数据修改也可能直接升级为 Governed。

## 产品边界

核心产品是可链接、可 Review 的仓库知识，以及面向交付结果的轻量契约。它规定交接时必须保留什么，不规定 Agent 必须如何思考或运行哪个命令。

- **核心**：`AGENTS.md`、`zettelkasten/` 知识入口和链接、按需记录的稳定工作意图、验证证据与经验写回。
- **可选**：Companion Skill 提供的知识检查、WORK 和 Learning Candidate 更新、受保护的 worktree 辅助脚本；以及从 `adapters/` 显式安装的专业 Agent 模型路由 overlay。
- **非目标**：自主循环、任务调度、隐藏记忆、强制 CLI，以及替代 Git、Issue Tracker、CI 和项目测试系统。

知识网络使用纯 Markdown 和 Wiki 链接，可以作为兼容 Obsidian 的 vault 打开；Obsidian 只是可选编辑器，不是 runtime 或插件依赖。

## 仓库学习闭环

每个任务在验证后检查用户纠正、可重复根因、缺失不变量、可复用命令序列或稳定流程。Direct 工作没有已验证候选时保持零产物；存在长期候选时，先升级为 Tracked 再写共享知识。每个 Tracked 或 Governed WORK 记录候选证据和最终的 `promoted`、`updated`、`no-op` 或 `not-promoted` 决策。

| 经验 | 固化位置 |
|---|---|
| 所有 Agent 必须遵守的规则 | `AGENTS.md` |
| Bug 根因、错误假设 | `zettelkasten/gotchas.md` |
| 架构事实和不变量 | `zettelkasten/architecture.md` 或链接的领域知识笔记 |
| 简单环境或验证步骤 | quick reference / runbook |
| 有触发条件、验证和恢复步骤的稳定流程 | `project-skills/<name>/SKILL.md` 和 `project-skills/INDEX.md` |

项目 Skill 必须说明何时使用、何时不用、执行步骤、验证、恢复和来源。单次事故、低置信猜测和普通编码常识不升级成 Skill。

经验固化必须是幂等的：先搜索已有目标，原位更新 canonical 规则、笔记、runbook 或 Skill；内容已经是最新时记录 no-op。Tracked 或 Governed 工作先把共享目标加入 `owned_paths`；其他活跃 WORK 已拥有同一目标时，只保留一个写入者，或者延后固化。

写回始终表现为 task branch 上可 Review 的 Git Diff，而不是模型隐藏记忆。仓库级指令、架构约束、安全或权限行为、发布流程和已有 Skill 契约，需要和等价代码或策略变更相同的证据、Review 或 Governed 门禁。项目 Skill 保留可移植的 `SKILL.md` 核心，宿主特有的激活元数据放入显式 adapter。

知识健康分为两层。普通交接只检查结构：分支与 WORK 的映射、checkpoint 字段、链接、所有权和 Skill 路由。重要的多上下文交接或恢复协议发生变化时，再让一个没有聊天历史的真实 Fresh Agent 执行语义恢复探针，在修改前报告路径、验收状态、checkpoint、验证、风险和下一步。手写预期响应只能测试 evaluator，不能证明 Agent 可以恢复；详见 [Fresh-Agent Resume Evaluation](../fresh-agent-resume-evaluation.md)。

## 项目反哺模板

下游 Agent 只在重要 checkpoint、任务关闭或用户纠正流程行为后，静默判断是否出现有证据的模板摩擦。正常任务不创建反馈文件。

项目特有经验仍写入本项目的规则、架构、gotcha、runbook 或项目 Skill。重复或高影响的模板级问题，以及明确的厂商特有问题，才按需写入 `zettelkasten/workflow-observations.md`。未经用户明确批准，不得发送遥测或创建上游 Issue/PR。

## 并行开发和提交

Tracked 和 Governed 工作使用 task branch；同时进行的任务或 Agent 使用独立 Git worktree：

```bash
work_id="WORK-$(date +%Y%m%d%H%M%S)-<short-name>"
git worktree add ../<short-name> -b "task/${work_id}" <base>
```

默认分支只用于集成。有依赖或路径重叠的任务需要明确集成计划，共享知识固化通过 `owned_paths` 确立唯一写入者。每个产生持久变更的 Agent 上下文或完整实现切片必须形成当前任务提交；纯分析和只读 Review 不创建空提交。

## 主要结构

```text
template/                          默认安装的核心模板
  AGENTS.md                        仓库级共享规则
  zettelkasten/AI.md               最小上下文入口
  zettelkasten/workflow.md         任务路由与经验写回
  zettelkasten/validation-runbook.md 项目验证流程
  zettelkasten/work/               路径稳定的 WORK
  project-skills/INDEX.md          项目 Skill 触发索引
adapters/
  codex/.codex/                    Codex 显式启用的模型路由 overlay
  claude/.claude/                  Claude Code 显式启用的模型路由 overlay
```

`template/` 是 canonical 默认下游核心；`adapters/` 保存独立的显式 opt-in overlay，默认安装不会复制它们。维护仓库不会再保存第二套根级知识库。

## 验证

下游项目使用自身构建、测试和 Review 命令验证行为。安装 Companion Skill 后，可以用可选 Doctor 检查链接、WORK 状态、项目 Skill 路由和跨 worktree 冲突等结构健康；Fresh-Agent 语义恢复仍是独立且需要真实证据的评估。

本模板仓库运行：

```bash
python3 scripts/validate_distribution.py
```

验证覆盖纯核心初始化、模型路由显式 opt-in、单一 WORK 路由、Governed 门禁、项目 Skill、并行 worktree、Wiki 链接、可选 helper 和 bootstrap 行为。

真实模型路由的质量和可比额度证据按 [模型路由 A/B 评估](../model-routing-evaluation.md) 收集；评估器不会把自身的合成回归夹具当成 Agent 效果证据。`.github/workflows/validate.yml` 会在 Pull Request 和 `main` 上重复检查版本一致性、完整分发生命周期、空白错误，以及官方 Skills CLI 的安装和 bootstrap 冒烟测试。

核心模板只依赖 Markdown 与 Git。辅助工具不产生独立状态，也不是理解或执行流程的前置条件。
