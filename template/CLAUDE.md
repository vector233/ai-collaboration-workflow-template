@AGENTS.md

# Claude Code Adapter

`AGENTS.md` is imported above as the canonical cross-agent instruction file. Keep Claude-specific additions minimal and do not duplicate shared workflow rules here.

## Model-Routing Adapter

`.claude/settings.json` selects `opusplan` for new Claude Code sessions: Opus in plan mode and Sonnet during execution. `.claude/agents/` defines the shared specialist roles with fixed model and tool policies:

- `explorer`: Haiku, read-only discovery and evidence gathering.
- `implementer`: Sonnet, one understood scoped change and targeted validation.
- `reviewer`: Opus, read-only correctness and regression review.
- `architect`: Opus, read-only high-impact design and root-cause analysis.

Follow the Specialist Delegation and Git Isolation rules in `AGENTS.md`. These files are optional Claude Code adapters: model availability or local policy may require changing their settings, but no route, checkpoint, validation, or durable project state depends on them.
