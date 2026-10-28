---
title: Product owner decision backlog
summary: Prioritized list of open decisions that block modeling or architecture, each to be grilled and then moved into an ADR or requirement.
tags: [discussion, backlog, product-owner]
status: draft
updated: 2026-10-28
---

# Product owner decision backlog

Ordered by how much they block. Resolve via the `grill` skill; record in ADRs/requirements.

| # | Decision | Blocks | Detail |
|---|---|---|---|
| 1 | Accept/modify ADR-0003, 0004, 0005 (`proposed`) | everything | [adr/](../adr/) |
| 2 | Regulatory profiles at launch (food + 17025 only? GxP EU/US? clinical at all?) | event design, PII | [profiles comparison](../knowledge/lims/regulatory-profiles-comparison.md) |
| 3 | Who edits regulatory profiles, with which approval | ADR-0003 | [ownership](regulatory-profile-ownership.md) |
| 4 | Extensibility tiers: config only / formula language / plugins (GAMP 4 vs 5) | core architecture | [workflow vs scripts](workflow-engine-vs-embedded-scripts.md) |
| 5 | Expected events: facts or projection | process managers | [expected events](expected-events.md) |
| 6 | PII strategy: separate store vs crypto-shredding | every event schema | [GDPR](gdpr-vs-immutable-log.md) |
| 7 | Usage decision and price bonus: LIMS or ERP? | bounded contexts | [margarine example](../domain/examples/margarine-incoming-inspection.md) |
| 8 | CAPA/deviation/training/calibration: modules or integrations | scope | [core modules](../knowledge/lims/core-modules-quality-events.md) |
| 9 | SaaS default isolation, data residency | ADR-0004 | [IT admin](../knowledge/lims/stakeholder-it-admin.md) |
| 10 | Release channels vs frozen validated versions | ops, validation | [GAMP 5](../knowledge/lims/gamp5-csv-csa.md) |
| 11 | Contract-lab mode (customer-within-tenant, portal, invoicing) in v1? | tenancy model | [customer](../knowledge/lims/stakeholder-customer.md) |
| 12 | ESDB licensing budget (25k free-tier cap per instance) | prod/staging | [licensing](../knowledge/eventsourcingdb/licensing-and-limits.md) |
| 13 | Accessibility target (WCAG 2.2 AA?), first UI languages | frontend (later) | [NFRs](../knowledge/lims/non-functional-requirements.md) |
