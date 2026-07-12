---
title: Project Skill Lifecycle
status: active
project: {{PROJECT_NAME}}
last_verified_at: YYYY-MM-DD
source_of_truth: project
review_after_days: 180
related:
  - "[[00-governance/ai-workflow]]"
  - "[[00-governance/gotchas]]"
  - "[[06-work/README]]"
---

# Project Skill Lifecycle

## Purpose

Project Skills preserve repeatable procedures and load them only when their trigger matches. They complement rules, facts, and runbooks; they do not replace them.

## Promotion Gate

Create or update a project Skill only when all are true:

- the procedure is specific enough to execute;
- it is likely to recur or has high failure impact;
- its assumptions have been verified;
- it needs more than a short rule or command;
- it has observable validation and a recovery path.

Do not promote story-specific implementation detail, temporary incidents, guesses, duplicated documentation, or generic coding advice.

## Lifecycle

1. Record a candidate in the active `WORK-*`.
2. Check existing entries in `project-skills/INDEX.md` and update instead of duplicating.
3. Copy [[00-governance/templates/project-skill]] to `project-skills/<skill-name>/SKILL.md`.
4. Keep Skill frontmatter limited to `name` and `description`; the description must contain concrete triggers.
5. Add use, non-use, procedure, validation, recovery, and provenance sections.
6. Add or update the compact routing row in `project-skills/INDEX.md`, including status, verification date, and review interval.
7. Check the Skill structure, index routing, trigger uniqueness, links, and verification date; use the optional companion validator when available.
8. Retrieval-test with a fresh agent or a realistic prompt when the procedure is important or easy to misroute.
9. Mark stale Skills `needs-verification` in the index. Deprecate superseded Skills and point to the replacement.

## Destination Test

Use the smallest durable form:

- one mandatory sentence -> `AGENTS.md`;
- one fact or failure mode -> gotcha or architecture note;
- short command sequence -> runbook;
- conditional multi-step behavior -> project Skill.

Repository-specific Skills remain in the repository. Do not copy them into the shared workflow Skill unless the lesson is genuinely reusable across unrelated projects and separately reviewed.
