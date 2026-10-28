---
title: Product vision
summary: Why this LIMS exists — event-sourced, user-friendly, audit-ready and extensible, replacing monolithic CRUD LIMS.
tags: [vision, goals]
status: accepted
updated: 2026-10-28
---

# Product vision

## Problem

Laboratory information management systems are central to how labs run their business, but:

- Incumbents are huge monoliths (Java/C#, relational DB, CRUD) with decade-long life cycles.
  Strict regulatory audits and certification keep new architectures rare.
- UX for non-technical lab users is poor: 90s look, nested collapsible tables, sub-windows,
  information overload. See [legacy UX pain points](../knowledge/lims/legacy-ux-pain-points.md).
- The relational model does not match reality: lab work **is** a sequence of events.

## Lab work is event-driven

1. A customer places a measurement order.
2. The physical sample arrives.
3. The sample is aliquoted into QR-labelled containers.
4. A measurement is performed.
5. The result is verified by the lab principal.
6. The result is reported to the customer; the customer is billed.

Captured as events, the history can later be projected into whatever shape new questions
require — without having anticipated those questions at design time.

## Goals (in priority order of non-negotiability)

1. **Pleasant UX for all stakeholders** — see [stakeholders](../domain/stakeholders.md).
2. **Audit-trail readiness** — immutable, attributable, complete history.
3. **Extensibility** — fulfill customer customization requests to a reasonable extent without
   forking the core.

## Secondary purpose: realistic test case

This repository is also a demanding real-world test case for EventSourcingDB, architecturekit
and ESDM. Findings go to [upstream feedback](../upstream-feedback/architecturekit.md)
([ADR-0007](../adr/0007-dogfood-architecturekit-and-eventsourcingdb.md)).

## Initial stakeholders

- Lab staff running experiments and tests
- Lab managers approving results
- Data scientists investigating efficiency and test quality
- Controllers writing invoices

The full stakeholder analysis is in [stakeholders](../domain/stakeholders.md).

## Context

LIMS rarely run alone — ERP, logistics, gate control, instruments raise and consume
**integration events**. See the [margarine example](../domain/examples/margarine-incoming-inspection.md).
