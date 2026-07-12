# Practical Scenario Snippets

These snippets show how to keep the workflow light while preserving state that a future agent can use. They are not a full initialized knowledge base.

## Tiny Documentation Fix

Use this when the change is non-behavioral, local, and easy to validate.

```text
Task: fix a broken internal wiki link in an architecture note.
Path: tiny waiver.
Artifacts: no REQ, no REVIEW.
Validation: git diff --check; python3 scripts/workflow_doctor.py.
Writeback: final response mentions the fixed link and validation.
Rule Promotion Check: not applicable unless the broken link reveals a repeatable authoring mistake.
CURRENT.md: unchanged unless this was part of active work.
```

Do not stretch tiny mode to cover API, schema, permission, persistence, deployment, billing, provider, or cross-module behavior.

## Bounded Bug Fix

Use this when the root cause is known, impact is local, and one focused validation path proves the fix.

```text
REQ -> inline technical readiness -> implementation -> REVIEW -> Rule Promotion Check -> writeback
```

Minimum state:

- REQ records task weight `bounded`, root cause, affected paths, non-goals, and focused validation plan.
- REVIEW records fix summary, command output, worktree status, next allowed action, and Rule Promotion Check.
- `CURRENT.md` points to the active REQ and open REVIEW until the review closes.
- `gotchas.md` gets a prevention rule if the root cause is likely to recur.

Example promotion:

```text
Candidate lesson: API handlers must reject expired invitation tokens before workspace membership lookup.
Decision: promote.
Destination: gotchas.md and the auth/invitation architecture note.
Do not put in root AGENTS.md because it is a domain invariant, not a repository-wide agent behavior rule.
```

## Long Task Resume

Use this when work spans sessions, agents, owners, or multiple slices.

```text
REQ -> TECH when needed -> PLAN -> per-slice implementation -> REVIEW -> CURRENT.md update
```

Before pausing:

- Update the PLAN resume state with current slice, last completed step, blockers, and next allowed action.
- Update the current REVIEW with exact validation and residual risk.
- Update `CURRENT.md` so a fresh agent can find the active REQ, controlling TECH/PLAN, open REVIEW, and next action without chat history.
- Run `python3 scripts/workflow_doctor.py`; resolve errors and treat warnings as routing reminders.

Fresh-agent prompt:

```text
Read AGENTS.md, zettelkasten/AI.md, and zettelkasten/CURRENT.md. Report the active REQ, controlling TECH/PLAN, open REVIEW, validation status, residual risk, and next allowed action before editing files.
```

## Review Fix With Rule Promotion

Use this when review feedback exposes a real process gap or repeatable false assumption.

```text
REVIEW in-review -> verify evidence -> fix confirmed issue -> validate -> Rule Promotion Check -> close REVIEW
```

Handling rules:

- Evidence-free feedback gets clarification, not code churn.
- Confirmed feedback gets a fix, validation evidence, and a REVIEW feedback-table update.
- False feedback gets counter-evidence in the REVIEW.
- Rule Promotion Check decides where the lesson belongs.

Destination examples:

| Lesson | Destination |
|---|---|
| "Always run the workflow doctor before closing a review" | `AGENTS.md` |
| "Token expiry must be checked before membership lookup" | `gotchas.md` and architecture note |
| "Sandbox webhook retries require this manual cleanup command" | `05-reference/e2e-test.md` |
| "This was a one-off reviewer misunderstanding" | REVIEW only |
