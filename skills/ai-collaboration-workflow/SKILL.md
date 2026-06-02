---
name: ai-collaboration-workflow
description: Use when working in a repository that uses the AI Collaboration Workflow Template, or when the user asks to initialize, maintain, or apply the template. Supports creating and updating REQ, TECH, and REVIEW documents; checking implementation readiness gates; recording validation; handling evidence-based review feedback; updating gotchas, architecture notes, and runbooks; and keeping AGENTS.md, CLAUDE.md, and zettelkasten/AI.md aligned.
---

# AI Collaboration Workflow

## Core Rule

Treat `AGENTS.md` as the canonical repository instruction file. Treat `zettelkasten/AI.md` as the knowledge-base entry point. Treat `CLAUDE.md` as a Claude Code adapter only; do not duplicate canonical rules there.

## First Context To Load

When using this workflow in an initialized project, read the smallest relevant set:

1. `AGENTS.md`
2. `zettelkasten/AI.md`
3. `zettelkasten/00-governance/ai-workflow.md`
4. `zettelkasten/06-requirements/README.md`
5. `zettelkasten/08-technical-designs/README.md`
6. `zettelkasten/07-review/README.md`
7. The specific REQ, TECH, REVIEW, architecture note, or runbook linked from the task

For initialization work, read `INIT.md` first and follow it exactly.

## Task Decision Tree

- **Initialize a project**: follow `INIT.md`; replace placeholders; rename `zettelkasten/{{PROJECT_NAME}}.md`; prune umbrella-only content if needed; create the first project-specific overview, quick reference, architecture flow, and validation runbook; delete `INIT.md`; run checks; commit.
- **New feature or non-trivial fix**: find or create a `REQ-YYYYMMDDHHMMSS-short-name.md` in `06-requirements/backlog/` or `in-progress/`.
- **Before business-code implementation**: confirm the linked `TECH-YYYYMMDDHHMMSS-short-name.md` is in `08-technical-designs/approved/`, or record a tiny-fix waiver in the REQ or REVIEW document.
- **Implementation handoff**: create or update `REVIEW-YYYYMMDDHHMMSS-short-name.md` in `07-review/pending/` with scope, commit, validation, worktree status, risks, next steps, and review focus.
- **Review feedback**: require evidence, verify independently, fix confirmed issues, reject unsupported issues with counter-evidence, then update the review document.
- **Memory writeback**: update `gotchas.md`, `current-architecture-flow.md`, `e2e-test.md`, workflow boards, or related notes when durable facts change.

## Creating Documents

Copy templates instead of inventing structure:

- Requirement: `zettelkasten/00-governance/templates/requirement.md`
- Technical design: `zettelkasten/00-governance/templates/technical-design.md`
- Review handoff: `zettelkasten/00-governance/templates/review.md`

Use timestamped names:

- `REQ-YYYYMMDDHHMMSS-short-name.md`
- `TECH-YYYYMMDDHHMMSS-short-name.md`
- `REVIEW-YYYYMMDDHHMMSS-short-name.md`

Keep document IDs stable when moving files between state directories.

## Implementation Readiness

Do not treat `06-requirements/in-progress/` as implementation approval. Implementation is ready only when:

- the REQ has clear goals, non-goals, context pack, impact, and acceptance criteria;
- the linked TECH is in `08-technical-designs/approved/`;
- open decisions that affect implementation are resolved or scoped out;
- validation expectations are explicit.

Tiny-fix waivers are acceptable only for low-risk changes that do not alter contracts, data, security, billing, permissions, persistence, deployment, or cross-module behavior.

## Validation

Use project-specific commands from:

- `zettelkasten/01-overview/quick-reference.md`
- `zettelkasten/05-reference/e2e-test.md`
- `zettelkasten/00-governance/validation-discipline.md`

Always record what ran, what passed or failed, and what remains untested. If validation cannot run, record the blocker and residual risk in the REVIEW document.

## Review Handling

Review feedback is a hypothesis until verified.

- Evidence can be code location, failing command, log excerpt, screenshot, commit, linked document, official source, or reproducible manual flow.
- Confirmed or partially confirmed feedback becomes fix work.
- Unsupported or false feedback should be rejected with counter-evidence.
- Do not start the next implementation slice until the current review is closed or explicitly waived.

## Final Checks

Before handoff or commit, run relevant checks:

- `git diff --check`
- scan for leftover placeholders: `rg '\{\{[A-Z_]+\}\}'`
- scan for stale vendor-specific links if entry files changed: `rg 'zettelkasten/CLAUDE|\\[\\[CLAUDE\\]\\]'`
- verify changed wiki links point to existing notes
- check `git status --short` for unrelated changes
