---
title: "ADR-0017: Container is a core aggregate separate from sample"
summary: The physical, labelled container is its own aggregate; samples relate to containers optionally (in-situ samples have none); the label identifies the container, not the sample.
tags: [adr, domain, container, sample, label, chain-of-custody]
status: accepted
updated: 2026-10-28
---

# ADR-0017: Container is a core aggregate separate from sample

## Context

Product owner experience with LES (chat 2026-10-28): whatever a "sample" means, it sits in
something physical that is tracked by its QR/barcode label. ISO/IEC 17025 §7.4.2 requires
unambiguous identification retained through sub-division and transfer
([ISO 17025](../knowledge/lims/regulation-iso-17025.md)); our research already concluded that
physical objects and logical samples must be modelled separately
([sample lifecycle](../knowledge/lims/core-modules-sample-lifecycle.md)).

## Decision

- **Sample** = identity of the test item: what was taken, from where, when, for which order.
- **Container** = physical vessel with label: labelled, filled, moved, stored, emptied,
  disposed. Its own aggregate and event stream.
- Sample ↔ container is **optional and many-to-many over time**: aliquots (new derived
  samples in new containers), pooled samples, transfers, container hierarchies (plate → wells).
  In-situ samples (inline NIR, probe, field) have no container.
- The **label identifies the container**. Printing/reprinting is an event. Pre-labelled
  customer barcodes are alias identifiers, unique per tenant ([ADR-0004](0004-multi-tenancy-from-day-one.md)).
- Container events are candidates for **published** events ([ADR-0012](0012-out-of-process-extensions.md))
  so an LES works on LIMS containers instead of keeping its own.

## Alternatives considered

| Option | Pros | Cons |
|---|---|---|
| Separate aggregate (this) | Physical tracking, scan-first UX, aliquots/pools/plates natural | One more aggregate; more events |
| Container as sample attribute | Simple 1:1 case | Breaks on aliquots, pools, re-used carriers, plates |

## Consequences

- Scan-first UX: scanning a label resolves container → sample → order → open tests.
- Every move is an event — watch the ESDB licensing cap ([backlog #6](../discussions/po-decision-backlog.md)).
- The 1:1 case (one sample, one container, label = sample id) must stay as cheap as today.
