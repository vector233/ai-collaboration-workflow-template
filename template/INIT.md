# INIT.md - Initialize This Knowledge Layer

> Follow these steps in order. Delete this file only after all checks pass.

## 1. Discover Before Asking

Inspect the repository for its name, purpose, stack, commands, modules, default branch, existing Git policy, and existing agent instructions. Ask only for facts that cannot be discovered safely.

Required placeholders:

| Placeholder | Meaning |
|---|---|
| `{{PROJECT_NAME}}` | project name |
| `{{PROJECT_DESCRIPTION}}` | one-sentence description |
| `{{TECH_STACK}}` | short stack summary |
| `{{DOMAINS}}` | domains and ports table |
| `{{REPOS}}` | repository list |

Ask for missing facts one at a time. Distinguish confirmed facts from assumptions.

## 2. Replace Placeholders

Replace placeholders in Markdown under `zettelkasten/`.

Do not replace generic workflow examples with invented project facts.

## 3. Write The Minimum Project Context

Rewrite these files with verified repository-specific content:

- `AGENTS.md`: merge existing instructions; keep Direct/Tracked/Governed routing, context preservation, the evidence-backed Learning Loop and idempotent experience promotion, Git isolation, context commits, validation, and cross-agent rules.
- `zettelkasten/project.md`: purpose, stack, modules, constraints.
- `zettelkasten/quick-reference.md`: commands, ports, URLs, repository locations.
- `zettelkasten/architecture.md`: verified current or planned flow.
- `zettelkasten/validation-runbook.md`: known validation commands and realistic-environment gaps.
- `zettelkasten/git-collaboration.md`: preserve stricter local branch, PR, and merge policies.

`zettelkasten/AI.md` may be adapted to the project, but its baseline line is a machine-parsed contract, not prose. Keep the literal `Template baseline:` prefix and the backticked version:

```text
Template baseline: `v4.4.1` (`canonical-payload-v4`).
```

Trailing detail such as an initialization date may be appended. Rewording the prefix — for example to `Repo Continuity baseline:` — leaves the repository unable to resolve its own baseline, so every later upgrade fails until it is passed by hand with `--baseline-ref`.

Set every maintained note's `last_verified_at` to the initialization date. Notes with `review_after_days` must have a concrete ISO date before strict validation.

Keep `project-skills/INDEX.md` empty unless the repository already has a verified repeatable procedure worth indexing. Do not invent initial Skills.

## 4. Confirm Stable Work Layout

The initialized project uses:

```text
zettelkasten/work/        stable WORK files
project-skills/           on-demand repository procedures
```

State is frontmatter. Files never move for status changes. Do not create empty work artifacts during initialization.

## 5. Configure Git Defaults

Determine the repository's default branch and record any project-specific policy in `AGENTS.md` and `git-collaboration.md`.

Default behavior when no stricter policy exists:

- tracked and governed tasks use `task/<work-id>` branches;
- concurrent tasks use separate worktrees;
- each agent context or coherent slice ends with a task-scoped commit;
- incomplete checkpoint commits stay off the default branch.

Do not create a branch, worktree, or commit merely to initialize the template unless the user requested it or repository policy requires it.

## 6. Validate

```bash
if grep -rE '\{\{[A-Z_]+\}\}' zettelkasten/ 2>/dev/null; then
  echo 'FAIL: placeholders remain'
fi

git diff --check
```

Remove initialization files after checking links, required fields, project-Skill routing, concrete review dates, and the diff:

```bash
rm -f .repo-continuity-template .ai-collaboration-workflow-template INIT.md
```

The optional companion Skill may automate the knowledge checks. Fix all failures. If repository policy requires a commit, commit only initialization changes with a concise conventional message. Otherwise leave the verified changes for the user.

After initialization, daily work starts from `AGENTS.md` and `zettelkasten/AI.md`. Read the branch-matched WORK only when the task needs durable state, and update it directly from the templates.
