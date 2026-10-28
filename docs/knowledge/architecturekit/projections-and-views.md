---
title: architecturekit read side - projections and views
summary: How architecturekit projects events into views (plain, resumable, transactional), keeps views idempotent, supports read-your-writes, and publishes events to other systems.
tags: [architecturekit, rust, projections, views, read-models, cqrs, integration-events]
status: draft
sources: [https://docs.rs/architecturekit/0.21.0, https://github.com/thenativeweb/architecturekit-rust, https://github.com/thenativeweb/architecturekit-golang]
updated: 2026-10-28
---

# Read side: projections and views

## Projection kinds

| Trait                     | Position after restart                 | Use for                           |
|---------------------------|----------------------------------------|-----------------------------------|
| `Projection`              | rebuilds from the first event          | in-memory views                   |
| `ResumableProjection`     | `checkpoint()` / `save_checkpoint()`   | external stores, publishers       |
| `TransactionalProjection` | events + checkpoint in one `Transaction` (`begin`/`apply`/`commit`/`rollback`) | SQL read models |

```rust
pub trait Projection: Send + Sync + 'static {
    type Event: Projected;            // an `Events` enum, or eventsourcingdb::Event (raw)
    type Error: Error + Categorized + Send + Sync + 'static;
    fn apply(&self, event: Envelope<Self::Event>) -> impl Future<Output = Result<(), Self::Error>> + Send;
    fn upcasters() -> Option<&'static Upcasters> { None }
    fn seen(&self, event_id: &str) {}
}
```

- `Envelope<E>` (`#[non_exhaustive]`): `id`, `time`, `source`, `subject`,
  `event_type`, `trace_parent`, `trace_state`, `part`, `data`.
- `seen` is called for every stored event incl. ignored types, so views can
  report their revision.
- `catch_up_batch_size()` batches checkpoints/transactions while catching up
  (default 1 event).
- Error category decides: transient → reconnect from checkpoint with
  exponential backoff; other → run stops.

## Running

```rust
let run = store.start_projection(Subjects::tree("/books"), Arc::clone(&book_list),
    token.clone(), ProjectionOptions::named("book list"));
wait_caught_up(&[&run]).await?;
```

- Also `start_resumable_projection`, `start_transactional_projection`, and
  one-shot `catch_up_*projection` (batch jobs, tests).
- `Subjects::tree(path)` (recursive) or `Subjects::exact(path)`.
- `ProjectionRun::status()` → `ProjectionStatus { phase, since, error,
  attempts, revision, has_caught_up }`; `Phase` = `CatchingUp | Live |
  Reconnecting | Stopped`. Stopped via `CancellationToken`.
- A transient failure is retried **without limit**; detect via status or
  `StoreBuilder::reconnect_observer`.

## Views

`View<T>` (`all()` → `Stream`) and `KeyedView<K, T>` (`get(&key)`). The only
implementations shipped are in memory:

- `InMemoryView<K, T>::new(key_of)` with `insert`, `upsert`, `update`,
  `delete`, `update_where`, `delete_where`. Each item remembers the revision
  of the event that last changed it → applying an event twice is a no-op
  (`Outcome`).
- `with_revision_in(..)` writes the revision into a field of the item.
- `InMemoryIndex` = secondary index on a view (`lookup`, `update`, `delete`).
- Filtering/ordering/paging: use `futures::TryStreamExt` on `all()`; there is
  no query combinator module in Rust (Go has `query`).

## Read your writes

`Revisioned` (`revision()`, `wait_for(rev)`) is implemented by
`InMemoryView`. `wait_for_written(&view, &written, timeout)` waits until a
view has seen the events a command wrote; over HTTP the `Wait-For-Revision`
header does the same (see [http-api.md](http-api.md)). Helpers:
`revision_of(&events)`, `parse_revision`, `compare_revisions`.

## Publishing to other systems (integration events)

From the Go docs, applies equally to Rust: never publish from where a
command is executed (lost on crash). Instead write a **resumable projection**
that publishes (mail, webhook, broker), returns transient errors on failure,
and passes `Envelope::id` downstream for de-duplication — delivery is
**at-least-once**. Initialise the checkpoint to the latest event id to skip
history. Systems that can read EventSourcingDB should observe it directly.
