---
title: Shareable AI Collaboration Workflow Skill
status: in-review
project: AI Collaboration Workflow Template
review_id: REVIEW-20260618174000-shareable-workflow-skill
created: 2026-06-18
reviewer:
target:
  - "[[06-requirements/in-progress/REQ-20260618170000-shareable-workflow-skill]]"
  - "[[08-technical-designs/approved/TECH-20260618170500-shareable-workflow-skill]]"
related:
  - "[[07-review/README]]"
---

# Shareable AI Collaboration Workflow Skill

## What This Review Answers

This handoff records the implementation and validation evidence for the portable Skill bootstrap and daily workflow guidance.

## Task Goal And Scope

- Goal: make the companion Skill shareable and capable of guiding or executing safe template bootstrap before project-specific initialization.
- This slice covers: canonical payload separation, initialized root project knowledge, Skill instructions, UI metadata, bootstrap script, distribution E2E, English and Chinese usage docs, contribution boundary, requirement, technical design, and review evidence.
- This slice does not cover: publishing the Skill, global installation, semantic conflict merging, a versioned offline template archive, or independent sub-agent forward testing.

## Completed Changes

- Reworked `SKILL.md` around repository-state classification, safe bootstrap, `INIT.md` initialization, daily workflow gates, validation, and target-repository authority.
- Added `scripts/bootstrap_template.py` with local or remote source selection, dry-run, inspection, conflict protection, symlink protection, and explicit exit codes.
- Added canonical `template/` payload with an explicit source marker and complete empty workflow state directories.
- Initialized the root knowledge base for this repository and separated maintenance REQ/TECH/REVIEW and publishing material from downstream content.
- Added `scripts/validate_distribution.py` to test payload boundaries, local and Git clone sources, dry-run, identical rerun, conflict and symlink safety, sample initialization, wiki links, and first REQ/TECH/REVIEW creation.
- Added a repeatable fresh-agent resume evaluation for longitudinal continuity testing.
- Updated `agents/openai.yaml`, root README, Chinese guide, and contribution guidance.

## Latest Commit

- Implementation commit: `2b48c31` (`feat: harden workflow template distribution`) on `main`.
- Handoff metadata: committed separately after recording the implementation SHA.
- PR / MR: none.

## Validation Results

- Skill schema: `quick_validate.py skills/ai-collaboration-workflow` passed using temporary PyYAML dependencies.
- UI metadata: YAML parse, short-description length, and `$ai-collaboration-workflow` default prompt checks passed.
- Python syntax: `python3 -m compileall -q -f scripts skills/ai-collaboration-workflow/scripts` passed; generated caches were removed.
- Distribution lifecycle: `python3 scripts/validate_distribution.py` passed.
- Local bootstrap: repository-root and direct-payload sources, dry-run, install, inspect, identical rerun, and complete state directories passed.
- Conflict safety: differing `AGENTS.md` content remained unchanged and returned exit code `2`.
- Symlink safety: a target `zettelkasten` symlink was reported as conflict and no file was written through it.
- Git source: validator created and cloned a temporary Git repository with the current `template/` layout; remote-style bootstrap passed.
- Initialization smoke: sample placeholder replacement, single-repository pruning, `INIT.md` removal, wiki-link validation, and first REQ/TECH/REVIEW creation passed.
- Payload isolation: repository URL, publishing runbook, and maintenance task IDs are absent from `template/`.
- Root dogfood: root project index, overview, product vision, architecture, roadmap, validation runbook, decisions, and gotchas contain concrete project context.
- Documentation: `git diff --check` passed.
- Links: wiki links in the new REQ and TECH documents resolve.
- Placeholders: task-scoped placeholder scan passed; canonical template placeholders remain intentionally in template source files.

## Current Worktree Status

- Branch: `main`, tracking `origin/main`.
- Modified: root repository guidance, English and Chinese docs, Skill metadata/instructions, and initialized root knowledge notes.
- Deleted from root maintenance project: `INIT.md` and the placeholder-named project index; their canonical template versions now live under `template/`.
- Added: canonical `template/` payload, bootstrap and distribution scripts, initialized project index, fresh-agent evaluation, and active REQ/TECH/REVIEW documents.
- No unrelated paths or generated caches were detected.

## Known Risks / Blockers

- Risk: remote bootstrap follows `main` by default, so an old installed Skill can fetch a newer template. Use `--ref` with a release branch or tag when reproducibility is required.
- Release dependency: resolved when commits containing the marked `template/` payload are pushed to `origin/main`. Pre-push validation used a temporary Git repository containing the current worktree layout.
- Risk: conflict resolution remains an AI-assisted manual merge because arbitrary repository instructions cannot be merged safely by a generic script.
- Risk: the script assumes Python 3.9+ and Git for remote bootstrap; `--source` removes the Git and network requirement.
- Residual validation gap: the distribution lifecycle is executable, but the core long-term-memory claim still needs repeated clean-agent runs in real software projects. Use [[05-reference/fresh-agent-resume-evaluation]].

## Next Steps

- Next: review the canonical payload boundary, bootstrap marker contract, and distribution validator.
- Work that should wait until review closes: move the REQ to `done/`, move the TECH to `implemented/`, publish, install globally, commit, or push.

## Suggested Review Focus

- Confirm that target-repository authority and bootstrap-versus-initialization boundaries are unambiguous.
- Confirm that `template/` contains every downstream file and no repository-maintenance content.
- Confirm exit code `2` is appropriate for both incomplete inspection and non-destructive conflicts.
- Confirm following `main` by default is acceptable for the first release.

## Reviewer Feedback

| Round | Feedback summary | Evidence | Judgment | Status |
|---|---|---|---|---|
| Round 1 | Bootstrap omits workflow state directories | Original failure reproduced; distribution validator now creates first workflow artifacts successfully | confirmed | fixed in `2b48c31` |
| Round 1 | Manual installation omits `INIT.md` | English and Chinese instructions now copy `template/.`, explicitly including `INIT.md` | confirmed | fixed in `2b48c31` |
| Round 1 | Template payload contains repository-maintenance material | Canonical payload moved to `template/`; leakage scan and clean-state checks pass | confirmed | fixed in `2b48c31` |
| Round 1 | Repository does not dogfood an initialized knowledge base | Root project knowledge is initialized and has no unresolved project placeholders outside reusable templates | confirmed | fixed in `2b48c31` |
| Round 1 | Long-lived workflow has no executable distribution smoke | `scripts/validate_distribution.py` passes; fresh-agent continuity has a repeatable evaluation runbook | confirmed | fixed in `2b48c31` with residual longitudinal validation |

## Close Conditions

- Important feedback has evidence.
- The implementation owner has verified each item.
- Confirmed or partial issues are fixed, validated, and committed.
- Rejected issues have counter-evidence.
- This review round is explicitly closed.
