---
title: architecturekit write side - states, commands, deciders
summary: How architecturekit replays states, declares commands with preconditions, decides with deciders and executes or writes events with optimistic concurrency.
tags: [architecturekit, rust, commands, deciders, preconditions, optimistic-concurrency, aggregates]
status: draft
sources: [https://docs.rs/architecturekit/0.21.0, https://github.com/thenativeweb/architecturekit-rust, https://github.com/thenativeweb/architecturekit-golang]
updated: 2026-10-28
---

# Write side: states, commands, deciders

The kit follows the functional **decider pattern** (decide + evolve), not
classic OO aggregates. One command acts on one subject.

## State

```rust
pub trait State: Default + Clone + Send + 'static {
    type Event: Events;
    fn evolve(self, event: &Self::Event) -> Self;
    fn upcasters() -> Option<&'static Upcasters> { None }
    fn from_latest() -> Option<&'static str> { None }
}
```

- Starts from `Default`, folded over the events of **exactly one subject**
  (non-recursive read).
- `evolve` must be pure (no clock, no I/O); it runs on every load.
- `from_latest()` names an event type whose `evolve` arm sets the full state;
  loading starts at the latest event of that type (a "snapshot as event",
  Go docs: "Reading Long Streams"). Naming a type without a variant panics.

## Command

```rust
pub trait Command {
    fn subject(&self) -> String;
    fn preconditions(&self) -> Vec<Precondition>;
}
```

At least one precondition is mandatory (`check_preconditions` enforces it):

| Constructor                              | Meaning                                                   |
|------------------------------------------|-----------------------------------------------------------|
| `Precondition::on_state_read()`          | Optimistic concurrency against the state just read        |
| `Precondition::on_pristine_subject(s)`   | Subject must have no events (creation)                    |
| `Precondition::on_populated_subject(s)`  | Subject must exist (ESDB >= 1.2)                          |
| `Precondition::on_event_id(s, id)`       | Caller-supplied revision (If-Match style)                 |
| `Precondition::require(esdb_precond)`    | Any client-SDK precondition, e.g. EventQL query true      |
| `Precondition::unconditionally()`        | No check; can not be combined                             |

Cross-subject invariants (uniqueness, quotas) use
`require(eventsourcingdb::Precondition::is_eventql_query_true("FROM e IN events ..."))`.
Values interpolated into EventQL must be validated in the decider first
(injection risk, per Go docs). A violated EventQL precondition is reported as
a transient *conflict* (409), not a domain error.

## SubjectScheme

`SubjectScheme::new("/tenant/{tenant}/workshop/{workshop}")` builds subjects
(`build(&[..])`, checks values), reads values back (`value(subject, "tenant")`,
`match_subject`) and gives the `root()` for tree reads.

## Decider

```rust
Decider::new(|cmd: BorrowBook, book: Book| async move {
    if book.is_borrowed { return Err(DomainError::new("already borrowed")); }
    Ok(vec![BookEvent::Borrowed(BookBorrowed { reader: cmd.reader })])
})
```

- `Decider<C, S: State, D>`; returns `Result<Vec<S::Event>, D>`.
- Async so it may `store.load::<Other>(..)` other states — but the write is
  guarded only on its own subject unless further preconditions are added.
- Takes owned command and state (futures are `Send`).
- Error type `D` is `DomainError` or own type implementing `Categorized`.

## Store::execute

`store.execute(&decider, command).await -> Result<Vec<eventsourcingdb::Event>, ExecuteError<D>>`

1. Checks preconditions, 2. loads/folds the state (optionally from the state
cache), 3. decides, 4. writes all events atomically with resolved
preconditions (`on_state_read` → last event id). With
`StoreBuilder::conflict_retries(n)` it re-decides on conflicts caused by
`on_state_read`. Once the write starts it runs on its own task, so dropping
the future can not cut it in half. Returns the stored events (with ids =
revisions).

## Store::write and Store::load

- `store.write(Vec<EventOn>, Vec<Precondition>)` writes to several subjects
  atomically, without a decider (`EventOn::new(subject, &event)`).
- `store.load::<S>(subject)` reads one state for queries.
- `store.read(&Subjects, &ReadOptions)` streams raw `eventsourcingdb::Event`s
  (verified), with bounds/order options.

See [error-model.md](error-model.md) for the error categories.
