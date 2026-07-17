# Repo Continuity

**一个仓库，多种 Coding Agent，一套持续演进的项目知识。**

Coding Agent 很强，但它们的上下文是暂时的：会话会结束，上下文会被压缩，执行任务的 Agent 会变化，重要的项目知识也会被反复重新发现。

Repo Continuity 让仓库成为所有 Agent 共享的可信上下文：

- **接着做，而不是重新开始。** 新 Agent 不依赖聊天历史，也能恢复当前目标、决策、验证、风险和下一步。
- **只读取真正需要的知识。** 链接式知识和按需 Project Skills 避免每次加载完整项目历史。
- **小任务保持轻量。** Direct、Tracked、Governed 只在持续时间、协作或风险需要时增加流程。
- **让项目从开发中持续学习。** 已验证的修复和重复流程会固化为规则、笔记、runbook 或 Project Skills，而不是遗失在会话里。
- **让并行 Agent 安全协作。** Task branch、worktree、owned paths 和稳定 WORK 避免不同任务静默覆盖彼此。

所有必要状态都保存在可 Review 的 Markdown 和 Git 中。Companion Skill 可以自动完成初始化与检查，但项目不依赖服务、数据库、隐藏记忆或自主执行 runtime。

## 快速开始

以下命令固定到当前版本 `v4.1.1`。已经初始化的项目不会被自动修改，可以按需人工采用新版改进。

### 推荐：安装 Companion Skill

为 Claude Code 安装固定版本：

```bash
npx skills add \
  https://github.com/vector233/repo-continuity/tree/v4.1.1/skills/ai-collaboration-workflow \
  --skill ai-collaboration-workflow \
  -a claude-code \
  -g -y
```

为 Codex 安装固定版本：

```bash
npx skills add \
  https://github.com/vector233/repo-continuity/tree/v4.1.1/skills/ai-collaboration-workflow \
  --skill ai-collaboration-workflow \
  -a codex \
  -g -y
```

然后进入目标项目，让 Agent 执行：

```text
使用 $ai-collaboration-workflow 初始化当前仓库。
先检查已有项目规则，保留更严格的本地策略，并完整执行 INIT.md。
```

Skill 会先预览，再复制缺失文件，不会覆盖内容不同的仓库文件。如果 `AGENTS.md`、`CLAUDE.md` 或其他文件发生冲突，Agent 必须保留原文件并有意识地合并适用的共享规则。

### 只安装核心模板

Companion Skill 不是必需项。如果是一个尚不存在 Agent 指令或知识目录冲突的新仓库，可以复制固定版本的 payload：

```bash
git clone --branch v4.1.1 --depth 1 \
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
- `INIT.md` 和 `.ai-collaboration-workflow-template` 已删除；
- 没有创建空 WORK，也没有凭空发明项目 Skill；
- 只有项目策略或用户要求时才提交初始化变更。

初始化后，项目只依赖 Markdown、Git 和项目自身的验证系统。移除 Companion Skill 不会丢失项目知识或工作状态。

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

启动并行任务：

```text
将这个任务作为隔离的并行任务执行。使用 task branch 和独立 worktree，
声明 owned paths，并在修改前检查是否与活跃 WORK 重叠。
```

关闭 Tracked 或 Governed 工作：

```text
验证验收行为，记录最终提交和证据，关闭所有 Governed 门禁，
执行 Experience Promotion Check，更新长期知识，然后关闭 WORK。
```

没有安装 Skill 时，仅在 Tracked 或 Governed 路径下手工创建 WORK：

```bash
cp zettelkasten/templates/work-item.md \
  zettelkasten/work/WORK-$(date +%Y%m%d%H%M%S)-<slug>.md
