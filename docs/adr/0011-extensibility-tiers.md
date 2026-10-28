---
title: "ADR-0011: Extensibility tiers — configuration and formulas first"
summary: Launch extensibility is declarative configuration (tier 1) plus a sandboxed deterministic formula language (tier 2); in-process plugins (tier 3) are deferred until a stable, versioned extension interface exists.
tags: [adr, extensibility, customization, configuration, formulas, gamp5, validation]
status: accepted
updated: 2026-10-28
---

# ADR-0011: Extensibility tiers — configuration and formulas first

## Context

Extensibility is one of the three non-negotiable goals ([product vision](../vision/product-vision.md)).
Customer code inside the core collides with validation (GAMP 5 Category 5,
[GAMP 5 / CSA](../knowledge/lims/gamp5-csv-csa.md)) and with upgrades — customizations that
break on upgrade are a top legacy-LIMS complaint ([pain points](../knowledge/lims/legacy-ux-pain-points.md)).
Options discussed in [workflow vs scripts](../discussions/workflow-engine-vs-embedded-scripts.md).

## Decision

| Tier | What | At launch | Validation class |
|---|---|---|---|
| 1 | Declarative configuration: specifications, limits, decision catalogs, signature/review rules, routing, report templates, labels | **yes** | GAMP 4 (configured) |
| 2 | Sandboxed, deterministic formula language: derived results, price bonus/malus, custom checks | **yes** | GAMP 4/5 boundary, per formula |
| 3 | In-process plugins (WASM / Rhai hooks) | **no — deferred** | GAMP 5 (custom) |

Rules for tiers 1 and 2:

- Configuration and formulas are **event-sourced and versioned**; every domain event that
  used them references the exact version (MHRA "record-specific configuration").
- Formulas are **pure**: no I/O, no clock, no randomness — replay yields identical results.
- Each tenant's configuration is subject to change control per its regulatory profile.
- A customization request that tiers 1/2 cannot express is logged as a **gap**, not hacked —
  it drives the configuration model.

## Alternatives considered

| Option | Pros | Cons |
|---|---|---|
| Tiers 1+2 (this) | Validatable, upgrade-safe, forces a good config model | Some requests can't be served at launch |
| Tiers 1–3 at launch | Maximum flexibility | Customer code coupled to internals; every refactor breaks someone; Cat. 5 validation |
| Tier 1 only | Simplest | Calculations like the price bonus need core releases |

## Consequences

- The formula language choice (own DSL, CEL, Rhai in restricted mode, …) is a follow-up ADR.
- Tier 3 needs a stable, versioned extension interface first; its design can borrow the
  published-language contracts from [ADR-0005](0005-integration-events-are-persisted.md).

## Open points

- Out-of-process extensions (customer services consuming published events and calling the
  command API) — in scope for launch? See chat 2026-10-28.
