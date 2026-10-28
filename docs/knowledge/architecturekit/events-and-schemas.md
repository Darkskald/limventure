---
title: architecturekit events, schemas and upcasting
summary: How architecturekit defines events, derives immutable JSON schemas for EventSourcingDB, and versions events with upcasters.
tags: [architecturekit, rust, events, json-schema, upcasting, versioning]
status: draft
sources: [https://docs.rs/architecturekit/0.21.0, https://github.com/thenativeweb/architecturekit-rust, https://github.com/thenativeweb/architecturekit-golang]
updated: 2026-10-28
---

# Events, schemas and upcasting

## Event

An event is a serde struct with a derived `Event` that names its event type:

```rust
#[derive(Serialize, Deserialize, Event)]
#[event(type = "io.eventsourcingdb.library.book-acquired")]
struct BookAcquired { title: String, author: String }
```

`trait Event: Serialize + DeserializeOwned + Schema { const EVENT_TYPE: &'static str; }`.
Events can not be generic (one type = one data shape). The type string is the
EventSourcingDB `type` field.

## Events enum

The events of one state/projection are listed in an enum with one newtype
variant per event type; `#[derive(Events)]` implements `schemas()`,
`event_type()`, `to_data()`, `from_data()`. The derive refuses two variants with
the same event type at compile time. An event of a type that is not in the
enum is **silently skipped** when reading.

## Schema derivation

`Event` also derives `Schema` (JSON Schema). `Store::register_schemas` registers
them in EventSourcingDB, which then rejects non-conforming writes. Registered
schemas are **immutable**, so the derive rules are frozen across kit versions.
Rules (abridged from `Schema` docs):

- Named-field struct → object, `required` = all fields except those with
  `skip_serializing_if`; `additionalProperties: false`. Honors `rename`,
  `rename_all`, `skip`, `transparent`.
- Primitives, `Vec`/sets → array, maps → object, `Option` → nullable,
  chrono `DateTime` → `date-time` string, `serde_json::Value` → anything.
- **Not derivable** (compile error → implement `Schema` by hand): enums,
  unions, unit/tuple structs, `tag`/`content`/`flatten`/`with` attributes,
  recursive types. Nested structs derive `Schema` separately.
- EventSourcingDB reads numbers as f64: integers beyond 2^53-1 lose precision
  silently — store them as strings.

Hand-written `Schema` is how to add patterns/formats (e.g. ID regex).

## Versioning with upcasters

A changed shape means a **new event type** (e.g. `...book-acquired.v2`) plus an
upcaster; schemas can not be changed in place.

```rust
static UPCASTERS: LazyLock<Upcasters> = LazyLock::new(|| {
    Upcasters::new().upcast("io.eventsourcingdb.library.book-acquired.v1", |event| {
        let title = event.data()["title"].clone();
        Ok::<_, std::convert::Infallible>(vec![
            event.with_type("io.eventsourcingdb.library.book-acquired.v2")
                 .with_data(json!({ "title": title, "author": "unknown" })),
        ])
    })
});
```

- One shared set per application, referenced from `State::upcasters()` and
  `Projection::upcasters()` so write and read side see the same events.
- Upcasters work on `UpcastEvent` (type, JSON data, subject, id, time, source),
  can split one event into several (`Envelope::part` = position), are chained
  (max 16 steps), and never write back.
- Registering the same source type twice panics at build time.

## Time

States and projections must never read the clock; deciders receive a clock
(Go docs: "Using the Current Time") and write time-derived facts into events.
The database-recorded write time is available as `Envelope::time`.
