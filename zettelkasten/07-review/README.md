# 07-review

## 这篇文档回答什么问题

本目录用于回答：AI 或人工 reviewer 应该去哪里查待 review 的阶段性交接文档、review 反馈写在哪里、开发方如何记录判断和处理结果，以及什么时候可以继续下一轮开发。

## 目录定位

`07-review/` 是跨 AI review 的交互目录，**不是需求源头**，也不是长期架构说明。

它负责保存：

- 待 review 的阶段性交接文档
- reviewer 带证据的反馈
- 开发方对反馈是否成立的判断
- review 修改、验证、提交和关闭结果

## 目录结构

- `pending/` — 已输出交接文档，等待 reviewer 阅读和反馈
- `in-review/` — reviewer 已反馈，开发方正在判断或修改
- `done/` — 双方确认本轮 review 修改工作结束

## 使用方式

1. 阶段性工作完成后，开发方从 [[00-governance/templates/review]] 复制模板，在 `pending/` 新建 review 文档
2. reviewer 从 `pending/` 读取待 review 文档
3. reviewer 的每条关键反馈必须附带关联文档、代码位置、提交或验证证据
4. 如果 reviewer 需要测试前端功能，必须使用 Playwright（或等价 UI 测试工具），并从对应 reference note 获取本地测试账号
5. 开发方必须先独立验证反馈，**不允许默认同意 reviewer 意见**
6. 如果反馈成立或部分成立，开发方完成修改、验证和提交
7. 如果反馈不成立，开发方必须在 review 文档中贴出反证：相关代码、文档、测试输出或提交证据，并把该意见打回给 reviewer
8. review 进入处理阶段时，把文档移动到 `in-review/`
9. 双方确认本轮 review 修改工作结束后，把文档移动到 `done/`
10. `done/` 后才继续下一轮开发工作

## Subagent 协作

- 允许并行 subagents 处理互不冲突的任务
- 派发任务时必须明确目录 / 文件 ownership，避免多个 agent 修改同一组文件
- 每个阶段性实现仍必须创建或更新 `pending/` review 文档
- reviewer 更新 review 文档后，开发方可以派 subagent 监控文档变化、汇总反馈和证据；最终是否修复**仍由开发方独立验证后决定**

## 命名方式

文件名使用：

- `REVIEW-YYYYMMDDHHMM-short-name.md`

例如：

- `REVIEW-202604281530-tenant-onboarding-flow.md`

## Review 文档至少要包含什么

详见 [[00-governance/templates/review]]。最关键的几项：

- 当前任务目标和范围
- 已完成改动 / 最新提交
- 验证结果（编译 / 测试 / 手动验证 / E2E）
- 当前工作区未提交状态
- 已知风险 / 阻塞
- 后续计划
- 建议 review 重点
- reviewer 反馈记录
- 开发方判断和处理结论
- 不成立反馈的反证和打回结论
- 本轮 review 关闭条件

## 状态迁移规则

| 状态目录 | 进入条件 | 离开条件 |
|---|---|---|
| `pending/` | 阶段性工作完成，开发方输出交接文档 | 收到 reviewer 反馈 → 移到 `in-review/` |
| `in-review/` | reviewer 已反馈 | 成立问题已处理；不成立问题已带证据打回；双方确认 → 移到 `done/` |
| `done/` | 双方确认本轮 review 关闭 | 不再移动 |

> 移动状态时只移动 review 文档位置，**不修改需求文档的 `requirement_id`**。

## 判断原则

- **不因为 reviewer 提出意见就默认修改**
- 必须先核对 reviewer 提供的关联文档、代码位置、提交或验证证据
- 证据不足时，要求 reviewer 补充证据，不直接改代码
- 前端功能反馈如果没有 UI 测试证据，应要求 reviewer 补充验证或说明无法执行的原因
- 反馈不成立时，要在 review 文档中写清楚反证，并标记为 `不成立 / 已打回`
- 只有成立或部分成立的问题才进入修改、验证和提交

## 与需求文档的关系

需求文档负责描述需求本身和实现进度；review 文档负责保存阶段性 review 交互。

需求文档里的 `阶段性交接 / Review 文档` 和 `Review 反馈处理记录` 必须链接到本目录下对应 review 文档。review 文档也必须反向链接到对应需求文档。

## 参见

- [[06-requirements/README]]
- [[08-technical-designs/README]]
- [[00-governance/templates/review]]
