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

1. 从这个 GitHub template 创建新仓库，或把 `AGENTS.md` 和 `zettelkasten/` 复制到已有项目。
2. 让 AI 执行：

   ```text
   Initialize this knowledge base by following INIT.md.
   ```

3. 回答项目名称、技术栈、仓库类型、常用命令、域名端口等问题。
4. AI 会替换占位符、初始化第一批 note、删除 `INIT.md` 并提交。
5. 后续每个非极小任务按 `REQ -> TECH -> implementation -> validation -> REVIEW -> writeback` 推进。

## E2E 的定位

E2E 或真实环境验证不是所有项目、所有任务都必须强制执行。模板里的原则是：

- 能跑真实链路时，应在 review handoff 里记录命令、环境、结果和证据。
- 如果真实 E2E 成本太高或环境不可用，必须记录 blocker 和 residual risk。
- 不能把“本地单测通过”伪装成“真实链路已验证”。

具体项目怎么跑，写在 `zettelkasten/05-reference/e2e-test.md`。

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
