---
title: Exotic sparks
summary: Unconventional ideas from the product owner — persisted integration events and modeling expected future events.
tags: [vision, ideas, integration-events, expected-events]
status: draft
updated: 2026-10-28
---

# Exotic sparks

Ideas raised by the product owner at project start. Each one is followed up in its own
discussion or ADR.

## 1. Integration events are first-class and persisted

Semantically distinguish **integration events** (raised by or for other IT systems) from
**domain events** — but, because of the hard auditing requirements, persist and treat
integration events with the same rigor.
→ [ADR-0005](../adr/0005-integration-events-are-persisted.md)

## 2. Expected events

Events are normally facts that have already happened. Interesting: also model the
**expectation** of events that will happen in the future (e.g. "the delivery announced for
14:00 is expected; the IR measurement is expected within 2 h"), so that absence, delay and
overdue states become explicit, queryable and auditable.
→ [ADR-0013](../adr/0013-expected-events-are-facts.md), [discussion](../discussions/expected-events.md)
