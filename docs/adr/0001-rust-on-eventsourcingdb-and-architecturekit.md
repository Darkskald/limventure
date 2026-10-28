---
title: "ADR-0001: Rust on EventSourcingDB and architecturekit"
summary: The backbone is written in Rust, persists events in EventSourcingDB and uses the architecturekit crate for DDD/CQRS building blocks.
tags: [adr, rust, eventsourcingdb, architecturekit]
status: accepted
updated: 2026-10-28
---

# ADR-0001: Rust on EventSourcingDB and architecturekit

## Context

Lab processes are event-driven (see [product vision](../vision/product-vision.md)); audit
requirements demand an immutable, complete history. The product owner mandated the stack.

## Decision

- Core services in **Rust** (Cargo workspace under `crates/`).
- **EventSourcingDB** is the system of record for all events (domain and integration).
- **architecturekit** provides aggregates, commands, events and read-model plumbing.
- Local/dev instances via `infra/eventsourcingdb/docker-compose.yml`.

## Alternatives considered

| Option | Pros | Cons |
|---|---|---|
| Rust + ESDB + architecturekit | Event-native store, typed, fast, safe | Young crate, small community |
| Kotlin/Java + Axon | Mature ecosystem | Heavy, exactly the legacy feel we want to avoid |
| Rust + Postgres-as-event-store | Ubiquitous ops knowledge | Rebuild integrity/signature/query features ourselves |

## Consequences

- Vendor dependency on EventSourcingDB (licensing, see
  [licensing and limits](../knowledge/eventsourcingdb/licensing-and-limits.md)).
- architecturekit is young — see [go vs rust gaps](../knowledge/architecturekit/go-vs-rust-gaps.md).
  *Superseded in part by [ADR-0007](0007-dogfood-architecturekit-and-eventsourcingdb.md): no
  wrapping layer; gaps are logged as upstream feedback.*
- Audit trail comes "for free" structurally, but signatures, attribution and retention still
  need explicit design ([ADR-0003](0003-compliance-baseline-and-regulatory-profiles.md)).
