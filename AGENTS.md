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
- The downstream core must remain usable with Markdown and Git alone. Companion-Skill scripts are optional automation and must not be copied into or required by `template/`.
- Downstream workflow feedback is opt-in, evidence-backed, sanitized, and user-approved before publication. Never add telemetry or automatic cross-project collection.
- When workflow behavior changes, align the canonical payload, Skill, documentation, examples, and validation as applicable.
- Never put repository-specific release, publishing, or maintenance material in `template/`.

## Development Workflow

1. Inspect the smallest relevant set of files.
2. Use a task branch for non-trivial work. Use a dedicated Git worktree for each concurrently active task or agent.
3. Make a scoped change and preserve unrelated user or agent work.
4. Update every affected distribution surface.
5. Run focused validation.
6. End each agent context that produces persistent changes, or each coherent slice, with a task-scoped commit. Do not create empty commits for read-only analysis. Keep incomplete checkpoints off `main`.
7. Run a Rule Promotion Check for long tasks, fixes, and review corrections: if the lesson would prevent a likely repeat mistake, record durable maintainer guidance in `AGENTS.md`, `CONTRIBUTING.md`, or `docs/`.

The Direct/Tracked/Governed routing model, stable WORK artifacts, optional TECH/PLAN/REVIEW gates, project-Skill promotion, and Git isolation policy are the product being distributed. Downstream WORK artifacts are not required for routine maintenance of this template repository itself.

## Review Rules

- Treat review findings as hypotheses and verify them with code, commands, temporary-project output, or official references.
- Reproduce distribution behavior in a temporary target, not only in the source tree.
- Keep harness self-tests separate from Agent behavior evidence. A bundled or synthetically derived response fixture may test the evaluator, but must not be reported as a fresh-Agent workflow result.
- Check payload changes for repository-specific content leakage.
- Do not claim validation that did not run.

## Validation

At minimum:

- Documentation: `git diff --check`
- Payload, Skill bootstrap, or distribution behavior: `python3 scripts/validate_distribution.py`
- Skill metadata: run the Skill validator when its dependencies are available
- Wiki links: validate links under `template/zettelkasten/`

## Git Hygiene

- Treat `main` as an integration branch for non-trivial work.
- One branch and worktree must not be shared by concurrent agents.
- Stage only files related to the current task.
- Do not revert unrelated user or agent changes.
- Keep generated artifacts, temporary clones, caches, secrets, and machine-specific files out of commits.
- Use `checkpoint:` or `wip:` only on task branches, and do not merge broken checkpoints.
- Use concise conventional-style commits.
