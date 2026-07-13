# Templates

Copy the work item when [[workflow]] selects Tracked or Governed. Keep it in `zettelkasten/work/` for its full lifecycle and update frontmatter in place.

| Template | Use | Output |
|---|---|---|
| `work-item.md` | default tracked or governed task record | `work/WORK-<timestamp>-<slug>.md` |
| `project-skill.md` | promoted repeatable repository procedure | `project-skills/<skill-name>/SKILL.md` |
| `workflow-observations.md` | created only after evidence-backed template friction | `workflow-observations.md` |

Create a WORK:

```bash
cp zettelkasten/templates/work-item.md \
  zettelkasten/work/WORK-$(date +%Y%m%d%H%M%S)-<slug>.md
```

Update identifiers, status, branch, worktree, next action, links, and body. Governed tasks record their gates in the same file.
