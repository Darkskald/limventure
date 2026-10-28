---
title: EventSourcingDB upstream feedback
summary: Gaps, papercuts and wishes for EventSourcingDB and its Rust SDK found while dogfooding it in this repository, each with id, repro and current workaround.
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
| ESDB-002 | Single API token, no users/roles/read-only tokens | access control in our services, ESDB on isolated network; forces dedicated instances for GxP tenants (ADR-0004). Wish: per-subject-prefix tokens | open |
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
| ESDB-014 | No scheduled / delayed events or "fire at" mechanism (expected events, ADR-0013) | external scheduler writes `-overdue` with precondition | open |
| ESDB-015 | *PO.* No way to **seal** a subject (1.2.0 preconditions: `isSubjectPristine`, `isSubjectPopulated`, `isSubjectOnEventId`, `isEventQlQueryTrue` — `eventsourcingdb-4.0.4/src/client/precondition.rs:36-126`). Server-side enforcement is the only place a terminal guarantee holds for every writer, and would enable caching/archival (retention classes, ADR-0003). **Caveat:** a hard seal conflicts with correction events after the end of a lifecycle ("disposed on the wrong date"); needs either seal-with-exception (privileged, audited unseal or correction-only event types) or sealing only at archival time | none; decider-level refusal only | open — partially confirmed |
| ESDB-016 | 1.2.0: an event has exactly one `subject` and no tags (`eventsourcingdb-4.0.4/src/event/` has no tag field), so a DCB decision in the Pellegrini sense — **one** event relevant to several boundaries — cannot be stored as one event. Repro: aliquoting (ADR-0022) must write `aliquoted`/`withdrawn`/`filled` to N subjects. Not yet checked whether 1.3 (`preview`) adds tags; verify before asking | N events in one atomic write sharing an `operationId` (ADR-0022) | open — confirmed for 1.2.0 |

## Template

`| ESDB-nnn | what, minimal repro | how we work around it | open/reported/fixed |`
