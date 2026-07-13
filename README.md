# AI Collaboration Workflow Template

A vendor-neutral project knowledge network and lightweight delivery contract for AI-assisted software development.

The template gives capable but context-temporary, vendor-diverse, and potentially parallel agents the same trusted project knowledge, then makes durable writeback part of delivery. It is not an autonomous runtime and requires no helper tool to remain usable.

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

## Product Boundary

The core product is linked, reviewable repository knowledge plus a lightweight delivery contract. It defines what must remain true at handoff, not how an agent must think or which command it must run.

- **Core**: `AGENTS.md`, the `zettelkasten/` entry and links, stable work intent when needed, validation evidence, and durable experience writeback.
- **Optional**: companion-Skill scripts for knowledge checks, WORK edits, and guarded worktree creation.
- **Non-goals**: autonomous loops, task scheduling, hidden memory, mandatory CLIs, or replacing Git, issue trackers, CI, and project test systems.

A project must remain understandable and operable after removing the companion Skill.

## Why It Is Lighter

- Workflow files never move between status directories; frontmatter is the state.
- Ordinary tracked work keeps requirement, approach, slices, validation, review, checkpoint, and experience candidates in one `WORK-*`.
- TECH, PLAN, and REVIEW are optional independent artifacts, not mandatory stages.
- There is no manually duplicated `CURRENT.md`; the current branch and stable WORK files expose active state.
- Project Skills load on demand from a compact trigger index instead of expanding `AGENTS.md`.
- Knowledge categories remain separate where they improve retrieval, but active workflow state is consolidated under one directory.
- Optional companion-Skill helpers automate checks and edits without adding runtime state to downstream projects.

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

## Project-To-Template Feedback

Downstream agents silently check for workflow friction only at meaningful checkpoints or after a user correction. Normal tasks create no feedback artifact. Evidence-backed template-wide or vendor-specific observations are stored locally in `zettelkasten/00-governance/workflow-observations.md`, created only on first use.

The companion Skill can classify, deduplicate, and sanitize those observations when the user asks to prepare upstream feedback. It never scans unrelated projects, sends telemetry, or creates an Issue or PR without explicit user approval.

## Parallel Development

Tracked and Governed tasks use dedicated task branches. Concurrent tasks or agents use separate Git worktrees using normal Git:

```bash
git worktree add ../example -b task/work-example <base>
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

Then ask the agent to follow `INIT.md`. Initialization discovers repository facts, merges local instructions, records Git defaults, removes placeholders, and validates the knowledge network.

## Daily Use

The agent starts with `AGENTS.md` and `zettelkasten/AI.md`, then reads a branch-matched `WORK-*` only when durable task state exists. It loads only linked notes or a matched project Skill, not the entire vault.

Create tracked work from the repository template:

```bash
cp zettelkasten/00-governance/templates/work-item.md \
  zettelkasten/06-work/WORK-<timestamp>-<slug>.md
```

Update frontmatter and checkpoint fields directly. All WORK, TECH, PLAN, and REVIEW files remain under `zettelkasten/06-work/` for their full lifecycle. The companion Skill offers optional Doctor, WORK, and worktree helpers for teams that want deterministic automation.

## Structure

```text
template/
  AGENTS.md
  CLAUDE.md
  INIT.md
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

The Agent Skills-compatible companion is under `skills/ai-collaboration-workflow/`. It handles installation and routing, and optionally provides deterministic work-item, knowledge-check, and worktree helpers.

Install with:

```bash
npx skills add vector233/ai-collaboration-workflow-template \
  --skill ai-collaboration-workflow \
  -a claude-code \
  -g
```

For Codex, copy it to `~/.codex/skills/`; for Claude Code, copy it to `~/.claude/skills/` or the repository's project-Skill location supported by the tool.

The initialized repository remains fully usable without the companion Skill. `AGENTS.md`, linked Markdown, Git, and project validation remain canonical.

## Validation

For a downstream project, validate the changed behavior with project commands and inspect changed knowledge links, work state, review dates, and project-Skill routing. When the companion Skill is installed, its optional Doctor automates these checks and can report cross-worktree state.

For this distribution repository:

```bash
python3 scripts/validate_distribution.py
```

The distribution validator exercises bootstrap, initialization, stable work artifacts, project-Skill discovery, worktree isolation, wiki links, and doctor behavior in temporary repositories.

Fresh-agent routing behavior can be checked with [docs/workflow-behavior-evaluation.md](docs/workflow-behavior-evaluation.md).

Maintainers and downstream users can follow [docs/workflow-feedback.md](docs/workflow-feedback.md) to prepare a privacy-reviewed report.

Chinese guide: [docs/zh-CN/README.md](docs/zh-CN/README.md).

## License

MIT. See [LICENSE](LICENSE).
