---
title: architecturekit relevance for the LIMS
summary: Own conclusions on how architecturekit fits the event-sourced LIMS - tenancy, audit attribution, integration events, scripting hooks, read models and adoption risks.
tags: [architecturekit, rust, lims, multi-tenancy, audit-trail, integration-events, assessment]
status: draft
sources: [https://docs.rs/architecturekit/0.21.0, https://github.com/thenativeweb/architecturekit-rust, https://github.com/thenativeweb/architecturekit-golang]
updated: 2026-10-28
---

# Relevance for the LIMS

**Everything below is own conclusion**, derived from the facts in the other
notes of this folder; nothing here is a statement of the library authors.

## Fit

Good fit for the write side: decider pattern, optimistic concurrency,
immutable derived schemas, upcasters and hash/signature verification match
the LIMS needs for an immutable, verifiable audit trail (GxP / 21 CFR Part 11
style). The read side is a thin skeleton: we will implement our own
persistent views (`TransactionalProjection` over Postgres or similar).

## Multi-tenancy

- Put the tenant first in every subject:
  `SubjectScheme::new("/tenants/{tenant_id}/samples/{sample_id}")`.
- Per-tenant projections via `Subjects::tree("/tenants/acme")`; global ones
  via `Subjects::tree("/tenants")` with `SubjectScheme::value(..)` to route.
- The kit enforces nothing: tenant checks belong in the axum extractor (who
  is the caller) and in command construction (subject built from the
  authenticated tenant, never from the request body).
- Separate ESDB instances per tenant remain possible (one `Store` each).

## Audit metadata and actor attribution

- The kit writes **no metadata** besides `source`, `subject`, `type`, `data`
  (`traceinfo: None`). ESDB records `time`, `id`, hash.
- Therefore actor, on-behalf-of, reason-for-change, e-signature references
  and client/instrument ids **must live in event data**. Proposal: a shared
  nested `Schema`-derived struct (e.g. `Audit { actor, reason, signature_id }`)
  embedded in every event type; the decider copies it from the command.
- Use `source` per deployment/service, not per user.
- Distributed tracing on write would need an upstream change or bypassing
  `Store::write` with the raw client.

## Integration events

- Domain events stay internal; integration events (to ERP, instruments,
  notification) via **resumable projections** that publish with at-least-once
  delivery and event id as idempotency key (Go "Publishing Events").
- Systems allowed to read ESDB can observe directly.

## Scripting / customer hooks

- No hook mechanism exists. Natural extension points: (a) inside deciders
  (pre-commit validation scripts, must be deterministic and get time via an
  injected clock), (b) as projections (post-commit reactions, async).
- Scripts must never run inside `State::evolve` (replayed on every load).

## Identifiers and constraints

- Uniqueness across subjects (barcodes, external sample ids) via
  `Precondition::require(is_eventql_query_true(..))`, validating values
  before interpolation; or via a lookup view checked in the decider.
- 64-bit integers > 2^53 as strings (ESDB stores numbers as f64).
- Long streams (instruments, stability studies): use `from_latest()` with
  periodic "snapshot" events.

## Risks

- **Maturity**: 22 breaking releases in ~28 h, ~200 downloads, single
  vendor, no changelog. Pin `=0.21.0`, keep an anti-corruption layer
  (own `Command`/event modules, thin adapter around `Store`), budget for
  upgrades or a fork.
- Tight coupling to `eventsourcingdb` client 4.x types in the public API.
- Tokio + `log` only; we need a `tracing`-to-`log` bridge.
- Licensing of EventSourcingDB itself (not of the kit, MIT) needs separate
  review (see the eventsourcingdb knowledge notes).
