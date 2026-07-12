# AI 协作流程模板：中文说明

> 这里是中文说明层，不是模板源文件的中文副本。唯一 canonical 模板位于 `template/`。

## 这个项目是什么

`AI Collaboration Workflow Template` 是一套给 AI coding agents 使用的项目文档模板。它的目标不是写更多文档，而是让 AI 在长期项目中能稳定回答这些问题：

- 当前任务最少需要读哪些上下文？
- 这次改动的需求、非目标和验收标准是什么？
- 开发前技术方案是否已经足够明确？
- 完成后用什么验证结果证明它真的可用？
- review 反馈是否有证据，如何处理？
- 本轮学到的架构事实、测试流程或踩坑应该写回哪里？
- 长任务或问题修复暴露出的重复性错误，是否应该升级成项目基础规则？

它借鉴 Zettelkasten 的笔记方式：每个 note 尽量短、聚焦一个主题，并通过链接组成知识网络。模板里的 `zettelkasten/` 也可以作为 Obsidian vault 使用。

## 为什么不复制一套中文模板

这个仓库采用英文作为唯一模板源。中文内容只做理念和使用说明，不复制完整目录和模板文件。

这样做是为了避免：

- 英文和中文模板字段不一致；
- 工作流规则在两个版本里漂移；
- 用户不知道哪个版本才是最新；
- 维护成本随着模板演进翻倍。

如果需要中文文档，建议只维护这类说明文档，而不是翻译整套 `zettelkasten/`。

## 核心目录

模板初始化后，主要使用这些目录：

| 路径 | 作用 |
|---|---|
| `AGENTS.md` | AI agent 的仓库级工作规则 |
| `CLAUDE.md` | Claude Code 适配层，指向 `AGENTS.md` 和知识库入口 |
| `zettelkasten/AI.md` | 当前知识库入口，说明如何导航项目上下文 |
| `zettelkasten/CURRENT.md` | 当前 active work、open review、验证快照和 next action |
| `zettelkasten/00-governance/ai-workflow.md` | AI 协作流程：上下文、需求、设计、验证、review、规则升级和回写 |
| `zettelkasten/06-requirements/` | 需求状态机：`backlog -> in-progress -> done` |
| `zettelkasten/08-technical-designs/` | 按需使用的独立技术方案：`pending -> approved -> implemented` |
| `zettelkasten/09-implementation-plans/` | 按需使用的独立实施计划 |
| `zettelkasten/07-review/` | review 交接状态机：`pending -> in-review -> done` |
| `zettelkasten/05-reference/e2e-test.md` | 项目具体 E2E / smoke / 验证命令 |
| `zettelkasten/00-governance/gotchas.md` | 历史踩坑、根因和教训 |
| `scripts/workflow_doctor.py` | 检查工作流状态、wiki 链接、占位符、review handoff 和规则升级字段 |

## 推荐使用流程

1. 安装 companion Skill，然后让 AI 执行：

   ```text
   Use $ai-collaboration-workflow to initialize this repository.
   ```

   也可以把 canonical payload 完整复制到已有项目：

   ```bash
   cp -R /path/to/ai-collaboration-workflow-template/template/. /path/to/your-project/
   ```

2. 如果手工复制 payload，让 AI 执行：

   ```text
   Initialize this knowledge base by following INIT.md.
   ```

3. 回答项目名称、技术栈、仓库类型、常用命令、域名端口等问题。
4. AI 会替换占位符、合并项目自己的 `AGENTS.md` 规则、初始化第一批 note 并删除 `INIT.md`。只有用户要求或仓库规则明确要求时才提交。
5. 后续任务按 `REQ -> [TECH] -> [PLAN] -> implementation & validation -> REVIEW -> Rule Promotion Check -> writeback` 推进。方括号表示独立文档按风险和复杂度选用。

