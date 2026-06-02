---
name: ai-collaboration-workflow
description: Use when working in a repository that uses the AI Collaboration Workflow Template, when the user asks to initialize, install, maintain, or apply the template, or when the current project lacks the template and needs bootstrapping before REQ/TECH/REVIEW work. Supports installing template files into the current repo; creating and updating REQ, TECH, and REVIEW documents; checking implementation readiness gates; recording validation; handling evidence-based review feedback; updating gotchas, architecture notes, and runbooks; and keeping AGENTS.md, CLAUDE.md, and zettelkasten/AI.md aligned.
---

# AI Collaboration Workflow

## Core Rule

Treat `AGENTS.md` as the canonical repository instruction file. Treat `zettelkasten/AI.md` as the knowledge-base entry point. Treat `CLAUDE.md` as a Claude Code adapter only; do not duplicate canonical rules there.

## Template Presence Check

Before creating REQ, TECH, REVIEW, or writeback documents, check whether the current project already has the template installed.

Required core files:

- `AGENTS.md`
- `CLAUDE.md`
- `INIT.md` or an already-initialized `zettelkasten/AI.md`
- `zettelkasten/00-governance/ai-workflow.md`
- `zettelkasten/06-requirements/README.md`
- `zettelkasten/08-technical-designs/README.md`
- `zettelkasten/07-review/README.md`

If these files are missing, stop the requested workflow and bootstrap the template first. Do not invent REQ/TECH/REVIEW structure from memory when the template can be installed.

## Bootstrap Missing Template

When the current repo lacks the template and the user asks to use this skill, offer to install the template files into the current project. If the user already asked to initialize or install the workflow, proceed.

Use a temporary clone and copy only the template runtime files:

```bash
tmpdir="$(mktemp -d)"
git clone --depth 1 https://github.com/vector233/ai-collaboration-workflow-template "$tmpdir"
cp "$tmpdir/AGENTS.md" .
cp "$tmpdir/CLAUDE.md" .
cp "$tmpdir/INIT.md" .
cp -R "$tmpdir/zettelkasten" .
rm -rf "$tmpdir"
```

If any target file already exists, inspect it first and merge conservatively instead of overwriting user content. For existing projects, preserve local rules and add template guidance around them.

After copying, follow `INIT.md` to initialize placeholders, project metadata, first notes, and checks. Delete `INIT.md` only when initialization is complete.

## First Context To Load

When using this workflow in an initialized project, read the smallest relevant set:

1. `AGENTS.md`
2. `zettelkasten/AI.md`
3. `zettelkasten/00-governance/ai-workflow.md`
4. `zettelkasten/06-requirements/README.md`
5. `zettelkasten/08-technical-designs/README.md`
6. `zettelkasten/07-review/README.md`
7. The specific REQ, TECH, REVIEW, architecture note, or runbook linked from the task

For initialization or bootstrap work, read `INIT.md` first and follow it exactly after the template files are present.

## Task Decision Tree

- **Template missing**: bootstrap template files first, then follow `INIT.md`.
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
