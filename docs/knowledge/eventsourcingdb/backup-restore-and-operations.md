---
title: EventSourcingDB backup, restore and operational modes
summary: Full NDJSON backups, restore-into-empty-only semantics, failure handling, read-only mode, disk reserve, upgrades and lack of HA.
tags: [eventsourcingdb, backup, restore, operations]
status: draft
sources:
  - https://docs.eventsourcingdb.io/deployment-and-operations/backup-and-restore/
  - https://docs.eventsourcingdb.io/deployment-and-operations/read-only-mode/
  - https://docs.eventsourcingdb.io/deployment-and-operations/upgrading-eventsourcingdb/
  - https://docs.eventsourcingdb.io/deployment-and-operations/scaling-and-high-availability/
  - https://docs.eventsourcingdb.io/reference/api-overview/
updated: 2026-10-28
---

# EventSourcingDB backup, restore and operational modes

## Backup

- `POST /api/v1/backup` → NDJSON stream of **all events and schemas**
  (snapshots included as they are events). Verified on 1.2.0.
- **Full backups only** — no incremental/differential.
- Runs online (also in read-only mode); writes continue; backup = state at its
  start.
- Errors arrive in-stream: `{"type":"error","payload":"<string>"}` (payload is
  a plain string here, unlike other routes). **HTTP 200 is sent first → check
  the last line**; discard backups that end with an error.

## Restore

- `POST /api/v1/restore` with `--data-binary @backup.json`.
- **Only into an empty database**; otherwise rejected.
- Lockdown during restore: **no reads and no writes**.
- On failure (invalid backup, over licensed capacity, shutdown) ESDB removes
  what it restored; if that fails it refuses reads/writes (health: `locked`,
  `fail`). A **hard kill during restore** leaves a data directory ESDB refuses
  to start on → empty it and restore again.
- Backups are version-tolerant forward; backward only if the older version can
  read everything (v2-hash events need ≥ 1.3).

## Read-only mode

- `--read-only` flag (survives restarts) or `POST /api/v1/put-into-read-only-mode`
  (until next start; cannot be switched off at runtime).
- Blocks writes and schema registration with **503**; reads, observe, EventQL
  keep working.
- Automatic read-only after a storage failure (until restart; health
  `read-only`/`fail`) — the failed write's client cannot tell if it was stored.
- Automatic read-only when free disk < **1 GiB**; writes resume by themselves at
  ≥ 2 GiB. `system:diskRemaining` warns earlier.

## Upgrades and availability

- Upgrade = stop, swap image, start on same data directory. Downtime required.
- **No downgrade** of a data directory; back up before upgrading.
- **No HA, clustering, replication or failover** (planned for the future).

## GDPR / erasure

No deletion or redaction API. Erasure only via backup → filter/transform →
restore into a fresh instance, or crypto-shredding at application level.
Vendor recommends keeping personal data out of events (references/pseudonyms).

## Relevance for the LIMS (own conclusions)

- Backup = full dump; for large stores schedule nightly full backups and
  verify each (last line + test restore into a scratch instance +
  `audit-history` on it). Store backups on WORM/immutable storage.
- Restore lockdown + no HA → define RTO honestly; consider a warm standby fed
  by an observer that writes to a second (licensed) instance.
- Migration-based redaction alters the history, so the original hash chain no
  longer applies (how restore treats a modified backup is undocumented —
  test before relying on it) → conflicts with audit-trail immutability. Design for crypto-shredding of personal data (patients,
  employees) from day one; keep PII out of events.
