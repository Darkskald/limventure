---
title: architecturekit overview
summary: What the architecturekit Rust crate (the native web) is, what it covers, its maturity, and where the other notes on it live.
tags: [architecturekit, rust, event-sourcing, cqrs, ddd, eventsourcingdb]
status: draft
sources: [https://crates.io/crates/architecturekit, https://github.com/thenativeweb/architecturekit-rust, https://docs.rs/architecturekit/0.21.0, https://github.com/thenativeweb/architecturekit-golang]
updated: 2026-10-28
---

# architecturekit overview

`architecturekit` is a library by *the native web* with building blocks for
DDD/CQRS/event-sourced applications on top of
[EventSourcingDB](https://www.eventsourcingdb.io). It exists for Go (v2, the
reference, with the most documentation) and Rust (this note: crate version
**0.21.0**). It is a library, not a framework: no runtime, no container, no
code generation besides derive macros.

## Scope (Rust 0.21.0)

| Covered                                         | Not covered                                    |
|-------------------------------------------------|------------------------------------------------|
| Events with derived JSON schemas               | Sagas / process managers / policies as a type  |
| States replayed from events (`State::evolve`)  | Snapshots stored outside the event stream      |
| Commands, preconditions, deciders, `execute`   | Event metadata on write (traceparent, actor)   |
| Multi-subject atomic `write`                   | Authentication/authorization (app's job)       |
| Upcasters (event versioning)                    | Query combinators (filter/order/page)          |
| Projections (plain, resumable, transactional)  | Persistent view implementations (only memory)  |
| `InMemoryView`, `InMemoryIndex`, read-your-writes | Message broker / outbox integration        |
| HTTP glue for `http` / `axum` 0.8, health probes |                                              |
| Given-when-then tests, testcontainers database |                                                |

The DDD "aggregate" is not a type: it is the combination of a **subject**
(EventSourcingDB stream path), a **state** and the **deciders** acting on it.
"Policies" and "flows" do not exist as concepts; side effects are modelled as
resumable projections (see [projections-and-views.md](projections-and-views.md)).

## Facts

- License MIT; edition 2024; MSRV (`rust-version`) **1.88**.
- Hard dependencies: `eventsourcingdb` 4.0.4 (official client SDK, reqwest-based),
  `tokio` 1.52+, `serde`/`serde_json`, `chrono`, `ed25519-dalek` 3 (signature
  verification), `futures-util`, `tokio-util`, `log`.
- Async-only, Tokio-bound. Logging via the `log` facade (no `tracing`).

## Maturity (as of 2026-10-28)

- First release 0.1.0 on 2026-10-27 08:46 UTC, 0.21.0 on 2026-10-28 12:49 UTC:
  **22 releases in ~28 hours**, all minor bumps (= breaking under 0.x semver).
- ~200 total downloads on crates.io; no CHANGELOG in the package.
- The Go v2 line is clearly the more mature sibling; the Rust crate appears to
  be a port that converges on it. Pin an exact version (`=0.21.0`).

## Notes in this folder

- [events-and-schemas.md](events-and-schemas.md) — events, schemas, upcasting
- [state-commands-deciders.md](state-commands-deciders.md) — write side
- [error-model.md](error-model.md) — error categories and their meaning
- [projections-and-views.md](projections-and-views.md) — read side
- [http-api.md](http-api.md) — `http` / `axum` features
- [rust-api.md](rust-api.md) — public types and traits
- [configuration-and-runtime.md](configuration-and-runtime.md) — features, store options
- [testing.md](testing.md) — deciders, projections, containers
- [go-vs-rust-gaps.md](go-vs-rust-gaps.md) — what Go has that Rust lacks
- [lims-relevance.md](lims-relevance.md) — own conclusions for the LIMS
