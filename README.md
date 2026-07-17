# Repo Continuity

**One repository. Many coding agents. One durable project memory.**

Coding agents are powerful, but their context is temporary. Sessions end, context gets compacted, agents change, and important project knowledge is rediscovered or lost.

Repo Continuity makes the repository their shared source of truth:

- **Resume, do not restart.** A fresh agent can recover the active goal, decisions, validation, risks, and next action without chat history.
- **Load only what matters.** Linked knowledge and on-demand project Skills keep context focused instead of loading the whole repository story.
- **Keep small work small.** Direct, Tracked, and Governed routes add process only when duration, coordination, or risk requires it.
- **Make the project learn.** Verified fixes and repeated procedures become durable rules, notes, runbooks, or project Skills instead of being forgotten in a conversation.
- **Run parallel work safely.** Task branches, worktrees, owned paths, and stable WORK records keep agents from silently overwriting one another.

Everything required stays in reviewable Markdown and Git. The Companion Skill can automate setup and checks, but there is no required service, database, hidden memory, or autonomous runtime.

## Quick Start

The commands below are pinned to the current release, `v4.1.1`. Existing initialized projects are not modified automatically; adopt selected updates manually when useful.

### Recommended: Install The Companion Skill

Install the pinned release for Claude Code:

```bash
npx skills add \
  https://github.com/vector233/repo-continuity/tree/v4.1.1/skills/ai-collaboration-workflow \
  --skill ai-collaboration-workflow \
  -a claude-code \
  -g -y
```

Or install it for Codex:

```bash
npx skills add \
  https://github.com/vector233/repo-continuity/tree/v4.1.1/skills/ai-collaboration-workflow \
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
git clone --branch v4.1.1 --depth 1 \
  https://github.com/vector233/repo-continuity.git

cp -R repo-continuity/template/. /path/to/your-project/
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

Pause or hand off a long-running task:

```text
Update the existing WORK so a fresh agent can recover the route, acceptance state,
completed step and commit, exact validation, unresolved risks, next action, and experience candidates.
Commit the checkpoint; do not create another handoff file.
```

Checkpoint only at meaningful boundaries: after each bounded Tracked or Governed slice, and before an unfinished task crosses a handoff, long pause, agent or session switch, detectable context compaction, or a yield that would leave decisions only in chat. Direct work that completes, validates, and commits in the current context still needs no WORK; otherwise it becomes Tracked. Runtime context telemetry is optional, never a core dependency.

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

## Optional Codex Model Routing

The payload includes an optional `.codex/` adapter that routes bounded specialist work to fixed Codex model settings. Workflow routing and model routing are separate: choose Direct, Tracked, or Governed first, then delegate only when a specialist materially improves the result.

| Agent | Use for | Default model policy |
|---|---|---|
| root | task routing and ordinary work | `gpt-5.6-terra`, medium reasoning |
| `explorer` | read-only discovery, tracing, and evidence gathering | `gpt-5.6-terra`, low reasoning |
| `implementer` | one understood, scoped change and targeted validation | `gpt-5.6-terra`, medium reasoning |
| `reviewer` | read-only correctness, security, regression, and test review | `gpt-5.6-sol`, high reasoning |
| `architect` | read-only high-impact design or difficult root-cause analysis | `gpt-5.6-sol`, extra-high reasoning |

The adapter caps Codex at three threads and one delegation level. Read-only specialists may work in parallel on independent scopes. The implementer is write-capable and must work serially with other writers in its task worktree; concurrent write tasks require their own task branch and worktree.

The listed models must be available to the target account. If one is unavailable, replace only that agent's `model` setting with an account-supported equivalent. Model routing is an optional Codex capability: the repository's Markdown/Git workflow, checkpoints, validation, and handoff continue to work in Codex without subagents and in other clients.

## Core Model

```text
Task
  -> Route: Direct | Tracked | Governed
  -> Load only the active WORK and matched knowledge
  -> Implement, validate, and review as required
  -> Preserve recoverable state at meaningful context boundaries
  -> Commit every context that produces persistent changes or a coherent slice
  -> Promote reusable experience into rules, notes, runbooks, or project Skills
```

Routing considers scope, uncertainty, risk, reversibility, duration, coordination, and verification. A small security or data change can be Governed even when its diff is tiny.

## Product Boundary

The core product is linked, reviewable repository knowledge plus a lightweight delivery contract. It defines what must remain true at handoff, not how an agent must think or which command it must run.

- **Core**: `AGENTS.md`, the `zettelkasten/` entry and links, stable work intent when needed, validation evidence, and durable experience writeback.
- **Optional**: companion-Skill scripts for knowledge checks, WORK edits, and guarded worktree creation; the `.codex/` model-routing adapter for Codex specialist agents.
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

Promotion is idempotent. Search existing destinations first, update the canonical rule, note, runbook, or Skill in place, and record a no-op when it is already current. For Tracked or Governed work, add shared destinations to `owned_paths`; when another active WORK owns the same destination, coordinate one writer or defer the promotion.

Knowledge health has two levels. Normal handoff checks structure: branch-to-WORK mapping, checkpoint fields, links, ownership, and Skill routing. For important multi-context handoffs or changes to resume semantics, a real fresh agent with no chat history performs a semantic resume probe and reports the route, acceptance state, checkpoint, validation, risk, and next action before editing. Synthetic expected responses test only the evaluator, not Agent recovery; see [docs/fresh-agent-resume-evaluation.md](docs/fresh-agent-resume-evaluation.md).

## Project-To-Template Feedback

Downstream agents silently check for workflow friction only at meaningful checkpoints or after a user correction. Normal tasks create no feedback artifact. Evidence-backed template-wide or vendor-specific observations are stored locally in `zettelkasten/workflow-observations.md`, created only on first use.

The companion Skill can classify, deduplicate, and sanitize those observations when the user asks to prepare upstream feedback. It never scans unrelated projects, sends telemetry, or creates an Issue or PR without explicit user approval. See [docs/workflow-feedback.md](docs/workflow-feedback.md).

## Parallel Development

Tracked and Governed tasks use task branches. Concurrent tasks or agents use separate Git worktrees:

```bash
work_id="WORK-$(date +%Y%m%d%H%M%S)-<short-name>"
git worktree add ../<short-name> -b "task/${work_id}" <base>
```

The default branch is integration-only. Dependent or overlapping tasks need an explicit integration plan. Shared knowledge promotion uses `owned_paths` to establish one writer. Every context that produces persistent changes, or each coherent slice, ends with a task-scoped commit; read-only analysis creates no empty commit.

## Structure

```text
template/
  .codex/
    config.toml
    agents/
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

Downstream projects use their own build, test, and review commands. When the companion Skill is installed, its optional Doctor can inspect structural knowledge health such as links, WORK state, project-Skill routing, and cross-worktree overlap. Semantic Fresh-Agent recovery remains a separate, evidence-backed evaluation.

For this distribution repository:

```bash
python3 scripts/validate_distribution.py
```

The distribution validator exercises tool-free initialization, single-WORK routing, governed gates, project-Skill discovery, worktree isolation, wiki links, optional helpers, and bootstrap behavior in temporary repositories.

Fresh-agent routing behavior can be checked with [docs/workflow-behavior-evaluation.md](docs/workflow-behavior-evaluation.md).

Chinese guide: [docs/zh-CN/README.md](docs/zh-CN/README.md).

## License

MIT. See [LICENSE](LICENSE).
