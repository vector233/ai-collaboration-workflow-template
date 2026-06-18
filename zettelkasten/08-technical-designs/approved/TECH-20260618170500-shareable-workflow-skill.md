---
title: Shareable AI Collaboration Workflow Skill
status: approved
project: AI Collaboration Workflow Template
technical_design_id: TECH-20260618170500-shareable-workflow-skill
last_verified_at: 2026-06-18
source_of_truth: mixed
related_requirement:
  - "[[06-requirements/in-progress/REQ-20260618170000-shareable-workflow-skill]]"
related:
  - "[[02-architecture/current-architecture-flow]]"
  - "[[08-technical-designs/README]]"
---

# Shareable AI Collaboration Workflow Skill

## What This Design Answers

This design defines how one portable Skill can guide daily workflow operations and safely bootstrap one canonical downstream template payload while the repository maintains its own initialized knowledge base separately.

## Related Requirement

- Requirement: [[06-requirements/in-progress/REQ-20260618170000-shareable-workflow-skill]]
- Requirement status: in-progress
- Acceptance summary: the Skill must be portable, conflict-safe, executable, and explicit about bootstrap versus project initialization.

## Current Architecture Facts

- `skills/ai-collaboration-workflow/SKILL.md` already describes template presence checks and daily workflow rules.
- Bootstrap currently uses an inline shallow clone plus direct `cp`, which can overwrite local files and is difficult to validate independently.
- The repository root currently mixes downstream template content and project-maintenance content.
- `template/INIT.md` is the canonical downstream initialization runbook.
- GitHub's template-repository feature cannot exclude repository-maintenance files.

## Target Technical Flow

1. The Skill checks for the required core template files in the target repository.
2. If the template is present, the agent reads the target repository's canonical workflow files and performs the requested REQ/TECH/REVIEW or writeback operation.
3. If the template is missing and bootstrap is authorized, the agent invokes the bundled Python script.
4. The script resolves a source from `--source` or clones `--repo-url` at `--ref` into a temporary directory.
5. The script selects `<source>/template/` when present, or accepts a direct payload directory for offline use.
6. The script inventories `AGENTS.md`, `CLAUDE.md`, `INIT.md`, and all files under the payload's `zettelkasten/`, including empty-state `.gitkeep` files.
7. Missing files are copied; identical files are skipped; differing existing files are reported as conflicts and left untouched.
8. The agent inspects conflicts and merges repository-specific rules manually.
9. The agent follows the target repository's `INIT.md`, gathers project-specific answers, replaces placeholders, validates, and removes `INIT.md`.
10. After initialization, the target repository's `AGENTS.md` and `zettelkasten/` become authoritative.
11. The repository root maintains separate initialized project knowledge and review evidence.
12. A distribution smoke test verifies the clean payload and first REQ/TECH/REVIEW creation.

## Decisions

| Decision | Outcome | Reason | Impact |
|---|---|---|---|
| Template payload | Store canonical downstream files under `template/` | Separate distributable content from repository maintenance and avoid Skill duplication | README and bootstrap must always target this directory |
| GitHub template button | Do not present the repository root as the clean install path | GitHub copies every repository file and cannot exclude maintenance evidence | Users install through the Skill or copy `template/` contents |
| Default conflict behavior | Never overwrite differing files | Repository instructions are high-value local content | AI must merge conflicts explicitly |
| Implementation language | Python standard library | Portable and testable without third-party packages | Requires Python 3.9+ |
| Initialization authority | Continue through `INIT.md` | Project-specific metadata cannot be inferred safely | Bootstrap and initialization remain separate phases |
| Daily workflow authority | Target repository files | Installed Skill may lag project-specific rules | Skill provides routing, not a competing source of truth |
| Cross-agent instruction authority | `AGENTS.md` is canonical; `CLAUDE.md` imports it | Codex reads `AGENTS.md` directly while Claude Code officially loads `CLAUDE.md` | One shared rule set without duplicated vendor files |
| Session memory | Repository artifacts are authoritative | Vendor memory and chat history are not portable or guaranteed | Handoffs must persist resume context in REQ/TECH/REVIEW and durable notes |

## Impact Boundaries

- Projects / modules: `template/`, Skill folder, root project knowledge, tests, and usage documentation.
- APIs: command-line arguments and exit codes only.
- Data model: none.
- Background jobs / queues: none.
- Config / secrets: none.
- Third-party services: canonical Git repository when remote source is used.
- Security and privacy: preserve local files; do not send project contents externally.
- Observability: concise action summary plus explicit conflict paths.

## Non-Goals

- This design does not implement semantic merging of Markdown instructions.
- This design does not initialize project-specific placeholders without user context.
- This design does not guarantee remote bootstrap when Git or network access is unavailable.
- This design does not add a release or auto-update mechanism.
- This design does not maintain a second Git branch solely for GitHub's template button.

## Open Decisions

| Question | Decision owner | Default recommendation | Deadline / blocking point |
|---|---|---|---|
| Should a future release embed a versioned template archive? | Maintainer | Revisit only if offline installation becomes a concrete requirement | Future release |

## Validation Plan

- Unit / contract: run script against temporary source and target directories.
- Integration: test local-source bootstrap, `--inspect`, state-directory presence, and first workflow artifact creation.
- Remote: avoid relying on network for required validation; local source exercises the same copy path.
- Skill: run `skill-creator/scripts/quick_validate.py`.
- Documentation: run `git diff --check`, placeholder scan scoped to new task files, and wiki-link checks.

## Architecture Writeback Checklist

- [[02-architecture/current-architecture-flow]]: update to describe payload, Skill, and validation flow.
- Related `05-reference/` notes: no runbook change required unless validation finds a reusable gotcha.
- Root and Chinese README: update installation and bootstrap examples.

## State History

| Date | State | Notes | Commit |
|---|---|---|---|
| 2026-06-18 | approved | Design decisions are resolved for implementation |  |
| 2026-06-18 | approved | Updated after review to separate canonical payload from repository maintenance |  |
