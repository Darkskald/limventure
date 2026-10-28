---
title: "ADR-0013: Expected events are facts"
summary: An expectation of a future event is itself recorded as an event (XExpected), resolved by XFulfilled, XOverdue or XCancelled; a durable scheduler emits Overdue — making delay and absence auditable.
tags: [adr, expected-events, deadlines, sla, scheduler, process-manager]
status: accepted
updated: 2026-10-28
---

# ADR-0013: Expected events are facts

Resolves the main question of [expected events](../discussions/expected-events.md),
originating from [exotic sparks](../vision/exotic-sparks.md).

## Decision

- An expectation is a **domain event**: `<thing>-expected` with `expectedBy` (instant or window),
  the source of the deadline (specification, contract SLA, regulatory profile) and its version.
- Each expectation ends in exactly one terminal event:
  `-fulfilled` (references the fulfilling event), `-overdue` (emitted at the deadline),
  or `-cancelled` (with mandatory reason).
- Overdue is **not** terminal for the business process: a late fulfillment still produces
  `-fulfilled`, flagged late — SLA analytics need both facts.
- A **durable scheduler** emits `-overdue`: driven by a projection of open expectations,
  idempotent (precondition: expectation still open), survives restarts, catches up after downtime.
- In ESDM: process managers with timers (`at: <expectedBy field>`), Given-When-Then scenarios
  for the timer path ([process managers and timers](../knowledge/esdm/process-managers-and-timers.md)).

## Alternatives considered

| Option | Pros | Cons |
|---|---|---|
| Facts (this) | Auditable, SLA measurable from the stream, explicit absence | Scheduler to build; more events |
| Projection from process definition | No extra events | History ambiguous when definitions change |
| External workflow timers (Temporal) | Mature timers | Expectations live outside the event store |

## Consequences

- Neither architecturekit nor EventSourcingDB offers scheduled/delayed events → we build the
  scheduler; logged as AK-011 / ESDB-014 / ESDM-006.
- Expected events add to the event volume (licensing cap, [ADR-0005](0005-integration-events-are-persisted.md)).

## Escalation (agreed 2026-10-28)

- Escalation is **tier 1 configuration** per expectation type and tenant
  ([ADR-0011](0011-extensibility-tiers.md)): who is notified, after which delay (escalation
  levels), whether the task is reassigned. Versioned and audited like all configuration.
- Escalation steps are events (`escalation-triggered` with level and configuration version).
- Notifications are **outbound integration events** ([ADR-0005](0005-integration-events-are-persisted.md))
  delivered by channel adapters (e-mail, Teams, gate control system, …); delivery attempts are events.
- Hard-coded escalation logic in the core is not allowed.
