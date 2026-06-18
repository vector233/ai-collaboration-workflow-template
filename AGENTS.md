# Repository Guidelines

This repository develops and distributes the AI Collaboration Workflow Template. It also dogfoods the workflow through the initialized root `zettelkasten/`.

## First Files To Read

Before changing the template, Skill, scripts, or project documents, read:

- `zettelkasten/AI.md`
- `zettelkasten/00-governance/ai-workflow.md`
- `zettelkasten/06-requirements/README.md`
- `zettelkasten/08-technical-designs/README.md`
- `zettelkasten/07-review/README.md`
- The active requirement, technical design, review handoff, architecture note, or runbook linked from the task

## Product And Maintenance Boundaries

- `template/` is the canonical downstream payload copied into user projects.
- `skills/ai-collaboration-workflow/` is the companion Agent Skill and bootstrap tooling.
- Root `zettelkasten/` is this repository's own project knowledge and maintenance evidence.
- `docs/` and `examples/` explain the product but are not copied into initialized projects.
- Never place repository-specific release, marketing, or maintenance records inside `template/`.

Any change to workflow rules must consider both the payload and the Skill. Do not update the root maintenance knowledge base as a substitute for updating `template/`.

## Cross-Agent Collaboration Contract

- `AGENTS.md` is the canonical shared instruction file. Codex reads it directly; `CLAUDE.md` imports it for Claude Code.
- Root `zettelkasten/` is the shared project memory. Required state must not exist only in chat history, Codex memories, Claude auto memory, or another tool's local files.
- Every agent starts from the repository state and linked workflow documents, not assumptions about what a previous agent did.
- Before editing, inspect the active REQ, approved TECH, and open REVIEW. If a handoff is open, continue or close it before starting another implementation slice.
- Before yielding, persist completed work, exact validation, worktree state, unresolved decisions, risks, and the next allowed action.
- Vendor-specific files are adapters only. Shared requirements, architecture, decisions, validation, and handoff rules remain vendor-neutral.

## Development Workflow

For non-trivial changes:

1. Confirm or create a root requirement under `zettelkasten/06-requirements/`.
2. Confirm the linked technical design is in `zettelkasten/08-technical-designs/approved/`.
3. Keep implementation within the paths declared by the active requirement.
4. Run focused validation, including `python3 scripts/validate_distribution.py` when payload or Skill behavior changes.
5. Create or update a root review handoff under `zettelkasten/07-review/`.
6. Record exact validation, risks, commit state, and worktree state.
7. Write durable distribution or workflow lessons back to root architecture, decisions, gotchas, or runbooks.

Tiny-fix waivers are limited to non-behavioral documentation and similarly low-risk local changes.

## Review Rules

- Treat review feedback as a hypothesis until evidence confirms it.
- Reproduce distribution findings against a temporary target, not only the source tree.
- Review payload changes for repository-specific content leakage.
- Do not close a review until confirmed findings are fixed and validation is recorded.

## Validation

Use commands from `zettelkasten/01-overview/quick-reference.md` and `zettelkasten/05-reference/e2e-test.md`.

At minimum:

- Documentation: `git diff --check`
- Payload or bootstrap: `python3 scripts/validate_distribution.py`
- Skill metadata: run the skill creator validator when its dependencies are available
- Wiki links: validate both root `zettelkasten/` and `template/zettelkasten/`

Do not claim validation that did not run.

## Git Hygiene

- Stage only files related to the active task.
- Do not revert unrelated user or agent changes.
- Keep generated artifacts, temporary clones, caches, secrets, and machine-specific files out of commits.
- Use concise conventional-style commits.
