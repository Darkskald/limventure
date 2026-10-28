---
title: EventSourcingDB upstream feedback
summary: Gaps, papercuts and wishes for EventSourcingDB and its Rust SDK found while building the LIMS, each with id, repro and current workaround.
tags: [upstream-feedback, eventsourcingdb, rust-sdk]
status: draft
updated: 2026-10-28
---

# EventSourcingDB upstream feedback

Policy: [ADR-0007](../adr/0007-dogfood-architecturekit-and-eventsourcingdb.md).
Versions tested: server 1.2.0, Rust SDK 4.0.4. Background: [knowledge/eventsourcingdb](../knowledge/eventsourcingdb/overview.md).

| Id | Finding | Workaround here | State |
|---|---|---|---|
| ESDB-001 | Docs site describes unreleased ~1.3 (`preview`): `/api/v2`, hash v2, `--require-event-schemas` 404/absent in 1.2.0; no per-page version marker | verify every feature against pinned image | open |
| ESDB-002 | Single API token, no users/roles/read-only tokens | access control in LIMS services, ESDB on isolated network | open |
| ESDB-003 | Event signature is server-side, recomputed on read, unverifiable after key rotation; no endpoint to fetch the public key | — | open |
| ESDB-004 | No field for actor / action time / reason in the event envelope (`time` = write time) | audit data in payload (see AK-001) | open |
| ESDB-005 | `audit-history` / `verify-store` return HTTP 200 before finishing; result only in last NDJSON line | parse last line | open |
| ESDB-006 | Hash chain can be recomputed by someone with disk access; no external anchoring | anchor last audited hash externally (planned) | open |
| ESDB-007 | Configuration via CLI flags only → API token visible in `docker inspect` | — | open |
| ESDB-008 | Server re-sorts keys in `data`; stored payload not byte-identical to submitted | hash over canonical JSON if we ever sign payloads | open |
| ESDB-009 | No delete/redact API; GDPR only via backup-rewrite or crypto-shredding | [GDPR discussion](../discussions/gdpr-vs-immutable-log.md) | open |
| ESDB-010 | Numbers stored as f64 — integers > 2^53 lose precision silently | large integers as strings | open |
| ESDB-011 | Image has no built-in HEALTHCHECK | busybox `wget` in compose | open |
| ESDB-012 | Rust SDK testcontainer defaults to `latest` tag | pin tag explicitly | open |
| ESDB-013 | Restore only into empty DB, blocks I/O; killed restore leaves unstartable data dir | — | open |

## Template

`| ESDB-nnn | what, minimal repro | how we work around it | open/reported/fixed |`
