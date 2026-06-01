# 06-requirements

## Purpose

This directory answers: where requirements live, how they are written, how their state changes, and how they connect implementation work to existing context.

Requirements are not current-state documentation. They are the entry point for future change.

## Directory Structure

- `backlog/` — identified but not active
- `in-progress/` — active analysis, design, implementation, validation, or acceptance
- `done/` — completed, reviewed, and written back to current-state docs

## Board

<!-- Maintain a current requirement board here. Example:

| Priority | Status | Requirement | Next step |
|---|---|---|---|
| P0 | in-progress | [[06-requirements/in-progress/REQ-YYYYMMDDHHMMSS-example]] | One-sentence next step |
-->

## Workflow

Follow [[00-governance/ai-workflow]].

1. Copy [[00-governance/templates/requirement]] into `backlog/`.
2. Fill in background, goals, non-goals, context pack, confirmed facts, impact, and acceptance criteria.
3. Move the requirement to `in-progress/` when it becomes active.
4. Create or confirm the linked technical design under [[08-technical-designs/README]].
5. Do not start business-code implementation until the linked technical design is in `approved/`, unless a tiny-fix waiver is recorded.
6. After each implementation slice, create or update a review handoff under [[07-review/README]].
7. Handle review feedback with evidence.
8. After implementation, validation, review close, and documentation writeback, move the requirement to `done/`.

## Naming

Use:

- `REQ-YYYYMMDDHHMMSS-short-name.md`

Example:

- `REQ-20260428153045-team-invitation-links.md`

## State Transitions

| State directory | Enter when | Leave when |
|---|---|---|
| `backlog/` | Requirement is identified but not active | Decided for current work -> move to `in-progress/` |
| `in-progress/` | Requirement is active | Implementation, validation, review, and writeback are complete -> move to `done/` |
| `done/` | Completed and written back | Do not move |

Move the file between state directories. Do not change `requirement_id`.

## Minimum Contents

Every requirement should include:

- background;
- goals;
- non-goals;
- context pack;
- confirmed facts;
- open questions;
- impact boundaries;
- acceptance criteria;
- linked technical design;
- linked review handoff;
- validation record;
- documentation writeback checklist.

The most important sections are:

- **Context pack**: tells future agents what to read first.
- **Confirmed facts**: separates known facts from guesses.
- **Technical design**: defines implementation readiness.
- **Review feedback handling**: prevents unsupported review comments from becoming code churn.
- **Documentation writeback checklist**: prevents current-state docs from going stale.

## Technical Design Gate

Every requirement that reaches implementation should satisfy:

- it links to a `TECH-YYYYMMDDHHMMSS-short-name.md`;
- the technical design is in `approved/`, or a tiny-fix waiver is recorded;
- the technical design links relevant architecture and reference notes;
- architecture writeback is planned if the system flow changes.

A requirement in `in-progress/` with a `pending/` technical design can continue clarification, design, validation prep, or review handling. It is not implementation-ready.

## See Also

- [[00-governance/ai-workflow]] — default AI workflow
- [[08-technical-designs/README]] — technical design workflow
- [[07-review/README]] — review workflow
- [[00-governance/templates/requirement]] — requirement template
