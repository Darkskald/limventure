---
title: ESDM policies and event handlers
summary: Stateless event consumers in ESDM - policies that emit commands and event handlers that cause external side effects - with delivery guarantees, idempotency owners and verified YAML.
tags: [esdm, policy, event-handler, idempotency, delivery-guarantee, integration]
status: draft
sources: [https://www.esdm.io/concepts/policy/, https://www.esdm.io/concepts/event-handler/, https://www.esdm.io/reference/core-schema/policy/, https://www.esdm.io/reference/core-schema/event-handler/]
updated: 2026-10-28
---

# Policies and event handlers

Three event-consuming kinds, all **domain-scoped** (`scope: {domain}`) and all with a
required `deliveryGuarantee: at-least-once | at-most-once`; `at-least-once` makes
`idempotency` required.

| Kind | State | Output | Pick when |
|---|---|---|---|
| `policy` | none | `emits[]` command refs | "do the next thing in the domain" – one event, one rule |
| `event-handler` | none | `sideEffects[]` (`external-call` / `other`) | "tell the world" – mail, webhook, audit log, metrics |
| `process-manager` | per instance | commands + timers | needs memory, several events, deadlines – see [process-managers-and-timers.md](process-managers-and-timers.md) |

Never combine command emission and side effects in one element. A handler that must
react to the *result* of an external call → wrap the external system so it produces its
own events back into the model.

`idempotency.owner`: `self` (consumer dedups), `downstream` (callee dedups, e.g.
idempotency key), `infrastructure` (broker/outbox), `none` (dangerous, document why),
`not-required` (naturally idempotent). Optional `strategy` prose.

Policy (verified) – crosses BCs, so a context mapping between the two is expected:

```yaml
apiVersion: schema.esdm.io/core/v1
kind: policy
name: book-slot-on-receipt
scope:
  domain: lims
deliveryGuarantee: at-least-once
idempotency:
  owner: not-required
handles:
  - boundedContext: sample-reception
    aggregate: sample
    event: received
emits:
  - boundedContext: analysis
    dynamicConsistencyBoundary: instrument-slot
    command: book-slot
```

Event handler (verified):

```yaml
apiVersion: schema.esdm.io/core/v1
kind: event-handler
name: notify-portal-on-receipt
scope:
  domain: lims
deliveryGuarantee: at-least-once
idempotency:
  owner: downstream
  strategy: Event id is sent as idempotency key.
handles:
  - boundedContext: sample-reception
    aggregate: sample
    event: received
sideEffects:
  - type: external-call
    externalSystem: customer-portal
    rule: Publish the sample-received integration event to the portal.
```

Optional on both: `constraints[]` (activation conditions such as business hours).
Removing the analysis↔reception mapping triggered (verified)
`esdm/modeling/cross-bounded-context-reference-without-mapping` on the policy.

## Relevance for the LIMS (own conclusion)

Outbound integration (ADR-0005) = event handler with `external-call` +
`at-least-once` + `idempotency.owner: downstream` (event id as key). ESDM has no kind
for "persist the integration event first"; that outbox step is implementation, but it
can be made explicit by modeling an `outbound-message` aggregate whose events
(`queued`, `delivered`, `delivery-failed`) are the audited integration events, with the
handler consuming `queued`. See [lims-mapping.md](lims-mapping.md).
