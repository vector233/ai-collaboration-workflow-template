---
title: AI Workflow
status: active
project: {{PROJECT_NAME}}
last_verified_at: YYYY-MM-DD
source_of_truth: mixed
related:
  - "[[AI]]"
  - "[[06-work/README]]"
  - "[[00-governance/skill-lifecycle]]"
  - "[[00-governance/git-collaboration]]"
---

# AI Workflow

## Purpose

This workflow keeps AI-assisted development resumable without forcing every task through the same document chain. Knowledge is durable; process artifacts are created only when risk or coordination justifies them.

## Minimal Context

Start with `AGENTS.md`, [[AI]], and:

```bash
python3 scripts/workflow_doctor.py --status
```

For active work, read its stable `WORK-*` document. Load only linked notes, runbooks, and matching project Skills. Do not scan the whole vault by default.

## Route Decision

Classify independent dimensions instead of relying on diff size alone:

| Dimension | Low signal | Escalation signal |
|---|---|---|
| Scope | one obvious local boundary | cross-module, cross-repository, shared contract |
| Uncertainty | known cause and approach | unresolved design or competing approaches |
| Risk | reversible and isolated | security, permissions, billing, data, production, destructive action |
| Duration | one coherent context | multiple contexts or dependent slices |
| Coordination | one owner | parallel agents, teams, migrations, release sequencing |
| Verification | focused deterministic check | realistic environment, independent approval, semantic review |

Choose one route:

| Route | Use when | Required state |
|---|---|---|
| Direct | local, reversible, low-risk, one context | change, validate, context commit |
| Tracked | meaningful behavior, multiple contexts, bug investigation, or resumability needed | one `WORK-*` with inline approach, slices, validation, review, and experience candidates |
| Governed | important uncertainty, high risk, independent approval, migration, release, or multi-owner coordination | `WORK-*` plus only the independent `TECH-*`, `PLAN-*`, or `REVIEW-*` artifacts triggered by the task |

Hard governed triggers include schema or data migration, security and permissions, billing, production deployment, destructive operations, important API compatibility, and unresolved architecture decisions.

The user may override a route. Record the reason in the work item.

## Stable Work Artifacts

All workflow artifacts live directly under [[06-work/README]] and never move for status changes:

- `WORK-YYYYMMDDHHMMSS-short-name.md`: canonical task state and default all-in-one record;
- `TECH-YYYYMMDDHHMMSS-short-name.md`: optional independent technical decision;
- `PLAN-YYYYMMDDHHMMSS-short-name.md`: optional independent execution coordination;
- `REVIEW-YYYYMMDDHHMMSS-short-name.md`: optional independent review lifecycle.

Use frontmatter status and update the file in place. Stable paths prevent link churn and make parallel branches easier to merge.

Create a separate artifact only when it is reused, independently approved, independently owned, too large for the work item, or has a different lifecycle. Otherwise keep the content inline.

## Tracked Work Loop

1. Create a `WORK-*` from [[00-governance/templates/work-item]].
2. Record the route, acceptance criteria, context pack, task branch, worktree, affected paths, and next action.
3. Resolve any governed TECH or PLAN gate.
4. Implement one bounded slice.
5. Run the smallest meaningful validation.
6. Review inline, or use an independent REVIEW when triggered.
7. Record a context checkpoint and commit all current-task changes.
8. Record experience candidates.
9. Repeat until acceptance and validation pass, then run Experience Promotion and close the work item.

Prefer the deterministic helper for state changes:

```bash
python3 scripts/workflow_task.py new <slug> --route tracked
python3 scripts/workflow_task.py checkpoint <WORK-ID> --completed-step <text> --validation <evidence> --next-action <text>
python3 scripts/workflow_task.py close <WORK-ID> --acceptance-complete --gates-closed --promotion-complete --writeback-complete --integration-result <text>
```

## Project Skill Routing

Before rediscovering a procedure, scan `project-skills/INDEX.md`. Load only the matching Skill. A project Skill is procedural memory, not general project documentation.

Create or update one only when the procedure is stable, likely to recur, has clear triggers, and includes validation and recovery. See [[00-governance/skill-lifecycle]].

## Experience Promotion Check

Run this check at context handoff and before closing tracked or governed work.

| Experience shape | Destination | Promotion bar |
|---|---|---|
| Every future agent must obey it before editing | `AGENTS.md` | high; concise must/never/check-before rule |
| Bug root, false assumption, troubleshooting fact | [[00-governance/gotchas]] | likely to recur |
| Architecture or data-flow invariant | `02-architecture/` or `04-cross-cutting/` | changes implementation choices |
| Simple command, setup order, or validation step | [[01-overview/quick-reference]] or [[05-reference/e2e-test]] | tested and reusable |
| Multi-step procedure with triggers, validation, and recovery | `project-skills/<name>/SKILL.md` | stable, repeated or high-impact, and retrieval-tested |
| One-off observation or low-confidence guess | active `WORK-*` only | do not promote |

For every candidate, record the decision, reason, destination, and exact content written. Avoid promoting duplicate or stale instructions.

## Git Isolation

Tracked and governed work uses a task branch. Concurrent work uses a dedicated worktree per task. Shared knowledge updates are delayed until Experience Promotion at task close to reduce merge hotspots. See [[00-governance/git-collaboration]].

## Completion

Tracked or governed work is complete when:

- acceptance criteria are satisfied;
- required validation ran or residual risk is explicit;
- required independent gates are closed;
- every context has a traceable commit;
- experience candidates have explicit promotion decisions;
- durable knowledge and project Skills are updated where required;
- the work item has `status: done` and the task worktree is clean.
