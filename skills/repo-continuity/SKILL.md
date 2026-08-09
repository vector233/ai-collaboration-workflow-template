---
name: repo-continuity
description: Initialize, inspect, safely reconcile upgrades for, and operate Repo Continuity. Use when an agent needs to install the repository-owned knowledge layer; produce a read-only three-way upgrade report or apply only conflict-free upstream changes without overwriting project customization; route work into Direct, Tracked, or Governed delivery; decompose a large requirement through an external Epic or one bounded local Initiative with independent child WORK records; preserve, resume, or verify stable work across context boundaries; run the evidence-backed Learning Check and idempotently promote repository experience into rules, knowledge, runbooks, or an on-demand project Skill; identify, sanitize, or prepare evidence-backed template feedback; isolate parallel Git work; use optional Codex or Claude Code specialist model routing; optionally automate knowledge checks and Markdown updates; or hand off durable project context across agents.
---

# Repo Continuity

## Authority

Treat the target repository as authoritative after installation:

- read `AGENTS.md` for mandatory rules;
- enter knowledge through `zettelkasten/AI.md`;
- use `zettelkasten/workflow.md` for routing;
- keep repository procedures in `project-skills/`;
- treat `CLAUDE.md` and other vendor files as adapters.

## Inspect Or Bootstrap

Resolve this Skill directory as `SKILL_ROOT`, then inspect:

```bash
python3 "$SKILL_ROOT/scripts/bootstrap_template.py" --target <repo-root> --inspect
```

If core files are missing and the user authorized installation, preview and bootstrap:

```bash
python3 "$SKILL_ROOT/scripts/bootstrap_template.py" --target <repo-root> --dry-run
python3 "$SKILL_ROOT/scripts/bootstrap_template.py" --target <repo-root>
```

The default bootstrap is core-only. Install model routing only after the user explicitly opts in:

```bash
python3 "$SKILL_ROOT/scripts/bootstrap_template.py" --target <repo-root> --with-model-routing codex --dry-run
python3 "$SKILL_ROOT/scripts/bootstrap_template.py" --target <repo-root> --with-model-routing codex
# Use `claude` or `all` instead when requested.
```

Use `--source <checkout-or-template>` for local or offline core installation. Model-routing opt-in requires the full checkout, or a direct template directory whose parent also contains `adapters/`. The bootstrap copies missing files, skips identical files, and never overwrites differing repository files.

If `INIT.md` exists, follow it completely. Preserve stricter local rules, replace all placeholders, initialize only verified project facts, remove initialization files, and verify the knowledge links and required fields.

## Reconcile An Upgrade

Treat an initialized project as three inputs: its recorded old upstream baseline, its current repository-owned customization, and the newer upstream release. Start with a read-only preview:

```bash
python3 "$SKILL_ROOT/scripts/bootstrap_template.py" --target <repo-root> --upgrade-report
python3 "$SKILL_ROOT/scripts/bootstrap_template.py" --target <repo-root> --upgrade-apply --dry-run
```

The report classifies files as added, unchanged, local-modified, upstream-modified, or both-modified and prints both sides of the diff. The apply preview maps them to concrete actions: add-upstream, apply-upstream, merge-clean, preserve-local, unchanged, pending-removal, or conflict.

Upgrade is a Tracked or Governed repository change. Create a task branch, record and commit the pre-upgrade WORK checkpoint, and require a clean worktree before applying:

```bash
python3 "$SKILL_ROOT/scripts/bootstrap_template.py" --target <repo-root> --upgrade-apply
```

The helper transactionally writes only upstream additions, upstream-only modifications, and clean text three-way merges. It preserves local-only changes. It does not delete a path removed upstream, overwrite a true conflict, follow target symlinks, run on `main` or `master`, or advance the `Template baseline`. A result with pending removals or conflicts exits with status 2 after applying the safe subset; resolve those paths deliberately in the same task branch.

