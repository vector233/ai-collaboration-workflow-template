# Git Isolation And Context Commits

## Choose Isolation

- Direct low-risk work may use the current non-protected branch when repository policy allows it.
- Tracked or governed work uses a dedicated task branch.
- Concurrent tasks, delegated agents, long-lived tasks, or work that must preserve another dirty checkout use separate Git worktrees.
- Dependent tasks or materially overlapping owned paths should run serially or define an explicit integration plan.

Use the repository helper when available:

```bash
python3 scripts/task_worktree.py create <WORK-ID> --slug <short-name>
python3 scripts/task_worktree.py list
```

## Commit Contract

At the end of each agent context or coherent slice:

1. inspect the diff and exclude unrelated files;
2. run the smallest meaningful validation;
3. update the WORK checkpoint and experience candidates;
4. commit all current-task changes;
5. record the commit and next action.

Use conventional commits for validated slices. Use `checkpoint:` or `wip:` only on task branches when incomplete state must be handed off. Never merge a broken checkpoint into the default branch.

Delay shared `AGENTS.md`, runbook, and project-Skill edits until closeout when practical. This lets parallel branches record candidates without competing over shared knowledge files.
