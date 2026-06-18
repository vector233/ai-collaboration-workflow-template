---
title: E2E Test Runbook
status: draft
project: AI Collaboration Workflow Template
last_verified_at: 2026-06-18
source_of_truth: mixed
related:
  - "[[00-governance/ai-workflow]]"
  - "[[00-governance/validation-discipline]]"
  - "[[07-review/README]]"
  - "[[05-reference/fresh-agent-resume-evaluation]]"
---

# E2E Test Runbook

## What This Answers

This note records the project-specific commands and evidence rules for realistic validation. [[00-governance/validation-discipline]] defines when realistic validation is required; this runbook defines how to perform it for this project.

## Local Checks

<!-- Fill in during initialization or first implementation slice. -->

| Area | Command | Notes |
|---|---|---|
| Docs | `git diff --check` | No trailing whitespace or patch formatting issues |
| Distribution | `python3 scripts/validate_distribution.py` | Validates clean payload, bootstrap, state directories, and first workflow files |
| Bootstrap preview | `python3 skills/ai-collaboration-workflow/scripts/bootstrap_template.py --source . --target <tmp> --dry-run` | Must not modify target |
| Skill | `quick_validate.py skills/ai-collaboration-workflow` | Requires PyYAML in the validation runtime |

## Browser / UI Smoke

- Not applicable; the project has no browser UI.

## API / Integration Smoke

- Environment: temporary local directory
- Auth setup: none
- Required read paths: `template/` and Skill files
- Required write paths: temporary target only
- Cleanup: validator removes temporary files automatically

## Real Environment Smoke

Use this section for staging, device, installer, desktop, mobile, hardware, provider sandbox, or other realistic validation.

- Environment: local filesystem plus optional public Git clone
- Build artifact: repository checkout
- Setup: Python 3; Git only for remote-source smoke
- Command or manual flow: run distribution validator, then optional remote bootstrap dry-run
- Pass criteria: clean payload, complete state directories, no maintenance leakage, first REQ/TECH/REVIEW creation succeeds
- Evidence to paste into review: command, exit code, and summary

## Evidence Redaction Rules

Do not paste:

- secrets or tokens;
- real passwords;
- private customer data;
- full production payloads;
- unredacted logs that contain credentials, personal data, or business-sensitive content.

Prefer:

- short command summaries;
- sanitized request/response excerpts;
- screenshot paths or trace links;
- aggregate counts;
- commit SHA and environment name.

## Known Gaps

| Gap | Risk | Owner | Next action |
|---|---|---|---|
| Longitudinal fresh-agent resume test requires a clean AI session | Core memory value remains only partially proven | Maintainer | Run [[05-reference/fresh-agent-resume-evaluation]] across multiple real-project slices |
