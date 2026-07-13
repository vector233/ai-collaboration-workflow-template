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

## Context Preservation And Resume

After a bounded slice, the agent must pause for another task. It updates the existing WORK with the completed step and commit, exact validation, unresolved risk, next allowed action, and experience candidates, then commits the checkpoint. It does not create a new handoff file.

For an important handoff, a fresh agent with no prior chat starts from `AGENTS.md` and `zettelkasten/AI.md`, follows the current branch to the WORK, and reports the recoverable state before editing. Routine slices do not run this semantic probe.

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

Each context commits only its task. Both tasks record experience candidates locally. Before promotion, one WORK claims the shared destination in `owned_paths`; the other task coordinates or defers, avoiding competing edits to `AGENTS.md` or a project Skill.

## Project Skill Promotion

A third-party sandbox reset procedure repeatedly causes failed tests:

1. Record the verified procedure as an experience candidate.
2. Confirm it is more than a short command and has a safe recovery path.
3. Search existing rules, runbooks, Skills, and index rows; update the canonical destination when one already exists.
4. Claim the Skill path and index in `owned_paths`, then create or update `project-skills/reset-provider-sandbox/SKILL.md` with one writer.
5. Add or update trigger metadata in `project-skills/INDEX.md` without duplicating its row.
6. Check the index entry and test whether a fresh agent selects it for the next sandbox failure; use the optional Doctor when installed.

## Template Feedback Without Telemetry

The user corrects a workflow instruction that made an optional helper necessary, and the same workaround recurs in another task:

```text
verify evidence -> classify template-wide -> create local workflow-observations.md
-> sanitize -> wait for explicit user approval before any upstream Issue or PR
```

A normal task, one-off model mistake, or project-specific lesson creates no template feedback entry.
