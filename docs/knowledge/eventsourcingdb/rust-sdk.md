---
title: EventSourcingDB Rust SDK
summary: The official `eventsourcingdb` crate — version, features, API surface, v1/v2 API negotiation, error model, hash/signature verification and Testcontainers support.
tags: [eventsourcingdb, rust, sdk, testing]
status: draft
sources:
  - https://docs.eventsourcingdb.io/client-sdks/rust-sdk/
  - https://crates.io/crates/eventsourcingdb
  - https://github.com/thenativeweb/eventsourcingdb-client-rust
updated: 2026-10-28
---

# EventSourcingDB Rust SDK

## Package

| Item | Value |
|------|-------|
| Crate | `eventsourcingdb` (`cargo add eventsourcingdb`) |
| Latest | **4.0.4** (published 2026-10-28) |
| Edition / MSRV | 2024 / Rust **1.88** (`polars` feature: 1.95) |
| License | MIT, official, by the native web GmbH |
| Features | `testcontainer`, `cloudevents`, `polars` (all off by default) |
| Stack | `reqwest` 0.13, `tokio`, `serde_json` (`raw_value`), `ed25519-dalek` 3, `sha2`, `jsonschema` |

Release churn is high: 3.1.0 → 4.0.4 within ten days (Oct 2026), 4.0 was a
breaking change (precondition constructors). The docs page still lists SDK
1.0.0 tested against server 1.2.0.

## Scope

Application-level only: ping, verify token, write (with all preconditions,
OTel trace context), read (recursive, order, bounds, `fromLatestEvent`),
observe, EventQL, register schema, list subjects/types, read one type,
**verify hash**, **verify signature**. **Excludes** backup, restore, health,
audit, verify-store — call those via HTTP.

## Behaviour worth knowing

- `Client::new(url, token)` sends nothing; `ping()` needs no auth.
- **API negotiation**: first request asks whether the server has the v2 API;
  uses v2 if yes, else v1. Re-asks on 404/405. Recursive preconditions need
  v2 → `ClientError::IncompatibleServer` against 1.2.0, nothing is sent.
- **Stall timeout** 30 s (inactivity, not total), `builder().stall_timeout()`;
  needs a Tokio runtime with time driver.
- Errors: `ClientError::DbApiError { code, description, details, status,
  retry_after }`, codes in `eventsourcingdb::error::code` (e.g.
  `PRECONDITION_VIOLATED`); v1 servers have no codes, SDK maps obvious ones.
- `ClientError::OutcomeUnknown`: write may or may not be stored (stall, broken
  connection, 500, future dropped after send) → read before retrying.
- `ClientError::InvalidServerHeader` if a non-ESDB proxy answers.
- `event.verify_hash()` supports hash v1 and v2; unknown version →
  `EventError::UnsupportedHashVersion`. `event.verify_signature(&key)` checks
  hash first, then signature (`MissingSignature`, `MalformedSignature`,
  `SignatureVerificationFailed`).

## Testcontainers (`testcontainer` feature)

- `Container::start_default()` → `get_client()`. Waits for ping 200, 30 s per
  attempt, up to 3 containers.
- Builder: `with_image_tag` (**default `latest`**), `with_port`,
  `with_api_token`, `with_startup_timeout`, `with_signing_key()` (generates key
  pair; `get_signing_key()`, `get_verification_key()`).

## Minimal write

```rust
let event = EventCandidate::builder()
    .source("tag:limventure.io,2026:sample-service".to_string())
    .subject("/samples/42".to_string())
    .ty("io.limventure.sample.sample-registered.v1")
    .data(json!({ "matrix": "serum" }))
    .build();
client.write_events(vec![event], vec![Precondition::is_subject_pristine("/samples/42", None)]).await?;
```

(Precondition constructor signatures are from 4.x README; check the docs.rs
version you pin.)

## Relevance for the LIMS (own conclusions)

- Pin the crate exactly (`=4.0.4`) and pin `with_image_tag("1.2.0")` in tests —
  `latest` will silently jump to 1.3 and change hash format/API.
- Wrap the SDK behind our own port/trait (event-store adapter) to absorb the
  frequent breaking releases and to keep backup/audit HTTP calls in one place.
- Use `verify_hash` in projections and an independent audit job.
