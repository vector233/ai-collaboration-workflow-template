# 05-reference

存放对外部权威文档的**摘要 / 速查索引**，而不是文档本身。

## 用途

- 给项目根目录下的长文档（如 `PROJECT_PRD.md`、`ARCHITECTURE.md`、`task.md`）做精简摘要，避免每次都全文 grep
- 把第三方文档的关键章节抽到这里
- 维护任务进度索引

## 规则

- 这里的 note **不是原创内容**，而是其他文档的精简映射
- 当原文档大改时，同步更新这里
- 用 wiki-link 指回原文档：`原文：[[../../PROJECT_PRD]]` 或外部 URL

## 建议 note

- `prd.md` — 产品 PRD 摘要
- `architecture.md` — 完整架构文档摘要
- `e2e-test.md` — 联调流程速查
- `competitor-api-landscape.md` — 竞品 / 市场参考资料

## 参见

- [[CLAUDE]] — 知识库使用规则
