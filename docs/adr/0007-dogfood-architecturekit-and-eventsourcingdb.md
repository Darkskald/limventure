---
title: "ADR-0007: Dogfood architecturekit and EventSourcingDB"
summary: Besides the LIMS itself, this repo is a realistic test case for architecturekit and EventSourcingDB — use them directly, track the latest releases, and log every gap as upstream feedback instead of hiding it.
tags: [adr, architecturekit, eventsourcingdb, esdm, dogfooding, upstream-feedback]
status: accepted
updated: 2026-10-28
---

# ADR-0007: Dogfood architecturekit and EventSourcingDB

Partially supersedes the "wrap it behind our own thin domain traits" consequence of
[ADR-0001](0001-rust-on-eventsourcingdb-and-architecturekit.md).

## Context

The product owner is in direct contact with the author of architecturekit, EventSourcingDB
and ESDM. A second purpose of this repository is to be a **realistic, demanding test case**
for these tools — regulated domain, multi-tenancy, audit trail, integrations.

## Decision

- Use architecturekit and the EventSourcingDB SDK **directly and idiomatically**. No
  abstraction layer whose only purpose is replaceability.
- Track recent releases; upgrades are deliberate commits with a note on what broke.
- Every gap, bug, papercut or doc mismatch is logged in
  [docs/upstream-feedback/](../upstream-feedback/) with a stable id (`AK-nnn`, `ESDB-nnn`,
  `ESDM-nnn`), a minimal repro and the workaround we use.
- Workarounds in our code reference their feedback id in a comment, so they can be removed
  when upstream fixes land.
- Where the LIMS needs something the tools lack, first ask "should this be upstream?"
  before building it locally.

## Alternatives considered

| Option | Pros | Cons |
|---|---|---|
| Dogfood directly (this) | Real-world pressure on the tools, fast feedback loop | Upgrade churn hits us first |
| Anti-corruption layer around the kit | Swappable | Hides exactly the friction worth reporting |
| Freeze versions | Stability | Feedback goes stale against moving upstream |

## Consequences

- Breaking upstream changes are expected and acceptable; the test suite must catch them.
- The feedback log is a first-class deliverable, reviewed like code.

## Open points

- Version policy: exact pin with frequent bumps vs caret range — see open question in chat.
- Whether feedback items are filed as GitHub issues by agents or curated by the PO.
