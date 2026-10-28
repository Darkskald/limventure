---
title: ESDM aggregates, dynamic consistency boundaries and entities
summary: The two first-class consistency units in ESDM (aggregate and DCB), their identity strategies, invariants and consults, plus entities as identity anchors, with verified YAML.
tags: [esdm, aggregate, dcb, dynamic-consistency-boundary, entity, invariants]
status: draft
sources: [https://www.esdm.io/concepts/aggregate/, https://www.esdm.io/concepts/dynamic-consistency-boundary/, https://www.esdm.io/concepts/entity/, https://www.esdm.io/reference/core-schema/aggregate/, https://www.esdm.io/reference/core-schema/dynamic-consistency-boundary/, https://www.esdm.io/reference/core-schema/entity/]
updated: 2026-10-28
---

# Aggregates, DCBs, entities

| Kind | Required | Identity | Notes |
|---|---|---|---|
| `aggregate` | `scope`, `identifiedBy`, `state` | one of `{source: state, field}`, `{source: static, value}`, `{source: generated, generator}` | container, one id, persistent state, `invariants[]` |
| `dynamic-consistency-boundary` | `scope`, `identifiedBy[]`, `consults[]` | list of `{name, source: command-payload, field}` / `static` / `generated` | no state; decision state = consulted events; append condition implicit |
| `entity` | `scope`, `schema`, `identifiedBy` | `{source: schema, field}` or `{source: static, value}` | not a consistency unit, no commands; names the thing behind an id |

Invariants are state rules checked when a command is handled. **Authorization is never
an invariant** – it lives in `command.actors`.

## Aggregate (verified)

```yaml
apiVersion: schema.esdm.io/core/v1
kind: aggregate
name: sample
scope:
  domain: lims
  boundedContext: sample-reception
identifiedBy:
  source: state
  field: barcode
state:
  type: object
  properties:
    barcode: { type: string }
    received: { type: boolean }
  required: [barcode, received]
invariants:
  - name: receive-once
    rule: A sample that has been received cannot be received again.
```

## DCB + entity (verified)

```yaml
apiVersion: schema.esdm.io/core/v1
kind: entity
name: instrument
scope: { domain: lims, boundedContext: analysis }
schema:
  type: object
  properties: { instrumentId: { type: string } }
  required: [instrumentId]
identifiedBy: { source: schema, field: instrumentId }
---
apiVersion: schema.esdm.io/core/v1
kind: dynamic-consistency-boundary
name: instrument-slot
scope: { domain: lims, boundedContext: analysis }
identifiedBy:
  - { name: instrument, source: command-payload, field: instrumentId }
  - { name: slot, source: command-payload, field: slot }
consults:
  - boundedContext: analysis
    event: slot-booked
    criteria: All slot-booked events with the same instrumentId and slot.
invariants:
  - name: slot-free
    rule: A slot on an instrument can be booked at most once.
```

A DCB-bound command uses `scope.dynamicConsistencyBoundary` and publishes
**free-standing** events (`scope: {domain, boundedContext}`), see
[commands-events-actors.md](commands-events-actors.md). DCB is BC-local; cross-BC
consistency is process-manager territory. Boundaries may overlap.

## Relevance for the LIMS (own conclusion)

EventSourcingDB supports DCB-style conditional appends, so DCBs fit naturally for
rules spanning several ids (instrument slot booking, "one active approval per batch").
Keep aggregates for clear lifecycles (sample, test order, delivery). Whether
architecturekit supports DCBs must be checked before modeling many of them.
