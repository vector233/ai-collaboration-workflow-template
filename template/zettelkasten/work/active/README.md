# Open Work Routes

Routing status: pending

Set the literal line above to `Routing status: ready` only after initialization or an explicit inventory has created every open route. A newly copied directory does not prove an existing project has been migrated. The optional `reindex` helper preserves this README and updates that line after building the routes.

Each `*.ref.md` points to one open WORK or Initiative. The directory contains only navigation, never duplicated status, validation, checkpoints or child rollups. See [[knowledge-lifecycle]].

For `work/WORK-YYYYMMDDHHMMSS-short-name.md`, create `work/active/WORK-YYYYMMDDHHMMSS-short-name.ref.md`:

```markdown
# WORK-YYYYMMDDHHMMSS-short-name

Branch hint: `task/work-id-short-name`

Source: [[work/WORK-YYYYMMDDHHMMSS-short-name]]

Routing only; read the source for authoritative state.
```

Use the actual ID and branch. An Initiative uses its own ID and `coordination` as its branch hint. Add/update this route with its source and remove it when the source becomes `done` or `cancelled`. Reopening recreates it. A blocked or backlog task remains discoverable. Each task owns its own route file.

Select the matching route, then read that source. Do not enumerate or search closed WORK bodies to find open work. Missing or stale routing requires a targeted repair or an explicit full rebuild.
