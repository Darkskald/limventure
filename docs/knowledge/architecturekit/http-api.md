---
title: architecturekit HTTP API support
summary: What the http and axum features of architecturekit provide - strict JSON extraction, command and query answers, QUERY method, read-your-writes headers, health probes.
tags: [architecturekit, rust, http, axum, api]
status: draft
sources: [https://docs.rs/architecturekit/0.21.0, https://github.com/thenativeweb/architecturekit-rust, https://github.com/thenativeweb/architecturekit-golang]
updated: 2026-10-28
---

# HTTP API support (`http`, `axum`)

Module `architecturekit::httpapi`. Feature `http` uses only the `http` crate
types (framework-neutral: `body_of`, `no_body`, `Reading::of`); `axum` adds
extractors/handlers for **axum 0.8**.

## Commands

```rust
async fn borrow(State(app): State<App>, Path(book_id): Path<String>,
    Strict(request): Strict<BorrowRequest>) -> Result<CommandAnswer, HttpError> {
    let written = app.store.execute(&app.borrow_book, BorrowBook { book_id, reader: request.reader }).await?;
    Ok(CommandAnswer::new(&written))   // {"revision":"42"}
}
```

- `Strict<T>`: JSON body, rejects unknown fields with 400 and a precise
  message; `NoBody` for body-less commands; `MAX_REQUEST_BODY` = 1 MiB.
- `?` converts every kit error into `HttpError` by category (see
  [error-model.md](error-model.md)).
- Authentication/authorization: **own axum extractor**; refuse with
  `HttpError::unauthorized` / `HttpError::forbidden`. No user abstraction in
  Rust (Go has `UserOf`).

## Queries

- Sent with HTTP method **`QUERY`**, the query in the body; route with
  `httpapi::query(handler)`.
- `Reading` extractor + `reading.revisioned(view, &query, DEFAULT_WAIT, || ..)`
  waits for `Wait-For-Revision` (max `DEFAULT_WAIT` = 5 s), answers with the
  view's `Revision` header and an ETag (304 on match).
- `QueryAnswer::found(Option<T>)` → 200 or 404.

## Operations

- `Health::readiness([runs])` / `Health::liveness([runs])` as axum handlers:
  200/503 with JSON per projection (phase, revision, attempts). Readiness
  needs all runs caught up; liveness fails only once a run stopped.
- `answer_panic` for `tower_http::catch_panic::CatchPanicLayer` → 500 + log.
