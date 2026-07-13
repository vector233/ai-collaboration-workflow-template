---
title: Work Items
status: active
project: {{PROJECT_NAME}}
last_verified_at: YYYY-MM-DD
source_of_truth: project
related:
  - "[[workflow]]"
  - "[[git-collaboration]]"
  - "[[skill-lifecycle]]"
---

# Work Items

Tracked and governed work items live in this directory for their entire lifecycle. Never move a file to represent status; update frontmatter in place.

## Artifact Types

| Prefix | Purpose | Typical states |
|---|---|---|
| `WORK-*` | canonical task state, governed gates, validation, review, and handoff | backlog, active, blocked, review, done, cancelled |

## Naming

Use stable timestamped IDs:

- `WORK-YYYYMMDDHHMMSS-short-name.md`

## Resume

Inspect the current Git branch, select the matching active work item, and read its context pack, checkpoint, validation, and next action. Do not maintain a second manual current-state document.

Update the Markdown file directly. Optional companion-Skill helpers may automate creation, status inspection, and closure without owning any separate state.
