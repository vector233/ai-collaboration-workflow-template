# {{PROJECT_NAME}} AI Knowledge Entry

The human-readable project index is [[{{PROJECT_NAME_SAFE}}]]. Repository rules are in `AGENTS.md`.

Template baseline: `canonical-payload-v3`. Use a release tag or commit instead when known more precisely.

## Resume With Minimal Context

1. Read `AGENTS.md`.
2. Inspect the current Git branch and `06-work/` index.
3. Read the active `WORK-*` matching the branch or assigned task, when one exists.
4. Read only its linked architecture notes, runbooks, and matching entry from `project-skills/INDEX.md`.

Do not load the whole vault by default. Workflow state lives in stable files under [[06-work/README]], not in chat history or a manually duplicated current-state note.

For parallel coordination, compare active WORK branch and owned-path fields with registered Git worktrees. Optional companion-Skill tools may automate this inspection.

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
| Evidence-backed workflow or template friction | [[00-governance/ai-workflow]] Template Feedback Check |

## Writeback

At every context checkpoint, update the active work item with the commit, validation, risks, next action, and experience candidates. At closeout, promote only durable knowledge to rules, gotchas, architecture notes, runbooks, decisions, or project Skills.

When the workflow itself caused repeatable friction, route a sanitized observation through the Template Feedback Check. Normal work produces no feedback artifact.

Use stable paths and wiki links. New knowledge notes must have an inbound link from an existing entry point or work item.
