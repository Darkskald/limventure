---
title: "Stakeholder: QA/QC, compliance officer, auditor/inspector"
summary: "What QA, compliance officers and external auditors expect: complete audit trails, readable exports, access control evidence, deviation/CAPA linkage, validation state."
tags: [lims, stakeholder, qa, compliance, audit, inspection]
status: draft
sources:
  - https://health.ec.europa.eu/system/files/2016-11/annex11_01-2011_en_0.pdf
  - https://www.law.cornell.edu/cfr/text/21/11.10
  - https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/687246/MHRA_GxP_data_integrity_guide_March_edited_Final.pdf
  - https://www.fda.gov/media/119570/download
  - https://picscheme.org/en/news/adoption-and-entry-into-force-of-pics-guidance-on-good-pract
  - https://www.limswiki.org/index.php/LII:LIMSpec/Maintaining_Laboratory_Workflow_and_Operations
updated: 2026-10-28
---

# Stakeholder: QA/QC, compliance officer, auditor/inspector

QA owns the quality system; auditors (internal, certification body, accreditation
body, regulator) test whether records can be trusted. They rarely use the LIMS daily
but their requirements dominate the architecture.

## What they ask for during an audit / inspection

| Need | Basis |
|---|---|
| Accurate, complete copies in human-readable **and** electronic form | 21 CFR 11.10(b) |
| Audit trail of create/modify/delete with who/what/when/why, previous value kept | 11.10(e); Annex 11 §9; MHRA 6.13; LIMSpec 9.2–9.4 |
| Audit trail "convertible to a generally intelligible form and regularly reviewed" | Annex 11 §9 |
| Users cannot switch off/amend audit trail; admin changes recorded | MHRA 6.13 |
| Record of creation/change/cancellation of access authorisations | Annex 11 §12.3 |
| Printouts showing whether data changed since original entry (batch release) | Annex 11 §8.2 |
| System inventory, description of data flows and interfaces | Annex 11 §4.3 |
| Validation evidence, change control, periodic evaluation | Annex 11 §4, §10, §11 |
| Incident management feeding CAPA | Annex 11 §13 |
| Audit trail review frequency aligned with data review (e.g. before release) | FDA DI Q&A 2018 |

## Data governance view (PIC/S PI 041-1)

PIC/S PI 041-1 (in force 1 July 2021) defines data integrity as the extent to which
data are complete, consistent and accurate throughout the data lifecycle, and expects
manufacturers to assess systems for vulnerabilities. Hybrid (paper + electronic)
systems and outsourced activities are explicitly in scope. See
[data-integrity-alcoa-plus.md](data-integrity-alcoa-plus.md).

## Typical red flags inspectors look for (MHRA 2018 §6.16)

- Is this the only data generated for the activity (no hidden "trial" runs)?
- Indicators of unauthorised changes; IT requests to amend data after review.
- Shared accounts, admin rights held by lab users (conflict of interest).

## Food/ISO context

For ISO/IEC 17025 assessors and IFS/BRCGS auditors the focus shifts to traceability of
results to methods, equipment calibration, competence of staff, decision rules and
report content rather than Part 11 formalities. See
[regulation-iso-17025.md](regulation-iso-17025.md) and
[regulation-food-safety-ifs-brc-haccp.md](regulation-food-safety-ifs-brc-haccp.md).

## Own conclusions (not from sources)

- Provide an **auditor read-only role** with time-boxed access and its own audit
  trail of what was viewed — useful in SaaS where auditors cannot get DB access.
- "Show me the history of this result" must be answerable in one screen; the event
  stream is the natural source, but it must be rendered in business language, not as
  raw JSON events.
- Compliance evidence packs (config snapshot, user/role list, validation status,
  audit-trail review log) should be exportable per tenant on demand.
