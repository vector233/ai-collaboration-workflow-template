# Upgrading An Initialized Repository

An initialized Repo Continuity project contains two kinds of value in the same files: upstream workflow improvements and repository-owned facts, rules, and learned procedures. A normal template copy cannot distinguish them. Repo Continuity therefore upgrades with a three-way reconciliation:

```text
recorded old upstream + current initialized project + target upstream
                              |
                              v
                    reviewable task-branch diff
```

## Upgrade Contract

The old upstream version comes from `Template baseline` in `zettelkasten/AI.md`. The target comes from the installed Companion Skill's pinned release. The current project remains authoritative for local facts and stricter policy.

The reconciler chooses these actions:

| Situation | Action |
|---|---|
| New upstream path, absent locally | add it |
| Upstream changed, local still matches the old baseline | adopt upstream |
| Local changed, upstream still matches the old baseline | preserve local |
| Both changed in independent text regions | apply a clean three-way merge |
| Both changed incompatibly, a local path is unsafe, or an addition collides | leave a conflict untouched |
| Upstream removed a path | leave a pending removal untouched |

The last two cases require judgment because a removal or overlap may affect project-owned knowledge. No command advances the baseline automatically.

## Recommended Flow

1. Install the Companion Skill for the target release.
2. Create one Tracked or Governed upgrade WORK on a task branch. Record the old and target releases, owned paths, validation plan, and rollback plan. Commit this pre-upgrade checkpoint so the worktree is clean.
3. Generate the detailed report and apply preview:

   ```bash
   python3 "$SKILL_ROOT/scripts/bootstrap_template.py" --target . --upgrade-report
   python3 "$SKILL_ROOT/scripts/bootstrap_template.py" --target . --upgrade-apply --dry-run
   ```

4. Apply the safe subset:

   ```bash
   python3 "$SKILL_ROOT/scripts/bootstrap_template.py" --target . --upgrade-apply
   ```

   Exit status 0 means no blocked paths remain. Status 2 means safe changes were applied but pending removals or conflicts still require review. Status 1 means a safety precondition failed and no planned file was written.

5. Resolve pending removals and conflicts. Preserve verified project facts, stricter local rules, and useful learned procedures. Do not restore `INIT.md` or the payload marker.
6. Run the project's validation, Repo Continuity Doctor or equivalent structural checks, and review the complete Git diff.
7. Update `Template baseline` to the target release only after the result is accepted. Record validation and the upgrade decision in the same WORK, complete the Learning Check, and commit.

Optional model-routing overlays participate only when `--with-model-routing codex`, `claude`, or `all` is explicitly passed. Use `--json` for an Agent-readable result and `--baseline-ref` only when the repository's recorded baseline cannot be resolved.

## Safety And Recovery

`--upgrade-apply` requires the repository root, a named branch other than `main` or `master`, and a clean worktree. Planned writes are transactional: if a write fails, earlier writes from that invocation are restored. Target symlinks and non-regular files are never followed.

The task branch and pre-upgrade commit are the rollback boundary. Before the baseline is advanced, rerunning the report still compares against the old release. After a successful upgrade, the new baseline becomes the reference for the next three-way reconciliation; it does not erase the project's Git history or local ownership.

## Migrate Open-Work Routing

When upgrading a project that has no `zettelkasten/work/active/` routes, preserve its canonical WORK files and local policy. After reconciling the new lifecycle and entry rules, explicitly inventory the stable records once and create one `*.ref.md` for each open record. Do this manually or preview `workflow_archive.py reindex --root <repo-root> --dry-run`, then apply `reindex` on the upgrade task branch. Review source metadata errors and coordinate with other writers first.

Run `workflow_doctor.py --root <repo-root> --full --strict` and review the Markdown routes before enabling ordinary scoped discovery. The full check covers omitted open routes as well as history. A normal status lookup must report missing routing instead of silently reading every old WORK. No upgrade or reindex operation archives, deletes or rewrites project evidence; archive selected terminal records separately after current knowledge is preserved. See the [knowledge lifecycle](../template/zettelkasten/knowledge-lifecycle.md).
