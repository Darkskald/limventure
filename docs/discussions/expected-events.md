---
title: "Open: modeling expected (future) events"
summary: How to represent expectations of future events (deliveries, measurements, sign-offs) so that delay and absence become explicit, auditable facts.
tags: [discussion, expected-events, deadlines, sla, process-manager]
status: superseded
updated: 2026-10-28
---

# Open: modeling expected (future) events

> Main question resolved by [ADR-0013](../adr/0013-expected-events-are-facts.md): expectations are facts; overdue escalates via tier-1 configuration.

Origin: [exotic sparks](../vision/exotic-sparks.md).

## Question

Is an expectation a **fact** ("on 10:02 we started expecting X by 14:00") stored as an event,
or a **projection** derived from the process definition?

## Options

| Option | Pros | Cons |
|---|---|---|
| `XExpected` event + `XFulfilled` / `XOverdue` / `XCancelled` | Explicit, auditable, queryable; overdue is a fact with timestamp | Needs a scheduler emitting `Overdue`; more events |
| Projection from process definition | No extra events | Expectation changes with the definition — history becomes ambiguous |
| External workflow timers (Temporal) | Mature timers | Expectation lives outside the event store |

## Examples from the margarine case

- Supplier announces delivery → `DeliveryExpected(window)`; truck arrives → fulfilled.
- Sample registered → `MeasurementExpected(method, due)` per test of the specification.
- Rejection proposed → `CounterSignatureExpected(role=head-of-analytics)`.

## Questions for the product owner

1. Who defines due dates — specification, contract SLA, regulatory profile?
2. Does overdue trigger escalation (notification) or only reporting?
3. Must an expectation be cancellable, and with which reason?
