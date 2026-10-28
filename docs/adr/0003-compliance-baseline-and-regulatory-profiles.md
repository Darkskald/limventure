---
title: "ADR-0003: Fixed compliance baseline plus configurable regulatory profiles"
summary: The core always meets the strictest audit baseline (immutable attributable events, e-signature capability); regulation-specific rules are configurable, versioned, audited profiles per tenant.
tags: [adr, compliance, audit-trail, e-signature, configuration, regulation]
status: proposed
updated: 2026-10-28
---

# ADR-0003: Fixed compliance baseline plus configurable regulatory profiles

## Context

Target customers range from food labs (ISO/IEC 17025, IFS/BRC) to pharma (21 CFR Part 11,
EU GMP Annex 11, GAMP 5). The product owner wants the policy to be configurable. See
[requirements catalog](../domain/requirements-catalog.md) and `docs/knowledge/lims/regulation-*`.

## Decision

**Baseline — always on, not configurable:**

- Every event carries tenant, actor (person or system), timestamp and causation/correlation ids.
- Events are never updated or deleted; corrections are new events referencing the original.
- E-signature *capability* (signer, meaning, timestamp bound to the signed record) exists in
  the core.
- Store integrity/signature features of EventSourcingDB are enabled.

**Regulatory profile — configurable per tenant, itself event-sourced:**

- Which commands require a signature, with which meaning (*reviewed*, *approved*, *rejected*).
- Four-eyes / counter-signature rules (e.g. rejection needs head of analytics).
- Mandatory reason-for-change on corrections.
- Retention classes and archiving rules.
- Profile changes are events: who changed which rule when — auditors will ask.

## Alternatives considered

| Option | Pros | Cons |
|---|---|---|
| Baseline + profiles (this) | One core, provable floor | Profile engine is real work |
| Fully configurable incl. audit trail | Max flexibility | A misconfiguration voids compliance |
| Hard-code strictest (Part 11) for all | Simple | Food labs drown in signatures — UX goal fails |

## Consequences

- Profiles need versioning: a result is evaluated against the profile version valid at the time.
- Validation (CSV/CSA) can certify the core once and the profile per customer.

## Open points

- Who may edit a profile (vendor, customer QA, both)? Needs PO decision.
