---
title: EventSourcingDB overview and release status
summary: What EventSourcingDB is, its core properties, and the gap between the published docs and the latest released version (1.2.0).
tags: [eventsourcingdb, event-store, overview, versions]
status: draft
sources:
  - https://docs.eventsourcingdb.io/
  - https://docs.eventsourcingdb.io/about-eventsourcingdb/changelog/
  - https://docs.eventsourcingdb.io/about-eventsourcingdb/consistency-guarantees/
  - https://docs.eventsourcingdb.io/reference/api-overview/
  - https://docs.eventsourcingdb.io/deployment-and-operations/scaling-and-high-availability/
  - https://docs.eventsourcingdb.io/deployment-and-operations/upgrading-eventsourcingdb/
  - https://hub.docker.com/r/thenativeweb/eventsourcingdb
updated: 2026-10-28
---

# EventSourcingDB overview and release status

EventSourcingDB (ESDB) is a purpose-built, **closed-source** event store by
the native web GmbH. Single binary (Go), HTTP API, CloudEvents-shaped events.

## Core properties

- Append-only log; events **cannot be updated or deleted** via any API.
- Every event gets a **global, gap-free, monotonically increasing numeric `id`**
  (string `"0"`, `"1"`, ...) across all subjects.
- Writes are **atomic per request**, also across multiple subjects; concurrent
  writes are serialized internally. No automatic deduplication.
- Events are visible only after commit; observers get them pushed afterwards
  (clients must resume by last seen `id` after a disconnect).
- Every event carries `hash` + `predecessorhash` (store-wide hash chain);
  optional Ed25519 `signature`. See [integrity](integrity-signatures-auditing.md).
- **Single instance only**: no clustering, replication, failover. Upgrades need
  downtime. Running two instances on one data directory may corrupt data.
- No distributed transactions with external systems.

## Release status (as of 2026-10-28)

| Item | Value |
|------|-------|
| Latest stable image tag | `1.2.0` (pushed 2025-11-02) |
| `latest` tag | = 1.2.0 |
| `preview` tag | rebuilt 2026-10-28, reports `(version unavailable)` |
| Changelog top entry | 1.2.0 (2025-11-03) |

**The docs site describes an unreleased version (≈1.3 / preview).** Examples:

- API overview says `/api/v1` is deprecated in favour of `/api/v2`
  (`QUERY` HTTP method, RFC 10008). On 1.2.0, `/api/v2/system/openapi` → **404**.
- Hash format `esdb:hash:v2:` is "written since version 1.3"; 1.2.0 writes
  unprefixed v1 hashes (verified).
- `--require-event-schemas` and `--rate-limit-requests-per-second` exist only in
  `preview`, not in `1.2.0 run --help` (verified).
- Recursive preconditions are v2-API only (per Rust SDK README).

Verified present in 1.2.0: `/api/v1/audit-history`, `/api/v1/verify-store`,
`/api/v1/backup`, `/api/v1/health`, `--signing-key-file`, `--read-only`.

Upgrade facts: same data directory, one-time index conversion on first start
(some requests 503 meanwhile), **no downgrade** of a data directory, backups
with v2 hashes cannot be restored into pre-1.3. Update hash-verifying clients
**before** upgrading the server to 1.3.

## Related

- [Running and configuration](running-and-configuration.md)
- [Licensing and limits](licensing-and-limits.md)
- [Rust SDK](rust-sdk.md)

## Relevance for the LIMS (own conclusions)

- Pin `1.2.0` now; plan a validated upgrade to 1.3 (hash v2, API v2) as a
  change-controlled event — it changes the integrity verification algorithm.
- Docs cannot be trusted 1:1 for the pinned version; test every feature
  against the pinned image (CSV/IQ-OQ evidence anyway).
- Single-instance + no HA is acceptable for a lab LIMS if backup/restore and
  RTO are defined; document it in the risk assessment.
- Closed source + small vendor → supplier assessment and escrow/exit strategy
  (backup NDJSON format is the exit path).
