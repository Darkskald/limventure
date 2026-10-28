---
title: Running and configuring EventSourcingDB
summary: CLI flags, ports, Docker image facts, health endpoints, management UI and shutdown behaviour of EventSourcingDB 1.2.0.
tags: [eventsourcingdb, operations, docker, configuration]
status: draft
sources:
  - https://docs.eventsourcingdb.io/getting-started/installing-eventsourcingdb/
  - https://docs.eventsourcingdb.io/getting-started/running-eventsourcingdb/
  - https://docs.eventsourcingdb.io/getting-started/using-the-management-ui/
  - https://docs.eventsourcingdb.io/reference/cli-overview/
  - https://docs.eventsourcingdb.io/deployment-and-operations/deploying-with-docker/
  - https://docs.eventsourcingdb.io/deployment-and-operations/managing-configuration-and-secrets/
  - https://docs.eventsourcingdb.io/deployment-and-operations/logging-and-monitoring/
updated: 2026-10-28
---

# Running and configuring EventSourcingDB

Ready-made compose setup: [`infra/eventsourcingdb/`](../../../infra/eventsourcingdb/README.md).

## Configuration model

- **Flags only.** No environment-variable or config-file support. Secrets from
  env must be expanded into the args (shell, Compose, K8s `$(VAR)`).
- Subcommands: `run`, `diagnostics`, `docs` (embedded docs server), `generate`
  (sample events), `version`, `completion`.

## `run` flags (1.2.0, from `run --help`)

| Flag | Default | Meaning |
|------|---------|---------|
| `--api-token` | — (required) | single bearer token for API + UI |
| `--data-directory` | — | persistent store dir (required for prod) |
| `--data-directory-temporary` | off | temp dir on disk, wiped on shutdown |
| `--https-enabled` | **true** | HTTPS on `--https-port` (default **4000**) |
| `--https-certificate-file` / `--https-private-key-file` | — | TLS material |
| `--http-enabled` | false | plain HTTP on `--http-port` (default **3000**) |
| `--signing-key-file` | — | Ed25519 PKCS#8 PEM key → event signatures |
| `--license-file` / `--license-string` | — | commercial license |
| `--read-only` | off | reject all writes |
| `--with-ui` | off | management UI on the same port |
| `--development-mode` | off | vendor-internal only, needs special license |
| `--ai-model` / `--ai-option` | — | "EventAI" query generation in the UI |

Data directory: ESDB owns it; **never touch files inside** (some hold
confirmed-but-not-yet-compacted writes). Observed layout: `events/`,
`indexes/`, `schemas/`.

## Docker image facts (`thenativeweb/eventsourcingdb:1.2.0`, observed)

- Alpine base, runs as user `esdb` (uid 100), entrypoint `eventsourcingdb`,
  workdir `/var/lib/esdb`, exposes 3000 + 4000. **No built-in HEALTHCHECK**;
  busybox `wget` is available for one.
- Vendor production baseline: `--init`, `--restart always`, volume at
  `/var/lib/esdb` **plus** `--data-directory=/var/lib/esdb` (mount alone is not
  enough), config dir `/etc/esdb` (TLS, license), pinned tag, HTTP disabled.

## Health and monitoring

- `GET /api/v1/ping` — **no auth**, 200 when running, 503 while shutting down.
  Response is a CloudEvent `io.eventsourcingdb.api.ping-received`.
- `GET /api/v1/health` — auth required; RFC-draft health JSON
  (`application/health+json`) or `?format=openmetrics` for Prometheus.
  Checks include `store:eventCount`, `store:eventCapacity`,
  `license:remaining`, `store:operationMode`, `system:diskRemaining`.
- `POST /api/v1/verify-api-token` — 200 + `api-token-verified` event, or 401.
- Logs: structured JSON (Go `slog`) on stdout.
- Every response has `Server: EventSourcingDB/<version>`.
- `eventsourcingdb diagnostics --url … --api-token …` prints versions, license
  details and the server's options.

## Management UI (`--with-ui`)

Dashboard (status, live latest events, license, event count, disk, CPU/RAM
graphs — data from the health endpoint) and an EventQL editor. Login with the
API token. Vendor: **dev/debug only, never expose publicly.** Browser-blocked
ports (e.g. 6000) break the UI but not the API.

## Shutdown

`SIGTERM`/`SIGQUIT`/Ctrl+C = graceful: long-running reads/audits/backups end
with `database is shutting down: try again later`, others get 5 s, buffered
data is flushed. Non-graceful kill loses **no confirmed write** (WAL replay on
next start, slower start). A kill during **restore** leaves an unstartable
data directory (see [backup-restore-and-operations](backup-restore-and-operations.md)).

## Relevance for the LIMS (own conclusions)

- Token in args is visible via `docker inspect`/`ps`; acceptable for dev, for
  prod use an orchestrator secret and restrict host access.
- Use `/api/v1/ping` for liveness and `/api/v1/health` (with token) for
  readiness/monitoring, including the `license:remaining` and capacity checks.
