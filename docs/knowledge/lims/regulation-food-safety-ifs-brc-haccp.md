---
title: "Regulation: food safety regimes (HACCP, IFS Food, BRCGS, EU food law)"
summary: "Food-sector regimes affecting a LIMS: Codex HACCP verification records, IFS Food v8 and BRCGS Issue 9 testing/release clauses, ISO 17025 for critical analyses, EU traceability."
tags: [lims, regulation, food, haccp, ifs, brcgs, gfsi]
status: draft
sources:
  - https://www.fao.org/fao-who-codexalimentarius/codex-texts/codes-of-practice/en/
  - https://ask.ifas.ufl.edu/publication/FS143
  - https://www.ifs-certification.com/en/news/ifs-food-version-8-audits-are-mandatory-from-1-january
  - https://www.tuev-nord.de/en/company/certification/services/ifs-food-version-8
  - https://ascfoodsafety.com/brcgs-for-food-safety-changes-product-control/
  - https://eur-lex.europa.eu/eli/reg/2002/178/oj
  - https://eur-lex.europa.eu/eli/reg/2017/625/oj
  - https://limswiki.org/index.php/LII:LIMSpec_2022_R2
updated: 2026-10-28
---

# Regulation: food safety regimes

The margarine scenario sits here. Food regimes are less prescriptive about software
than GxP, but demand traceability, documented testing programmes, reliable results,
and positive release.

## Codex HACCP (CXC 1-1969, rev. 2020)

- Codex General Principles of Food Hygiene, revised 2020 (first major overhaul in ~50
  years); clarified GHP vs HACCP, distinguished validation from verification; a 2022
  amendment added a CCP decision tree.
- HACCP principle: documentation and record keeping. Verification includes review of
  CCP monitoring records, corrective-action records and **calibration records**
  (UF/IFAS FS143).
- LIMS role: lab tests often serve as verification activities or as monitoring of
  prerequisite programmes (e.g. raw-material acceptance).

## IFS Food version 8

- Published April 2023; audits mandatory from 1 January 2024.
- Clause 5.6 "Testing and environmental monitoring": new requirement that
  environmental-monitoring criteria be documented, implemented and maintained based
  on risk (TÜV Nord summary). Testing plans cover internal and external analyses.
- Detailed sub-clause wording on lab accreditation not verified here — consult the
  standard text (available from ifs-certification.com).

## BRCGS Food Safety Issue 9

Per ASC Food Safety summary of Issue 9 (verify sub-clause numbers in the standard):
- 5.6 renamed "Product inspection, on-site product testing and laboratory analysis";
  "authenticity" added to the intent; a fundamental-type clause.
- Testing programme documents methods, sampling (incl. delivery to a lab), frequency
  and specified limits.
- Procedures must ensure reliability of lab results, using recognised methods where
  available.
- Analyses critical to safety, authenticity or legality: lab has recognised
  accreditation or operates to **ISO/IEC 17025** principles; justification documented
  where non-accredited methods are used.
- 5.7 Product release: positive release procedures where required.

## EU food law

- Reg. (EC) 178/2002 Art. 18: one-step-back / one-step-forward **traceability** of
  food and ingredients (supplier lot ↔ tanker ↔ production batch).
- Reg. (EU) 2017/625: official control labs must be accredited to ISO/IEC 17025
  (Art. 37). Private plant labs are not official labs but are often accredited anyway.

## LIMSpec

LIMSpec 2022 R2 §19 "Agriculture and food data management" (December 2022 update added
~30 food and beverage sources).

## Own conclusions (not from sources)

- A "food profile" = ISO 17025 + HACCP + IFS/BRCGS: needs audit trail and change
  reasons, but typically **no** Part 11-style e-signature ceremony — a simple
  authenticated approval suffices. Over-enforcing GxP friction would hurt UX.
- Supplier certificates (supplier CoA with tanker delivery) and incoming-goods
  inspection are core food use cases; link supplier lot, delivery note (DESADV),
  vehicle and sample in one traceability graph.
- Release-by-catalog (scenario step 9) is a specification + decision rule; the
  counter-signature on rejection is an internal policy, not a food-law requirement.
