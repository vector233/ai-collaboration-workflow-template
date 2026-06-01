---
title: Current Architecture Flow
status: active
project: {{PROJECT_NAME}}
last_verified_at: YYYY-MM-DD
source_of_truth: mixed
related:
  - "[[00-governance/project-overview]]"
  - "[[00-governance/agent-harness]]"
  - "[[08-technical-designs/README]]"
---

# Current Architecture Flow

## What This Answers

This note should describe how the current system actually works today. It is the architecture fact base that agents read before changing behavior.

Keep it current. After an implemented TECH changes system flow, write the still-true conclusions back here or into a more specific architecture note.

## System Components

<!-- Replace with the actual components in the initialized project.

| Component | Responsibility | Runtime / owner |
|---|---|---|
| Web app | User-facing UI | frontend |
| API | HTTP API and business rules | backend |
| Worker | Async jobs | backend |
| Database | Persistent state | PostgreSQL |
-->

## Main Flow

<!-- Describe the 5-10 most important end-to-end steps.

1. User performs an action in the UI.
2. UI calls the API with authenticated request.
3. API validates permissions and writes domain state.
4. Worker processes async side effects.
5. UI receives status through polling, push, or refresh.
-->

## Contracts

- Public APIs:
- Internal APIs:
- Data ownership:
- Auth / permission boundaries:
- Event or job contracts:

## Current Constraints

- Known limitation:
- Operational constraint:
- Security / privacy constraint:

## Open Questions

| Question | Owner | Related REQ / TECH | Status |
|---|---|---|---|
|  |  |  |  |

## Writeback Log

| Date | Source TECH / review | Change |
|---|---|---|
| YYYY-MM-DD |  | Initial placeholder |
