# Architectural Decisions

Each architecture decision record answers: **what decision was made, why, and what it affects**.

Append new decisions to this file. Do not delete historical decisions. If a decision is replaced, add a new entry such as `AD-004: Replace AD-002 with ...`.

## AD-001: Use A Linked Knowledge Base Instead Of A Linear Docs Folder

**Decision**: project knowledge is organized as atomic notes connected by wiki links.

**Why**:

- AI agents need fast retrieval of related context.
- Architecture decisions often affect multiple modules, which a simple directory tree does not express well.
- New notes must connect to existing notes, reducing orphaned documentation.

**Impact**:

- Notes should be small and focused.
- New notes must link to at least one existing note.
- The navigation entry point is [[AI]].

## AD-002: Select Standalone Design And Planning By Risk

**Decision**: tracked work uses a REQ as its primary record. Standalone TECH and PLAN artifacts are selected by risk and complexity rather than required universally.

**Why**:

- AI agents can infer too much from local code and drift from product scope.
- Every change needs technical reasoning and execution decomposition.
- Forcing separate documents for a bounded low-risk bug adds duplication without improving safety.
- Complex changes still need durable design and planning artifacts for review and resumption.

**Impact**:

- A bounded bug may use `REQ -> implement and validate -> REVIEW -> writeback` when the REQ contains inline technical readiness and sufficient implementation slices.
- A standalone TECH is required for meaningful architectural, contract, data, security, deployment, third-party, cross-module, or unresolved technical decisions.
- A standalone PLAN is required when dependencies, sequencing, ownership, multi-session work, or per-slice checkpoints need durable coordination.
- Implementation starts only when the REQ's selected TECH/PLAN path is ready.

**See also**: [[00-governance/ai-workflow]], [[06-requirements/README]], [[08-technical-designs/README]], [[09-implementation-plans/README]]

## AD-003: Review Feedback Must Be Evidence-Backed

**Decision**: important AI or human review feedback must include evidence, and the implementation owner must independently verify it.

**Why**:

- AI reviewers can sound certain while being wrong.
- Evidence-free review creates churn.
- Counter-evidence prevents future agents from re-processing rejected claims.

**Impact**:

- Review documents record feedback, evidence, judgment, handling status, and closure conditions.
- Confirmed issues require validation after the fix.
- Rejected findings require counter-evidence.

**See also**: [[07-review/README]], [[00-governance/ai-workflow]]

## See Also

- [[00-governance/project-overview]] — project overview
- [[00-governance/gotchas]] — bugs and lessons that may motivate decisions
