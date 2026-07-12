# ExampleSaaS Walkthrough

This fictional walkthrough shows a Governed feature using stable work artifacts and an on-demand project Skill.

## Task

Add expiring team invitation links across API, database, email, and browser flows.

Routing finds elevated scope, data migration, security-sensitive tokens, multiple slices, and realistic verification. The selected route is Governed.

## Stable Artifacts

```text
zettelkasten/06-work/
  WORK-20260601103000-team-invitation-links.md
  TECH-20260601104500-team-invitation-links.md
  PLAN-20260601110000-team-invitation-links.md
  REVIEW-20260601123000-team-invitation-links.md
```

The files never move. Status changes in frontmatter.

The WORK owns:

- user goal, non-goals, and acceptance criteria;
- route decision and reasons for separate TECH, PLAN, and REVIEW;
- context pack and affected paths;
- task branch and dedicated worktree;
- current slice, validation, context commit, and next action;
- experience candidates and final promotion decisions.

The TECH owns token hashing, expiry, compatibility, migration, and rollback decisions. The PLAN owns backend, email, UI, browser verification, and integration ordering. The REVIEW exists separately because security and migration behavior need independent approval.

## Git Isolation

```bash
python3 scripts/task_worktree.py create \
  WORK-20260601103000-team-invitation-links \
  --slug team-invitation-links
```

Each implementation context updates the WORK checkpoint and commits its task-scoped changes. Broken checkpoints remain on the task branch.

## Experience Promotion

During browser validation, the team discovers that invite-link tests require clearing a provider sandbox cache before resending email. The task records the candidate first.

If the sequence is verified, recurring, conditional, and needs validation and recovery, it becomes:

```text
project-skills/reset-invite-sandbox/SKILL.md
```

`project-skills/INDEX.md` receives a trigger such as "invite email sandbox returns stale token or resend tests reuse previous state." A simple invariant such as "store only invitation token hashes" belongs in architecture or security rules instead of another Skill.

## Resume

A fresh agent reads `AGENTS.md`, `zettelkasten/AI.md`, runs `workflow_doctor.py --status`, opens the branch-matched WORK, and then reads only the linked TECH, PLAN, REVIEW, security note, validation runbook, and matching project Skill.
