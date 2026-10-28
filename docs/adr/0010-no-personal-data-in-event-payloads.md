---
title: "ADR-0010: No personal data in event payloads"
summary: Events reference people only by opaque ids; names, contact data and other personal data live in an erasable person registry, so GDPR erasure and a future clinical profile never require rewriting the immutable log.
tags: [adr, gdpr, privacy, personal-data, clinical, event-design]
status: accepted
updated: 2026-10-28
---

# ADR-0010: No personal data in event payloads

Resolves the clinical open point of [ADR-0009](0009-launch-profile-food-and-iso-17025.md)
and the [GDPR discussion](../discussions/gdpr-vs-immutable-log.md).

## Context

Clinical (ISO 15189 / CLIA, patient data) is **"not now" — not ruled out** (PO, 2026-10-28).
Events are immutable and EventSourcingDB has no redact API
([ESDB-009](../upstream-feedback/eventsourcingdb.md)). Whatever personal data enters an event
payload stays there for the store's lifetime.

## Decision

- Event payloads contain **no personal data** — not even of employees. People appear only as
  opaque, stable ids (`person:<uuid>`), e.g. in `lims_kernel::Actor`.
- A **person registry** (separate, mutable, erasable store) maps ids to names, contact data,
  roles. Erasure = deleting/anonymising the registry entry; events keep the opaque id.
- Free-text fields in events (reasons, comments) are flagged as *may contain personal data*;
  the UI warns, and the data model keeps them out of payloads where feasible (stored in the
  registry/blob store, referenced by id + hash).
- Raw inbound messages already go to the blob store ([ADR-0005](0005-integration-events-are-persisted.md)).
- Signature records hold the signer's id; the printed name at signing time is captured in an
  erasable signature manifest, not in the event (a GxP retention exemption may later allow
  keeping it longer — decided per profile).

## Alternatives considered

| Option | Pros | Cons |
|---|---|---|
| Ids only + person registry (this) | Erasure trivial, clinical-ready, no key management | Extra lookup for every display; registry is audit-relevant |
| Crypto-shredding (per-person keys) | Data stays in events | Key management, regulators' view on shredding = erasure unclear, encrypted fields not queryable |
| Names in events, rely on retention exemption | Simplest | Breaks the moment clinical or a GDPR request without exemption arrives |

## Consequences

- Read models join on the registry; projections must tolerate erased persons ("former user").
- Audit trail views show names resolved *at display time*; the registry keeps name history
  (for "who was person:x at the time") as long as retention allows.
- Code review rule: a new event field holding names, emails, phone numbers etc. is a defect.
- A future `limtool` check could scan event schemas for suspicious field names.
