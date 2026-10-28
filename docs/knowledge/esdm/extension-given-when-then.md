---
title: ESDM Given-When-Then extension
summary: The given-when-then feature kind - behavioral scenarios per consistency unit in four variants (aggregate, DCB, process manager, read model) - with verified YAML including a timer scenario.
tags: [esdm, given-when-then, bdd, testing, specification, extension]
status: draft
sources: [https://www.esdm.io/extensions/given-when-then/introduction/, https://www.esdm.io/extensions/given-when-then/concepts/feature/, https://www.esdm.io/extensions/given-when-then/concepts/scenario/, https://www.esdm.io/extensions/given-when-then/reference/overview/, https://www.esdm.io/extensions/given-when-then/reference/feature/, https://www.esdm.io/extensions/given-when-then/reference/scenario/]
updated: 2026-10-28
---

# Given-When-Then extension

`apiVersion: schema.esdm.io/given-when-then/v1`, `kind: feature`. One feature = one
consistency unit; the `scope` discriminator selects the variant:

| Variant | `scope` | `given[]` | `when` | `then` |
|---|---|---|---|---|
| Aggregate | `domain, boundedContext, aggregate` | `{event, data}` bare | `{command, data, actor?}` | `{events: [{event, data}]}` or `{rejection: {invariant}}` |
| DCB | `domain, boundedContext, dynamicConsistencyBoundary` | scoped event refs + `data` | as aggregate | as aggregate |
| Process manager | `domain, processManager` | scoped refs + `data` | scoped event + `data`, or `{timer}` | any of `emits[]` (command refs + `data`), `setTimers`, `cancelTimers`, `state`, `ended: true` |
| Read model | `domain, boundedContext, readModel` | scoped refs + `data` | `{query, parameters}` | `{result: ...}` or `{readModel: ...}` |

Scenario fields: `name`, `description?`, `given` (may be `[]`), `when`, `then`.
`then.events: []` expresses idempotency. Rejections must name a declared invariant;
`when.actor` must be in the command's `actors`. Features live next to their unit, not
in a `tests/` dir. Scenarios are meant as executable test fixtures.

Verified (aggregate):

```yaml
apiVersion: schema.esdm.io/given-when-then/v1
kind: feature
name: receiving-a-sample
scope:
  domain: lims
  boundedContext: sample-reception
  aggregate: sample
scenarios:
  - name: first-receipt
    given:
      - event: announced
        data: { barcode: S-1, expectedBy: "2026-11-01T12:00:00Z" }
    when:
      command: receive
      data: { barcode: S-1 }
      actor: lab-technician
    then:
      events:
        - event: received
          data: { barcode: S-1 }
  - name: second-receipt-rejected
    given:
      - event: received
        data: { barcode: S-1 }
    when:
      command: receive
      data: { barcode: S-1 }
    then:
      rejection:
        invariant: receive-once
```

Verified (process manager, timer path):

```yaml
apiVersion: schema.esdm.io/given-when-then/v1
kind: feature
name: sample-arrival-deadline
scope:
  domain: lims
  processManager: await-sample
scenarios:
  - name: deadline-passes
    given:
      - boundedContext: sample-reception
        aggregate: sample
        event: announced
        data: { barcode: S-1, expectedBy: "2026-11-01T12:00:00Z" }
    when:
      timer: arrival-deadline
    then:
      emits:
        - boundedContext: sample-reception
          aggregate: sample
          command: flag-overdue
          data: { barcode: S-1 }
      ended: true
```

## Relevance for the LIMS (own conclusion)

Features are a direct input for architecturekit decider tests (given events, when
command, then events/refusal). A `limtool` generator from feature YAML to Rust test
cases would keep model and code verifiably in sync. `uncovered-invariant` forces
regulatory rules (four-eyes, sign-off) to have a rejecting scenario.
