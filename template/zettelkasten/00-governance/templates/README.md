# Templates

Copy the artifact triggered by [[00-governance/ai-workflow]]. Keep every workflow file in `zettelkasten/06-work/` for its full lifecycle and update frontmatter in place.

| Template | Use | Output |
|---|---|---|
| `work-item.md` | default tracked or governed task record | `06-work/WORK-<timestamp>-<slug>.md` |
| `technical-design.md` | independent architecture or risk decision | `06-work/TECH-<timestamp>-<slug>.md` |
| `implementation-plan.md` | independent sequencing or ownership coordination | `06-work/PLAN-<timestamp>-<slug>.md` |
| `review.md` | independent review or approval lifecycle | `06-work/REVIEW-<timestamp>-<slug>.md` |
| `project-skill.md` | promoted repeatable repository procedure | `project-skills/<skill-name>/SKILL.md` |

Create a WORK:

```bash
cp zettelkasten/00-governance/templates/work-item.md \
  zettelkasten/06-work/WORK-$(date +%Y%m%d%H%M%S)-<slug>.md
```

Update identifiers, status, branch, worktree, next action, links, and body. Do not create empty optional artifacts in advance.
