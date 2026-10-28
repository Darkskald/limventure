---
title: "Core module: tests, methods, specifications, worksheets, results review"
summary: "Expected functions for test/analysis definitions, method versioning, specifications and decision rules, worksheets, calculations, result entry, review/approval and autoverification."
tags: [lims, module, test, method, specification, worksheet, review]
status: draft
sources:
  - https://www.limswiki.org/index.php/LII:LIMSpec/Primary_Laboratory_Workflow
  - https://www.limswiki.org/index.php/LII:LIMSpec/Maintaining_Laboratory_Workflow_and_Operations
  - https://law.resource.org/pub/us/cfr/ibr/inc/iec/iec.17025.2017.pdf
  - https://ilac.org/latest_ilac_news/revised-ilac-g8-published/
  - https://www.law.cornell.edu/cfr/text/21/211.194
  - https://database.ich.org/sites/default/files/ICH_Q2%28R2%29_Guideline_2023_1130.pdf
  - https://health.ec.europa.eu/system/files/2016-11/annex11_01-2011_en_0.pdf
updated: 2026-10-28
---

# Core module: tests, methods, specifications, worksheets

## Master data ("static data")

| Concept | Expectation | Source |
|---|---|---|
| Method / SOP | Approval, rejection, revision of sampling and test methods incl. limits and holding times; link each test to the SOP revision used | LIMSpec 7.4, 7.5 |
| Method validation | Record validation data for new/modified in-house methods; ICH Q2(R2) characteristics | LIMSpec 7.6; ICH Q2(R2) |
| Method version | Use latest valid version unless inappropriate; verify standard methods, validate non-standard | ISO 17025 7.2 |
| Specification | Limits per product/material/customer; results checked and exceedances flagged | LIMSpec 4.1, 4.6 |
| Decision rule | Documented decision rule incl. risk of false accept/reject | ISO 17025 7.8.6; ILAC G8 |
| Analysis / test | Components (analytes), units, rounding, calculations, data type | LIMSpec 3.9 |

## Worksheets and result capture

- Results per sample or per test, spreadsheet upload (LIMSpec 3.5, 3.6).
- Reagents/standards recorded per test with lot/expiry/status (3.1).
- Retests without loss of original (3.8); OOS alert at entry (3.12).
- Complete test record incl. performer and reviewer signatures (3.13).
- 21 CFR 211.194(a): complete data from all tests incl. graphs, charts, spectra;
  calculations shown; second-person review.
- Annex 11 §6: second check for manual critical entries; ISO 17025 7.11.6:
  calculations and data transfers checked systematically.

## Review and approval

- Full audit trail on modified results (LIMSpec 4.3); multi-level review (4.4).
- Autoverification of in-limit results (4.2), **validatable, rapidly switchable off**
  (4.7). See [stakeholder-lab-manager.md](stakeholder-lab-manager.md).

## Scenario illustration (margarine plant)

Product "refined sunflower oil, supplier contract X" has a specification with:
sensory (colour, turbidity, consistency — categorical pass/fail), iodine value
(numeric, units g I₂/100 g, limits), IR spectrum (file + derived values). The
"release strictly by catalog" is the specification evaluation plus a decision rule;
grades for the price bonus are additional specification bands. See
[margarine example](../../domain/examples/margarine-incoming-inspection.md).

## Own conclusions (not from sources)

- Specs, methods, calculations, decision rules and worksheet layouts are **versioned
  configuration aggregates** with their own lifecycle (draft → approved → effective →
  retired) and e-signed approval. Results reference the exact version.
- Calculations (formulas) are the riskiest customer extension: provide a sandboxed,
  deterministic expression language (no I/O, no clock) whose evaluation is
  reproducible on replay; store inputs, formula version and output in the event.
- Rounding, significant figures and "< LOQ" handling must be explicit, per analyte
  and per report, because pass/fail and trends depend on it.
- Specification bands beyond pass/fail (grades A/B/C) are common in food
  (price bonus) and should be generic, not a scenario-specific hack.
- Worksheet UX: generated from the test definition, with per-tenant layout overrides;
  avoid hand-built forms per method (legacy pain point).
