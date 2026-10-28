---
title: LIMS candidate requirements catalog
summary: Prioritized, ID'd candidate requirements (REQ-xxx) tagged with stakeholder, regulation and MoSCoW; all entries are candidates needing product-owner agreement.
tags: [domain, requirements, lims, moscow]
status: draft
updated: 2026-10-28
---

# LIMS candidate requirements catalog

> **Every entry is "candidate — needs PO agreement".** Nothing here is accepted scope.
> Sources and rationale: [stakeholders.md](stakeholders.md) and `docs/knowledge/lims/`.
> MoSCoW is a proposal from research, assuming food + pharma profiles at launch.

**Stakeholders:** AN analyst · LM lab manager/head · QA QA/compliance/auditor ·
DS data scientist · FIN controller/billing · CU customer · IT IT/admin · EXT external system.
**Regulation:** P11 21 CFR Part 11 · A11 EU GMP Annex 11 · DI MHRA/PIC/S/WHO data integrity ·
17025 ISO/IEC 17025 · FOOD HACCP/IFS/BRCGS · CLIN ISO 15189/CLIA · GAMP GAMP 5/CSA ·
GDPR · — none.

## Audit trail, data integrity, e-signature

| ID | Requirement | Stakeholder | Regulation | MoSCoW (candidate) |
|---|---|---|---|---|
| REQ-001 | Every state change is recorded as an immutable event with authenticated user, server UTC timestamp, previous/new value | QA | P11, A11, DI, 17025 | Must |
| REQ-002 | Changes to regulated data require a reason (free text + optional code), configurable per profile/field criticality | QA, AN | A11, DI | Must |
| REQ-003 | Human-readable audit-trail view and export (PDF/CSV) per record, in business language | QA | P11, A11 | Must |
| REQ-004 | Audit trail cannot be disabled or altered by any user incl. admins; admin config changes are themselves audited | QA, IT | DI | Must |
| REQ-005 | Electronic signature with manifestation (name, date/time, meaning) shown on screen and in reports | LM, QA | P11, A11, DI | Must |
| REQ-006 | Signature cryptographically bound to the signed record version (content hash); later change invalidates/supersedes | QA | P11 §11.70, A11 §14 | Must |
| REQ-007 | Part 11 signing mode: re-authentication with two components; continuous-session rules; step-up via IdP | LM, IT | P11 §11.200 | Must |
| REQ-008 | Configurable signature policies: required signers, roles, sequences, conditional counter-signature (e.g. on reject) | LM, QA | A11 §15, scenario | Must |
| REQ-009 | Audit-trail review workflow with exception report (validated rule set) and documented review record | LM, QA | DI, FDA DI Q&A | Should |
| REQ-010 | Tamper evidence for the event store (hash chain or signed checkpoints), verifiable on demand | QA, IT | DI | Should |
| REQ-011 | Every record references the config/spec/method/profile versions under which it was created and evaluated | QA, DS | DI, 17025 7.5 | Must |
| REQ-012 | Second check for manually entered critical data (second person or validated electronic check), per profile | AN, QA | A11 §6, 211.194 | Should |

## Regulatory profiles and multi-tenancy

| ID | Requirement | Stakeholder | Regulation | MoSCoW (candidate) |
|---|---|---|---|---|
| REQ-020 | Named, versioned regulatory profiles (food, 17025, GxP-EU, GxP-US, clinical) with composable "strictest wins" merge | QA, IT | all | Must |
| REQ-021 | Profile version pinned per record; profile changes are signed change-control events | QA | A11 §10, 17025 7.11.2 | Must |
| REQ-022 | Multi-tenant SaaS with tenant ID on every event, per-tenant encryption keys, no cross-tenant reads | IT | A11 §12, GDPR | Must |
| REQ-023 | Same product deployable on-prem and SaaS from identical artefacts | IT | — | Must |
| REQ-024 | Selectable isolation level per tenant (shared, dedicated store, dedicated deployment) | IT | A11 §3 | Should |
| REQ-025 | Second-level scoping for contract labs: customer within tenant | CU, IT | 17025 | Should |
| REQ-026 | Release channels: continuous vs validated long-term-support | IT, QA | GAMP | Should |

