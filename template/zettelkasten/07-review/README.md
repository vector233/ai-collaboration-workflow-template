# 07-review

## Purpose

This directory answers: where review handoffs live, where reviewer feedback is recorded, how implementation owners judge feedback, and when the next implementation slice can begin.

Review documents are not requirements and not long-term architecture docs. They are handoff and feedback records.

## Directory Structure

- `pending/` — handoff exists and waits for review
- `in-review/` — feedback is being evaluated or fixed
- `done/` — this review round is closed

## Workflow

Review is the evidence checkpoint in [[00-governance/ai-workflow]].

1. When a slice is ready, copy [[00-governance/templates/review]] into `pending/`.
2. The handoff records scope, commit, validation, worktree status, risks, next steps, suggested review focus, and the Rule Promotion Check.
3. A reviewer reads the handoff, linked requirement, any controlling TECH or PLAN, and changed files.
4. Important feedback must include evidence: code location, failing command, log, screenshot, linked doc, commit, or reproducible flow.
5. Move the document to `in-review/` when feedback is being handled.
6. The implementation owner verifies each claim before fixing or rejecting it.
7. Confirmed or partially confirmed issues are fixed, validated, and recorded.
8. False or unsupported issues are rejected with counter-evidence.
9. Complete the Rule Promotion Check before closing a long-running task, bug fix, review fix, or repeated failure mode.
10. Move the document to `done/` when this review round is explicitly closed.
11. Do not start the next implementation slice until the current review is closed or explicitly waived.

## Naming

Use:

- `REVIEW-YYYYMMDDHHMMSS-short-name.md`

Example:

- `REVIEW-20260428153045-team-invitation-links.md`

## Review Document Must Include

- task goal and scope;
- completed changes;
- latest commit;
- validation results;
- current worktree status;
- known risks and blockers;
- next steps;
- suggested review focus;
- Rule Promotion Check result;
- reviewer feedback;
- implementation-owner judgment and handling status;
- counter-evidence for rejected findings;
- close conditions.

## Readiness

If a slice depends on a real browser, database, third-party service, device, installer, background job, queue, deployment environment, or external network, review readiness should follow [[00-governance/validation-discipline]].

If realistic validation could not run, the handoff must record the blocker and residual risk.

## State Transitions

| State directory | Enter when | Leave when |
|---|---|---|
| `pending/` | Handoff is ready for review | Reviewer feedback starts -> move to `in-review/` |
| `in-review/` | Feedback is being evaluated or fixed | Confirmed issues fixed; rejected issues have evidence; review closed -> move to `done/` |
| `done/` | Review round is closed | Do not move |

Move the review file between state directories. Do not change linked requirement IDs.

## Judgment Rules

- Do not modify code just because review feedback exists.
- Check the reviewer's evidence first.
- Ask for evidence when feedback is vague or unsupported.
- UI feedback should include browser evidence or a clear explanation of why it could not be run.
- Rejected feedback must include counter-evidence.
- Only confirmed or partially confirmed issues become fix work.

## Rule Promotion

Use the Rule Promotion Check to prevent repeat mistakes. A lesson should be promoted when it is likely to recur across sessions, agents, modules, or future tasks and can be written as a clear project rule.

Common destinations:

- `AGENTS.md` for repository-wide agent behavior;
- [[00-governance/gotchas]] for bug roots and false assumptions;
- `02-architecture/` or `04-cross-cutting/` for invariants and cross-module rules;
- [[05-reference/e2e-test]] or [[01-overview/quick-reference]] for setup, validation, and operational steps;
- [[00-governance/decisions]] for accepted design or process decisions.

## Relationship To Requirements

Requirement documents describe the work and implementation progress. Review documents preserve handoff, feedback, judgment, fixes, validation, and closure.

Requirements should link to their review documents, and review documents should link back to their requirements and any controlling technical designs or implementation plans.

## See Also

- [[06-requirements/README]]
- [[08-technical-designs/README]]
- [[09-implementation-plans/README]]
- [[00-governance/ai-workflow]]
- [[00-governance/validation-discipline]]
- [[00-governance/templates/review]]
