---
title: "Stakeholder: data scientist / quality analyst"
summary: "What data and quality analysts expect: queryable historical results, SPC/control charts, OOT trending, method validation data, lab efficiency KPIs, clean exports."
tags: [lims, stakeholder, data-science, spc, trending, method-validation]
status: draft
sources:
  - https://limswiki.org/index.php/LII:LIMSpec_2022_R2
  - https://itl.nist.gov/div898/handbook/pmc/section1/pmc14.htm
  - https://en.wikipedia.org/wiki/Western_Electric_rules
  - https://database.ich.org/sites/default/files/ICH_Q2%28R2%29_Guideline_2023_1130.pdf
  - https://gmp-compliance.org/files/eca/userFiles/seminarpdf/ECA-Handling-OOE-OOT-Results.pdf
  - https://www.limswiki.org/index.php/LII:LIMSpec/Primary_Laboratory_Workflow
  - https://astrixinc.com/wp-content/uploads/2019/04/LIMS-Survey-Summary-Report-Final.pdf
updated: 2026-10-28
---

# Stakeholder: data scientist / quality analyst

Uses LIMS data *after* it is produced: supplier quality, process capability, method
performance, lab productivity. Often frustrated because legacy LIMS lock data in
proprietary schemas and report designers.

## Expectations

| Topic | Expectation | Source |
|---|---|---|
| Trending & control charts | Statistical trending and control charts are a LIMSpec functional area (§18) | LIMSpec 2022 R2 |
| SPC rules | Shewhart charts with Western Electric (WECO) rules and trend rules to flag out-of-control | NIST e-Handbook 6.1.4 |
| Rule trade-off | Combining rules raises sensitivity but also false alarms | Western Electric rules (summary) |
| OOT detection | Out-of-trend / out-of-expectation results handled distinctly from OOS; trend-based, may lead to preventive action | ECA OOE/OOT SOP material |
| Method validation | Data for accuracy, precision (repeatability, intermediate precision), specificity, LOD/LOQ, linearity, range | ICH Q2(R2) |
| In-house methods | Record validation data for new or modified methods | LIMSpec 7.6 |
| Exports | CSV/XML/PDF export of data | LIMSpec 6.2 |
| Lean lab / KPIs | Lean laboratory and continuous improvement; scheduling and capacity planning | LIMSpec 28, 29 |
| AI | "Artificial intelligence and smart systems" now a LIMSpec category | LIMSpec 30 |

## Typical analytical questions (scenario: sunflower oil)

- Iodine value per supplier over 24 months; Cpk against contract specification.
- Does IR-predicted value correlate with reference iodine-value instrument (method
  comparison, bias)?
- Rejection rate per supplier → input to supplier rating and contract negotiation.
- Turnaround from tanker arrival to gate notification; bottleneck analysis.

## Data requirements implied

- Results stored with **units, method version, specification version, instrument,
  analyst, timestamps** — otherwise trends are not comparable.
- Distinguish *reported* value vs *raw* value vs *rounded* value.
- Censored values ("< LOQ") need structured representation (LIMSpec 6.4 allows
  semi-quantitative reporting).

## Own conclusions (not from sources)

- Event sourcing is a strong fit: every state change is a timestamped fact, so
  process-mining (lead times, rework loops) comes almost for free from the event log.
- Provide an analytical read model (columnar/warehouse export, e.g. Parquet or a SQL
  projection) separate from operational projections; never let analysts query the
  event store directly in production.
- Bitemporal queries ("what did we know at release time?" vs "what is true now after
  correction?") are a frequent ask in investigations and are natural with events.
- SPC/OOT rule evaluation could run as a projection/subscriber that emits
  `TrendAlertRaised` events — making alerts themselves auditable.
