# 06-requirements

## 这篇文档回答什么问题

本目录用于回答：后续每一轮迭代需求应该放在哪里、怎么写、什么时候移动状态，以及如何把需求和现有上下文文档关联起来。

## 目录定位

`06-requirements/` **不是现状说明**，而是后续迭代开发的入口。

它的核心作用是：

- 让每个需求都有明确的背景、目标、影响范围和验收标准
- 让每个需求在开始实现前，就能挂接最小必要上下文
- 避免为了做一个需求，再重新从头梳理整个项目

## 目录结构

- `backlog/` — 已识别但尚未进入实施的需求
- `in-progress/` — 正在分析、设计、开发或联调的需求
- `done/` — 已完成并已回写现状文档的需求

## 当前需求看板

<!-- 在此维护当前所有需求的总览表格，按 P0/P1/P2 分级排序。示例：

| 优先级 | 状态 | 需求 | 下一步 |
|---|---|---|---|
| P0 | in-progress | [[06-requirements/in-progress/REQ-YYYYMMDDHHMMSS-example]] | 一句话下一步 |

随着需求新增/完成，及时更新本表格。 -->

## 使用方式

需求推进默认遵循 [[00-governance/agent-harness]]：先收敛最小上下文包，再确认需求、TECH、验证和 review gate。

推荐每个需求按下面的流程推进：

1. 从 [[00-governance/templates/requirement]] 复制一份新需求文档
2. 初始放到 `backlog/`
3. 在需求文档里补"最小上下文包"，优先链接现有现状文档
4. 如果现有文档不够支撑实现，再补最小必要新文档
5. 需求确认后，把需求移动到 `in-progress/`；`in-progress` 可以表示分析/设计/联调中，**不自动代表已经允许写代码**
6. 代码开发前必须创建或确认 [[08-technical-designs/README]] 下对应技术方案，状态至少进入 `approved/`
7. 技术方案要把需求转换为架构流程、数据/API/job/config 边界、关键决策、风险和验证口径
8. 技术方案确认后才开始代码开发；如果开发中发现架构假设不成立，先回改技术方案再继续
9. 阶段性工作完成后，在 [[07-review/README]] 的 `pending/` 下输出 review 交接文档，供另一个 AI 或人工 reviewer 做阶段性 review
10. reviewer 的反馈必须附带关联文档或证据，开发方**先独立验证**，不允许默认同意 reviewer 意见
11. 成立或部分成立的问题完成修改、验证和提交；不成立的问题必须贴出反证并打回 reviewer
12. 等待双方确认本轮 review 修改工作结束
13. 开发完成并回写对应现状文档后，再移动到 `done/`

## 推荐命名方式

文件名使用：

- `REQ-YYYYMMDDHHMMSS-short-name.md`

例如：

- `REQ-20260428153045-clinic-device-sync.md`

好处：

- 时间顺序清晰，同一天多个文档不会互相混淆
- 主题可读
- 在不同目录之间移动时不需要改内部编号

## 状态迁移规则

| 状态目录 | 进入条件 | 离开条件 |
|---|---|---|
| `backlog/` | 需求已识别但本轮不做 | 决定本轮要做 → 移到 `in-progress/` |
| `in-progress/` | 已确认本轮要做，开始分析/设计/联调 | 代码、验证、文档回写都完成 → 移到 `done/` |
| `done/` | 完成并 review 关闭 | 不再移动 |

> 移动状态时只移动文件位置，**不修改 `requirement_id`**。

## 每个需求至少要写什么

每个需求文档至少应包含（详见模板）：

- 背景
- 目标
- 不做什么
- 最小上下文包
- 当前已确认事实
- 待确认问题
- 影响范围
- 验收标准
- 阶段性交接 / Review 文档
- Review 反馈处理记录
- 文档回写清单

其中最关键的是：

- **最小上下文包** — 直接告诉后续实现时最先该读哪些文档和代码入口
- **当前已确认事实** — 防止把猜测带进实现
- **文档回写清单** — 防止需求做完后现状文档失效
- **阶段性交接 / Review 文档** — 防止阶段性 review 时 reviewer 需要重新摸索当前范围、最新提交、验证结果和剩余风险
- **Review 反馈处理记录** — 要求 reviewer 的意见绑定关联文档或证据；待 review 文档和 review 结果统一到 [[07-review/README]] 查询

## 技术方案门槛

需求文档解决"为什么做、做什么、如何验收"；技术方案文档解决"系统如何流转、架构边界在哪里、关键技术决策是什么"。

每个进入开发的需求必须满足：

- 关联一个 `TECH-YYYYMMDDHHMMSS-short-name.md`
- 技术方案已从 `pending/` 移到 `approved/`，或者在 review 文档中明确说明为什么本次是极小修复可免除
- 技术方案已链接相关 `02-architecture/`、`04-cross-cutting/`、`05-reference/` 文档
- 如果改变现有架构流程，已更新或计划更新 [[02-architecture/current-architecture-flow]]

需求停留在 `in-progress/` 但技术方案仍为 `pending/` 时，只允许继续需求澄清、技术方案修订和 review 处理；**不能开始业务代码实现**。

## 关联原则

一个好的需求文档，至少要能反向链接到这三类上下文：

- **全局总览** — 系统全貌和跨项目关系（[[00-governance/project-overview]]）
- **项目现状** — 各子项目的代码入口和专属文档
- **跨模块流程** — 如果需求跨系统，链接 `02-architecture/` 或 `04-cross-cutting/` 里的对应主链路文档

## 当前模板

- [[00-governance/templates/requirement]] — 标准需求模板
- [[00-governance/templates/technical-design]] — 标准技术方案模板
- [[00-governance/templates/review]] — 标准 review 模板

## 参见

- [[00-governance/agent-harness]] — AI agent 工作流、gate、验证、review 和记忆回写
- [[07-review/README]] — Review 工作流
- [[08-technical-designs/README]] — 技术方案工作流
- [[CLAUDE]] — 知识库使用规则
