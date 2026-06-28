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
4. Decide whether standalone TECH and PLAN documents are required, and record the reasons.
5. If TECH is required, create or confirm it under [[08-technical-designs/README]] and wait for `approved/`. Otherwise complete inline technical readiness in the REQ.
6. If PLAN is required, create it under [[09-implementation-plans/README]] and wait for `status: ready`. Otherwise keep sufficient implementation slices in the REQ.
7. Implement and validate one bounded slice.
8. Create or update a review handoff under [[07-review/README]].
9. Handle review feedback with evidence.
10. After implementation, validation, review close, Rule Promotion Check, and documentation writeback, move the requirement to `done/`.

## Naming

Use:

- `REQ-YYYYMMDDHHMMSS-short-name.md`

Example:

- `REQ-20260428153045-team-invitation-links.md`

## State Transitions

| State directory | Enter when | Leave when |
|---|---|---|
| `backlog/` | Requirement is identified but not active | Decided for current work -> move to `in-progress/` |
| `in-progress/` | Requirement is active | Implementation, validation, review, Rule Promotion Check, and writeback are complete -> move to `done/` |
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
- delivery-path decision;
- linked technical design when required, or inline technical readiness;
- linked implementation plan when required, or inline implementation slices;
- linked review handoff;
- validation record;
- Rule Promotion Check result;
- documentation writeback checklist.

The most important sections are:

- **Context pack**: tells future agents what to read first.
- **Confirmed facts**: separates known facts from guesses.
- **Delivery path**: makes TECH and PLAN requirements explicit instead of silently skipping them.
- **Technical readiness**: records either an approved TECH or enough inline evidence for a bounded low-risk change.
- **Implementation slices**: provide enough execution structure when no standalone PLAN is used.
- **Review feedback handling**: prevents unsupported review comments from becoming code churn.
- **Rule Promotion Check**: prevents repeated mistakes from remaining trapped in one session's review context.
- **Documentation writeback checklist**: prevents current-state docs from going stale.

## Implementation Readiness Gate

Every requirement that reaches implementation must satisfy its selected delivery path.

When standalone TECH is required:

- the REQ links a `TECH-YYYYMMDDHHMMSS-short-name.md`;
- the TECH is in `approved/`;
- relevant architecture, compatibility, risk, and validation decisions are resolved.

When standalone TECH is not required, the REQ records:

- why the change is bounded and low risk;
- confirmed root cause or technical approach;
- affected paths and behavior boundaries;
- focused validation plan.

When standalone PLAN is required:

- the REQ links a `PLAN-YYYYMMDDHHMMSS-short-name.md`;
- the PLAN has `status: ready`;
- dependencies, ownership, checkpoints, and per-slice validation are explicit.

When standalone PLAN is not required, the REQ implementation slices must be sufficient to execute and resume the work.

## See Also

- [[00-governance/ai-workflow]] — default AI workflow
- [[08-technical-designs/README]] — technical design workflow
- [[09-implementation-plans/README]] — implementation plan workflow
- [[07-review/README]] — review workflow
- [[00-governance/templates/requirement]] — requirement template
