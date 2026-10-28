---
title: architecturekit upstream feedback
summary: Gaps, papercuts and wishes for architecturekit (Rust) found while dogfooding it in this repository, each with id, repro and current workaround.
tags: [upstream-feedback, architecturekit, rust]
status: draft
updated: 2026-10-28
---

# architecturekit upstream feedback

Policy: [ADR-0007](../adr/0007-dogfood-architecturekit-and-eventsourcingdb.md). Version tested: 0.21.0.
Details on most items: [go vs rust gaps](../knowledge/architecturekit/go-vs-rust-gaps.md).

| Id | Finding | Workaround here | State |
|---|---|---|---|
| AK-001 | `Store` writes no metadata beyond source/subject/type/data (`traceinfo: None`); no place for actor, reason, correlation | `lims_kernel::Audit` embedded in every event payload | open |
| AK-002 | `Schema` derive rejects enums and `tag`/`content`/`flatten`/`with` — even a simple `Actor::User \| System` enum fails | `Actor` as struct with `kind: String` | open |
| AK-003 | No process managers / sagas / policies | resumable projections, at-least-once + event-id dedup (planned) | open |
| AK-004 | Only in-memory views (`InMemoryView`, `InMemoryIndex`) | none yet | open |
| AK-005 | No multi-tenancy concept beyond subject paths; no authorization hooks | tenant-first subjects via `lims_kernel::subject` | open |
| AK-006 | Rust lacks Go v2 features: query combinators, user abstraction in HTTP layer, schemas from files, context in deciders | — | open |
| AK-007 | Public API re-exports `eventsourcingdb` 4.x types → lock-step upgrades; pulls reqwest 0.12 and 0.13 | — | open |
| AK-008 | Cross-subject uniqueness via EventQL precondition surfaces as 409 conflict, not as a domain refusal | — | open |
| AK-009 | Logs via `log` only, no `tracing` spans | — | open |
| AK-010 | Much guidance (time, publishing, batching) only documented in the Go README | — | open |
| AK-011 | No timers / scheduled commands / durable scheduler (needed for expected events, ADR-0013) | own scheduler from projection of open expectations (planned) | open |
| AK-012 | *PO.* `Command::subject()` returns `String`; there is **no `Subject` newtype in architecturekit or the eventsourcingdb crate**. `SubjectScheme::build` also **panics** on invalid values (`subject.rs:160`) and has no fallible `try_build`/`parse` → invalid ids from user input crash instead of refuse; ids can't be parsed back out of a subject. Wish: `Subject` newtype produced by a fallible scheme build, accepted by `Command`/`Precondition`/`Subjects` | `lims_kernel::subject()` returns `Result<String>` | open — confirmed |
| AK-013 | *PO.* `Command::preconditions()` returns a fresh `Vec<Precondition>`. A `&'static` slice is not possible (preconditions own per-command subjects/event ids), and the allocation is negligible next to the HTTP round-trip — but `impl IntoIterator<Item = Precondition>` would allow arrays (`[p]`) with no API cost | — | open — partially confirmed (ergonomics, not perf) |
| AK-014 | *PO.* No closure-based subscription. Filtering exists (`start_projection(Subjects, Arc<P>, CancellationToken, ProjectionOptions)` + event enum), but every handler needs a struct + `Projection` impl with `Event`/`Error` associated types. Wish: `store.on_event::<E>(subjects, \|env\| async { … })` (+ sync variant) returning `ProjectionRun` | — | open — confirmed (ergonomics) |
| AK-015 | *PO.* CloudEvents fields underused: writes set `traceinfo: None` (`store.rs:632`) although projections *read* `traceparent` → traces never propagate write→read; `source` is fixed per `Store` (`Store::builder(client, source)`), so per-partner sources for inbound integration events (ADR-0005) need one store per source. Wish: traceparent from current span/context, per-command source override | separate stores per source (planned) | open — confirmed |

## Template

`| AK-nnn | *origin.* what, minimal repro, verdict basis | how we work around it (file:line) | open/reported/fixed — verdict |`
