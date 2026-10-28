---
title: "ADR-0018: Specification pinned at order creation, binding and agreed limits"
summary: The applicable specification is resolved via configurable inheritance levels when the order is created and pinned as a snapshot; binding limits can never be overridden, agreed limits follow most-specific-wins.
tags: [adr, domain, specification, limits, order, iso-17025]
status: accepted
updated: 2026-10-28
---

# ADR-0018: Specification pinned at order creation, binding and agreed limits

## Context

Margarine judges against a catalog (material, supplier contract); OH number against customer
limits or a product specification (chat 2026-10-28). If the specification were resolved at
evaluation time, a catalog change between sampling and evaluation makes the verdict ambiguous.

## Decision

- The specification is **resolved when the [order](0016-analysis-order-is-a-core-aggregate.md)
  is created** and stored on the order as a **snapshot** of resolved limits, each with its
  source and version. Evaluation uses only this snapshot.
- Resolution follows **inheritance levels** (material, contract, sample kind, product, order
  override, …). Levels and precedence are tier-1 configuration per tenant, owned by QA,
  changed under audit ([ADR-0011](0011-extensibility-tiers.md)).
- Each limit has a **kind**:
  - **binding** (regulatory, company policy) — always applies, never overridden downstream;
  - **agreed** (contract, customer) — most specific level wins.
- "In spec" = all binding limits **and** the applicable agreed limits hold.
- Changing the specification of a running order is its own event with a reason (signature
  per regulatory profile). Loosening a binding limit is a deviation
  ([ADR-0019](0019-out-of-spec-results-open-a-deviation.md)), never configuration.

## Alternatives considered

| Option | Pros | Cons |
|---|---|---|
| Pinned snapshot, two limit kinds (this) | Unambiguous history; legal limits protected; source shown in reports | Versioned spec catalog from day one; non-trivial resolution logic |
| Resolve at evaluation time | Simple | Verdict depends on when it was evaluated |
| Pure override chain | Simple lookup | A customer contract could loosen a legal limit |

## Consequences

- "Which limits applied on date X?" is answered by one event.
- Reports can name the failing limit's source ("binding: Regulation (EC) 1881/2006").
- Feeds the ISO/IEC 17025 §7.8.6 decision rule (with measurement uncertainty,
  [ADR-0020](0020-replicates-and-acceptance-defined-by-method-version.md)).
