# {{PROJECT_NAME}} AI Knowledge Entry

The project overview is [[project]]. Repository rules are in `AGENTS.md`.

Template baseline: `v4.1.1` (`canonical-payload-v4`).

## Resume With Minimal Context

1. Read `AGENTS.md`.
2. Inspect the current Git branch and `work/` index.
3. Read the active `WORK-*` matching the branch or assigned task, when one exists.
4. Read only its linked architecture notes, runbooks, and matching entry from `project-skills/INDEX.md`.

Do not load the whole vault by default. Workflow state lives in stable files under [[work/README]], not in chat history or a manually duplicated current-state note.

For parallel coordination, compare active WORK branch and owned-path fields with registered Git worktrees. Optional companion-Skill tools may automate this inspection.

## Cross-Agent Entry Points

| Agent | Instruction entry | Durable knowledge |
|---|---|---|
| Codex | `AGENTS.md`; explicitly installed optional `.codex/agents/` model-routing overlay | `zettelkasten/`, `project-skills/` |
| Claude Code | `CLAUDE.md` imports `AGENTS.md`; explicitly installed optional `.claude/agents/` model-routing overlay | `zettelkasten/`, `project-skills/` |
| Other repository-aware agents | explicitly read `AGENTS.md` | `zettelkasten/`, `project-skills/` |

The optional Codex and Claude Code overlays assign model, reasoning, and tool settings to the specialist roles in `AGENTS.md` only after explicit installation. They do not override the root-session model or replace the route decision, Git isolation, or Markdown checkpoint requirements.

## Route Tasks

Use [[workflow]] to choose Direct, Tracked, or Governed work. Route by scope, uncertainty, risk, reversibility, duration, coordination, and verification needs.

- Direct work creates no workflow artifact.
- Tracked work creates one `WORK-*` under [[work/README]].
- Governed work uses the same `WORK-*`, with explicit decisions, approvals, owners, evidence, and gates.

## Knowledge Routing

| Need | Read |
|---|---|
| Commands, ports, local setup | [[quick-reference]] |
| Project scope and constraints | [[project]] |
| Current architecture | [[architecture]] |
| Decisions and rationale | [[decisions]] |
| Known failure modes | [[gotchas]] |
| Validation policy and flows | [[validation-policy]], [[validation-runbook]] |
| Active or historical task state | [[work/README]] |
| On-demand project procedures | `project-skills/INDEX.md` |
| Skill creation and maintenance | [[skill-lifecycle]] |
| Parallel Git work | [[git-collaboration]] |
| Evidence-backed workflow or template friction | [[workflow]] Template Feedback Check |

## Writeback

Do not write a checkpoint after every turn. Update the active work item after each bounded Tracked or Governed slice and before an unfinished task crosses a handoff, long pause, agent or session switch, detectable context compaction, or any yield that would otherwise leave decisions only in chat. Direct work that completes, validates, and commits in the current context needs no WORK; otherwise re-route it to Tracked before yielding.

A checkpoint must let a fresh agent recover the route, acceptance state, completed step and commit, exact validation, risks or unresolved decisions, next allowed action, and experience candidates. Optional adapters may detect context pressure, but Markdown and Git remain sufficient.

At closeout, promote only durable knowledge to rules, gotchas, architecture notes, runbooks, decisions, or project Skills. Search first, update the canonical destination in place, and make repeated promotion a no-op when the knowledge is already current. For tracked or governed work, declare a shared destination in `owned_paths` and resolve overlap before editing it.

When the workflow itself caused repeatable friction, route a sanitized observation through the Template Feedback Check. Normal work produces no feedback artifact.

Use stable paths and wiki links. New knowledge notes must have an inbound link from an existing entry point or work item.
