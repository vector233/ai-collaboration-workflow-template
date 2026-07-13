# Template Feedback

## Detect

Run the target repository's Template Feedback Check silently at tracked or governed checkpoints, closeout, and after a user corrects workflow behavior. A normal task creates no feedback artifact.

Evidence-backed signals include repeated workflow workarounds, unnecessary artifacts or context, missing or contradictory knowledge routing, an optional helper becoming necessary, and promoted knowledge failing retrieval when its trigger recurs.

## Classify

- Project-specific facts, commands, or procedures go to the project's normal Experience Promotion destinations.
- Template-wide friction goes to `zettelkasten/00-governance/workflow-observations.md`, created on first use from the repository template.
- Vendor-specific behavior uses scope `vendor-specific` and must not change vendor-neutral rules without broader evidence.
- One-off model mistakes, preferences, and unsupported opinions are not recorded.

## Prepare

When the user asks for upstream feedback:

1. read local observations and group duplicates;
2. verify each claim against repository evidence or a reproducible flow;
3. remove private code, secrets, customer data, internal URLs, names, and identifying business details;
4. include the template baseline or release, agent/model when relevant, expected and observed behavior, impact, recurrence, and suggested change;
5. label uncertain inference explicitly;
6. present the sanitized report for user review.

## Publish

Do not scan unrelated projects, send telemetry, contact an upstream service, or create an Issue or PR without explicit user approval. After approval, use the upstream repository's workflow-feedback Issue template when available. Preserve the local observation's reported link or status only after publication succeeds.