## Extensibility and configuration

| ID | Requirement | Stakeholder | Regulation | MoSCoW (candidate) |
|---|---|---|---|---|
| REQ-030 | Declarative configuration of sample types, fields, ID formats, lifecycles without code | LM, IT | GAMP (Cat. 4) | Must |
| REQ-031 | Configuration as versioned, diffable bundles promotable DEV→TEST→PROD with approval | IT, QA | A11 §10, 17025 7.11.2 | Must |
| REQ-032 | Sandboxed deterministic expression language for calculations and rules (no I/O), replay-safe | LM, DS | 17025 7.11.6, GAMP | Must |
| REQ-033 | Plugin/extension API with stable contracts surviving upgrades; extension risk tier visible | IT | GAMP (Cat. 5) | Should |
| REQ-034 | Customer-specific workflows (e.g. counter-sign + special archiving on rejection) via configuration | LM, QA | scenario | Must |
| REQ-035 | Event subscriptions/webhooks for customer integrations | IT, EXT | — | Should |

## Sample lifecycle

| ID | Requirement | Stakeholder | Regulation | MoSCoW (candidate) |
|---|---|---|---|---|
| REQ-040 | Pre-login of samples from external triggers (delivery notice, schedule, API) | AN, EXT | — | Must |
| REQ-041 | Unique sample IDs with configurable format; barcode label printing | AN | 17025 7.4.2 | Must |
| REQ-042 | Chain-of-custody events for each transfer incl. location/condition | AN, QA | 17025 7.4, LIMSpec | Must |
| REQ-043 | Aliquots/sub-samples with parent linkage; containers separate from samples | AN | 17025 7.4.2 | Must |
| REQ-044 | Receipt check against sampling requirements; rejection at receipt with reason | AN | 17025 7.4 | Should |
| REQ-045 | Storage location tracking and disposition record | AN, QA | 17025 7.4.1 | Should |

## Tests, specifications, results

| ID | Requirement | Stakeholder | Regulation | MoSCoW (candidate) |
|---|---|---|---|---|
| REQ-050 | Versioned methods, analyses, specifications with approval lifecycle | LM, QA | 17025 7.2, A11 | Must |
| REQ-051 | Specification evaluation with pluggable decision rules (simple acceptance, guard band) and grade bands | LM, CU | 17025 7.8.6, ILAC G8 | Must |
| REQ-052 | Generated worksheets from test definitions with per-tenant layout overrides | AN | — | Must |
| REQ-053 | Structured sensory/categorical results alongside numeric and file results | AN | FOOD | Must |
| REQ-054 | Retest/re-sample/invalidate without losing originals; reason mandatory | AN, QA | 211.192, 17025 7.5.2 | Must |
| REQ-055 | Immediate OOS flag at entry and notification | AN, LM | FDA OOS | Must |
| REQ-056 | Multi-level review and approval; review-by-exception inbox; batch signing | LM | 211.194, DI | Must |
| REQ-057 | Autoverification rules, validatable and instantly switchable off | LM, QA | LIMSpec 4.7 | Could |
| REQ-058 | Explicit rounding, significant figures, censored values (< LOQ) per analyte | AN, DS | 17025 | Must |

## Resources

| ID | Requirement | Stakeholder | Regulation | MoSCoW (candidate) |
|---|---|---|---|---|
| REQ-060 | Instrument register with calibration/maintenance schedule and lock-out when not fit | AN, LM | 17025 6.4, FOOD | Must |
| REQ-061 | Reagent/standard lots with expiry and status; block expired or unapproved | AN | 17025, LIMSpec 3.2 | Must |
| REQ-062 | Training/competency matrix gating who may perform which method/sign which step | LM, QA | 17025 6.2, P11 §11.10(i) | Should |
| REQ-063 | Impact query: all results affected by an instrument/reagent/analyst over a time span | QA, DS | DI | Should |
| REQ-064 | Inventory and reorder management | LM | — | Could |

