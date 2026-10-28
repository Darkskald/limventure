---
title: architecturekit Go vs Rust differences
summary: Where the Rust architecturekit 0.21.0 differs from or lacks features of the more mature Go v2 distribution.
tags: [architecturekit, rust, go, comparison, gaps]
status: draft
sources: [https://github.com/thenativeweb/architecturekit-golang, https://github.com/thenativeweb/architecturekit-rust, https://docs.rs/architecturekit/0.21.0]
updated: 2026-10-28
---

# Go v2 vs Rust 0.21.0

The Go README (~3400 lines) is the conceptual reference; the Rust README and
rustdoc cover the same core with less depth.

## Same concepts, different shape

| Topic             | Go v2                                          | Rust 0.21.0                                      |
|-------------------|------------------------------------------------|--------------------------------------------------|
| Events            | struct + `EventType()` method; schema derived at runtime from `encoding/json` rules (or from files) | `#[derive(Event)]`, schema derived at compile time from serde attributes |
| Event set         | dynamic `[]architecturekit.Event`              | closed enum `#[derive(Events)]`, compile-checked |
| Projection        | `NewTypedProjection().On(handler)` builder; mode by implemented interfaces | `Projection` trait + `match` on enum; mode by trait choice |
| Deciders          | `NewDecider(state, func(ctx, cmd, state))`     | `Decider::new(|cmd, state| async move {..})`, no ctx |
| Reading           | `iter.Seq2` iterators                          | `futures::Stream`                                |
| HTTP              | own `httpapi.Handle` on `net/http`             | axum 0.8 extractors or `http`-crate helpers      |
| Version           | v2 (v1 unmaintained)                           | 0.x, 22 minor releases in 28 h                   |

## Missing or thinner in Rust

- **`query` package**: Go has filter/order/page/count combinators over
  views; Rust says to use `TryStreamExt` on `View::all`.
- **User handling**: Go `httpapi` determines the user (`UserOf`) and lets
  command mappers return `ErrForbidden`; Rust leaves this to axum extractors
  (`HttpError::unauthorized`/`forbidden` exist).
- **Schemas from files**: Go section "Keeping Schemas in Files"; Rust only
  derived or hand-written `Schema` impls.
- **Documentation depth**: guidance on sharing preconditions between
  commands, time handling, publishing, batching, health, upgrade notes is
  only in the Go README.
- **No context propagation** in Rust deciders (Go passes `context.Context`).

## Missing in both

- Writing `traceparent`/`tracestate` or other metadata on events.
- Sagas/process managers, scheduled commands, outbox.
- Persistent view implementations (SQL etc.) — only traits plus in-memory.
- Multi-tenancy primitives beyond subject paths.
- Authorization model.

## Rust advantages

- Exhaustive `match` over the events enum forces every state/projection to
  handle new event types consciously.
- Schema derivation happens at compile time; non-derivable shapes fail to
  compile instead of at registration.
- Compile-time refusals (generic events, duplicate types) documented as
  `compile_fail` doctests.
