---
title: ESDM external systems and context mapping
summary: The exact ESDM vocabulary for context mappings (eight patterns, role names, endpoints, term pairs) and external systems (direction, category, capabilities), with verified YAML.
tags: [esdm, context-mapping, external-system, integration, anti-corruption-layer, published-language]
status: draft
sources: [https://www.esdm.io/concepts/context-mapping/, https://www.esdm.io/concepts/external-system/, https://www.esdm.io/reference/core-schema/context-mapping/, https://www.esdm.io/reference/core-schema/external-system/]
updated: 2026-10-28
---

# External systems and context mapping

## External system

Domain-scoped, inventoried once (`external-systems.esdm.yaml`). Required `direction`:
`inbound` (calls us: webhooks), `outbound` (we call it), `bidirectional`. Optional
free-form `category` (`payment`, `mail`, `webhook-source`, ...) and `capabilities[]`
(prose). Not an actor: an inbound call is issued by an internal `system` actor that
is `backedBy` the external system. No URLs, auth or payload schemas.

```yaml
apiVersion: schema.esdm.io/core/v1
kind: external-system
name: customer-portal
scope:
  domain: lims
direction: bidirectional
category: webhook-source
capabilities:
  - receive sample-announced webhook
  - push result-released notification
```

## Context mapping vocabulary

No `scope`; `name` is only a handle. Exactly two endpoints.

| `type` | Role fields | Endpoints may be external system? | `terms` pair keys |
|---|---|---|---|
| `customer-supplier` | `customer`, `supplier` | yes | `customer`, `supplier` |
| `conformist` | `conformist`, `upstream` | yes | `conformist`, `upstream` |
| `anti-corruption-layer` | `downstream` (owns the ACL), `upstream` | yes | `downstream`, `upstream` |
| `open-host-service` | `host`, `consumer` | yes | `host`, `consumer` |
| `published-language` | `publisher`, `consumer` | yes | `publisher`, `consumer` |
| `shared-kernel` | `participants: [bc, bc]` | no | – |
| `partnership` | `participants: [bc, bc]` | no | – |
| `separate-ways` | `participants: [bc, bc]` | no | – |

Endpoint = `{domain, boundedContext}` or `{domain, externalSystem}`. `terms` (optional,
asymmetric types only) relate canonical ubiquitous-language terms of both sides; both
endpoints must then be bounded contexts and the terms must exist. One publisher with
many consumers = several mappings.

Verified:

```yaml
apiVersion: schema.esdm.io/core/v1
kind: context-mapping
name: portal-to-reception
type: anti-corruption-layer
downstream:
  domain: lims
  boundedContext: sample-reception
upstream:
  domain: lims
  externalSystem: customer-portal
---
apiVersion: schema.esdm.io/core/v1
kind: context-mapping
name: reception-to-portal
type: published-language
publisher:
  domain: lims
  boundedContext: sample-reception
consumer:
  domain: lims
  externalSystem: customer-portal
---
apiVersion: schema.esdm.io/core/v1
kind: context-mapping
name: reception-to-analysis
type: customer-supplier
customer:
  domain: lims
  boundedContext: analysis
supplier:
  domain: lims
  boundedContext: sample-reception
terms:
  - customer: Specimen
    supplier: Sample
```

A policy, read model or handler reaching into two BCs without a mapping between them
raises `cross-bounded-context-reference-without-mapping`.

## Relevance for the LIMS (own conclusion)

ADR-0005 maps directly: inbound partner messages = `anti-corruption-layer` with the
partner as `upstream` external system; outbound contracts = `published-language` with
our BC as `publisher`. Each partner (ERP, supplier portal, gate control, instrument
middleware) is one `external-system`. ESDM cannot describe the integration message
*schemas* themselves – see [lims-mapping.md](lims-mapping.md).
