---
title: ESDM upstream feedback
summary: Gaps, papercuts and wishes for the ESDM language, schemas and CLI found while dogfooding it in this repository, each with id, repro and current workaround.
tags: [upstream-feedback, esdm]
status: draft
updated: 2026-10-28
---

# ESDM upstream feedback

Policy: [ADR-0007](../adr/0007-dogfood-architecturekit-and-eventsourcingdb.md). Version tested: 0.15.0.
Background: [knowledge/esdm](../knowledge/esdm/overview.md).

| Id | Finding | Workaround here | State |
|---|---|---|---|
| ESDM-001 | Website says process-manager `endsWhen` entries are `{name, rule}`; schema requires `{name, condition}`. `startsWhen` documented as single ref, schema wants array | trust the schema | open |
| ESDM-002 | One wrong field inside an alternative shape (`oneOf`) produces many `unknown-field` errors on valid siblings | fix first odd field, re-lint | open |
| ESDM-003 | `$ref` to a non-existent value object in event/command payloads lints clean | review manually | open |
| ESDM-004 | No way to express tenant, actor, reason or signature metadata on events | prose / `metadata.labels` | open |
| ESDM-005 | Only one event kind — no distinction between domain and integration events | separate aggregates (`inbound-message`, …) + labels | open |
| ESDM-006 | Timers support `at: <field>` or fixed `after`, but not "field + offset" | — | open |
| ESDM-007 | `lint` exits 1 with "no esdm files found" on an empty model | seeded `model/domain.esdm.yaml` | open |
| ESDM-008 | `add-schema` / `update-schema` only operate on cwd (no `-d`) | `limtool esdm` runs inside `model/` | open |
| ESDM-009 | *PO.* Aggregates have no declarative **lifecycle end**: no `terminal` flag on events, no `endsWhen` on `aggregate` (only `process-manager.endsWhen`, `core/v1.yaml:1380`). "Disposed is final" can only be a prose invariant on every command, so tooling (lint, codegen, AK-016) cannot see it. Wish: `aggregate.endsWhen: [{name, event}]` mirroring the process manager, lint check that terminal events have no outgoing command except declared corrections | `invariants` prose on each command | open — confirmed |
| ESDM-010 | Aggregates and DCBs "may coexist and overlap" (`core/v1.yaml`, DCB block), but an aggregate cannot declare that its state also folds **free-standing events written by a DCB** to its subject. Consequence: an aggregate feature cannot use them in `given`. Repro: in `model/sample-management/sample.feature.esdm.yaml` add `given: [{event: aliquoted, …}]` → `esdm/gwt/scenario-references-unknown-event` ("not declared in the model"), although `aliquoted` is declared BC-wide. So "dispose an aliquot" is untestable at aggregate level. Wish: `aggregate.alsoFolds: [{boundedContext, event}]` (or scoped refs in aggregate `given`), and lint that a DCB's published events are folded by the aggregates it writes to | prose in `aggregate.description`; lifecycle of aliquots covered only via DCB features | open — confirmed |

## Template

`| ESDM-nnn | what, minimal repro | how we work around it | open/reported/fixed |`
