---
title: "ADR-0012: Out-of-process extensions via published events and command API"
summary: Customers extend the LIMS with their own services that subscribe to published integration events and act only through the public command API — at launch, with versioned public contracts.
tags: [adr, extensibility, integration-events, api, contracts, versioning]
status: accepted
updated: 2026-10-28
---

# ADR-0012: Out-of-process extensions via published events and command API

Resolves the open point of [ADR-0011](0011-extensibility-tiers.md).

## Context

Tiers 1+2 (configuration, formulas) cannot express everything customers ask for, and
in-process plugins are deferred. Customer code outside our process is just another external
system — it does not enter our validation scope.

## Decision

- **Extensions are external services** (any language, customer-operated or hosted separately).
- **Input:** they subscribe to **published integration events** (published language,
  [ADR-0005](0005-integration-events-are-persisted.md)) — never to internal domain events.
- **Output:** they act only via the **public command API**, as a tenant-scoped **service
  principal** (`Actor` kind `system`), subject to the same authorization, regulatory-profile
  rules (reason, signatures) and audit as human users.
- **Delivery:** at-least-once, ordered per subject, with event ids for idempotency.
- **Contracts are public from day one:** published events and commands are versioned
  (`.vN` in the type), changes are additive within a version, breaking changes get a new
  version plus a deprecation period. Internal domain events stay free to change.
- **Not possible:** synchronous veto inside a transaction. Blocking rules are tier 1/2.

## Alternatives considered

| Option | Pros | Cons |
|---|---|---|
| Out-of-process at launch (this) | Arbitrary customer logic, core stays validatable, upgrade-safe | Public contract discipline from day one |
| Only later | Free to rename early | Weak extensibility at launch; contracts designed without pressure |
| In-process plugins instead | Synchronous hooks | Category 5 validation, upgrade breakage ([ADR-0011](0011-extensibility-tiers.md)) |

## Consequences

- Each bounded context defines its **published language** explicitly (ESDM: `published-language`
  context mapping); an anti-corruption layer separates it from internal events.
- Contract tests for published events and commands; a future `limtool` check can detect
  breaking schema changes between versions.
- Service principals need provisioning, credentials and per-tenant permissions.
- Strong dogfooding case for architecturekit projections (at-least-once delivery) — log
  friction under [upstream feedback](../upstream-feedback/architecturekit.md).
