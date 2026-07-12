# {{PROJECT_NAME}} — AI Project Knowledge Base

## Purpose

This knowledge base is written for AI coding agents. Its job is to turn a new task into the smallest useful context, a clear requirement, the right amount of design and planning, focused implementation and validation, a review handoff, rule-promotion decisions, and durable memory writeback.

It is not a linear documentation site. The useful object is the network of notes and links.

The human-readable project index is [[{{PROJECT_NAME_SAFE}}]].
The current resume snapshot is [[CURRENT]].

## Cross-Agent Entry Points

| Agent | Automatic project instruction entry | Shared knowledge entry |
|---|---|---|
| Codex | `AGENTS.md` | this file |
| Claude Code | `CLAUDE.md`, which imports `AGENTS.md` | this file |
| Other repository-aware agents | explicitly read `AGENTS.md` | this file |

Agent-local memory and chat history may help an individual session, but they are never required project state. A fresh agent must be able to reconstruct the current task, implementation gate, validation evidence, risks, and next allowed action from committed or visible repository files.

## Core Wiki-Link Rules

1. **Atomic notes**: one concept or workflow per note.
2. **Wiki-style links**: use `[[01-overview/quick-reference]]` and `[[00-governance/ai-workflow]]` to connect related notes.
3. **No orphan notes**: a new note must link to at least one existing note.
4. **Inbound links prove relevance**: notes with no inbound links are candidates for deletion, merge, or better indexing.
5. **Update in place**: when a linked note changes, update that note instead of changing all incoming links.
6. **Prefer explicit paths**: use `[[02-architecture/current-architecture-flow]]` instead of a bare filename when possible.

## Vault Structure

```text
zettelkasten/
  AI.md                             <- AI-facing entry point
  CURRENT.md                        <- active work and next-action snapshot
  {{PROJECT_NAME_SAFE}}.md           <- human-readable project index
  00-governance/
    project-overview.md              <- project purpose, stack, constraints
    ai-workflow.md                   <- AI task workflow, gates, validation, rule promotion, writeback
    external-skill-interoperability.md <- optional external workflow mapping
    validation-discipline.md         <- realistic validation policy
    glossary.md                      <- project terms
    decisions.md                     <- architecture decisions and rationale
    gotchas.md                       <- bugs, root causes, and lessons
    templates/                       <- requirement, technical design, implementation plan, review templates
  01-overview/
    quick-reference.md               <- commands, URLs, ports, accounts, endpoints
    product-vision.md                <- positioning and audience
  02-architecture/
    current-architecture-flow.md     <- current system flow
    README.md                        <- architecture note rules
  03-roadmap/
    phases.md                        <- roadmap and phase status
  04-cross-cutting/
    README.md                        <- umbrella/cross-module concerns
  05-reference/
    README.md                        <- summarized long docs and runbooks
    e2e-test.md                      <- project-specific validation runbook
  06-requirements/
    README.md                        <- requirement workflow and board
    backlog/                         <- identified but not active
    in-progress/                     <- analysis, design, implementation, or validation
    done/                            <- complete with docs writeback
  07-review/
    README.md                        <- review handoff workflow
    pending/                         <- waiting for review
    in-review/                       <- feedback being evaluated or fixed
    done/                            <- closed review
  08-technical-designs/
    README.md                        <- optional standalone design workflow
    pending/                         <- proposed, not yet implementation input
    approved/                        <- approved implementation input
    implemented/                     <- implemented and written back
  09-implementation-plans/
    README.md                        <- optional detailed execution planning
```

Directories are physical organization. Double-bracket wiki links are the retrieval system.

## Syntax Compatibility

This vault is Obsidian-compatible Markdown.

Use these defaults:

| Use case | Syntax | Reason |
|---|---|---|
| Link between project notes | `[[02-architecture/current-architecture-flow]]` | Compact Obsidian wiki link; useful for graph navigation |
| External URL | `[label](https://example.com)` | Standard Markdown; readable in GitHub and Obsidian |
| Image or asset that should render on GitHub | `![alt](assets/example.png)` | Standard Markdown image syntax |
| Obsidian-only file embed | `![[example.png]]` | Valid in Obsidian, but do not expect GitHub to render it |

Prefer wiki links for note-to-note navigation inside `zettelkasten/`. Prefer standard Markdown for external links and images that should render outside Obsidian.

## Task Routing

| Task type | Start here |
|---|---|
| Current active work, open reviews, and next action | [[CURRENT]] |
| AI workflow, gates, review, rule promotion, memory writeback | [[00-governance/ai-workflow]] |
| Commands, URLs, ports, accounts | [[01-overview/quick-reference]] |
| Product scope and audience | [[01-overview/product-vision]] |
| Current architecture | [[02-architecture/current-architecture-flow]] |
| Architecture decisions | [[00-governance/decisions]] |
| Known bugs and lessons | [[00-governance/gotchas]] |
| Requirement workflow | [[06-requirements/README]] |
| Technical design workflow | [[08-technical-designs/README]] |
| Implementation planning | [[09-implementation-plans/README]] |
| Review workflow | [[07-review/README]] |
| Validation policy | [[00-governance/validation-discipline]] |
| External process Skill conflicts | [[00-governance/external-skill-interoperability]] |

## Standard Task Flow

1. **Classify**: feature, bugfix, review feedback, architecture change, documentation, validation, release, or research.
2. **Load context**: read this file, [[00-governance/ai-workflow]], and the minimum linked notes for the task.
3. **Check current state**: read [[CURRENT]], then find or create the related requirement under [[06-requirements/README]].
4. **Choose the delivery path**: record whether standalone TECH and PLAN documents are required.
5. **Check implementation readiness**: approve required TECH/PLAN artifacts, or complete inline readiness and slices in the REQ.
6. **Check review state**: if an earlier handoff is open under [[07-review/README]], handle it before starting the next implementation slice.
7. **Implement and validate the slice**: keep edits inside declared paths and run the smallest meaningful checks.
8. **Create review handoff**: record scope, commit, validation, worktree status, risks, and review focus.
9. **Handle feedback with evidence**: verify reviewer claims before fixing or rejecting.
10. **Run the Rule Promotion Check and close**: decide whether repeated lessons should become project rules, then update architecture, gotchas, runbooks, boards, or reference notes when durable facts change.

Use `python3 scripts/workflow_doctor.py` to check workflow state after changing requirements, designs, plans, review handoffs, wiki links, or initialization files.

Update [[CURRENT]] when active work, open review state, validation status, or next allowed action changes.

`in-progress` means a requirement is active. It does not automatically mean implementation is allowed. The REQ's recorded TECH/PLAN decisions determine readiness.

## When To Update The Knowledge Base

Update notes when any of these change:

- Architecture, data flow, API contract, permission model, deployment, or persistence behavior.
- Build, lint, test, E2E, browser, or realistic-environment validation procedure.
- Product scope, target audience, pricing, launch plan, or roadmap.
- A bug root cause, false assumption, or reviewer lesson worth remembering.
- Subproject ownership, module boundaries, or task handoff rules.

## Relationship To Project Code

The root `AGENTS.md` defines repository-wide agent rules. This zettelkasten defines durable project context and task workflow. Subprojects can add their own `AGENTS.md`, `CLAUDE.md`, or `zettelkasten/` for module-specific details.

For umbrella repositories, the top-level zettelkasten owns cross-project architecture and governance. Subproject notes own module-level implementation details.
