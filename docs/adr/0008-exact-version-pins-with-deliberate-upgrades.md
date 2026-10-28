---
title: "ADR-0008: Exact version pins with deliberate upgrades"
summary: architecturekit, the EventSourcingDB SDK and server image, and the ESDM CLI are pinned exactly; each upgrade is a dedicated commit with an upgrade-log entry describing what broke.
tags: [adr, dependencies, versioning, upstream-feedback, dogfooding]
status: accepted
updated: 2026-10-28
---

# ADR-0008: Exact version pins with deliberate upgrades

Resolves the version-policy open point of [ADR-0007](0007-dogfood-architecturekit-and-eventsourcingdb.md).

## Context

The upstream tools are 0.x or move fast (architecturekit: 22 releases in ~28 h). As a test
case we want to follow them closely, but feedback is only useful if every breakage can be
attributed to exactly one upstream change.

## Decision

- Exact pins:
  - `Cargo.toml`: `architecturekit = "=x.y.z"`, `eventsourcingdb = "=x.y.z"`;
  - `infra/eventsourcingdb/docker-compose.yml`: image tag, never `latest`/`preview`;
  - `tools/src/limtool/esdm.py`: `VERSION` + SHA256 per platform.
- `limtool deps outdated` compares the pins with the latest upstream releases (deterministic).
- One upgrade = one commit, nothing else in it. Message: `Upgrade <tool> a → b`.
- Each upgrade appends an entry to [upgrade log](../upstream-feedback/upgrade-log.md): what
  broke, how it was fixed, which feedback ids it resolves or creates.
- Upgrade cadence: whenever `deps outdated` reports something and no feature work is mid-flight.

## Alternatives considered

| Option | Pros | Cons |
|---|---|---|
| Exact pins, deliberate bumps (this) | Clean attribution, precise feedback | Manual effort per bump |
| Caret ranges | Breakage noticed sooner | Our and their changes mix; murky feedback |
| Track `latest` / git main | Earliest signal | Non-reproducible builds; unusable in a regulated context |

## Consequences

- Reproducible builds — also a prerequisite for validated (GxP) releases later.
- Someone must run `deps outdated` regularly; candidate for a scheduled job.
