# Knowledge Lifecycle

Keep current knowledge small enough to navigate. Preserve history without making historical bodies part of routine discovery, search, or context loading.

## Reading Boundaries

| Layer | Content | Default access |
|---|---|---|
| Entry | `AGENTS.md`, [[AI]], open-work routing, project Skill index | read the concise navigation needed for this task |
| Current knowledge | selected WORK, applicable constraints, verified notes and procedures | read or search only task-relevant paths |
| History | closed WORK bodies, retired notes, replaced procedures and old evidence | exclude from ordinary search; retrieve exact evidence only for a historical question or explicit full audit |

Start from the current branch and [[work/active/README]]. Each small `*.ref.md` points to a stable WORK or Initiative; its branch is a hint. Read the selected source for authoritative state. Do not scan every stable work file to discover the current task. Read a linked Initiative only for a relevant shared constraint; do not load its siblings. An exact `depends_on` reference may require reading a closed WORK's compact summary to confirm completion. Stop at that terminal record; its older prerequisites and parent history belong to an explicit full audit.

Ordinary content searches must name the relevant current paths. Exclude `zettelkasten/archive/`, unselected `zettelkasten/work/` records, and unmatched project Skills. A repository-wide recursive search or a search followed by status filtering still reads history and does not satisfy this rule. A `.gitignore` entry is not a portable reading policy; keep historical evidence tracked in Git.

Missing or contradictory routing must be reported. Use a known assigned WORK path when available, then repair its route. A full index rebuild is an explicit maintenance operation; never silently fall back to scanning every historical record. The optional helper can preview and rebuild routes. All routes can also be maintained with Markdown and Git alone.

## Open Work Routes

Use one `work/active/<ID>.ref.md` per `backlog`, `active`, `blocked`, or `review` WORK or Initiative. Retain blocked and backlog work until it is explicitly completed or cancelled; age alone does not retire it. Use the format in [[work/active/README]]. There is no central table containing a second copy of task status.

Create or update a route with its source, remove it on `done` or `cancelled`, and commit both together. Declare the source and its route in the same task's `owned_paths`. Separate tasks own separate route files. A full rebuild requires serial coordination with writers. On reopening a task, restore its body first when archived, update its canonical status, branch and checkpoint, and recreate its route in the same change.

The default status helper reports open work and exact dependency/parent records. Its Initiative rollup is scoped; it must not claim a complete historical child count. Final Initiative acceptance and closure require an explicit full membership check against canonical child frontmatter.

## Close, Then Archive

Archival is a knowledge-retention step following delivery closure. Keep the existing `done` or `cancelled` status; do not introduce an `archived` delivery status or move the canonical WORK path.

At task closeout:

1. Decide every experience candidate and update the smallest existing current rule, note, runbook, decision or Skill. Leave an explicit no-op or non-promotion reason when appropriate.
2. Resolve acceptance, integration and required gates. For cancellation, record the reason, disposition of partial changes, and explicit gate resolutions or waivers; do not present cancellation as accepted delivery.
3. Set the terminal status and remove the open route. A terminal record is already excluded from routine task discovery.
4. Archive substantial historical bodies once current knowledge and the remaining summary are sufficient. For a short terminal record, retaining it at its stable path is sufficient; do not manufacture an empty history file. Do not archive active constraints, unresolved candidates, pending gates, or an Initiative with open children.
5. Verify the summary, evidence retrieval, links and absence from ordinary discovery; commit the complete lifecycle change on the task branch.

The optional archive helper requires a concise outcome summary and a reason. It stores the original bytes under `archive/<original-vault-path-without-extension>/<sha256>.md`, then replaces the source body with a compact summary and historical link. It retains original headings as section-link landing points. Original task identity, state, parent and dependencies stay in source frontmatter. The snapshot is historical evidence and never a second canonical WORK. Its bytes retain the original link text: interpret relative Markdown references against the stable source directory, not the snapshot storage directory. Wiki links remain relative to the vault.

Archive metadata at the stable path:

| Field | Meaning |
|---|---|
| `archive_ref` | repository-relative path under `zettelkasten/archive/` |
| `archive_sha256` | SHA-256 of the original file bytes |
| `archived_at` | ISO archival date; separate from verification of current facts |
| `archive_summary` | concise result and the location of still-applicable knowledge |
| `archive_reason` | why the body is no longer needed during ordinary work |

Repeated archival is a no-op. Restore only after checking the stored bytes against their checksum; restore preserves the original terminal or retired state. Reopening is a separate deliberate update. Restoring and archiving changed content creates a different snapshot; old evidence is retained. Do not automatically delete history by age or rewrite Git history.

The same contract can be performed manually: preserve the original bytes, calculate their checksum with a standard Git/OS tool, keep the stable source metadata and headings, add the summary and reference, and update the route. Review all files together; the Companion Skill scripts are optional conveniences.

## Retire Knowledge And Procedures

Archive based on applicability, not age. Old but binding decisions remain current. Verification that is overdue means recheck the fact or procedure, not automatically archive it.

For a replaced or retired knowledge note, first promote useful facts into its current replacement, update live navigation, and mark the old note `superseded`, `deprecated`, or `retired`. Archive its body using the same stable-summary contract. The summary must name the replacement or explain why none is needed. Keep required navigation and workflow policy files current rather than archiving them. The absence of an active inbound link alone is not evidence that a constraint can be retired.

For a retired project Skill, identify its replacement, update live callers and remove its row from `project-skills/INDEX.md`. Preserve the complete retired Skill directory, including references and scripts, under `zettelkasten/archive/project-skills/<unique-retirement-id>/`. This directory move is manual, reviewable, and must repair affected links; the file archive helper does not move multi-file Skills. Keep portable `SKILL.md` metadata unchanged. The archived directory is not a discoverable active Skill. Restore the complete directory and reverify it before routing it again.

Keep entry points brief. Update canonical knowledge in place, split genuinely distinct topics behind links, and replace obsolete explanations. Do not append every task's story to `AGENTS.md`, [[AI]], architecture, gotchas or the Skill index. Preserve concise rationale for binding decisions even when detailed deliberations are archived.

## Checks And Migration

Routine checks inspect current knowledge, open work, and exact dependencies. They check an encountered archive reference exists without loading its body. They do not claim to validate all historical evidence or detect every omitted route. Use an explicit full audit for complete route coverage, all child memberships, historical wiki links and archive checksums, including before completing an archive migration or integrating workflow changes.

Old installations need a one-time route migration: inspect the full stable work set, create routes only for open records, report invalid metadata, preview the diff, and commit the routes with the updated entry rules. A freshly installed routing README starts with `Routing status: pending`; mark it `ready` only after the inventory or initialization establishes complete open routes. This prevents an empty directory added by an upgrade from hiding existing work. Do not automatically archive or delete old records during installation or upgrade. Preserve local customization through the normal three-way upgrade workflow. Keep the minimal-reading claim conditional on completing this migration.

See [[work/README]], [[skill-lifecycle]] and [[validation-policy]] for the delivery and validation contracts.
