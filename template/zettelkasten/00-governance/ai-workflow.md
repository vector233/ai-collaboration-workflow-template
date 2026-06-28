---
title: AI Workflow
status: active
project: {{PROJECT_NAME}}
last_verified_at: YYYY-MM-DD
source_of_truth: mixed
related:
  - "[[AI]]"
  - "[[06-requirements/README]]"
  - "[[08-technical-designs/README]]"
  - "[[09-implementation-plans/README]]"
  - "[[07-review/README]]"
  - "[[00-governance/gotchas]]"
---

# AI Workflow

## Purpose

This note defines the default workflow for AI-assisted development in {{PROJECT_NAME}}. It is intentionally lightweight: the goal is not to add a management framework, but to make AI work traceable, reviewable, and easy to resume.

The workflow answers eight questions for every tracked task:

- What is the smallest useful context?
- What is the requirement and acceptance criteria?
- Does this task need a standalone technical design?
- Does this task need a standalone implementation plan?
- Is the selected delivery path ready for implementation?
- What validation proves the change works?
- Which lessons should be promoted into durable project rules?
- What should be written back for future agents?

## Default Flow

1. **Classify the task** as feature, bugfix, review feedback, architecture change, documentation, validation, release, or research.
2. **Load the context pack**: read this file, [[01-overview/quick-reference]], and the requirement, technical design, review handoff, architecture note, or runbook linked from the task.
3. **Check the requirement**: find or create a requirement under [[06-requirements/README]].
4. **Choose the delivery path**: in the REQ, mark standalone TECH and PLAN as required or not required, with reasons.
5. **Check implementation readiness**: approve required TECH/PLAN artifacts. When they are not required, complete the REQ's inline technical readiness and implementation slices.
6. **Implement and validate one slice**: keep the change within declared paths and run the smallest check that gives signal.
7. **Create or update review handoff**: record scope, commit, validation, worktree status, risks, and review focus under [[07-review/README]].
8. **Handle feedback with evidence**: verify reviewer claims before fixing or rejecting them.
9. **Run the Rule Promotion Check**: decide whether the work exposed a repeatable lesson that should become a durable project rule.
10. **Close the loop**: close the review, write back current-state facts, and update any REQ, TECH, or PLAN states that exist.

## Delivery Paths

Use the lightest path that preserves safety and resumability:

| Change shape | Default path |
|---|---|
| Tiny, non-behavioral change | change -> validate |
| Bounded, low-risk bug with known cause and local impact | REQ -> implement and validate -> REVIEW -> Rule Promotion Check -> writeback |
| Standard feature or change with meaningful technical decisions | REQ -> TECH -> implement and validate -> REVIEW -> Rule Promotion Check -> writeback |
| Complex, multi-slice, multi-session, or coordinated change | REQ -> TECH when needed -> PLAN -> implement and validate -> REVIEW -> Rule Promotion Check -> writeback |

Technical reasoning is never optional. A standalone TECH is optional when the REQ can clearly record the confirmed cause or approach, affected paths, risks, and validation plan.

Execution decomposition is never optional. A standalone PLAN is optional when the REQ's implementation slices are sufficient for one agent or session to proceed safely.

## Standalone TECH Triggers

Create a TECH when any of these apply:

- architecture, API, schema, persistence, security, billing, permission, deployment, or data-retention behavior changes;
- multiple modules, repositories, jobs, or third-party systems are affected;
- important technical decisions or competing approaches remain unresolved;
- rollback, compatibility, migration, or operational behavior needs design review;
- the technical flow is too large or unstable to remain clear inside the REQ.

## Standalone PLAN Triggers

Create a PLAN under [[09-implementation-plans/README]] when any of these apply:

- implementation has multiple dependent slices;
- work is expected to span multiple sessions, agents, owners, or repositories;
- file ownership, sequencing, migration order, or release checkpoints must be explicit;
- each slice needs its own validation and review checkpoint;
- a detailed execution plan materially improves safe resumption.

