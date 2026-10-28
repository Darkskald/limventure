---
title: "Stakeholder: IT, system administrator, system owner"
summary: "What IT and system owners expect: deployability on-prem and SaaS, identity integration, controlled configuration change, backups/restore, validation support, upgrade path."
tags: [lims, stakeholder, it, admin, deployment, validation, saas]
status: draft
sources:
  - https://health.ec.europa.eu/system/files/2016-11/annex11_01-2011_en_0.pdf
  - https://ispe.org/node/147362
  - https://docs.aws.amazon.com/whitepapers/latest/gxp-systems-on-aws/qualification-strategy-for-life-science-organizations.html
  - https://www.rdworldonline.com/the-cloud-meets-gmp-regulations-part-2-saas-and-qualified-it-infrastructure/
  - https://ispe.org/index.php/pharmaceutical-engineering/july-august-2026/continuous-operational-control-paas-gxp-environments
  - https://www.limswiki.org/index.php/LII:LIMSpec/Maintaining_Laboratory_Workflow_and_Operations
  - https://limswiki.org/index.php/LII:LIMSpec_2022_R2
  - https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/687246/MHRA_GxP_data_integrity_guide_March_edited_Final.pdf
updated: 2026-10-28
---

# Stakeholder: IT, system administrator, system owner

Annex 11 distinguishes the **process owner** (business process) from the **system
owner** (availability, maintenance, data security) and requires close cooperation with
QPs and IT (Annex 11 §2, glossary).

## Expectations

| Area | Expectation | Source |
|---|---|---|
| Supplier agreements | Formal agreements stating third-party responsibilities (hosting, remote support) | Annex 11 §3.1 |
| Supplier audit | Need for supplier audit based on risk; QMS info available to inspectors | Annex 11 §3.2, §3.4 |
| Change control | Configuration changes only in a controlled manner per procedure | Annex 11 §10 |
| Backups | Regular backups; restore ability checked during validation and periodically | Annex 11 §7.2 |
| Business continuity | Documented, tested fallback for system breakdown | Annex 11 §16 |
| Migration | Data not altered in value/meaning during migration | Annex 11 §4.8 |
| Archiving | Archived data remain accessible/readable; retrieval tested after system change | Annex 11 §17 |
| Access | Access authorisation changes recorded | Annex 11 §12.3 |
| Admin segregation | Admin actions on audit trail recorded; lab users should not hold admin rights | MHRA 2018 §6.13 |
| Platform functions | Configuration management, validation/commissioning, system administration, cybersecurity, privacy | LIMSpec 31–36 |

## SaaS and multi-tenancy

- ISPE GAMP *IT Infrastructure Control and Compliance* (2nd ed., 2017) covers IaaS/PaaS/SaaS
  and a platform/building-block qualification approach.
- Opinion is split on multi-tenant GxP SaaS: an R&D World article prefers single-tenant;
  others accept multi-tenant with audited security framework and extra security testing.
- Cloud providers update continuously; point-in-time infrastructure qualification is
  increasingly impractical (ISPE Pharmaceutical Engineering, 2026, PaaS article).
- Regulated customers still own validation for intended use even when the vendor
  qualifies infrastructure and application (shared responsibility, AWS GxP whitepaper).

## Integration ownership

IT owns interfaces to ERP, MES, instruments, identity (LDAP/AD, OIDC/SAML), e-mail,
printers/label printers. See [integrations.md](integrations.md).

## Own conclusions (not from sources)

- Same artefact for on-prem and SaaS (container images + declarative config); tenant
  config as versioned, signed bundles promotable DEV → TEST → PROD — this is what
  makes Annex 11 §10 change control cheap.
- Upgrade cadence is a contested decision: SaaS wants continuous delivery, regulated
  customers want frozen validated versions. Expect **release channels** (fast /
  validated-LTS) and vendor-supplied validation packages per release.
- Isolation options per tenant (shared schema, schema-per-tenant, DB/event-store per
  tenant, dedicated deployment) should be a deployment decision, not a code fork.
- Time synchronization (NTP, UTC storage, time-zone display) is an audit-trail
  prerequisite (MHRA: "time and time zone where applicable").
