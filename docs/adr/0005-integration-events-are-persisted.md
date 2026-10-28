---
title: "ADR-0005: Integration events are persisted and audited"
summary: Integration events (inbound from and outbound to other systems) are stored in EventSourcingDB in their own namespace, separate from but as durable as domain events.
tags: [adr, integration-events, audit-trail, context-mapping]
status: accepted
updated: 2026-10-28
---

# ADR-0005: Integration events are persisted and audited

## Context

LIMS cooperate with ERP, supplier portals, gate control, instruments (see
[margarine example](../domain/examples/margarine-incoming-inspection.md)). Auditors ask
"what did you receive, when, and what did you tell whom?". The product owner wants
integration events treated as persistently as domain events.

## Decision

- Two event type namespaces, e.g. `io.limventure.<context>.<event>` (domain) and
  `io.limventure.integration.<partner>.<event>` (integration). Exact scheme TBD with the model.
- **Inbound**: every received message is first recorded as an integration event, then an
  anti-corruption layer translates it into domain commands.
- **Raw payloads live outside the event store (agreed 2026-10-28).** The integration event
  carries metadata (partner, protocol, received-at, content type, size) and the **SHA-256 of
  the raw bytes**; the bytes go to a **write-once (WORM) blob store** (e.g. S3 Object Lock),
  keyed by hash. Reasons: ESDB's 64 KiB event limit, and personal data in raw messages must
  stay erasable ([GDPR](../discussions/gdpr-vs-immutable-log.md), ESDB-009).
- **Outbound**: domain events are translated into published-language integration events,
  persisted, then delivered (outbox semantics; delivery attempts are events too).
- Integration event contracts are versioned; they map to ESDM context mappings with
  External Systems.

## Alternatives considered

| Option | Pros | Cons |
|---|---|---|
| Persist both, separate namespace (this) | Full audit, replayable integrations | More events, storage, license cap |
| Domain events only, log integrations | Lean | Logs aren't audit-grade evidence |
| Same namespace | Simple | Couples external contracts to internal model |

## Consequences

- Free-tier event cap is reached faster — relevant for licensing.
- The blob store is audit-relevant: retention, backup, integrity checks (hash re-verification)
  and access control are in scope for validation. The same store serves instrument raw files,
  PDFs and other attachments.
- Erasing personal data means deleting/redacting a blob under a documented procedure; the
  event keeps the hash, so the evidence chain shows *that* something was received and erased.
- Delivery guarantees (at-least-once + idempotency keys) must be designed.

## Open points

- Local dev blob store (e.g. MinIO with object lock) in `infra/` — to be added with the first
  integration.
- Erasure vs WORM retention lock: legal-hold and retention periods per regulatory profile.
