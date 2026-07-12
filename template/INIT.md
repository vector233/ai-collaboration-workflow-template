# INIT.md — Initialize This Knowledge Base

> <EXTREMELY-IMPORTANT>
> This file is meant to be executed by an AI coding assistant. Follow the steps in order. Do not skip checks. Delete this file after initialization is complete.
> </EXTREMELY-IMPORTANT>

## 0. Trigger

The user says:

```text
Initialize this knowledge base by following INIT.md.
```

Then follow sections 1 through 6.

## 1. Placeholder Inventory

Replace every placeholder below:

| Placeholder | Meaning | Example |
|---|---|---|
| `{{PROJECT_NAME}}` | Project name for titles and prose | `ExampleSaaS` |
| `{{PROJECT_NAME_SAFE}}` | Project index filename without `.md`; replace spaces with underscores | `Example_SaaS` |
| `{{PROJECT_DESCRIPTION}}` | One-sentence project description | `Team workspace for collaborative project planning` |
| `{{TECH_STACK}}` | Short stack summary | `TypeScript · Next.js · PostgreSQL · Redis` |
| `{{REPO_TYPE}}` | `umbrella` or `single` | `umbrella` |
| `{{SUB_PROJECTS}}` | Umbrella only: Markdown table of subprojects | See example below |
| `{{DOMAINS}}` | Markdown table of domains and ports | See example below |
| `{{REPOS}}` | Markdown list of repositories | See example below |

Example `{{SUB_PROJECTS}}`:

```markdown
| Subproject | Path | Repository |
|---|---|---|
| Backend | backend/ | example-owner/foo-backend |
| Portal | portal/ | example-owner/foo-portal |
```

Example `{{DOMAINS}}`:

```markdown
| Environment | Domain / port |
|---|---|
| Production | foo.example.com |
| Local API | localhost:8080 |
```

Example `{{REPOS}}`:

```markdown
- example-owner/foo-backend
- example-owner/foo-portal
```

## 2. Ask The User

Ask these questions one at a time. If the user already provided an answer, skip that question.

1. What is the project name?
2. What is the one-sentence project description?
3. What is the main tech stack? List 3-6 items.
4. Is this an umbrella repository or a single-project repository?
5. If umbrella: what are the subprojects? Include name, path, and repository.
6. What are the main domains and local ports?
7. What Git repositories belong to the project?
8. What are the 2-3 most common local development or validation commands?

Format scattered answers into Markdown tables or lists before writing them into files.

## 3. Apply Replacements

### 3.1 Rename The Project Index

```bash
cd <repo-root>
PROJECT_NAME_SAFE="$(echo '<PROJECT_NAME>' | tr ' ' '_')"
mv 'zettelkasten/{{PROJECT_NAME}}.md' "zettelkasten/${PROJECT_NAME_SAFE}.md"
```

If the project name contains spaces, use underscores in the filename.

### 3.2 Replace Placeholders

Replace placeholders in all Markdown files under `zettelkasten/`:

- `{{PROJECT_NAME}}`
- `{{PROJECT_NAME_SAFE}}`
- `{{PROJECT_DESCRIPTION}}`
- `{{TECH_STACK}}`
- `{{DOMAINS}}`
- `{{REPOS}}`
- `{{REPO_TYPE}}`
- `{{SUB_PROJECTS}}`

Single-line values can be replaced mechanically:

```bash
find zettelkasten -type f -name '*.md' -exec \
  sed -i.bak \
    -e 's/{{PROJECT_NAME}}/<value>/g' \
    -e 's/{{PROJECT_NAME_SAFE}}/<filename-safe-value>/g' \
    -e 's/{{PROJECT_DESCRIPTION}}/<value>/g' \
    -e 's/{{TECH_STACK}}/<value>/g' \
    -e 's/{{REPO_TYPE}}/<umbrella-or-single>/g' \
    {} \;
find zettelkasten -name '*.bak' -delete
```

