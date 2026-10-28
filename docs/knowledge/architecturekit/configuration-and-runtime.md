---
title: architecturekit configuration and runtime
summary: Cargo features, dependencies, MSRV, StoreBuilder options (verification, retries, cache, reconnects) and runtime behaviour of architecturekit 0.21.0.
tags: [architecturekit, rust, configuration, cargo-features, tokio, runtime]
status: draft
sources: [https://crates.io/crates/architecturekit, https://docs.rs/architecturekit/0.21.0, https://github.com/thenativeweb/architecturekit-rust]
updated: 2026-10-28
---

# Configuration and runtime

## Cargo

| Feature          | Default | Adds                                                        |
|------------------|---------|-------------------------------------------------------------|
| `derive`         | yes     | `Event`, `Events`, `Schema` derives (`architecturekit-macros` =0.21.0) |
| `http`           | no      | `httpapi` with `http` crate types                           |
| `axum`           | no      | axum 0.8 extractors/handlers; implies `http`               |
| `testing`        | no      | `architecturekit::testing` (no Docker)                      |
| `testcontainers` | no      | `testing::Database`; implies `testing` + `eventsourcingdb/testcontainer` |

- Edition 2024, `rust-version = "1.88"`. Verified locally with rustc 1.96.
- Required companions: `eventsourcingdb = "4.0.4"` (for `Client`), `serde`
  with `derive`, `tokio` with `macros, rt-multi-thread`.
- The `eventsourcingdb` 4.0.4 client currently pulls both reqwest 0.12 and
  0.13 (duplicate dependency tree, longer builds).

## StoreBuilder

```rust
let store = Store::builder(client, "https://library.eventsourcingdb.io")
    .conflict_retries(3)
    .state_cache(10_000)
    .reconnect_delays(Duration::from_secs(1), Duration::from_secs(60))
    .build();
```

| Option                           | Default       | Effect                                                       |
|----------------------------------|---------------|--------------------------------------------------------------|
| `source` (builder arg)           | required      | CloudEvents `source` of every written event                  |
| hash verification                | on            | verifies the hash chain of every read event (~1 µs/event)    |
| `without_hash_verification()`    | —             | turns it off; panics on `build()` if combined with signatures |
| `signature_verification(key)`    | off           | Ed25519 `VerifyingKey`; requires ESDB running with signing key |
| `conflict_retries(n)`            | 0             | re-decide on `on_state_read` conflicts                        |
| `state_cache(max_subjects)`      | 0 (off)       | LRU of states; still reads newer events → multi-process safe |
| `reconnect_delays(init, max)`    | 1 s / 60 s    | exponential backoff of projections                           |
| `reconnect_observer(fn)`         | none          | callback per reconnect attempt (logging/metrics)              |

## Runtime behaviour

- Tokio only; writes and schema registrations run on detached tasks so a
  dropped request future can not leave a half-known write.
- Schemas: call `store.register_schemas(MyEvents::schemas())` on **every**
  start; mismatches with registered schemas fail permanently.
- Logging via `log` crate; no `tracing` spans, no metrics built in.
- Writes set no `traceinfo`; read envelopes expose `trace_parent`/`trace_state`.
- No configuration file or env parsing: everything is code.
