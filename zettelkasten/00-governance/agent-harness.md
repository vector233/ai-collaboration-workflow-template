---
title: Agent Harness
status: active
project: {{PROJECT_NAME}}
last_verified_at: YYYY-MM-DD
source_of_truth: mixed
related:
  - "[[CLAUDE]]"
  - "[[00-governance/harness-engineer-roles]]"
  - "[[00-governance/harness-assignment-cards]]"
  - "[[06-requirements/README]]"
  - "[[08-technical-designs/README]]"
  - "[[07-review/README]]"
  - "[[00-governance/gotchas]]"
---

# Agent Harness

## What This Answers

This note defines how AI agents should work in {{PROJECT_NAME}}: which context to read, when code changes are allowed, how to verify work, how to handle review feedback, and where to write back durable lessons.

The goal is to make each task answerable:

- What is the smallest useful context pack?
- Which gate decides whether implementation is allowed?
- Which validation gives real signal?
- Which review feedback is supported by evidence?
- What did we learn that future agents should inherit?

## Harness Layers

| Layer | Project object | Purpose |
|---|---|---|
| Context Harness | [[CLAUDE]], [[01-overview/quick-reference]], relevant REQ/TECH/review notes | Load only the context needed for this task |
| Decision Harness | [[06-requirements/README]], [[08-technical-designs/README]], [[00-governance/decisions]] | Fix scope, boundaries, and architectural decisions before implementation |
| Implementation Harness | Owned paths, module conventions, existing code style | Keep changes inside the current slice |
| Verification Harness | [[05-reference/e2e-test]], builds, tests, lint, browser checks, realistic environment checks | Validate behavior with executable evidence |
| Review Harness | [[07-review/README]], review handoffs, reviewer feedback tables | Convert subjective feedback into evidence-backed decisions |
| Memory Harness | [[00-governance/gotchas]], architecture notes, runbooks, boards | Preserve lessons for the next agent |

## Default Task State Machine

1. **Intake**: classify the task as feature, bugfix, review feedback, architecture, docs, validation, or release.
2. **Context pack**: read the smallest set of linked notes and code entry points.
3. **Requirement gate**: confirm a requirement exists, or create one from [[00-governance/templates/requirement]].
4. **Technical design gate**: before business-code edits, confirm a linked TECH is in `approved/`, or record a tiny-fix waiver.
5. **Implementation slice**: edit only files in the current owned paths.
6. **Verification**: run focused checks for the changed boundary.
7. **Review handoff**: create or update a `REVIEW-...` document in `07-review/pending/`.
8. **Feedback handling**: independently verify reviewer claims before fixing or rejecting them.
9. **Memory writeback**: update gotchas, architecture, runbooks, or boards when durable facts change.
10. **Closeout**: move the requirement, TECH, or review document only when the state migration rules are satisfied.

`in-progress` means active analysis, design, implementation, or validation. It does not by itself permit code changes.

## TECH Gate

Technical design documents live under [[08-technical-designs/README]].

Implementation can start when:

- the requirement links to a TECH document;
- the TECH document is in `approved/`;
- open decisions that affect implementation are resolved or explicitly scoped out;
- required validation is known.

If implementation proves a design assumption wrong, stop the affected work, update the TECH document, and only then continue.

## Tiny-Fix Waivers

A tiny-fix waiver can be recorded in the requirement or review document when the change is low risk and does not alter any contract.

Examples:

- typo, link, comment, formatting, or documentation-only correction;
- localized test fixture adjustment;
- obvious local nil/null guard with no contract change;
- non-user-visible log wording.

Not tiny fixes:

- API, schema, migration, cache key, persistence, permission, billing, quota, secret, provider, deployment, or data-retention changes;
- cross-module behavior changes;
- any change that cannot be validated with a focused local command or realistic smoke test.

## Verification Matrix

Use project-specific commands from [[01-overview/quick-reference]] and [[05-reference/e2e-test]]. As a default:

| Impact | Default validation |
|---|---|
| Docs only | `git diff --check` and link sanity check |
| Backend/API | affected unit tests, integration tests, API smoke |
| Frontend/UI | lint, build, browser or Playwright check for changed flows |
| Database | migration test and realistic schema verification |
| Auth/security/permissions | positive and negative-path tests |
| Background jobs/queues | worker test, idempotency check, retry behavior |
| Third-party integration | sandbox or realistic environment smoke |
| Installer/desktop/mobile/hardware | real-device or closest realistic-environment smoke |

Do not claim coverage that was not run. Record blockers and residual risk in the review handoff.

## Review Feedback Rules

Review feedback is a hypothesis until verified.

- Evidence can be a code location, failing command, log excerpt, screenshot, commit, linked document, official source, or reproducible manual flow.
- Evidence-free critical feedback should be returned for clarification.
- Confirmed or partially confirmed issues should be fixed, validated, and recorded.
- False or unsupported issues should be rejected with counter-evidence in the review document.
- The next development slice should not start until the current review is closed or explicitly waived.

## Memory Writeback Rules

Write durable lessons back when:

- a bug root cause would likely recur;
- an architecture or data-flow fact changed;
- validation commands or runbooks changed;
- a reviewer found a real process gap;
- a requirement or TECH status changed;
- an external dependency, provider, or deployment assumption changed.

Suggested destinations:

- bugs and false assumptions -> [[00-governance/gotchas]]
- architecture facts -> `02-architecture/`
- cross-module rules -> `04-cross-cutting/`
- validation commands -> [[05-reference/e2e-test]] or [[01-overview/quick-reference]]
- workflow status -> [[06-requirements/README]], [[08-technical-designs/README]], [[07-review/README]]

## Definition Of Done

A development slice is done when:

- related requirement and TECH status are explicit;
- changes are within owned paths;
- required validation ran or blockers are recorded;
- review handoff is created or updated;
- confirmed review feedback is fixed and false feedback has counter-evidence;
- durable architecture, test, gotcha, or runbook changes are written back;
- worktree contains no unintended temporary files, secrets, logs, or unrelated changes.
