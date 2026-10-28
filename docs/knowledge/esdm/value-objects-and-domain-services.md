---
title: ESDM value objects and domain services
summary: ESDM value objects (schema plus invariants, no identity) and domain services (stateless functions with arguments, returns and rules), their limits, with verified YAML.
tags: [esdm, value-object, domain-service, ddd]
status: draft
sources: [https://www.esdm.io/concepts/value-object/, https://www.esdm.io/concepts/domain-service/, https://www.esdm.io/reference/core-schema/value-object/, https://www.esdm.io/reference/core-schema/domain-service/]
updated: 2026-10-28
---

# Value objects and domain services

- **Value object** (BC-scoped): `schema` (shape of one instance, required), optional
  `invariants[]` (checksums, cross-field rules, units). No identity, no lifecycle.
- **Domain service** (BC-scoped): `functions[]` (≥1), each `{name, arguments, returns}`
  (JSON Schemas, required) plus optional `description`, `rules[]`. Stateless and
  side-effect free: computes, never mutates. Sending mail is an event handler, waiting
  for events is a process manager.

Verified:

```yaml
apiVersion: schema.esdm.io/core/v1
kind: value-object
name: measured-value
scope: { domain: lims, boundedContext: analysis }
schema:
  type: object
  properties:
    value: { type: number }
    unit: { type: string }
  required: [value, unit]
invariants:
  - name: known-unit
    rule: The unit must be a UCUM code.
---
apiVersion: schema.esdm.io/core/v1
kind: domain-service
name: unit-conversion
scope: { domain: lims, boundedContext: analysis }
functions:
  - name: convert
    arguments:
      type: object
      properties:
        value: { type: number }
        from: { type: string }
        to: { type: string }
    returns:
      type: object
      properties:
        value: { type: number }
    rules:
      - name: ucum-only
        rule: Conversion uses UCUM factors only.
```

**Limitation (observed):** the schema offers no structured way to *use* a value object
inside a command/event `data`, aggregate `state` or read model schema; those are opaque
JSON Schemas and the linter does not resolve `$ref`s to value objects. The connection is
only by name/convention. Value objects are BC-local; sharing across BCs is "a separate
decision" not represented in the model.

## Relevance for the LIMS (own conclusion)

Candidates: measured value with unit, specification limit, batch number with checksum.
Specification-based release decisions ("strict catalog") could be a domain service
(`evaluate-against-specification`) – pure computation, the decision itself remains a
command on an aggregate.
