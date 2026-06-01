# Gotchas

Each entry answers: **what happened, root cause, fix, and lesson**.

AI agents should search this file before debugging or designing related changes.

## General

### Example: Initialization Left Template Placeholders

**Problem**: after initializing the template, some Markdown files still contained `{{...}}` placeholders.

**Root cause**: the replacement step missed a subdirectory or tried to replace multiline Markdown tables with a single-line command.

**Fix**: run the placeholder scan in `INIT.md` and fix every remaining match before committing the initialized project.

**Lesson**: bulk text replacement needs a final grep-style gate. Do not trust a successful command exit code alone.

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
