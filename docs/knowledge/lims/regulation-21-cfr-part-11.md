---
title: "Regulation: FDA 21 CFR Part 11 (electronic records, electronic signatures)"
summary: "Key Part 11 controls relevant to LIMS design: closed-system controls, audit trails, signature manifestation, signature/record linking, two-component signatures, FDA scope narrowing."
tags: [lims, regulation, fda, part-11, e-signature, audit-trail, gxp]
status: draft
sources:
  - https://www.law.cornell.edu/cfr/text/21/part-11
  - https://www.law.cornell.edu/cfr/text/21/11.10
  - https://www.law.cornell.edu/cfr/text/21/11.50
  - https://www.law.cornell.edu/cfr/text/21/11.70
  - https://www.law.cornell.edu/cfr/text/21/11.200
  - https://www.fda.gov/regulatory-information/search-fda-guidance-documents/part-11-electronic-records-electronic-signatures-scope-and-application
  - https://public-inspection.federalregister.gov/2025-18468.pdf
updated: 2026-10-28
---

# Regulation: FDA 21 CFR Part 11

Applies to electronic records/signatures used to meet FDA **predicate rules** (e.g.
21 CFR 211 for drug CGMP). Structure: Subpart A general (11.1–11.3), B electronic
records (11.10–11.70), C electronic signatures (11.100–11.300).

## §11.10 Controls for closed systems (abridged)

| Clause | Requirement |
|---|---|
| (a) | Validation: accuracy, reliability, consistent intended performance, ability to discern invalid or altered records |
| (b) | Accurate, complete copies in human-readable and electronic form for FDA inspection |
| (c) | Protection of records for ready retrieval throughout retention period |
| (d) | Limit system access to authorized individuals |
| (e) | "secure, computer-generated, time-stamped audit trails to independently record the date and time of operator entries and actions that create, modify, or delete electronic records"; changes shall not obscure previous information; retained as long as the record |
| (f) | Operational system checks to enforce permitted sequencing of steps |
| (g) | Authority checks: only authorized individuals can sign, alter records, perform operations |
| (h) | Device checks for validity of data input source |
| (i) | Training/qualification of developers, maintainers, users |
| (j) | Written policies holding individuals accountable for actions under their e-signature |
| (k) | Controls over systems documentation, change control audit trail |

## Signature content and binding

- **§11.50 manifestation**: signed records show printed name, date and time, and
  **meaning** (review, approval, responsibility, authorship); these items are subject to
  the same controls as the record and appear in human-readable output.
- **§11.70 linking**: signatures must be linked to their records so they "cannot be
  excised, copied, or otherwise transferred to falsify an electronic record by ordinary
  means".
- **§11.100**: each signature unique to one individual, never reused or reassigned;
  identity verified before issuing.
- **§11.200(a)**: non-biometric signatures use at least two distinct components (e.g.
  ID + password). In one continuous session, the first signing uses all components,
  later signings at least one private component; outside a continuous session all
  components each time. Misuse must require collaboration of two or more persons.
- **§11.300**: ID/password uniqueness, periodic revision, loss management, transaction
  safeguards against unauthorized use, device testing.

## FDA interpretation

- **Scope and Application guidance (2003)**: FDA narrowed Part 11 scope and announced
  enforcement discretion for validation, audit trail, record retention and copying
  requirements — but predicate rules still apply and audit trails remain expected when
  needed for record trustworthiness.
- **CSA final guidance (Sept 2025)**: risk-based assurance for production and quality
  system software (device sector); see [gamp5-csv-csa.md](gamp5-csv-csa.md).

## Own conclusions (not from sources)

- 11.10(e) "independently record" ⇒ audit metadata must be system-generated (server
  clock, authenticated principal), never client-supplied.
- 11.70 is the hardest design point for e-signatures: a signature event must carry a
  **cryptographic hash of the signed content** (record state + meaning) so the binding
  is verifiable and a signature cannot be replayed onto another record version.
- Signature meaning must be a controlled vocabulary per tenant (e.g. "Reviewed",
  "Approved", "Counter-signed on rejection").
- 11.200 continuous-session rule allows batch signing with password re-entry only;
  re-authentication against an external IdP (OIDC step-up) is a common pattern.
