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

The requirement or review handoff should make those boundaries explicit before an agent edits files.

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
