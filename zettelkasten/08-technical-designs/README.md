---
title: Technical Designs
status: active
project: AI Collaboration Workflow Template
last_verified_at: 2026-06-18
source_of_truth: mixed
related:
  - "[[00-governance/ai-workflow]]"
  - "[[06-requirements/README]]"
  - "[[02-architecture/current-architecture-flow]]"
  - "[[00-governance/templates/technical-design]]"
  - "[[07-review/README]]"
---

# 08-technical-designs

## Purpose

This directory answers: after a requirement is understood, how does it become an implementation-ready technical plan?

Requirements describe **why, what, non-goals, and acceptance criteria**. Technical designs describe **system flow, boundaries, decisions, risks, and validation**.

## Directory Structure

- `pending/` — proposed design, not yet implementation input
- `approved/` — confirmed design, allowed as implementation input
- `implemented/` — implemented, reviewed, and written back to current architecture notes

## Workflow

The technical design is the implementation readiness gate in [[00-governance/ai-workflow]].

1. When a requirement enters `in-progress/`, check whether it has a linked technical design.
2. If not, copy [[00-governance/templates/technical-design]] into `pending/`.
3. Keep the design at architecture-flow level. Do not turn it into line-by-line implementation instructions.
4. Resolve decisions that affect implementation.
5. Move the design to `approved/` when it is ready to guide code work.
6. If implementation proves a design assumption wrong, update the design before continuing.
7. Link review handoffs back to the technical design.
8. After implementation, review close, and architecture writeback, move the design to `implemented/`.

## Naming

Use:

- `TECH-YYYYMMDDHHMMSS-short-name.md`

Example:

- `TECH-20260428154500-team-invitation-links.md`

## Minimum Contents

Every technical design should include:

- linked requirement;
- current architecture facts;
- target technical flow;
- decisions;
- impact boundaries;
- non-goals;
- open decisions;
- validation plan;
- architecture writeback checklist.

## Board

<!-- Maintain a current technical design board here. Example:

| State | Technical design | Requirement | Next step |
|---|---|---|---|
| approved | [[08-technical-designs/approved/TECH-YYYYMMDDHHMMSS-example]] | [[06-requirements/in-progress/REQ-YYYYMMDDHHMMSS-example]] | One-sentence next step |
-->

## State Transitions

| State directory | Enter when | Leave when |
|---|---|---|
| `pending/` | Design is proposed but not confirmed | Decisions resolved -> move to `approved/` |
| `approved/` | Ready as implementation input | Requirement done, review closed, architecture written back -> move to `implemented/` |
| `implemented/` | Implemented and written back | Do not move |

Move the file between state directories. Do not change `technical_design_id`.

## Relationship To Review

- A technical design is not a review handoff.
- A design can be reviewed before it becomes `approved/`.
- Implementation handoffs should link the technical design used for the slice.
- Review feedback about a design still needs evidence.

## See Also

- [[00-governance/ai-workflow]] — implementation readiness gate
- [[06-requirements/README]] — requirement workflow
- [[07-review/README]] — review workflow
- [[00-governance/templates/technical-design]] — technical design template
