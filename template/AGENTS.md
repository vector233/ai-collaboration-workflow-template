# AI Collaboration Rules

## Start Here

Read only the smallest context needed:

1. `AGENTS.md`
2. `zettelkasten/AI.md`
3. the current Git branch and matching `zettelkasten/work/WORK-*.md`, when one exists
4. `project-skills/INDEX.md` for a matching procedure
5. only the linked architecture note, runbook, or project Skill needed for the current slice

Repository files are the durable source of truth. Chat history and vendor memory are optional caches.

## Workflow Routing

Before editing, choose the lightest safe route from `zettelkasten/workflow.md`:

- **Direct**: local, reversible, low-risk work. No workflow artifact is required.
- **Tracked**: create one stable `WORK-*` document with scope, acceptance, validation, checkpoints, review, and experience candidates.
- **Governed**: create one `WORK-*` and record required decisions, approvals, owners, evidence, and release or rollback gates in that file.

Route by scope, uncertainty, risk, reversibility, duration, and coordination. A small security, permission, billing, migration, production, or destructive change is governed even when its code diff is small.

Do not move workflow files to represent state. Update frontmatter in place so links remain stable.

Create and update WORK artifacts from `zettelkasten/templates/work-item.md`. Optional companion-Skill tools may automate the same Markdown updates, but repository files remain authoritative.

## Context Preservation

Do not checkpoint every turn. For Tracked or Governed work, preserve context after each bounded slice. For any unfinished task, preserve it before a handoff, long pause, agent or session switch, detectable context compaction, or any yield that would otherwise leave decisions only in chat. Direct work that completes, validates, and commits in the current context needs no WORK; if it cannot, re-route it to Tracked before yielding.

For Tracked or Governed work, update the active WORK so a fresh agent can recover the selected route, current acceptance state, latest completed step and commit, exact validation, unresolved risks or decisions, next allowed action, and experience candidates. Then commit the current-task changes. Context-pressure detection may be supplied by an optional vendor adapter, but the core protocol never depends on runtime telemetry.

## Project Skills And Experience

Project Skills are durable, on-demand procedures under `project-skills/`. Scan `project-skills/INDEX.md` for matching triggers before rediscovering a known procedure, then read only the matched `SKILL.md`.

After validation, run a lightweight Learning Check before completing every task. Direct work with no verified reusable lesson creates no artifact. If Direct work exposes a verified reusable lesson that should change shared knowledge, re-route it to Tracked before durable writeback. Tracked and Governed work records every candidate and final decision in the active WORK.

The Learning Loop is: detect a lesson, capture evidence, search existing knowledge, classify the smallest durable destination, write or record a no-op, validate retrieval, and commit the resulting diff. At each context checkpoint, preserve unresolved candidates. Before closing tracked or governed work, run the Experience Promotion Check:

- repository-wide must/never/check-before behavior -> `AGENTS.md`;
- bug roots and false assumptions -> `zettelkasten/gotchas.md`;
- architecture facts and invariants -> `zettelkasten/architecture.md` or a linked domain note;
- simple commands and environment steps -> runbooks;
- repeated, stable, multi-step procedures with validation and recovery -> `project-skills/<skill-name>/SKILL.md` plus `project-skills/INDEX.md`.

Do not create a Skill from a one-off incident, an unverified guess, or a procedure that is simpler as a short rule or runbook entry. Follow `zettelkasten/skill-lifecycle.md`.

Before durable writeback, search the intended destination and `project-skills/INDEX.md`. Update the existing canonical rule, note, runbook, or Skill instead of creating a duplicate. For Tracked or Governed work, the active WORK owns each pending candidate; add a shared destination to `owned_paths` and check active WORK overlap before editing it. If another task owns that destination, coordinate or defer the promotion. Re-running the promotion must update the same destination or record a no-op, not create a second copy.

Learning writeback is repository change, not hidden agent memory. Make it on the task branch as a reviewable Git diff. Do not silently change repository-wide rules, architecture constraints, security or permission behavior, release procedures, or an existing Skill's contract on the default branch. Require evidence and the same review or Governed gates that an equivalent code or policy change would need.

