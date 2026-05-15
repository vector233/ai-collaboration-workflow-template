<!-- UMBRELLA-ONLY: keep this directory only if {{REPO_TYPE}} == umbrella -->

# 04-cross-cutting

**仅伞形项目使用**。存放跨多个子项目的横切关注点：多品牌路由、统一鉴权、跨服务的数据一致性策略、共享安全模型等。

如果你的项目是单仓库（single-repo），INIT.md 会在初始化时**删除整个 `04-cross-cutting/` 目录**。

## 典型 note 示例

- `multi-brand-routing.md` — 多品牌 / 多租户的路由设计
- `shared-auth.md` — 跨子项目的统一鉴权
- `zero-persistence.md` — 跨链路的数据隐私模型

## 参见

- [[CLAUDE]] — 知识库使用规则

<!-- /UMBRELLA-ONLY -->
