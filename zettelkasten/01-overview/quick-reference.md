# Quick Reference

This is the highest-frequency lookup note. Agents should check here before running commands, looking for domains, ports, credentials, or key endpoints.

## Common Commands

```bash
python3 scripts/validate_distribution.py
python3 skills/ai-collaboration-workflow/scripts/bootstrap_template.py \
  --source . \
  --target /tmp/ai-workflow-smoke \
  --dry-run
git diff --check
```

## Domains And Ports

| Environment | Domain / port |
|---|---|
| Source repository | `https://github.com/vector233/ai-collaboration-workflow-template` |
| Local runtime | None; repository is Markdown and Python tooling |

## API Endpoints

<!-- Example:

| Endpoint | Description |
|---|---|
| `GET /health` | Health check |
| `POST /api/v1/auth/login` | Login |
| `GET /api/v1/users/me` | Current user |
-->

## Database Tables

<!-- List important tables and one-line responsibilities. -->

## Cache / Queue Keys

<!-- Example:

| Pattern | Purpose |
|---|---|
| `user:{id}` | User cache |
| `ratelimit:{ip}:{bucket}` | Rate limit bucket |
-->

## Environment Variables / Config

<!-- List important config files and required environment variables. -->

## Test Accounts

<!-- Local-only test accounts. Never commit production credentials. -->

## Git Repositories

- `vector233/ai-collaboration-workflow-template`

## Community Publishing

- [[05-reference/community-publishing]] — platform-specific posting flow for Obsidian Forum, X, and future launch channels

## See Also

- [[01-overview/product-vision]] — product positioning and audience
- [[02-architecture/current-architecture-flow]] — current architecture flow
- [[00-governance/glossary]] — terminology
