# Templates

Copy the work item when [[workflow]] selects Tracked or Governed. Keep it in `zettelkasten/work/` for its full lifecycle and update frontmatter in place. Use an Initiative only when a requirement contains multiple independently deliverable WORK records and no external Epic, Issue, or Milestone already owns coordination.

| Template | Use | Output |
|---|---|---|
| `initiative.md` | optional local coordination for a large multi-deliverable requirement | `work/INITIATIVE-<timestamp>-<slug>.md` |
| `work-item.md` | default tracked or governed task record | `work/WORK-<timestamp>-<slug>.md` |
| `project-skill.md` | promoted repeatable repository procedure | `project-skills/<skill-name>/SKILL.md` |
| `workflow-observations.md` | created only after evidence-backed template friction | `workflow-observations.md` |

Create a WORK:

```bash
cp zettelkasten/templates/work-item.md \
  zettelkasten/work/WORK-$(date +%Y%m%d%H%M%S)-<slug>.md
```

Update identifiers, status, branch, worktree, next action, links, and body. Governed tasks record their gates in the same file.

For a local Initiative, copy `initiative.md`, give it a stable `INITIATIVE-*` ID, and set that ID in each child WORK's `initiative_id`. Do not add another hierarchy level or duplicate child status in the Initiative. When an external tracker owns the parent lifecycle, skip the local Initiative and set `external_parent` in each child WORK instead.
