---
title: "Regulation: EU GMP Annex 11 (computerised systems)"
summary: "EU GMP Annex 11 (2011) clauses relevant to LIMS — risk management, suppliers, validation, accuracy checks, audit trail, security, e-signature, batch release, archiving — plus the 2025 draft revision."
tags: [lims, regulation, eu-gmp, annex-11, pic-s, audit-trail, e-signature]
status: draft
sources:
  - https://health.ec.europa.eu/system/files/2016-11/annex11_01-2011_en_0.pdf
  - https://gmp-compliance.org/gmp-news/drafts-of-eu-gmp-guideline-annex-11-annex-22-and-chapter-4-released-for-comment
  - https://www.lachmanconsultants.com/2025/08/eu-gmp-annex-11-whats-changing-in-the-2025-draft-concept-paper/
  - https://www.ema.europa.eu/en/human-regulatory-overview/research-development/compliance-research-development/good-manufacturing-practice/guidance-good-manufacturing-practice-good-distribution-practice-questions-answers
updated: 2026-10-28
---

# Regulation: EU GMP Annex 11

EudraLex Vol. 4, Annex 11 "Computerised Systems", revision 1, in operation since
30 June 2011. Adopted equivalently by PIC/S. Principle: "The application should be
validated; IT infrastructure should be qualified." Replacing a manual operation must
not decrease quality or increase overall risk.

## Clause digest

| § | Topic | LIMS-relevant essence |
|---|---|---|
| 1 | Risk management | Extent of validation and data-integrity controls based on documented risk assessment |
| 2 | Personnel | Process owner, system owner, QP, IT cooperate; defined responsibilities |
| 3 | Suppliers | Formal agreements; risk-based supplier audit; review COTS docs against URS |
| 4 | Validation | Lifecycle docs; system inventory; URS traceable; test parameter/data limits and error handling; migration checks (4.8) |
| 5 | Data | Built-in checks for electronic data exchange |
| 6 | Accuracy checks | Manually entered critical data need second check (person or validated electronic means) |
| 7 | Data storage | Protect, check readability; backups with tested restore |
| 8 | Printouts | Clear printouts; for batch-release records, printouts indicating changes since original entry |
| 9 | Audit trails | Risk-based; record all GMP-relevant changes and deletions; **reason documented**; intelligible form; regularly reviewed |
| 10 | Change/config management | Controlled changes incl. configuration |
| 11 | Periodic evaluation | Confirm valid state; incidents, upgrades, security |
| 12 | Security | Access control; record grant/change/revoke; record identity of operators entering, changing, confirming or deleting data with date/time |
| 13 | Incident management | All incidents assessed; root cause → CAPA |
| 14 | Electronic signature | Same impact as handwritten within the company; **permanently linked to record**; include time and date |
| 15 | Batch release | Only Qualified Persons certify; identify and record the person; via e-signature |
| 16 | Business continuity | Documented, tested fallback |
| 17 | Archiving | Archived data checked for accessibility, readability, integrity; retrieval tested after system changes |

## 2025 draft revision (status: consultation, not final)

- EU Commission consultation opened 7 July 2025 on revised Chapter 4 (Documentation),
  revised Annex 11 and new Annex 22 (AI); comments closed 7 October 2025.
- Draft Annex 11 grows from 5 to ~19 pages; dedicated sections on security, identity
  and access management, audit trails, e-signatures; scope extended to cloud services
  and static AI/ML models (secondary-source summaries).
- Draft Chapter 4 codifies data-integrity principles (ALCOA++ per secondary sources).
- **Adoption status unverified as of 2026-10-28** — re-check before relying on it.

## EMA Q&A

EMA's GMP/GDP Q&A pages include a data-integrity section applying to paper and
electronic systems; to be read with EudraLex Vol. 4.

## Own conclusions (not from sources)

- §9 "reason for change" ⇒ every correcting command needs a mandatory `reason` field
  (free text + optional controlled code), stored *in* the event, not in a side table.
- §8.2 "printouts indicating if data changed" ⇒ CoA/report renderer needs access to
  the change history of every printed value — trivial with events, hard with CRUD.
- §14 "permanently linked" aligns with Part 11 §11.70; one design can satisfy both.
- Expect the revised Annex 11 to tighten audit-trail review and IAM; design for the
  draft now (it is the direction of travel) and make strictness configurable.
