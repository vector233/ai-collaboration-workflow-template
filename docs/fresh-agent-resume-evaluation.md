# Fresh-Agent Resume Evaluation

Use this maintainer evaluation to verify semantic recovery: a fresh agent can resume from repository state without chat history. File and field checks are structural validation; they do not prove that an agent can reconstruct the work correctly.

## When To Run

Run this probe after changing workflow or resume semantics, before a release that changes the payload, or for an important multi-context handoff where failed recovery would be costly. It is not a routine per-task gate.

## Setup

Prepare an initialized temporary project with:

- one active `WORK-*` on a task branch;
- at least one completed context checkpoint and commit;
- validation evidence and a next action;
- one experience candidate;
- optionally one matching project Skill and linked project-native approval evidence.

First confirm structurally that the branch maps to one active WORK, checkpoint fields and links exist, shared knowledge destinations are declared in `owned_paths`, and project Skills are reachable from the index. The semantic probe starts only after those checks pass.

## Prompt

```text
Review this repository's current project state using only repository files and Git. Start from AGENTS.md and zettelkasten/AI.md, identify the work item matching the current branch, and report its selected route, acceptance state, last checkpoint and commit, validation evidence, unresolved risk, next allowed action, pending or decided experience candidates, and any matching project Skill. Distinguish an existing active Skill from a candidate that has not been promoted or updated yet. Do not run companion workflow helpers and do not edit files.
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

## Evidence Integrity

Record the repository commit and branch, exact prompt, unedited response, agent and model identifier, and run time. Keep generated run output outside the canonical payload unless a sanitized maintainer record is explicitly needed.

Do not give the fresh agent this scorecard, an expected answer, a previous response, or the conclusions being tested. A synthetic or copied response may test a score parser, but it must never be reported as Fresh-Agent behavior evidence.

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

Record the run provenance with the scorecard. A passing structure validator and a missing real-agent run must be reported separately, not combined into one PASS.

Record which unnecessary files the agent loaded. Context breadth is a regression signal even when the final answer is correct.
