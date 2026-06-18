---
name: ai-collaboration-workflow
description: Guide AI-assisted project work with the AI Collaboration Workflow Template. Use when Codex or another coding agent needs to install or initialize the template in a repository; create, advance, or close REQ, TECH, and REVIEW documents; check implementation readiness; record validation; evaluate review feedback with evidence; or write durable lessons back to architecture notes, gotchas, and runbooks.
---

# AI Collaboration Workflow

## Authority

After the template is present, treat the target repository as authoritative:

- Read `AGENTS.md` for repository-wide rules.
- Enter project knowledge through `zettelkasten/AI.md`.
- Follow `zettelkasten/00-governance/ai-workflow.md` for task gates.
- Treat `CLAUDE.md` as an adapter; keep canonical rules in `AGENTS.md`.
- Prefer target-repository rules over this Skill when they differ.

## Classify Repository State

Before creating workflow artifacts, inspect the target repository. Resolve this Skill's directory as `SKILL_ROOT`, then run:

```bash
python3 "$SKILL_ROOT/scripts/bootstrap_template.py" --target <repo-root> --inspect
```

Classify the result:

- **Missing or incomplete**: core files are absent. Bootstrap before creating REQ, TECH, or REVIEW documents.
- **Present, not initialized**: `INIT.md` exists or template placeholders remain. Continue initialization.
- **Initialized**: core files exist, `INIT.md` is absent, and placeholder checks pass. Apply the daily workflow.

Do not recreate the template structure from memory.

## Bootstrap A Missing Template

If the user asked to install or initialize the workflow, proceed. If the user requested another task and bootstrap would add files unexpectedly, obtain permission first.

Preview the bootstrap:

```bash
python3 "$SKILL_ROOT/scripts/bootstrap_template.py" \
  --target <repo-root> \
  --dry-run
```

Run it after reviewing the plan:

```bash
python3 "$SKILL_ROOT/scripts/bootstrap_template.py" \
  --target <repo-root>
```

The default source is the canonical Git repository; the script selects its `template/` payload. For offline or development use, supply either the repository checkout or the payload directory directly:

```bash
python3 "$SKILL_ROOT/scripts/bootstrap_template.py" \
  --target <repo-root> \
  --source <repository-checkout-or-template-directory>
```

Interpret exit codes:

- `0`: bootstrap or inspection succeeded.
- `1`: source, Git, or filesystem operation failed.
- `2`: the target is incomplete or differing files were left untouched.

The script copies missing files and skips identical files. It never overwrites a differing file. For every reported conflict:

1. Read the target file and corresponding template source.
2. Preserve repository-specific instructions.
3. Merge only applicable template guidance.
4. Remove no local rule unless the user explicitly approves it.
5. Rerun `--inspect`.

If remote access fails, use `--source` with a local checkout or ask the user to provide one.

## Initialize The Copied Template

After bootstrap, read and follow `<repo-root>/INIT.md` exactly.

- Ask only for facts not already discoverable from the repository.
- Ask initialization questions one at a time.
- Distinguish confirmed facts from assumptions.
- Replace all placeholders and rename the project index.
- Handle single-repository versus umbrella mode.
- Rewrite the first project overview, quick reference, product vision, architecture flow, and validation runbook with concrete content.
- Preserve existing project instructions while integrating the workflow.
- Delete `INIT.md` only after every initialization check passes.
- Commit only if the user requested a commit or the active repository instructions explicitly require it.

## Load The Smallest Context Pack

For initialized projects, read:

1. `AGENTS.md`
2. `zettelkasten/AI.md`
3. `zettelkasten/00-governance/ai-workflow.md`
4. The relevant requirement, technical design, review handoff, architecture note, or runbook
5. The workflow README for any state being changed

Read subproject-specific `AGENTS.md`, `CLAUDE.md`, or module notes before editing that subproject.

## Apply The Daily Workflow

Use the target repository's templates instead of inventing document structures:

- Requirement: `zettelkasten/00-governance/templates/requirement.md`
- Technical design: `zettelkasten/00-governance/templates/technical-design.md`
- Review handoff: `zettelkasten/00-governance/templates/review.md`

Use timestamped names and keep IDs stable when moving files:

- `REQ-YYYYMMDDHHMMSS-short-name.md`
- `TECH-YYYYMMDDHHMMSS-short-name.md`
- `REVIEW-YYYYMMDDHHMMSS-short-name.md`

Route work as follows:

- **New feature or non-trivial fix**: find or create a REQ and link a TECH.
- **Before business-code edits**: require the TECH in `approved/`, unless a documented tiny-fix waiver applies.
- **Implementation slice complete**: create or update a REVIEW with scope, validation, worktree state, risks, and review focus.
- **Review feedback**: treat it as a hypothesis; require evidence, verify independently, fix confirmed issues, and record counter-evidence for rejected findings.
- **Durable learning**: update architecture notes, `gotchas.md`, validation runbooks, and workflow boards.
- **Next slice**: wait until the current review is closed or explicitly waived.

Do not treat a REQ in `in-progress/` as implementation approval. Do not claim validation that did not run.

## Validate And Hand Off

Use project-specific commands from:

- `zettelkasten/01-overview/quick-reference.md`
- `zettelkasten/05-reference/e2e-test.md`
- `zettelkasten/00-governance/validation-discipline.md`

Before handoff, run the smallest relevant checks and record exact results. At minimum for documentation changes:

```bash
git diff --check
rg '\{\{[A-Z_]+\}\}' zettelkasten
git status --short
```

Verify changed wiki links resolve. Record blockers and residual risk rather than implying unperformed coverage.
