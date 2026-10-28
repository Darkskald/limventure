---
title: "ADR-0005: Exact version pins with deliberate upgrades"
summary: architecturekit, the EventSourcingDB SDK and server image, and the ESDM CLI are pinned exactly; each upgrade is a dedicated commit with an upgrade-log entry describing what broke.
tags: [adr, dependencies, versioning, upstream-feedback, dogfooding]
status: accepted
updated: {{date}}
---

# ADR-0005: Exact version pins with deliberate upgrades

## Context

The upstream tools are 0.x or move fast. Feedback is only useful if every breakage can be
attributed to exactly one upstream change ([ADR-0004](0004-dogfood-architecturekit-and-eventsourcingdb.md)).

## Decision

- Exact pins:
  - `Cargo.toml`: `architecturekit = "=x.y.z"`, `eventsourcingdb = "=x.y.z"`;
  - `infra/eventsourcingdb/docker-compose.yml`: image tag, never `latest`/`preview`;
  - `tools/src/{{tool}}/esdm.py`: `VERSION` + SHA256 per platform.
- `{{tool}} deps outdated` compares the pins with the latest upstream releases.
- One upgrade = one commit, nothing else in it. Message: `Upgrade <tool> a → b`.
- Each upgrade appends an entry to [upgrade log](../upstream-feedback/upgrade-log.md): what
  broke, how it was fixed, which feedback ids it resolves or creates.

## Alternatives considered

| Option | Pros | Cons |
|---|---|---|
| Exact pins, deliberate bumps (this) | Clean attribution, precise feedback | Manual effort per bump |
| Caret ranges | Breakage noticed sooner | Our and their changes mix; murky feedback |
| Track `latest` / git main | Earliest signal | Non-reproducible builds |

## Consequences

- Reproducible builds.
- Someone must run `deps outdated` regularly.
