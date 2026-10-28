---
title: "ADR-0001: Rust on EventSourcingDB and architecturekit"
summary: The backbone is written in Rust, persists events in EventSourcingDB and uses the architecturekit crate for DDD/CQRS building blocks.
tags: [adr, rust, eventsourcingdb, architecturekit]
status: accepted
updated: {{date}}
---

# ADR-0001: Rust on EventSourcingDB and architecturekit

## Context

The project is event-sourced by design and exists partly to exercise this stack
([ADR-0004](0004-dogfood-architecturekit-and-eventsourcingdb.md)).

## Decision

- Core services in **Rust** (Cargo workspace under `crates/`).
- **EventSourcingDB** is the system of record for all events.
- **architecturekit** provides aggregates, commands, events and read-model plumbing, used
  directly (no wrapping layer).
- Local/dev instances via `infra/eventsourcingdb/docker-compose.yml`.

## Alternatives considered

| Option | Pros | Cons |
|---|---|---|
| Rust + ESDB + architecturekit | Event-native store, typed, fast, safe | Young crate, small community |
| Rust + Postgres-as-event-store | Ubiquitous ops knowledge | Rebuild integrity/signature/query features ourselves |

## Consequences

- Vendor dependency on EventSourcingDB (licensing, see
  [licensing and limits](../knowledge/eventsourcingdb/licensing-and-limits.md)).
- architecturekit is young — see [go vs rust gaps](../knowledge/architecturekit/go-vs-rust-gaps.md);
  gaps are logged as upstream feedback.
