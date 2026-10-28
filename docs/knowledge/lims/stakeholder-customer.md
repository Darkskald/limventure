---
title: "Stakeholder: customer / client / requester"
summary: "What external clients and internal requesters expect: online sample submission, status tracking, CoA/test reports with correct mandatory content, amended-report handling."
tags: [lims, stakeholder, customer, portal, coa, reporting]
status: draft
sources:
  - https://www.limswiki.org/index.php/LII:LIMSpec/Primary_Laboratory_Workflow
  - https://www.limswiki.org/index.php/Laboratory_information_management_system
  - https://www.law.cornell.edu/cfr/text/42/493.1291
  - https://www.iso.org/standard/66912.html
  - https://ilac.org/latest_ilac_news/revised-ilac-g8-published/
  - https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/687246/MHRA_GxP_data_integrity_guide_March_edited_Final.pdf
updated: 2026-10-28
---

# Stakeholder: customer / client / requester

The party that ordered the test: an external client of a contract lab, a hospital
clinician (clinical), or an internal department (production, purchasing, gate).

## Expectations

| Need | Detail | Source |
|---|---|---|
| Sample submission | Register samples before shipping (pre-login), via web or API | LIMSpec 1.1, 1.4 |
| Status tracking | Where is my sample, when are results due | own synthesis of LIMSpec 6.3 (TAT alerts) |
| Certificates of analysis | Generated only after verified approval | LIMSpec 6.5, 6.6 |
| Formats | PDF plus machine-readable (CSV/XML) | LIMSpec 6.2 |
| Amended reports | Clearly marked, changes and reasons shown | LIMSpec 6.9 |
| Conformity statements | When a pass/fail statement is requested, the decision rule must be agreed and reported | ISO/IEC 17025:2017 7.1.3, 7.8.6; ILAC G8:09/2019 |
| Clinical reports | Patient ID, lab location, report date, test, result with units, reference intervals; corrected reports promptly issued and originals retained | 42 CFR 493.1291(c),(d),(k) |

## Portal

LIMSwiki lists "supplier/vendor/customer management" among LIMS functions; a customer
web portal is standard in commercial contract-lab LIMS (market observation, not a
regulatory requirement).

## Data shared across organisations

MHRA 2018 §6.15: summary reports supplied between contract giver and acceptor "are
limited and critical supporting data and metadata may not be included"; the receiving
organisation should evaluate the data provider's data-integrity controls. Portals
offering access to underlying raw data and audit trail extracts reduce this gap.

## Scenario illustration (margarine plant)

Here the "customers" are internal: purchasing (price), production (release), and the
**gate control room**, which must be notified "without delay" to unload or send the
tanker away (step 11). Gate notification is a push integration, not a portal.

## Own conclusions (not from sources)

- A CoA is a **projection over signed, released events** with a frozen template version;
  re-rendering a historic CoA must reproduce the original byte-for-byte or be marked
  as a re-issue. Store the issued PDF (hash) as an artifact.
- Customer-facing data needs tenant **and** customer scoping (a contract lab is one
  tenant serving many customers) — a two-level isolation model.
- Notifications (email, webhook, SMS to gate) must be idempotent and must not be
  re-sent on event replay (see [event-sourcing-fit.md](event-sourcing-fit.md)).
