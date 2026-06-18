# AI Collaboration Workflow Template

> A reusable documentation workflow and companion Skill for long-running software projects built with AI coding agents

This note is the human-readable project index. The AI-facing entry point is [[AI]].

## Quick Positioning

- **What it is**: A reusable documentation workflow and companion Skill for long-running software projects built with AI coding agents
- **Tech stack**: Markdown · Python 3 · Agent Skills · Obsidian wiki links · Git
- **Domains and ports**: see [[01-overview/quick-reference]]

## Subprojects

| Subproject | Path | Responsibility |
|---|---|---|
| Template payload | `template/` | Canonical downstream project files |
| Companion Skill | `skills/ai-collaboration-workflow/` | Installation and workflow guidance |
| Maintenance knowledge | `zettelkasten/` | This repository's own project memory |

Each subproject should keep implementation-specific details in its own `AGENTS.md`, `CLAUDE.md`, or `zettelkasten/`.

## Repositories

- `vector233/ai-collaboration-workflow-template`

## Must-Read Notes

| Note | Purpose |
|---|---|
| [[AI]] | AI entry point: method, routing, standard task flow |
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