## Quality events

| ID | Requirement | Stakeholder | Regulation | MoSCoW (candidate) |
|---|---|---|---|---|
| REQ-070 | OOS investigation workflow (phase I/II) linked to results | LM, QA | 211.192, FDA OOS | Should |
| REQ-071 | OOT detection via configurable statistical rules | DS, QA | MHRA OOS, ECA | Could |
| REQ-072 | Deviation/nonconforming-work records with link to external QMS/CAPA | QA, EXT | 17025 7.10, ICH Q10 | Should |
| REQ-073 | Stability study protocols, pull schedules, trending | LM, DS | ICH Q1A | Could |

## Reporting, retention, analytics

| ID | Requirement | Stakeholder | Regulation | MoSCoW (candidate) |
|---|---|---|---|---|
| REQ-080 | CoA/test report generation from released data with versioned templates and 17025 mandatory content | CU, LM | 17025 7.8.2, LIMSpec 6.5 | Must |
| REQ-081 | Report amendments as new uniquely identified versions referencing the original | CU, QA | 17025 7.8.8, CLIA | Must |
| REQ-082 | Issued report stored immutably (hash) and reproducible | QA | DI | Must |
| REQ-083 | Retention policies per record type/outcome, legal hold, auditable archival and deletion | QA, IT | EU GMP Ch.4, 211.180, CLIA | Must |
| REQ-084 | SPC/control charts and supplier trend dashboards | DS, LM | 17025 7.7 | Should |
| REQ-085 | Analytical export projection (SQL/columnar) separate from operational store | DS | — | Should |
| REQ-086 | Workload, backlog, TAT/SLA tracking with alerts | LM | LIMSpec 6.3, 28 | Should |
| REQ-087 | Customer portal for submission, status and report download | CU | — | Could |

## Integrations

| ID | Requirement | Stakeholder | Regulation | MoSCoW (candidate) |
|---|---|---|---|---|
| REQ-090 | SAP QM adapter (inspection lot in, results/usage decision out) | EXT, IT | A11 §5 | Should |
| REQ-091 | Instrument edge agent (files, serial, SiLA 2, OPC UA LADS) with raw data retained | AN, IT | 211.194, A11 §5 | Must |
| REQ-092 | Inbound messages stored verbatim before mapping; mapping version recorded | QA, IT | DI | Must |
| REQ-093 | Outbound notifications via outbox, idempotent, never re-fired on replay | IT, EXT | — | Must |
| REQ-094 | Gate/yard notification within configurable time after release decision | EXT | scenario | Should |
| REQ-095 | Delivery notice intake (GS1 DESADV or API) | EXT | FOOD | Could |
| REQ-096 | Price/grade facts emitted for ERP-side pricing; optional pricing policy module | FIN | — | Could |

## Non-functional

| ID | Requirement | Stakeholder | Regulation | MoSCoW (candidate) |
|---|---|---|---|---|
| REQ-100 | Task-centric, scan/touch-first UI; key bench actions in ≤ 3 interactions | AN | — | Must |
| REQ-101 | WCAG 2.2 AA | AN, CU | EN 301 549 | Should |
| REQ-102 | Multi-language UI/reports; locale-safe numeric entry; time zones | AN, CU | DI | Must |
| REQ-103 | PII kept out of immutable events or crypto-shreddable | IT, QA | GDPR | Must |
| REQ-104 | Validation package per release (URS map, risk assessment, automated test evidence) | QA, IT | GAMP, CSA, A11 §4 | Should |
| REQ-105 | Per-tenant backup/restore with tested restore; documented continuity fallback | IT | A11 §7, §16 | Must |
| REQ-106 | Read-only auditor role with time-boxed access | QA | A11 §12 | Should |