Use a normal file edit for multiline placeholders such as `{{DOMAINS}}`, `{{REPOS}}`, and `{{SUB_PROJECTS}}`. Do not use `sed` for multiline Markdown tables.

### 3.3 Handle Umbrella Or Single-Repo Mode

If `{{REPO_TYPE}} == single`:

```bash
rm -rf zettelkasten/04-cross-cutting
find zettelkasten -name '*.md' -exec \
  sed -i.bak '/<!-- UMBRELLA-ONLY/,/<!-- \/UMBRELLA-ONLY -->/d' {} \;
find zettelkasten -name '*.bak' -delete
```

If `{{REPO_TYPE}} == umbrella`, keep the umbrella-only content but remove the marker comments:

```bash
find zettelkasten -name '*.md' -exec \
  sed -i.bak \
    -e '/<!-- UMBRELLA-ONLY/d' \
    -e '/<!-- \/UMBRELLA-ONLY -->/d' \
    {} \;
find zettelkasten -name '*.bak' -delete
```

## 4. Generate First Project-Specific Notes

Rewrite these files with concrete content from the user's answers. Do not leave them as generic examples.

### 4.0 `AGENTS.md`

Keep the adaptive REQ/TECH/PLAN workflow, review rules, optional external Skill interoperability, validation discipline, and Git hygiene. Replace generic repository wording with project-specific structure, common commands, module boundaries, and any existing local agent rules. If the target already had an `AGENTS.md`, merge conservatively instead of discarding local instructions.

### 4.1 `zettelkasten/00-governance/project-overview.md`

Fill in project purpose, naming rules if relevant, tech stack, subprojects if umbrella, and project constraints.

### 4.2 `zettelkasten/CURRENT.md`

Initialize the current-state snapshot. If there is no active work yet, keep `None` rows and record the initial branch or worktree state if useful.

### 4.3 `zettelkasten/01-overview/quick-reference.md`

Fill in common commands, domains/ports, repositories, and any known local URLs.

### 4.4 `zettelkasten/01-overview/product-vision.md`

Write one paragraph describing the current product direction. Leave unknown market or pricing details as explicit TODOs.

### 4.5 `zettelkasten/02-architecture/current-architecture-flow.md`

Write the first current-architecture summary. If the project is not implemented yet, mark sections as planned or unknown instead of presenting assumptions as facts.

### 4.6 `zettelkasten/05-reference/e2e-test.md`

Fill in known validation commands. If no realistic environment validation exists yet, record that gap and its risk.

### 4.7 Other Files

Keep workflow files, templates, decisions, glossary, and gotchas generic. Replace placeholders only. The project can refine them later.

## 5. Self-Check

```bash
cd <repo-root>

if grep -rE '\{\{[A-Z_]+\}\}' zettelkasten/ 2>/dev/null; then
  echo "FAIL: placeholders remain"
else
  echo "OK: no placeholders"
fi

if grep -r 'UMBRELLA-ONLY' zettelkasten/ 2>/dev/null; then
  echo "FAIL: UMBRELLA-ONLY markers remain"
else
  echo "OK: no umbrella markers"
fi

test -f "zettelkasten/{{PROJECT_NAME}}.md" && echo "FAIL: project index not renamed" || echo "OK: project index renamed"

git diff --check
```

Fix any failure before continuing.

## 6. Finish

Delete this file:

```bash
rm -f .ai-collaboration-workflow-template
rm INIT.md
```

Run the workflow doctor after deleting the initialization files:

```bash
python3 scripts/workflow_doctor.py --strict
```

Fix any reported error before handoff.

If the user requested a commit, or repository instructions require one, create the first commit:

```bash
git add -A
git commit -m "chore: initialize knowledge base for <PROJECT_NAME>"
```

Otherwise report the initialized files and leave them uncommitted. After that, use `AGENTS.md` and `zettelkasten/AI.md` as the daily entry points.