Preserve project facts and stricter local policy, run repository validation, review the final Git diff, and only then update `Template baseline` in `zettelkasten/AI.md` to the target release and commit the upgrade. Do not re-add `INIT.md` or a payload marker to an initialized project. Use `--baseline-ref <tag>` if the recorded baseline is unavailable, `--json` for machine-readable output, and `--with-model-routing codex`, `claude`, or `all` only when the corresponding optional overlay should also be reconciled.

## Load Minimal Context

For initialized projects:

1. Read `AGENTS.md` and `zettelkasten/AI.md`.
2. Inspect the current Git branch and `zettelkasten/work/`.
3. Read the active `WORK-*` matching the assigned task or current branch, when one exists.
4. When that WORK declares a local `initiative_id`, read the Initiative only if a shared gate, dependency, or integration constraint affects the current slice. Do not load sibling WORK records by default.
5. Read only linked knowledge, runbooks, and matching rows from `project-skills/INDEX.md`.

Do not scan all workflow artifacts or project Skills by default.

Repository Markdown and Git are sufficient. Do not require helper execution to understand or operate the workflow.

## Use Optional Helpers

Resolve this Skill directory as `SKILL_ROOT`. Use bundled helpers only when deterministic automation materially helps:

```bash
python3 "$SKILL_ROOT/scripts/workflow_doctor.py" --root <repo-root> --status
python3 "$SKILL_ROOT/scripts/workflow_task.py" initiative-new <slug> --root <repo-root>
python3 "$SKILL_ROOT/scripts/workflow_task.py" new <slug> --root <repo-root>
(cd <repo-root> && python3 "$SKILL_ROOT/scripts/task_worktree.py" create <WORK-ID>)
```

The helpers read and write the same repository files and Git state. They are optional, own no hidden state, and must not become project requirements.

When a Tracked or Governed task reaches its Learning Check, the WORK helper can manage the same Markdown candidate table deterministically:

```bash
python3 "$SKILL_ROOT/scripts/workflow_task.py" learn-add <WORK-ID> \
  --candidate "<lesson>" --shape <shape> --evidence "<verified evidence>" --root <repo-root>
python3 "$SKILL_ROOT/scripts/workflow_task.py" learn-decide <WORK-ID> \
  --candidate "<lesson>" --decision <promoted|updated|no-op|not-promoted> \
  --destination "<repo-relative-path[; second-path]>" --reason "<result>" --root <repo-root>
python3 "$SKILL_ROOT/scripts/workflow_task.py" learn-status <WORK-ID> \
  --require-complete --root <repo-root>
```

Use `learn-none <WORK-ID> --reason "<why no verified lesson exists>"` when a Tracked or Governed task has no reusable lesson. The helper records decisions; the agent still judges relevance, writes the selected destination, and validates the result.

## Route The Task

Read [routing.md](references/routing.md) when classifying new work or reconsidering its route.

- **Direct**: no workflow artifact; validate and commit the current context.
- **Tracked**: create one stable `WORK-*` under `zettelkasten/work/`.
- **Governed**: use one `WORK-*` with explicit decisions, approvals, owners, evidence, and gates.

Use repository templates or the optional WORK helper. Keep artifact paths stable and update frontmatter status in place.

## Decompose Large Requirements

Read [routing.md](references/routing.md) before treating a large request as one WORK. Keep one WORK for a tightly coupled acceptance and rollback boundary. Split independently acceptable, assignable, testable, reversible, or releasable outcomes into separate child WORK records.

Prefer the existing project-native Epic, Issue, or Milestone and set `external_parent` in each child. If no suitable external coordination authority exists, create one thin local `INITIATIVE-*` from `zettelkasten/templates/initiative.md` and set its ID as each child's `initiative_id`. Never set both. The only local hierarchy is Initiative -> WORK; do not create recursive Initiatives or parent-WORK trees.

The Initiative is not branch-bound implementation state. Keep only the overall goal, cross-child acceptance, shared decisions or gates, integration order, derived rollup, and next coordination action there. Each child owns its own route, branch or worktree, acceptance, dependencies, validation, checkpoint, Learning Check, and closure. Record ordering through `depends_on`, keep child membership canonical in WORK frontmatter, and update Initiative coordination serially rather than making parallel children concurrent writers of the parent.

