# Optional Codex Model Routing

Use this reference only when the target repository contains `.codex/agents/` and Codex is the active client. It describes a vendor adapter; the repository's Markdown and Git workflow remains authoritative and client-neutral.

The adapter's root default is `gpt-5.6-terra` at medium reasoning. The root classifies work, chooses the repository route, and decides whether a specialist is warranted; it does not dynamically change its own model during a task.

## Roles

| Role | Route to it for | Default adapter policy |
|---|---|---|
| `explorer` | narrow read-only discovery, tracing, and evidence gathering | `gpt-5.6-terra`, low reasoning, read-only |
| `implementer` | one understood, scoped change and targeted validation | `gpt-5.6-terra`, medium reasoning, workspace-write |
| `reviewer` | correctness, security, regression, or missing-test review | `gpt-5.6-sol`, high reasoning, read-only |
| `architect` | ambiguous high-impact design or difficult unresolved root cause | `gpt-5.6-sol`, extra-high reasoning, read-only |

The configured model identifiers require the target account to expose them. If a model is unavailable, change only the affected `.codex/agents/*.toml` model setting to an account-supported equivalent; do not weaken the role's scope or durable workflow requirements.

## Delegation Rules

1. Use the cheapest capable role and do not delegate routine Direct work merely to use an agent.
2. Delegate only independent, bounded work. Keep delegation one level deep and end the agent after it reports a concise result.
3. Explorers, reviewers, and architects are read-only. They can run in parallel only when their scopes do not overlap materially.
4. An implementer is write-capable. Keep it serial with every other write-capable agent in its task worktree; use a separate task worktree for any concurrent write task.
5. Preserve findings, decisions, validation, risks, and next actions in the active WORK whenever the selected route requires a checkpoint. A subagent result is not durable state by itself.

## Recovery

If custom agents are unavailable, model access is denied, or the client does not support delegation, continue with the root agent and the normal repository workflow. Do not create a substitute runtime, hidden state file, or required orchestration service.
