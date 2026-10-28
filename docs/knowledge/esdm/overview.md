---
title: ESDM overview
summary: What ESDM (Event-Sourced Domain Modeling) is, what it is not, its design principles, and a map of the other ESDM notes.
tags: [esdm, domain-model, ddd, event-sourcing, overview]
status: draft
sources: [https://www.esdm.io/introduction/what-is-esdm/, https://www.esdm.io/introduction/design-principles/, https://www.esdm.io/introduction/use-cases/, https://www.esdm.io/introduction/license/, https://www.esdm.io/ecosystem/]
updated: 2026-10-28
---

# ESDM overview

ESDM is a YAML modeling language plus a single CLI binary (`esdm`, by *the native web*,
MIT licensed) for describing event-sourced domains: Domains, Bounded Contexts,
Aggregates, Dynamic Consistency Boundaries, Commands, Events, Process Managers, Read
Models, Context Mappings and more. Version researched: **0.15.0**, schema revision
`1.0.0` for core and both extensions.

**Not** an event store, runtime, framework or code generator. It is a static,
descriptive layer that lives next to the code and is linted in CI.

## Design principles (from the docs)

- **The model is files, not a service.** `.esdm.yaml` in the repo, fully offline
  (only exception: a once-a-day update check, see [installation](installation.md)).
- **The schema is the contract.** `apiVersion` pins a document to a schema embedded in
  the binary. Non-breaking changes bump `x-esdm-schema-revision`; breaking changes would
  bump the `apiVersion` major (Kubernetes-style API groups).
- **Extensions sit beside the core.** Given-When-Then and Domain Storytelling have
  their own `apiVersion`s; they never add kinds to the core. Not user-extensible.
- **Rules are fixed.** No config file, no disabling, no severity overrides.
- **Diagnostics are locations** (`file:line:col`), not stack traces.

## Core kinds (18)

`domain`, `subdomain`, `bounded-context`, `context-mapping`, `aggregate`,
`dynamic-consistency-boundary`, `command`, `event`, `event-handler`, `policy`,
`process-manager`, `read-model`, `query`, `entity`, `value-object`, `domain-service`,
`actor`, `external-system`. Extension kinds: `feature` (given-when-then),
`domain-story` (domain-storytelling).

Rules that do not fit a grammar (invariants, emission logic, projection effects, ...)
are **prose**: `namedRule {name, rule}`, `namedCondition {name, condition}`, or
`rule`/`criteria` fields. ESDM models the *what*; the implementation provides the *how*.

## Map of notes

| Topic | Note |
|---|---|
| Download, checksums, update check | [installation.md](installation.md) |
| CLI subcommands and flags | [cli.md](cli.md) |
| Files, directories, schemas | [project-layout-and-files.md](project-layout-and-files.md) |
| Names, scopes, `esdm:` references | [naming-and-references.md](naming-and-references.md) |
| Domain, subdomain, bounded context | [strategic-design.md](strategic-design.md) |
| Aggregate, DCB, entity | [consistency-units.md](consistency-units.md) |
| Command, event, actor | [commands-events-actors.md](commands-events-actors.md) |
| Read model, query | [read-side.md](read-side.md) |
| Value object, domain service | [value-objects-and-domain-services.md](value-objects-and-domain-services.md) |
| Policy, event handler | [policies-and-event-handlers.md](policies-and-event-handlers.md) |
| Process manager, timers | [process-managers-and-timers.md](process-managers-and-timers.md) |
| External system, context mapping | [context-mapping.md](context-mapping.md) |
| Linter rule catalog | [linter-rules.md](linter-rules.md) |
| Given-When-Then extension | [extension-given-when-then.md](extension-given-when-then.md) |
| Domain Storytelling extension | [extension-domain-storytelling.md](extension-domain-storytelling.md) |
| Modeling with an AI agent | [ai-workflow.md](ai-workflow.md) |
| Mapping to LIMS concerns (own conclusions) | [lims-mapping.md](lims-mapping.md) |

## Ecosystem

Only listed third-party tool: **ESDM Visualizer** (Impierce Technologies, Apache-2.0),
`docker run -p 3000:3000 -v .:/data impierce/esdm-visualizer`, verified with 0.15.0.
"Modeling Guides" and "Recipes" sections of the site are still empty (in preparation).

## Doc/binary discrepancies found

- Reference page for `process-manager` says `endsWhen` entries are `{name, rule}` and
  `startsWhen` is a single reference. The embedded schema (authoritative, verified with
  `esdm lint`) uses `{name, condition}` and an **array** for `startsWhen`.
- Always trust `model/schemas/core/v1.yaml` over the website.
