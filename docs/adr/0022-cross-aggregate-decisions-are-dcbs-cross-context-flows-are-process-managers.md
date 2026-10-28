---
title: "ADR-0022: Cross-aggregate decisions are DCBs, cross-context flows are process managers"
summary: A decision spanning several aggregates within one bounded context at one moment is an atomic multi-subject write (DCB) with one event-id precondition per subject; flows across contexts or time are process managers with explicit compensation, never distributed transactions.
tags: [adr, architecture, consistency, dcb, process-manager, architecturekit]
status: accepted
updated: 2026-10-28
---

# ADR-0022: Cross-aggregate decisions are DCBs, cross-context flows are process managers

## Context

Physical lab acts touch several aggregates at once. Aliquoting changes the source sample's
lineage, withdraws quantity from the source container, and labels and fills N target
containers ([ADR-0017](0017-container-is-a-core-aggregate-separate-from-sample.md)); pooling
is the many-to-one mirror. A half-done aliquot must never be visible.

Other flows span bounded contexts or time: an off verdict opens a deviation
([ADR-0019](0019-out-of-spec-results-open-a-deviation.md)), an expectation turns overdue
([ADR-0013](0013-expected-events-are-facts.md)), a resample yields a new sample and order.

What the pinned stack offers (architecturekit 0.21.0, EventSourcingDB 1.2.0):

- ESDB writes are atomic across subjects, with per-subject preconditions.
- architecturekit has `Store::write(Vec<EventOn>, Vec<Precondition>)` and
  `Precondition::on_event_id`, but no multi-subject decider, no public load-with-event-id,
  no retry for `write` and no multi-subject `given` (AK-017). No process managers or
  durable timers (AK-003, AK-011).
- ESDM models DCBs as their own consistency unit
  ([consistency units](../knowledge/esdm/consistency-units.md)).

## Decision

1. **Within one bounded context, at one moment** — a decision whose invariants span several
   aggregates is a **DCB**: load every involved state with its last event id, decide once,
   write all events in **one** atomic multi-subject write with one `on_event_id`
   (or `on_pristine_subject`) precondition **per involved subject**, retry on conflict.
   EventSourcingDB 1.2.0 has exactly one subject per event and no event tags (ESDB-016), so
   the act is written as **one event per involved subject** (e.g. `aliquoted` on each new
   sample, `withdrawn` on the source container, `filled` on each target) in the same
   atomic write. All carry the same `operationId`, actor, reason and timestamp; together
   they are one fact. Each aggregate folds only its own subject's events.
2. **Across bounded contexts or over time** — a **process manager** (or a stateless policy
   where no memory is needed) reacting to events, with explicit compensation events.
   No distributed transactions, no two-phase commit.
3. Atomicity is **never** emulated by a saga: if a half state must not be visible, it is a
   DCB, and the boundary must be drawn so that it fits in one bounded context.
4. **Interim helper:** until AK-017 is resolved upstream, `lims-kernel` provides one small
   multi-subject decide-and-write helper (load with event ids, derive preconditions,
   retry), marked `// upstream: AK-017`, deleted once architecturekit ships an equivalent.
   It is not a general wrapper layer ([ADR-0007](0007-dogfood-architecturekit-and-eventsourcingdb.md)).

## Alternatives considered

| Option | Pros | Cons |
|---|---|---|
| DCB in-context, process managers across (this) | Atomic where physics demands it; loose coupling across contexts; maps 1:1 to ESDM | Interim helper until AK-017; DCB scope must be kept small (contention) |
| Saga for everything | One mechanism | Half-aliquoted states visible; compensations for physical acts are fiction |
| Larger aggregates (sample owns its containers) | Single-subject deciders suffice | Breaks ADR-0017 (pools, plates, re-used containers); hot streams |
| Hand-written `Store::write` at every call site | No helper code | Every forgotten precondition silently breaks consistency |

## Consequences

- **Audit:** one physical act = one atomic write, one `operationId`, one actor, one reason,
  one timestamp — the trail reads like the lab notebook, grouped by `operationId`. Compensations across contexts are themselves attributable
  events, never deletions.
- **Correctness:** preconditions are derived from what was loaded, not hand-listed.
- **Extensibility:** extensions (ADR-0012) observe the single DCB fact via published events;
  they never take part in the transaction.
- **Contention:** a DCB locks all involved subjects for one write; keep DCBs to the subjects
  the invariant genuinely needs (no "all containers of the tenant").
- **Upstream:** AK-017 becomes a dogfooding priority; process managers stay blocked on
  AK-003/AK-011 and need their own decision (library vs. separate crate).

## Open points

- Uniqueness rules over unbounded sets (external barcode per tenant) — DCB over an index
  subject vs. EventQL precondition; interacts with AK-008.
- Whether process-manager infrastructure belongs in architecturekit or in this repo.
