# AI Collaboration Workflow Template

A Zettelkasten-style, Obsidian-compatible documentation template for long-running software projects built with AI coding agents.

This repository packages a practical AI collaboration workflow. It gives agents a durable project memory, explicit requirement and design gates, evidence-based review handoffs, and a place to write back lessons after each slice of work.

## Quick Start

1. Install the companion Skill and ask:

   ```text
   Use $ai-collaboration-workflow to initialize this repository.
   ```

   Or copy the canonical payload into an existing repository:

   ```bash
   cp -R /path/to/ai-collaboration-workflow-template/template/. /path/to/your-project/
   ```

2. If you copied the payload manually, ask your AI coding assistant:

   ```text
   Initialize this knowledge base by following INIT.md.
   ```

3. Start non-trivial work with the workflow below.

```text
Task
  -> REQ       define scope, non-goals, and acceptance criteria
  -> [TECH]    add a standalone technical design when risk or uncertainty requires it
  -> [PLAN]    add a standalone execution plan when coordination requires it
  -> Build     implement one bounded slice and run meaningful validation
  -> REVIEW    hand off evidence, feedback, and risk
  -> Writeback update durable knowledge and close the loop
```

| Stage | Artifact | Purpose |
|---|---|---|
| Requirement | `REQ-*` | Define what changes and how it will be accepted |
| Technical design, optional | `TECH-*` | Resolve architecture, contract, risk, and operational decisions |
| Implementation plan, optional | `PLAN-*` | Make dependencies, ownership, sequence, and checkpoints explicit |
| Implementation and validation | Code/docs slice plus evidence | Keep the change bounded and verify the changed boundary |
| Review | `REVIEW-*` | Preserve feedback, evidence, and risk |
| Writeback | Architecture/gotchas/runbooks | Keep future agents from rediscovering context |

## What It Solves

AI coding agents are strong at local implementation but weak at long-lived project continuity unless the project gives them structure. This template turns project documentation into a lightweight operating workflow:

- **Context pack**: agents read the smallest necessary context instead of re-discovering the whole repo.
- **Requirement workflow**: every non-trivial change has scope, acceptance criteria, and known non-goals.
- **Adaptive design and planning**: standalone TECH and PLAN documents are used when risk or coordination justifies them; bounded bugs can keep the necessary reasoning inside the REQ.
- **Review handoff**: review feedback is treated as a hypothesis that needs evidence and independent verification.
- **Validation discipline**: build, test, browser, integration, and realistic-environment checks are recorded where future agents can find them.
- **Memory writeback**: architecture changes, test procedures, and gotchas are written back into the knowledge base.

The default template is intentionally plain: no specialized process jargon, no heavy role system, and no requirement to run multiple agents.

## Zettelkasten Inspiration

This template is inspired by the Zettelkasten note-taking method: small notes, explicit links, and knowledge that grows through connections instead of one large document. In this project, that idea is adapted for AI coding agents: requirements, technical designs, review handoffs, architecture notes, validation runbooks, and gotchas are separate notes that link to each other.

The goal is practical retrieval. A future agent should be able to start from a task, follow links to the minimum context, do the work, and write back what changed.

## Obsidian And Markdown Compatibility

The knowledge base is designed to work well as an Obsidian vault, but it stays close to plain Markdown where that helps GitHub readability.

| Use case | Preferred syntax | Notes |
|---|---|---|
| Link between notes in `zettelkasten/` | `[[00-governance/ai-workflow]]` | Obsidian-compatible wiki link; compact and good for graph navigation |
| External links | `[label](https://example.com)` | Standard Markdown; works in Obsidian and GitHub |
| Images or assets that should render on GitHub | `![alt](assets/example.png)` | Standard Markdown image syntax |
| Obsidian-only embeds | `![[example.png]]` | Good inside Obsidian, but not rendered by GitHub Markdown |

Obsidian supports both wiki links and Markdown links for internal notes. This template uses wiki links for project-note navigation because the Zettelkasten graph is the core workflow. Use standard Markdown links and images when the content should render cleanly outside Obsidian.

## Language

The template is English-first. Keeping the canonical version in one language reduces drift and makes the project easier to reuse globally. Translations can be added later as guides under `docs/zh-CN/` without duplicating the full template.

Chinese guide: [docs/zh-CN/README.md](docs/zh-CN/README.md).

## Structure

```text
.
├── template/                  # Canonical downstream payload
│   ├── AGENTS.md
│   ├── CLAUDE.md
│   ├── INIT.md
│   └── zettelkasten/
├── skills/
│   └── ai-collaboration-workflow/
├── scripts/
│   └── validate_distribution.py
├── docs/                      # Maintainer and publishing documentation
└── examples/                  # Fictional initialized-project walkthroughs
```

Only `template/` is downstream project content. The repository intentionally has no second root knowledge base, which keeps product files distinct from maintainer documentation.

## Install The Template Payload

1. Use the Skill bootstrap, or copy everything under `template/` into the target repository. This includes `INIT.md`.
2. In your AI coding tool, say:

   ```text
   Initialize this knowledge base by following INIT.md.
   ```

3. Answer the initialization questions.
4. Let the agent replace placeholders, merge project-specific `AGENTS.md` rules, prune single-repo or umbrella-only sections, create the first notes, and remove `INIT.md`. Commit only when requested or required by repository policy.

Do not treat the full repository root as the install payload. GitHub's template-repository feature copies maintenance files as well, so the supported clean installation surfaces are the Skill and `template/`.

## Daily Workflow In An Initialized Project

For non-trivial work, agents should follow this loop:

