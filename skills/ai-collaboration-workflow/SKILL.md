---
name: ai-collaboration-workflow
description: Guide AI-assisted project work with the AI Collaboration Workflow Template. Use when Codex or another coding agent needs to install or initialize the template; create a REQ and choose whether standalone TECH or PLAN artifacts are needed; create or close REVIEW handoffs; check implementation readiness; run the workflow doctor; record validation; evaluate review feedback; run the Rule Promotion Check; write durable lessons back; or integrate an external process Skill such as Superpowers without creating parallel project state.
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

- **Missing or incomplete**: core files are absent. Bootstrap before creating workflow artifacts.
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
3. `zettelkasten/CURRENT.md`
4. `zettelkasten/00-governance/ai-workflow.md`
5. The relevant requirement, technical design, implementation plan, review handoff, architecture note, or runbook
6. The workflow README for any state being changed

Read subproject-specific `AGENTS.md`, `CLAUDE.md`, or module notes before editing that subproject.

## Apply The Daily Workflow

Use the target repository's templates instead of inventing document structures:

- Requirement: `zettelkasten/00-governance/templates/requirement.md`
- Technical design: `zettelkasten/00-governance/templates/technical-design.md`
- Implementation plan: `zettelkasten/00-governance/templates/implementation-plan.md`
- Review handoff: `zettelkasten/00-governance/templates/review.md`

Use timestamped names and keep IDs stable when moving files:

- `REQ-YYYYMMDDHHMMSS-short-name.md`
- `TECH-YYYYMMDDHHMMSS-short-name.md`
- `PLAN-YYYYMMDDHHMMSS-short-name.md`
- `REVIEW-YYYYMMDDHHMMSS-short-name.md`

Route work as follows:

- **Task weight**: classify work as tiny, bounded, standard, or complex. Use the lightest workflow path that preserves safety and resumability.
- **Tracked feature or fix**: find or create a REQ and record the delivery-path decision.
- **Standalone TECH**: require it for architecture, API, schema, persistence, security, billing, permission, deployment, third-party, cross-module, migration, or unresolved technical decisions. Otherwise complete inline technical readiness in the REQ.
- **Standalone PLAN**: require it for dependent slices, multi-session or multi-agent work, cross-repository coordination, migration or release sequencing, or explicit ownership and checkpoints. Otherwise keep sufficient implementation slices in the REQ.
- **Before business-code edits**: require every artifact selected by the REQ to be ready: TECH in `approved/`, PLAN with `status: ready`, or complete inline readiness and slices.
- **Implementation slice complete**: create or update a REVIEW with scope, validation, worktree state, risks, and review focus.
- **Review feedback**: treat it as a hypothesis; require evidence, verify independently, fix confirmed issues, and record counter-evidence for rejected findings.
- **Rule Promotion Check**: before handoff or closeout for a long-running task, bug fix, review fix, or repeated failure mode, decide whether a lesson should become a durable project rule.
- **Durable learning**: update `AGENTS.md`, architecture notes, `gotchas.md`, validation runbooks, decisions, and workflow boards when the Rule Promotion Check or changed facts require it.
- **Workflow doctor**: after workflow-state changes, run `python3 scripts/workflow_doctor.py` and fix reported errors before handoff.
- **Current state**: update `zettelkasten/CURRENT.md` when active work, open review state, validation status, or next allowed action changes.
- **Next slice**: wait until the current review is closed or explicitly waived.

Do not treat a REQ in `in-progress/` as implementation approval. Check its selected delivery path. Do not claim validation that did not run.

Promote a lesson when it is likely to recur and can be written as a clear "must", "never", "prefer", or "check before" rule. Use `AGENTS.md` only when every future agent must obey the rule before touching the repo. Use `gotchas.md` for bug roots and false assumptions, architecture or cross-cutting notes for invariants, `05-reference/e2e-test.md` or `01-overview/quick-reference.md` for setup and validation commands, and `00-governance/decisions.md` for accepted decisions. Do not promote one-off observations or low-confidence guesses; leave those in the current REQ or REVIEW.

## Interoperate With External Process Skills

External process Skills are optional. Never make Superpowers or another plugin a prerequisite for using this workflow.

When an external Skill is present or invoked:

1. Read `zettelkasten/00-governance/external-skill-interoperability.md`.
2. Keep the repository REQ and selected TECH, PLAN, and REVIEW artifacts canonical.
3. Map brainstorming output into the active REQ and a standalone TECH only when the REQ requires one.
4. Map detailed planning into a required PLAN or the REQ implementation slices.
5. Map TDD, debugging, execution, verification, and review evidence into the current REVIEW and durable gotcha or runbook notes.
6. Run the Rule Promotion Check before treating external Skill output as complete.
7. Do not create `docs/superpowers/specs/`, `docs/superpowers/plans/`, or another parallel workflow tree unless the user explicitly requests an export.
8. Treat an approved TECH or complete inline technical readiness as satisfying an external design gate. Treat a ready PLAN or sufficient REQ slices as satisfying an external planning gate.
9. Follow repository Git rules instead of an external Skill's default commit, branch, or worktree behavior.

If no external process Skill is installed, ignore this section and apply the daily workflow unchanged.

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

Before closing the handoff, complete the REVIEW's Rule Promotion Check and either write the promoted rule to the selected durable destination or record why promotion is not applicable.

When workflow files, requirements, technical designs, implementation plans, review handoffs, wiki links, or initialization state changed, run:

```bash
python3 scripts/workflow_doctor.py
```

Use `--strict` after initialization or when warnings should fail the handoff.
