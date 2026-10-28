---
title: ESDM process managers and timers
summary: Stateful, correlated process managers in ESDM with startsWhen, endsWhen, reactions and relative or absolute timers - the mechanism for deadlines and overdue detection - with verified YAML.
tags: [esdm, process-manager, timers, deadlines, saga, expected-events]
status: draft
sources: [https://www.esdm.io/concepts/process-manager/, https://www.esdm.io/reference/core-schema/process-manager/]
updated: 2026-10-28
---

# Process managers and timers

Domain-scoped, long-running coordinator; one instance per correlation key.

Required: `scope`, `deliveryGuarantee` (+ `idempotency` if at-least-once),
`correlatedBy {source: event-field, field}`, `state` (JSON Schema), `startsWhen[]`
(event refs, **array**), `endsWhen[]` (`{name, condition}` – *not* `rule`; the website
reference is wrong here, verified with lint), `reactions[]`.
Optional: `timers[]`, `invariants[]`, `constraints[]`.

- `correlatedBy.field` must exist on every `startsWhen` and `reactions[].when` event
  (linter: `process-manager-correlated-by-field`).
- `reactions[]`: `{when, rule, emits?, setTimers?, cancelTimers?}`; `when` is an event
  ref or `{timer: <name>}`.
- `timers[]`: `{name, description?}` plus exactly one of
  `after: {value, unit}` (`seconds|minutes|hours|days|weeks|months|years`, calendar
  arithmetic) or `at: <state field>` holding an absolute timestamp
  (linter: `process-manager-timer-at-field`).
- A process manager **emits commands only**; it cannot publish events itself.

Verified – deadline for an announced sample:

```yaml
apiVersion: schema.esdm.io/core/v1
kind: process-manager
name: await-sample
scope:
  domain: lims
deliveryGuarantee: at-least-once
idempotency:
  owner: self
  strategy: Track processed event ids per instance.
correlatedBy:
  source: event-field
  field: barcode
state:
  type: object
  properties:
    barcode: { type: string }
    expectedBy: { type: string, format: date-time }
    closed: { type: boolean }
startsWhen:
  - boundedContext: sample-reception
    aggregate: sample
    event: announced
endsWhen:
  - name: closed
    condition: state.closed is true
timers:
  - name: arrival-deadline
    at: expectedBy
reactions:
  - when:
      boundedContext: sample-reception
      aggregate: sample
      event: announced
    rule: Store `expectedBy` and arm the arrival deadline.
    setTimers: [arrival-deadline]
  - when:
      boundedContext: sample-reception
      aggregate: sample
      event: received
    rule: Mark the instance closed and cancel the deadline.
    cancelTimers: [arrival-deadline]
  - when:
      timer: arrival-deadline
    rule: Flag the sample overdue and close the instance.
    emits:
      - boundedContext: sample-reception
        aggregate: sample
        command: flag-overdue
```

`flag-overdue` is an ordinary command on the `sample` aggregate publishing
`flagged-overdue`. Given-When-Then can test the timer path
([extension-given-when-then.md](extension-given-when-then.md)).

## Relevance for the LIMS (own conclusion)

This is the ESDM answer to "expected future events": the expectation itself is a fact
(`announced` with `expectedBy`), the deadline is a process-manager timer, and absence
becomes an explicit, auditable event (`flagged-overdue`). Details in
[lims-mapping.md](lims-mapping.md).
