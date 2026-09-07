# Experience Promotion

## Candidate Flow

1. Run a Learning Check after validation and capture the lesson plus evidence in the active WORK experience table.
2. Verify it with code, commands, logs, official references, or repeated observation.
3. Search existing rules, notes, runbooks, and `project-skills/INDEX.md` for duplicates.
4. Choose the smallest canonical destination. For tracked or governed work, add a shared destination to `owned_paths` and check active WORK overlap.
5. Coordinate a single writer when another active task owns the destination; otherwise update it in place.
6. Write the rule, fact, procedure, no-op result, or non-promotion reason in the candidate row.
7. Run structural checks and a retrieval test when an important project Skill changes.

The flow must be idempotent: repeating it updates the same destination or records that the verified knowledge is already current. It must not create a second note, Skill directory, or index row. Deprecate and link superseded knowledge when replacement is safer than deletion. After current facts are promoted, retire historical bodies through the repository knowledge lifecycle. Update the task's individual open route with its source; closeout removes the route. Archive does not erase unresolved candidates or waive gates.

Direct work with no verified reusable lesson creates no artifact. If Direct work discovers a candidate that should change shared knowledge, re-route it to Tracked before writeback. The active WORK then owns the evidence and promotion decision.

Writeback is a task-branch Git diff, not hidden agent memory. Repository-wide instructions, architecture constraints, security or permission behavior, release procedures, and existing Skill contracts require the same evidence, review, and Governed gates as equivalent code or policy changes.

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

Keep the repository Skill portable: use the common `SKILL.md`, optional `references/`, and optional `scripts/` structure. Put host-specific activation or tool metadata in adapters.
