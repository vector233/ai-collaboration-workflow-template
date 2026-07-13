# AI 协作流程模板

这是面向 AI coding agents 的项目知识网络和轻量交付契约。它让上下文暂时、来源不同、可能并行工作的 Agent 获得同一套可信项目知识，并把开发中新产生的知识可靠地写回仓库。

`v4.1.0` 是当前面向新项目的模板。固定安装这个版本的新项目包含上下文边界保存、Fresh-Agent 语义恢复检查和幂等知识写回；已经初始化的项目不会自动更新，可以按需人工采用其中的改进。v4 系列不迁移或模拟早期目录结构，原因见[为什么 v4 是破坏性更新](#为什么-v4-是破坏性更新)。

## 快速开始

### 推荐：安装 Companion Skill

为 Claude Code 安装固定版本：

```bash
npx skills add \
  https://github.com/vector233/ai-collaboration-workflow-template/tree/v4.1.0/skills/ai-collaboration-workflow \
  --skill ai-collaboration-workflow \
  -a claude-code \
  -g -y
```

为 Codex 安装固定版本：

```bash
npx skills add \
  https://github.com/vector233/ai-collaboration-workflow-template/tree/v4.1.0/skills/ai-collaboration-workflow \
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
git clone --branch v4.1.0 --depth 1 \
  https://github.com/vector233/ai-collaboration-workflow-template.git

cp -R ai-collaboration-workflow-template/template/. /path/to/your-project/
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

## 为什么 v4 是破坏性更新

早期版本使用多个编号知识目录，并为需求、技术设计、执行计划和 Review 分别维护工件。这种结构可以显式展示每个阶段，但真实 AI 辅助开发暴露出的成本已经超过收益：

- 小型和中型任务也会产生没有独立决策价值的文档；
- 范围、状态、计划和验证信息在多个文件中重复；
- 生命周期文件移动或改名会造成链接波动，恢复入口容易失效；
- 每次结构调整都必须同步模板、Skill、示例、脚本和文档，容易遗漏；
- Agent 为重建当前状态需要加载额外层级，增加 token 消耗和过期假设风险；
- 并行开发会放大共享索引和流程文件上的冲突。

v4 把仓库知识重新确立为产品，并让流程成本与任务风险匹配：

- 长期知识使用 `project.md`、`architecture.md`、`gotchas.md` 等扁平语义入口；
- Direct 任务不创建流程记录；
- Tracked 和 Governed 都只使用一个稳定 WORK，Governed 的决策和审批表现为门禁；
- Git、Issue、Pull Request、CI 和发布系统继续拥有它们本来的生命周期；
- Companion 工具保持可选，不拥有隐藏的项目状态。

项目不提供自动迁移，是因为旧项目可能同时定制了知识内容和流程工件。通用转换器无法可靠地区分长期事实与过期流程状态；同时保留两套模型也会延续 v4 想消除的复杂度。已有项目可以人工选择采用 v4 的部分原则，但 v4 只定义干净的新项目契约。

## 产品边界

核心产品是可链接、可 Review 的仓库知识，以及面向交付结果的轻量契约。它规定交接时必须保留什么，不规定 Agent 必须如何思考或运行哪个命令。

- **核心**：`AGENTS.md`、`zettelkasten/` 知识入口和链接、按需记录的稳定工作意图、验证证据与经验写回。
- **可选**：Companion Skill 提供的知识检查、WORK 更新和受保护的 worktree 辅助脚本。
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
