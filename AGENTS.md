# Repository Guidelines

This repository develops and distributes the AI Collaboration Workflow Template. The product knowledge-base payload lives under `template/`; this maintenance repository intentionally does not keep a second root `zettelkasten/`.

## Repository Structure

- `template/`: canonical files copied into downstream projects.
- `skills/ai-collaboration-workflow/`: companion Agent Skill and bootstrap tooling.
- `scripts/validate_distribution.py`: end-to-end distribution contract.
- `docs/`: maintainer and publishing documentation.
- `examples/`: fictional initialized-project walkthroughs.

## Cross-Agent Collaboration Contract

- `AGENTS.md` is the canonical shared instruction file. Codex reads it directly; `CLAUDE.md` imports it for Claude Code.
- Shared behavior belongs in repository files, not chat history, vendor memory, or tool-local state.
- Vendor-specific files are adapters only. Keep requirements, workflow semantics, validation, and handoff rules vendor-neutral.
- When workflow behavior changes, align the canonical payload, Skill, documentation, examples, and validation as applicable.
- Never put repository-specific release, publishing, or maintenance material in `template/`.

## Development Workflow

1. Inspect the smallest relevant set of files.
2. Make a scoped change and preserve unrelated user or agent work.
3. Update every affected distribution surface.
4. Run focused validation.
5. Run a Rule Promotion Check for long tasks, fixes, and review corrections: if the lesson would prevent a likely repeat mistake, record durable maintainer guidance in `AGENTS.md`, `CONTRIBUTING.md`, or `docs/`.

The REQ, TECH, and REVIEW workflow is the product being distributed. It is not required for routine maintenance of this template repository itself.

## Review Rules

- Treat review findings as hypotheses and verify them with code, commands, temporary-project output, or official references.
- Reproduce distribution behavior in a temporary target, not only in the source tree.
- Check payload changes for repository-specific content leakage.
- Do not claim validation that did not run.

## Validation

At minimum:

- Documentation: `git diff --check`
- Payload, Skill bootstrap, or distribution behavior: `python3 scripts/validate_distribution.py`
- Skill metadata: run the Skill validator when its dependencies are available
- Wiki links: validate links under `template/zettelkasten/`

## Git Hygiene

- Stage only files related to the current task.
- Do not revert unrelated user or agent changes.
- Keep generated artifacts, temporary clones, caches, secrets, and machine-specific files out of commits.
- Use concise conventional-style commits.
