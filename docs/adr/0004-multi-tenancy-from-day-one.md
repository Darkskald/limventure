---
title: "ADR-0004: Multi-tenancy from day one"
summary: Every subject, command, event and projection is tenant-scoped so the same code runs on-prem (single tenant) and as SaaS (many tenants).
tags: [adr, multi-tenancy, deployment, saas, on-prem]
status: proposed
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
  - *SaaS dedicated*: one EventSourcingDB per tenant (regulated customers).

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
