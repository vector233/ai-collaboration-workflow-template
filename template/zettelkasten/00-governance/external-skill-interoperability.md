---
title: External Skill Interoperability
status: active
project: {{PROJECT_NAME}}
last_verified_at: YYYY-MM-DD
source_of_truth: project
related:
  - "[[AI]]"
  - "[[00-governance/ai-workflow]]"
  - "[[06-work/README]]"
---

# External Skill Interoperability

External process Skills are optional execution aids. Repository work items, knowledge notes, runbooks, and project Skills remain the durable source of truth.

## Mapping

| External output | Canonical destination |
|---|---|
| goals, scope, acceptance | active `WORK-*` |
| architecture or risk decisions | inline approach or independent `TECH-*` |
| detailed sequencing | inline slices or independent `PLAN-*` |
| execution, TDD, debugging, review evidence | active `WORK-*` or independent `REVIEW-*` |
| reusable lesson | Experience Promotion destination or project Skill |

Do not create a tool-specific parallel tree unless the user explicitly requests an export. External Git defaults do not override [[00-governance/git-collaboration]].

## No External Skill Installed

No external command, plugin, directory, or document is required. Follow [[00-governance/ai-workflow]] directly:

```text
route -> [WORK] -> [TECH / PLAN / REVIEW only when triggered] -> validate -> commit -> promote experience
```