`Rule Promotion Check` 用于解决长任务或问题修复后下次又犯同类错误的问题。AI 在关闭长任务、bug fix、review fix 或重复踩坑时，需要判断这次经验是否应该升级成稳定项目规则：仓库级 agent 行为写入 `AGENTS.md`，bug 根因和错误假设写入 `gotchas.md`，架构不变量写入 `02-architecture/` 或 `04-cross-cutting/`，验证和环境步骤写入 `05-reference/e2e-test.md` 或 `01-overview/quick-reference.md`。一次性现象、低置信猜测和临时事故只记录在当前 REQ 或 REVIEW，不升级成规则。

任务按重量选择最轻安全路径：

| 模式 | 适用情况 | 最小状态 |
|---|---|---|
| Tiny | 非行为变更、本地、可逆、明显 | 最终回复和验证结果 |
| Bounded | 局部行为变更或已知根因 bug | REQ 内联技术准备和 REVIEW |
| Standard | 有明确产品或技术决策 | REQ，必要时 TECH |
| Complex | 多 slice、多 session、迁移、发布或协作 | REQ，按需 TECH/PLAN |

工作流状态变更后可以运行：

```bash
python3 scripts/workflow_doctor.py
```

它会检查核心文件、初始化占位符、wiki 链接、REQ/TECH/REVIEW 状态目录、REVIEW 是否包含 Rule Promotion Check、PLAN 状态、`CURRENT.md` 是否引用 active work，以及 open review / active requirement 的路由提醒。初始化完成后可用 `--strict` 让 warning 也导致命令失败。

本仓库自身不维护第二套根 `zettelkasten/`。请使用 Skill 或复制 `template/` 的内容；不要把整个仓库根目录当作干净模板。

## 跨 AI 协作

核心流程不绑定某一家 AI：

| AI | 自动读取入口 | 共享项目状态 |
|---|---|---|
| Codex | `AGENTS.md` | `zettelkasten/` |
| Claude Code | `CLAUDE.md` 通过 `@AGENTS.md` 导入同一份规则 | `zettelkasten/` |
| 其他能读取仓库的 AI | 明确要求先读取 `AGENTS.md` | `zettelkasten/` |

聊天记录、Codex memory、Claude auto memory 或其他工具的本地状态都只能作为辅助缓存，不能成为项目继续推进所必需的信息。新的 AI 应当能从当前 REQ、存在时的 TECH / PLAN、open REVIEW、验证证据、worktree 状态、风险和 next action 恢复工作。

Skill 使用 Codex 和 Claude Code 都支持的 Agent Skills 开放格式；项目初始化完成后，即使没有安装 Skill，仓库内的规范仍然能够独立指导 AI。

## 可选外部流程 Skill

模板不依赖 Superpowers 或其他流程插件。没有安装这些插件时，Codex、Claude Code 或其他 AI 仍然直接使用：

```text
REQ -> [TECH] -> [PLAN] -> implementation & validation -> REVIEW -> Rule Promotion Check -> writeback
```

独立 TECH 用于架构、接口、数据、安全、部署、跨模块或方案不确定的变更；独立 PLAN 用于多 slice、多 session、多 AI、依赖顺序或迁移发布协调。根因明确、影响局部的小型 BUG 可以在 REQ 内记录技术准备和实施 slices，不必创建独立 TECH 或 PLAN。

如果项目安装了 Superpowers，仓库规则会把它的 brainstorming、planning、TDD、debugging 和 review 过程映射到选定的 REQ、TECH、PLAN、REVIEW、gotchas 和 runbook。它不能建立 `docs/superpowers/` 平行事实源。

因此这只是兼容层：

- 模板不会安装 Superpowers；
- 没有任何外部命令是必需的；
- 禁用或删除 Superpowers 不影响知识库工作流；
- 外部 Skill 默认要求的 commit、branch 或 worktree 仍需服从项目 Git 规则和用户明确指令。

## Skill 安装

仓库内提供一个可选 skill：

```text
skills/ai-collaboration-workflow/
```

