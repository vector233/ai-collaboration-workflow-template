# AI 协作流程模板：中文说明

> 这里是中文说明层，不是模板源文件的中文副本。模板的 canonical 版本仍然是英文，位于仓库根目录和 `zettelkasten/` 下。

## 这个项目是什么

`AI Collaboration Workflow Template` 是一套给 AI coding agents 使用的项目文档模板。它的目标不是写更多文档，而是让 AI 在长期项目中能稳定回答这些问题：

- 当前任务最少需要读哪些上下文？
- 这次改动的需求、非目标和验收标准是什么？
- 开发前技术方案是否已经足够明确？
- 完成后用什么验证结果证明它真的可用？
- review 反馈是否有证据，如何处理？
- 本轮学到的架构事实、测试流程或踩坑应该写回哪里？

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
| `zettelkasten/00-governance/ai-workflow.md` | AI 协作流程：上下文、需求、设计、验证、review、回写 |
| `zettelkasten/06-requirements/` | 需求状态机：`backlog -> in-progress -> done` |
| `zettelkasten/08-technical-designs/` | 技术方案状态机：`pending -> approved -> implemented` |
| `zettelkasten/07-review/` | review 交接状态机：`pending -> in-review -> done` |
| `zettelkasten/05-reference/e2e-test.md` | 项目具体 E2E / smoke / 验证命令 |
| `zettelkasten/00-governance/gotchas.md` | 历史踩坑、根因和教训 |

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
5. 后续每个非极小任务按 `REQ -> TECH -> implementation -> validation -> REVIEW -> writeback` 推进。

仓库根目录还包含本项目自身的需求、技术设计、review 和发布资料，不是下游模板内容。请使用 Skill 或复制 `template/` 的内容；不要把整个仓库根目录当作干净模板。

## Skill 安装

仓库内提供一个可选 skill：

```text
skills/ai-collaboration-workflow/
```

它用于帮助 AI 正确使用这套模板：安全引导或执行模板安装、初始化项目、创建 REQ/TECH/REVIEW、检查开发准入、记录验证结果、处理带证据的 review 反馈，以及回写 gotchas / architecture / runbook。

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
Use $ai-collaboration-workflow to create a requirement, technical design, or review handoff.
```

## E2E 的定位

E2E 或真实环境验证不是所有项目、所有任务都必须强制执行。模板里的原则是：

- 能跑真实链路时，应在 review handoff 里记录命令、环境、结果和证据。
- 如果真实 E2E 成本太高或环境不可用，必须记录 blocker 和 residual risk。
- 不能把“本地单测通过”伪装成“真实链路已验证”。

具体项目怎么跑，写在 `zettelkasten/05-reference/e2e-test.md`。

## 发布和宣传流程

如果要维护本仓库在 Obsidian Forum、X 等平台的宣传内容，参考根知识库中的项目维护 runbook：

```text
zettelkasten/05-reference/community-publishing.md
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
