---
title: "ADR-0021: Calculated results declare explicit dependencies"
summary: Formulas declare their input results in bindings, forming an explicit per-sample dependency graph; calculated results record input and formula versions; upstream changes supersede downstream results and trigger amended reports.
tags: [adr, domain, formula, dependencies, amended-report, iso-17025]
status: accepted
updated: 2026-10-28
---

# ADR-0021: Calculated results declare explicit dependencies

## Context

The OH number is corrected by the acid value of the same sample; the margarine price bonus
depends on all three analyses ([ADR-0014](0014-lims-owns-release-and-quality-pricing.md)).
The product owner requires the dependency graph to be explicit and visible in the formula
editor (chat 2026-10-28).

## Decision

- Formula **bindings** declare input results (e.g. `result(acid_value, same sample)`)
  ([ADR-0015](0015-formula-language-rhai-behind-a-replaceable-engine-port.md)). Ordering a test
  pulls in its dependencies as visible tests on the order.
- Dependencies form a **graph per sample**; cycles are rejected when the method is saved.
- A calculated result is a **fact** recording the exact input result versions and formula
  version it used.
- If an input changes (correction, retest), the dependent result is **marked superseded** and
  a new one is calculated as a new event — never silently recalculated in place.
- If a superseded result was already reported, an **amended report** is required
  (ISO/IEC 17025 §7.8.8).

## Alternatives considered

| Option | Pros | Cons |
|---|---|---|
| Declared graph, supersede (this) | Explicit, editor can draw it, full lineage | Dependency resolver in the core |
| Implicit references in formula text | Familiar from legacy LIMS | Graph invisible, breaks silently — the pain point to avoid |
| Recalculate in place | Simple | Destroys history; violates immutability |

## Consequences

- The quality-based price is the same mechanism one level up.
- Amended reports are needed from day one.
