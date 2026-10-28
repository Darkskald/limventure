---
title: Technology direction
summary: Mandated stack (Rust, EventSourcingDB, architecturekit, ESDM) and the open question of scriptability/workflows.
tags: [vision, technology, rust, eventsourcingdb, architecturekit, esdm]
status: accepted
updated: 2026-10-28
---

# Technology direction

Set by the product owner:

| Concern            | Choice                                         | ADR |
|--------------------|------------------------------------------------|-----|
| Backbone language  | Rust                                           | [0001](../adr/0001-rust-on-eventsourcingdb-and-architecturekit.md) |
| Event store        | EventSourcingDB                                | [0001](../adr/0001-rust-on-eventsourcingdb-and-architecturekit.md) |
| DDD/CQRS framework | `architecturekit` (Rust crate)                 | [0001](../adr/0001-rust-on-eventsourcingdb-and-architecturekit.md) |
| Domain modeling    | ESDM (event-sourced domain modeling language)  | [0002](../adr/0002-esdm-for-domain-modeling.md) |
| Frontend           | Out of scope for now                           | — |

## Open: scriptability and workflows

A LIMS must be extremely flexible. Undecided whether this needs a workflow engine
(Temporal or similar) or whether "run an embedded script on a particular event" suffices.
Tracked in [workflow engine vs embedded scripts](../discussions/workflow-engine-vs-embedded-scripts.md).

Knowledge: [ESDM](../knowledge/esdm/), [EventSourcingDB](../knowledge/eventsourcingdb/),
[architecturekit](../knowledge/architecturekit/).
