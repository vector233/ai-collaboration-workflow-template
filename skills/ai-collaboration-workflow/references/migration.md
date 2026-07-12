# Stable Work-Item Migration

Use this guide when a project contains `zettelkasten/CURRENT.md`, `06-requirements/`, `07-review/`, `08-technical-designs/`, or `09-implementation-plans/`.

1. Finish or checkpoint active legacy work before migration.
2. Create `zettelkasten/06-work/` and copy each active artifact into it without changing its stable ID.
3. Convert the primary active REQ into a WORK document, merging current-state, validation, review, and rule-promotion data.
4. Keep separate TECH, PLAN, or REVIEW files only when they still have an independent lifecycle.
5. Update links to stable `06-work/<ID>` targets.
6. Remove `CURRENT.md` only after its unique state is present in WORK checkpoints.
7. Remove empty legacy state directories after all links and boards are migrated.
8. Add `project-skills/INDEX.md` without inventing Skills.
9. Run the doctor in strict mode and commit migration separately from product work.

Do not mix old moving-state paths and new stable paths for one active task. Bootstrap never overwrites differing files, so migrate repository-specific content deliberately.
