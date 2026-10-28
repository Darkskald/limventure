---
title: "Core module: OOS/OOT investigations, deviations, CAPA, stability studies"
summary: "Expected functions for out-of-specification and out-of-trend handling, deviations and nonconforming work, CAPA linkage, and ICH-style stability study management."
tags: [lims, module, oos, oot, deviation, capa, stability]
status: draft
sources:
  - https://www.fda.gov/regulatory-information/search-fda-guidance-documents/investigating-out-specification-test-results-pharmaceutical-production
  - https://www.law.cornell.edu/cfr/text/21/211.192
  - https://www.gov.uk/government/publications/out-of-specification-investigations
  - https://gmp-compliance.org/files/eca/userFiles/seminarpdf/ECA-Handling-OOE-OOT-Results.pdf
  - https://www.ema.europa.eu/en/ich-q10-pharmaceutical-quality-system-scientific-guideline
  - https://database.ich.org/sites/default/files/Q1A%28R2%29%20Guideline.pdf
  - https://www.law.cornell.edu/cfr/text/21/211.166
  - https://law.resource.org/pub/us/cfr/ibr/inc/iec/iec.17025.2017.pdf
  - https://health.ec.europa.eu/system/files/2016-11/annex11_01-2011_en_0.pdf
updated: 2026-10-28
---

# Core module: quality events and stability

## OOS (out of specification)

- FDA guidance *Investigating OOS Test Results for Pharmaceutical Production*, Rev. 1
  (May 2022, "Level 2 revision" of the 2006 guidance). Recommendations, but grounded
  in 21 CFR 211.192: documented investigation incl. conclusions and follow-up for any
  OOS, also for rejected batches.
- Phase I (laboratory investigation: obvious errors, analyst/supervisor assessment) →
  Phase II (full-scale, manufacturing + lab) → conclusions. MHRA guidance (gov.uk)
  describes phase I, II, III.
- OOS may not be invalidated as lab error without a demonstrable root cause; "testing
  into compliance" is unacceptable; averaging and outlier tests are restricted
  (2022 revision clarified outlier and averaging practices).
- Retest/resample rules must be predefined; originals always retained.

## OOT / OOE (out of trend / out of expectation)

- Not defined in US regulation; ECA's OOE/OOT SOP material and MHRA treat OOT as a
  result deviating from expected trend (typically stability; also in-process/raw
  materials), handled via trend analysis that may lead to preventive action.
- Needs statistical methods (regression, control charts, prediction intervals) — see
  [stakeholder-data-scientist.md](stakeholder-data-scientist.md).

## Deviations, nonconforming work, incidents

- ISO/IEC 17025 7.10: nonconforming work procedure (evaluate significance, halt work,
  withhold reports, notify customer, recall reports if needed).
- Annex 11 §13: all incidents reported and assessed; root cause of critical incidents
  forms the basis of CAPA.

## CAPA

- ICH Q10 (2008; FDA guidance 2009) lists the CAPA system as a pharmaceutical quality
  system element alongside process performance monitoring, change management and
  management review.
- LIMS typically links OOS/deviation records to CAPA in a QMS (eQMS) rather than
  owning CAPA fully; LIMSpec §16 "Investigation and quality management".

## Stability studies

- ICH Q1A(R2): long-term (e.g. 25 °C/60 % RH or 30 °C/65 % RH), intermediate
  (30 °C/65 % RH) and accelerated (40 °C/75 % RH) conditions; long-term pull points
  typically 0, 3, 6, 9, 12, 18, 24 months then annually; accelerated ≥ 3 points
  (0, 3, 6 months). ICH Q1D bracketing/matrixing reduces pulls. A consolidated ICH
  Q1 revision has been in progress (check status).
- 21 CFR 211.166: written stability testing programme.
- LIMS expectations: study protocol, conditions, chamber inventory, pull schedule
  auto-generating samples, results trending, shelf-life estimation, OOT detection.

## Scenario illustration (margarine plant)

A sunflower-oil sample failing the iodine-value limit triggers (a) a lab check
(Phase I: instrument, reagent, calculation), (b) on confirmed failure a *reject*
decision needing counter-signature by the head of analytics and special archiving,
(c) a supplier complaint/deviation in the QMS. Stability studies are less relevant
for incoming oil, but margarine shelf-life studies are a typical second use case.

## Own conclusions (not from sources)

- OOS is a **process manager / saga** triggered by `ResultEvaluated{status: OOS}`;
  its steps (phase I checklist, retest authorization, conclusion) are events on an
  investigation stream linked to the result stream.
- Invalidating a result = `ResultInvalidated{reason, investigationRef}`, never
  deletion; reports must show valid results while history shows everything.
- Stability pull schedules are time-driven commands — requires a reliable scheduler
  whose firing is itself recorded as an event (idempotent on replay).
- Decide early whether CAPA/deviation are in-product modules or integrations.
