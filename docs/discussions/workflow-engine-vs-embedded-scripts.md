---
title: "Open: workflow engine vs embedded scripts"
summary: Should customer-specific process logic run in a durable workflow engine (Temporal/Restate) or as sandboxed scripts triggered by events (Rhai/Lua/WASM)?
tags: [discussion, extensibility, workflow, scripting]
status: draft
updated: 2026-10-28
---

# Open: workflow engine vs embedded scripts

## Question

How do customers customize behavior — "when X happens, do Y" — without forking the core?

## Options (to be grilled, not decided)

| Option | Fit | Concerns |
|---|---|---|
| Embedded scripts on events (Rhai, Lua via mlua) | Simple, in-process, Rust-native (Rhai) | Long-running/timeout logic awkward; script versions must be audited |
| WASM components (wasmtime, WIT interfaces) | Strong sandbox, any language, deterministic | Tooling burden for customers |
| Process managers in Rust + declarative config (YAML rules) | Validatable, no Turing-complete customer code | Less flexible; every new rule shape is core work |
| Temporal / Restate | Durable timers, retries, long-running sagas | Second source of truth next to ESDB; ops burden; audit of workflow history |
| Event-sourced process managers with **expected events** as timers | Single source of truth, auditable | Must build scheduling ourselves |

## Consequences to weigh

- **Validation**: in GxP, every customer script is software that needs validation. Declarative
  rules are far cheaper to validate than code.
- **Determinism**: replaying events must not re-trigger side effects.
- **Audit**: script/rule version that produced a decision must be recorded in the event.
- **Tenancy**: scripts are per tenant; isolation and resource limits.

## Own initial take (not agreed)

Layered: declarative rules first (covers catalog decisions, signature requirements, routing),
WASM/Rhai hooks for the remaining 20 %, durable timers via [expected events](expected-events.md).
Temporal only if long-running cross-system sagas prove unmanageable.
