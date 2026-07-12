---
title: Requirement Title
status: backlog
project: {{PROJECT_NAME}}
requirement_id: REQ-YYYYMMDDHHMMSS-short-name
last_verified_at: YYYY-MM-DD
source_of_truth: mixed
affected_projects:
  - <project-or-module>
related:
  - "[[00-governance/project-overview]]"
  - "[[01-overview/quick-reference]]"
  - "[[02-architecture/current-architecture-flow]]"
  - "[[05-reference/e2e-test]]"
  - "[[08-technical-designs/README]]"
  - "[[09-implementation-plans/README]]"
  - "[[07-review/README]]"
---

# Requirement Title

## What This Requirement Answers

This document explains what should change, why it matters, what is out of scope, where the implementation context lives, and how the work will be accepted.

## Background

- Business context:
- Trigger:
- Current pain:

## Goals

- Goal 1:
- Goal 2:

## Non-Goals

- Not included:
- Not changed:

## Context Pack

Read these first before implementation. If they are not enough, add the smallest missing note.

- Current architecture notes:
- Cross-module flow notes:
- Key code entry points:
- Subproject instructions:

## Confirmed Facts

- Fact 1:
- Fact 2:

## Open Questions

- Question 1:
- Question 2:

## Impact

### Projects / Modules

- Affected projects or modules:
  - <project-or-module-1>
  - <project-or-module-2>

### Interfaces / Data / Jobs / Config

- APIs:
- Data tables / views:
- Queues / scheduled jobs / third parties:
- Config / environment:

## Proposed Change

- Summary:
- Key changes:
- Compatibility risks:

## Delivery Path

Choose the lightest path that preserves safety and resumability.

- Task weight: bounded / standard / complex / high-risk
- Tiny waiver used before this REQ: yes / no
- Standalone TECH: required / not required
- TECH decision reason:
- Standalone PLAN: required / not required
- PLAN decision reason:

## Technical Readiness

If standalone TECH is required:

- Technical design: `TECH-YYYYMMDDHHMMSS-short-name.md`
- Current state: pending / approved / implemented

If standalone TECH is not required:

- Why inline readiness is sufficient:
- Confirmed root cause or technical approach:
- Affected paths and behavior boundaries:
- Compatibility / rollback considerations:
- Focused validation plan:

## Implementation Slices

- Slice 1:
- Slice 2:

If standalone PLAN is required:

- Implementation plan: `PLAN-YYYYMMDDHHMMSS-short-name.md`
- Current state: draft / ready / executing / completed / superseded

If standalone PLAN is not required, the slices above must include enough scope, ordering, affected paths, and validation detail to execute and resume safely.

## Acceptance Criteria

- Criterion 1:
- Criterion 2:

## Validation Record

- Build:
- Unit / integration tests:
- API / DB / queue / third-party smoke:
- Browser / E2E / realistic environment:
- New or existing blockers:

## Review Handoff

When a slice is ready for review, create a handoff under [[07-review/README]]:

- `REVIEW-YYYYMMDDHHMMSS-short-name.md`

The handoff should include:

- Task goal and scope:
- Completed changes:
- Latest commit:
- Validation results:
- Current worktree status:
- Known risks / blockers:
- Next steps:
- Suggested review focus:

This requirement's review handoff:

- Review document:

## Review Feedback Handling

Reviewers must attach evidence to important feedback. The implementation owner must independently verify each claim before fixing or rejecting it.

| Round | Source | Evidence | Feedback summary | Judgment | Status | Fix commit / counter-evidence |
|---|---|---|---|---|---|---|
| Round 1 |  |  |  | pending / confirmed / partial / rejected | pending / fixed / rejected / no action |  |

Review closes when:

- important feedback has evidence;
- the implementation owner has verified each item;
- confirmed or partial issues are fixed, validated, and committed;
- rejected issues have counter-evidence;
- both sides agree this review round is done.

## Integration Flow

If a reusable flow exists, link to [[05-reference/e2e-test]]. Add requirement-specific steps here.

- Preconditions:
- Build order:
- Startup order:
- Auth setup:
- Validation sequence:

## Known Issues And Troubleshooting

- Issue:
- Confirmed conclusion:
- Resume point for next session:

## Documentation Writeback Checklist

After implementation, check and update:

- Rule Promotion Check:
- Current architecture notes:
- Cross-module flow notes:
- Module / API / data docs:
- [[03-roadmap/phases]] or task tracker:

## Evidence Checklist

- Code evidence:
- Config evidence:
- API / SQL / handoff artifacts:
