# Architectural Decisions

Append durable decisions. Supersede historical decisions with a new entry instead of deleting them.

## AD-001: Use Linked, On-Demand Project Knowledge

**Decision**: keep durable project facts as linked notes and load only the active work item plus matched context.

**Why**: broad context loading wastes tokens and increases stale-assumption risk.

**Impact**: [[AI]] is the navigation entry; work items link the smallest context pack; `project-skills/INDEX.md` routes procedural memory.

## AD-002: Keep Work Paths Stable

**Decision**: every tracked or governed task has at most one workflow-specific `WORK-*` record under [[work/README]]. Status is frontmatter, not a directory move.

**Why**: moving files forces link updates, creates merge churn, and duplicates board state.

**Impact**: governed decisions and approvals remain in the WORK record. Durable facts go to knowledge notes; project-native Issues, pull requests, and release systems keep their own lifecycle.

## AD-003: Route Process By Risk Dimensions

**Decision**: choose Direct, Tracked, or Governed routes using scope, uncertainty, risk, reversibility, duration, coordination, and verification.

**Why**: diff size alone misclassifies small high-risk changes and large low-risk changes.

**Impact**: hard-risk triggers escalate to Governed; users may override with a recorded reason.

## AD-004: Promote Procedures Into Project Skills

**Decision**: stable repeatable procedures may become project Skills; rules, facts, gotchas, and simple commands remain in their smaller durable forms.

**Why**: project Skills provide progressive disclosure without turning every lesson into always-loaded instructions.

**Impact**: follow [[skill-lifecycle]] and update `project-skills/INDEX.md`.

## AD-005: Isolate Parallel Work With Worktrees

**Decision**: tracked work uses task branches and concurrently active tasks use separate Git worktrees.

**Why**: branch-only context switching does not isolate simultaneous agents or dirty working trees.

**Impact**: every context commits task-scoped changes; shared knowledge is promoted near integration to reduce conflicts. See [[git-collaboration]].
