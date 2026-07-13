# Workflow Feedback

Use this path to turn downstream evidence into reviewable improvements without adding telemetry or project-data leakage.

## Downstream Collection

The downstream Template Feedback Check creates `zettelkasten/00-governance/workflow-observations.md` only after evidence-backed friction. Normal tasks and one-off model mistakes produce no entry.

Useful evidence includes:

- a repeated workflow workaround or user correction;
- unnecessary artifacts or context caused by template guidance;
- missing, stale, duplicated, or contradictory knowledge routing;
- an optional helper becoming necessary for the core path;
- promoted knowledge failing retrieval when its trigger recurs.

## Report Preparation

Before submitting upstream:

1. reproduce or otherwise verify the observation;
2. merge duplicates and state recurrence accurately;
3. remove private code, customer data, secrets, internal URLs, project names, and identifying business details;
4. include template baseline or release, relevant agent/model, expected behavior, observed behavior, impact, and suggested change;
5. separate template-wide behavior from vendor-specific behavior and project-local lessons;
6. have the user review the exact report.

## Submission

Use the repository's **Workflow feedback** Issue form after explicit user approval. A local observation is not permission to transmit data. Link the created Issue or PR back to the local observation only after publication succeeds.

Maintainers should treat reports as hypotheses, reproduce them when possible, and promote only changes that preserve the knowledge-first, process-light, tools-optional boundary.
