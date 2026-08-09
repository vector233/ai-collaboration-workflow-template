# Workflow Routing

## Decision Dimensions

Evaluate scope, uncertainty, risk and reversibility, duration, coordination, and verification independently. Do not use code-diff size as the only proxy.

## Routes

### Direct

Use when work is local, reversible, low-risk, obvious, and can finish in one coherent context. Examples include typos, links, comments, formatting, and focused non-behavioral cleanup.

Do not create a WORK artifact. Validate and commit the context.

### Tracked

Use when behavior changes, debugging context must survive, work spans contexts, or acceptance and validation need durable state.

Create one `WORK-*` from `zettelkasten/templates/work-item.md`. Keep approach, slices, validation, inline review, checkpoints, and experience candidates in that file. The bundled WORK helper may automate this edit but is not required.

### Governed

Use when independent decisions, approvals, or coordination are required. Hard triggers include schema or data migration, security and permissions, billing, production deployment, destructive operations, important compatibility contracts, unresolved architecture, multiple repositories, and multi-owner release sequencing.

Use one `WORK-*`. Record each decision or approval as a governed gate with an owner, required evidence, and status. Link project-native Issues, pull requests, release records, or external approvals when they own part of the lifecycle.

## Route Output

Record selected route, user override, governed gates, isolation mode, affected paths, and validation strategy. Re-route when new risk or uncertainty appears.

## Large Requirement Decomposition

Run this check before using slices to represent a long-lived requirement:

- one coupled acceptance, rollback, and release boundary -> one WORK with bounded slices;
- independently acceptable, assignable, testable, reversible, or releasable outcomes -> separate WORK records;
- durable facts or procedures -> linked knowledge, decisions, runbooks, or project Skills rather than more WORK history.

Use an existing Jira, GitHub, GitLab, or other project-native Epic, Issue, or Milestone as the parent whenever it already owns coordination. Record that authority in each child WORK's `external_parent` and do not mirror its lifecycle locally.

When repository-local coordination must survive without a suitable external parent, create one `INITIATIVE-*`. Each child sets `initiative_id`; a child may not also set `external_parent`. Limit the local graph to Initiative -> WORK. Dependencies between WORK records use `depends_on` and do not create another hierarchy level. Resume a child from its own branch and WORK, load the Initiative only for a relevant shared constraint, and do not load siblings by default.
