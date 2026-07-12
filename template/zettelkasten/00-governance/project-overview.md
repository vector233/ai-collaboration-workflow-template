# Project Overview — {{PROJECT_NAME}}

## Product Positioning

**{{PROJECT_NAME}} is {{PROJECT_DESCRIPTION}}.**

<!-- Add 2-4 sentences describing the problem, target users, and core value. -->

## Naming Rules

<!-- If the project has multiple names, brand migrations, product slugs, or legacy repo names, define them here.

- Public product name:
- Machine-readable slug:
- Legacy names that may remain in old files:
-->

## Tech Stack

{{TECH_STACK}}

<!-- Optional detailed stack table:

| Component | Technology |
|---|---|
| Backend | TypeScript · Node.js · PostgreSQL |
| Frontend | Next.js · React · Tailwind CSS |
| Auth | Session cookies · OAuth |
-->

<!-- UMBRELLA-ONLY: keep this section only if {{REPO_TYPE}} == umbrella -->

## Subprojects

{{SUB_PROJECTS}}

<!-- /UMBRELLA-ONLY -->

## Project Constraints

<!-- Capture project-level non-negotiables. Examples:

- Workspace isolation: every data access path must enforce a workspace boundary.
- Auditability: write operations must leave an audit trail.
- Privacy: logs must not include sensitive payloads.
-->

## AI Collaboration Rules

- Route work through Direct, Tracked, or Governed mode using [[00-governance/ai-workflow]].
- Keep tracked state in one stable `WORK-*` under [[06-work/README]] unless an independent artifact is justified.
- Promote repeatable procedures through [[00-governance/skill-lifecycle]].
- Use task branches and dedicated worktrees for parallel work as defined in [[00-governance/git-collaboration]].
- Write architecture facts, validation procedures, gotchas, and project rules back to their durable destinations.

## See Also

- [[00-governance/ai-workflow]] — AI collaboration workflow
- [[01-overview/product-vision]] — product direction and audience
- [[02-architecture/current-architecture-flow]] — current architecture flow
- [[00-governance/glossary]] — terminology
- [[00-governance/decisions]] — architecture decisions
