---
title: Work Items
status: active
project: {{PROJECT_NAME}}
last_verified_at: YYYY-MM-DD
source_of_truth: project
related:
  - "[[workflow]]"
  - "[[git-collaboration]]"
  - "[[skill-lifecycle]]"
---

# Work Items

Tracked and governed work items live in this directory for their entire lifecycle. Never move a file to represent status; update frontmatter in place.

## Artifact Types

| Prefix | Purpose | Typical states |
|---|---|---|
| `INITIATIVE-*` | optional thin coordination record for multiple independent WORK outcomes | backlog, active, blocked, review, done, cancelled |
| `WORK-*` | canonical task state, governed gates, validation, review, and handoff | backlog, active, blocked, review, done, cancelled |

## Naming

Use stable timestamped IDs:

- `WORK-YYYYMMDDHHMMSS-short-name.md`
- `INITIATIVE-YYYYMMDDHHMMSS-short-name.md`

## Bounded Hierarchy

Keep hierarchy optional and limited to two levels:

1. An external Epic, Issue, or Milestone is the preferred parent when it already owns planning and reporting. Each local WORK links it through `external_parent`; do not mirror the parent lifecycle in Markdown.
2. Without a suitable external parent, one local `INITIATIVE-*` may coordinate multiple independently deliverable WORK records. Each child declares the Initiative through `initiative_id`.
3. A WORK never parents another WORK or Initiative. Each child remains branch-bound, independently resumable, and independently closable.

Use an Initiative because delivery boundaries differ, not merely because a document crossed an arbitrary line count. Split when outcomes can be accepted, routed, assigned, validated, rolled back, or released independently. Keep a single WORK when the activity is still one tightly coupled delivery, and move durable facts into linked Zettels, decisions, runbooks, or project Skills instead of growing an execution log.

Initiative membership is derived from child WORK frontmatter. The Initiative stays thin: overall goal, cross-child acceptance, shared gates, integration order, rollup, and next coordination action. Child status, detailed validation, implementation history, and experience decisions remain authoritative in each WORK.

`depends_on` is a strict execution prerequisite: a dependent WORK remains `backlog` or `blocked` until every referenced WORK is `done`. Use prose coordination rather than `depends_on` when work may proceed in parallel and only final integration ordering matters.

## Resume Contract

Inspect the current Git branch, select the matching active WORK, and read its context pack, checkpoint, validation, and next action. Load its Initiative only when the child links one and the parent contains a shared gate, dependency, or integration constraint needed for the current slice. Do not load sibling WORK records by default and do not maintain a second manual current-state document.

A recoverable WORK lets an agent with no prior chat identify the selected route, acceptance state, latest completed step and commit, exact validation, unresolved risk or decision, next allowed action, pending or decided experience candidates, and matching project Skill while loading only linked knowledge. It distinguishes existing active knowledge from candidates that still need evidence or a promotion decision. That semantic result matters more than file existence alone.

Use a Fresh-Agent Resume Probe for important multi-context handoffs or after changing the resume contract. Routine checkpoints require only normal structural checks; the probe is not a per-task ceremony. See [[validation-policy]].

Update the Markdown file directly. Optional companion-Skill helpers may automate creation, status inspection, and closure without owning any separate state.
