# Repo Continuity

**One repository. Many coding agents. One durable project memory.**

[![Validate distribution](https://github.com/vector233/repo-continuity/actions/workflows/validate.yml/badge.svg)](https://github.com/vector233/repo-continuity/actions/workflows/validate.yml)

Coding agents are powerful, but their context is temporary. Sessions end, context gets compacted, agents change, and important project knowledge is rediscovered or lost.

Repo Continuity makes the repository their shared source of truth:

- **Resume, do not restart.** A fresh agent can recover the active goal, decisions, validation, risks, and next action without chat history.
- **Load only what matters.** Linked knowledge and on-demand project Skills keep context focused instead of loading the whole repository story.
- **Keep small work small.** Direct, Tracked, and Governed routes add process only when duration, coordination, or risk requires it.
- **Keep large work bounded.** Existing Epics stay authoritative; without one, a thin local Initiative coordinates independent child WORK records without recursive task trees.
- **Make the project learn.** Verified fixes and repeated procedures become durable rules, notes, runbooks, or project Skills instead of being forgotten in a conversation.
- **Run parallel work safely.** Task branches, worktrees, owned paths, and stable WORK records keep agents from silently overwriting one another.

Everything required stays in reviewable Markdown and Git. The Companion Skill can automate setup and checks, but there is no required service, database, hidden memory, or autonomous runtime.

## Quick Start

The commands below are pinned to the current release, `v4.5.0`. Existing initialized projects are not modified automatically; use the three-way upgrade workflow to reconcile a newer release when useful.

> [!TIP]
> **Upgrading from `v4.1.1` or earlier:** the Companion Skill was renamed from `ai-collaboration-workflow` to `repo-continuity`.
>
> Remove the old global Skill with `npx skills remove ai-collaboration-workflow -g -y`, then install and invoke `$repo-continuity`. Repositories that already completed `INIT.md` do not need to be initialized again. For an interrupted setup, continue `INIT.md`; the Doctor still recognizes the legacy payload marker.

### Recommended: Install The Companion Skill

Install the pinned release for Claude Code:

```bash
npx skills add \
  https://github.com/vector233/repo-continuity/tree/v4.5.0/skills/repo-continuity \
  --skill repo-continuity \
  -a claude-code \
  -g -y
```

Or install it for Codex:

```bash
npx skills add \
  https://github.com/vector233/repo-continuity/tree/v4.5.0/skills/repo-continuity \
  --skill repo-continuity \
  -a codex \
  -g -y
```

Then enter the target repository and ask the agent:

```text
Use $repo-continuity to initialize this repository.
Inspect existing project rules first, preserve stricter local policy, and complete INIT.md.
```

`npx skills add` installs the Companion Skill only; it does not copy the full repository payload into the target project. When invoked, the Skill runs its bundled bootstrap, which fetches the same pinned release and previews or copies missing core files without overwriting differing repository files. Its default installation is core-only and does not add model-routing configuration. When `AGENTS.md`, `CLAUDE.md`, or other target files conflict, the agent must preserve the existing file and merge the applicable shared rules deliberately.

### Core-Only Installation

The Skill is optional. For a new repository that has no conflicting agent or knowledge files, copy the pinned payload:

```bash
git clone --branch v4.5.0 --depth 1 \
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
- `INIT.md`, `.repo-continuity-template`, and any legacy `.ai-collaboration-workflow-template` marker are removed;
- no empty WORK or invented project Skill was created;
- initialization changes are committed only when repository policy or the user requires it.

After initialization, the repository remains usable with only Markdown, Git, and project-native validation. Removing the companion Skill must not remove project knowledge or workflow state.

## Safely Reconcile An Upgrade

An initialized project is not a disposable template copy. It is the recorded old upstream baseline plus repository facts, rules, and learned Skills that may have diverged intentionally. Install the target Skill release, enter the project, and ask:

```text
Use $repo-continuity to upgrade this initialized repository to the Skill's pinned release.
Create an isolated upgrade task branch, preview the three-way reconciliation, apply only safe changes,
preserve local customization, resolve remaining conflicts, validate, and advance the baseline last.
```

The Companion Skill uses a true three-way reconciliation: old upstream, current project, and target upstream. A read-only report and dry-run are available first. The apply command automatically installs upstream additions, adopts upstream-only changes, and performs clean text merges while preserving local-only changes. True conflicts and upstream removals stay untouched for explicit review.

Application requires a clean task branch and is transactional. It refuses to run on `main` or `master`, never follows target symlinks, and never updates the `Template baseline` itself. After resolving the remaining paths, run project validation, review the Git diff, and advance the baseline as the final gate. See the [upgrade guide](docs/upgrading.md) and exact [Companion Skill workflow](skills/repo-continuity/SKILL.md#reconcile-an-upgrade).

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

## Large Requirements Without Large WORK Files

Do not turn one WORK into an unbounded Epic log. Keep one WORK when the result still has one tightly coupled acceptance and rollback boundary. Split it when outcomes can be accepted, routed, assigned, validated, rolled back, or released independently.

Use this bounded hierarchy:

```text
existing external Epic / Issue / Milestone (preferred)
└── independent WORK records

or, when no suitable external parent exists:

one optional local INITIATIVE
├── independent WORK-A
├── independent WORK-B
└── independent WORK-C
```

There is no third level. A WORK never parents another WORK or Initiative. Each child keeps its own route, task branch or worktree, acceptance, `depends_on` relationships, validation, checkpoint, Learning Check, and closure. `depends_on` is strict: keep the dependent child in backlog or blocked until every prerequisite is done; use prose coordination when only final integration order matters. The Initiative remains a thin coordination record for the overall goal, shared gates, integration order, derived rollup, and next coordination action. Durable facts still belong in linked Zettels, decisions, runbooks, or project Skills.

When Jira, GitHub, GitLab, or another project-native tracker already owns the parent lifecycle, set `external_parent` in each child WORK and do not mirror the Epic locally. For repository-local coordination, copy `zettelkasten/templates/initiative.md` or use the optional helper:

```bash
python3 skills/repo-continuity/scripts/workflow_task.py initiative-new <slug>
python3 skills/repo-continuity/scripts/workflow_task.py new <child-slug> \
  --initiative <INITIATIVE-ID> --depends-on <WORK-ID>
```

Use `--external-parent <tracker-ref>` instead of `--initiative` when the external record is authoritative. Resume from the child branch and WORK; load the Initiative only when a shared gate, dependency, or integration constraint affects that slice, and do not load sibling WORK records by default.

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

After validation, every route runs a lightweight Learning Check. Direct work with no verified reusable lesson creates no artifact. If a Direct task discovers a lesson that should change shared project knowledge, it becomes Tracked before writeback so the evidence and decision remain recoverable.

Start work that must run in parallel:

```text
Run this as an isolated parallel task. Use a task branch and dedicated worktree,
declare owned paths, and check overlap with active WORK records before editing.
```

Close tracked or governed work:

```text
Validate the accepted behavior, record the final commit and evidence, close all governed gates,
run the Learning Check, decide every candidate, validate durable writeback, and then close the WORK.
```

Without the Skill, create a WORK manually only when the selected route is Tracked or Governed:

```bash
cp zettelkasten/templates/work-item.md \
  zettelkasten/work/WORK-$(date +%Y%m%d%H%M%S)-<slug>.md
```

Update frontmatter and checkpoints in place. A WORK never moves for a status change.

When the Companion Skill is active, ask the agent to use its bundled WORK helper; its absolute installation path is host-specific. From a Repo Continuity source checkout, the equivalent commands are:

```bash
python3 skills/repo-continuity/scripts/workflow_task.py learn-add <WORK-ID> \
  --candidate "<lesson>" --shape project-skill --evidence "<verified evidence>"
python3 skills/repo-continuity/scripts/workflow_task.py learn-decide <WORK-ID> \
  --candidate "<lesson>" --decision promoted \
  --destination "project-skills/<name>/SKILL.md; project-skills/INDEX.md" \
  --reason "<writeback and validation result>"
python3 skills/repo-continuity/scripts/workflow_task.py learn-status <WORK-ID> --require-complete
```

Use `learn-none <WORK-ID> --reason "<why no verified reusable lesson exists>"` for a Tracked or Governed task with no candidate. These commands manage Markdown rows and closure checks; the agent still judges relevance, writes the destination, and validates retrieval.

## Optional Codex Model Routing

The repository ships a separate Codex overlay under `adapters/codex/`. Neither the default bootstrap nor the raw `template/` copy installs it. Opt in explicitly with the safe bootstrap:

```bash
python3 skills/repo-continuity/scripts/bootstrap_template.py \
  --source . \
  --target /path/to/your-project \
  --with-model-routing codex \
  --dry-run

python3 skills/repo-continuity/scripts/bootstrap_template.py \
  --source . \
  --target /path/to/your-project \
  --with-model-routing codex
```

For a new conflict-free project using the manual copy path, copy `adapters/codex/.` after `template/.`. Workflow routing and model routing are separate: choose Direct, Tracked, or Governed first, then delegate only when a specialist materially improves the result. The root keeps the model selected by the user or current Codex session.

| Agent | Use for | Default model policy |
|---|---|---|
| root | task routing and ordinary work | current user or session selection; not overridden |
| `explorer` | read-only discovery, tracing, and evidence gathering | `gpt-5.6-terra`, low reasoning |
| `implementer` | one understood, scoped change and targeted validation | `gpt-5.6-terra`, medium reasoning |
| `reviewer` | read-only correctness, security, regression, and test review | `gpt-5.6-sol`, high reasoning |
| `architect` | read-only high-impact design or difficult root-cause analysis | `gpt-5.6-sol`, extra-high reasoning |

The adapter caps Codex at three threads and one delegation level. Read-only specialists may work in parallel on independent scopes. The implementer is write-capable and must work serially with other writers in its task worktree; concurrent write tasks require their own task branch and worktree.

The listed models must be available to the target account. If one is unavailable, replace only that agent's `model` setting with an account-supported equivalent.

## Optional Claude Code Model Routing

The separate overlay under `adapters/claude/` is also opt-in:

```bash
python3 skills/repo-continuity/scripts/bootstrap_template.py \
  --source . \
  --target /path/to/your-project \
  --with-model-routing claude \
  --dry-run

python3 skills/repo-continuity/scripts/bootstrap_template.py \
  --source . \
  --target /path/to/your-project \
  --with-model-routing claude
```

Use `--with-model-routing all` to install both overlays. For a new conflict-free project, the manual equivalent is copying `adapters/claude/.` after the core template. The overlay installs `.claude/agents/` but no `.claude/settings.json`, so the root session keeps the user's current Claude Code model while specialized agents use fixed model and tool policies.

| Agent | Use for | Default model policy |
|---|---|---|
| root | task routing, planning, and ordinary work | current user or client selection; not overridden |
| `explorer` | read-only discovery, tracing, and evidence gathering | Haiku; `Read`, `Grep`, and `Glob` only |
| `implementer` | one understood, scoped change and targeted validation | Sonnet; write-capable |
| `reviewer` | read-only correctness, security, regression, and test review | Opus |
| `architect` | read-only high-impact design or difficult root-cause analysis | Opus |

Claude Code selects an agent from its description and context. Use `@explorer`, `@implementer`, `@reviewer`, or `@architect` when the exact role must run. The implementer remains serial with other writers in its task worktree; independent read-only roles may run in parallel. If a model is unavailable or restricted, Claude Code falls back to an inherited or permitted model; the same repository workflow still applies.

## Evaluate Model Routing

Do not infer cost savings from configuration alone. The [model-routing A/B evaluation](docs/model-routing-evaluation.md) defines six paired task classes, fresh-session provenance, independent acceptance results, high-risk-miss checks, specialist-role checks, duration, and optional comparable quota units. Its evaluator keeps synthetic harness fixtures visibly separate from real Agent evidence and reports cost as inconclusive when comparable quota data is unavailable.

## Core Model

```text
Task
  -> Route: Direct | Tracked | Governed
  -> Load only the active WORK and matched knowledge
  -> Implement, validate, and review as required
  -> Preserve recoverable state at meaningful context boundaries
  -> Commit every context that produces persistent changes or a coherent slice
  -> Run the Learning Check and promote verified experience into rules, notes, runbooks, or project Skills
```

Routing considers scope, uncertainty, risk, reversibility, duration, coordination, and verification. A small security or data change can be Governed even when its diff is tiny.

## Product Boundary

The core product is linked, reviewable repository knowledge plus a lightweight delivery contract. It defines what must remain true at handoff, not how an agent must think or which command it must run.

- **Core**: `AGENTS.md`, the `zettelkasten/` entry and links, stable work intent when needed, validation evidence, and durable experience writeback.
- **Optional**: companion-Skill scripts for knowledge checks, WORK and Learning Candidate edits, and guarded worktree creation; explicitly installed model-routing overlays from `adapters/` for specialist agents.
- **Non-goals**: autonomous loops, task scheduling, hidden memory, mandatory CLIs, or replacing Git, issue trackers, CI, and project test systems.

The knowledge network uses plain Markdown and wiki links. It can be opened as an Obsidian-compatible vault, but Obsidian is an optional editor rather than a runtime or plugin dependency.

## Keep History Outside Routine Context

Repo Continuity separates concise entry points, task-relevant current knowledge, and historical evidence. Open WORK and Initiative records each have a small Markdown route under `zettelkasten/work/active/`. The canonical source owns status and checkpoint state; closure removes its route. Ordinary discovery and search skip archive storage and unselected historical WORK bodies.

After verified lessons are promoted and closure gates are resolved, archive substantial history while keeping a compact summary, original relationships and evidence link at the same source path. Snapshots preserve the original bytes and their checksum. Short closed records already leave routine discovery. Current constraints stay current regardless of age.

The optional Companion Skill supports `workflow_archive.py archive`, `restore`, and a previewable `reindex` migration. Ordinary Doctor checks are scoped; use `workflow_doctor.py --full --strict` for complete historical integrity and route coverage. Existing installations must explicitly build open routes before using scoped discovery. Bootstrap and upgrade never automatically archive project content.

See the [canonical knowledge lifecycle](template/zettelkasten/knowledge-lifecycle.md), [helper guide](skills/repo-continuity/references/knowledge-lifecycle.md), and [upgrade guide](docs/upgrading.md). Markdown and Git remain sufficient.

## Repository Learning Loop

After validation, every task checks for a correction, repeatable root cause, missing invariant, reusable command sequence, or stable procedure. Direct work with no verified candidate remains artifact-free; a Direct task with a durable candidate becomes Tracked before shared writeback. Each Tracked or Governed WORK records candidate evidence and the final `promoted`, `updated`, `no-op`, or `not-promoted` decision.

| Experience | Destination |
|---|---|
| repository-wide mandatory behavior | `AGENTS.md` |
| bug root or false assumption | `zettelkasten/gotchas.md` |
| architecture fact or invariant | `zettelkasten/architecture.md` or a linked domain note |
| simple setup or validation flow | quick reference or runbook |
| stable conditional multi-step procedure | `project-skills/<name>/SKILL.md` plus `project-skills/INDEX.md` |

Project Skills include concrete triggers, exclusions, procedure, validation, recovery, and provenance. One-off incidents and unverified guesses do not become Skills.

Promotion is idempotent. Search existing destinations first, update the canonical rule, note, runbook, or Skill in place, and record a no-op when it is already current. For Tracked or Governed work, add shared destinations to `owned_paths`; when another active WORK owns the same destination, coordinate one writer or defer the promotion.

Writeback is always a task-branch Git diff, never hidden model memory. Repository-wide instructions, architecture constraints, security or permission behavior, release procedures, and existing Skill contracts require evidence and the same review or Governed gates as equivalent code or policy changes. Project Skills keep the portable `SKILL.md` core; host-specific activation metadata stays in explicit adapters.

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
    knowledge-lifecycle.md
    validation-policy.md
    validation-runbook.md
    templates/
    work/
      active/
    archive/
adapters/
  codex/
    .codex/
      config.toml
      agents/
  claude/
    .claude/
      agents/
```

`template/` is the canonical default downstream core. `adapters/` contains separate opt-in overlays and is never copied by the default installation. This maintenance repository intentionally has no second root `zettelkasten/`.

## Validation

Downstream projects use their own build, test, and review commands. When the companion Skill is installed, its optional Doctor can inspect structural knowledge health such as links, WORK state, project-Skill routing, and cross-worktree overlap. Semantic Fresh-Agent recovery remains a separate, evidence-backed evaluation.

For this distribution repository:

```bash
python3 scripts/validate_distribution.py
```

The distribution validator exercises tool-free core initialization, explicit model-routing opt-in, single-WORK routing, governed gates, project-Skill discovery, worktree isolation, wiki links, archival and restore, scoped read boundaries, explicit route migration, optional helpers, and bootstrap behavior in temporary repositories.

Fresh-agent routing behavior can be checked with [docs/workflow-behavior-evaluation.md](docs/workflow-behavior-evaluation.md).
Actual model-routing quality and comparable quota evidence use [docs/model-routing-evaluation.md](docs/model-routing-evaluation.md); the evaluator never treats its synthetic regression fixture as Agent evidence.

`.github/workflows/validate.yml` repeats release-version alignment, the full distribution lifecycle, whitespace checks, and an official Skills CLI install/bootstrap smoke test on pull requests and `main`.

Chinese guide: [docs/zh-CN/README.md](docs/zh-CN/README.md).

## License

MIT. See [LICENSE](LICENSE).
