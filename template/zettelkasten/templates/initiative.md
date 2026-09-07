---
title: Initiative Title
status: backlog
project: {{PROJECT_NAME}}
initiative_id: INITIATIVE-YYYYMMDDHHMMSS-short-name
next_action: define independently deliverable child work
last_verified_at: YYYY-MM-DD
related: []
---

# Initiative Title

## Goal And Boundaries

- Problem or opportunity:
- Goal:
- Non-goals:
- Why one WORK is insufficient:

## Overall Acceptance

- [ ] Outcome 1
- [ ] Outcome 2

## Shared Decisions And Gates

Record only decisions or gates that constrain more than one child. Keep child-specific approval and evidence in that child WORK, and link durable architecture decisions instead of copying them here.

| Decision or gate | Owner | Applies to | Evidence | Status |
|---|---|---|---|---|
|  |  |  |  |  |

## Decomposition Contract

Child membership is canonical in each `WORK-*` frontmatter through `initiative_id`. Do not copy child status or validation logs into this file. For current coordination, use open-work routes; scoped rollups omit unreferenced historical children. For final closure, explicitly audit the full stable WORK set for this initiative ID. See [[knowledge-lifecycle]].

- Decomposition rule: one Initiative level followed by independent WORK records; no recursive Initiative or parent-WORK tree.
- Child independence: each child has its own route, acceptance, branch, validation, checkpoint, and closure.
- Dependency rule: record execution dependencies in each child `depends_on`; siblings remain independently resumable.
- External tracker: when an Epic, Issue, or Milestone already owns coordination, do not create this local Initiative; link the external parent directly from each child WORK.

## Integration And Closure

- Integration order:
- Overall validation:
- Unresolved cross-child risk:
- Final outcome:

Maintain this Initiative's own `work/active/<ID>.ref.md` route; remove it on closure. An Initiative may become `done` only after a full membership check confirms its children are terminal and the overall acceptance and shared gates are resolved. Child status remains authoritative in each WORK.

## Coordination Checkpoint

- Completed coordination step:
- Child rollup:
- Shared validation or decision evidence:
- Risks or unresolved decisions:
- Next allowed coordination action:
