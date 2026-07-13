# Practical Scenarios

## Direct Documentation Fix

Broken internal link, local and reversible:

```text
route Direct -> edit -> link check -> git diff --check -> context commit
```

No WORK is created. If the failure reveals a repeatable authoring procedure, record it in the final context and consider a runbook or project Skill separately.

## Tracked Bounded Bug

Known local root cause with focused regression test:

```text
create one WORK -> task branch -> implement one slice -> test -> inline review
-> checkpoint commit -> experience decision -> done
```

The WORK contains the root cause, affected paths, acceptance, validation, commit, and next action. No separate artifact is needed.

## Governed Data Migration

Schema migration with rollback and release ordering:

```text
one WORK with migration, rollback, release, and approval gates -> dedicated worktree
-> per-slice commits and validation -> approval evidence -> experience promotion
```

The WORK remains in `zettelkasten/work/`; its status and gate evidence change in place.

## Parallel Tasks

Two independent tasks with non-overlapping paths:

```text
WORK-A -> task branch A -> worktree A -> Agent A
WORK-B -> task branch B -> worktree B -> Agent B
```

Each context commits only its task. Both tasks record experience candidates locally. Shared rules or project Skills are curated during integration, avoiding competing edits to `AGENTS.md`.

## Project Skill Promotion

A third-party sandbox reset procedure repeatedly causes failed tests:

1. Record the verified procedure as an experience candidate.
2. Confirm it is more than a short command and has a safe recovery path.
3. Create `project-skills/reset-provider-sandbox/SKILL.md`.
4. Add trigger metadata to `project-skills/INDEX.md`.
5. Check the index entry and test whether a fresh agent selects it for the next sandbox failure; use the optional Doctor when installed.

## Template Feedback Without Telemetry

The user corrects a workflow instruction that made an optional helper necessary, and the same workaround recurs in another task:

```text
verify evidence -> classify template-wide -> create local workflow-observations.md
-> sanitize -> wait for explicit user approval before any upstream Issue or PR
```

A normal task, one-off model mistake, or project-specific lesson creates no template feedback entry.