```

直接更新 frontmatter 和 checkpoint。WORK 不会因为状态变化而移动。

## 可选的 Codex 模型路由

模板包含一个可选的 `.codex/` 适配层，将边界清晰的专业子任务路由到固定的 Codex 模型配置。流程路由与模型路由相互独立：先选择 Direct、Tracked 或 Governed，再判断是否由专业 Agent 提高结果质量或效率。

| Agent | 适用任务 | 默认模型策略 |
|---|---|---|
| root | 任务路由和普通工作 | `gpt-5.6-terra`，中等推理强度 |
| `explorer` | 只读代码定位、调用路径追踪和证据收集 | `gpt-5.6-terra`，低推理强度 |
| `implementer` | 已确认路径的单个局部改动与定向验证 | `gpt-5.6-terra`，中等推理强度 |
| `reviewer` | 只读正确性、安全性、回归和测试覆盖审查 | `gpt-5.6-sol`，高推理强度 |
| `architect` | 只读高影响架构决策或疑难根因分析 | `gpt-5.6-sol`，超高推理强度 |

适配层将 Codex 限制为最多三个线程和一层委派。作用域独立时，多个只读 Agent 可以并行；`implementer` 有写入权限，必须与同一任务 worktree 中的其他写入 Agent 串行执行。并发写入任务必须使用各自的 task branch 和 worktree。

表中的模型需要目标账户实际可用。如果某个模型不可用，只替换对应 `.codex/agents/*.toml` 的 `model` 配置为账户支持的等价模型。

## 可选的 Claude Code 模型路由

模板同时包含 `.claude/settings.json` 和 `.claude/agents/`。根会话默认使用 `opusplan`：计划模式使用 Opus，执行阶段自动使用 Sonnet；专业 Agent 则把旁路工作保留在各自独立且聚焦的上下文中。

| Agent | 适用任务 | 默认模型策略 |
|---|---|---|
| root | 任务路由、规划和普通工作 | `opusplan`：计划阶段 Opus，执行阶段 Sonnet |
| `explorer` | 只读代码定位、调用路径追踪和证据收集 | Haiku；仅 `Read`、`Grep`、`Glob` |
| `implementer` | 已确认路径的单个局部改动与定向验证 | Sonnet；可写 |
| `reviewer` | 只读正确性、安全性、回归和测试覆盖审查 | Opus |
| `architect` | 只读高影响架构决策或疑难根因分析 | Opus |

Claude Code 根据 Agent 的描述和当前上下文自动选择。需要固定角色时，使用 `@explorer`、`@implementer`、`@reviewer` 或 `@architect`。`implementer` 必须与同一任务 worktree 中的其他写入 Agent 串行执行；作用域独立的只读角色可以并行。如果模型不可用或被组织策略限制，Claude Code 会回退到继承或允许的模型，仓库工作流仍然保持不变。

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
- **可选**：Companion Skill 提供的知识检查、WORK 更新和受保护的 worktree 辅助脚本；以及面向专业 Agent 的 `.codex/` 和 `.claude/` 模型路由适配层。
- **非目标**：自主循环、任务调度、隐藏记忆、强制 CLI，以及替代 Git、Issue Tracker、CI 和项目测试系统。

知识网络使用纯 Markdown 和 Wiki 链接，可以作为兼容 Obsidian 的 vault 打开；Obsidian 只是可选编辑器，不是 runtime 或插件依赖。

## 经验固化

每个 WORK 都记录 Experience Candidates。在 checkpoint 和关闭任务时，根据经验形态选择最小目标：

| 经验 | 固化位置 |
|---|---|
| 所有 Agent 必须遵守的规则 | `AGENTS.md` |
| Bug 根因、错误假设 | `zettelkasten/gotchas.md` |
| 架构事实和不变量 | `zettelkasten/architecture.md` 或链接的领域知识笔记 |
| 简单环境或验证步骤 | quick reference / runbook |
| 有触发条件、验证和恢复步骤的稳定流程 | `project-skills/<name>/SKILL.md` 和 `project-skills/INDEX.md` |

项目 Skill 必须说明何时使用、何时不用、执行步骤、验证、恢复和来源。单次事故、低置信猜测和普通编码常识不升级成 Skill。

经验固化必须是幂等的：先搜索已有目标，原位更新 canonical 规则、笔记、runbook 或 Skill；内容已经是最新时记录 no-op。Tracked 或 Governed 工作先把共享目标加入 `owned_paths`；其他活跃 WORK 已拥有同一目标时，只保留一个写入者，或者延后固化。

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
.claude/                           Claude Code 的可选模型路由适配层
.codex/                            Codex 的可选模型路由适配层
AGENTS.md                         仓库级共享规则
zettelkasten/AI.md                最小上下文入口
zettelkasten/project.md           项目定位和范围
zettelkasten/architecture.md      架构事实和不变量
zettelkasten/workflow.md          任务路由与经验写回
zettelkasten/validation-runbook.md 项目验证流程
zettelkasten/work/                路径稳定的 WORK
project-skills/INDEX.md           项目 Skill 触发索引
```

`template/` 是唯一 canonical 下游模板；维护仓库不会再保存第二套根级知识库。

## 验证

下游项目使用自身构建、测试和 Review 命令验证行为。安装 Companion Skill 后，可以用可选 Doctor 检查链接、WORK 状态、项目 Skill 路由和跨 worktree 冲突等结构健康；Fresh-Agent 语义恢复仍是独立且需要真实证据的评估。

本模板仓库运行：

```bash
python3 scripts/validate_distribution.py
```

验证覆盖纯知识路径初始化、单一 WORK 路由、Governed 门禁、项目 Skill、并行 worktree、Wiki 链接、可选 helper 和 bootstrap 行为。

核心模板只依赖 Markdown 与 Git。辅助工具不产生独立状态，也不是理解或执行流程的前置条件。
