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

## AD-002: Non-Trivial Implementation Requires Requirement And Technical Design State

**Decision**: except for documented tiny-fix waivers, business-code implementation must have a requirement and an approved technical design.

**Why**:

- AI agents can infer too much from local code and drift from product scope.
- Requirements define why, what, non-goals, and acceptance criteria.
- Technical designs define the target flow, boundaries, risks, and validation plan.

**Impact**:

- `in-progress` means a requirement is active, not necessarily implementation-ready.
- Technical designs in `pending/` are not implementation inputs.
- If implementation invalidates a design assumption, update the design before continuing.

**See also**: [[00-governance/ai-workflow]], [[06-requirements/README]], [[08-technical-designs/README]]

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

## AD-004: Separate The Downstream Payload From Repository Maintenance

**Decision**: files installed into user projects live under `template/`. The root knowledge base and workflow state directories describe this repository and are not distribution content.

**Why**:

- GitHub's template-repository feature copies every repository file and cannot exclude maintenance evidence.
- The Skill, manual installation, and validation need one identical payload.
- Repository-specific release notes, publishing runbooks, requirements, designs, and reviews should not appear in user projects.

**Impact**:

- The supported install surfaces are Skill bootstrap and copying the contents of `template/`.
- Bootstrap resolves `<source>/template/` when given a repository checkout.
- Distribution validation must prove state directories exist and maintenance content is absent.
- Root `zettelkasten/` can now be initialized and used to dogfood the workflow.

**See also**: [[02-architecture/current-architecture-flow]], [[05-reference/e2e-test]]

## See Also

- [[00-governance/project-overview]] — project overview
- [[00-governance/gotchas]] — bugs and lessons that may motivate decisions
