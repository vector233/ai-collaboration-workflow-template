# 02-architecture

存放系统架构相关的 note：请求流程、鉴权模型、关键组件交互、数据模型等。

## 建议初始化 note

启动新项目时，按需创建以下 note：

- `request-flow.md` — 端到端请求路径
- `auth-model.md` — 鉴权机制
- `data-model.md` — 核心数据模型
- `current-architecture-flow.md` — 当前架构总览（应作为最重要的"现状"文档，跨多个其他 note 引用）

## 规则

- 每个 note 应原子化，描述一个清晰的架构主题
- 所有外部依赖（云服务、第三方 API、消息队列等）应在 [[00-governance/decisions]] 有对应决策记录
- 架构变更后，及时回写本目录下的相关 note

## 参见

- [[00-governance/decisions]] — 架构决策 ADR
- [[CLAUDE]] — 知识库使用规则
