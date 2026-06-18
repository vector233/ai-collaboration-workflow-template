---
title: AI Workflow
status: active
project: AI Collaboration Workflow Template
last_verified_at: 2026-06-18
source_of_truth: mixed
related:
  - "[[AI]]"
  - "[[06-requirements/README]]"
  - "[[08-technical-designs/README]]"
  - "[[07-review/README]]"
  - "[[00-governance/gotchas]]"
---

# AI Workflow

## Purpose

This note defines the default workflow for AI-assisted development in AI Collaboration Workflow Template. It is intentionally lightweight: the goal is not to add a management framework, but to make AI work traceable, reviewable, and easy to resume.

The workflow answers five questions for every non-trivial task:

- What is the smallest useful context?
- What is the requirement and acceptance criteria?
- Is the technical approach ready for implementation?
- What validation proves the change works?
- What should be written back for future agents?

## Default Flow

1. **Classify the task** as feature, bugfix, review feedback, architecture change, documentation, validation, release, or research.
2. **Load the context pack**: read this file, [[01-overview/quick-reference]], and the requirement, technical design, review handoff, architecture note, or runbook linked from the task.
3. **Check the requirement**: find or create a requirement under [[06-requirements/README]].
4. **Check implementation readiness**: before business-code edits, confirm the related technical design is in `approved/`, or record a tiny-fix waiver.
5. **Implement one slice**: keep the change small and within the task's declared paths.
6. **Validate the changed boundary**: run the smallest test, build, browser check, integration smoke, or realistic environment check that gives signal.
7. **Create or update review handoff**: record scope, commit, validation, worktree status, risks, and review focus under [[07-review/README]].
8. **Handle feedback with evidence**: verify reviewer claims before fixing or rejecting them.
9. **Write durable lessons back**: update gotchas, architecture notes, runbooks, or workflow boards when facts change.
10. **Close the loop**: move requirement, technical design, and review documents only when their state rules are satisfied.

`in-progress` means the requirement is active. It does not automatically mean implementation is allowed. Implementation readiness is decided by the technical design gate.

## Tiny-Fix Waivers

A tiny-fix waiver can be recorded in the requirement or review document when the change is clearly low risk and does not alter behavior contracts.

Good candidates:

- typos, broken links, comments, formatting, or documentation-only cleanup;
- localized test fixture updates;
- obvious local null/empty guard with no API or data-contract change;
- non-user-visible log wording.

Not tiny fixes:

- API, schema, migration, cache key, persistence, permission, billing, quota, secret, provider, deployment, or data-retention changes;
- cross-module behavior changes;
- changes whose risk cannot be validated with a focused command or smoke test.

## Review Feedback

Review feedback is a hypothesis until verified.

- Evidence can be a code location, failing command, log excerpt, screenshot, commit, linked document, official source, or reproducible manual flow.
- Evidence-free critical feedback should be returned for clarification.
- Confirmed or partially confirmed issues should be fixed, validated, and recorded.
- False or unsupported issues should be rejected with counter-evidence in the review document.
- The next implementation slice should not start until the current review is closed or explicitly waived.

## Validation

Use project-specific commands from [[01-overview/quick-reference]] and [[05-reference/e2e-test]].

As a default:

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

## Memory Writeback

Write durable lessons back when:

- a bug root cause would likely recur;
- an architecture or data-flow fact changed;
- validation commands or runbooks changed;
- a reviewer found a real process gap;
- a requirement or technical design status changed;
- an external dependency, provider, or deployment assumption changed.

Suggested destinations:

- bugs and false assumptions -> [[00-governance/gotchas]]
- architecture facts -> `02-architecture/`
- cross-module rules -> `04-cross-cutting/`
- validation commands -> [[05-reference/e2e-test]] or [[01-overview/quick-reference]]
- workflow status -> [[06-requirements/README]], [[08-technical-designs/README]], [[07-review/README]]

## Definition Of Done

A slice is done when:

- the related requirement and technical design status are explicit;
- changes are scoped to the current task;
- required validation ran or blockers are recorded;
- review handoff is created or updated when needed;
- confirmed review feedback is fixed and false feedback has counter-evidence;
- durable architecture, test, gotcha, or runbook changes are written back;
- the worktree contains no unintended temporary files, secrets, logs, or unrelated changes.
