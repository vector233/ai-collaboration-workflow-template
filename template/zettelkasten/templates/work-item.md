---
title: Work Item Title
status: backlog
project: {{PROJECT_NAME}}
work_id: WORK-YYYYMMDDHHMMSS-short-name
initiative_id: ""
external_parent: ""
depends_on: []
route: tracked
risk: normal
branch: task/work-id-short-name
worktree: current
owned_paths: []
next_action: clarify acceptance criteria
last_verified_at: YYYY-MM-DD
related: []
---

# Work Item Title

## Parent Coordination

- Local initiative: use `initiative_id` only when a repository-local Initiative is the coordination authority.
- External parent: use `external_parent` when Jira, GitHub, GitLab, or another tracker owns the Epic or parent lifecycle.
- Dependencies: `depends_on` contains WORK IDs that must complete before this delivery unit can proceed.
- Boundary: a WORK cannot parent another WORK or Initiative. Large coordination has at most one Initiative layer.

## Goal And Acceptance

- Problem or opportunity:
- Goal:
- Non-goals:

### Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Route Decision

| Dimension | Assessment | Evidence or reason |
|---|---|---|
| Scope | low / elevated |  |
| Uncertainty | low / elevated |  |
| Risk and reversibility | low / elevated / high |  |
| Duration | one context / multiple contexts |  |
| Coordination | one owner / parallel or multi-owner |  |
| Verification | focused / realistic / independent |  |

- Selected route: tracked / governed
- User override, if any:
- Isolation: task branch / dedicated worktree

## Governed Gates

Leave this section empty for tracked work. For governed work, each gate needs an owner and verifiable closing evidence.

| Gate or decision | Owner or approver | Required evidence | Status |
|---|---|---|---|
|  |  |  | pending |

## Context Pack

- Confirmed facts:
- Open questions:
- Architecture notes:
- Runbooks:
- Matching project Skills:
- Code entry points:

## Scope And Ownership

- Affected modules:
- Owned paths: include this stable WORK and its `work/active/<ID>.ref.md` route.
- Interfaces or data affected:
- Parallel work overlap:
- Dependencies:

## Technical Approach

- Confirmed cause or approach:
- Compatibility and rollback:
- Durable decision or architecture note updated:

## Execution Slices

| Slice | Deliverable | Depends on | Owned paths | Validation | Status |
|---|---|---|---|---|---|
| S1 |  |  |  |  | pending |

## Validation

- Commands or flows:
- Expected signal:
- Actual result:
- Blockers and residual risk:

## Review

- Review mode: inline / independent / waived
- Reviewer or source:
- Evidence and findings:
- Judgment and fixes:
- Linked Issue, pull request, or approval record, if any:

## Experience Candidates

The active WORK owns each pending candidate. During the Learning Check, capture evidence before promotion. Before editing a shared destination, add its path to `owned_paths` and check overlap with active work. Search first and update the canonical destination; a repeated promotion should record a no-op instead of creating a duplicate. Write durable learning as a reviewable task-branch diff, never as hidden agent memory.

| Candidate | Reuse shape | Decision | Destination | Evidence and content written or reason not promoted |
|---|---|---|---|---|
|  | rule / gotcha / fact / runbook / project-skill / workflow-feedback | pending |  |  |

## Context Checkpoint

Update after a bounded slice and before handoff, long pause, agent or session switch, detectable context compaction, or a yield that would otherwise leave chat-only state. These fields must be enough for a fresh agent to resume without prior conversation.

- Last completed step:
- Commit:
- Validation:
- Worktree status:
- Risks or unresolved decisions:
- Next allowed action:

## Closure

- Acceptance complete: yes / no
- Required gates closed: yes / no
- Experience Promotion complete: yes / no
- Durable writeback complete: yes / no
- Integration result:
