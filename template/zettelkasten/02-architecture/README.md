# 02-architecture

Store architecture notes here: system flows, authentication model, component interactions, data model, integrations, and operational boundaries.

## Suggested Initial Notes

Create these as needed:

- `current-architecture-flow.md` — current system flow and source of truth for architecture facts
- `request-flow.md` — end-to-end request path
- `auth-model.md` — authentication and authorization model
- `data-model.md` — core data model
- `deployment-flow.md` — deploy and runtime topology

## Rules

- Each note should describe one clear architecture topic.
- Important external dependencies should have a related entry in [[00-governance/decisions]].
- Architecture changes should be written back to this directory after implementation.
- If a note describes planned behavior, label it as planned. Do not present assumptions as current facts.

## See Also

- [[00-governance/decisions]] — architecture decision records
- [[00-governance/ai-workflow]] — rule promotion and memory writeback rules
- [[AI]] — knowledge base entry point
