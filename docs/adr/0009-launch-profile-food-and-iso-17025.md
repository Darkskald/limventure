---
title: "ADR-0009: Launch profile is food + ISO/IEC 17025"
summary: The first shipped regulatory profile covers food testing labs (ISO/IEC 17025, IFS/BRCGS/HACCP); GxP follows as second profile on the ADR-0003 baseline; clinical is not in scope for launch.
tags: [adr, regulation, compliance, scope, iso-17025, food]
status: accepted
updated: 2026-10-28
---

# ADR-0009: Launch profile is food + ISO/IEC 17025

## Context

[ADR-0003](0003-compliance-baseline-and-regulatory-profiles.md) separates a fixed compliance
baseline from per-tenant profiles. Which profiles ship first decides signature ceremony,
validation effort and data-privacy design. Comparison:
[regulatory profiles](../knowledge/lims/regulatory-profiles-comparison.md).

## Decision

- **Launch profile:** food testing — [ISO/IEC 17025](../knowledge/lims/regulation-iso-17025.md),
  [IFS/BRCGS/HACCP](../knowledge/lims/regulation-food-safety-ifs-brc-haccp.md). Reference scenario:
  [margarine incoming inspection](../domain/examples/margarine-incoming-inspection.md).
- Signatures in this profile: authenticated approval with meaning (lab head sign-off,
  counter-signature on rejection) — **not** the full Part 11 two-component ceremony.
- **Second profile:** GxP EU/US (Annex 11, 21 CFR Part 11). The core baseline must not
  preclude it: signature records bound to record version + content hash from day one.
- **Clinical** (ISO 15189 / CLIA): not in scope for launch — see open point.

## Alternatives considered

| Option | Pros | Cons |
|---|---|---|
| Food + 17025 (this) | Fastest path to value, light signatures, no patient data | GxP customers must wait |
| + GxP at launch | Bigger market early | Validation package, Part 11 ceremony, dedicated SaaS ops from day one |
| + clinical | Largest scope | Patient data, HL7/FHIR, IVDR — would dominate the design |

## Consequences

- Shared SaaS mode is usable for all launch tenants (ADR-0004 restricts only GxP).
- Every signature-related feature is built against the GxP requirements in mind but only the
  17025 ceremony is shipped — GxP gaps are tracked as requirements, not hacks.

## Open points

- Clinical: ruled out permanently or just "not now"? Determines whether personal data must be
  kept out of core event payloads from the start.
