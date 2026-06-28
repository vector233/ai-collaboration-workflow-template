# Fresh Agent Resume Evaluation

## Purpose

This evaluation tests the project's core value: whether a new AI coding agent can resume work from repository knowledge without access to the earlier chat.

## Setup

1. Initialize the template in a real or representative software project.
2. Complete at least one REQ and its delivery-path decision. Include any TECH or PLAN selected by the REQ.
3. Implement one bounded slice and create a REVIEW with validation evidence, risks, and next steps.
4. Leave one explicit next action unresolved.
5. Start a fresh agent session with repository access only. Do not provide the previous conversation or a summary.

## Evaluation Prompt

```text
Review this repository's current project state. Identify the active requirement,
any technical design or implementation plan that controls implementation, any open review handoff,
what has been validated, the main residual risks, and the next allowed action.
Also report whether the current REVIEW includes a Rule Promotion Check and whether any promoted rule was written to a durable destination.
Do not modify files.
```

## Pass Criteria

The fresh agent must:

- read `AGENTS.md` and `zettelkasten/AI.md`;
- identify the correct active REQ, its TECH/PLAN decision and state, and open REVIEW;
- distinguish completed work from the next slice;
- report actual validation and untested risks without inventing coverage;
- identify whether the selected delivery path currently allows implementation;
- identify the Rule Promotion Check result or report that it is missing;
- find the correct project-specific validation commands;
- avoid relying on chat history.

## Evidence Record

Record:

| Field | Value |
|---|---|
| Project and commit |  |
| Agent/tool |  |
| Date |  |
| Correct active REQ | pass / fail |
| Correct TECH/PLAN path | pass / fail |
| Correct REVIEW state | pass / fail |
| Correct validation summary | pass / fail |
| Correct rule promotion state | pass / fail |
| Correct next action | pass / fail |
| Hallucinated facts |  |
| Missing context |  |
| Template improvement |  |

## Interpretation

One successful run proves only that the selected project state was recoverable. Repeat across multiple slices and projects before claiming that the workflow reliably preserves long-term context.

## See Also

- [Template payload](../template/)
- [Example walkthrough](../examples/example-saas/README.md)
