# Contributing

Contributions are welcome when they improve the template as a reusable AI project documentation workflow.

## Good Contributions

- clearer agent workflow rules;
- better requirement, TECH, review, or assignment templates;
- generic examples that do not depend on a private project;
- validation or link-check scripts;
- documentation that helps users initialize the template in real repositories.

## Keep It Generic

Do not add private project details, customer names, real credentials, internal URLs, production logs, or business-specific assumptions. Use fictional examples such as `ExampleSaaS`.

## Change Checklist

- Keep naming rules consistent:
  - `REQ-YYYYMMDDHHMMSS-short-name.md`
  - `TECH-YYYYMMDDHHMMSS-short-name.md`
  - `REVIEW-YYYYMMDDHHMMSS-short-name.md`
- Run `git diff --check`.
- Search for private project terms before submitting.
- Make sure non-placeholder wiki links resolve to files in `zettelkasten/`.

## Commit Style

Use concise conventional-style commits:

- `docs: clarify review evidence rules`
- `docs: add assignment card example`
- `fix: align technical design naming`