## Use Optional Model-Routing Adapters

Do not install model routing by default. When the user explicitly requests it, rerun the bootstrap with `--with-model-routing codex`, `claude`, or `all`; preview first and preserve differing local files as conflicts. The overlays configure only narrow specialist roles and leave the root-session model unchanged.

When operating in Codex and the target has `.codex/agents/`, read [codex-model-routing.md](references/codex-model-routing.md) before delegating. When operating in Claude Code and the target has `.claude/agents/`, read [claude-model-routing.md](references/claude-model-routing.md). Neither adapter replaces the Direct/Tracked/Governed route, Git isolation, validation, or durable handoff contract. If an adapter is absent, continue with the root agent.

## Isolate And Commit

Read [git-isolation.md](references/git-isolation.md) before starting tracked work, creating a branch or worktree, coordinating parallel agents, or handing off an incomplete context.

Tracked and governed work must not be implemented directly on the default branch. Concurrent tasks use separate worktrees. Every context that produces persistent changes, or each coherent slice, ends with a task-scoped commit; incomplete checkpoints stay on the task branch. Read-only contexts do not create empty commits.

## Preserve Context

Do not checkpoint every turn. Update the active WORK after each bounded Tracked or Governed slice and before an unfinished task crosses a handoff, long pause, agent or session switch, detectable context compaction, or any yield that would leave decisions only in chat. Direct work that completes, validates, and commits in the current context needs no WORK; otherwise re-route it to Tracked before yielding.

Persist the route, acceptance state, completed step and commit, exact validation, risks or unresolved decisions, next allowed action, and experience candidates. Optional vendor telemetry may signal context pressure, but never require it and never store project state outside the repository.

## Close With The Learning Loop

Read [experience-promotion.md](references/experience-promotion.md) when a task exposes a repeatable lesson, before closeout, or when creating/updating a project Skill.

After validation, run a lightweight Learning Check before completing every task. Direct work with no verified candidate creates no artifact. If Direct work exposes a reusable lesson that should change shared knowledge, re-route it to Tracked before writeback. For Tracked and Governed work, record candidates and evidence in the active work item first.

Search all likely destinations, update the smallest canonical destination, and make repeated promotion a no-op rather than a duplicate. Declare shared destinations in `owned_paths` and coordinate a single writer. Create a project Skill only for a stable conditional procedure with concrete triggers, validation, and recovery. Update the existing `project-skills/INDEX.md` row so future agents can wake it without loading every Skill.

All writeback is a reviewable task-branch Git diff. Do not use vendor memory or chat history as the durable destination, and do not silently change repository-wide instructions, architecture, security, permission, release, or existing Skill contracts without the evidence and review or Governed gates that an equivalent repository change requires.

## Improve The Template

Read [template-feedback.md](references/template-feedback.md) after a user corrects workflow behavior, when repeatable template friction has evidence, or when the user asks to prepare feedback for the upstream template.

Classify project lessons separately from template-wide and vendor-specific observations. Record nothing for normal tasks or one-off model mistakes. Keep observations local until the user explicitly approves a sanitized upstream report, Issue, or PR.

## Validate And Hand Off

Run relevant project checks and `git diff --check`. When workflow knowledge or project Skills changed, optionally run:

```bash
python3 "$SKILL_ROOT/scripts/workflow_doctor.py" --root <repo-root> --strict
```

Update the active work checkpoint with the commit reference, exact validation, risks, worktree status, and next allowed action before yielding.

Use a Fresh-Agent Resume Probe only for important multi-context handoffs, after changing resume semantics, or before a release where failed recovery is costly. A real probe uses an agent with no prior chat and records unedited run provenance; a synthetic expected response tests only the evaluator. The core path still requires no helper.

Do not claim validation that did not run. Do not stage unrelated user changes. Do not close work while experience candidates remain undecided.
