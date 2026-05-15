# Quick Reference — 高频速查

> 本 note 是最高频查阅的入口。所有 AI agent 在执行命令、查找域名 / 端口 / 凭证 / 接口前，先在这里查。

---

## 常用命令

<!-- 列出各子项目的常用开发命令。示例结构（替换为项目实际命令）：

### Backend

```bash
make build
make run
make test
```

### Frontend

```bash
npm run dev
npm run build
npm run lint
```
-->

---

## 域名

{{DOMAINS}}

<!-- 示例 Markdown 表格格式（INIT.md 会用真实表格替换上面的占位符）：

| 环境 | 域名 |
|---|---|
| Production | example.com |
| Staging    | staging.example.com |
| Local API  | localhost:8080 |
-->

---

## API 端点

<!-- 列出对外暴露的关键 HTTP 端点。示例：

| 端点 | 描述 |
|---|---|
| `GET /health`          | 健康检查（无认证） |
| `POST /api/v1/auth/login` | 登录 |
| `GET /api/v1/users/me` | 当前用户信息 |
-->

---

## 数据库表

<!-- 列出关键表 + 一句话说明，方便排查问题时定位。 -->

---

## 缓存 / 队列 Key 命名

<!-- 例如 Redis key pattern：

| Pattern | 用途 |
|---|---|
| `user:{id}` | 用户缓存 |
| `ratelimit:{ip}:{bucket}` | 限流 |
-->

---

## 环境变量 / 配置

<!-- 列出关键配置文件路径和必须设置的环境变量。 -->

---

## 测试凭证

<!-- 列出本地开发用的测试账号。**警告：永远不要在此提交生产凭证**。 -->

---

## Git 仓库

{{REPOS}}

<!-- 示例：

- example-owner/foo-backend
- example-owner/foo-portal
-->

---

## 参见

- [[01-overview/product-vision]] — 产品定位、市场分析
- [[02-architecture/request-flow]] — 请求流程
- [[00-governance/glossary]] — 术语表
