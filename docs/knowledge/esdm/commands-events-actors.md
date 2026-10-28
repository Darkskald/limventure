---
title: ESDM commands, events and actors
summary: Fields and rules for ESDM commands, aggregate-bound and free-standing events, and human or system actors, including event versioning and CloudEvents annotations, with verified YAML.
tags: [esdm, command, event, actor, authorization, cloudevents]
status: draft
sources: [https://www.esdm.io/concepts/command/, https://www.esdm.io/concepts/event/, https://www.esdm.io/concepts/actor/, https://www.esdm.io/reference/core-schema/command/, https://www.esdm.io/reference/core-schema/event/, https://www.esdm.io/reference/core-schema/actor/, https://www.esdm.io/getting-started/your-first-model/]
updated: 2026-10-28
---

# Commands, events, actors

- **Command** – intent, imperative, targets exactly one consistency unit. Required:
  `scope` (aggregate or DCB triple), `data` (JSON Schema; `data: {}` for no payload),
  `publishes` (≥1 bare event names). Optional: `actors` (bare names, = authorization
  and exposure), `constraints[]` (emission rules: ordering, conditional, exclusive).
  No delivery guarantee/idempotency fields – that is transport.
- **Event** – immutable fact, past tense. Required: `scope` (aggregate triple or BC
  pair for free-standing), `data`. **No versioning field**: an evolved event is a new
  event (`invoice-paid-v2`). Single publisher rule.
- **Actor** – role (not a user). `type: human | system`, optional `responsibilities[]`
  (prose), `backedBy[]` (external systems; forbidden on `human`). BC-scoped; the same
  person may be separate actors in different BCs.

Verified (aggregate-bound pair, CloudEvents type as annotation):

```yaml
apiVersion: schema.esdm.io/core/v1
kind: command
name: announce
scope:
  domain: lims
  boundedContext: sample-reception
  aggregate: sample
data:
  type: object
  properties:
    barcode: { type: string }
    expectedBy: { type: string, format: date-time }
  required: [barcode, expectedBy]
publishes: [announced]
actors: [portal-gateway]
---
apiVersion: schema.esdm.io/core/v1
kind: event
name: announced
scope:
  domain: lims
  boundedContext: sample-reception
  aggregate: sample
data:
  type: object
  properties:
    barcode: { type: string }
    expectedBy: { type: string, format: date-time }
  required: [barcode, expectedBy]
metadata:
  annotations:
    cloudevents.type: io.limventure.sample-reception.sample-announced
```

DCB-bound command with free-standing event (verified):

```yaml
apiVersion: schema.esdm.io/core/v1
kind: command
name: book-slot
scope:
  domain: lims
  boundedContext: analysis
  dynamicConsistencyBoundary: instrument-slot
data:
  type: object
  properties:
    instrumentId: { type: string }
    slot: { type: string }
    barcode: { type: string }
  required: [instrumentId, slot, barcode]
publishes: [slot-booked]
---
apiVersion: schema.esdm.io/core/v1
kind: event
name: slot-booked
scope:
  domain: lims
  boundedContext: analysis
data:
  type: object
  properties:
    instrumentId: { type: string }
    slot: { type: string }
    barcode: { type: string }
  required: [instrumentId, slot, barcode]
```

Actors (verified): a system actor backed by an external system.

```yaml
apiVersion: schema.esdm.io/core/v1
kind: actor
name: lab-technician
scope: { domain: lims, boundedContext: sample-reception }
type: human
responsibilities:
  - Registers incoming samples at the reception desk.
---
apiVersion: schema.esdm.io/core/v1
kind: actor
name: portal-gateway
scope: { domain: lims, boundedContext: sample-reception }
type: system
backedBy: [customer-portal]
```

Lint warnings: `event-without-publisher`, `event-without-consumer`,
`aggregate-without-commands/-events`, `orphan-actor`. Note: a command without `actors`
is not flagged (commands emitted by policies/process managers need none).

## Relevance for the LIMS (own conclusion)

- `actors` gives attributability at model level (ADR-0003); the runtime still has to
  record the concrete user/tenant on each event – ESDM does not model metadata like
  tenant or reason, so put those into every event's `data` or into a shared envelope
  convention documented outside ESDM.
- Corrections are new events (`result-corrected`), matching ESDM's no-versioning stance.
