---
title: EventSourcingDB event model — CloudEvents, subjects, types, sources, snapshots
summary: Event fields, server-assigned metadata, naming and validation rules for subjects, event types and sources, and the snapshots-as-events approach.
tags: [eventsourcingdb, cloudevents, subjects, event-types, modeling]
status: draft
sources:
  - https://docs.eventsourcingdb.io/fundamentals/cloud-events/
  - https://docs.eventsourcingdb.io/fundamentals/subjects/
  - https://docs.eventsourcingdb.io/fundamentals/event-types/
  - https://docs.eventsourcingdb.io/fundamentals/sources/
  - https://docs.eventsourcingdb.io/fundamentals/snapshots/
updated: 2026-10-28
---

# EventSourcingDB event model

## Fields

Client provides only: `source`, `subject`, `type`, `data`, optionally
`traceparent` / `tracestate` (OpenTelemetry). **Any other field → rejected.**

Server sets:

| Field | Value |
|-------|-------|
| `specversion` | `1.0` |
| `id` | global sequential numeric string, zero-based |
| `time` | RFC 3339, ns precision, UTC — **write time, not domain time** |
| `datacontenttype` | always `application/json` |
| `hash` | SHA-256 of the event (see [integrity](integrity-signatures-auditing.md)) |
| `predecessorhash` | hash of the previous event **store-wide**; first = 64 zeros |
| `signature` | Ed25519 signature or `null` |

- `data` must be a JSON **object** (`{}` allowed; arrays/scalars/null rejected).
- `dataschema` is **not supported**; use registered JSON schemas
  ([event-schemas](event-schemas.md)).
- Observed (1.2.0): the server **re-serializes `data` with sorted keys**
  (`{"z":1,"a":"x"}` came back as `{"a":"x","z":1}`).
- No author/user/actor field exists in the envelope.

## Subjects

- Identify the stream; **exactly one subject per event**.
- Path form: starts with `/`, segments of `[0-9A-Za-z_-]`; dots/spaces
  rejected; trailing slash normalized; **case-sensitive**.
- Read/observe filter: exact or **recursive** (`/books/42` also yields
  `/books/42/pages/1`). `/` + recursive = everything.
- Recommended: lowercase, hyphens, aligned with domain; avoid deep hierarchies.

## Event types

- Reverse-DNS namespace + name, e.g. `io.eventsourcingdb.library.book-acquired`.
- Enforced: **≥ 3 dot-separated segments** of `[0-9A-Za-z_-]`, first segment
  ≥ 2 chars. Verified on 1.2.0: `io.bad` → `malformed event type`.
- Conventions: past-tense verb, not verb-first, no generic `updated`.
- Versioning by suffix: `...book-acquired.v1`, `.v2` (no version field).
- Read/observe cannot filter by type (except `fromLatestEvent`); use EventQL.

## Sources

- Must be an **absolute RFC 3986 URI** (stricter than CloudEvents), e.g.
  `https://library.example.io` or tag URI `tag:example.io,2025:library`.
- Pure metadata; no effect on processing. Filterable only via EventQL.
- Uniqueness is guaranteed by `id` alone, regardless of `source`.

## Snapshots

- **No snapshot feature.** A snapshot is a normal event with a dedicated type.
- Replay from the last snapshot via `fromLatestEvent: {type: ...}` on
  read/observe. Vendor advice: only with measured need; prefer smaller streams.

## Relevance for the LIMS (own conclusions)

- `time` is ingestion time; Part 11 audit trail needs the **action timestamp
  and the acting user** → put `occurredAt`, `actor`, `reason`, e-signature
  meaning into `data` (envelope has no slot for them).
- Proposed type prefix: `io.limventure.<context>.<event>.v1`; source as tag
  URI per service, e.g. `tag:limventure.io,2026:sample-service`.
- Subjects like `/samples/<id>`, `/samples/<id>/aliquots/<n>` make recursive
  reads per sample cheap.
- Key-sorting means byte-exact `data` round-trips are not guaranteed; never
  hash the client-side JSON and expect it to equal what is stored.
