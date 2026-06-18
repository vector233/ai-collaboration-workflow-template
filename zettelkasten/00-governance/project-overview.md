# Project Overview — AI Collaboration Workflow Template

## Product Positioning

**AI Collaboration Workflow Template is a reusable documentation workflow and companion Skill for long-running software projects built with AI coding agents.**

The project helps AI coding agents and human maintainers preserve project context across sessions. It packages a canonical Markdown knowledge-base payload, an initialization runbook, and a companion Skill that applies requirement, design, validation, review, and memory-writeback gates consistently.

## Naming Rules

- Public product name: AI Collaboration Workflow Template
- Repository slug: `ai-collaboration-workflow-template`
- Skill name: `ai-collaboration-workflow`

## Tech Stack

Markdown · Python 3 · Agent Skills · Obsidian wiki links · Git

| Component | Technology |
|---|---|
| Template payload | Markdown · Obsidian wiki links |
| Bootstrap and validation | Python 3 standard library |
| Agent integration | Agent Skills-compatible `SKILL.md` |
| Distribution | Git · skills.sh · direct payload copy |

## Subprojects

| Subproject | Path | Responsibility |
|---|---|---|
| Template payload | `template/` | Canonical files copied into user repositories |
| Companion Skill | `skills/ai-collaboration-workflow/` | Bootstrap and daily workflow guidance |
| Project maintenance | root `zettelkasten/` | Requirements, designs, reviews, architecture, and runbooks for this repository |

## Project Constraints

- The canonical downstream payload lives only under `template/`.
- Repository-maintenance documents must not leak into downstream projects.
- Bootstrap must preserve differing existing files by default.
- Installation paths must be testable without relying on an AI reconstructing missing directories.
- Canonical template rules remain English-first; translations explain usage without duplicating the payload.

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
