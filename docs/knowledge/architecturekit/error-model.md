---
title: architecturekit error model
summary: The three error categories of architecturekit (domain, transient, permanent) plus outcome-unknown, and how they map to retries and HTTP status codes.
tags: [architecturekit, rust, errors, retries, http]
status: draft
sources: [https://docs.rs/architecturekit/0.21.0, https://github.com/thenativeweb/architecturekit-rust]
updated: 2026-10-28
---

# Error model

Every kit error implements `Categorized`:

```rust
pub trait Categorized { fn category(&self) -> Option<Category>; }
```

| Category / variant         | Meaning                                        | Action        | HTTP (`HttpError`) |
|----------------------------|------------------------------------------------|---------------|--------------------|
| Decider refusal (`DomainError` or own) | business rule violated             | final         | 422, own message   |
| `Transient::Conflict`      | precondition did not hold                     | retry/re-read | 409                |
| other `Transient`          | DB unreachable, timeouts, capacity            | retry later   | 503                |
| `Permanent`                | bad data, failed verification, refused request| fix code/data | 500                |
| `OutcomeUnknown`           | write may or may not be stored                 | reconcile     | 500                |

- `ExecuteError<D>` has `Decider(D)`, `Transient`, `Permanent`,
  `OutcomeUnknown`, `NotARevision`; `WriteError`, `LoadError`, `ReadError`,
  `RegisterSchemasError` follow the same scheme.
- `Failure` carries `message()` and an optional `cause()`.
- `Permanent::Unverified` = hash/signature mismatch of a read event.
- Projections use the category of their own `Error`: transient → reconnect
  and retry from checkpoint; anything else → run ends.
- `HttpError` hides internals behind fixed messages and logs the cause via
  `log`.

Own decider error types implement `Categorized` and (for tests)
`PartialEq + Debug`.
