---
title: "ADR-0002: ESDM as the domain model source"
summary: The domain model is written in ESDM YAML under model/, linted by the pinned esdm CLI, and is the reference for Rust code and docs.
tags: [adr, esdm, domain-model]
status: accepted
updated: 2026-10-28
---

# ADR-0002: ESDM as the domain model source

## Context

The product owner wants to try ESDM, a YAML-based event-sourced domain modeling language.
A machine-readable model lets agents and tools reason about the domain deterministically.

## Decision

- The model lives in `model/` (`*.esdm.yaml`, one artifact per file), schemas committed in
  `model/schemas/`.
- The `esdm` CLI is pinned (version + SHA256) and run via `limtool esdm …`.
- `limtool esdm lint` must be clean before a domain change is done.
- Code follows the model, not vice versa. Generators are a later option (ESDM itself is
  not a code generator).

## Alternatives considered

| Option | Pros | Cons |
|---|---|---|
| ESDM | Standard vocabulary, linter, AI-friendly | Very young (0.x), schema churn |
| Event Modeling / Miro boards | Visual, familiar | Not machine-checkable, drifts |
| Model only in Rust types | One source | Unreadable for domain experts |

## Consequences

- Schema upgrades (`esdm update-schema`) are explicit commits.
- Model and code can drift; a future `limtool` check should compare event names in
  `model/` with Rust event types.
