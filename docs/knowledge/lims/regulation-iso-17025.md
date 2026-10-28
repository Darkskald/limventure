---
title: "Standard: ISO/IEC 17025:2017 (testing and calibration laboratories)"
summary: "ISO/IEC 17025:2017 clauses that drive LIMS design: item identification, technical records with amendment tracking, decision rules, report content, report amendments, and 7.11 LIMS control."
tags: [lims, regulation, iso-17025, accreditation, food, reporting]
status: draft
sources:
  - https://www.iso.org/standard/66912.html
  - https://law.resource.org/pub/us/cfr/ibr/inc/iec/iec.17025.2017.pdf
  - https://www.pjlabs.com/downloads/webinar_slides/4.20.2020_Doc-Control-Records.pdf
  - https://ilac.org/latest_ilac_news/revised-ilac-g8-published/
updated: 2026-10-28
---

# Standard: ISO/IEC 17025:2017

The accreditation basis for testing and calibration labs worldwide; the default
regime for food, environmental and many industrial labs. Unlike Part 11 it is
technology-neutral but explicitly names "laboratory information management
system(s)" in 7.11. (Text checked against the 2017 edition as incorporated by
reference and published by law.resource.org.)

## Clauses with direct LIMS impact

| Clause | Essence |
|---|---|
| 6.2 / 6.4 / 6.5 | Personnel competence records; equipment records and calibration; metrological traceability |
| 7.1.3 | If the customer requests a conformity statement, the specification and **decision rule** are clearly defined and agreed |
| 7.2 | Method selection, verification and validation; use latest valid version |
| 7.3.3 | Retain sampling records (plan, who, conditions, location, deviations) |
| 7.4.1 | Procedure for transport, receipt, handling, storage, retention, disposal/return of items |
| 7.4.2 | Unambiguous item identification retained while under lab responsibility; accommodate **sub-division** (aliquots) and transfer |
| 7.4.4 | Storage/conditioning conditions maintained, monitored, recorded |
| 7.5.1 | Technical records contain results, report and enough information to identify factors affecting the result and its uncertainty and to **repeat** the activity; date and identity of persons performing and checking; original observations recorded at the time |
| 7.5.2 | Amendments trackable to previous versions/original; **both original and amended data retained**, with date, altered aspect and person |
| 7.6 | Measurement uncertainty evaluated |
| 7.7 | Ensuring validity of results (QC samples, proficiency testing, trending) |
| 7.8.2.1 | Mandatory report content (a–p): title, lab, location, unique report ID with end marker, customer, method, item, receipt/sampling dates, performance dates, issue date, sampling plan ref, "results relate only to items tested", results with units, method deviations, authorizer, external-provider results flagged |
| 7.8.6 | Conformity statements: document decision rule incl. risk (false accept/reject); report which results, which specs met/not met, rule applied |
| 7.8.7 | Opinions/interpretations only by authorized personnel, clearly identified |
| 7.8.8 | Amendments: clearly identified, reason where appropriate; "Amendment to Report, serial number…"; replacement report uniquely identified with reference to original |
| 7.10 | Nonconforming work |
| 7.11.2 | LIMS **validated for functionality incl. interfaces** before introduction; changes incl. configuration authorized, documented, validated; COTS in designed range may be considered sufficiently validated |
| 7.11.3 | Protected from unauthorized access; safeguarded against tampering and loss; maintained for data integrity; record system failures and corrective actions |
| 7.11.4 | Off-site / external-provider (SaaS) LIMS: provider must comply with the standard's applicable requirements |
| 7.11.6 | Calculations and data transfers checked systematically |
| 8.4 | Control of records (retention, protection) |

## Decision rules (ILAC G8:09/2019)

ILAC-G8 guides labs, assessors and regulators on decision rules for 17025 conformity
statements, incl. simple acceptance (acceptance limit = tolerance limit) and guarded
bands based on measurement uncertainty.

## Own conclusions (not from sources)

- 7.5.2 is satisfied natively by an append-only event log, *if* the UI makes original
  vs amended values and the amending person visible.
- 7.8.6 means "pass/fail" logic is not a boolean on a spec limit: the spec must carry
  a **decision rule** (simple acceptance, guard band with uncertainty) — model it as a
  pluggable strategy per spec.
- 7.8.8 maps to report *versions* as first-class events (`ReportIssued`,
  `ReportAmended{reason, supersedes}`); the scenario's special archiving on rejection
  is a tenant-specific policy layered on top.
- 7.11.4 makes the SaaS vendor part of the customer's accreditation scope — expect
  supplier questionnaires and audit requests.
