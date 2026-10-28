---
title: "Regulatory regimes compared: inputs for configurable profiles"
summary: "Side-by-side comparison of GxP (Part 11, Annex 11), ISO/IEC 17025, food (HACCP/IFS/BRCGS) and clinical (ISO 15189/CLIA) on audit trail, signatures, review, reporting, validation and retention."
tags: [lims, regulation, profiles, comparison, configuration]
status: draft
sources:
  - https://www.law.cornell.edu/cfr/text/21/part-11
  - https://health.ec.europa.eu/system/files/2016-11/annex11_01-2011_en_0.pdf
  - https://health.ec.europa.eu/system/files/2016-11/chapter4_01-2011_en_0.pdf
  - https://law.resource.org/pub/us/cfr/ibr/inc/iec/iec.17025.2017.pdf
  - https://ascfoodsafety.com/brcgs-for-food-safety-changes-product-control/
  - https://www.law.cornell.edu/cfr/text/42/493.1291
  - https://www.law.cornell.edu/cfr/text/42/493.1105
  - https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/687246/MHRA_GxP_data_integrity_guide_March_edited_Final.pdf
updated: 2026-10-28
---

# Regulatory regimes compared

Details per regime: [Part 11](regulation-21-cfr-part-11.md),
[Annex 11](regulation-eu-annex-11.md), [ISO 17025](regulation-iso-17025.md),
[food](regulation-food-safety-ifs-brc-haccp.md),
[clinical](regulation-clinical-iso-15189-clia.md),
[data integrity](data-integrity-alcoa-plus.md).

| Dimension | Pharma GxP (Part 11 / Annex 11 / MHRA) | ISO/IEC 17025 | Food (HACCP, IFS, BRCGS) | Clinical (ISO 15189, CLIA) |
|---|---|---|---|---|
| Audit trail | Required (risk-based in Annex 11 §9), who/what/when/why, secure, reviewed | Amendments traceable, original kept (7.5.2) | Via 17025 principles for critical analyses; record keeping (HACCP) | 15189 7.6 data control; CLIA keep original + corrected reports |
| Reason for change | Mandatory for GMP-relevant data (Annex 11 §9) | "indication of altered aspects" (7.5.2) | Not explicit | Corrected report reason expected (practice) |
| E-signature | Formal: manifestation, linking, 2-component (Part 11 §11.50/70/200) | Identity of persons + authorizer (7.5.1, 7.8.2.1 o) | Authorized release | Authorized release; pathologist sign-out |
| Second-person review | 211.194(a)(8); MHRA 6.15 | Checking data and results recorded (7.5.1) | Typical, not prescribed | Technical supervisor review (practice) |
| Release role | QP for batch certification (Annex 11 §15) | Authorized report signatory | Positive release (BRCGS 5.7) | Lab director / authorized personnel |
| Decision rule | Specification-based; OOS procedure (211.192) | Documented decision rule with risk (7.8.6) | Specification limits | Reference intervals, critical values |
| Report amendments | Change visibility in printouts (Annex 11 §8.2) | "Amendment to Report…" (7.8.8) | Not explicit | Corrected report, keep both (493.1291(k)) |
| Validation | CSV/CSA, GAMP 5, Annex 11 §4 | 7.11.2 validate incl. interfaces | Reliable results; method validation | 15189 + CLIA method verification |
| Retention | Batch docs ≥ 1 y after expiry / ≥ 5 y after QP (EU Ch.4 §4.11) | Defined by lab/contract (8.4) | Shelf life + period (scheme-specific) | ≥ 2 y, pathology 10 y (493.1105) |
| Outsourced/SaaS | Agreements, supplier audit (Annex 11 §3) | Provider must comply (7.11.4) | Accredited subcontract labs | Similar via accreditation |

## Own conclusions (not from sources)

A **regulatory profile** is a named, versioned bundle of policies, e.g.:

- `audit.reason_required_for`: none | critical fields | all GMP-relevant changes
- `signature.mode`: simple-approval | part11 (re-auth, meaning, manifestation)
- `signature.reauth_in_session`: password-only | full
- `review.levels` and `review.second_person_required` per record type
- `release.role` and conditional counter-sign rules (scenario: on reject)
- `decision_rule.default`: simple acceptance | guard band
- `report.amendment_style`: 17025 | CLIA corrected-report
- `retention.policy` per record type and outcome
- `audit_trail.review_required_before_release`: bool
- `manual_entry.second_check`: none | second person | validated electronic

Profiles must be **composable** (a food plant with an accredited lab = food + 17025;
a pharma QC lab supplying the US and EU = Part 11 + Annex 11) with "strictest wins"
merge semantics, and **pinned per record** (the profile version in force when the
record was created/signed is stored on the record). Loosening a profile on live data
is itself a controlled, signed change.
