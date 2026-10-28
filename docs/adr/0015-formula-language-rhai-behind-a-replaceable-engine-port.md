---
title: "ADR-0015: Formula language Rhai behind a replaceable engine port"
summary: Tier-2 formulas are structured bindings (inputs, units, sources) plus a script body; the body runs in a hardened Rhai engine behind a language-agnostic port so the language can be swapped later.
tags: [adr, extensibility, formula, scripting, determinism]
status: accepted
updated: 2026-10-28
---

# ADR-0015: Formula language Rhai behind a replaceable engine port

## Context

[ADR-0011](0011-extensibility-tiers.md) mandates a pure, deterministic tier-2 formula
language and left the choice open. Product owner requirements (chat 2026-10-28, OH-number
walkthrough — [example](../domain/examples/oh-number-determination.md)):

- Script-like and readable, not the free-text `v*ph*2*call_obscure_function(...)` fields of
  legacy LIMS ([pain points](../knowledge/lims/legacy-ux-pain-points.md)).
- The dependency graph (result → result, e.g. OH number corrected by acid value) must be
  explicit and visible in the formula editor.
- Modularity: the language may be replaced later.

Incumbents use proprietary languages (LabWare LIMS Basic, STARLIMS SSL, SampleManager VGL)
or unrestricted Groovy (LabVantage, SLIMS, Clarity) — own research 2026-10-28, sources in chat.

## Decision

1. **A formula version = bindings + body + tests.**
   - *Bindings* (structured, tier-1 style): output and each input with name, unit and source
     (`replicate(..)`, `result(..)`, `reagent(..)`, constant). The dependency graph is derived
     from bindings only, never by parsing the body.
   - *Body*: script that may reference declared names only; unknown names fail on save.
   - *Tests*: given-inputs → expected-output cases, run on save; they are validation evidence.
2. **Units are checked by the core**, not the language: a body whose result unit does not
   match the declared output cannot be saved.
3. **The body language is Rhai** (`rhai`, exact pin per [ADR-0008](0008-exact-version-pins-with-deliberate-upgrades.md)),
   hardened: `default-features = false` (drops `ahash/runtime-rng`), features `std`, `no_time`,
   `libm`; `Engine::new_raw()` with only the math packages we register; operation and depth
   limits set.
4. **Engine port.** The core talks to a `FormulaEngine` trait (compile/check, evaluate);
   Rhai is one adapter. Each formula version records `language` and engine version.
5. **Numerics.** Calculation in f64 with transcendental functions routed through pure-Rust
   `libm`; rounding for reporting is decimal and done by the core, never in the body.

## Alternatives considered

| Option | Pros | Cons |
|---|---|---|
| Rhai (this) | Rust-native, no I/O unless registered, operation limits, stable 1.x | Dynamic typing; purity needs feature hardening |
| Starlark (`starlark`) | Deterministic by spec, Python-like | 0.x crate, sparse docs outside Buck2 |
| Luau via `mlua` | Built-in sandbox mode, gradual types | Lua dialect, C++ VM, std-lib surface to audit |
| CEL | Non-Turing-complete, always terminates | Expressions only — candidate for tier-1 limit expressions, not bodies |
| Own DSL | Full control incl. units | A language to maintain forever |

## Consequences

- Calculated results are stored as facts with formula version and input result versions, so
  an engine switch never changes history; old versions keep their `language` tag.
- Switching language = new formula versions in the new language, proven equivalent by
  re-running the existing test cases; the old adapter stays as long as old versions must be
  re-verifiable.
- The formula editor (bindings form + graph view + code editor + test runner) is significant
  frontend work.
- Rhai-specific gaps go to `docs/upstream-feedback/` like the other dogfooded tools.

## Open points

- Whether CEL is used for tier-1 limit / decision-rule expressions — separate decision.
- Unit system implementation (own quantity type vs crate) — to be spiked.
