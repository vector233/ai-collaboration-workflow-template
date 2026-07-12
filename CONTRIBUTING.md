# Contributing

Contributions are welcome when they improve the template as a reusable AI project documentation workflow.

## Good Contributions

- clearer agent workflow rules;
- better WORK, optional TECH/PLAN/REVIEW, project-Skill, or routing templates;
- generic examples that do not depend on a private project;
- validation or link-check scripts;
- documentation that helps users initialize the template in real repositories.

## Keep It Generic

Do not add private project details, customer names, real credentials, internal URLs, production logs, or business-specific assumptions. Use fictional examples such as `ExampleSaaS`.

This repository does not initialize a second root knowledge base. Keep the product and its maintenance material separate:

- keep downstream files under `template/`;
- keep maintainer and publishing material under `docs/`;
- never copy repository-specific publishing, roadmap, or maintenance records into `template/`;
- validate the initialized output as well as the source repository with `python3 scripts/validate_distribution.py`.

## Change Checklist

- Keep naming rules consistent:
  - `WORK-YYYYMMDDHHMMSS-short-name.md`
  - `TECH-YYYYMMDDHHMMSS-short-name.md`
  - `PLAN-YYYYMMDDHHMMSS-short-name.md`
  - `REVIEW-YYYYMMDDHHMMSS-short-name.md`
- Keep workflow artifacts at stable paths under `template/zettelkasten/06-work/`; represent state in frontmatter.
- Use a task branch for non-trivial work and a dedicated worktree for concurrent work.
- End each agent context or coherent slice with a task-scoped commit.
- Run `git diff --check`.
- Search for private project terms before submitting.
- Make sure non-placeholder wiki links resolve to files in `template/zettelkasten/`.

## Commit Style

Use concise conventional-style commits:

- `docs: clarify review evidence rules`
- `docs: add project Skill example`
- `fix: align technical design naming`
