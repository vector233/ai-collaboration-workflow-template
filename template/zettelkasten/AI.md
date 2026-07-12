# {{PROJECT_NAME}} AI Knowledge Entry

The human-readable project index is [[{{PROJECT_NAME_SAFE}}]]. Repository rules are in `AGENTS.md`.

## Resume With Minimal Context

1. Read `AGENTS.md`.
2. Run `python3 scripts/workflow_doctor.py --status`.
3. Read the active `WORK-*` matching the current branch or assigned task.
4. Read only its linked architecture notes, runbooks, and matching entry from `project-skills/INDEX.md`.

Do not load the whole vault by default. Workflow state lives in stable files under [[06-work/README]], not in chat history or a manually duplicated current-state note.

For parallel coordination or tool integration, use `python3 scripts/workflow_doctor.py --status --all-worktrees --json`.

## Cross-Agent Entry Points

| Agent | Instruction entry | Durable knowledge |
|---|---|---|
| Codex | `AGENTS.md` | `zettelkasten/`, `project-skills/` |
| Claude Code | `CLAUDE.md` imports `AGENTS.md` | `zettelkasten/`, `project-skills/` |
| Other repository-aware agents | explicitly read `AGENTS.md` | `zettelkasten/`, `project-skills/` |

## Route Tasks

Use [[00-governance/ai-workflow]] to choose Direct, Tracked, or Governed work. Route by scope, uncertainty, risk, reversibility, duration, coordination, and verification needs.

- Direct work creates no workflow artifact.
- Tracked work creates one `WORK-*` under [[06-work/README]].
- Governed work adds independent TECH, PLAN, or REVIEW files only when triggered.

## Knowledge Routing

| Need | Read |
|---|---|
| Commands, ports, local setup | [[01-overview/quick-reference]] |
| Project scope and constraints | [[00-governance/project-overview]] |
| Current architecture | [[02-architecture/current-architecture-flow]] |
| Decisions and rationale | [[00-governance/decisions]] |
| Known failure modes | [[00-governance/gotchas]] |
| Validation policy and flows | [[00-governance/validation-discipline]], [[05-reference/e2e-test]] |
| Active or historical task state | [[06-work/README]] |
| On-demand project procedures | `project-skills/INDEX.md` |
| Skill creation and maintenance | [[00-governance/skill-lifecycle]] |
| Parallel Git work | [[00-governance/git-collaboration]] |

## Writeback

At every context checkpoint, update the active work item with the commit, validation, risks, next action, and experience candidates. At closeout, promote only durable knowledge to rules, gotchas, architecture notes, runbooks, decisions, or project Skills.

Use stable paths and wiki links. New knowledge notes must have an inbound link from an existing entry point or work item.
