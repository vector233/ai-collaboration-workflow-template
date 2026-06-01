# Project Overview — {{PROJECT_NAME}}

## 产品定位

**{{PROJECT_NAME}} 是 {{PROJECT_DESCRIPTION}}。**

<!-- 进一步描述项目要解决的核心问题、目标用户、核心价值，建议 2-4 句话 -->

---

## 命名规则

<!-- 如果项目有品牌迁移历史或多个对外名称，在此明确：
- 对外用户可见的统一品牌名
- 文件名 / 域名 / 机器可读 slug 使用哪种格式
- 历史品牌名允许保留在哪些范围
没有迁移历史可以删除本节。
-->

---

## 技术栈

{{TECH_STACK}}

<!-- 更详细的技术栈表格示例（删除示例行，填实际项目）：

| 组件 | 技术 |
|---|---|
| **Backend** | Go · Gin · GORM · MySQL · Redis |
| **Frontend** | Next.js 15 · React 19 · TypeScript · Tailwind CSS |
| **Auth** | Ed25519 JWT · SHA-256 API Key |
-->

---

<!-- UMBRELLA-ONLY: keep this section only if {{REPO_TYPE}} == umbrella -->

## 子项目

{{SUB_PROJECTS}}

<!-- /UMBRELLA-ONLY -->

---

## 核心约束

<!-- 项目级别的关键约束（架构红线、合规要求等）。示例：

- **零持久化**：服务端不持久化用户业务数据
- **工作区隔离**：所有数据访问必须按 workspace_id 或等价边界过滤
- **审计可追溯**：所有写操作必须有审计日志
-->

---

## AI 协作约束

- 非极小任务先经过 [[06-requirements/README]] 和 [[08-technical-designs/README]] 的 gate，再进入实现。
- 阶段性实现必须通过 [[07-review/README]] 交接，review 反馈按证据处理。
- 发现新的架构事实、验证流程或踩坑时，回写到对应 note，而不是只留在聊天记录里。
- 多 agent 并行时，按 [[00-governance/harness-engineer-roles]] 声明 owned paths 和 handoff。

---

## 参见

- [[00-governance/agent-harness]] — AI agent 工作流和 gate
- [[01-overview/product-vision]] — 核心问题、目标市场
- [[02-architecture/current-architecture-flow]] — 当前架构流程
- [[00-governance/glossary]] — 术语表
- [[00-governance/decisions]] — 关键架构决策
