# Knowledge Lifecycle

Read the target's `zettelkasten/knowledge-lifecycle.md` as authoritative. Keep current knowledge and concise task navigation available, and exclude historical bodies from routine discovery and searches. Core operation uses Markdown and Git alone.

## Ordinary Work

Read the current branch and small `zettelkasten/work/active/*.ref.md` hints, then only the selected canonical WORK. A route contains no duplicated status or checkpoint. Create/update each route in the same change as its source, remove it on closure, and declare both paths in `owned_paths`. Parallel tasks write different route files.

Use the optional Doctor's ordinary `--status` or validation for open work and exact dependency/parent paths. It does not enumerate closed records or descend into archive storage. A referenced archived dependency can be checked from its stable summary; stop at terminal records rather than expanding older prerequisite chains. Initiative rollups in this mode omit unreferenced historical children; use a full audit for final membership and closure.

Missing routes or `Routing status: pending` in the routing README are a repair signal. A directory copied during upgrade is not evidence of completed migration. Do not silently fall back to a full history scan. A known assigned WORK path remains usable directly; repair the matching route. For old installations or a broader routing repair, explicitly preview a full rebuild:

```bash
python3 "$SKILL_ROOT/scripts/workflow_archive.py" reindex --root <repo-root> --dry-run
python3 "$SKILL_ROOT/scripts/workflow_archive.py" reindex --root <repo-root>
python3 "$SKILL_ROOT/scripts/workflow_doctor.py" --root <repo-root> --full --strict
```

Reindex reads every stable record, keeps only routes for `backlog`, `active`, `blocked`, and `review`, and never archives or edits the source bodies. Coordinate this maintenance serially with writers. Manually creating the same small Markdown routes is equivalent.

## Archive And Restore

After closure and evidence-backed promotion, archive substantial historical bodies when their stable summary and current knowledge are sufficient. A short closed record already leaves ordinary discovery and does not need an extra file. Never retire current constraints based on age, or archive open work, pending experience decisions, unresolved gates, or an Initiative with open children.

Preview and then apply on the task branch:

```bash
python3 "$SKILL_ROOT/scripts/workflow_archive.py" archive <WORK-ID> \
  --summary "<outcome and location of current knowledge>" \
  --reason "<why the body is historical>" --root <repo-root> --dry-run
python3 "$SKILL_ROOT/scripts/workflow_archive.py" archive <WORK-ID> \
  --summary "<outcome and location of current knowledge>" \
  --reason "<why the body is historical>" --root <repo-root>
```

The target can also be an Initiative ID or a repository-relative retired Markdown note. Required workflow/navigation files cannot be archived. Notes must be marked `superseded`, `deprecated`, or `retired` after useful facts and live navigation are updated; identify the replacement or explain why none is needed in the summary.

The helper preserves original bytes in a content-addressed snapshot, leaves identity/status/relationships at the stable source, and adds a summary, reason, date, reference and checksum. Existing heading anchors remain landing points. Repeated archival is a no-op. Review and commit the source, snapshot, route removal and relevant current-knowledge updates together.

For evidence retrieval, read the exact `archive_ref` without restoring or searching all history. Resolve its unchanged relative Markdown references against the stable source directory. To restore a body:

```bash
python3 "$SKILL_ROOT/scripts/workflow_archive.py" restore <WORK-ID> --root <repo-root> --dry-run
python3 "$SKILL_ROOT/scripts/workflow_archive.py" restore <WORK-ID> --root <repo-root>
```

Restore verifies the checksum and preserves the snapshot and original terminal/retired state. Restore before reopening a WORK; update its state, branch, checkpoint and route deliberately. The helper does not publish, commit, delete old snapshots, rewrite Git history, or move multi-file project Skills. Retire a complete Skill directory manually following the target lifecycle, repairing live references and removing its active-index row.

## Validation

Ordinary checks verify current work and encountered archive references without reading snapshot bodies. Run `workflow_doctor.py --full --strict` to audit route completeness, all child memberships, checksums and historical links after migration or archival, and before integrating lifecycle changes. Keep the reported scope explicit.

Test I/O boundaries as well as returned results: reading every closed record and filtering afterwards does not satisfy scoped discovery. A real fresh-agent probe separately checks that entry instructions lead to the selected task and current knowledge without loading historical distractions. Synthetic or instrumented fixtures test the helpers, not fresh-agent behavior.
