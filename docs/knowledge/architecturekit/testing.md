---
title: architecturekit testing support
summary: Given-when-then tests for deciders, database-free projection tests and container-backed integration tests with the testing and testcontainers features of architecturekit.
tags: [architecturekit, rust, testing, tdd, testcontainers]
status: draft
sources: [https://docs.rs/architecturekit/0.21.0/architecturekit/testing/index.html, https://github.com/thenativeweb/architecturekit-rust, https://github.com/thenativeweb/architecturekit-golang]
updated: 2026-10-28
---

# Testing

Enable only for tests:

```toml
[dev-dependencies]
architecturekit = { version = "=0.21.0", features = ["testing"] }   # or "testcontainers"
```

## Deciders: given / when / then

```rust
// In a #[tokio::test]:
given(&borrow_book(), [BookEvent::Acquired(BookAcquired { title: "2001".to_owned(), author: "A. C. Clarke".to_owned() })])
    .when(BorrowBook { book_id: "42".to_owned(), reader: "John".to_owned() })
    .await
    .then_events([BookEvent::Borrowed(BookBorrowed { reader: "John".to_owned() })])
    .then_preconditions([Precondition::on_state_read()]);
```

- Assertions on `Decision`: `then_events`, `then_nothing`, `then_failed(err)`
  (needs `PartialEq + Debug` on the error), `then_some_event`,
  `then_every_event`, `then_no_event`, `then_state(|s| ..)`,
  `then_preconditions`, `result()`.
- Events are compared by type + JSON data (no `PartialEq` needed).
- History is round-tripped through JSON, so serde mistakes surface in tests.
- `given_stored(&decider, stored_events)` feeds raw stored events → tests
  upcasters from old event types.
- `replay` / `step` fold states directly.
- Time-dependent deciders: inject a clock into the decider factory (Go docs
  pattern), pass a fixed clock in tests.

## Projections without a database

```rust
project(&book_list, &stored_events("/books/42", [BookEvent::Acquired(..)])).await?;
let Ok(book) = book_list.books.get("42").await;
```

- `project` runs upcasters, skips unknown types, delivers split events part
  by part and calls `seen` — same semantics as a real run.
- `stored_events_at` sets explicit times; `StoredEvent` fields are public
  (craft unknown types, bad data).
- `project_transactional` for `TransactionalProjection`.
- `Envelope::new(subject, id, data)` for applying a single event to a view.

## Integration tests with a real EventSourcingDB

Feature `testcontainers` (needs Docker):

```rust
let database = Database::isolated().await;          // own container per test
let store = database.store("https://library.eventsourcingdb.io", BookEvent::schemas()).await;
let client = database.client().await;              // write events past the store
```

Image tag override via env `EVENTSOURCINGDB_IMAGE_TAG`. Startup ~1 s with
the image cached.

## Queries

No helper: query functions are plain functions over views and are tested
directly (Go: "Testing Queries").