它用于帮助 AI 正确使用这套模板：安全引导或执行模板安装、初始化项目、选择交付路径、按需创建 REQ/TECH/PLAN/REVIEW、检查开发准入、运行 workflow doctor、记录验证结果、处理带证据的 review 反馈、执行 Rule Promotion Check，以及回写 gotchas / architecture / runbook。

Skill 自带 bootstrap 脚本。脚本会先预览变更，只复制缺失文件、跳过相同文件，并把内容不同的已有文件报告为冲突，不会直接覆盖项目已有的 `AGENTS.md`、`CLAUDE.md` 或知识库内容。默认从 canonical Git 仓库的 `template/` 获取 payload；无网络环境可以传入仓库 checkout 或直接传入 `template/`。

### Claude Code

个人级安装，所有项目都可用：

```bash
mkdir -p ~/.claude/skills
cp -R skills/ai-collaboration-workflow ~/.claude/skills/
```

项目级安装，只对当前仓库生效，并可提交到 Git：

```bash
mkdir -p .claude/skills
cp -R skills/ai-collaboration-workflow .claude/skills/
git add .claude/skills/ai-collaboration-workflow
```

使用时可以在 Claude Code 中输入：

```text
/ai-collaboration-workflow create a requirement for <task>
```

Claude 也可能根据 skill 描述自动加载它。

### Codex

```bash
mkdir -p ~/.codex/skills
cp -R skills/ai-collaboration-workflow ~/.codex/skills/
```

使用时输入：

```text
Use $ai-collaboration-workflow to initialize this repository.
```

项目初始化后，可以继续输入：

```text
Use $ai-collaboration-workflow to choose the delivery path and create the required workflow artifacts.
```

## E2E 的定位

E2E 或真实环境验证不是所有项目、所有任务都必须强制执行。模板里的原则是：

- 能跑真实链路时，应在 review handoff 里记录命令、环境、结果和证据。
- 如果真实 E2E 成本太高或环境不可用，必须记录 blocker 和 residual risk。
- 不能把“本地单测通过”伪装成“真实链路已验证”。

具体项目怎么跑，写在 `zettelkasten/05-reference/e2e-test.md`。

## 发布和宣传流程

如果要维护本仓库在 Obsidian Forum、X 等平台的宣传内容，参考 `docs/` 下的项目维护 runbook：

```text
docs/community-publishing.md
```

这份文档记录平台规则、推荐文案、发布前检查、最终确认点，以及这次实际踩到的 X 富文本编辑器状态问题。

这份 runbook 不属于 `template/`，不会安装到用户项目中。

## Obsidian 和 Markdown 语法

这个模板兼容 Obsidian，但也尽量保留 GitHub 上的可读性。

| 场景 | 建议语法 | 说明 |
|---|---|---|
| `zettelkasten/` 内 note 互相链接 | `[[00-governance/ai-workflow]]` | Obsidian wiki link，适合知识图谱和双向链接 |
| 外部链接 | `[label](https://example.com)` | 普通 Markdown，Obsidian 和 GitHub 都能正常显示 |
| 希望 GitHub 正常显示的图片 | `![alt](assets/example.png)` | 普通 Markdown 图片语法 |
| 只在 Obsidian 内使用的嵌入 | `![[example.png]]` | Obsidian 可识别，但 GitHub 不会按图片渲染 |

简单原则：项目 note 之间用 `[[...]]`；外部链接、图片和需要 GitHub 渲染的资源用普通 Markdown。

## 适合什么项目

适合：

- 长期维护的软件项目；
- 多模块或多子项目仓库；
- 需要 AI 反复接手上下文的项目；
- 需要 review 证据链和验证记录的项目；
- 容易因为聊天记录丢失而失去工程记忆的项目。

不太适合：

- 一次性脚本；
- 很短生命周期的 demo；
- 不需要需求、设计、review 流程的个人小实验。

## 中文内容维护规则

中文内容只回答“怎么理解和使用这套模板”。不要在 `docs/zh-CN/` 里复制完整英文模板。

如果英文模板规则变化，中文说明只需要同步解释变化，不需要逐文件翻译。
