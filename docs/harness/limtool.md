---
title: limtool reference
summary: Reference of all limtool subcommands — the deterministic Python toolbox for docs, ADRs, ESDM and EventSourcingDB.
tags: [harness, tools, python, uv, limtool]
status: accepted
updated: 2026-10-28
---

# limtool reference

uv project in `tools/`. Invoke from anywhere in the repo:

```sh
uv run --project tools limtool <command>
```

| Command | Effect | Exit ≠ 0 when |
|---|---|---|
| `check` | harness check + docs lint + index freshness | any gate fails |
| `docs index [--check]` | regenerate `docs/INDEX.md` | `--check` and index stale |
| `docs lint` | frontmatter, status, sources, kebab-case, size, relative links | errors |
| `docs search <terms…> [--tag t] [--limit n]` | ranked search (title ×5, summary/tags ×3, body ×1), all terms must match | no hits |
| `adr new "<title>"` | create next numbered ADR from template | — |
| `esdm <args…>` | run pinned ESDM CLI inside `model/` (downloads + verifies SHA256 to `.tools/bin/`) | esdm fails |
| `esdm install` | only download/verify the binary | checksum mismatch |
| `esdb up [--dev]` / `down` / `logs` | docker compose in `infra/eventsourcingdb/` | compose fails |
| `esdb ping` | ping + verify API token using `infra/eventsourcingdb/.env` | unreachable/invalid |
| `deps outdated` | compare exact upstream pins with latest releases (crates.io, Docker Hub, esdm.io) | any pin outdated |
| `breakout <dir> --name <n> [--tool t]` | generate a LIMS-free harness for a new project from `tools/breakout/manifest.yaml` + templates; lists leaks | leaks remain |
| `harness check` | CLAUDE.md import, skills symlink, SKILL.md frontmatter | wiring broken |

## Development

```sh
cd tools
uv run pytest
uv run ruff check src tests && uv run ruff format --check src tests
```

Dependencies are kept minimal (`pyyaml`). Python ≥ 3.13.
