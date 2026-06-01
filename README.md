# AI Knowledge Base Skeleton

A reusable documentation template for long-running software projects built with AI coding agents.

This repository packages a practical AI collaboration workflow, not just a folder tree. It gives agents a durable project memory, explicit implementation gates, evidence-based review handoffs, and a place to write back lessons after each slice of work.

## What It Solves

AI coding agents are strong at local implementation but weak at long-lived project continuity unless the project gives them structure. This template turns project documentation into an operating system for agents:

- **Context harness**: agents read the smallest necessary context instead of re-discovering the whole repo.
- **Requirement gate**: every non-trivial change has scope, acceptance criteria, and a context pack.
- **Technical design gate**: code work waits for an approved design unless the task is explicitly a tiny low-risk fix.
- **Review harness**: review feedback is treated as a hypothesis that needs evidence and independent verification.
- **Memory writeback**: architecture changes, test procedures, and gotchas are written back into the knowledge base.
- **Role boundaries**: parallel agents get clear owned paths, read-only paths, validation, and handoff rules.

The result is a lightweight project governance template that works with Claude Code, Codex, Cursor, or any capable AI coding assistant.

## Structure

```text
.
├── AGENTS.md                  # Generic agent rules for an initialized project
├── INIT.md                    # AI-run initialization checklist
└── zettelkasten/
    ├── CLAUDE.md              # AI-facing knowledge base entry point
    ├── {{PROJECT_NAME}}.md    # Project index, renamed during init
    ├── 00-governance/         # Agent harness, roles, decisions, gotchas, templates
    ├── 01-overview/           # Quick reference and product vision
    ├── 02-architecture/       # Current architecture notes
    ├── 03-roadmap/            # Phases and release planning
    ├── 04-cross-cutting/      # Umbrella/cross-module concerns
    ├── 05-reference/          # External-doc summaries and runbooks
    ├── 06-requirements/       # Workflow: backlog -> in-progress -> done
    ├── 07-review/             # Workflow: pending -> in-review -> done
    └── 08-technical-designs/  # Workflow: pending -> approved -> implemented
```

## Use As A Template

1. Create a new repository from this template, or copy `AGENTS.md` and `zettelkasten/` into an existing project.
2. In your AI coding tool, say:

   ```text
   Initialize this knowledge base by following INIT.md.
   ```

3. Answer the initialization questions.
4. Let the agent replace placeholders, prune single-repo or umbrella-only sections, create the first notes, remove `INIT.md`, and commit the initialized knowledge base.

## Daily Workflow

For non-trivial work, agents should follow this loop:

1. Read `AGENTS.md`, `zettelkasten/CLAUDE.md`, and `zettelkasten/00-governance/agent-harness.md`.
2. Find or create the relevant requirement under `zettelkasten/06-requirements/`.
3. Confirm the linked technical design is approved under `zettelkasten/08-technical-designs/`.
4. Implement only the current slice and run the smallest meaningful verification.
5. Create or update a review handoff under `zettelkasten/07-review/`.
6. Handle reviewer feedback with evidence, then write durable lessons back to `00-governance/gotchas.md`, `02-architecture/`, or `05-reference/`.

See `examples/example-saas/` for a fictional end-to-end walkthrough.

## Naming Rules

- Requirements: `REQ-YYYYMMDDHHMMSS-short-name.md`
- Technical designs: `TECH-YYYYMMDDHHMMSS-short-name.md`
- Review handoffs: `REVIEW-YYYYMMDDHHMMSS-short-name.md`

## What To Customize

Start with these files after initialization:

- `AGENTS.md`: repo-specific AI rules, build commands, test discipline, branch policy.
- `zettelkasten/00-governance/project-overview.md`: project purpose, stack, constraints.
- `zettelkasten/01-overview/quick-reference.md`: commands, URLs, ports, test accounts, runbooks.
- `zettelkasten/02-architecture/current-architecture-flow.md`: current system flow.
- `zettelkasten/05-reference/e2e-test.md`: project-specific verification commands.

## License

MIT. Use it, fork it, and adapt it to your own AI engineering workflow.
