---
title: "Core module: instruments, calibration, reagents, inventory, training"
summary: "Expected functions for instrument/equipment management and calibration lock-out, reagent and standard lifecycle, inventory, and personnel training/competency gating."
tags: [lims, module, instrument, calibration, reagent, inventory, training]
status: draft
sources:
  - https://www.limswiki.org/index.php/LII:LIMSpec/Maintaining_Laboratory_Workflow_and_Operations
  - https://www.limswiki.org/index.php/LII:LIMSpec/Primary_Laboratory_Workflow
  - https://www.agilent.com/cs/library/whitepaper/public/5994-9418EN_led_1058_whitepaper.pdf
  - https://www.spectroscopyonline.com/where-are-we-now-usp
  - https://law.resource.org/pub/us/cfr/ibr/inc/iec/iec.17025.2017.pdf
  - https://www.law.cornell.edu/cfr/text/21/211.25
  - https://www.law.cornell.edu/cfr/text/21/11.10
  - https://ask.ifas.ufl.edu/publication/FS143
updated: 2026-10-28
---

# Core module: instruments, reagents, inventory, training

## Instruments and equipment (LIMSpec §10)

- Track usage and time, reservations/planning (10.1, 10.2, 10.4); online/offline
  manually or scheduled (10.3).
- Multiple event types/frequencies per instrument; grouping by type/location (10.5, 10.6).
- Calibration/maintenance intervals in days–years, manual or automatic scheduling
  (10.7, 10.12); alerts before due dates (10.8).
- **Flag and block** instruments out of calibration, overdue, or under investigation
  (10.9); parent offline when a child component goes offline (10.14).
- Link calibrations to reference materials; unique IDs for instrument and components
  (10.11, 10.13); chronological log with performer and verifying signatures (10.15).
- ISO/IEC 17025 6.4/6.5: equipment records, calibration programme, metrological
  traceability. HACCP verification reviews calibration records (UF/IFAS FS143).
- USP <1058>: qualification effort by group A/B/C; see [gamp5-csv-csa.md](gamp5-csv-csa.md).

## Reagents, standards, consumables (LIMSpec §2, §3, §14, §15)

- Chain of custody and storage history for standards and reagents (2.1, 2.2).
- Only active items usable; authorized users can flag items unavailable (2.5, 2.6).
- Per test: lot, expiry, approval status recorded (3.1); only approved, unexpired
  items selectable; block items expiring during the test (3.2, 3.3).
- Inventory amounts and status (2.9); reorder points and stock (LIMSpec 15).
- Preparation of solutions from parent lots (traceability tree) — common requirement
  in titration labs (iodine value uses Wijs reagent and thiosulfate titrant).

## Training and competency (LIMSpec §7.7, §8)

- Personnel records incl. certifications, training, evaluations (8.1).
- Schedule training; track attendance, assessments, certificates (8.3, 8.5).
- Map tasks/sample types/methods to required training; **restrict tasks to qualified
  staff** (7.7, 8.8); training matrix (8.7).
- 21 CFR 211.25: personnel have education, training and experience for assigned
  functions; 21 CFR 11.10(i): users of e-record systems trained. ISO/IEC 17025 6.2:
  competence requirements, authorization of personnel for specific activities.

## Scenario illustration (margarine plant)

The iodine-value instrument (titrator or NIR) and IR spectrometer must be in
calibration at the moment of measurement; the analyst must be authorized for
both methods and for sensory evaluation (sensory panels often need periodic
competency checks). Expired Wijs solution blocks the test.

## Own conclusions (not from sources)

- "Fitness checks" (instrument calibrated, reagent valid, analyst trained, method
  effective) are **preconditions evaluated in the command handler** at the moment
  of `ResultRecorded`; the evaluated preconditions and their versions are stored in
  the event — gives the auditor proof that checks ran.
- Retroactive invalidation: if a calibration later fails, a query over events
  ("all results on instrument X since last good calibration") must be one projection
  away — event sourcing makes impact assessment cheap.
- Resource modules are good candidates for optional/replaceable modules (some
  customers keep calibration in a CMMS/QMS) — design for integration, not ownership.
