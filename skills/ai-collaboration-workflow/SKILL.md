---
name: ai-collaboration-workflow
description: Initialize and operate Repo Continuity for new projects. Use when an agent needs to install the repository-owned knowledge layer; route work into Direct, Tracked, or Governed delivery; preserve, resume, or verify a stable WORK record across context boundaries; discover or idempotently promote repository experience into an on-demand project Skill; identify, sanitize, or prepare evidence-backed template feedback; isolate parallel Git work; use optional Codex specialist model routing; optionally automate knowledge checks and Markdown updates; or hand off durable project context across agents.
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

Use `--source <checkout-or-template>` for local or offline installation. The bootstrap copies missing files, skips identical files, and never overwrites differing repository files.

If `INIT.md` exists, follow it completely. Preserve stricter local rules, replace all placeholders, initialize only verified project facts, remove initialization files, and verify the knowledge links and required fields.

## Load Minimal Context

For initialized projects:

1. Read `AGENTS.md` and `zettelkasten/AI.md`.
2. Inspect the current Git branch and `zettelkasten/work/`.
3. Read the active `WORK-*` matching the assigned task or current branch, when one exists.
4. Read only linked knowledge, runbooks, and matching rows from `project-skills/INDEX.md`.

Do not scan all workflow artifacts or project Skills by default.

Repository Markdown and Git are sufficient. Do not require helper execution to understand or operate the workflow.

## Use Optional Helpers

Resolve this Skill directory as `SKILL_ROOT`. Use bundled helpers only when deterministic automation materially helps:

```bash
python3 "$SKILL_ROOT/scripts/workflow_doctor.py" --root <repo-root> --status
python3 "$SKILL_ROOT/scripts/workflow_task.py" new <slug> --root <repo-root>
(cd <repo-root> && python3 "$SKILL_ROOT/scripts/task_worktree.py" create <WORK-ID>)
```

The helpers read and write the same repository files and Git state. They are optional, own no hidden state, and must not become project requirements.

## Route The Task

Read [routing.md](references/routing.md) when classifying new work or reconsidering its route.

- **Direct**: no workflow artifact; validate and commit the current context.
- **Tracked**: create one stable `WORK-*` under `zettelkasten/work/`.
- **Governed**: use one `WORK-*` with explicit decisions, approvals, owners, evidence, and gates.

Use repository templates or the optional WORK helper. Keep artifact paths stable and update frontmatter status in place.

## Use Optional Codex Model Routing

When operating in Codex and the target has `.codex/agents/`, read [codex-model-routing.md](references/codex-model-routing.md) before delegating. The adapter assigns model and reasoning settings to narrow specialist roles; it never replaces the Direct/Tracked/Governed route, Git isolation, validation, or durable handoff contract.

## Isolate And Commit

Read [git-isolation.md](references/git-isolation.md) before starting tracked work, creating a branch or worktree, coordinating parallel agents, or handing off an incomplete context.

Tracked and governed work must not be implemented directly on the default branch. Concurrent tasks use separate worktrees. Every context that produces persistent changes, or each coherent slice, ends with a task-scoped commit; incomplete checkpoints stay on the task branch. Read-only contexts do not create empty commits.

## Preserve Context

Do not checkpoint every turn. Update the active WORK after each bounded Tracked or Governed slice and before an unfinished task crosses a handoff, long pause, agent or session switch, detectable context compaction, or any yield that would leave decisions only in chat. Direct work that completes, validates, and commits in the current context needs no WORK; otherwise re-route it to Tracked before yielding.

Persist the route, acceptance state, completed step and commit, exact validation, risks or unresolved decisions, next allowed action, and experience candidates. Optional vendor telemetry may signal context pressure, but never require it and never store project state outside the repository.

## Promote Experience

Read [experience-promotion.md](references/experience-promotion.md) when a task exposes a repeatable lesson, before closeout, or when creating/updating a project Skill.

Record candidates in the active work item first. Search all likely destinations, update the smallest canonical destination, and make repeated promotion a no-op rather than a duplicate. For tracked or governed work, declare shared destinations in `owned_paths` and coordinate a single writer. Create a project Skill only for a stable conditional procedure with concrete triggers, validation, and recovery. Update the existing `project-skills/INDEX.md` row so future agents can wake it without loading every Skill.

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
