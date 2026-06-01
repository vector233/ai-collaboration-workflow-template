<!-- UMBRELLA-ONLY: keep this directory only if {{REPO_TYPE}} == umbrella -->

# 04-cross-cutting

Use this directory only for umbrella repositories or systems with multiple subprojects.

Store cross-module concerns here: shared authentication, routing, consistency rules, privacy model, shared release process, common schemas, or platform-wide policies.

If this is a single-project repository, `INIT.md` removes this directory.

## Typical Notes

- `shared-auth.md` — authentication across subprojects
- `routing.md` — shared routing or tenancy boundaries
- `privacy-model.md` — cross-system privacy and data retention rules
- `release-coordination.md` — release ordering across subprojects

## See Also

- [[CLAUDE]] — knowledge base entry point
- [[02-architecture/current-architecture-flow]] — current architecture flow

<!-- /UMBRELLA-ONLY -->
