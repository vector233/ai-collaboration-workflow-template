# 04-cross-cutting

This repository has two distributed surfaces: the template payload and the companion Skill.

Cross-cutting rules:

- Workflow semantics must remain aligned between `template/` and the Skill.
- The root maintenance knowledge base is not downstream payload content.
- Distribution validation must exercise the same payload consumed by users.
- Documentation must not advertise an installation path that bypasses `INIT.md`.

## See Also

- [[AI]] — knowledge base entry point
- [[02-architecture/current-architecture-flow]] — current architecture flow
