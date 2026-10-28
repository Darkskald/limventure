---
title: architecturekit upstream feedback
summary: Gaps, papercuts and wishes for architecturekit (Rust) found while building the LIMS, each with id, repro and current workaround.
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

## Template

`| AK-nnn | what, minimal repro | how we work around it (file:line) | open/reported/fixed |`
