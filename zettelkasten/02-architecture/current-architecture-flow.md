---
title: Current Architecture Flow
status: active
project: AI Collaboration Workflow Template
last_verified_at: 2026-06-18
source_of_truth: mixed
related:
  - "[[00-governance/project-overview]]"
  - "[[00-governance/ai-workflow]]"
  - "[[08-technical-designs/README]]"
---

# Current Architecture Flow

## What This Answers

This note should describe how the current system actually works today. It is the architecture fact base that agents read before changing behavior.

Keep it current. After an implemented TECH changes system flow, write the still-true conclusions back here or into a more specific architecture note.

## System Components

| Component | Responsibility | Runtime / owner |
|---|---|---|
| Canonical payload | Files installed into downstream repositories | `template/` |
| Companion Skill | Routes agents through bootstrap and daily workflow | `skills/ai-collaboration-workflow/` |
| Bootstrap script | Copies payload safely from local or remote source | Python 3 |
| Distribution validator | Verifies payload isolation and first workflow artifacts | `scripts/validate_distribution.py` |
| Maintenance knowledge base | Tracks this repository's own work | root `zettelkasten/` |

## Main Flow

1. A maintainer changes the canonical payload, Skill, documentation, or validation tooling.
2. Root REQ and approved TECH define the intended product change.
3. `scripts/validate_distribution.py` checks payload boundaries and bootstraps a temporary project.
4. The bootstrap script selects `<source>/template/`, previews or copies missing files, and preserves conflicts.
5. The temporary target receives `AGENTS.md`, `CLAUDE.md`, `INIT.md`, the full knowledge base, and empty workflow state directories.
6. Validation creates sample REQ, TECH, and REVIEW artifacts to prove the first daily workflow step is possible.
7. A review handoff records evidence and risks before release.
8. Users install through the Skill or copy the contents of `template/`.

## Contracts

- Public interfaces: Skill invocation, bootstrap CLI, and payload file structure.
- Internal interfaces: `template/` layout expected by bootstrap and validation scripts.
- Data ownership: user projects own initialized copies; this repository owns the canonical payload.
- Security boundary: existing target files are never overwritten when content differs.
- Release contract: repository-maintenance files must not appear under `template/`.

## Current Constraints

- Known limitation: remote bootstrap follows a Git branch or tag and therefore depends on Git/network unless `--source` is used.
- Operational constraint: project-specific initialization still requires repository context and user answers.
- Security / privacy constraint: bootstrap operates only on local files and the selected public Git source; no project contents are uploaded.

## Open Questions

| Question | Owner | Related REQ / TECH | Status |
|---|---|---|---|
| Should releases pin a version tag by default? | Maintainer | [[08-technical-designs/approved/TECH-20260618170500-shareable-workflow-skill]] | deferred |

## Writeback Log

| Date | Source TECH / review | Change |
|---|---|---|
| 2026-06-18 | [[08-technical-designs/approved/TECH-20260618170500-shareable-workflow-skill]] | Separated downstream payload from repository maintenance |