## Cross-Agent Handoff Contract

The workflow must survive a change of AI vendor, model, session, or human owner.

- Treat repository files as the source of truth; chat history and agent-local memory are optional caches.
- Record confirmed facts separately from assumptions and unresolved decisions.
- Every active slice must link its REQ, any controlling TECH or PLAN, and current REVIEW.
- Every handoff must state the last completed step, exact validation evidence, current branch/worktree state, known risks, and next allowed action.
- Do not use vendor-specific capabilities as an undocumented prerequisite. Record required commands, tools, credentials setup, or manual steps in project runbooks.
- A receiving agent must verify repository state and evidence before continuing rather than trusting a previous agent's narrative.

## Optional External Process Skills

This workflow does not depend on Superpowers or any other external process Skill. When one is available, use it as an execution aid and map its durable output back into this knowledge base instead of creating a second source of truth.

Use [[00-governance/external-skill-interoperability]] when an external Skill requests its own spec, plan, review, commit, branch, or worktree workflow. Map its output to the REQ and optional TECH/PLAN selected for the task.

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

## Rule Promotion Check

Run this check before handing off a long-running task, closing a bug fix, closing a review fix, or ending work that required non-obvious setup, debugging, or recovery.

Promote a lesson to a durable rule when any of these are true:

- the same mistake would likely recur in another session;
- an AI or human made a false assumption that future agents may repeat;
- the task revealed a hidden ordering, setup, validation, environment, or tool requirement;
- a long-running command, migration, job, or external integration needed a non-obvious guardrail;
- review found a real process gap or undocumented invariant;
- the lesson can be expressed as a clear "must", "never", "prefer", or "check before" rule.

Do not promote one-off observations, subjective preferences, temporary incidents, or low-confidence guesses. Record those in the current REQ or REVIEW instead.

For each candidate, record:

- candidate lesson;
- decision: promote / do not promote;
- reason;
- destination note;
- exact rule or summary written.

Suggested destinations:

- repository-wide agent behavior -> `AGENTS.md`
- bugs, false assumptions, and repeated failure modes -> [[00-governance/gotchas]]
- architecture or data-flow invariants -> `02-architecture/`
- cross-module rules -> `04-cross-cutting/`
- validation commands, setup, and smoke-test procedures -> [[05-reference/e2e-test]] or [[01-overview/quick-reference]]
- accepted design or process decisions -> [[00-governance/decisions]]
- workflow state only -> [[06-requirements/README]], [[08-technical-designs/README]], [[09-implementation-plans/README]], or [[07-review/README]]

## Memory Writeback

Write durable lessons back when:

- a bug root cause would likely recur;
- an architecture or data-flow fact changed;
- validation commands or runbooks changed;
- a reviewer found a real process gap;
- a requirement, technical design, or implementation plan status changed;
- an external dependency, provider, or deployment assumption changed.

Suggested destinations:

- repository-wide agent rules -> `AGENTS.md`
- bugs and false assumptions -> [[00-governance/gotchas]]
- architecture facts -> `02-architecture/`
- cross-module rules -> `04-cross-cutting/`
- validation commands -> [[05-reference/e2e-test]] or [[01-overview/quick-reference]]
- workflow status -> [[06-requirements/README]], [[08-technical-designs/README]], [[09-implementation-plans/README]], [[07-review/README]]

## Definition Of Done

A slice is done when:

- the related requirement and any selected TECH/PLAN states are explicit;
- changes are scoped to the current task;
- required validation ran or blockers are recorded;
- review handoff is created or updated when needed;
- confirmed review feedback is fixed and false feedback has counter-evidence;
- the Rule Promotion Check is recorded for long-running tasks, bug fixes, review fixes, or repeated failure modes;
- durable architecture, test, gotcha, or runbook changes are written back;
- the worktree contains no unintended temporary files, secrets, logs, or unrelated changes.
