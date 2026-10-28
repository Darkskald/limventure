---
title: "Validation: GAMP 5, CSV and CSA"
summary: "How regulated customers validate a LIMS: GAMP 5 (2nd ed.) risk-based lifecycle and software categories, FDA CSA (2025), supplier leverage, and implications for a configurable SaaS product."
tags: [lims, validation, gamp5, csv, csa, gxp, saas]
status: draft
sources:
  - https://ispe.org/publications/guidance-documents/gamp-5-guide-2nd-edition
  - https://intuitionlabs.ai/articles/gamp-5-categories-explained
  - https://public-inspection.federalregister.gov/2025-18468.pdf
  - https://www.hoganlovells.com/en/publications/fda-finalizes-computer-software-assurance-guidance-for-production-and-quality-system-software
  - https://health.ec.europa.eu/system/files/2016-11/annex11_01-2011_en_0.pdf
  - https://ispe.org/node/147362
  - https://www.agilent.com/cs/library/whitepaper/public/5994-9418EN_led_1058_whitepaper.pdf
updated: 2026-10-28
---

# Validation: GAMP 5, CSV and CSA

## GAMP 5 Second Edition (ISPE, July 2022)

- Risk-based lifecycle approach to compliant GxP computerized systems; second edition
  emphasises **critical thinking**, focusing effort on high-risk functions rather than
  documentation volume; new appendices on Agile, software tools, AI/ML, distributed
  ledgers, IT infrastructure (secondary summaries).
- Software categories (1 infrastructure, 3 non-configured, 4 configured, 5 custom;
  category 2 retired in GAMP 5) are "a continuum", not a checklist.
- A configurable LIMS is typically **Category 4**; customer-specific scripts/plugins
  push the affected parts toward **Category 5** (more testing, code review).
- Supplier involvement: leverage supplier documentation and testing where the supplier
  is assessed (consistent with Annex 11 §3, §4.5).

## FDA Computer Software Assurance (CSA)

- Final guidance *Computer Software Assurance for Production and Quality System
  Software*, September 2025 (CDRH/CBER; docket FDA-2022-D-0795); supersedes Section 6
  of *General Principles of Software Validation*. An update was reported in Feb 2026.
- Steps: identify intended use → determine risk (process risk / high-process-risk
  features) → select assurance activities (scripted, unscripted, exploratory testing)
  → establish appropriate record. Covers cloud (IaaS/PaaS/SaaS).
- Formally for medical-device manufacturers, but widely adopted as mindset in pharma.

## EU Annex 11 / ISO 17025 validation hooks

- Annex 11 §4: lifecycle validation, URS traceable, test of parameter limits and error
  handling, automated test tools assessed for adequacy (§4.7), migration verification.
- ISO/IEC 17025 7.11.2: validated incl. interfaces; configuration changes authorized,
  documented, validated before implementation.

## Instruments (USP <1058>)

USP <1058> AIQ: Group A (observe), B (calibrate), C (qualify computerized systems, e.g.
HPLC, MS). A draft revision retitles it *Analytical Instrument and System
Qualification* (AISQ). Instruments connected to the LIMS are qualified separately;
the interface is validated with the LIMS.

## Infrastructure / cloud

ISPE GAMP GPG *IT Infrastructure Control and Compliance* (2nd ed., 2017) covers cloud
and a building-block qualification approach. See
[stakeholder-it-admin.md](stakeholder-it-admin.md).

## Own conclusions (not from sources)

- The product should ship a **validation accelerator**: URS template mapped to features,
  risk assessment, traceability matrix, and the vendor's automated test evidence per
  release (Annex 11 §4.7 explicitly allows automated testing tools).
- Extensibility must be **risk-tiered**: (1) configuration via declarative models
  (Cat. 4, low validation cost), (2) sandboxed scripts/formulas (Cat. 4/5 boundary),
  (3) compiled plugins (Cat. 5). Customers should see which tier each customization
  belongs to.
- Event sourcing helps validation: deterministic replay of recorded event streams
  against a new release ("golden stream" regression tests) gives strong objective
  evidence that calculations and state transitions are unchanged.
- Configuration must itself be versioned, diffable, and promotable — config change =
  change control record.
