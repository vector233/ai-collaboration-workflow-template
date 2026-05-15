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
- **多租户隔离**：所有 SQL 必须按 tenant_id 过滤
- **审计可追溯**：所有写操作必须有审计日志
-->

---

## 参见

- [[01-overview/product-vision]] — 核心问题、目标市场
- [[02-architecture/request-flow]] — 端到端请求流程
- [[00-governance/glossary]] — 术语表
- [[00-governance/decisions]] — 关键架构决策
