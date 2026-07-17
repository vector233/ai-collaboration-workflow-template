---
title: Git Collaboration
status: active
project: {{PROJECT_NAME}}
last_verified_at: YYYY-MM-DD
source_of_truth: project
review_after_days: 180
related:
  - "[[workflow]]"
  - "[[work/README]]"
---

# Git Collaboration

## Default Policy

- Keep the default branch integration-only for tracked and governed work.
- Give every work item one task branch.
- Give every concurrently active task or write-capable agent one worktree.
- Never share one worktree or branch between concurrent write-capable agents.
- Do not parallelize dependent tasks or tasks with materially overlapping owned paths without an integration plan.

Read-only delegated agents may inspect the current task worktree without a second checkout when their scopes are independent. A write-capable delegated agent works serially in the current task worktree; any concurrent write task gets its own task branch and worktree.

Recommended branch name:

```text
task/<work-id>
```

Create isolated work with normal Git:

```bash
work_id="WORK-$(date +%Y%m%d%H%M%S)-<short-name>"
git worktree add ../<short-name> -b "task/${work_id}" <base>
```

Use the same ID for the WORK filename and task branch. Confirm the base commit and do not silently reuse an existing task branch. The optional companion Skill provides a guarded helper for this operation.

Use a normal branch in the current checkout for one sequential task. Use a worktree when write-capable work overlaps in time, must preserve an existing dirty checkout, or is delegated to another write-capable agent. Independent read-only specialists may inspect the current task worktree.

Detached worktrees do not claim branch-owned active WORK until attached to the declared task branch.

## Context Commit Contract

Every agent context that produces persistent changes, or each coherent implementation slice, ends with a commit containing only current-task changes. Read-only analysis does not create an empty commit.

- Validated slice: use a conventional commit such as `fix(api): reject expired token`.
- Incomplete handoff: use `checkpoint:` or `wip:` only on the task branch.
- Record `Task`, `Validation`, and optional `Context` trailers in the commit body when useful.
- Never merge a broken checkpoint into the default branch.
- Before handoff, update the `WORK-*` checkpoint with commit, validation, worktree status, and next action.

## Integration

- Rebase or merge the latest default branch before final validation when repository policy requires it.
- Task branches should normally record experience candidates before editing shared rules. At promotion or integration, add the selected shared destination to `owned_paths`, check active overlap, and coordinate one writer; other tasks defer or consume the integrated result.
- Preserve per-context commits with a normal or no-fast-forward merge when traceability is required. Squash only when the repository explicitly prefers a compact integration history.
- Close the work item, validate, and remove the worktree only after integration is confirmed.
