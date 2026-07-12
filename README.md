# AI Collaboration Workflow Template

A vendor-neutral project knowledge layer for AI-assisted software development.

The template keeps project facts, active work, validation evidence, reusable procedures, and handoff state in the repository so a fresh agent can continue without chat history. It is not an autonomous runtime and does not require every task to create a chain of process documents.

This version is intended for new projects. It does not migrate or emulate the previous moving-state layout.

## Core Model

```text
Task
  -> Route: Direct | Tracked | Governed
  -> Load only the active work item and matched knowledge
  -> Implement, validate, review when needed
  -> Commit every context that produces persistent changes or a coherent slice
  -> Promote reusable experience into rules, notes, runbooks, or project Skills
```

| Route | Use when | Workflow state |
|---|---|---|
| Direct | local, reversible, low-risk, one context | none; validate and commit |
| Tracked | behavior change, debugging continuity, multiple contexts | one stable `WORK-*` |
| Governed | high risk, important uncertainty, independent approval, migration, release, multi-owner coordination | `WORK-*` plus only triggered TECH, PLAN, or REVIEW artifacts |

Routing considers scope, uncertainty, risk, reversibility, duration, coordination, and verification. A small security or data change can be Governed even when its diff is tiny.

## Why It Is Lighter

- Workflow files never move between status directories; frontmatter is the state.
- Ordinary tracked work keeps requirement, approach, slices, validation, review, checkpoint, and experience candidates in one `WORK-*`.
- TECH, PLAN, and REVIEW are optional independent artifacts, not mandatory stages.
- There is no manually duplicated `CURRENT.md`; `workflow_doctor.py --status` resolves active work.
- Project Skills load on demand from a compact trigger index instead of expanding `AGENTS.md`.
- Knowledge categories remain separate where they improve retrieval, but active workflow state is consolidated under one directory.

The knowledge base uses plain Markdown and wiki links and can be opened as an Obsidian-compatible vault. Obsidian is an optional editor, not a runtime dependency or plugin requirement.

## Durable Experience

Each tracked work item has an Experience Candidates table. At context checkpoints and closeout, agents decide whether each lesson should remain local or be promoted:

| Experience | Destination |
|---|---|
| repository-wide mandatory behavior | `AGENTS.md` |
| bug root or false assumption | `zettelkasten/00-governance/gotchas.md` |
| architecture fact or invariant | architecture or cross-cutting note |
| simple setup or validation flow | quick reference or runbook |
| stable conditional multi-step procedure | `project-skills/<name>/SKILL.md` plus `project-skills/INDEX.md` |

Project Skills include concrete triggers, exclusions, procedure, validation, recovery, and provenance. One-off incidents and unverified guesses do not become Skills.

## Parallel Development

Tracked and Governed tasks use dedicated task branches. Concurrent tasks or agents use separate Git worktrees:

```bash
python3 scripts/task_worktree.py create WORK-20260712120000-example --slug example
```

The default branch is integration-only. Shared knowledge updates are normally promoted near task closeout to reduce conflicts between parallel worktrees.

Every agent context that produces persistent changes, or each coherent slice, ends with a task-scoped commit. Read-only analysis does not create an empty commit. Incomplete `checkpoint:` or `wip:` commits may exist on task branches but must not enter the default branch while broken.

## Quick Start

Install the companion Skill and ask:

```text
Use $ai-collaboration-workflow to initialize this repository.
```

Or copy the canonical payload:

```bash
cp -R /path/to/ai-collaboration-workflow-template/template/. /path/to/your-project/
```

Then ask the agent to follow `INIT.md`. Initialization discovers repository facts, merges local instructions, records Git defaults, removes placeholders, and validates the knowledge layer.

## Daily Use

Start with:

```bash
python3 scripts/workflow_doctor.py --status
```

The agent reads `AGENTS.md`, `zettelkasten/AI.md`, the active `WORK-*`, and only the linked notes or matched project Skill. It does not scan the entire vault.

Create tracked work from:

```bash
python3 scripts/workflow_task.py new <slug> --route tracked --owned-path <path>
```

Use `workflow_task.py checkpoint` and `workflow_task.py close` for later state changes. Repeat `--owned-path` on a checkpoint to replace task ownership when scope changes. All WORK, TECH, PLAN, and REVIEW files remain directly under `zettelkasten/06-work/` for their full lifecycle.

For parallel coordination or machine consumers:

```bash
python3 scripts/workflow_doctor.py --status --all-worktrees --json
```

## Structure

```text
template/
  AGENTS.md
  CLAUDE.md
  INIT.md
  scripts/
    workflow_doctor.py
    workflow_task.py
    task_worktree.py
  project-skills/
    INDEX.md
  zettelkasten/
    AI.md
    00-governance/
    01-overview/
    02-architecture/
    03-roadmap/
    04-cross-cutting/
    05-reference/
    06-work/
```

`template/` is the only downstream payload. This maintenance repository intentionally has no second root `zettelkasten/`.

## Companion Skill

The Agent Skills-compatible companion is under `skills/ai-collaboration-workflow/`. It handles installation, task routing, stable work-item updates, minimal context loading, experience promotion, Git isolation, and validation.

Install with:

```bash
npx skills add vector233/ai-collaboration-workflow-template \
  --skill ai-collaboration-workflow \
  -a claude-code \
  -g
```

For Codex, copy it to `~/.codex/skills/`; for Claude Code, copy it to `~/.claude/skills/` or the repository's project-Skill location supported by the tool.

The initialized repository remains usable without the companion Skill. `AGENTS.md` and repository knowledge stay canonical.

## Validation

For a downstream project:

```bash
python3 scripts/workflow_doctor.py --strict
```

The doctor checks required knowledge files, stable artifact names and statuses, active task branches, ambiguous or broken wiki links, knowledge review dates, Experience Promotion closure, and project-Skill structure and routing. Its all-worktree status reports dirty state and possible owned-path overlap.

For this distribution repository:

```bash
python3 scripts/validate_distribution.py
```

The distribution validator exercises bootstrap, initialization, stable work artifacts, project-Skill discovery, worktree isolation, wiki links, and doctor behavior in temporary repositories.

Fresh-agent routing behavior can be checked with [docs/workflow-behavior-evaluation.md](docs/workflow-behavior-evaluation.md).

Chinese guide: [docs/zh-CN/README.md](docs/zh-CN/README.md).

## License

MIT. See [LICENSE](LICENSE).
