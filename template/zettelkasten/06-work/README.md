---
title: Work Items
status: active
project: {{PROJECT_NAME}}
last_verified_at: YYYY-MM-DD
source_of_truth: project
related:
  - "[[00-governance/ai-workflow]]"
  - "[[00-governance/git-collaboration]]"
  - "[[00-governance/skill-lifecycle]]"
---

# Work Items

Workflow artifacts live in this directory for their entire lifecycle. Never move a file to represent status; update frontmatter in place.

## Artifact Types

| Prefix | Purpose | Typical states |
|---|---|---|
| `WORK-*` | canonical task state and default all-in-one record | backlog, active, blocked, review, done, cancelled |
| `TECH-*` | optional independent technical decision | pending, approved, implemented, superseded |
| `PLAN-*` | optional independent execution coordination | draft, ready, executing, completed, superseded |
| `REVIEW-*` | optional independent review lifecycle | pending, in-review, done, waived |

Create separate TECH, PLAN, or REVIEW files only when they have an independent lifecycle. Ordinary tracked work stays in one `WORK-*`.

## Naming

Use stable timestamped IDs:

- `WORK-YYYYMMDDHHMMSS-short-name.md`
- `TECH-YYYYMMDDHHMMSS-short-name.md`
- `PLAN-YYYYMMDDHHMMSS-short-name.md`
- `REVIEW-YYYYMMDDHHMMSS-short-name.md`

## Resume

Inspect the current Git branch, select the matching active work item, and read its context pack, checkpoint, validation, and next action. Do not maintain a second manual current-state document.

Update the Markdown file directly. Optional companion-Skill helpers may automate creation, status inspection, and closure without owning any separate state.
