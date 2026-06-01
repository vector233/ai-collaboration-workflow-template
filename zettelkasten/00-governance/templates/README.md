# Templates

Use these templates for the three core workflows. Copy a template instead of writing a new document from scratch.

| Template | Purpose | Naming rule | Target directory |
|---|---|---|---|
| `requirement.md` | Requirement entry | `REQ-YYYYMMDDHHMMSS-<slug>.md` | `06-requirements/{backlog,in-progress,done}/` |
| `technical-design.md` | Technical design | `TECH-YYYYMMDDHHMMSS-<slug>.md` | `08-technical-designs/{pending,approved,implemented}/` |
| `review.md` | Review handoff | `REVIEW-YYYYMMDDHHMMSS-<slug>.md` | `07-review/{pending,in-review,done}/` |

## Usage

```bash
cp zettelkasten/00-governance/templates/requirement.md \
   zettelkasten/06-requirements/backlog/REQ-$(date +%Y%m%d%H%M%S)-<slug>.md
```

Then update frontmatter, document ID, status, links, and body.

## Rules

- Wiki links should point to existing notes. If a referenced note does not exist, create the smallest useful placeholder note first.
- When a document changes state, move it to the matching state directory.
- Follow the state transition rules in each workflow README.
- Business-code implementation requires an approved technical design unless a tiny-fix waiver is recorded in the requirement or review document.

## See Also

- [[06-requirements/README]] — requirement workflow
- [[07-review/README]] — review workflow
- [[08-technical-designs/README]] — technical design workflow
