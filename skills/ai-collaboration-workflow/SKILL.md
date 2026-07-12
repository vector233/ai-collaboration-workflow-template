---
name: ai-collaboration-workflow
description: Initialize and operate the AI Collaboration Workflow knowledge layer. Use when an agent needs to install or migrate the template; route a task into Direct, Tracked, or Governed work; create or resume stable WORK/TECH/PLAN/REVIEW artifacts; discover or promote repository experience into an on-demand project Skill; isolate parallel tasks with branches or Git worktrees; enforce per-context commits; validate workflow state; or hand off durable project knowledge across agents.
---

# AI Collaboration Workflow

## Authority

Treat the target repository as authoritative after installation:

- read `AGENTS.md` for mandatory rules;
- enter knowledge through `zettelkasten/AI.md`;
- use `zettelkasten/00-governance/ai-workflow.md` for routing;
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

If `INIT.md` exists, follow it completely. Preserve stricter local rules, replace all placeholders, initialize only verified project facts, remove initialization files, and run the doctor in strict mode.

If legacy `CURRENT.md`, moving-state REQ directories, or separate review/design/plan state trees exist, read [migration.md](references/migration.md) before creating new artifacts. Do not run both state models for the same task.

## Load Minimal Context

For initialized projects:

1. Read `AGENTS.md` and `zettelkasten/AI.md`.
2. Run `python3 scripts/workflow_doctor.py --status`.
3. Read the active `WORK-*` matching the assigned task or current branch.
4. Read only linked knowledge, runbooks, and matching rows from `project-skills/INDEX.md`.

Do not scan all workflow artifacts or project Skills by default.

## Route The Task

Read [routing.md](references/routing.md) when classifying new work or reconsidering its route.

- **Direct**: no workflow artifact; validate and commit the current context.
- **Tracked**: create one stable `WORK-*` under `zettelkasten/06-work/`.
- **Governed**: use a `WORK-*` and add only independently justified TECH, PLAN, or REVIEW artifacts.

Use repository templates. Keep artifact paths stable and update frontmatter status in place.

## Isolate And Commit

Read [git-isolation.md](references/git-isolation.md) before starting tracked work, creating a branch or worktree, coordinating parallel agents, or handing off an incomplete context.

Tracked and governed work must not be implemented directly on the default branch. Concurrent tasks use separate worktrees. Every agent context or coherent slice ends with a task-scoped commit; incomplete checkpoints stay on the task branch.

## Promote Experience

Read [experience-promotion.md](references/experience-promotion.md) when a task exposes a repeatable lesson, before closeout, or when creating/updating a project Skill.

Record candidates in the active work item first. Promote each candidate to the smallest durable destination. Create a project Skill only for a stable conditional procedure with concrete triggers, validation, and recovery. Update `project-skills/INDEX.md` so future agents can wake it without loading every Skill.

## Validate And Hand Off

Run relevant project checks, then:

```bash
python3 scripts/workflow_doctor.py
git diff --check
git status --short
```

Use `--strict` after initialization, migration, workflow changes, or project-Skill changes. Update the active work checkpoint with the commit, exact validation, risks, worktree status, and next allowed action before yielding.

Do not claim validation that did not run. Do not stage unrelated user changes. Do not close work while experience candidates remain undecided.
