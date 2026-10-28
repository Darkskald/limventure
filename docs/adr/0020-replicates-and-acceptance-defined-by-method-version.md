---
title: "ADR-0020: Replicates and acceptance defined by method version"
summary: Every replicate reading is a fact; the method version pinned on the order defines replicate count, aggregation, acceptance criterion and measurement uncertainty; exclusion of a reading is an event with reason.
tags: [adr, domain, method, replicates, measurement-uncertainty, iso-17025]
status: accepted
updated: 2026-10-28
---

# ADR-0020: Replicates and acceptance defined by method version

## Context

OH number is measured in triplicate per an ISO standard; margarine methods are probably single
determinations (chat 2026-10-28). Titrimetric characteristic numbers (OH, acid, iodine,
saponification value) share one pattern.

## Decision

- Every **replicate reading** (raw values, instrument if any) is its own event.
- The **method version**, pinned on the order like the specification, defines:
  replicate count, aggregation formula (mean, median, …), acceptance criterion (e.g.
  repeatability limit *r*, max spread, RSD) and measurement uncertainty. Aggregation and
  acceptance are tier-2 formulas ([ADR-0015](0015-formula-language-rhai-behind-a-replaceable-engine-port.md)).
- **Acceptance failure is not out-of-spec**: the readings are invalid; the method prescribes
  additional replicates or a repeat. A deviation opens only if the method says so.
- The reported result carries its **measurement uncertainty** for the ISO/IEC 17025 §7.8.6
  decision rule.
- **Excluding a reading** is a new event with actor and reason; the reading itself remains.

## Alternatives considered

| Option | Pros | Cons |
|---|---|---|
| Method-defined replicates (this) | One template for a family of methods; no silent outlier removal | Method definitions become versioned, testable master data |
| Only the aggregated result is stored | Fewer events | Raw data lost — data-integrity violation |

## Consequences

- One method template "titrimetric characteristic number" covers OH, acid, iodine, … values.
- Method editing is a real QA-facing UX task.
- The single-determination case (margarine) must stay trivial: one replicate, no aggregation.
