# Templates

存放三类工作流的标准模板。新增需求 / 技术方案 / review 文档时**必须**从这里 copy，不要从零写。

| 模板 | 用途 | 命名规则 | 目标位置 |
|---|---|---|---|
| `requirement.md` | 需求条目 | `REQ-YYYYMMDDHHMM-<slug>.md` | `06-requirements/{backlog,in-progress,done}/` |
| `technical-design.md` | 技术方案 | `TD-YYYYMMDDHHMM-<slug>.md` | `08-technical-designs/{pending,approved,implemented}/` |
| `review.md` | 阶段性 review | `REVIEW-YYYYMMDDHHMM-<slug>.md` | `07-review/{pending,in-review,done}/` |

## 使用

```bash
cp zettelkasten/00-governance/templates/requirement.md \
   zettelkasten/06-requirements/backlog/REQ-$(date +%Y%m%d%H%M)-<slug>.md
```

填写 frontmatter（修正 `requirement_id` / `last_verified_at` / `affected_projects`）和正文。

## 规则

- 所有 wiki-link 必须指向已存在的 note；若需要引用尚未存在的 note，先在 `02-architecture/` 等位置把目标 note 创建出来
- 状态变更（如 `backlog` → `in-progress`）的同时**必须**把文件从一个状态目录移动到对应目标目录
- 三类模板的状态迁移规则见各工作流目录的 README

## 参见

- [[06-requirements/README]] — 需求状态迁移
- [[07-review/README]] — Review 状态迁移
- [[08-technical-designs/README]] — 技术方案状态迁移
