---
title: "ADR-0005: Integration events are persisted and audited"
summary: Integration events (inbound from and outbound to other systems) are stored in EventSourcingDB in their own namespace, separate from but as durable as domain events.
tags: [adr, integration-events, audit-trail, context-mapping]
status: proposed
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
- **Inbound**: the raw message is persisted as an integration event first (as received,
  with source), then an anti-corruption layer translates it into domain commands.
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
- Delivery guarantees (at-least-once + idempotency keys) must be designed.
