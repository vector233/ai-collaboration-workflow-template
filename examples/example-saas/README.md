# ExampleSaaS Walkthrough

This fictional example shows how the template is intended to be used. It is not a complete project knowledge base.

## Scenario

ExampleSaaS wants to add "team invitation links".

## 1. Requirement

Create:

```text
zettelkasten/06-requirements/backlog/REQ-20260601103000-team-invitation-links.md
```

Key fields:

- Goal: workspace admins can create expiring invite links.
- Non-goal: SSO, domain allowlists, and paid-seat billing changes.
- Context pack: auth model, workspace membership model, API routes, frontend invite settings page.
- Acceptance: create link, revoke link, join by link, expired link rejected, non-admin cannot create link.

## 2. Technical Design

Create:

```text
zettelkasten/08-technical-designs/pending/TECH-20260601104500-team-invitation-links.md
```

Move it to `approved/` only after decisions are clear:

- token format;
- expiry and revocation semantics;
- API contract;
- database ownership;
- audit log behavior;
- validation plan.

Implementation starts only after this TECH is approved, unless the task is reduced to a documented tiny-fix waiver.

## 3. Implementation Slice

Example first slice:

- Owned paths: `backend/invitations/`, `backend/tests/invitations/`
- Read-only paths: `frontend/`, `zettelkasten/`
- Required validation: backend invitation tests plus API negative-path smoke
- Out of scope: frontend settings UI

The assignment card should make those boundaries explicit before an agent edits files.

## 4. Review Handoff

Create:

```text
zettelkasten/07-review/pending/REVIEW-20260601123000-team-invitation-links-backend.md
```

The handoff records:

- linked REQ and approved TECH;
- latest commit;
- validation commands and result summaries;
- current `git status --short`;
- known gaps, such as "frontend UI not implemented";
- reviewer focus, such as token expiry and permission checks.

## 5. Feedback Handling

If a reviewer says "non-admins can create links", the feedback must include evidence:

- code path;
- failing test;
- API request/response;
- or a reproducible command.

The implementation agent verifies the claim. If true, it fixes and records validation. If false, it writes counter-evidence in the review document.

## 6. Memory Writeback

After completion:

- move the REQ to `done/`;
- move the TECH to `implemented/`;
- move the review to `done/`;
- update `02-architecture/current-architecture-flow.md` with the invite flow;
- add any token/security lessons to `00-governance/gotchas.md` or `00-governance/decisions.md`.
