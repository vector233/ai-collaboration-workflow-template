# ExampleSaaS Walkthrough

This fictional example shows how the adaptive workflow is intended to be used. It is not a complete project knowledge base.

## Delivery Path Examples

A bounded bug with a confirmed local cause could use:

```text
REQ -> implement and validate -> REVIEW -> Rule Promotion Check -> writeback
```

The REQ would mark standalone TECH and PLAN as not required, then record the root cause, affected paths, focused fix, validation, and implementation slice inline.

The invitation-link feature below has security, persistence, API, and multi-slice concerns, so it uses a standalone TECH and PLAN.

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
- Delivery path: standalone TECH required; standalone PLAN required.

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

Implementation starts only after this TECH is approved.

## 3. Implementation Plan

Create:

```text
zettelkasten/09-implementation-plans/PLAN-20260601110000-team-invitation-links.md
```

Set it to `ready` after backend, frontend, migration, validation, and review dependencies are explicit.

## 4. Implementation Slice

Example first slice:

- Owned paths: `backend/invitations/`, `backend/tests/invitations/`
- Read-only paths: `frontend/`, `zettelkasten/`
- Required validation: backend invitation tests plus API negative-path smoke
- Out of scope: frontend settings UI

The requirement or review handoff should make those boundaries explicit before an agent edits files.

## 5. Review Handoff

Create:

```text
zettelkasten/07-review/pending/REVIEW-20260601123000-team-invitation-links-backend.md
```

The handoff records:

- linked REQ, approved TECH, and ready PLAN;
- latest commit;
- validation commands and result summaries;
- current `git status --short`;
- `CURRENT.md` entry pointing to this active slice and review;
- known gaps, such as "frontend UI not implemented";
- Rule Promotion Check, such as whether token expiry pitfalls should become a durable security rule;
- workflow doctor result, such as `python3 scripts/workflow_doctor.py`;
- reviewer focus, such as token expiry and permission checks.

## 6. Feedback Handling

If a reviewer says "non-admins can create links", the feedback must include evidence:

- code path;
- failing test;
- API request/response;
- or a reproducible command.

The implementation agent verifies the claim. If true, it fixes and records validation. If false, it writes counter-evidence in the review document.

## 7. Memory Writeback

After completion:

- move the REQ to `done/`;
- move the TECH to `implemented/`;
- set the PLAN to `completed`;
- move the review to `done/`;
- update `CURRENT.md` so the completed slice no longer appears as active work;
- complete the Rule Promotion Check;
- run `python3 scripts/workflow_doctor.py`;
- update `02-architecture/current-architecture-flow.md` with the invite flow;
- add any token/security lessons to `00-governance/gotchas.md` or `00-governance/decisions.md`.

Example promotion decision:

- Candidate lesson: invitation tokens must be stored only as hashes and validated with explicit expiry checks.
- Promote: yes.
- Destination: `00-governance/gotchas.md` for the root cause pattern, and `02-architecture/current-architecture-flow.md` for the current invite-token invariant.
- Rule written: "Invite-token flows must validate hash match, expiry, revocation, and workspace permission together before accepting the invite."

## Initialized File Snippets

These snippets show the shape of an initialized project without duplicating a full template.

### `zettelkasten/06-requirements/in-progress/REQ-20260601103000-team-invitation-links.md`

```md
# Team Invitation Links

## Goals

- Workspace admins can create expiring invitation links.
- Invitees can join a workspace through a valid link.
- Admins can revoke links.

## Non-Goals

- SSO.
- Domain allowlists.
- Paid-seat billing changes.

## Context Pack

- [[02-architecture/current-architecture-flow]]
- `backend/workspaces/`
- `backend/auth/`
- `frontend/settings/team/`

## Technical Design

- Technical design: [[08-technical-designs/approved/TECH-20260601104500-team-invitation-links]]
- Current state: approved

## Implementation Slices

- Implementation plan: [[09-implementation-plans/PLAN-20260601110000-team-invitation-links]]
- Current state: ready
```

### `zettelkasten/08-technical-designs/approved/TECH-20260601104500-team-invitation-links.md`

```md
# Team Invitation Links Technical Design

## Target Technical Flow

1. Admin creates an invite link from workspace settings.
2. API verifies admin permission.
3. API stores hashed token, expiry, creator, and workspace ID.
4. Invitee opens link and submits account details.
5. API verifies token hash, expiry, revocation, and workspace state.
6. API creates workspace membership and records an audit event.

## Validation Plan

- Unit tests for token expiry, revocation, and permission checks.
- API smoke for create, revoke, join, expired join, and non-admin create.
- Browser smoke for workspace settings once frontend slice exists.
```

### `zettelkasten/09-implementation-plans/PLAN-20260601110000-team-invitation-links.md`

```md
# Team Invitation Links Implementation Plan

## Execution Map

| Slice | Deliverable | Depends on | Owned paths | Validation | Status |
|---|---|---|---|---|---|
| S1 | Backend create/revoke/join API | approved TECH | `backend/invitations/` | backend tests and API smoke | ready |
| S2 | Workspace settings UI | S1 | `frontend/settings/team/` | lint, build, browser smoke | blocked |
| S3 | Final integration and writeback | S1, S2 | tests and zettelkasten | full invitation flow | blocked |
```

### `zettelkasten/07-review/pending/REVIEW-20260601123000-team-invitation-links-backend.md`

```md
# Team Invitation Links Backend Review

## Completed Changes

- Added invitation create/revoke/join API.
- Added token hashing and expiry validation.
- Added backend tests for positive and negative paths.

## Validation Results

- `npm run test -- invitations`: passed.
- API smoke: create/revoke/join/expired/non-admin paths passed.
- Browser smoke: not run; frontend slice is out of scope.

## Suggested Review Focus

- Token storage and hashing.
- Expiry and revocation behavior.
- Permission checks for admin-only create/revoke.
```
