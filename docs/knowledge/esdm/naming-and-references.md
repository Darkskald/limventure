---
title: ESDM names, scopes and the esdm reference notation
summary: Name pattern, bare naming of events and commands, the scope shapes per kind, how in-model references work, and the esdm URI notation for pointing at elements from outside.
tags: [esdm, naming, references, scope, conventions]
status: draft
sources: [https://www.esdm.io/reference/reference-notation/, https://www.esdm.io/concepts/event/, https://www.esdm.io/reference/core-schema/overview/, https://www.esdm.io/concepts/bounded-context/]
updated: 2026-10-28
---

# Names, scopes and references

## Names

- `name` pattern: `^[a-z][a-z0-9-]*$` (kebab-case). Property names inside JSON Schemas
  are free (`barcode`, `expectedBy` both fine).
- **Bare names.** Event = past tense without the aggregate: aggregate `sample` publishes
  `received`, not `sample-received` (warning
  `esdm/modeling/event-name-with-aggregate-prefix`). Command = imperative verb: `receive`.
  Spoken/derived forms: `SampleReceived`, `ReceiveSample`, CloudEvents type
  `<prefix>.sample-received` – composed by tools from scope + name.
- Free-standing (DCB) events have no aggregate and must carry a self-explanatory name
  (`slot-booked`); the prefix rule does not apply.
- Inside a BC, aggregates, DCBs, entities, value objects and domain services share one
  namespace (`esdm/structure/ambiguous-name`). Other kinds may reuse a name
  (aggregate `order` + read model `order`).

## Scope shapes

| Scope | Kinds |
|---|---|
| none | `domain`, `context-mapping` |
| `{domain}` | `subdomain`, `bounded-context`, `policy`, `event-handler`, `process-manager`, `external-system`, `domain-story` |
| `{domain, boundedContext}` | `aggregate`, `dynamic-consistency-boundary`, `read-model`, `query`, `entity`, `value-object`, `domain-service`, `actor`, free-standing `event` |
| `{domain, boundedContext, aggregate}` | aggregate-bound `command` / `event` |
| `{domain, boundedContext, dynamicConsistencyBoundary}` | DCB-bound `command` |

## In-model references

- **Bare** where scope fixes the context: `command.publishes`, `command.actors`,
  `query.readModel`, `query.actors`, `subdomain.boundedContexts`, `actor.backedBy`,
  `event-handler.sideEffects[].externalSystem`.
- **Triples** where the consumer is domain-scoped: event refs
  `{boundedContext, aggregate, event}` or `{boundedContext, event}`; command refs
  `{boundedContext, aggregate, command}` or `{boundedContext, dynamicConsistencyBoundary, command}`.
- Context mapping endpoints: `{domain, boundedContext}` or `{domain, externalSystem}`.
- Unresolvable reference → `esdm/structure/unresolved-reference` (with suggestion).

## Reference notation (outside the model)

URI with scheme `esdm:` (no `//` – a name, not a location); each segment `kind=name`
following containment:

```
esdm:domain=lims
esdm:domain=lims/bounded-context=sample-reception/aggregate=sample/event=received
esdm:domain=lims/bounded-context=analysis/event=slot-booked      # free-standing
esdm:domain=lims/process-manager=await-sample
esdm:context-mapping=reception-to-portal                       # no domain segment
esdm:domain=lims/bounded-context=sample-reception/aggregate=sample/feature=receiving-a-sample
```

References stop at elements (no schema fields, invariants or terms). Stable against
file moves, **not** against renames. `esdm documentation` maps a reference to a page by
replacing `=` with `_`.

## Relevance for the LIMS (own conclusion)

Use `esdm:` URIs in ADRs, discussions and code comments when pointing at model
elements – they are greppable and survive file reorganizations. Put the CloudEvents
event type into `metadata.annotations.cloudevents.type` so a future `limtool` check can
compare model and Rust code (ADR-0002 drift concern).
