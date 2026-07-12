# Community Publishing Runbook

Last validated: 2026-07-12.

Use this runbook when announcing the project on public community platforms. The goal is to make each post repeatable: prepare the same facts, respect platform rules, draft in a safe state, and only publish after an explicit final review.

## Pre-Publish Checklist

Before posting anywhere:

- Confirm the repository is public and the latest intended commit is pushed.
- Re-read the README first line, repository description, and topics so the external copy matches the current project positioning.
- Run a quick private/source-project information scan before broad promotion.
- Prepare one canonical short description and one platform-specific draft.
- Keep the project positioning precise: this is a vendor-neutral project knowledge layer and adaptive workflow template; its Markdown vault remains Obsidian-compatible, but it is not an Obsidian plugin.
- If an AI assistant controls a browser, have it fill drafts only. The human owner should confirm or perform the final publish action.

Canonical short description:

```text
AI Collaboration Workflow Template is a vendor-neutral project knowledge layer and adaptive workflow template for AI-assisted software development.
```

## Obsidian Forum: Share And Showcase

Use this flow for the Obsidian Forum `Share & showcase` category.

### Fit Check

This category accepts Obsidian plugins, themes, CSS snippets, tips, and custom vaults/workflow showcases. It rejects third-party apps that merely interact with Obsidian through Markdown files.

Position this project as:

```text
a custom vault / workflow showcase
```

Do not position it as:

```text
an Obsidian plugin
a third-party app for Obsidian
```

### Posting Steps

1. Open the `Share & showcase` category.
2. Sign in manually if needed. Do not have an agent enter passwords, passkeys, or one-time codes.
3. Click `New Topic`.
4. Re-read the category composer rules. Platform rules can change.
5. Delete the default rules text only after preserving the required disclaimer.
6. Fill the required disclaimer at the top.
7. Use a title that makes the vault/workflow nature clear.
8. Write the body as an Obsidian vault/workflow showcase and ask for Obsidian-user feedback.
9. Preview for broken links or accidental plugin claims.
10. Publish only after final human confirmation.

### Recommended Title

```text
AI Collaboration Workflow Template: project knowledge layer for coding agents
```

### Required Disclaimer

```text
Disclaimer
Is this project open source? Yes
Is this project completely free? Yes
Is this project vibe-coded beyond the author's ability to comprehend how it works? No
Community Directory: N/A - this is a custom vault / workflow showcase, not a plugin or theme.
```

### Body Template

````text
Hi everyone,

I open-sourced a vendor-neutral project knowledge layer and adaptive workflow template for AI-assisted software development. Its linked Markdown knowledge base can also be opened as an Obsidian-compatible vault.

The goal is to help AI coding agents and human maintainers keep project context over time without rediscovering everything from scratch.

Instead of one large project document or a mandatory document chain, the template uses small linked notes for:

- stable work items
- technical designs, implementation plans, and review handoffs only when independently required
- architecture notes
- validation runbooks
- gotchas / lessons learned
- on-demand project Skills promoted from verified experience

The basic workflow is:

```text
Task
  -> Route     Direct, Tracked, or Governed
  -> [WORK]    keep stable task state when tracking is useful
  -> Build     implement, validate, and commit one bounded context
  -> [Gates]   add TECH, PLAN, or REVIEW only when triggered
  -> Doctor    check workflow state, links, branches, and project Skills
  -> Promote   write recurring lessons to rules, notes, runbooks, or project Skills
```

It uses Obsidian-style wiki links like `[[00-governance/ai-workflow]]` for note-to-note navigation, while keeping standard Markdown links and images for GitHub compatibility.

This is not an Obsidian plugin. It is a reusable Markdown vault/workflow template that can be opened in Obsidian, edited in any Markdown editor, and kept in a normal Git repository.

There is also an optional companion skill for Claude/Codex-style agents, but the core project is just Markdown files and folders.

GitHub:
https://github.com/vector233/ai-collaboration-workflow-template

I would appreciate feedback from Obsidian users, especially on whether the folder structure and wiki-link approach feels natural for a project knowledge base.
````

### Obsidian Forum Gotchas

- Keep future updates for the same project in the same thread unless forum rules say otherwise.
- Do not add a Community Directory link unless the project is actually an approved plugin or theme.
- The forum may block or review posts from new accounts. Treat that as a platform moderation state, not a project failure.

## X

Use this flow for a short public announcement on X.

### Drafting Rules

- Keep the post visibly short and verify X's own character counter before publishing.
- Prefer a direct `intent/post` or `intent/tweet` URL for a clean composer state.
- Do not keep editing a corrupted rich-text composer. If the counter or text state looks wrong, close it and start from a fresh intent URL.
- Wait for the GitHub link preview to load if you want the repository card included.
- Publish only after final human confirmation.

### Recommended Text

```text
Open-sourced AI Collaboration Workflow Template: a vendor-neutral project knowledge layer and adaptive workflow for AI coding agents.

It keeps stable work items, validation, project knowledge, and on-demand skills linked over time.

https://github.com/vector233/ai-collaboration-workflow-template
```

### Clean Intent URL Flow

1. URL-encode the recommended text.
2. Open a fresh tab with:

   ```text
   https://x.com/intent/post?text=<URL_ENCODED_TEXT>
   ```

   `https://twitter.com/intent/tweet?text=<URL_ENCODED_TEXT>` may also redirect to the same X composer.

3. Confirm the visible text is correct.
4. Confirm the X counter allows posting.
5. Confirm the GitHub preview card appears or deliberately ignore it.
6. Publish only after final human confirmation.

### X Gotchas

- Direct UI automation can confuse X's rich-text composer and leave a stale character counter.
- Setting the content through accessibility APIs may show text visually but not update the internal composer state.
- Manual typing can drop line breaks or characters in the rich-text composer.
- A fresh intent URL is the most reliable recovery path.

## Post-Publish Record

After publishing, record the public URL and date in a project-specific release note, changelog, or marketing tracker. Use this format:

```text
Date: YYYY-MM-DD
Platform:
URL:
Post type:
Purpose:
Follow-up needed:
```

## See Also

- [Project README](../README.md) - project positioning, installation, and usage
- [Chinese guide](zh-CN/README.md) - Chinese-language overview
