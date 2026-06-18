# Repository Guidelines

This repository uses the AI Collaboration Workflow Template. The knowledge base lives in `zettelkasten/` and should guide every non-trivial change.

## First Files To Read

Before changing code or project documents, read the smallest relevant context pack:

- `zettelkasten/AI.md`
- `zettelkasten/00-governance/ai-workflow.md`
- `zettelkasten/06-requirements/README.md`
- `zettelkasten/08-technical-designs/README.md`
- `zettelkasten/07-review/README.md`
- Any requirement, technical design, review handoff, architecture note, or runbook linked from the current task

If this is an umbrella repository, also read the relevant subproject's own `AGENTS.md`, `CLAUDE.md`, or module-specific notes before editing that subproject.

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

## Development Workflow

For any non-trivial feature, fix, integration, or architecture change:

1. Confirm or create a requirement under `zettelkasten/06-requirements/`.
2. Confirm the requirement has a linked technical design under `zettelkasten/08-technical-designs/`.
3. Do not edit business code until the technical design is in `approved/`, unless the requirement or review document records a tiny-fix waiver.
4. Keep the implementation slice small and within the paths declared for the task.
5. Run focused validation for the changed boundary.
6. Create or update a review handoff under `zettelkasten/07-review/pending/`.
7. Record verification, known risks, commit hash, and worktree status in the handoff.
8. Write back durable lessons to `gotchas.md`, architecture notes, or E2E runbooks.

Tiny-fix waivers are appropriate for typo fixes, comments, non-behavioral docs, obvious local null checks, or similarly low-risk changes that do not change contracts, data, security, billing, permissions, persistence, deployment, or cross-module behavior.

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
- New review handoffs use `REVIEW-YYYYMMDDHHMMSS-short-name.md`.
- New notes must link to existing notes with double-bracket wiki links.
- When architecture, workflow, validation, or gotchas change, update the durable note that future agents should read.
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
