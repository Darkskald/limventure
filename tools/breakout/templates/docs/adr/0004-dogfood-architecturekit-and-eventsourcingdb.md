---
title: "ADR-0004: Dogfood architecturekit and EventSourcingDB"
summary: This repo is a test case for architecturekit, EventSourcingDB and ESDM — use them directly, track releases, and log every gap as upstream feedback instead of hiding it.
tags: [adr, architecturekit, eventsourcingdb, esdm, dogfooding, upstream-feedback]
status: accepted
updated: {{date}}
---

# ADR-0004: Dogfood architecturekit and EventSourcingDB

## Context

A purpose of this repository is to be a realistic test case for architecturekit,
EventSourcingDB and ESDM. Feedback is only valuable if friction stays visible.

## Decision

- Use architecturekit and the EventSourcingDB SDK **directly and idiomatically**. No
  abstraction layer whose only purpose is replaceability.
- Every gap, bug, papercut or doc mismatch is logged in
  [docs/upstream-feedback/](../upstream-feedback/) with a stable id (`AK-nnn`, `ESDB-nnn`,
  `ESDM-nnn`), a minimal repro and the workaround we use.
- Workarounds in code reference their feedback id in a comment (`// upstream: AK-nnn`).
- Before building around a gap, ask "should this be upstream?".
- Version policy: [ADR-0005](0005-exact-version-pins-with-deliberate-upgrades.md).

## Alternatives considered

| Option | Pros | Cons |
|---|---|---|
| Dogfood directly (this) | Real-world pressure on the tools, fast feedback loop | Upgrade churn hits us first |
| Anti-corruption layer around the kit | Swappable | Hides exactly the friction worth reporting |

## Consequences

- Breaking upstream changes are expected; the test suite must catch them.
- The feedback log is a first-class deliverable. Inherited entries come from earlier projects —
  re-verify them against the current pins before relying on them.
