# AI 协作流程模板

这是面向 AI coding agents 的项目知识层模板，不是自主执行 runtime。它把项目规则、当前工作、验证证据、可复用流程和交接状态保存在仓库中，让新的 Agent 不依赖聊天记录也能继续工作。

这个版本只面向新项目初始化，不兼容也不迁移旧的移动状态目录架构。

`template/` 是唯一 canonical 下游模板；中文文档只解释设计和使用方式，不复制一套中文模板。

## 新的轻量模型

任务先经过 Workflow Router：

| 路径 | 使用场景 | 最小工件 |
|---|---|---|
| Direct | 本地、可逆、低风险、一个上下文 | 无流程文档，验证后提交 |
| Tracked | 行为改动、调试连续性、多上下文 | 一个稳定 `WORK-*` |
| Governed | 高风险、重要不确定性、独立审批、迁移、发布、多人协调 | `WORK-*` 加按需 TECH、PLAN、REVIEW |

Router 不只看代码量，还判断影响范围、不确定性、风险与可逆性、持续时间、协作方式和验证要求。小型权限或数据修改也可能直接升级为 Governed。

## 为什么更轻

- 所有工作流工件固定保存在 `zettelkasten/06-work/`，状态只更新 frontmatter，不移动文件。
- 普通任务在一个 WORK 中记录目标、方案、切片、验证、Review、上下文 checkpoint 和经验候选。
- TECH、PLAN、REVIEW 只有在存在独立生命周期时才创建。
- 不再手工维护 `CURRENT.md`，使用 `python3 scripts/workflow_doctor.py --status` 查找当前工作。
- 项目级重复流程存入 `project-skills/`，根据索引触发后再加载，不塞进始终读取的 `AGENTS.md`。

## 经验固化

每个 WORK 都记录 Experience Candidates。关闭任务前根据经验形态选择最小目标：

| 经验 | 固化位置 |
|---|---|
| 所有 Agent 必须遵守的规则 | `AGENTS.md` |
| Bug 根因、错误假设 | `gotchas.md` |
| 架构事实和不变量 | architecture / cross-cutting note |
| 简单环境或验证步骤 | quick reference / runbook |
| 有触发条件、验证和恢复步骤的稳定流程 | `project-skills/<name>/SKILL.md` 和 `project-skills/INDEX.md` |

项目 Skill 必须说明何时使用、何时不用、执行步骤、验证、恢复和来源。单次事故、低置信猜测和普通编码常识不升级成 Skill。

## 并行开发和提交

Tracked 和 Governed 工作默认使用 task branch；同时进行的任务或 Agent 使用独立 Git worktree：

```bash
python3 scripts/task_worktree.py create <WORK-ID> --slug <short-name>
```

默认分支只用于集成。存在依赖或明显修改相同路径的任务不应直接并行。

每个产生持久化修改的 Agent 上下文或完整实现切片必须形成一个只包含当前任务变更的提交。纯分析和只读 Review 不创建空提交。未完成状态可以在 task branch 使用 `checkpoint:` 或 `wip:`，但破损 checkpoint 不能合入默认分支。

共享的 `AGENTS.md`、runbook 和项目 Skill 通常在任务关闭时统一升级，避免多个 worktree 同时修改热点文件。

## 主要结构

```text
AGENTS.md                      仓库级规则
zettelkasten/AI.md             最小上下文入口
zettelkasten/06-work/          路径稳定的 WORK/TECH/PLAN/REVIEW
project-skills/INDEX.md        项目 Skill 触发索引
scripts/workflow_doctor.py     状态和一致性检查
scripts/workflow_task.py       WORK 创建、范围更新、checkpoint 和关闭
scripts/task_worktree.py       安全创建并行任务 worktree
```

知识分类如 overview、architecture、gotchas 和 runbook 仍然保留，因为它们有不同检索用途；本次主要合并的是容易产生状态重复和路径联动的执行工件。

## 初始化

安装 companion Skill 后执行：

```text
Use $ai-collaboration-workflow to initialize this repository.
```

也可以复制 `template/` 后让 Agent 按 `INIT.md` 初始化。初始化会发现仓库事实、合并已有 Agent 规则、配置 Git 默认策略、清理占位符并运行严格验证。

日常恢复从以下内容开始：

```text
AGENTS.md
zettelkasten/AI.md
python3 scripts/workflow_doctor.py --status
当前分支对应的 WORK 文件
```

只读取 WORK 链接的知识和匹配的项目 Skill，不默认扫描整个知识库。

## Companion Skill

`skills/ai-collaboration-workflow/` 负责模板安装、流程路由、WORK 更新、最小上下文加载、经验升级、Git 隔离和状态验证。详细判断拆分在 `references/` 中，触发后按需加载。

核心知识层不依赖某一家 AI。`AGENTS.md` 是共享入口，`CLAUDE.md` 等文件只做适配；即使不安装 companion Skill，初始化后的仓库仍可以独立使用。

## 验证

下游项目运行：

```bash
python3 scripts/workflow_doctor.py --strict
```

本模板仓库运行：

```bash
python3 scripts/validate_distribution.py
```

检查范围包括稳定工件、状态字段、分支隔离、wiki 链接、占位符、经验升级完成度、项目 Skill 结构、bootstrap 和临时 worktree 行为。

并行协调或工具集成使用 `python3 scripts/workflow_doctor.py --status --all-worktrees --json`，它会聚合已注册 worktree、脏状态、最后提交和 owned paths 重叠提示，并单独披露 detached worktree，避免重复认领活跃 WORK。任务范围变化时，在 `workflow_task.py checkpoint` 中重复传入 `--owned-path` 以替换原范围。
