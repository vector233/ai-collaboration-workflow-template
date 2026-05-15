---
title: 技术方案与架构决策
status: active
project: {{PROJECT_NAME}}
last_verified_at: YYYY-MM-DD
source_of_truth: mixed
related:
  - "[[06-requirements/README]]"
  - "[[02-architecture/current-architecture-flow]]"
  - "[[00-governance/templates/technical-design]]"
  - "[[07-review/README]]"
---

# 08-technical-designs

## 这篇文档回答什么问题

本目录用于回答：需求确认后、代码开发前，如何把产品需求转换成技术架构流程、关键决策和开发边界。

## 目录定位

- `06-requirements/` 负责"为什么做、做什么、如何验收"
- `08-technical-designs/` 负责"系统怎么流转、哪些架构决策已确认、哪些风险和边界会影响实现"
- `02-architecture/` 负责沉淀当前项目整体架构现状

每个 technical design 完成实施后，必须把仍然成立的架构结论回写到 [[02-architecture/current-architecture-flow]] 或更细的架构文档。

## 目录结构

- `pending/` — 已提出但尚未确认的技术方案，**不应直接进入业务代码开发**
- `approved/` — 已确认，可作为开发输入的技术方案
- `implemented/` — 已实施、review 关闭，并已回写架构现状的技术方案

## 使用方式

1. 需求进入 `in-progress/` 后，先检查是否已有对应技术方案
2. 如果没有，从 [[00-governance/templates/technical-design]] 新建 `TD-YYYYMMDDHHMM-short-name.md` 到 `pending/`
3. 技术方案只写架构流程、关键决策、影响边界、风险和验证口径，**不展开到逐行实现**
4. 产品/技术关键问题确认后，将技术方案移动到 `approved/`
5. 代码开发必须以 approved 技术方案为输入；发现方案假设不成立时，**先回改方案再继续**。需求处于 `in-progress` 但技术方案仍为 `pending` 时，只能继续分析、方案修订和 review 处理
6. 阶段性代码完成后，review 文档必须链接相关技术方案
7. 需求完成、review 关闭、架构文档回写后，将技术方案移动到 `implemented/`

## 命名方式

新技术方案文件使用：

- `TD-YYYYMMDDHHMM-short-name.md`

## 技术方案至少要包含什么

详见 [[00-governance/templates/technical-design]]。最关键的几项：

- 关联需求
- 当前架构事实
- 目标技术流程
- 架构决策
- 影响边界
- 不做什么
- 待决策问题
- 验证口径
- 架构回写清单

## 当前方案看板

<!-- 在此维护当前所有技术方案的总览表格。示例：

| 状态 | 技术方案 | 对应需求 | 下一步 |
|---|---|---|---|
| approved | [[08-technical-designs/approved/TD-YYYYMMDDHHMM-example]] | [[06-requirements/in-progress/REQ-YYYYMMDDHHMM-example]] | 一句话下一步 |

随着技术方案新增/迁移状态，及时更新本表格。 -->

## 状态迁移规则

| 状态目录 | 进入条件 | 离开条件 |
|---|---|---|
| `pending/` | 已提出技术方案，未确认 | 关键问题确认后 → 移到 `approved/` |
| `approved/` | 可作为开发输入 | 需求完成、review 关闭、架构回写完成 → 移到 `implemented/` |
| `implemented/` | 已实施并回写架构 | 不再移动 |

> 移动状态时只移动文件位置，**不修改 `technical_design_id`**。

## 与 Review 的关系

- 技术方案**不是** review 文档
- 技术方案进入 `approved/` 前，可以被产品/架构 review
- 代码阶段性交接文档必须链接本轮使用的技术方案
- reviewer 对技术方案提出问题时，仍必须附带代码、文档、提交或外部来源证据

## 参见

- [[06-requirements/README]] — 需求工作流
- [[07-review/README]] — Review 工作流
- [[00-governance/templates/technical-design]] — 技术方案模板
