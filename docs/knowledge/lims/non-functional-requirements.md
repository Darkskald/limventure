---
title: "Non-functional expectations: validation, security, performance, i18n, accessibility"
summary: "Cross-cutting LIMS expectations beyond features: validated state, security and IAM, availability/continuity, performance, internationalisation, accessibility (WCAG/EN 301 549), privacy."
tags: [lims, non-functional, security, performance, i18n, accessibility, availability]
status: draft
sources:
  - https://health.ec.europa.eu/system/files/2016-11/annex11_01-2011_en_0.pdf
  - https://law.resource.org/pub/us/cfr/ibr/inc/iec/iec.17025.2017.pdf
  - https://limswiki.org/index.php/LII:LIMSpec_2022_R2
  - https://www.w3.org/TR/WCAG22/
  - https://www.w3.org/WAI/policies/european-union
  - https://karlgroves.com/the-european-accessibility-act-and-b2b-software-what-internal-platforms-must-comply-with/
  - https://eur-lex.europa.eu/eli/reg/2016/679/oj
  - https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/687246/MHRA_GxP_data_integrity_guide_March_edited_Final.pdf
updated: 2026-10-28
---

# Non-functional expectations

## Validation and change

- Validated state maintained through lifecycle, periodic evaluation (Annex 11 §4, §11);
  configuration changes controlled (§10; ISO 17025 7.11.2).
- See [gamp5-csv-csa.md](gamp5-csv-csa.md).

## Security and IAM

- Access restricted to authorised persons; extent by criticality (Annex 11 §12.1–12.2);
  access grants/changes/revocations recorded (§12.3).
- Protected from unauthorized access, tampering and loss (ISO 17025 7.11.3).
- LIMSpec §34–36: system administration, cybersecurity, information privacy.
- Individual accounts, no shared logins; admin role segregated from lab role
  (MHRA 2018 §6.13 and data governance sections).
- Draft Annex 11 (2025) adds dedicated security and IAM sections (see
  [regulation-eu-annex-11.md](regulation-eu-annex-11.md)).

## Availability and continuity

- Business continuity arrangements documented and tested (Annex 11 §16).
- Backups with verified restore (§7.2); record system failures and corrective
  actions (ISO 17025 7.11.3(e)).

## Performance (no regulatory numbers; own guidance)

- Interactive bench actions (scan, save result) should feel instant (sub-second);
  legacy complaints centre on slow screens (see
  [legacy-ux-pain-points.md](legacy-ux-pain-points.md)).
- Release decisions are time-critical in the scenario (tanker waiting at gate).

## Internationalisation

- Multi-language UI, locale-specific number/date formats (decimal comma vs point is a
  data-integrity risk in result entry), time zones (MHRA: time and time zone where
  applicable), units of measure.
- Report languages per customer; bilingual CoAs are common in export trade.

## Accessibility

- WCAG 2.2 (W3C Recommendation) is the current web accessibility guideline.
- EU: EN 301 549 harmonised standard; W3C notes it includes WCAG 2.1 AA for web
  content. The European Accessibility Act (Directive 2019/882) applies since June
  2025 to listed consumer products/services; B2B lab software is mainly affected
  indirectly via public procurement and customer policies (Karl Groves analysis).
- Practical target (own view): WCAG 2.2 AA.

## Privacy

GDPR applies to personal data of users (audit trail identities), customers and, in
clinical settings, patients (special category, Art. 9). See
[event-sourcing-fit.md](event-sourcing-fit.md).

## Own conclusions (not from sources)

- Multi-tenant SaaS needs per-tenant: data residency choice, encryption keys, backup/
  restore granularity (restore one tenant without affecting others), rate limiting.
- On-prem parity: same binaries, offline-capable licence, documented hardening guide.
- Observability (logs/metrics) is separate from the GxP audit trail; never rely on
  technical logs as audit evidence and never put PII into them.
