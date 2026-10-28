---
title: Mapping LIMS concerns onto ESDM
summary: Own analysis of how integration events, expected future events, deadlines, audit metadata and tenancy from the LIMS vision can and cannot be expressed in ESDM 0.15.0.
tags: [esdm, lims, integration-events, expected-events, audit-trail, multi-tenancy]
status: draft
sources: [https://www.esdm.io/reference/core-schema/process-manager/, https://www.esdm.io/reference/core-schema/context-mapping/, https://www.esdm.io/reference/core-schema/event-handler/, https://www.esdm.io/concepts/event/]
updated: 2026-10-28
---

# Mapping LIMS concerns onto ESDM

**Everything in this note is own conclusion**, derived from the schema and a lint-clean
test model, not from ESDM docs. Context: [ADR-0005](../../adr/0005-integration-events-are-persisted.md),
[exotic sparks](../../vision/exotic-sparks.md), [margarine example](../../domain/examples/margarine-incoming-inspection.md).

## Integration events vs domain events

ESDM has **one** `event` kind; it has no notion of "integration event". Building blocks:

| Concern | ESDM element |
|---|---|
| Partner (ERP, supplier portal, gate, instrument) | `external-system` (`direction`) |
| Inbound translation | `context-mapping type: anti-corruption-layer`, `downstream` = our BC, `upstream` = partner |
| Outbound contract | `context-mapping type: published-language`, `publisher` = our BC, `consumer` = partner |
| Who issues commands from a webhook | `actor type: system` with `backedBy: [partner]` |
| Delivery to partner | `event-handler` with `sideEffects: external-call`, at-least-once + idempotency |

To make ADR-0005's *persisted* integration events visible in the model, model them as
real events of dedicated aggregates, e.g. `inbound-message` (`received`,
`translated`, `rejected`) and `outbound-message` (`queued`, `delivered`,
`delivery-failed`), either in a per-partner integration BC or inside the consuming BC.
The ACL becomes a policy `inbound-message/received` → domain command; outbound becomes a
policy domain event → `outbound-message/queue` plus an event handler on `queued`.
Distinguish namespaces through `metadata.annotations.cloudevents.type`
(`io.limventure.integration.<partner>.<event>.vN` vs `io.limventure.<bounded-context>.<aggregate>-<event>.vN`, [ADR-0023](../../adr/0023-event-types-carry-a-version-suffix.md)) and/or
`metadata.labels` (`event-class: integration`). Labels are free-form and unchecked.

Gap: the published-language payload is only the `data` JSON Schema of the integration
event; ESDM has no contract versioning (new name = new version, `...-v2`).

## Expected future events

ESDM events are strictly past tense, but the **expectation is itself a fact**:

1. `delivery/announced` with `expectedAt` (the inbound integration fact).
2. A process manager correlated by delivery id starts on `announced`, stores
   `expectedAt`, arms `timers: [{name: arrival-due, at: expectedAt}]`.
3. `arrived` → cancel timer, end. Timer fires → emit `mark-overdue` → event
   `became-overdue` (explicit, auditable absence).
4. A read model `expected-deliveries` (status expected/arrived/overdue) makes it
   queryable; a GWT feature tests the timer path.

SLA-style expectations ("IR result within 2 h of receipt") use
`after: {value: 2, unit: hours}` set in the reaction to `received`. Verified pattern:
[process-managers-and-timers.md](process-managers-and-timers.md).
Limits: no "offset relative to a field" (e.g. expectedAt + 30 min tolerance) – compute
a `deadline` state field (prose in `rule`) and use `at: deadline`; rescheduling =
`cancelTimers` + `setTimers` in one reaction; timers are model statements only – the
runtime (architecturekit/EventSourcingDB) must provide a durable scheduler.

## Audit and tenancy

Not expressible in ESDM: tenant, user, reason, signature metadata on events. Options:
repeat required fields in every event `data` (lint-checked shape, verbose) or define an
envelope convention outside ESDM and enforce it with a `limtool` check. Signatures /
four-eyes fit as commands with `actors` (`lab-head`, `head-of-analytics`) plus aggregate
invariants and GWT rejection scenarios.

## Open questions (candidates for docs/discussions/)

- Integration BC per partner vs integration aggregates inside each BC.
- Which runtime provides PM timers; does architecturekit support DCBs and PMs?
