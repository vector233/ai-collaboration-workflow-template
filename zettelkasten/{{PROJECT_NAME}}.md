# {{PROJECT_NAME}}

> {{PROJECT_DESCRIPTION}}

This note is the human-readable project index. The AI-facing entry point is [[CLAUDE]].

## Quick Positioning

- **What it is**: {{PROJECT_DESCRIPTION}}
- **Tech stack**: {{TECH_STACK}}
- **Domains and ports**: see [[01-overview/quick-reference]]

<!-- UMBRELLA-ONLY: keep this block only if {{REPO_TYPE}} == umbrella -->

## Subprojects

{{SUB_PROJECTS}}

Each subproject should keep implementation-specific details in its own `AGENTS.md`, `CLAUDE.md`, or `zettelkasten/`.

<!-- /UMBRELLA-ONLY -->

## Repositories

{{REPOS}}

## Must-Read Notes

| Note | Purpose |
|---|---|
| [[CLAUDE]] | AI entry point: method, routing, standard task flow |
| [[00-governance/project-overview]] | Project purpose, stack, and constraints |
| [[00-governance/ai-workflow]] | AI workflow, implementation gate, review, validation, memory writeback |
| [[00-governance/validation-discipline]] | Realistic validation readiness policy |
| [[01-overview/quick-reference]] | Commands, domains, ports, endpoints |
| [[01-overview/product-vision]] | Product direction and audience |
| [[00-governance/decisions]] | Architecture decision records |
| [[00-governance/gotchas]] | Known bugs, root causes, and fixes |
| [[03-roadmap/phases]] | Roadmap and phase status |
| [[06-requirements/README]] | Requirement workflow |
| [[07-review/README]] | Review handoff workflow |
| [[08-technical-designs/README]] | Technical design workflow |

## External Documents

<!-- List external documents that are strongly related to this knowledge base.

Example:

- Source: `../PROJECT_PRD.md`
- Summary: `05-reference/prd.md`
-->
