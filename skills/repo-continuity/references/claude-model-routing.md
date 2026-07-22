# Optional Claude Code Model Routing

Use this reference only when the target repository contains `.claude/agents/` and Claude Code is the active client. It describes a vendor adapter; the repository's Markdown and Git workflow remains authoritative and client-neutral.

## Root And Roles

The adapter does not set Claude Code's root-session model. The root keeps the model selected by the user or current client configuration, while custom specialists keep recurring side work out of the main context:

| Role | Route to it for | Default adapter policy |
|---|---|---|
| `explorer` | narrow read-only discovery, tracing, and evidence gathering | Haiku; `Read`, `Grep`, and `Glob` only |
| `implementer` | one understood, scoped change and targeted validation | Sonnet; write-capable tools |
| `reviewer` | correctness, security, regression, or missing-test review | Opus; read-only tools plus Bash |
| `architect` | ambiguous high-impact design or difficult unresolved root cause | Opus; read-only discovery tools |

Claude uses an agent description and current context to decide when to delegate. Use `@explorer`, `@implementer`, `@reviewer`, or `@architect` when an exact role must run instead of relying on automatic selection. The custom `explorer` is intentionally separate from Claude Code's built-in `Explore` agent so it remains valid under the current lowercase custom-agent naming convention.

## Delegation Rules

1. Use the cheapest capable role and do not delegate routine Direct work merely to use an agent.
2. Delegate only independent, bounded work. Keep delegation one level deep and end the agent after it reports a concise result.
3. Explorers, reviewers, and architects are read-only. They can run in parallel only when their scopes do not overlap materially.
4. An implementer is write-capable. Keep it serial with every other write-capable agent in its task worktree; use a separate task worktree for any concurrent write task.
5. Preserve findings, decisions, validation, risks, and next actions in the active WORK whenever the selected route requires a checkpoint. A subagent result is not durable state by itself.

## Recovery

If the selected Claude model is unavailable or restricted by organization policy, Claude Code falls back to an inherited or permitted model. Continue with the same role boundaries and repository workflow. If custom agents are unavailable, continue with the root agent; do not create a substitute runtime, hidden state file, or required orchestration service.
