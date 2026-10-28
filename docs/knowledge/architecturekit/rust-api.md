---
title: architecturekit Rust public API (0.21.0)
summary: Map of the public types, traits and functions of the architecturekit 0.21.0 crate, grouped by purpose, with verbatim signatures.
tags: [architecturekit, rust, api-reference]
status: draft
sources: [https://docs.rs/architecturekit/0.21.0, https://github.com/thenativeweb/architecturekit-rust, https://crates.io/crates/architecturekit]
updated: 2026-10-28
---

# Rust public API (0.21.0)

All items are re-exported at the crate root (from `src/lib.rs`), except
`httpapi` (feature `http`) and `testing` (feature `testing`).

## By purpose

| Purpose           | Items                                                                                      |
|-------------------|--------------------------------------------------------------------------------------------|
| Events            | `Event` (trait + derive), `Events` (trait + derive), `Schema` (trait + derive), `EventSchema` |
| Versioning        | `Upcasters`, `UpcastEvent`                                                                 |
| Write side        | `State`, `Command`, `Precondition`, `check_preconditions`, `Decider`, `SubjectScheme`      |
| Store             | `Store`, `StoreBuilder`, `EventOn`                                                         |
| Reading           | `Subjects`, `ReadOptions`, `LowerBound`, `UpperBound`, `Order`, `IfLatestEventIsMissing`   |
| Replaying         | `replay`, `replay_stored`, `step`, `step_stored`                                           |
| Read side         | `Projection`, `ResumableProjection`, `TransactionalProjection`, `Transaction`, `Projected`, `Envelope` |
| Runs              | `ProjectionOptions`, `ProjectionRun`, `ProjectionStatus`, `Phase`, `Reconnect`, `wait_caught_up`, `CancellationToken` |
| Views             | `View`, `KeyedView`, `InMemoryView`, `InMemoryIndex`, `Outcome`, `ViewError`               |
| Revisions         | `Revisioned`, `revision_of`, `parse_revision`, `compare_revisions`, `wait_for_written`, `NotARevision`, `NotCaughtUp` |
| Errors            | `Categorized`, `Category`, `DomainError`, `Failure`, `Transient`, `Permanent`, `ExecuteError`, `WriteError`, `LoadError`, `ReadError`, `RegisterSchemasError`, `ProjectionError`, `CaughtUpError` |
| HTTP (`httpapi`)  | `Strict`, `NoBody`, `CommandAnswer`, `QueryAnswer`, `Reading`, `HttpError`, `Health`, `query`, `answer_panic`, `body_of`, `no_body`, `DEFAULT_WAIT`, `WAIT_FOR_REVISION`, `REVISION`, `MAX_REQUEST_BODY` |
| Tests (`testing`) | `given`, `given_stored`, `Fixture`, `Decision`, `project`, `project_transactional`, `stored_events`, `stored_events_at`, `StoredEvent`, `Database` (`testcontainers`) |

## Core signatures (verbatim)

```rust
pub trait Event: Serialize + DeserializeOwned + Schema {
    const EVENT_TYPE: &'static str;
}

pub trait State: Default + Clone + Send + 'static {
    type Event: Events;
    fn evolve(self, event: &Self::Event) -> Self;
    fn upcasters() -> Option<&'static Upcasters> { None }
    fn from_latest() -> Option<&'static str> { None }
}

pub trait Command {
    fn subject(&self) -> String;
    fn preconditions(&self) -> Vec<Precondition>;
}

impl<C, S: State, D> Decider<C, S, D> {
    pub fn new<F, Fut>(decide: F) -> Self
    where
        F: Fn(C, S) -> Fut + Send + Sync + 'static,
        Fut: Future<Output = Decision<S, D>> + Send + 'static,
}
```

```rust
impl Store {
    pub fn builder(client: Client, source: impl Into<String>) -> StoreBuilder;
    pub async fn load<S: State>(&self, subject: &str) -> Result<S, LoadError>;
    pub async fn execute<C, S, D>(&self, decider: &Decider<C, S, D>, command: C)
        -> Result<Vec<eventsourcingdb::Event>, ExecuteError<D>>
    where C: Command + Clone, S: State;
    pub async fn write(&self, events: Vec<EventOn>, preconditions: Vec<Precondition>)
        -> Result<Vec<eventsourcingdb::Event>, WriteError>;
    pub async fn register_schemas(&self, schemas: impl IntoIterator<Item = EventSchema>)
        -> Result<(), RegisterSchemasError>;
    pub fn start_projection<P: Projection>(&self, subjects: Subjects, projection: Arc<P>,
        token: CancellationToken, options: ProjectionOptions) -> ProjectionRun;
}
```

## Observations

- Kit types wrap or hand out client-SDK types directly
  (`eventsourcingdb::Client`, `eventsourcingdb::Event`,
  `eventsourcingdb::Precondition`) — the kit and the `eventsourcingdb` crate
  must be upgraded together.
- Traits use `async fn` in traits / RPITIT (`impl Future + Send`), no
  `async_trait`; projections are not object-safe (`dyn Projection` not possible).
- No `Context`/cancellation parameter in deciders (Go passes `ctx`).
