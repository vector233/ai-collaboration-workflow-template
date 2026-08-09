# ExampleSaaS Walkthrough

This fictional walkthrough shows a Governed feature using one stable work record and an on-demand project Skill.

The invitation-link feature has one coupled acceptance and rollback boundary, so it intentionally remains one WORK. If the roadmap later separates token infrastructure, admin migration, SDK compatibility, and production cutover into independently releasable outcomes, use the external roadmap Epic or one optional local Initiative with separate child WORK records instead of expanding this file indefinitely.

## Task

Add expiring team invitation links across API, database, email, and browser flows.

Routing finds elevated scope, data migration, security-sensitive tokens, multiple slices, and realistic verification. The selected route is Governed.

## Stable Work Record

```text
zettelkasten/work/
  WORK-20260601103000-team-invitation-links.md
```

The file never moves. Status changes in frontmatter.

The WORK owns:

- user goal, non-goals, and acceptance criteria;
- route decision plus migration, security, rollback, release, and independent-approval gates;
- context pack and affected paths;
- task branch and dedicated worktree;
- current slice, validation, context commit, and next action;
- experience candidates and final promotion decisions.

The WORK links durable architecture decisions for token hashing, expiry, compatibility, migration, and rollback. Its slices coordinate backend, email, UI, browser verification, and integration ordering. Independent security and migration approvals close named gates with their evidence or project-native review links.

## Git Isolation

```bash
git worktree add ../team-invitation-links \
  -b task/WORK-20260601103000-team-invitation-links <base>
```

Each implementation context updates the WORK checkpoint after a bounded slice or before a handoff, long pause, session switch, or detectable context compaction, then commits its task-scoped changes. Broken checkpoints remain on the task branch.

## Experience Promotion

During browser validation, the team discovers that invite-link tests require clearing a provider sandbox cache before resending email. The task records the candidate first.

If the sequence is verified, recurring, conditional, and needs validation and recovery, it becomes:

```text
project-skills/reset-invite-sandbox/SKILL.md
```

Before writing, the task searches rules, runbooks, Skills, and the index. It claims the selected shared paths in `owned_paths`, updates an existing canonical procedure when present, and otherwise creates one Skill and one index row. Repeating promotion records a no-op rather than another copy.

`project-skills/INDEX.md` receives a trigger such as "invite email sandbox returns stale token or resend tests reuse previous state." A simple invariant such as "store only invitation token hashes" belongs in architecture or security rules instead of another Skill.

## Resume

A fresh agent reads `AGENTS.md` and `zettelkasten/AI.md`, inspects the current branch, opens the matching WORK, and then reads only its linked security note, architecture decision, validation runbook, and matching project Skill. Before editing, it reports the route, acceptance state, checkpoint commit, validation, unresolved risk, and next allowed action. No companion helper is required.
