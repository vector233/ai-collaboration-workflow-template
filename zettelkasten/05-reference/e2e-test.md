---
title: E2E Test Runbook
status: draft
project: {{PROJECT_NAME}}
last_verified_at: YYYY-MM-DD
source_of_truth: mixed
related:
  - "[[00-governance/agent-harness]]"
  - "[[00-governance/e2e-discipline]]"
  - "[[07-review/README]]"
---

# E2E Test Runbook

## What This Answers

This note records the project-specific commands and evidence rules for realistic validation. [[00-governance/e2e-discipline]] defines when realistic validation is required; this runbook defines how to perform it for this project.

## Local Checks

<!-- Fill in during initialization or first implementation slice. -->

| Area | Command | Notes |
|---|---|---|
| Docs | `git diff --check` | No trailing whitespace or patch formatting issues |
| Backend |  |  |
| Frontend |  |  |
| Database |  |  |

## Browser / UI Smoke

- Tool:
- Base URL:
- Test accounts note:
- Required flows:
- Screenshot or trace location:

## API / Integration Smoke

- Environment:
- Auth setup:
- Required read paths:
- Required write paths:
- Cleanup:

## Real Environment Smoke

Use this section for staging, device, installer, desktop, mobile, hardware, provider sandbox, or other realistic validation.

- Environment:
- Build artifact:
- Setup:
- Command or manual flow:
- Pass criteria:
- Evidence to paste into review:

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
|  |  |  |  |
