# AI Collaboration Rules

## Start Here

Read only the smallest context needed:

1. `AGENTS.md`
2. `zettelkasten/AI.md`
3. `python3 scripts/workflow_doctor.py --status`
4. the active `zettelkasten/06-work/WORK-*.md`
5. only the linked architecture note, runbook, or project Skill needed for the current slice

Repository files are the durable source of truth. Chat history and vendor memory are optional caches.

## Workflow Routing

Before editing, choose the lightest safe route from `zettelkasten/00-governance/ai-workflow.md`:

- **Direct**: local, reversible, low-risk work. No workflow artifact is required.
- **Tracked**: create one stable `WORK-*` document with scope, acceptance, validation, checkpoints, review, and experience candidates.
- **Governed**: use a `WORK-*` document and create separate `TECH-*`, `PLAN-*`, or `REVIEW-*` documents only when they need an independent lifecycle.

Route by scope, uncertainty, risk, reversibility, duration, and coordination. A small security, permission, billing, migration, production, or destructive change is governed even when its code diff is small.

Do not move workflow files to represent state. Update frontmatter in place so links remain stable.

## Project Skills And Experience

Project Skills are durable, on-demand procedures under `project-skills/`. Scan `project-skills/INDEX.md` for matching triggers before rediscovering a known procedure, then read only the matched `SKILL.md`.

At each context checkpoint, record reusable experience candidates in the active work item. Before closing tracked or governed work, run the Experience Promotion Check:

- repository-wide must/never/check-before behavior -> `AGENTS.md`;
- bug roots and false assumptions -> `zettelkasten/00-governance/gotchas.md`;
- architecture facts and invariants -> architecture or cross-cutting notes;
- simple commands and environment steps -> runbooks;
- repeated, stable, multi-step procedures with validation and recovery -> `project-skills/<skill-name>/SKILL.md` plus `project-skills/INDEX.md`.

Do not create a Skill from a one-off incident, an unverified guess, or a procedure that is simpler as a short rule or runbook entry. Follow `zettelkasten/00-governance/skill-lifecycle.md`.

## Git Isolation And Commits

Follow `zettelkasten/00-governance/git-collaboration.md` unless stricter repository rules apply.

- Do not implement tracked or governed work directly on `main` or `master`.
- Use one task branch per work item. Use one Git worktree per concurrently active task or agent.
- Do not run dependent or overlapping tasks in parallel without an explicit integration plan.
- Each agent context or coherent implementation slice must end with a task-scoped commit.
- Use `checkpoint:` or `wip:` commits only on task branches when incomplete state must be handed off. Broken checkpoints must not be merged into the default branch.
- Stage only current-task files. Never commit secrets, caches, logs, local databases, generated junk, or unrelated user changes.
- Record the commit and exact validation result in the work item before yielding.

## Validation And Review

- Use project commands from `zettelkasten/01-overview/quick-reference.md` and `zettelkasten/05-reference/e2e-test.md`.
- Do not claim checks that did not run. Record blockers and residual risk.
- Treat review feedback as a hypothesis. Verify it with code, commands, logs, screenshots, commits, or official references.
- Keep review inline in the work item by default. Create a separate `REVIEW-*` only for independent reviewers, multiple rounds, high risk, or a distinct approval lifecycle.
- Run `python3 scripts/workflow_doctor.py` after workflow or project-Skill changes and before handoff.

## Cross-Agent Contract

- `AGENTS.md` is canonical shared instruction; `CLAUDE.md` is an adapter.
- Vendor-specific tools may assist execution but must not own required project state.
- External Skills must map durable output into the active work item, knowledge notes, runbooks, or project Skills.
- Before yielding, persist the current state, validation, commit, risks, unresolved decisions, and next allowed action.
