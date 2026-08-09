# Contributing

Contributions are welcome when they improve the template as a reusable AI project documentation workflow.

## Good Contributions

- clearer agent workflow rules;
- better WORK, project-Skill, or routing templates;
- generic examples that do not depend on a private project;
- validation or link-check scripts;
- documentation that helps users initialize the template in real repositories.

## Keep It Generic

Do not add private project details, customer names, real credentials, internal URLs, production logs, or business-specific assumptions. Use fictional examples such as `ExampleSaaS`.

This repository does not initialize a second root knowledge base. Keep the product and its maintenance material separate:

- keep the default downstream core under `template/` and explicit opt-in vendor overlays under `adapters/`;
- keep maintainer and publishing material under `docs/`;
- never copy repository-specific publishing, roadmap, or maintenance records into `template/`;
- validate the initialized output as well as the source repository with `python3 scripts/validate_distribution.py`.

## Change Checklist

- Name tracked and governed records `WORK-YYYYMMDDHHMMSS-short-name.md`.
- Keep work records at stable paths under `template/zettelkasten/work/`; represent state in frontmatter.
- Use a task branch for non-trivial work and a dedicated worktree for concurrent work.
- End each agent context that produces persistent changes, or each coherent slice, with a task-scoped commit; do not create empty commits for read-only analysis.
- Run `git diff --check`.
- Search for private project terms before submitting.
- Make sure non-placeholder wiki links resolve to files in `template/zettelkasten/`.

## Release Preparation

Keep the Quick Start tag, payload baseline, distribution validator version, and Companion Skill default ref aligned through the release helper:

```bash
python3 scripts/prepare_release.py --check
python3 scripts/prepare_release.py v4.3.0 --dry-run
python3 scripts/prepare_release.py v4.3.0
```

The helper changes only the known release-version anchors and fails if their shape or current values diverge. Review its diff, run `python3 scripts/validate_distribution.py`, and let `.github/workflows/validate.yml` repeat the distribution and official Skills CLI installation checks before tagging.

Model-routing claims need externally captured, fresh-session A/B evidence. Follow `docs/model-routing-evaluation.md`; never report a synthetic evaluator fixture as actual Agent quality or quota evidence.

## Commit Style

Use concise conventional-style commits:

- `docs: clarify review evidence rules`
- `docs: add project Skill example`
- `fix: align governed gate naming`
