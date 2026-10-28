---
title: "Core module: reporting/CoA, scheduling/SLA, retention and archiving"
summary: "Expected functions for certificates of analysis and reports, workload scheduling and turnaround-time tracking, and record retention/archiving periods across regimes."
tags: [lims, module, reporting, coa, scheduling, sla, tat, retention, archiving]
status: draft
sources:
  - https://www.limswiki.org/index.php/LII:LIMSpec/Primary_Laboratory_Workflow
  - https://limswiki.org/index.php/LII:LIMSpec_2022_R2
  - https://law.resource.org/pub/us/cfr/ibr/inc/iec/iec.17025.2017.pdf
  - https://health.ec.europa.eu/system/files/2016-11/chapter4_01-2011_en_0.pdf
  - https://health.ec.europa.eu/system/files/2016-11/annex11_01-2011_en_0.pdf
  - https://www.law.cornell.edu/cfr/text/21/211.180
  - https://www.law.cornell.edu/cfr/text/42/493.1105
  - https://www.law.cornell.edu/cfr/text/21/11.10
updated: 2026-10-28
---

# Core module: reporting, scheduling, retention

## Reports and certificates of analysis

- CoA generated only after verified approval (LIMSpec 6.5, 6.6); standard and custom
  reports incl. chain-of-custody and QA reports (6.7, 6.8); CSV/XML/PDF (6.2).
- Amended/reissued reports clearly marked with changes and reasons (LIMSpec 6.9;
  ISO 17025 7.8.8 "Amendment to Report, serial number…").
- ISO/IEC 17025 7.8.2.1 mandatory content (a–p); conformity statements with decision
  rule (7.8.6); opinions by authorized persons only (7.8.7). See
  [regulation-iso-17025.md](regulation-iso-17025.md).
- Annex 11 §8: clear printouts; batch-release printouts show changes since entry.
- MHRA 2018: custom reports may embed key actions if validated and locked.

## Scheduling, workload, SLA / turnaround time

- LIMSwiki core phase: assignment, scheduling and tracking of samples and workload.
- LIMSpec §12 scheduled event management, §28 scheduling and capacity planning,
  §29 lean laboratory; advance alerts on likely late TAT (6.3).
- Typical SLAs: contract-lab TAT per test package and priority (routine/rush/stat);
  in-house: "release before the tanker's slot ends" (scenario step 11: notify the gate
  "without delay").

## Retention periods (examples, not exhaustive)

| Regime | Requirement |
|---|---|
| EU GMP Ch. 4 §4.11 | Batch documentation: 1 year after batch expiry or ≥ 5 years after QP certification, whichever longer |
| EU GMP Ch. 4 §4.12 | Critical data supporting the marketing authorisation (e.g. validation, stability raw data) kept while authorisation in force |
| 21 CFR 211.180 | Production, control and distribution records ≥ 1 year after batch expiry (special cases: 3 years after distribution for certain OTC) |
| 21 CFR 11.10(c),(e) | Records retrievable throughout retention; audit trail kept at least as long as the record |
| 42 CFR 493.1105 | CLIA: e.g. test records ≥ 2 years; reports ≥ 2 years after report date (longer for pathology, immunohematology) |
| ISO 17025 8.4 | Records retained per lab's own defined period, contractual and legal obligations |
| Food (IFS/BRCGS) | Typically product shelf life + defined period (standard-specific; verify) |

## Archiving

- Annex 11 §17: archived data checked for accessibility, readability and integrity;
  retrieval tested after system changes. §7: backups with tested restore.
- MHRA 2018: retention must include raw data, metadata, audit trail, configuration
  settings per record and processing runs.

## Scenario illustration (margarine plant)

"On rejection the record must be archived separately" (step 10) — e.g. longer
retention, legal hold for supplier dispute, export to a write-once archive.

## Own conclusions (not from sources)

- Retention is a **per-tenant policy over event streams** (by record type, outcome,
  legal hold); archiving moves sealed streams to a cold tier with hash manifest —
  never edits them.
- Report templates are versioned config; an issued report stores template version,
  data snapshot hash and rendered PDF hash. Re-rendering an old report must be
  deterministic or clearly marked as a re-issue.
- Deleting data at end of retention must itself be an auditable event (tombstone +
  deletion certificate), which conflicts with "append-only forever" — see
  [event-sourcing-fit.md](event-sourcing-fit.md).
- SLA timers are projections over timestamps; breaching should emit events that drive
  dashboards and escalations.
