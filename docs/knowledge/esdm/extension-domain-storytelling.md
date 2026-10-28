---
title: ESDM Domain Storytelling extension
summary: The domain-story kind for capturing discovery stories (actors, work objects, numbered sentences, groups, classification dimensions) as lintable ESDM documents, with verified YAML.
tags: [esdm, domain-storytelling, discovery, extension, workshop]
status: draft
sources: [https://www.esdm.io/extensions/domain-storytelling/introduction/, https://www.esdm.io/extensions/domain-storytelling/concepts/overview/, https://www.esdm.io/extensions/domain-storytelling/concepts/sentence/, https://www.esdm.io/extensions/domain-storytelling/concepts/work-object/, https://www.esdm.io/extensions/domain-storytelling/reference/overview/, https://www.esdm.io/extensions/domain-storytelling/reference/domain-story/]
updated: 2026-10-28
---

# Domain Storytelling extension

`apiVersion: schema.esdm.io/domain-storytelling/v1`, `kind: domain-story`, canon of
Hofer/Schwentner. A discovery artifact that precedes the core model; it validates
independently of the core and does not reference core elements.

- `scope: {domain}` (stories often cross BCs).
- Classifiers (optional, informational): `pointInTime: as-is | to-be`,
  `granularity: coarse-grained | fine-grained`, `domainPurity: pure | digitalized`.
  Discovery usually starts as-is / coarse-grained / pure.
- `sentences[]` (required): `sequenceNumber` (int ≥1; duplicates = parallel sentences),
  `edges[]` (required, flat list of `{from, to, label?, annotation?, groups?}`), optional
  `workObjects[]`.
- Node reference: `{actor: name}` or `{workObject: name}`. Actors are story-scoped (one
  icon per story), work objects sentence-scoped (redrawn per sentence).
- Declare `actors[]` / `workObjects[]` only when they need `annotation` or `groups`;
  inline references need no declaration.
- `groups[]`: `{name, description?, annotation?}`; membership via `groups: [name]` on
  actors, work objects, edges.
- `annotation` (in-diagram text) ≠ `metadata.annotations` (tooling).

Verified:

```yaml
apiVersion: schema.esdm.io/domain-storytelling/v1
kind: domain-story
name: sample-intake
scope:
  domain: lims
pointInTime: as-is
granularity: coarse-grained
domainPurity: pure
sentences:
  - sequenceNumber: 1
    edges:
      - from: { actor: customer }
        to: { workObject: sample }
        label: sends
      - from: { workObject: sample }
        to: { actor: lab-technician }
        label: to
  - sequenceNumber: 2
    edges:
      - from: { actor: lab-technician }
        to: { workObject: sample }
        label: registers
```

`esdm view` lists it as `domain-story sample-intake (as-is, coarse-grained, pure)  2
sentences`. Story actors are independent of core `actor` documents (here `customer` has
no core counterpart and no warning is raised).

## Relevance for the LIMS (own conclusion)

The customer scenarios in `docs/domain/examples/` (e.g. margarine incoming inspection)
can be transcribed 1:1 into as-is domain stories under `model/stories/`, giving the
grill/interview process a lintable intermediate artifact before aggregates are derived.
