---
title: Validation Discipline
status: active
project: {{PROJECT_NAME}}
last_verified_at: YYYY-MM-DD
source_of_truth: mixed
related:
  - "[[00-governance/ai-workflow]]"
  - "[[07-review/README]]"
  - "[[05-reference/e2e-test]]"
  - "[[00-governance/gotchas]]"
---

# Validation Discipline

## Purpose

This note defines when a change needs realistic validation before review. Project-specific commands belong in [[05-reference/e2e-test]]. This note defines the policy.

## Rule

Before moving a slice into `07-review/pending/`, the owner should run the most realistic smoke test available for the changed behavior, or clearly record why that validation could not be run.

The review handoff should include:

- command or manual flow executed;
- environment used;
- commit SHA or build artifact;
- pass/fail result;
- important request/response, screenshot, or log summary;
- redacted sensitive values;
- known gaps that remain untested.

When workflow files, requirements, technical designs, implementation plans, review handoffs, wiki links, or initialization state changed, run:

```bash
python3 scripts/workflow_doctor.py
```

Fix reported errors before handoff. Informational open-review or active-requirement messages are routing constraints, not validation failures.

## When Realistic Validation Matters

Run a realistic smoke test when a slice touches:

- browser-visible UI flows;
- authentication, authorization, billing, quotas, or entitlements;
- database migrations, raw SQL, indexes, schema assumptions, or data backfills;
- third-party APIs, webhooks, email/SMS/push, payments, maps, storage, analytics, or AI providers;
- installers, desktop apps, mobile apps, hardware integrations, OS services, permissions, or file paths;
- queues, cron jobs, workers, retries, idempotency, locks, or long-running processes;
- deployment, DNS, TLS, secrets, environment variables, ports, or ingress routing.

## Why This Exists

Local tests often verify code assumptions, not environment facts. Common failure modes:

- a real database schema differs from fixtures;
- browser behavior differs from component assumptions;
- third-party sandbox state differs from mocked responses;
- installers or packaged apps fail on the target OS;
- scheduled jobs, queues, retries, and idempotency fail only under realistic timing;
- credentials, DNS, TLS, ports, permissions, or filesystem paths differ from local development.

## Redaction Rules

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

## Relationship To Review

[[07-review/README]] owns the review workflow. This note is a review readiness policy. A slice can still be handed off with a blocker, but the review document must clearly say that validation is incomplete and why.
