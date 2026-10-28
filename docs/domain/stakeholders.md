---
title: LIMS stakeholders overview
summary: Overview of LIMS stakeholder groups and external systems, their primary concerns, and links to the per-stakeholder knowledge files.
tags: [domain, stakeholders, lims]
status: draft
updated: 2026-10-28
---

# LIMS stakeholders overview

Derived from [knowledge/lims](../knowledge/lims/) research. Scenario references point to
the margarine incoming-inspection example ([margarine example](examples/margarine-incoming-inspection.md)).
Requirements per stakeholder: [requirements-catalog.md](requirements-catalog.md).

## Human stakeholders

| Stakeholder | Primary concerns | Scenario role | Knowledge file |
|---|---|---|---|
| Lab technician / analyst | Fast login and result entry, guided worksheets, no re-typing, instrument capture, clear "my work" queue | Receives tube sample, runs sensory, iodine value, IR | [stakeholder-lab-analyst.md](../knowledge/lims/stakeholder-lab-analyst.md) |
| Lab manager / lab head | Review & approval, review by exception, workload/TAT, release decisions with signature | Signs off release decision | [stakeholder-lab-manager.md](../knowledge/lims/stakeholder-lab-manager.md) |
| Head of analytics (senior approver) | Escalated decisions, counter-signatures, special archiving | Counter-signs rejection | [stakeholder-lab-manager.md](../knowledge/lims/stakeholder-lab-manager.md) |
| QA/QC, compliance officer, auditor | Audit trail, data integrity, validation state, inspection readiness, CAPA linkage | Audits release and rejection records | [stakeholder-qa-compliance.md](../knowledge/lims/stakeholder-qa-compliance.md) |
| Data scientist / quality analyst | Historical data access, SPC, OOT, supplier trends, method validation, lab KPIs | Supplier quality trends, bonus statistics | [stakeholder-data-scientist.md](../knowledge/lims/stakeholder-data-scientist.md) |
| Controller / billing | Price lists, invoicing (contract labs), cost allocation, quality-based price adjustments | Bonus price calculation → payment | [stakeholder-controller-billing.md](../knowledge/lims/stakeholder-controller-billing.md) |
| Customer / requester | Submission, status, CoA/report content, amendments, portal/API | Purchasing, production, gate control room | [stakeholder-customer.md](../knowledge/lims/stakeholder-customer.md) |
| IT / system owner / admin | Deployment (on-prem/SaaS), IAM, change control, backups, upgrades, validation support | Operates plant integrations | [stakeholder-it-admin.md](../knowledge/lims/stakeholder-it-admin.md) |

## External systems

| System | Typical exchange | Scenario | Knowledge file |
|---|---|---|---|
| ERP / SAP QM | Inspection lot in, results/usage decision out, price/payment follow-up | Delivery, release, bonus, payment | [integrations.md](../knowledge/lims/integrations.md) |
| MES / production | Release status, in-process samples | Oil released for production | [integrations.md](../knowledge/lims/integrations.md) |
| Instruments / CDS | Results and raw data (SiLA 2, OPC UA LADS, files) | Iodine value, IR spectrometer | [integrations.md](../knowledge/lims/integrations.md) |
| SDMS / ELN / LES | Raw data archive, experiment context | IR spectra archive | [integrations.md](../knowledge/lims/integrations.md) |
| Supplier / logistics (GS1 DESADV) | Delivery notice, supplier CoA | Electronic delivery notice | [integrations.md](../knowledge/lims/integrations.md) |
| Gate / yard management | Release/reject notification | Unload or send tanker away | [integrations.md](../knowledge/lims/integrations.md) |
| Pneumatic tube system | Transport events (vendor-specific) | Sample transport to lab | [core-modules-sample-lifecycle.md](../knowledge/lims/core-modules-sample-lifecycle.md) |
| QMS / eQMS | Deviations, CAPA, complaints, training | Supplier complaint on rejection | [core-modules-quality-events.md](../knowledge/lims/core-modules-quality-events.md) |
| Identity provider | SSO, step-up re-authentication for signatures | All users | [stakeholder-it-admin.md](../knowledge/lims/stakeholder-it-admin.md) |

## Regulatory regimes (configurable profiles)

| Regime | Knowledge file |
|---|---|
| Comparison / profile inputs | [regulatory-profiles-comparison.md](../knowledge/lims/regulatory-profiles-comparison.md) |
| FDA 21 CFR Part 11 | [regulation-21-cfr-part-11.md](../knowledge/lims/regulation-21-cfr-part-11.md) |
| EU GMP Annex 11 | [regulation-eu-annex-11.md](../knowledge/lims/regulation-eu-annex-11.md) |
| ALCOA+ / data integrity | [data-integrity-alcoa-plus.md](../knowledge/lims/data-integrity-alcoa-plus.md) |
| GAMP 5 / CSV / CSA | [gamp5-csv-csa.md](../knowledge/lims/gamp5-csv-csa.md) |
| ISO/IEC 17025 | [regulation-iso-17025.md](../knowledge/lims/regulation-iso-17025.md) |
| Food: HACCP, IFS, BRCGS | [regulation-food-safety-ifs-brc-haccp.md](../knowledge/lims/regulation-food-safety-ifs-brc-haccp.md) |
| Clinical: ISO 15189, CLIA | [regulation-clinical-iso-15189-clia.md](../knowledge/lims/regulation-clinical-iso-15189-clia.md) |

## Cross-cutting

- Core modules: [sample lifecycle](../knowledge/lims/core-modules-sample-lifecycle.md),
  [tests/specs](../knowledge/lims/core-modules-testing-specifications.md),
  [resources](../knowledge/lims/core-modules-resources.md),
  [quality events](../knowledge/lims/core-modules-quality-events.md),
  [reporting/retention](../knowledge/lims/core-modules-reporting-scheduling-retention.md)
- [Non-functional](../knowledge/lims/non-functional-requirements.md),
  [legacy UX pain points](../knowledge/lims/legacy-ux-pain-points.md),
  [event sourcing fit](../knowledge/lims/event-sourcing-fit.md)

## Tension map (own analysis)

| Tension | Between |
|---|---|
| Speed/low friction vs. signature and reason ceremony | Analyst ↔ QA |
| Per-customer customization vs. validated, upgradeable core | PO/customers ↔ IT/QA |
| Immutable history vs. erasure/retention deletion | QA ↔ privacy/IT |
| Continuous SaaS delivery vs. frozen validated versions | Vendor ops ↔ regulated customers |
| LIMS-owned vs. ERP-owned decisions (usage decision, pricing) | Lab ↔ ERP owners |
