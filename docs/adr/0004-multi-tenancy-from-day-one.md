---
title: "ADR-0004: Multi-tenancy from day one"
summary: Every subject, command, event and projection is tenant-scoped so the same code runs on-prem (single tenant) and as SaaS (many tenants).
tags: [adr, multi-tenancy, deployment, saas, on-prem]
status: accepted
updated: 2026-10-28
---

# ADR-0004: Multi-tenancy from day one

## Context

The product owner wants both on-prem and SaaS deployments. Retrofitting tenancy into an
event store is painful: subjects and events are immutable.

## Decision

- Tenant id is part of every subject: `/tenants/<tenant-id>/<bounded-context>/<aggregate>/<id>`.
- Every command carries a tenant context; handlers reject cross-tenant access.
- Projections are partitioned by tenant.
- Isolation level is a deployment choice:
  - *on-prem*: one EventSourcingDB, one tenant;
  - *SaaS shared*: one EventSourcingDB, many tenants (subject prefix isolation);
  - *SaaS dedicated*: one EventSourcingDB per tenant.
- **Constraint (agreed 2026-10-28): tenants under a GxP profile (Part 11 / Annex 11) are
  always *dedicated*.** *SaaS shared* is only allowed for non-GxP tenants (e.g. food, ISO 17025).
  Reason: EventSourcingDB has a single API token without roles
  ([ESDB-002](../upstream-feedback/eventsourcingdb.md)), so shared-mode isolation rests
  entirely on application code — not defensible in a GxP audit.

## Alternatives considered

| Option | Pros | Cons |
|---|---|---|
| Tenant in subject (this) | Uniform code, flexible isolation | Longer subjects, must never be forgotten |
| Instance per tenant only | Strong isolation | Ops cost; on-prem/SaaS code paths diverge |
| Add tenancy later | Faster start | Immutable history makes migration expensive |

## Consequences

- Tenant-scoped subject construction must be a single typed helper — no string concatenation.
- Customer-specific extensions are registered per tenant.
- Verify ESDB subject-prefix queries/observe scale for the shared model.
- Each GxP customer costs at least one licensed ESDB instance plus operations.
- The regulatory profile ([ADR-0003](0003-compliance-baseline-and-regulatory-profiles.md))
  determines the allowed isolation level; provisioning must enforce it.
- Upstream wish: per-subject-prefix tokens / RBAC in ESDB would make shared GxP tenancy viable.
