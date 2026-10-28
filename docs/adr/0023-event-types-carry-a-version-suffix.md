---
title: "ADR-0023: Event types carry a version suffix"
summary: Every event type, internal or published, ends in .vN; this fixes the event type scheme left open in ADR-0005; an ESDM event name ending in -vN maps to .vN, breaking changes get a new version and old versions are upcast on read.
tags: [adr, events, versioning, cloudevents, esdm, architecturekit]
status: accepted
updated: 2026-10-28
---

# ADR-0023: Event types carry a version suffix

## Context

[ADR-0005](0005-integration-events-are-persisted.md) left the event type scheme "TBD with the
model". [ADR-0012](0012-out-of-process-extensions.md) requires `.vN` for **published** events
only and leaves internal domain events free to change. The first ESDM slice
(`model/sample-management/`) used types without a suffix, while the walking-skeleton crate
already used `io.limventure.sampling.sample-registered.v1`.

Internal events are not free to change in practice: the event store keeps every stored event
forever, so a changed payload shape means old and new shapes coexist in the same stream.
ESDM has no version field. A changed event is a new event named `…-v2`. architecturekit
upcasters (`upcast.rs`) map one stored type to another on read and never write back.

## Decision

Product owner decision, 2026-10-28: **every** event type carries a version suffix.

| Event | CloudEvents type |
|---|---|
| Aggregate event | `io.limventure.<bounded-context>.<aggregate>-<event>.v<N>` |
| Free-standing (DCB) event | `io.limventure.<bounded-context>.<event>.v<N>` |
| Integration event | `io.limventure.integration.<partner>.<event>.v<N>` |

- Versions start at `.v1`.
- **ESDM mapping:** ESDM event `received` maps to `.v1`, and `received-v2` maps to `.v2`.
  Each version is its own ESDM event. The type goes in `metadata.annotations.cloudevents.type`.
- **Breaking change:** create a new version and add an architecturekit upcaster from the
  previous version to the new one. Stored events are never rewritten. Additive, optional
  fields stay within a version.
- Published events also follow ADR-0012: a deprecation period applies before a version is
  no longer emitted.

## Alternatives considered

| Option | Pros | Cons |
|---|---|---|
| `.vN` on all events (this) | One rule; the stored history is self-describing; upcasters key on the type | Longer type names; `.v1` everywhere even if a type never changes |
| `.vN` on published events only | Shorter internal types | Internal shape changes are invisible in the type; a two-rule scheme invites mistakes when an internal event gets published |
| Version in the payload | Type stays stable | ESDB schemas and upcasters key on the type; the version is hidden from filters and EventQL |

## Consequences

- **Audit:** every stored event names the exact contract it was written under. Readers
  years later can still interpret it.
- **Extensibility:** promoting an internal event to a published one (ADR-0012) needs no rename.
- ESDM event names gain a `-vN` suffix only from v2 onwards, so v1 names stay clean.
- `lims-sampling`'s `sample-registered.v1` already conforms. The model types are updated to `.v1`.

## Open points

- Deprecation period length for published versions (ADR-0012).
