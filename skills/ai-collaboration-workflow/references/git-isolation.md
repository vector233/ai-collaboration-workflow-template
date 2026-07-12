# Git Isolation And Context Commits

## Choose Isolation

- Direct low-risk work may use the current non-protected branch when repository policy allows it.
- Tracked or governed work uses a dedicated task branch.
- Concurrent tasks, delegated agents, long-lived tasks, or work that must preserve another dirty checkout use separate Git worktrees.
- Dependent tasks or materially overlapping owned paths should run serially or define an explicit integration plan.

Use normal Git or the bundled guarded helper:

```bash
git worktree add ../<short-name> -b task/<work-id>-<short-name> <base>
(cd <repo-root> && python3 "$SKILL_ROOT/scripts/task_worktree.py" create <WORK-ID> --slug <short-name>)
```

The helper may create a new worktree while the current checkout is dirty; it warns that uncommitted changes stay in the original checkout. It refuses to reuse an existing task branch unless `--reuse-existing` is explicit, and `--base` is never applied to a reused branch.

When machine-readable coordination helps, use `python3 "$SKILL_ROOT/scripts/workflow_doctor.py" --root <repo-root> --status --all-worktrees --json` to aggregate active work and possible owned-path overlap.

## Commit Contract

At the end of each agent context that produces persistent changes, or each coherent slice:

1. inspect the diff and exclude unrelated files;
2. run the smallest meaningful validation;
3. update the WORK checkpoint and experience candidates;
4. commit all current-task changes;
5. record the commit and next action.

Use conventional commits for validated slices. Use `checkpoint:` or `wip:` only on task branches when incomplete state must be handed off. Never merge a broken checkpoint into the default branch.

Do not create an empty commit for a read-only analysis or review context.

Delay shared `AGENTS.md`, runbook, and project-Skill edits until closeout when practical. This lets parallel branches record candidates without competing over shared knowledge files.
