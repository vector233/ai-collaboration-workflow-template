# Workflow Routing

## Decision Dimensions

Evaluate scope, uncertainty, risk and reversibility, duration, coordination, and verification independently. Do not use code-diff size as the only proxy.

## Routes

### Direct

Use when work is local, reversible, low-risk, obvious, and can finish in one coherent context. Examples include typos, links, comments, formatting, and focused non-behavioral cleanup.

Do not create WORK, TECH, PLAN, or REVIEW artifacts. Validate and commit the context.

### Tracked

Use when behavior changes, debugging context must survive, work spans contexts, or acceptance and validation need durable state.

Create one `WORK-*` from `zettelkasten/00-governance/templates/work-item.md`. Keep approach, slices, validation, inline review, checkpoints, and experience candidates in that file.

### Governed

Use when independent decisions, approvals, or coordination are required. Hard triggers include schema or data migration, security and permissions, billing, production deployment, destructive operations, important compatibility contracts, unresolved architecture, multiple repositories, and multi-owner release sequencing.

Start with a `WORK-*`. Create:

- TECH only for an independent technical decision or approval;
- PLAN only for independent sequencing, ownership, or recovery coordination;
- REVIEW only for an independent reviewer, multiple rounds, high risk, or distinct approval lifecycle.

## Route Output

Record selected route, user override, optional-artifact decisions, isolation mode, affected paths, and validation strategy. Re-route when new risk or uncertainty appears.
