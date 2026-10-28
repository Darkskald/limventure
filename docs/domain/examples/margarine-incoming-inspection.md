---
title: "Example: incoming inspection of sunflower oil (margarine plant)"
summary: Reference scenario with several departments and IT systems — delivery notice, sampling, three analyses, catalog-based release, dual sign-off, pricing, gate notification.
tags: [example, domain, integration-events, release, e-signature]
status: accepted
updated: 2026-10-28
---

# Example: incoming inspection of sunflower oil

*Translated from the product owner's original German scenario (`beispiel.md`).*

We are a margarine manufacturer and look at the incoming-goods inspection of refined
sunflower oil. Framework contracts exist with several suppliers; tanker trucks with new oil
deliveries arrive at the plant regularly. Before the oil is released for production it is
analysed in the lab ("trust is good, control is better").

Several departments and several software systems talk to each other. The process:

1. The supplier announces the delivery electronically.
2. The tanker truck arrives at production.
3. A sample of the tank content is taken and sent to the lab by pneumatic tube.
4. The lab performs several analyses:
   1. Sensory examination (colour, turbidity, consistency).
   2. Iodine value measurement with an instrument.
   3. Infrared spectroscopy.
5. It is decided whether the delivery is released for production. If yes, the final price
   is calculated depending on raw-material quality (bonus for better quality) and the payment
   process is initiated.
6. The decision follows a strict catalog but must be **signed off by the lab head**.
7. If quality is too low and rejection is imminent, the **head of analytics must
   counter-sign** and the record must be **archived separately**.
8. The result is reported **immediately** to the control room at the gate and the truck is
   unloaded or sent away.

## What this example stresses (own analysis)

| Aspect | Where |
|---|---|
| Inbound integration event from supplier system | 1 |
| Expected event (truck expected, then arrives — or not) | 1 → 2 |
| Physical chain of custody (sample, pneumatic tube) | 3 |
| Manual vs instrument results, multiple methods per sample | 4 |
| Specification/catalog-based decision support | 5, 6 |
| Outbound integration events: pricing/payment (ERP), gate | 5, 8 |
| E-signature, four-eyes on negative outcome, retention class | 6, 7 |
| Time criticality / SLA (truck waiting) | 8 |
