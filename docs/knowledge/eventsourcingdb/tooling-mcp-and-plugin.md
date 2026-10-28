---
title: EventSourcingDB tooling — MCP server, Claude Code plugin, CLI helpers
summary: The vendor's MCP server and Claude Code plugin for LLM access to EventSourcingDB, plus built-in CLI helpers and API tooling.
tags: [eventsourcingdb, tooling, mcp, claude-code, harness]
status: draft
sources:
  - https://docs.eventsourcingdb.io/extensions/mcp-server/introduction/
  - https://docs.eventsourcingdb.io/extensions/mcp-server/getting-started/
  - https://docs.eventsourcingdb.io/extensions/mcp-server/available-tools/
  - https://docs.eventsourcingdb.io/extensions/claude-code-plugin/introduction/
  - https://docs.eventsourcingdb.io/extensions/claude-code-plugin/getting-started/
  - https://docs.eventsourcingdb.io/extensions/claude-code-plugin/available-skills/
  - https://docs.eventsourcingdb.io/reference/api-overview/
  - https://docs.eventsourcingdb.io/reference/cli-overview/
updated: 2026-10-28
---

# EventSourcingDB tooling

## MCP server

- Docker image `thenativeweb/eventsourcingdb-mcp`; transport **Streamable
  HTTP**; talks to ESDB via its HTTP API.
- `run` flags: `--esdb-url`, `--esdb-api-token`, `--api-token` (optional
  bearer token for MCP clients — **off by default**), `--http-enabled`
  (default false), `--http-port` 3000, `--https-enabled` (default true),
  `--https-port` 4000, `--https-certificate-file`, `--https-private-key-file`.
- Tools: `esdb_ping`, `esdb_verify_api_token`, `esdb_write_events`,
  `esdb_register_event_schema`, `esdb_read_events`, `esdb_read_subjects`,
  `esdb_read_event_types`, `esdb_read_event_type`, `esdb_run_eventql_query`,
  `esdb_get_eventql_documentation`.
- Vendor: for interactive/exploratory use, **not for production write paths**.

## Claude Code plugin

- Install: `/plugin marketplace add thenativeweb/claude-plugins`, then
  `/plugin install esdb@thenativeweb`. Skills issue `curl` calls; no SDK, no
  background process.
- Env: `ESDB_URL` (default `http://localhost:3000`), `ESDB_API_TOKEN`,
  `ESDB_SOURCE`, `ESDB_EVENT_TYPE_PREFIX`.
- Skills: `/esdb:start-server` (Docker, temp data, HTTP, UI, simple token —
  data lost on stop), `ping`, `verify-api-token`, `write-events`,
  `read-events`, `observe-events` (default 30 s timeout), `read-subjects`,
  `read-event-types`, `read-event-type`, `run-eventql-query`,
  `register-event-schema` (schemas immutable).
- Already installed in this harness (skills `esdb:*` are listed).

## Built-in CLI and API helpers

- `eventsourcingdb generate` — semi-realistic sample events for a domain.
- `eventsourcingdb docs` — embedded docs server (version-matched docs!).
- `eventsourcingdb diagnostics` — versions, license, server options.
- OpenAPI: v1 YAML at `/.well-known/openapi`; v2 JSON at
  `/api/v2/system/openapi` (≥ 1.3); catalog `/.well-known/api-catalog`.
- Bruno collection: `thenativeweb/eventsourcingdb-client-bruno`.

## Relevance for the LIMS (own conclusions)

- Point the plugin at the dev compose instance
  (`ESDB_URL=http://localhost:3000`, `ESDB_EVENT_TYPE_PREFIX=io.limventure`)
  for exploratory modelling; never at validated environments (the single
  token grants full write access).
- `eventsourcingdb docs` from the pinned image gives docs matching 1.2.0 —
  better reference than the website, which documents the preview.
- MCP server without `--api-token` is an open write proxy; only on localhost.
