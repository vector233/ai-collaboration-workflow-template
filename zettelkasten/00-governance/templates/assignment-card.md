# Assignment Card Template

Use this card when handing work to another AI session or splitting parallel work.

```md
## Assignment

- Role:
- Requirement:
- Technical design:
- Review doc:
- Gate status: ready / blocked / partial / review-only
- Gate note:
- Goal:
- Owned paths:
  - 
- Read-only paths:
  - 
- Out of scope:
  - 
- Decisions allowed:
  - 
- Must escalate:
  - 
- Required validation:
  - 
- Expected handoff:
  - 
- Branch / commit scope:
  - 
```

## Gate Status

- `ready`: gate is satisfied; implementation is allowed within owned paths.
- `blocked`: gate is not satisfied; only exploration, design, validation prep, or review is allowed.
- `partial`: only explicitly listed sub-scope is allowed.
- `review-only`: read, verify, and write review feedback; do not edit implementation files.

## Checklist

- Owned paths do not overlap with another active role.
- Read-only paths are enough for context but not editable.
- Required validation is concrete and runnable.
- Handoff location is explicit.
- Escalation boundaries include API/schema/auth/security/billing/data-retention/deployment/public-contract changes when relevant.
