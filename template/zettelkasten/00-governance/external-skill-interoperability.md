---
title: External Skill Interoperability
status: active
project: {{PROJECT_NAME}}
last_verified_at: YYYY-MM-DD
source_of_truth: project
related:
  - "[[AI]]"
  - "[[00-governance/ai-workflow]]"
  - "[[06-requirements/README]]"
  - "[[08-technical-designs/README]]"
  - "[[07-review/README]]"
---

# External Skill Interoperability

## Purpose

External process Skills can improve brainstorming, planning, TDD, debugging, or review. They are optional execution aids, not project dependencies. An agent without them must still be able to use the standard workflow.

The repository knowledge base remains the only durable source of truth.

## Artifact Mapping

| External process output | Canonical project destination |
|---|---|
| Brainstormed goals, scope, user stories, acceptance criteria | Active REQ |
| Approved architecture, interfaces, data flow, decisions | Linked TECH when required, otherwise REQ technical readiness |
| Detailed implementation steps | Linked PLAN when required, otherwise REQ implementation slices |
| TDD or execution progress | Current REVIEW validation and resume context |
| Debugging findings and root causes | Current REVIEW and `00-governance/gotchas.md` |
| Code-review findings | Current REVIEW feedback table |
| Durable architecture or operational learning | Architecture notes or runbooks |

Do not create a tool-specific parallel tree such as `docs/superpowers/specs/` or `docs/superpowers/plans/` unless the user explicitly asks for an export. Use the selected REQ, TECH, and PLAN artifacts instead.

## Gate Mapping

- A user-approved REQ plus either an approved TECH or complete inline technical readiness satisfies external brainstorming and design gates.
- The REQ's delivery-path decision defines implementation readiness.
- Detailed standalone planning is optional unless the REQ marks PLAN required.
- A tiny-fix waiver may skip external brainstorming and planning.
- An open REVIEW still blocks the next implementation slice unless explicitly waived.

If an external Skill is invoked after suitable REQ, TECH, or PLAN documents already exist, continue and refine them. Do not restart discovery solely to satisfy the external Skill's default document layout.

## Superpowers Mapping

When Superpowers is installed:

1. Use `brainstorming` as a questioning and design-review method.
2. Write its approved requirement content into the active REQ and its technical design content into the linked TECH when one is required.
3. Treat the REQ plus selected technical-readiness content as the requested spec output; do not also create `docs/superpowers/specs/`.
4. Map `writing-plans` into a required PLAN or the REQ implementation slices; do not create `docs/superpowers/plans/`.
5. Record TDD, execution, verification, and code-review evidence in the current REVIEW.
6. Follow repository Git rules. Do not commit, branch, or create a worktree solely because an external Skill defaults to doing so.

Superpowers may still be used for its process discipline. This mapping changes where durable state is stored, not whether its reasoning methods may be used.

## No External Skill Installed

Do nothing special. Follow [[00-governance/ai-workflow]] normally:

```text
REQ -> [TECH] -> [PLAN] -> implementation and validation -> REVIEW -> writeback
```

No external command, plugin, directory, or document is required.
