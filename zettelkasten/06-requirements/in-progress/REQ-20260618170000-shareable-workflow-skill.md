---
title: Shareable AI Collaboration Workflow Skill
status: in-progress
project: AI Collaboration Workflow Template
requirement_id: REQ-20260618170000-shareable-workflow-skill
last_verified_at: 2026-06-18
source_of_truth: mixed
affected_projects:
  - template repository
related:
  - "[[00-governance/ai-workflow]]"
  - "[[01-overview/quick-reference]]"
  - "[[02-architecture/current-architecture-flow]]"
  - "[[05-reference/e2e-test]]"
  - "[[08-technical-designs/README]]"
  - "[[07-review/README]]"
---

# Shareable AI Collaboration Workflow Skill

## What This Requirement Answers

This document defines how the repository's companion Skill should guide an AI agent both when applying the workflow in an initialized project and when bootstrapping the template into a project that does not have it.

## Background

- Business context: users should be able to share and install one Skill that teaches an AI agent how to use this repository's workflow.
- Trigger: the existing Skill describes bootstrap steps but relies on ad hoc shell commands and does not provide a validated, conflict-safe bootstrap tool.
- Current pain: copying from the template repository can overwrite local instruction files, and the Skill has no executable validation path for template presence or initialization readiness.

## Goals

- Provide a shareable Agent Skills-compatible Skill for daily REQ/TECH/REVIEW workflow guidance.
- Provide a deterministic bootstrap script that can source the template from a local checkout or the canonical Git repository.
- Preserve existing project files by default and report conflicts for AI-assisted merging.
- Document initialization, validation, and post-bootstrap authority clearly.
- Define one canonical downstream template payload that excludes this repository's maintenance evidence.
- Make the repository itself use an initialized knowledge base instead of template placeholders.
- Provide an executable distribution smoke test that creates the first workflow artifacts.

## Non-Goals

- Do not make the Skill a second canonical copy of the full template.
- Do not silently merge arbitrary existing `AGENTS.md`, `CLAUDE.md`, or project knowledge.
- Do not automate project-specific answers that require user or repository context.
- Do not publish, install globally, commit, or push the Skill as part of this slice.
- Do not keep advertising the repository root as a clean GitHub Template while maintenance files live beside the payload.

## Context Pack

- Current workflow: [[00-governance/ai-workflow]]
- Requirement rules: [[06-requirements/README]]
- Technical design rules: [[08-technical-designs/README]]
- Review rules: [[07-review/README]]
- Template initialization runbook: `template/INIT.md`
- Existing Skill: `skills/ai-collaboration-workflow/SKILL.md`

## Confirmed Facts

- The repository already contains an Agent Skills-compatible Skill folder.
- The root currently mixes downstream template files with repository-maintenance files.
- GitHub's template-repository feature copies the whole repository and cannot exclude maintenance files.
- Initialization requires project-specific user answers and must continue to be driven by `INIT.md`.
- Existing project instruction files must not be overwritten without inspection.

## Open Questions

- None blocking this slice.

## Impact

### Projects / Modules

- `skills/ai-collaboration-workflow/`
- `template/`
- Root project knowledge and validation scripts
- Repository usage documentation
- Workflow requirement, design, and review notes

### Interfaces / Data / Jobs / Config

- CLI: bootstrap script arguments and exit codes.
- Filesystem: copies template runtime files into a target repository.
- Network: optional canonical Git repository clone when no local source is supplied.
- Security: no credentials, customer data, or production state involved.

## Proposed Change

- Add a Python bootstrap script with inspect, dry-run, local-source, remote-source, and conflict reporting behavior.
- Move the canonical downstream payload under `template/`.
- Initialize the root knowledge base for this repository and keep maintenance REQ/TECH/REVIEW files there.
- Rewrite the Skill instructions around a clear presence check, bootstrap flow, initialization flow, daily workflow, and validation contract.
- Keep the target repository's initialized files authoritative after bootstrap.
- Update English and Chinese usage documentation.

## Technical Design

- Technical design: [[08-technical-designs/approved/TECH-20260618170500-shareable-workflow-skill]]
- Current state: approved
- If waived, reason: not applicable

## Implementation Slices

- Slice 1: add requirement and approved technical design.
- Slice 2: implement the bootstrap script and Skill instructions.
- Slice 3: validate bootstrap behavior in temporary repositories and create the review handoff.
- Slice 4: address review findings by separating the payload, dogfooding the root knowledge base, and adding distribution E2E validation.

## Acceptance Criteria

- Installing or sharing only the Skill gives an AI agent enough guidance to bootstrap the canonical template.
- The bootstrap script never overwrites a differing existing file by default.
- A local template checkout can be used without network access.
- A remote canonical repository can be used when no local source is available.
- The Skill distinguishes template bootstrap from project-specific initialization.
- The Skill validates with `quick_validate.py`.
- Focused tests cover missing-file copy, identical-file skip, conflict reporting, dry-run, and template-presence inspection.
- Every documented install path includes `INIT.md` and produces all workflow state directories.
- Downstream payload contains no repository-specific publishing or maintenance records.
- The root knowledge base describes this repository with no unresolved project placeholders.
- A distribution smoke test bootstraps a temporary project and creates sample REQ, TECH, and REVIEW files.

## Validation Record

- Skill validation: `quick_validate.py` passed.
- Bootstrap script tests: local repository/direct payload source, dry-run/install/inspect, identical rerun, conflict protection, symlink protection, complete state directories, maintenance-artifact exclusion, and temporary Git clone source passed.
- Distribution lifecycle: sample initialization and first REQ/TECH/REVIEW creation passed through `python3 scripts/validate_distribution.py`.
- Documentation checks: `git diff --check` and Python compile checks passed.
- Placeholder and wiki-link checks: task-scoped placeholder scan and new workflow-document wiki-link checks passed.

## Review Handoff

- Review document: [[07-review/in-review/REVIEW-20260618174000-shareable-workflow-skill]]

## Review Feedback Handling

| Round | Source | Evidence | Feedback summary | Judgment | Status | Fix commit / counter-evidence |
|---|---|---|---|---|---|---|
| Round 1 | Project review | Reproducible commands and file locations in linked review | Distribution and self-dogfooding gaps | confirmed | fixed | uncommitted; see linked review evidence |

## Documentation Writeback Checklist

- Skill usage in root README: complete
- Chinese usage guide: complete
- Durable contribution boundary: recorded in `CONTRIBUTING.md`
- Architecture note: updated [[02-architecture/current-architecture-flow]]
- Decisions and gotchas: updated for payload ownership and empty-directory failure
- Longitudinal evaluation: added [[05-reference/fresh-agent-resume-evaluation]]

## Evidence Checklist

- Code evidence: bootstrap script and Skill diff
- Validation evidence: command output recorded in linked review handoff
- Worktree evidence: `git status --short`
