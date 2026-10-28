---
title: EventSourcingDB event schemas
summary: JSON-schema registration per event type — immutable, retroactively validated, optional closed-world enforcement.
tags: [eventsourcingdb, schemas, validation, versioning]
status: draft
sources:
  - https://docs.eventsourcingdb.io/getting-started/registering-event-schemas/
  - https://docs.eventsourcingdb.io/fundamentals/event-types/
  - https://docs.eventsourcingdb.io/fundamentals/cloud-events/
updated: 2026-10-28
---

# EventSourcingDB event schemas

## Mechanics

- `POST /api/v1/register-event-schema` with `{eventType, schema}` (JSON Schema).
- **Exactly one schema per event type**; it applies to **past and future**
  events of that type.
- On registration **all existing events of that type are validated**; one
  violation → registration rejected. Reads/writes continue meanwhile; an event
  written during the check counts as existing.
- Registering before the first event of the type is instant.
- **Schemas cannot be modified or removed.** A changed schema = new event
  type (hence `.v1`, `.v2` suffixes).
- `$ref` only to local parts (`#/$defs/...`); external files/URLs rejected.
- Schemas are included in backups.
- Read back via `read-event-types` / `read-event-type`.

## Closed set of types (`--require-event-schemas`)

Documented: rejects writes whose type has no schema; does not re-validate
existing events; existing schema-less types become unwritable; startup log
warns about them; restore requires every type in the backup to have a schema.

**Not available in 1.2.0** (flag only in the `preview` image, verified).

## Relevance for the LIMS (own conclusions)

- Register the schema in the same deployment step that introduces a new event
  type, before the first write — immutable schemas fit GxP change control well
  (a schema is effectively a released specification).
- Keep schemas in the repo as source of truth and register them idempotently
  at startup; compare against `read-event-type` to detect drift.
- Use `additionalProperties: false` to stop silent payload creep.
- Enable `--require-event-schemas` once on ≥ 1.3.
