---
title: Implementation Plans
status: active
project: {{PROJECT_NAME}}
last_verified_at: YYYY-MM-DD
source_of_truth: mixed
related:
  - "[[00-governance/ai-workflow]]"
  - "[[06-requirements/README]]"
  - "[[08-technical-designs/README]]"
  - "[[00-governance/templates/implementation-plan]]"
  - "[[07-review/README]]"
---

# 09-implementation-plans

## Purpose

This directory stores optional standalone implementation plans. A PLAN explains execution order, dependencies, file ownership, checkpoints, and per-slice validation. It does not replace the REQ or TECH.

## When To Create A Standalone PLAN

Create one when the REQ marks it required because:

- multiple implementation slices depend on each other;
- work spans multiple sessions, agents, owners, modules, or repositories;
- migration, rollout, or release order matters;
- file ownership and interfaces between slices must be explicit;
- each slice needs its own validation and review checkpoint.

Do not create one for a bounded task whose implementation slices fit clearly in the REQ.

## Workflow

1. Confirm the REQ marks standalone PLAN as required.
2. Copy [[00-governance/templates/implementation-plan]] into this directory.
3. Link the controlling REQ and any TECH.
4. Set `status: ready` only when dependencies, files, sequence, validation, and stop conditions are explicit.
5. During implementation, use `status: executing` and keep the current slice and resume point current.
6. If reality invalidates the plan, update it before continuing dependent work.
7. Set `status: completed` after all slices are implemented, validated, reviewed, and written back.
8. Use `status: superseded` when another PLAN replaces it.

## Naming

Use:

- `PLAN-YYYYMMDDHHMMSS-short-name.md`

## Minimum Contents

- linked REQ and optional TECH;
- goal and global constraints;
- dependency and execution order;
- exact affected paths or ownership boundaries;
- per-slice deliverables and validation;
- checkpoints, stop conditions, risks, and resume point.

## States

| Status | Meaning |
|---|---|
| `draft` | Still being decomposed; not implementation input |
| `ready` | Safe to use as implementation input |
| `executing` | At least one slice is active |
| `completed` | All planned work is reviewed and written back |
| `superseded` | Replaced by another PLAN |

PLAN status lives in frontmatter; plans do not need separate state directories.
