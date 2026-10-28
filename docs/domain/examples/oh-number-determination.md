---
title: "Example: hydroxyl (OH) number determination in triplicate"
summary: Contrasting reference scenario — ordered analysis of a characteristic number (OH number) with aliquoting, triplicate measurement per ISO standard and action on deviation.
tags: [example, domain, aliquot, replicates, specification]
status: draft
updated: 2026-10-28
---

# Example: hydroxyl (OH) number determination

*Product owner's scenario, 2026-10-28. Stands for a whole family of titrimetric
characteristic numbers (acid, iodine, saponification, amine value, …).*

1. A customer announces a sample and orders the analysis. The requester can also be the
   company's own production.
2. The sample arrives, goes to the lab and is aliquoted.
3. The OH number is measured in triplicate according to an ISO standard.
4. The result is recorded; if it is off, action is taken.

## What this example stresses (own analysis)

| Aspect | Where |
|---|---|
| Explicit order by an external **or** internal requester | 1 |
| Announced sample (expected event, [ADR-0013](../../adr/0013-expected-events-are-facts.md)) | 1 → 2 |
| Derived samples (aliquots) with lineage | 2 |
| Standardised, versioned method; replicates aggregated to one reported result | 3 |
| Calculated result (titration volumes, blank, weight; possibly corrected by acid value) | 3 |
| Specification check and a deviation workflow | 4 |

## Contrast with the margarine scenario

[Margarine](margarine-incoming-inspection.md) is triggered by a delivery and ends in a
disposition of goods. Here the trigger is an order and the outcome is a result report to a
requester. Both share: announced sample, methods, specification check, action on deviation.

## Open

"Action taken if off" is unspecified: retest, OOS investigation, customer notification or disposition are all possible.
