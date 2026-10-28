---
name: eventsourcingdb
description: Start, stop, check and inspect the local EventSourcingDB used by the LIMS. Use when you need a running event store for development, tests, or to inspect events/subjects.
---

# EventSourcingDB (local)

Setup lives in `infra/eventsourcingdb/` (see its README). Knowledge: `docs/knowledge/eventsourcingdb/`.

| Task                          | Command                                              |
|-------------------------------|------------------------------------------------------|
| Start persistent instance     | `uv run --project tools limtool esdb up`             |
| Start throw-away dev instance | `uv run --project tools limtool esdb up --dev`       |
| Health + token check          | `uv run --project tools limtool esdb ping`           |
| Logs                          | `uv run --project tools limtool esdb logs`           |
| Stop                          | `uv run --project tools limtool esdb down`           |

First time: `cp infra/eventsourcingdb/.env.example infra/eventsourcingdb/.env` and set a token.

## Inspecting data

- Claude Code: use the `esdb:*` plugin skills (read-events, run-eventql-query, read-subjects, …)
  with the URL/token from `.env`.
- Codex / shell: use the HTTP API (`docs/knowledge/eventsourcingdb/`) with `curl`.

## Rules

- Never write events to an instance you did not start for the task unless the user says so.
- The persistent instance is capped by the free license tier — do not flood it with
  generated test data; use `--dev` for load or experiments.
- Subjects follow the tenant-scoped scheme from ADR-0004.
