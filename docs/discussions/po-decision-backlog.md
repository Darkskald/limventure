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
| 1 | Who edits regulatory profiles, with which approval | ADR-0003 | [ownership](regulatory-profile-ownership.md) |
| 2 | CAPA/deviation/training/calibration: modules or integrations | scope | [core modules](../knowledge/lims/core-modules-quality-events.md) |
| 3 | SaaS default isolation for non-GxP tenants, data residency | ADR-0004 | [IT admin](../knowledge/lims/stakeholder-it-admin.md) |
| 4 | Release channels vs frozen validated versions | ops, validation | [GAMP 5](../knowledge/lims/gamp5-csv-csa.md) |
| 5 | Contract-lab mode (customer-within-tenant, portal, invoicing) in v1? | tenancy model | [customer](../knowledge/lims/stakeholder-customer.md) |
| 6 | ESDB licensing budget (25k free-tier cap per instance) | prod/staging | [licensing](../knowledge/eventsourcingdb/licensing-and-limits.md) |
| 7 | Accessibility target (WCAG 2.2 AA?), first UI languages | frontend (later) | [NFRs](../knowledge/lims/non-functional-requirements.md) |
