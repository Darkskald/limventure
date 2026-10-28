---
title: "ADR-0014: LIMS owns release decision and quality-based pricing"
summary: The LIMS decides on release and computes quality grade and bonus factor via a versioned tier-2 formula; ERP only consumes a published release event and executes payment.
tags: [adr, bounded-context, release, pricing, erp, integration-events]
status: accepted
updated: 2026-10-28
---

# ADR-0014: LIMS owns release decision and quality-based pricing

## Context

[Margarine example](../domain/examples/margarine-incoming-inspection.md), steps 5–7: release
by catalog, lab-head sign-off, counter-signature on rejection, price bonus by quality,
payment. Ownership between LIMS and ERP (SAP QM/MM/FI) determines bounded contexts.

## Decision

- **LIMS decides**: release/rejection (catalog = tier-1 configuration, signatures per
  regulatory profile).
- **LIMS computes** quality grade and bonus factor with a **tier-2 formula**
  ([ADR-0011](0011-extensibility-tiers.md)); the decision event references formula and catalog versions.
- **ERP executes**: it consumes the published event, e.g.
  `io.limventure.integration.release.delivery-released.v1 {deliveryRef, grade, bonusFactor, …}`
  or `delivery-rejected.v1`, and runs payment. No price logic is duplicated in the LIMS beyond the factor.
- **Variant**: a tenant may disable the bonus formula; the event then carries the grade only and
  pricing stays entirely in ERP. Same contract, optional field.

## Alternatives considered

| Option | Pros | Cons |
|---|---|---|
| LIMS decides + prices (this) | Lab logic stays in the lab, versioned and auditable formula | ERP integration must accept LIMS-computed factors |
| ERP decides (SAP QM usage decision) | Fits SAP-heavy plants | LIMS degrades to a measurement supplier; sign-off approves a proposal |
| LIMS decides, ERP prices | Clean commercial split | Covered by the variant above |

## Consequences

- A **release** capability (decision, sign-off, counter-signature, grade, bonus) is a core
  part of the LIMS domain model — candidate bounded context.
- The ERP contract is a published language ([ADR-0012](0012-out-of-process-extensions.md)) — versioned from day one.
- SAP QM-IDI customers expecting SAP to own the usage decision need an adapter that maps our
  decision onto the SAP usage decision (anti-corruption layer on their side or ours).
