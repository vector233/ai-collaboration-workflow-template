---
title: Harness Engineer Roles
status: active
project: {{PROJECT_NAME}}
last_verified_at: YYYY-MM-DD
source_of_truth: mixed
related:
  - "[[00-governance/agent-harness]]"
  - "[[00-governance/harness-assignment-cards]]"
  - "[[06-requirements/README]]"
  - "[[08-technical-designs/README]]"
  - "[[07-review/README]]"
---

# Harness Engineer Roles

## What This Answers

This note defines role boundaries for one or more AI agents working on {{PROJECT_NAME}}. Roles are not job titles. They are bounded operating modes with owned paths, decision rights, validation, and handoff obligations.

An agent without a clear assignment can explore and review, but should not edit business code.

## Core Principles

- Every implementation role must bind to a requirement, TECH document, or review handoff.
- Every role needs explicit owned paths and read-only paths.
- A role can decide local implementation details inside owned paths.
- Cross-role contracts, API/schema changes, auth, security, billing, data retention, deployment, or architecture changes must return to requirement, TECH, or review.
- Each role records validation and handoff evidence.
- Review handoff documents are the async interface between agents.

## Assignment Card Shape

Use [[00-governance/templates/assignment-card]] or the examples in [[00-governance/harness-assignment-cards]].

```md
## Assignment

- Role:
- Requirement:
- Technical design:
- Review doc:
- Gate status:
- Gate note:
- Goal:
- Owned paths:
- Read-only paths:
- Out of scope:
- Decisions allowed:
- Must escalate:
- Required validation:
- Expected handoff:
- Branch / commit scope:
```

`Gate status` values:

- `ready`: gate is satisfied; implementation is allowed within owned paths.
- `blocked`: gate is not satisfied; only exploration, design, validation prep, or review is allowed.
- `partial`: only explicitly listed sub-scope is allowed.
- `review-only`: read, verify, and write review feedback; do not edit implementation files.

## Default Roles

| Role | Main responsibility | Can decide | Must escalate |
|---|---|---|---|
| Coordinator Harness Engineer | Gate status, assignment split, ownership conflicts, board updates | work order, owned paths, handoff routing | product priority, TECH conclusions, cross-role contract conflicts |
| Requirement Harness Engineer | Requirements, acceptance criteria, context packs | wording, scope clarification, acceptance item expression | priority, product direction, launch boundaries |
| Architecture Harness Engineer | TECH docs, architecture flow, boundaries, risks | technical flow wording, risk framing, validation strategy | schema, API contract, auth, security, billing, data retention |
| Backend Harness Engineer | Backend services, APIs, jobs, data access, tests | module-internal implementation and tests | API contract, schema, permissions, cross-service cache or data semantics |
| Frontend Harness Engineer | UI, routes, client state, browser flows | component structure and local UI behavior | route contracts, permission semantics, data-source changes |
| Integration Harness Engineer | Third-party services, installers, desktop/mobile/hardware, external systems | local integration details and diagnostics | provider changes, secrets, public contracts, deployment assumptions |
| Verification Harness Engineer | Test matrix, E2E, browser/device/real-environment validation | test order, evidence format, reproduction scripts | business logic changes needed to pass tests |
| Review Harness Engineer | Review pending handoffs, evidence, severity, closure | severity, evidence grouping, feedback wording | requests to modify business logic or overturn TECH decisions |
| Release / Memory Harness Engineer | Docs writeback, gotchas, runbooks, release notes | note placement, board updates, link repair | architecture fact disputes, unverified release claims |

## Role Lifecycle

1. **Assigned**: read the assignment card and confirm goal, owned paths, and validation.
2. **Context loaded**: read only the linked context pack and necessary code entry points.
3. **Local decision**: decide within allowed scope; record important assumptions.
4. **Execute**: edit only owned paths.
5. **Self-verify**: run required validation and record command/result/risk.
6. **Commit / handoff**: prepare a scoped commit and update review handoff.
7. **Await feedback**: do not expand scope while review is open.
8. **Close / transfer**: write status, risks, and next actions back to the relevant notes.

## Parallel Work Rules

- One file has one write owner.
- Shared contracts are owned by Coordinator or Architecture unless explicitly assigned.
- Agents must check worktree status before editing.
- If a required edit crosses owned paths, stop and record the conflict in the review handoff.
- Requirement, TECH, and review README boards should have one owner during parallel work.

## Conflict Escalation

Stop and escalate when:

- two roles need to edit the same file;
- implementation invalidates the TECH;
- reviewer feedback lacks evidence but requests behavior changes;
- validation contradicts acceptance criteria;
- a change touches secrets, providers, billing, permissions, retention, deployment, or public contracts.

Default escalation path:

1. Record conflict and evidence in the relevant review handoff.
2. Let the current file owner decide local implementation conflicts.
3. Return architecture or contract conflicts to TECH.
4. Return product scope conflicts to requirement.
5. Let Verification or Release / Memory record launch risk and blockers.
