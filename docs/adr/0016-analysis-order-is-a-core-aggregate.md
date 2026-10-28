---
title: "ADR-0016: Analysis order is a core aggregate"
summary: Every analysis belongs to an analysis order (requester, samples, tests, pinned specification); orders are created manually, by inbound events via inspection plans, or by schedules.
tags: [adr, domain, order, aggregate, tenancy]
status: accepted
updated: 2026-10-28
---

# ADR-0016: Analysis order is a core aggregate

## Context

Walkthrough of the [margarine](../domain/examples/margarine-incoming-inspection.md) and
[OH number](../domain/examples/oh-number-determination.md) scenarios (chat 2026-10-28,
[concept map](../domain/scenario-concept-map.md)). Margarine has no explicit order — the
delivery notice implies one; OH number has an explicit order from a customer or production.

## Decision

- The **analysis order** is its own aggregate, separate from the sample: who requests
  (external customer, internal cost center, system trigger), which samples, which tests,
  which specification ([ADR-0018](0018-specification-pinned-at-order-creation-with-binding-and-agreed-limits.md)).
- **No analysis without an order**, including ad-hoc tests.
- Orders are created by: a person, an **inspection plan** (tier-1 configuration reacting to
  an inbound integration event, e.g. a delivery notice), or a schedule.

## Alternatives considered

| Option | Pros | Cons |
|---|---|---|
| Order aggregate (this) | Uniform attribution, TAT, cost allocation, billing for every requester | One more aggregate; inspection-plan configuration |
| Order as part of the sample | Fewer concepts | One order spanning several samples is awkward; implicit orders stay invisible |

## Consequences

- Every result is traceable to a requester.
- Contract-lab mode ([backlog #5](../discussions/po-decision-backlog.md)) becomes a requester
  type, not a separate mode.
- Auto-created orders (margarine) must stay invisible to analysts unless they need them (UX).
- "Quick check without order" requires a fast order-creation path, or users will resent it.

## Open points

- Inspection-plan configuration model (matching rules on material, supplier, …).
