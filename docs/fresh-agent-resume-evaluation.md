# Fresh-Agent Resume Evaluation

Use this maintainer evaluation to verify that a fresh agent can resume from repository state without chat history.

## Setup

Prepare an initialized temporary project with:

- one active `WORK-*` on a task branch;
- at least one completed context checkpoint and commit;
- validation evidence and a next action;
- one experience candidate;
- optionally one matching project Skill and one independent governed artifact.

## Prompt

```text
Review this repository's current project state. Start from AGENTS.md and zettelkasten/AI.md, run the workflow status command, and identify the work item matching the current branch. Report its selected route, acceptance state, last checkpoint and commit, validation evidence, unresolved risk, next allowed action, and any matching project Skill. Do not edit files.
```

## Pass Criteria

- reads `AGENTS.md` and `zettelkasten/AI.md`;
- uses `workflow_doctor.py --status` instead of scanning every work file;
- selects the correct stable WORK file for the branch;
- does not require `CURRENT.md` or chat history;
- loads only linked knowledge and matching project Skills;
- reports exact validation and commit evidence;
- distinguishes pending experience candidates from promoted knowledge;
- recognizes any governed TECH, PLAN, or REVIEW gate;
- does not begin implementation before reporting the next allowed action.

## Scorecard

| Check | Result |
|---|---|
| Correct active WORK | pass / fail |
| Correct route and gates | pass / fail |
| Correct checkpoint and commit | pass / fail |
| Correct validation and risk | pass / fail |
| Correct next action | pass / fail |
| Minimal context behavior | pass / fail |
| Project Skill retrieval | pass / fail / not applicable |

Record which unnecessary files the agent loaded. Context breadth is a regression signal even when the final answer is correct.
