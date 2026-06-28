# Gotchas

Each entry answers: **what happened, root cause, fix, lesson, and prevention rule**.

AI agents should search this file before debugging or designing related changes.

Promote a gotcha into `AGENTS.md`, an architecture note, a cross-cutting note, or a runbook when the lesson is a repository-wide rule rather than a local troubleshooting record.

## General

### Example: Initialization Left Template Placeholders

**Problem**: after initializing the template, some Markdown files still contained `{{...}}` placeholders.

**Root cause**: the replacement step missed a subdirectory or tried to replace multiline Markdown tables with a single-line command.

**Fix**: run the placeholder scan in `INIT.md` and fix every remaining match before committing the initialized project.

**Lesson**: bulk text replacement needs a final grep-style gate. Do not trust a successful command exit code alone.

**Prevention rule**: after bulk placeholder replacement, run the placeholder scan and resolve every remaining match before handoff.

## Entry Template

```md
### <Short problem title>

**Problem**: <symptom, error, or failed behavior>

**Root cause**: <why it happened>

**Fix**: <code/docs/config change, commit, or file reference>

**Lesson**: <what future agents should remember>

**Prevention rule**: <must/never/prefer/check-before rule if this is likely to recur>

**See also**: [[02-architecture/current-architecture-flow]] or `<path>`
```

## See Also

- [[00-governance/decisions]] — architecture decisions
- [[00-governance/ai-workflow]] — rule promotion and memory writeback rules
