# Experience Promotion

## Candidate Flow

1. Capture the lesson in the active WORK experience table.
2. Verify it with code, commands, logs, official references, or repeated observation.
3. Search existing rules, notes, runbooks, and `project-skills/INDEX.md` for duplicates.
4. Choose the smallest durable destination.
5. Write the rule, fact, procedure, or non-promotion reason.
6. Run the doctor and a retrieval test when a project Skill changes.

## Destination

| Lesson | Destination |
|---|---|
| repository-wide must/never/check-before | `AGENTS.md` |
| root cause or false assumption | `zettelkasten/gotchas.md` |
| architecture invariant | `zettelkasten/architecture.md` or a linked domain note |
| simple setup or validation sequence | quick reference or runbook |
| conditional multi-step procedure | `project-skills/<name>/SKILL.md` and `project-skills/INDEX.md` |
| evidence-backed workflow-template friction | use the template feedback workflow and record a local workflow observation |

## Project Skill Gate

Require a stable trigger, likely reuse or high failure impact, verified assumptions, observable validation, and safe recovery. Do not create a Skill for one-off detail, guesses, duplicated docs, or generic advice.

Keep Skill YAML frontmatter to `name` and `description`. Make the description include concrete trigger situations. Include Use, Do Not Use, Procedure, Validation, Recovery, and Provenance sections.

Mark stale Skills `needs-verification` in the index. Deprecate superseded Skills and route to the replacement.
