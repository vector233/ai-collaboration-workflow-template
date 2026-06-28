# Repository Guidelines

This repository uses the AI Collaboration Workflow Template. The knowledge base lives in `zettelkasten/` and should guide every non-trivial change.

## First Files To Read

Before changing code or project documents, read the smallest relevant context pack:

- `zettelkasten/AI.md`
- `zettelkasten/00-governance/ai-workflow.md`
- `zettelkasten/06-requirements/README.md`
- `zettelkasten/08-technical-designs/README.md`
- `zettelkasten/09-implementation-plans/README.md` when the task uses a standalone plan
- `zettelkasten/07-review/README.md`
- Any requirement, technical design, implementation plan, review handoff, architecture note, or runbook linked from the current task

If this is an umbrella repository, also read the relevant subproject's own `AGENTS.md`, `CLAUDE.md`, or module-specific notes before editing that subproject.

## Cross-Agent Collaboration Contract

- `AGENTS.md` is the canonical shared instruction file. Codex reads it directly; `CLAUDE.md` imports it for Claude Code.
- `zettelkasten/` is the shared project memory. Required state must not exist only in chat history, Codex memories, Claude auto memory, or another tool's local files.
- Every agent starts from repository state and linked workflow documents, not assumptions about a previous agent's conversation.
- Before editing, inspect the active REQ, any controlling TECH or PLAN, and open REVIEW. Continue or close an open handoff before starting another implementation slice.
- Before yielding, persist completed work, exact validation, worktree state, unresolved decisions, risks, and the next allowed action.
- After long-running tasks, bug fixes, or review fixes, perform a Rule Promotion Check: decide whether the lesson should become a durable project rule, and write it to the future agent entry point that will prevent the mistake from recurring.
- Vendor-specific files are adapters only. Shared requirements, architecture, decisions, validation, and handoff rules remain vendor-neutral.

## Optional External Process Skills

External process skills, plugins, and agent frameworks are optional. The repository workflow must remain fully usable when none are installed.

- Repository files and the `REQ -> [TECH] -> [PLAN] -> implementation and validation -> REVIEW -> Rule Promotion Check -> writeback` flow remain the source of truth. Bracketed artifacts are optional unless the REQ marks them required.
- External brainstorming may refine the active REQ and TECH; it must not create a parallel specification system.
- External implementation planning should update the REQ implementation slices or a linked PLAN. It does not make PLAN mandatory for every task.
- External TDD, debugging, execution, or review skills may guide how work is performed, but their durable results must be recorded in the current REQ, TECH, PLAN, REVIEW, architecture note, gotcha, or runbook.
- Do not create `docs/superpowers/specs/`, `docs/superpowers/plans/`, or equivalent tool-specific project state unless the user explicitly requests a parallel export.
- An approved TECH, or complete inline technical readiness in the REQ when standalone TECH is not required, satisfies an external design gate.
- External instructions to commit, branch, or create a worktree do not override this repository's Git policy or explicit user direction.

Read `zettelkasten/00-governance/external-skill-interoperability.md` only when an external process skill is installed, invoked, or causing workflow conflicts.

## Project Structure

- `zettelkasten/00-governance/`: AI workflow, validation policy, decisions, glossary, gotchas, templates.
- `zettelkasten/01-overview/`: quick reference, product vision, high-frequency commands and URLs.
- `zettelkasten/02-architecture/`: current architecture facts and system flows.
- `zettelkasten/03-roadmap/`: phase and release planning.
- `zettelkasten/04-cross-cutting/`: cross-module concerns for umbrella projects.
- `zettelkasten/05-reference/`: summaries of long docs, E2E runbooks, external references.
- `zettelkasten/06-requirements/`: requirement workflow, `backlog/ -> in-progress/ -> done/`.
- `zettelkasten/07-review/`: review handoff workflow, `pending/ -> in-review/ -> done/`.
- `zettelkasten/08-technical-designs/`: design workflow, `pending/ -> approved/ -> implemented/`.
- `zettelkasten/09-implementation-plans/`: optional detailed execution plans.

## Development Workflow

For any tracked feature, fix, integration, or architecture change:

1. Confirm or create a requirement under `zettelkasten/06-requirements/`.
2. In the REQ, decide whether standalone TECH and PLAN documents are required.
3. If TECH is required, do not edit business code until it is in `approved/`. If it is not required, complete the REQ's inline technical readiness.
4. If PLAN is required, do not implement until it is `ready`. If it is not required, keep sufficient implementation slices in the REQ.
5. Implement one bounded slice and run focused validation for the changed boundary.
6. Create or update a review handoff under `zettelkasten/07-review/pending/`.
7. Record verification, known risks, commit hash, and worktree status in the handoff.
8. Run the Rule Promotion Check and write back durable lessons to `AGENTS.md`, `gotchas.md`, architecture notes, cross-cutting rules, or E2E runbooks.

Standalone TECH is normally required for architecture, API, schema, persistence, security, billing, permission, deployment, third-party, or cross-module changes, and when important technical decisions remain unresolved.

Standalone PLAN is normally useful for multiple dependent slices, multiple sessions or agents, cross-repository work, migrations, releases, or work needing precise file ownership and checkpoints.

Tiny-fix waivers may bypass REQ/TECH/PLAN documents only for typo fixes, comments, non-behavioral docs, or similarly low-risk changes. A bounded bug can keep a REQ while marking standalone TECH and PLAN as not required.

## Review Rules

Review feedback is not automatically true. Treat each important review point as a hypothesis:

- Accept evidence from code locations, reproducible commands, logs, screenshots, commits, docs, or official references.
- Ask for evidence when feedback is vague or unsupported.
- Fix confirmed or partially confirmed issues, then record validation.
- Reject unsupported or false findings with concrete counter-evidence in the review handoff.
- Do not start the next development slice until the current review handoff is closed or explicitly waived.

## Documentation Rules

- New requirements use `REQ-YYYYMMDDHHMMSS-short-name.md`.
- New technical designs use `TECH-YYYYMMDDHHMMSS-short-name.md`.
- New implementation plans use `PLAN-YYYYMMDDHHMMSS-short-name.md`.
- New review handoffs use `REVIEW-YYYYMMDDHHMMSS-short-name.md`.
- New notes must link to existing notes with double-bracket wiki links.
- When architecture, workflow, validation, or gotchas change, update the durable note that future agents should read.
- Promote a lesson to a durable rule when it prevents a likely repeat mistake. Use `AGENTS.md` for repository-wide must/never/always behavior, `gotchas.md` for bug roots and false assumptions, architecture or cross-cutting notes for system invariants, and runbooks for commands or environment steps.
- Never commit secrets, tokens, real credentials, private customer data, or unredacted production logs.

## Validation

Use project-specific commands from `zettelkasten/01-overview/quick-reference.md` and `zettelkasten/05-reference/e2e-test.md`.

As a default:

- Documentation-only changes: run `git diff --check`.
- Backend/API changes: run unit or integration tests for the affected package.
- Frontend changes: run lint/build and browser verification for user-visible flows.
- Database or migration changes: verify schema changes against a realistic database.
- Installer, desktop, mobile, hardware, or third-party integration changes: run the closest real-environment smoke test before review.

If required validation cannot be run, record the blocker and residual risk in the review handoff. Do not imply coverage you did not perform.

## Git Hygiene

- Stage only files related to the current task.
- Do not revert unrelated user or agent changes.
- Use concise conventional-style commits such as `docs: add checkout requirements` or `fix(api): reject expired session tokens`.
- Keep generated artifacts, temporary logs, secrets, local databases, and machine-specific files out of commits.
