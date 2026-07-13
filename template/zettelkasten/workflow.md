---
title: AI Workflow
status: active
project: {{PROJECT_NAME}}
last_verified_at: YYYY-MM-DD
source_of_truth: mixed
related:
  - "[[AI]]"
  - "[[work/README]]"
  - "[[skill-lifecycle]]"
  - "[[git-collaboration]]"
---

# AI Workflow

## Purpose

This workflow keeps AI-assisted development resumable without forcing every task through a document chain. Knowledge is durable; process records stay proportional to the work.

## Minimal Context

Start with `AGENTS.md` and [[AI]]. For active work, inspect the current branch and read its stable `WORK-*` document. Load only linked notes, runbooks, and matching project Skills. Do not scan the whole vault by default.

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
| Governed | important uncertainty, high risk, independent approval, migration, release, or multi-owner coordination | one `WORK-*` with explicit decision, approval, evidence, release, and rollback gates |

Hard governed triggers include schema or data migration, security and permissions, billing, production deployment, destructive operations, important API compatibility, and unresolved architecture decisions.

The user may override a route. Record the reason in the work item.

## Stable Work Record

Tracked and governed work has one canonical record under [[work/README]]:

- `WORK-YYYYMMDDHHMMSS-short-name.md`: scope, route, context, gates, implementation slices, validation, review, checkpoint, and experience writeback.

Use frontmatter status and update the file in place. Stable paths prevent link churn and make parallel branches easier to merge.

Write durable architecture facts, decisions, runbooks, and gotchas to their knowledge notes. Link project-native Issues, pull requests, release records, or external approvals instead of duplicating their lifecycle in workflow-specific files.

## Context Preservation

Preserve context at meaningful boundaries, not after every turn. For Tracked or Governed work, update the checkpoint after each bounded implementation slice. For any unfinished task, preserve state before:

- handing work to another agent or reviewer;
- a long pause, session switch, or detectable context compaction;
- yielding while a decision, validation result, risk, or next action exists only in chat.

Direct work that completes, validates, and commits in the current context needs no WORK. If it cannot finish before one of these boundaries, re-route it to Tracked and create a WORK. Update the WORK with the selected route, acceptance state, completed step and commit, exact validation, unresolved risks or decisions, next allowed action, and experience candidates. Commit the current-task state after the checkpoint. Vendor-specific context-pressure detection may prompt this step, but it is optional and owns no project state.

## Tracked Work Loop

1. Create a `WORK-*` from [[templates/work-item]].
2. Record the route, acceptance criteria, context pack, task branch, worktree, affected paths, and next action.
3. Resolve any governed decision or approval gate recorded in the work item.
4. Implement one bounded slice.
5. Run the smallest meaningful validation.
6. Record review evidence and link any project-native review or approval.
7. At a preservation boundary, record a context checkpoint and commit all current-task changes.
8. Record experience candidates.
9. Repeat until acceptance and validation pass, then run Experience Promotion and close the work item.

Edit the Markdown state directly. If the companion Skill is installed, its optional helpers may create or update the same file. The helper is never the source of truth.

## Project Skill Routing

Before rediscovering a procedure, scan `project-skills/INDEX.md`. Load only the matching Skill. A project Skill is procedural memory, not general project documentation.

Create or update one only when the procedure is stable, likely to recur, has clear triggers, and includes validation and recovery. See [[skill-lifecycle]].

## Experience Promotion Check

Run this check at context handoff and before closing tracked or governed work.

| Experience shape | Destination | Promotion bar |
|---|---|---|
| Every future agent must obey it before editing | `AGENTS.md` | high; concise must/never/check-before rule |
| Bug root, false assumption, troubleshooting fact | [[gotchas]] | likely to recur |
| Architecture or data-flow invariant | [[architecture]] or a linked domain note | changes implementation choices |
| Simple command, setup order, or validation step | [[quick-reference]] or [[validation-runbook]] | tested and reusable |
| Multi-step procedure with triggers, validation, and recovery | `project-skills/<name>/SKILL.md` | stable, repeated or high-impact, and retrieval-tested |
| Evidence-backed workflow-template friction | `workflow-observations.md` | repeated, high-impact, or a user correction identified reusable template behavior; sanitized |
| One-off observation or low-confidence guess | active `WORK-*` only | do not promote |

For every candidate, record the decision, reason, destination, and exact content written.

### Idempotent Writeback

1. Search existing rules, notes, runbooks, decisions, and `project-skills/INDEX.md` before writing.
2. Update the smallest canonical destination instead of creating parallel instructions. Mark obsolete content as superseded and link its replacement when deletion would lose useful history.
3. For Tracked or Governed work, treat the active WORK as the candidate owner. Add any shared destination to `owned_paths` and check active WORK overlap before editing it.
4. When another active task owns the same destination, coordinate a single writer or defer promotion until integration.
5. Record a no-op decision when the destination already contains the current verified knowledge. Re-running promotion must not create duplicate notes, Skills, or index rows.

## Template Feedback Check

Run this as a silent classification at tracked or governed checkpoints, closeout, and after a user corrects workflow behavior. If no trigger is present, create no observation and add no completion ceremony.

Record a local observation only when there is concrete evidence that one of these occurred:

- the workflow required unnecessary artifacts or context;
- an expected knowledge route was missing, stale, duplicated, or contradictory;
- the same workflow clarification or workaround recurred;
- an optional helper became necessary to complete the core path;
- promoted experience was not discoverable when its documented trigger recurred;
- the user or reviewer corrected a likely reusable template behavior.

Classify before writing:

| Scope | Destination |
|---|---|
| project-specific fact or procedure | normal Experience Promotion destination |
| template-wide workflow friction | create `workflow-observations.md` from [[templates/workflow-observations]] on first use |
| vendor-specific behavior | the same observation file with scope `vendor-specific` |
| one-off model mistake or unsupported opinion | do not record |

Include expected behavior, observed behavior, reproducible evidence, impact, and a privacy check. Do not include private code, customer data, secrets, internal URLs, or identifying business details. Local observations never authorize network transmission; prepare or submit upstream feedback only after explicit user review and approval.

## Git Isolation

Tracked and governed work uses a task branch. Concurrent work uses a dedicated worktree per task. Shared knowledge updates are delayed until Experience Promotion at task close when practical, then claimed in `owned_paths` before editing to reduce merge hotspots. See [[git-collaboration]].

## Completion

Tracked or governed work is complete when:

- acceptance criteria are satisfied;
- required validation ran or residual risk is explicit;
- required governed gates are closed;
- every context has a traceable commit;
- the latest checkpoint is sufficient for a fresh agent to identify the next allowed action without chat history;
- experience candidates have explicit promotion decisions;
- durable knowledge and project Skills are updated where required;
- the work item has `status: done` and the task worktree is clean.
