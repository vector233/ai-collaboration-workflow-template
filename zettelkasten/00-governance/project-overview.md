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

- Non-trivial work goes through [[06-requirements/README]] and [[08-technical-designs/README]] before implementation.
- Review handoffs live under [[07-review/README]], and review feedback must be evidence-backed.
- New architecture facts, validation procedures, and gotchas must be written back to durable notes.
- Parallel AI work must declare non-overlapping file ownership in the requirement or review handoff.

## See Also

- [[00-governance/ai-workflow]] — AI collaboration workflow
- [[01-overview/product-vision]] — product direction and audience
- [[02-architecture/current-architecture-flow]] — current architecture flow
- [[00-governance/glossary]] — terminology
- [[00-governance/decisions]] — architecture decisions
