# Gotchas

Each entry answers: **what happened, root cause, fix, and lesson**.

AI agents should search this file before debugging or designing related changes.

## General

### Example: Initialization Left Template Placeholders

**Problem**: after initializing the template, some Markdown files still contained `{{...}}` placeholders.

**Root cause**: the replacement step missed a subdirectory or tried to replace multiline Markdown tables with a single-line command.

**Fix**: run the placeholder scan in `INIT.md` and fix every remaining match before committing the initialized project.

**Lesson**: bulk text replacement needs a final grep-style gate. Do not trust a successful command exit code alone.

### Recursive Bootstrap Dropped Empty Workflow Directories

**Problem**: a bootstrapped project contained workflow README files but not `backlog/`, `in-progress/`, `pending/`, `approved/`, or other state directories, so creating the first workflow document failed.

**Root cause**: bootstrap excluded maintenance state paths and copied files only. The `.gitkeep` files that preserve empty directories were excluded with them.

**Fix**: keep clean state directories inside the canonical `template/` payload and copy their `.gitkeep` files normally. Validate the first REQ, TECH, and REVIEW creation in a temporary target.

**Lesson**: validate the behavior of the distributed output, not only the source inventory.

**See also**: [[05-reference/e2e-test]], `scripts/validate_distribution.py`

### Repository Maintenance Leaked Into The Template

**Problem**: repository-specific publishing instructions and maintenance workflow documents could be installed into user projects.

**Root cause**: the repository root acted as both project workspace and downstream template payload.

**Fix**: make `template/` the only canonical payload and keep root project knowledge separate.

**Lesson**: every repository file needs an explicit ownership classification: downstream payload or maintainer evidence.

**See also**: [[00-governance/decisions]], [[02-architecture/current-architecture-flow]]

## Entry Template

```md
### <Short problem title>

**Problem**: <symptom, error, or failed behavior>

**Root cause**: <why it happened>

**Fix**: <code/docs/config change, commit, or file reference>

**Lesson**: <what future agents should remember>

**See also**: [[02-architecture/current-architecture-flow]] or `<path>`
```

## See Also

- [[00-governance/decisions]] — architecture decisions
- [[00-governance/ai-workflow]] — memory writeback rules
