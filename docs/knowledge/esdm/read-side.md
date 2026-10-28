---
title: ESDM read models and queries
summary: How ESDM models the read side - read models with projections, schema and paradigm, and queries with parameters, result, actors and constraints - with verified YAML.
tags: [esdm, read-model, query, projection, cqrs]
status: draft
sources: [https://www.esdm.io/concepts/read-model/, https://www.esdm.io/concepts/query/, https://www.esdm.io/reference/core-schema/read-model/, https://www.esdm.io/reference/core-schema/query/]
updated: 2026-10-28
---

# Read models and queries

- **Read model** (BC-scoped). Required: `projections[]` (event ref + prose `rule`),
  `schema` (shape of the *whole* materialized view, typically `type: array`). Optional
  `paradigm`: `tabular | document | graph | stream | key-value | search-index |
  time-series | column | vector` (hint only). May project events from other BCs (then a
  context mapping is expected, otherwise warning
  `cross-bounded-context-reference-without-mapping`).
- **Query** (same BC as its read model). Required: `readModel` (bare), `result` (JSON
  Schema). Optional: `parameters` (JSON Schema), `paradigm`, `actors`, `constraints[]`
  (filter/sort/limit as prose). Concrete API shapes (pagination envelopes) are out of
  scope.
- Warnings: `read-model-without-query`, `read-model-without-projections`,
  `query-without-read-model`, `query-without-result`.

Verified:

```yaml
apiVersion: schema.esdm.io/core/v1
kind: read-model
name: inbound-samples
scope:
  domain: lims
  boundedContext: sample-reception
paradigm: tabular
schema:
  type: array
  items:
    type: object
    properties:
      barcode: { type: string }
      status: { type: string, enum: [announced, received, overdue] }
projections:
  - boundedContext: sample-reception
    aggregate: sample
    event: announced
    rule: Append a row with status `announced`.
  - boundedContext: sample-reception
    aggregate: sample
    event: received
    rule: Set status to `received`.
  - boundedContext: sample-reception
    aggregate: sample
    event: flagged-overdue
    rule: Set status to `overdue`.
---
apiVersion: schema.esdm.io/core/v1
kind: query
name: list-inbound-samples
scope:
  domain: lims
  boundedContext: sample-reception
readModel: inbound-samples
parameters:
  type: object
  properties:
    status: { type: string }
result:
  type: array
  items: { type: object }
actors: [lab-technician]
constraints:
  - name: filter-by-status
    rule: When `status` is given, return only rows with that status.
```

## Relevance for the LIMS (own conclusion)

`query.actors` documents who may see which view – useful for the role matrix (analyst,
lab head, QA, controller). Overdue/expected states become ordinary read-model columns
fed by explicit events (see [lims-mapping.md](lims-mapping.md)).
