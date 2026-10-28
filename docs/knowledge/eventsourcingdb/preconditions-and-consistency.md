---
title: EventSourcingDB preconditions and consistency
summary: Write preconditions (pristine, populated, on-event-id, EventQL) and their transactional and performance semantics.
tags: [eventsourcingdb, consistency, concurrency, preconditions]
status: draft
sources:
  - https://docs.eventsourcingdb.io/fundamentals/preconditions/
  - https://docs.eventsourcingdb.io/about-eventsourcingdb/consistency-guarantees/
  - https://docs.eventsourcingdb.io/best-practices/dynamic-consistency-boundaries/
  - https://github.com/thenativeweb/eventsourcingdb-client-rust
updated: 2026-10-28
---

# EventSourcingDB preconditions and consistency

## Mechanics

- `POST /api/v1/write-events` body: `{"events": [...], "preconditions": [...]}`.
- Preconditions are evaluated **in the same transaction** as the write.
  All pass → all events written; any fails → nothing written, **409 Conflict**
  naming the first failing one (`state conflict: /preconditions/2: ...`).
- Unevaluable precondition (bad EventQL, non-boolean result) → **400**.

## Types

| Type | Since | Holds if |
|------|-------|----------|
| `isSubjectPristine` | 1.0 | subject has no events |
| `isSubjectPopulated` | 1.2.0 | subject has ≥ 1 event |
| `isSubjectOnEventId` | 1.0 | last event of subject has given `eventId` (optimistic lock) |
| `isEventQlQueryTrue` | 1.1.0 | EventQL query returns exactly one `true` |

Recursive variants (subject + all nested subjects) exist **only on the v2 API**
(≥ 1.3); the Rust SDK refuses them against 1.2.0 with `IncompatibleServer`.

## `isEventQlQueryTrue` costs

- While it is evaluated **every other write waits** (reads continue).
- The query scans **all events** unless the `WHERE` bounds `e.id`
  (e.g. `e.id > 1000`), so cost grows with store size.
- Evaluated after all other preconditions. Frequent use makes all writes queue.
- Vendor advice: prefer the subject-based preconditions; bound by event ID.

## Other guarantees

- Atomic multi-subject writes; global strict order by `id`; commit-then-publish.
- **No dedup**: retrying a write stores it twice unless guarded by a
  precondition. Rust SDK returns `OutcomeUnknown` when a write may or may not
  have been stored (stall, broken connection, 500).

## Relevance for the LIMS (own conclusions)

- Aggregate commands: `isSubjectOnEventId` on the last seen event = standard
  optimistic concurrency; `isSubjectPristine` for creation (e.g. sample
  registration, prevents duplicate IDs).
- Cross-stream invariants (unique sample barcode, instrument booked once per
  slot) can use `isEventQlQueryTrue`, but keep them rare and ID-bounded, or
  use dedicated "reservation" subjects (e.g. `/barcodes/<code>` + pristine).
- Idempotent retries: on `OutcomeUnknown` read back before resending; make
  command handlers idempotent via preconditions.
