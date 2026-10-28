---
title: "Stakeholder: lab manager / lab head"
summary: "What lab heads and principals expect: multi-level review and approval, review-by-exception, workload and TAT visibility, disposition decisions with e-signature."
tags: [lims, stakeholder, lab-manager, approval, review-by-exception]
status: draft
sources:
  - https://www.limswiki.org/index.php/LII:LIMSpec/Primary_Laboratory_Workflow
  - https://www.law.cornell.edu/cfr/text/21/211.194
  - https://chromatographyonline.com/view/data-integrity-chromatography-laboratory-part-v-second-person-review
  - https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/687246/MHRA_GxP_data_integrity_guide_March_edited_Final.pdf
  - https://www.ey.com/en_us/insights/life-sciences/electronic-batch-records-improve-pharma-manufacturing
  - https://health.ec.europa.eu/system/files/2016-11/annex11_01-2011_en_0.pdf
  - https://limswiki.org/index.php/LII:LIMSpec_2022_R2
updated: 2026-10-28
---

# Stakeholder: lab manager / lab head

Responsible for result validity, release decisions, staffing and turnaround. In the
margarine scenario: the **lab head signs off** every release decision; on rejection
the **head of analytics counter-signs** (see [margarine example](../../domain/examples/margarine-incoming-inspection.md)).

## Review and approval

- **Multiple review levels** before release (LIMSpec 4.4); statuses approved / rejected /
  cancelled plus retest and re-sampling (LIMSpec 5.3).
- During approval the reviewer must see instruments, reagents, raw data and reports
  behind a result (LIMSpec 5.2) — not just the final number.
- US pharma: 21 CFR 211.194(a)(8) requires initials/signature of a **second person**
  showing the original records were reviewed for accuracy, completeness and compliance.
  LCGC commentary: the second reviewer must see the complete data set incl. aborted runs.
- MHRA 2018 §6.15: data review must be documented with a **positive statement** whether
  issues were found, the date, and the reviewer's signature; it includes a risk-based
  review of relevant audit-trail entries.

## Review by exception (RBE)

- MHRA 2018 §6.13: audit trails may be reviewed "by an 'exception reporting' process";
  an exception report is "a validated search tool" identifying predetermined abnormal
  data or actions.
- Autoverification of in-limit results is a LIMSpec requirement (4.2), but it "must be
  validatable and capable of rapid shutdown and revalidation" (4.7).
- Industry (EY on eBR) reports large review reductions when only flagged exceptions are
  reviewed; this presumes validated rules and processes (vendor/consultant claim).

## Operations visibility

- Workload by analyst/instrument, backlog, due dates; advance alerts for likely late
  turnaround or OOS (LIMSpec 6.3); scheduling and capacity planning (LIMSpec 28).
- Instrument availability, calibration due dates (LIMSpec 10.8, 10.10).
- Training matrix: who may run which method (LIMSpec 8.7, 8.8).

## Signatures on decisions

- Pharma batch certification: only Qualified Persons, via electronic signature
  (Annex 11 §15). Analogous role-gated signatures apply to the lab head in the scenario.
- Signature manifestation: name, date/time, meaning (21 CFR 11.50; see
  [regulation-21-cfr-part-11.md](regulation-21-cfr-part-11.md)).

## Own conclusions (not from sources)

- Approval inbox = prioritized list of *exceptions*; clean records batch-signable
  with one signature act (Part 11 continuous-session rules permit reduced re-entry,
  see 11.200(a)(1)(i)).
- Signature policies (who signs, how many, which conditions trigger a counter-signature
  such as "reject") must be **configuration per customer**, not code — the scenario's
  "counter-sign on rejection" is a typical conditional rule.
- RBE rules themselves are validated configuration and must be versioned; a result
  approved under rule v3 must record that it was rule v3.
