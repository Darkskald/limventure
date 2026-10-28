---
title: ESDM upstream feedback
summary: Gaps, papercuts and wishes for the ESDM language, schemas and CLI found while modeling the LIMS, each with id, repro and current workaround.
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

## Template

`| ESDM-nnn | what, minimal repro | how we work around it | open/reported/fixed |`
