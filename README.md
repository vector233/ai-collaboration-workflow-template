# ai-knowledge-base-skeleton

A reusable scaffold for an **AI-agent-driven Zettelkasten knowledge base**, intended to live inside a project repo as `zettelkasten/`.

The scaffold encodes:

- A 9-directory layout (`00-governance` / `01-overview` / `02-architecture` / `03-roadmap` / `04-cross-cutting` / `05-reference` / `06-requirements` / `07-review` / `08-technical-designs`)
- Three state-machine workflows — **Requirements**, **Review**, **Technical Designs** — each with `pending → in-progress → done`-style transitions
- Wiki-link conventions for AI agents to navigate the knowledge graph
- Markdown templates for each workflow
- A `CLAUDE.md` that lays out the methodology in language tuned for Claude Code

> 中文说明：这是一份面向 AI agent 的知识库脚手架，详见 `zettelkasten/CLAUDE.md`。

## Use as a template

1. On GitHub, click **Use this template** to create your own project repo.
2. Clone the new repo locally.
3. In Claude Code (or any capable AI assistant), say:

   > **"请按 INIT.md 初始化此知识库"**
   >
   > or in English: **"Initialize this knowledge base by following INIT.md."**

4. Answer the questions the AI asks (project name, tech stack, repo type, etc.).
5. The AI will replace all `{{...}}` placeholders, prune branches you don't need, generate the first batch of notes, delete `INIT.md` itself, and create the first commit.

You're done — the resulting `zettelkasten/` is a customized knowledge base ready for daily use.

## What's inside

```
zettelkasten/
├── CLAUDE.md                # AI-facing methodology
├── {{PROJECT_NAME}}.md      # project index (renamed by INIT.md)
├── 00-governance/           # decisions, glossary, gotchas, templates
├── 01-overview/             # quick-reference, product-vision
├── 02-architecture/         # system architecture notes (start empty)
├── 03-roadmap/              # phases.md
├── 04-cross-cutting/        # umbrella-projects only — single-repo init removes this
├── 05-reference/            # external doc summaries (start empty)
├── 06-requirements/         # workflow: backlog → in-progress → done
├── 07-review/               # workflow: pending → in-review → done
└── 08-technical-designs/    # workflow: pending → approved → implemented
```

## Manual fallback

If you prefer not to use AI: open `INIT.md`, work through §1-§6 by hand (substitute placeholders, delete `04-cross-cutting/` if single-repo, generate first-batch notes yourself), delete `INIT.md` when finished.

## License

MIT — see `LICENSE`.