## Workflow Feedback

At a tracked or governed checkpoint, at closeout, or after the user corrects workflow behavior, silently check for evidence-backed template friction. Record nothing when the workflow was adequate.

- Project-specific lessons follow the normal Experience Promotion destinations.
- Repeated or high-impact template-wide friction goes to `zettelkasten/workflow-observations.md`, created on first use from the repository template.
- Vendor-specific behavior is labeled separately and must not become a vendor-neutral core rule without cross-agent evidence.
- Never include secrets, customer data, private code, or internal identifiers. Never transmit feedback or create an upstream issue without explicit user approval.

Follow the Template Feedback Check in `zettelkasten/workflow.md`.

## Specialist Delegation

When the current client exposes configured specialist agents, use the cheapest capable specialist only for an independent, bounded subtask that materially improves speed or confidence:

- **Explorer**: read-only codebase discovery, symbol lookup, execution tracing, logs, and evidence gathering before a change.
- **Implementer**: one well-scoped feature, fix, test update, or routine refactor after the code path and acceptance criteria are understood.
- **Reviewer**: read-only correctness, security, regression, data-consistency, or missing-test review.
- **Architect**: read-only analysis of ambiguous, high-impact cross-module design, migration, or root-cause decisions after ordinary investigation is insufficient.

Do not delegate routine Direct work merely to use an agent. Keep delegation at one level, return concise evidence rather than raw logs, and stop an agent once its assigned task is complete. Read-only specialists may run in parallel only when their scopes are independent. A write-capable implementer must be the only write-capable agent in its task worktree; use a dedicated task worktree for any concurrent write task.

When explicitly installed, the optional Codex and Claude Code overlays in `.codex/agents/` and `.claude/agents/` bind these roles to available models, reasoning levels, and tool policies without changing the root-session model. No route, checkpoint, validation, or durable project state may depend on an adapter.

## Git Isolation And Commits

Follow `zettelkasten/git-collaboration.md` unless stricter repository rules apply.

- Do not implement tracked or governed work directly on `main` or `master`.
- Use one task branch per work item. Use one Git worktree per concurrently active task or write-capable agent. Independent read-only specialists may inspect the current task worktree.
- Do not run dependent or overlapping tasks in parallel without an explicit integration plan.
- Each agent context that produces persistent changes, or each coherent implementation slice, must end with a task-scoped commit. Read-only analysis does not create an empty commit.
- Use `checkpoint:` or `wip:` commits only on task branches when incomplete state must be handed off. Broken checkpoints must not be merged into the default branch.
- Stage only current-task files. Never commit secrets, caches, logs, local databases, generated junk, or unrelated user changes.
- Record the commit and exact validation result in the work item before yielding.

## Validation And Review

- Use project commands from `zettelkasten/quick-reference.md` and `zettelkasten/validation-runbook.md`.
- Do not claim checks that did not run. Record blockers and residual risk.
- Treat review feedback as a hypothesis. Verify it with code, commands, logs, screenshots, commits, or official references.
- Keep review and approval evidence in the work item. Link project-native Issues, pull requests, or decision records when another system owns the approval.
- Check changed knowledge links, work state, and project-Skill routing before handoff. Optional companion-Skill tools may automate these checks.
- For important multi-context handoffs or changes to resume semantics, use the semantic Fresh-Agent Resume Probe in `zettelkasten/validation-policy.md`; routine work needs only the normal structural checks.
- Coordinate parallel tasks from Git branches, worktrees, and declared owned paths; do not depend on hidden tool state.

## Cross-Agent Contract

- `AGENTS.md` is canonical shared instruction; `CLAUDE.md` and optional `.codex/` or `.claude/` configuration are vendor adapters.
- Vendor-specific tools may assist execution but must not own required project state.
- External Skills must map durable output into the active work item, knowledge notes, runbooks, or project Skills.
- Before a preservation trigger yields control, satisfy the Context Preservation contract above.
