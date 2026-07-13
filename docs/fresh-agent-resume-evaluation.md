# Fresh-Agent Resume Evaluation

Use this maintainer evaluation to verify that a fresh agent can resume from repository state without chat history.

## Setup

Prepare an initialized temporary project with:

- one active `WORK-*` on a task branch;
- at least one completed context checkpoint and commit;
- validation evidence and a next action;
- one experience candidate;
- optionally one matching project Skill and linked project-native approval evidence.

## Prompt

```text
Review this repository's current project state using only repository files and Git. Start from AGENTS.md and zettelkasten/AI.md, identify the work item matching the current branch, and report its selected route, acceptance state, last checkpoint and commit, validation evidence, unresolved risk, next allowed action, and any matching project Skill. Do not run companion workflow helpers and do not edit files.
```

## Pass Criteria

- reads `AGENTS.md` and `zettelkasten/AI.md`;
- identifies active work without requiring a helper script or scanning every work file;
- selects the correct stable WORK file for the branch;
- does not require `CURRENT.md` or chat history;
- loads only linked knowledge and matching project Skills;
- reports exact validation and commit evidence;
- distinguishes pending experience candidates from promoted knowledge;
- recognizes governed gates and their closing evidence in the WORK;
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
