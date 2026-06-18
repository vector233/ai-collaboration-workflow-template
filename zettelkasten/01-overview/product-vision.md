# Product Vision

## Current Positioning

A reusable documentation workflow and companion Skill for long-running software projects built with AI coding agents

The first version focuses on durable project memory and explicit engineering gates without introducing a heavyweight project-management system. It is a repository-native Markdown workflow, not an issue tracker, hosted service, autonomous multi-agent framework, or Obsidian plugin.

## Core Problem

AI coding sessions are effective locally but lose decisions, validation evidence, and architectural context over time. Chat transcripts are poor project memory, while generic documentation folders rarely tell an agent what to read, when implementation is allowed, or what must be written back.

## Target Users

| User type | Core need | Typical situation |
|---|---|---|
| Solo developer using AI agents | Preserve decisions and avoid rediscovery | Repeatedly resumes work across short coding sessions |
| Small engineering team | Make AI-generated changes reviewable | Humans and agents hand work between sessions |
| Multi-module repository maintainer | Route agents to bounded context | Changes cross repositories or subprojects |

## Target Market

Global software projects that keep source and documentation in Git. The initial focus is individual developers and small teams maintaining projects longer than a demo lifecycle.

## Core Experience

```text
Install Skill or copy payload
  -> initialize project knowledge
  -> create REQ and approved TECH
  -> implement and validate one slice
  -> create REVIEW
  -> write durable facts back
```

## Pricing / Packaging

| Plan | Price | Includes | Best for |
|---|---|---|---|
| Open source | Free | Template payload, Skill, examples, and validation scripts | All users |

## Competitive Positioning

- Plain `AGENTS.md` is simpler for small repositories but does not preserve task history or linked project memory.
- Issue trackers are stronger for team planning but do not automatically provide repository-local AI context.
- Large architecture or PRD documents centralize facts but become expensive for agents to retrieve and update.
- This project combines small linked notes with explicit implementation and review gates.

## Technical Advantages

- One canonical payload shared by manual installation and Skill bootstrap.
- Repository-local context routing through linked atomic notes.
- Explicit requirement and approved-design gate.
- Evidence-based review handling and realistic validation records.
- Durable memory writeback after each implementation slice.

## See Also

- [[00-governance/project-overview]] — project overview
- [[01-overview/quick-reference]] — commands, domains, endpoints