1. Read `AGENTS.md`, `zettelkasten/AI.md`, and `zettelkasten/00-governance/ai-workflow.md`.
2. Find or create the relevant requirement under `zettelkasten/06-requirements/`.
3. In the REQ, decide whether standalone TECH and PLAN documents are required.
4. Approve required TECH/PLAN artifacts, or complete inline readiness and slices in the REQ.
5. Implement only the current slice and run the smallest meaningful validation.
6. Create or update a review handoff under `zettelkasten/07-review/`.
7. Handle reviewer feedback with evidence, then write durable lessons back to `00-governance/gotchas.md`, `02-architecture/`, or `05-reference/`.

See `examples/example-saas/` for a fictional end-to-end walkthrough.

To evaluate whether a fresh agent can resume from repository state alone, use [docs/fresh-agent-resume-evaluation.md](docs/fresh-agent-resume-evaluation.md).

## Cross-Agent Compatibility

The workflow is vendor-neutral; tool-specific files are thin adapters:

| Agent | Project instruction entry | Shared workflow state |
|---|---|---|
| Codex | `AGENTS.md` | `zettelkasten/` |
| Claude Code | `CLAUDE.md` imports `AGENTS.md` | `zettelkasten/` |
| Other repository-aware agents | explicitly read `AGENTS.md` | `zettelkasten/` |

Required project state must not live only in a chat transcript, Codex memory, Claude auto memory, or another agent's private state. A different agent must be able to resume from the active REQ, any controlling TECH or PLAN, open REVIEW, validation evidence, worktree state, risks, and next allowed action.

The companion Skill follows the open Agent Skills format used by both Codex and Claude Code, but the core workflow does not depend on the Skill being installed after initialization.

## Optional External Process Skills

The initialized template does not require Superpowers or any other process plugin. Codex, Claude Code, and other repository-aware agents can use `REQ -> [TECH] -> [PLAN] -> implementation and validation -> REVIEW -> writeback` with only the files in the target repository.

If Superpowers is installed, repository instructions map its brainstorming, planning, TDD, debugging, and review methods into the selected REQ, TECH, PLAN, REVIEW, gotcha, and runbook documents. It must not create a parallel `docs/superpowers/` source of truth.

This is compatibility only:

- no external plugin is installed by the template;
- no external command is required;
- standalone TECH and PLAN artifacts remain optional unless the REQ marks them required;
- removing or disabling the external plugin does not change the repository workflow.

## Companion Skill

This repository includes an optional Agent Skills-compatible skill:

```text
skills/ai-collaboration-workflow/
```

Use it when you want an AI agent to apply the template consistently: initialize a project, create REQ/TECH/PLAN/REVIEW documents when appropriate, check implementation readiness, record validation, handle evidence-based review feedback, and write lessons back to the knowledge base.

The skill is a companion to the template. If you invoke it in a project that does not yet contain `AGENTS.md`, `CLAUDE.md`, and `zettelkasten/`, it can safely bootstrap the template before continuing. Its bootstrap script previews changes, copies only missing files, skips identical files, and leaves differing existing files untouched for explicit merging.

Install with skills.sh:

```bash
npx skills add vector233/ai-collaboration-workflow-template \
  --skill ai-collaboration-workflow \
  -a claude-code \
  -g
```

### Install For Claude Code

Personal install, available across all Claude Code projects:

```bash
mkdir -p ~/.claude/skills
cp -R skills/ai-collaboration-workflow ~/.claude/skills/
```

Project install, committed to one repository:

```bash
mkdir -p .claude/skills
cp -R skills/ai-collaboration-workflow .claude/skills/
git add .claude/skills/ai-collaboration-workflow
```

Then start Claude Code in the project and invoke:

```text
/ai-collaboration-workflow create a requirement for <task>
```

Claude may also load the skill automatically when your request matches the skill description.

### Install For Codex

```bash
mkdir -p ~/.codex/skills
cp -R skills/ai-collaboration-workflow ~/.codex/skills/
```

Then invoke:

```text
Use $ai-collaboration-workflow to initialize this repository.
```

For an initialized project:

```text
Use $ai-collaboration-workflow to choose the delivery path and create the required workflow artifacts.
```

The default bootstrap source is this canonical Git repository and automatically selects its `template/` directory. For offline use, pass either the repository checkout or `template/` directly with `--source`.

## Distribution Validation

Run:

```bash
python3 scripts/validate_distribution.py
```

The smoke test checks payload isolation, state-directory presence, bootstrap dry-run and installation, sample initialization, wiki links, a bounded REQ-only bug path, and a full REQ/TECH/PLAN/REVIEW path.

## Naming Rules

- Requirements: `REQ-YYYYMMDDHHMMSS-short-name.md`
- Technical designs: `TECH-YYYYMMDDHHMMSS-short-name.md`
- Implementation plans: `PLAN-YYYYMMDDHHMMSS-short-name.md`
- Review handoffs: `REVIEW-YYYYMMDDHHMMSS-short-name.md`

## What To Customize

Start with these files after initialization:

- `AGENTS.md`: repo-specific AI rules, build commands, test discipline, branch policy.
- `zettelkasten/00-governance/project-overview.md`: project purpose, stack, constraints.
- `zettelkasten/01-overview/quick-reference.md`: commands, URLs, ports, test accounts, runbooks.
- `zettelkasten/02-architecture/current-architecture-flow.md`: current system flow.
- `zettelkasten/05-reference/e2e-test.md`: project-specific validation commands.

## License

MIT. Use it, fork it, and adapt it to your own AI engineering workflow.
