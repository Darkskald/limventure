---
title: "Data integrity: ALCOA+ and regulator expectations"
summary: "ALCOA+ definition (MHRA, WHO, PIC/S), metadata and true copies, audit-trail review, electronic-signature expectations and data review as stated in MHRA 2018 and companion guidance."
tags: [lims, data-integrity, alcoa, mhra, pic-s, who, fda, audit-trail]
status: draft
sources:
  - https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/687246/MHRA_GxP_data_integrity_guide_March_edited_Final.pdf
  - https://picscheme.org/en/news/adoption-and-entry-into-force-of-pics-guidance-on-good-pract
  - https://www.who.int/publications/m/item/annex-4-trs-1033
  - https://www.fda.gov/media/119570/download
  - https://www.ema.europa.eu/en/human-regulatory-overview/research-development/compliance-research-development/good-manufacturing-practice/guidance-good-manufacturing-practice-good-distribution-practice-questions-answers
updated: 2026-10-28
---

# Data integrity: ALCOA+ and regulator expectations

Primary texts: MHRA *GXP Data Integrity Guidance and Definitions* rev. 1 (March 2018),
PIC/S PI 041-1 (in force 1 July 2021), WHO TRS 1033 Annex 4 (2021), FDA *Data
Integrity and Compliance With Drug CGMP — Q&A* (Dec 2018), EMA GMP Q&A.

## ALCOA+

MHRA 2018: ALCOA = **A**ttributable, **L**egible, **C**ontemporaneous, **O**riginal,
**A**ccurate; "+" = **Complete, Consistent, Enduring, Available**. "There is no
difference in expectations regardless of which acronym is used." The draft EU GMP
Chapter 4 (2025) reportedly adds *Traceable* (ALCOA++); unconfirmed final text.

## Key concepts (MHRA 2018)

- **Metadata** give data context and meaning and "form an integral part of the
  original record" (e.g. analyst, date, units, batch).
- **Raw data**: original records incl. metadata and all subsequent transformations
  allowing full reconstruction of the GXP activity.
- **True copies** of electronic data must include meaning (date formats, context,
  e-signatures) and the full GXP audit trail.
- **Retention** must include raw data, metadata, audit trail, result files, *variable
  system configuration settings specific to each record*, and processing runs
  (incl. methods) necessary to reconstruct the data set.
- Metadata are captured only when the user saves to durable storage — an
  e-signature may be needed for the record to become permanent.

## Audit trail (MHRA 6.13)

- Who/what/when/**why**; must not obscure or overwrite the original; time and time
  zone; reason for change recorded.
- Audit trail switched on; users cannot amend or disable it; admin changes recorded.
- Review need not include every system activity (log-on/off, keystrokes).
- Review may be a list or "exception reporting" via a **validated search tool**.
- FDA 2018 Q&A: audit-trail review frequency follows the data review it supports
  (e.g. before batch release); aborted/incomplete runs must be captured and justified.

## Electronic signatures (MHRA 6.14)

- Attributable to an individual; the signing act recorded so it "cannot be altered or
  manipulated without invalidating the signature or status of the entry".
- Signature manifestation: who, title, date (and time if significant), meaning.
- An inserted signature image or a "signed electronically" footnote is **not adequate**.
- PDF/paper copies must keep the signature metadata.
- Advanced electronic signatures to be considered where risk assessment requires.

## Data review (MHRA 6.15)

- Documented procedure; positive statement whether issues found; date; reviewer
  signature; corrections keep original visible.
- Customised reports may embed key actions if validated and **locked**.

## Governance

PIC/S PI 041-1: data integrity is the extent data are complete, consistent and
accurate across the lifecycle; applies to paper, electronic and hybrid systems and to
outsourced activities. WHO TRS 1033 Annex 4 replaced TRS 996 Annex 5 (2016).

## Own conclusions (not from sources)

| ALCOA+ attribute | Event-sourced realisation |
|---|---|
| Attributable | Authenticated principal + on-behalf-of in every event envelope |
| Legible | Rendered history view in business language; export to PDF/CSV |
| Contemporaneous | Server timestamp at append; separate "observed at" for bench time |
| Original | First event is the original; never mutated |
| Accurate | Validation in command handlers; instrument capture over typing |
| Complete | No delete; failed/aborted runs are events too |
| Consistent | Monotonic per-stream sequence, global ordering, UTC |
| Enduring | Archive-grade storage, format migration plan, hash chain |
| Available | Projections rebuildable; retention-aware archival tier |

"Configuration settings specific to each record" ⇒ events must reference the exact
config/spec/method **version** they were evaluated under.
