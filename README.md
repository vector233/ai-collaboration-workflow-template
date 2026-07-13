# AI Collaboration Workflow Template

A vendor-neutral project knowledge network and lightweight delivery contract for AI-assisted software development.

The template gives capable but context-temporary, vendor-diverse, and potentially parallel agents the same trusted project knowledge, then makes durable writeback part of delivery. It is not an autonomous runtime and requires no helper tool to remain usable.

Version `v4.0.0` is a new-project template. It intentionally does not migrate or emulate earlier layouts; see [Why v4 Is Breaking](#why-v4-is-breaking).

## Quick Start

### Recommended: Install The Companion Skill

Install the pinned release for Claude Code:

```bash
npx skills add \
  https://github.com/vector233/ai-collaboration-workflow-template/tree/v4.0.0/skills/ai-collaboration-workflow \
  --skill ai-collaboration-workflow \
  -a claude-code \
  -g -y
```

Or install it for Codex:

```bash
npx skills add \
  https://github.com/vector233/ai-collaboration-workflow-template/tree/v4.0.0/skills/ai-collaboration-workflow \
  --skill ai-collaboration-workflow \
  -a codex \
  -g -y
```

Then enter the target repository and ask the agent:

```text
Use $ai-collaboration-workflow to initialize this repository.
Inspect existing project rules first, preserve stricter local policy, and complete INIT.md.
```

The Skill previews and bootstraps missing files without overwriting differing repository files. When `AGENTS.md`, `CLAUDE.md`, or other target files conflict, the agent must preserve the existing file and merge the applicable shared rules deliberately.

### Core-Only Installation

The Skill is optional. For a new repository that has no conflicting agent or knowledge files, copy the pinned payload:

```bash
git clone --branch v4.0.0 --depth 1 \
  https://github.com/vector233/ai-collaboration-workflow-template.git

cp -R ai-collaboration-workflow-template/template/. /path/to/your-project/
```

Then ask the agent:

```text
Follow INIT.md completely. Initialize only verified project facts, validate the knowledge links,
and remove the initialization files only after all checks pass.
```

Do not use the raw copy command over an existing `AGENTS.md`, `CLAUDE.md`, `zettelkasten/`, or `project-skills/`. Use the companion Skill or merge those files explicitly instead.

## Initialization Is Complete When

- existing repository instructions and stricter Git policy are preserved;
- project purpose, stack, architecture, commands, and validation flows use verified facts;
- all template placeholders are resolved;
- wiki links and required knowledge fields pass validation;
- `INIT.md` and `.ai-collaboration-workflow-template` are removed;
- no empty WORK or invented project Skill was created;
- initialization changes are committed only when repository policy or the user requires it.

After initialization, the repository remains usable with only Markdown, Git, and project-native validation. Removing the companion Skill must not remove project knowledge or workflow state.

## Daily Use

Start ordinary work with an outcome, not a requested document chain:

```text
Follow AGENTS.md and zettelkasten/AI.md for this task:
<task description>
Choose the lightest safe route and keep durable project knowledge current.
```

The agent chooses:

| Route | Use when | Workflow state |
|---|---|---|
| Direct | local, reversible, low-risk, one context | none; validate and commit |
| Tracked | behavior change, debugging continuity, multiple contexts | one stable `WORK-*` |
| Governed | high risk, important uncertainty, independent approval, migration, release, multi-owner coordination | the same `WORK-*` with explicit gates and evidence |

Resume a long-running task:

```text
Use the current Git branch to find its WORK. Read the checkpoint and next_action,
load only linked knowledge and matching project Skills, then continue.
```

Start work that must run in parallel:

```text
Run this as an isolated parallel task. Use a task branch and dedicated worktree,
declare owned paths, and check overlap with active WORK records before editing.
```

Close tracked or governed work:

```text
Validate the accepted behavior, record the final commit and evidence, close all governed gates,
run the Experience Promotion Check, update durable knowledge, and then close the WORK.
```

Without the Skill, create a WORK manually only when the selected route is Tracked or Governed:

```bash
cp zettelkasten/templates/work-item.md \
  zettelkasten/work/WORK-$(date +%Y%m%d%H%M%S)-<slug>.md
```

Update frontmatter and checkpoints in place. A WORK never moves for a status change.

## Core Model

```text
Task
  -> Route: Direct | Tracked | Governed
  -> Load only the active WORK and matched knowledge
  -> Implement, validate, and review as required
  -> Commit every context that produces persistent changes or a coherent slice
  -> Promote reusable experience into rules, notes, runbooks, or project Skills
```

Routing considers scope, uncertainty, risk, reversibility, duration, coordination, and verification. A small security or data change can be Governed even when its diff is tiny.

## Why v4 Is Breaking

Earlier versions modeled delivery as several numbered knowledge areas and separate requirement, technical-design, plan, and review artifacts. That structure made each lifecycle stage explicit, but real AI-assisted development exposed costs that outweighed the benefit:

- small and medium tasks accumulated documents that added no independent decision value;
- the same scope, status, plan, and validation facts were repeated across files;
- moving or renaming lifecycle files caused link churn and fragile resume paths;
- every structural update had to be synchronized across templates, Skills, examples, scripts, and documentation;
- agents loaded extra layers to reconstruct current state, increasing token use and stale-assumption risk;
- parallel work amplified conflicts in shared indexes and frequently edited process files.

v4 makes repository knowledge the product and keeps process proportional to risk:

- durable knowledge uses flat, semantic entry points such as `project.md`, `architecture.md`, and `gotchas.md`;
- Direct work creates no workflow record;
- Tracked and Governed work use one stable WORK, with governed decisions and approvals represented as gates;
- Git, Issues, pull requests, CI, and release systems retain the lifecycle they already own;
- companion tooling remains optional and owns no hidden project state.

There is no automatic migration because previous projects may have customized both their knowledge and workflow artifacts. A generic converter cannot reliably distinguish durable facts from stale process state, and carrying both models forward would preserve the complexity v4 removes. Existing projects may adopt selected v4 ideas manually, but v4 defines only the clean new-project contract.

## Product Boundary

The core product is linked, reviewable repository knowledge plus a lightweight delivery contract. It defines what must remain true at handoff, not how an agent must think or which command it must run.

- **Core**: `AGENTS.md`, the `zettelkasten/` entry and links, stable work intent when needed, validation evidence, and durable experience writeback.
- **Optional**: companion-Skill scripts for knowledge checks, WORK edits, and guarded worktree creation.
- **Non-goals**: autonomous loops, task scheduling, hidden memory, mandatory CLIs, or replacing Git, issue trackers, CI, and project test systems.

The knowledge network uses plain Markdown and wiki links. It can be opened as an Obsidian-compatible vault, but Obsidian is an optional editor rather than a runtime or plugin dependency.

## Durable Experience

Each WORK records Experience Candidates. At checkpoints and closeout, agents decide whether each lesson stays local or is promoted:

| Experience | Destination |
|---|---|
| repository-wide mandatory behavior | `AGENTS.md` |
| bug root or false assumption | `zettelkasten/gotchas.md` |
| architecture fact or invariant | `zettelkasten/architecture.md` or a linked domain note |
| simple setup or validation flow | quick reference or runbook |
| stable conditional multi-step procedure | `project-skills/<name>/SKILL.md` plus `project-skills/INDEX.md` |

Project Skills include concrete triggers, exclusions, procedure, validation, recovery, and provenance. One-off incidents and unverified guesses do not become Skills.

## Project-To-Template Feedback

Downstream agents silently check for workflow friction only at meaningful checkpoints or after a user correction. Normal tasks create no feedback artifact. Evidence-backed template-wide or vendor-specific observations are stored locally in `zettelkasten/workflow-observations.md`, created only on first use.

The companion Skill can classify, deduplicate, and sanitize those observations when the user asks to prepare upstream feedback. It never scans unrelated projects, sends telemetry, or creates an Issue or PR without explicit user approval. See [docs/workflow-feedback.md](docs/workflow-feedback.md).

## Parallel Development

Tracked and Governed tasks use task branches. Concurrent tasks or agents use separate Git worktrees:

```bash
work_id="WORK-$(date +%Y%m%d%H%M%S)-<short-name>"
git worktree add ../<short-name> -b "task/${work_id}" <base>
```

The default branch is integration-only. Dependent or overlapping tasks need an explicit integration plan. Every context that produces persistent changes, or each coherent slice, ends with a task-scoped commit; read-only analysis creates no empty commit.

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
    project.md
    architecture.md
    decisions.md
    gotchas.md
    workflow.md
    validation-policy.md
    validation-runbook.md
    templates/
    work/
```

`template/` is the only downstream payload. This maintenance repository intentionally has no second root `zettelkasten/`.

## Validation

Downstream projects use their own build, test, and review commands. When the companion Skill is installed, its optional Doctor can inspect knowledge links, WORK state, project-Skill routing, and cross-worktree overlap.

For this distribution repository:

```bash
python3 scripts/validate_distribution.py
```

The distribution validator exercises tool-free initialization, single-WORK routing, governed gates, project-Skill discovery, worktree isolation, wiki links, optional helpers, and bootstrap behavior in temporary repositories.

Fresh-agent routing behavior can be checked with [docs/workflow-behavior-evaluation.md](docs/workflow-behavior-evaluation.md).

Chinese guide: [docs/zh-CN/README.md](docs/zh-CN/README.md).

## License

MIT. See [LICENSE](LICENSE).
