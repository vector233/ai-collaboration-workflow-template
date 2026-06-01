# Architectural Decisions — 关键架构决策

每条决策记录（ADR）回答：**做了什么决定 / 为什么 / 影响**。新增决策时往本文件追加新条目，**不要删除历史决策**（即使已被推翻，也应该新增"AD-NNN: 推翻 AD-MMM"而非删除原条目）。

---

## AD-001: 使用 Zettelkasten 双向链接组织知识

**决策**：项目知识库采用 Zettelkasten 方法，note 之间用双向 wiki-link 互相引用，而不是树状目录文档库。

**原因**：
- AI agent 接任务时需要快速跳转到相关上下文；wiki-link 比目录路径更直接
- 知识有交叉性（一个架构决策可能同时影响多个组件），树状结构无法表达这种关系
- 添加新 note 强制引用旧 note，避免悬空内容

**影响**：
- 所有 note 必须原子化（一个 note 一个想法）
- 新增 note 必须显式链接到至少一个已有 note
- 详细规则见 [[CLAUDE]] §核心原则

---

<!-- 示例 ADR 模板（保留以供参考；项目实际 ADR 从 AD-002 开始追加）

## AD-NNN: <一句话描述决策>

**决策**：<具体做了什么决定>

**原因**：
- <理由 1>
- <理由 2>

**影响**：
- <对架构/工程/团队的具体影响>

**参见**：[[02-architecture/...]]、[[00-governance/gotchas]]

---

-->

## AD-002: 非极小实现必须经过 Requirement 和 TECH Gate

**决策**：除 tiny-fix waiver 外，业务代码实现前必须先有需求文档，并且对应 TECH 已进入 `approved/`。

**原因**：

- AI agent 容易从局部代码直接推断全局设计，导致范围漂移。
- Requirement 固定"为什么做、做什么、怎么验收"。
- TECH 固定"系统如何流转、边界在哪里、风险怎么验证"。

**影响**：

- `in-progress` 只代表需求活跃，不代表允许写代码。
- TECH 仍在 `pending/` 时，只能做澄清、设计、验证准备或 review。
- 如果实现发现 TECH 假设不成立，先回改 TECH，再继续实现。

**参见**：[[00-governance/agent-harness]]、[[06-requirements/README]]、[[08-technical-designs/README]]

---

## AD-003: Review 反馈必须证据化

**决策**：AI 或人工 reviewer 的关键意见必须附带证据，开发方必须独立验证后再修复或打回。

**原因**：

- AI reviewer 可能语气确定但事实错误。
- 没有证据的 review 会把猜测转化成代码 churn。
- 反证记录能保护未来 agent 不重复处理已否定的问题。

**影响**：

- review 文档保存反馈、证据、判断、处理状态和关闭条件。
- 成立或部分成立的问题修复后必须补验证记录。
- 不成立的问题必须写 counter-evidence 并标记打回。

**参见**：[[07-review/README]]、[[00-governance/agent-harness]]

## 参见

- [[00-governance/project-overview]] — 项目总览
- [[00-governance/gotchas]] — 历史踩坑（决策的实证依据）
