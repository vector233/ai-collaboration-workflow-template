# INIT.md - Initialize This Knowledge Layer

> Follow these steps in order. Delete this file only after all checks pass.

## 1. Discover Before Asking

Inspect the repository for its name, purpose, stack, commands, modules, default branch, existing Git policy, and existing agent instructions. Ask only for facts that cannot be discovered safely.

Required placeholders:

| Placeholder | Meaning |
|---|---|
| `{{PROJECT_NAME}}` | project name |
| `{{PROJECT_NAME_SAFE}}` | project-index filename without `.md` |
| `{{PROJECT_DESCRIPTION}}` | one-sentence description |
| `{{TECH_STACK}}` | short stack summary |
| `{{REPO_TYPE}}` | `umbrella` or `single` |
| `{{SUB_PROJECTS}}` | umbrella subproject table |
| `{{DOMAINS}}` | domains and ports table |
| `{{REPOS}}` | repository list |

Ask for missing facts one at a time. Distinguish confirmed facts from assumptions.

## 2. Replace And Rename

Replace placeholders in Markdown under `zettelkasten/`. Rename:

```bash
mv 'zettelkasten/{{PROJECT_NAME}}.md' 'zettelkasten/<PROJECT_NAME_SAFE>.md'
```

For a single repository, remove `zettelkasten/04-cross-cutting/` and all `UMBRELLA-ONLY` blocks. For an umbrella repository, retain the content and remove marker comments.

Do not replace generic workflow examples with invented project facts.

## 3. Write The Minimum Project Context

Rewrite these files with verified repository-specific content:

- `AGENTS.md`: merge existing instructions; keep Direct/Tracked/Governed routing, project-Skill promotion, Git isolation, context commits, validation, and cross-agent rules.
- `zettelkasten/00-governance/project-overview.md`: purpose, stack, modules, constraints.
- `zettelkasten/01-overview/quick-reference.md`: commands, ports, URLs, repository locations.
- `zettelkasten/01-overview/product-vision.md`: current product direction; mark unknowns.
- `zettelkasten/02-architecture/current-architecture-flow.md`: verified current or planned flow.
- `zettelkasten/05-reference/e2e-test.md`: known validation commands and realistic-environment gaps.
- `zettelkasten/00-governance/git-collaboration.md`: preserve stricter local branch, PR, and merge policies.

Set every maintained note's `last_verified_at` to the initialization date. Notes with `review_after_days` must have a concrete ISO date before strict validation.

Keep `project-skills/INDEX.md` empty unless the repository already has a verified repeatable procedure worth indexing. Do not invent initial Skills.

## 4. Confirm Stable Work Layout

The initialized project uses:

```text
zettelkasten/06-work/     stable WORK, TECH, PLAN, and REVIEW files
project-skills/           on-demand repository procedures
```

State is frontmatter. Files never move for status changes. Do not create empty work artifacts during initialization.

## 5. Configure Git Defaults

Determine the repository's default branch and record any project-specific policy in `AGENTS.md` and `git-collaboration.md`.

Default behavior when no stricter policy exists:

- tracked and governed tasks use `task/<work-id>-<slug>` branches;
- concurrent tasks use separate worktrees;
- each agent context or coherent slice ends with a task-scoped commit;
- incomplete checkpoint commits stay off the default branch.

Do not create a branch, worktree, or commit merely to initialize the template unless the user requested it or repository policy requires it.

## 6. Validate

```bash
if grep -rE '\{\{[A-Z_]+\}\}' zettelkasten/ 2>/dev/null; then
  echo 'FAIL: placeholders remain'
fi

if grep -r 'UMBRELLA-ONLY' zettelkasten/ 2>/dev/null; then
  echo 'FAIL: umbrella markers remain'
fi

git diff --check
```

Remove initialization files after checking links, required fields, project-Skill routing, concrete review dates, and the diff:

```bash
rm -f .ai-collaboration-workflow-template INIT.md
```

The optional companion Skill may automate the knowledge checks. Fix all failures. If repository policy requires a commit, commit only initialization changes with a concise conventional message. Otherwise leave the verified changes for the user.

After initialization, daily work starts from `AGENTS.md` and `zettelkasten/AI.md`. Read the branch-matched WORK only when the task needs durable state, and update it directly from the templates.
