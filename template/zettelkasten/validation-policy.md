---
title: Validation Discipline
status: active
project: {{PROJECT_NAME}}
last_verified_at: YYYY-MM-DD
source_of_truth: mixed
review_after_days: 180
related:
  - "[[workflow]]"
  - "[[work/README]]"
  - "[[validation-runbook]]"
  - "[[gotchas]]"
---

# Validation Discipline

## Purpose

This note defines when a change needs realistic validation before review. Project-specific commands belong in [[validation-runbook]]. This note defines the policy.

## Rule

Before a slice enters review or is committed as complete, run the most realistic smoke test available for the changed behavior, or clearly record why it could not run.

The review handoff should include:

- command or manual flow executed;
- environment used;
- commit SHA or build artifact;
- pass/fail result;
- important request/response, screenshot, or log summary;
- redacted sensitive values;
- known gaps that remain untested.

When work items, project Skills, workflow files, wiki links, or initialization state change, inspect their links, required fields, and routing entries before handoff. Routine checks use current knowledge, open-work routes and exact dependencies; they do not read archived bodies or prove complete historical coverage. Use an explicit full audit for route completeness, final Initiative membership, archive checksums and historical links, including after a lifecycle migration. See [[knowledge-lifecycle]]. The optional companion Skill can automate this check, but validation evidence remains in repository files.

## Knowledge Recoverability

Treat knowledge health as two separate checks:

- **Structural check**: the branch maps to one active WORK, required checkpoint fields and links exist, shared destinations are represented in `owned_paths`, matching project Skills are reachable from the index, and any Initiative or external-parent relationship remains bounded and unambiguous. Local Initiative IDs resolve, WORK dependencies exist without cycles, and terminal Initiative state does not hide active children.
- **Semantic Fresh-Agent Resume Probe**: an agent with no prior chat starts from `AGENTS.md` and [[AI]], uses the current branch to select the WORK, loads only linked knowledge, and reports the route, acceptance state, checkpoint and commit, validation, unresolved risk, next allowed action, pending or decided experience candidates, and matching project Skill before implementation. It recognizes a declared local Initiative or authoritative external parent, loads the Initiative only for a relevant shared constraint, and does not load sibling WORK records. It distinguishes already active knowledge from a candidate that has not been promoted or updated yet.

Run structural checks at normal handoff. Run the semantic probe only for an important multi-context handoff, after changing workflow or resume semantics, or before a release where failed recovery would be costly. Record a concise result and provenance in the WORK or project-native review evidence; retain the unedited prompt, response, agent or model identity, and time there when the full evidence matters. A synthetic or copied expected response can test an evaluator, but it is not evidence that a fresh agent recovered the work.

The probe requires no helper and must not edit the repository. Failure means the checkpoint or knowledge routing is incomplete even when every file exists.

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

[[work/README]] owns workflow state. A slice can still be handed off with a blocker, but the work item or independent review must clearly say that validation is incomplete and why.
