---
title: Real-Environment E2E Discipline
status: active
project: {{PROJECT_NAME}}
last_verified_at: YYYY-MM-DD
source_of_truth: mixed
related:
  - "[[00-governance/agent-harness]]"
  - "[[07-review/README]]"
  - "[[05-reference/e2e-test]]"
  - "[[00-governance/gotchas]]"
---

# Real-Environment E2E Discipline

## What This Answers

This note defines when a slice must be validated outside unit tests before review. The rule is intentionally generic: any behavior that depends on a real browser, database engine, external provider, device, installer, queue, scheduler, filesystem, network, or operating system needs a realistic smoke test before it is treated as review-ready.

Project-specific commands belong in [[05-reference/e2e-test]]. This note defines the policy.

## Why This Exists

Local tests often verify code assumptions, not environment facts. Common failure modes:

- a real database schema differs from fixtures;
- browser behavior differs from component assumptions;
- third-party sandbox state differs from mocked responses;
- installers or desktop/mobile packages fail on the target OS;
- scheduled jobs, queues, retries, and idempotency fail only under realistic timing;
- credentials, DNS, TLS, ports, permissions, or filesystem paths differ from local development.

For affected slices, review handoff without realistic evidence pushes discovery to the reviewer or the next development slice.

## Rule

Before moving a slice into `07-review/pending/`, the development owner must:

1. Run the most realistic smoke test available for the changed behavior.
2. Record pass/fail, commands, inputs, outputs, screenshots/log summaries, and relevant environment in the review handoff.
3. If the smoke test exposes an environment mismatch, write the lesson to [[00-governance/gotchas]] or a module-specific gotchas note before or alongside the fix.
4. If realistic validation cannot run, record the blocker, owner, and residual risk in the review handoff.

Reviewers should reject or mark blocked any handoff that claims readiness for environment-dependent behavior but has no realistic validation evidence and no explicit blocker.

## Default Triggers

Run a realistic smoke test when a slice touches:

- browser-visible UI flows;
- authentication, authorization, billing, quotas, or entitlements;
- database migrations, raw SQL, indexes, schema assumptions, or data backfills;
- third-party APIs, webhooks, email/SMS/push, payments, maps, storage, analytics, or AI providers;
- installers, desktop apps, mobile apps, hardware integrations, OS services, permissions, or file paths;
- queues, cron jobs, workers, retries, idempotency, locks, or long-running processes;
- deployment, DNS, TLS, secrets, environment variables, ports, or ingress routing.

## Evidence To Record

At minimum:

- command or manual flow executed;
- environment used;
- commit SHA or build artifact;
- pass/fail result;
- important request/response or screenshot/log summary;
- redacted sensitive values;
- known gaps that remain untested.

Do not paste secrets, tokens, customer data, private payloads, or full production logs.

## Project-Specific Runbook

Maintain the actual commands in [[05-reference/e2e-test]]. Suggested sections:

- local build/test/lint commands;
- browser or Playwright flows;
- database migration verification;
- third-party sandbox setup;
- staging smoke;
- real-device/installer/mobile/desktop smoke;
- evidence redaction rules.

## Relationship To Review

[[07-review/README]] owns the review workflow. This note is a review readiness gate. A slice can still be handed off with a blocker, but the review document must clearly say that validation is incomplete and why.
