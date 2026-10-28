---
title: ESDM project layout, files and schemas
summary: File suffix, multi-document files, schema modelines, the schemas/ directory written by add-schema, drift detection, and the recommended by-bounded-context directory layout.
tags: [esdm, project-layout, schemas, conventions, editor]
status: draft
sources: [https://www.esdm.io/getting-started/editor-support/, https://www.esdm.io/reference/core-schema/overview/, https://www.esdm.io/reference/cli/, https://www.esdm.io/reference/linter-rules/, https://www.esdm.io/getting-started/your-first-model/]
updated: 2026-10-28
---

# ESDM project layout, files and schemas

## Files

- Suffix **`.esdm.yaml`** (`x-esdm-file-suffix`). Other `.yaml` files are ignored, so
  the schemas themselves are never linted as model.
- One file may hold several documents separated by `---` (`x-esdm-document-separator`).
  ESDM's own guide uses one artifact per file; the schema leaves granularity open.
- Every document: `apiVersion`, `kind`, `name` (required), optional `description`,
  `metadata.labels`, `metadata.annotations` (string maps, non-semantic). Unknown keys
  are errors (`unevaluatedProperties: false`).
- `apiVersion`: `schema.esdm.io/core/v1`, `schema.esdm.io/given-when-then/v1`,
  `schema.esdm.io/domain-storytelling/v1`. `kind` disambiguates within a schema.
- References are **logical** (names + scope), never file paths: files can be split,
  merged and moved freely.

## Schemas directory (`esdm add-schema`)

Run in the project root (cwd); it writes:

```
schemas/
├── core/v1.yaml                 # 1889 lines, revision 1.0.0
├── given-when-then/v1.yaml      # 619 lines
└── domain-storytelling/v1.yaml  # 267 lines
```

Template `schemas/{name}/{version}.yaml` (`x-esdm-project-layout`). Commit it.

**Drift check (verified):** if `<lint dir>/schemas/` exists, `esdm lint` compares it
**byte-for-byte** with the embedded schemas and aborts with
`esdm/system/schemas-directory-drift` (error) on *any* difference – even a comment edit.
Without a `schemas/` dir, lint simply runs. `update-schema` overwrites older revisions
and refuses newer ones. Never edit the schema files.

## Editor modeline

```yaml
# yaml-language-server: $schema=./schemas/core/v1.yaml
apiVersion: schema.esdm.io/core/v1
kind: aggregate
```

Path is relative to the file (`../schemas/...` one level down). One modeline per
document in multi-doc files. Optional – lint does not need it.

## Recommended layout (`x-esdm-project-layout.document-organization`)

- **Primary axis: bounded context** – one top-level directory per BC. Do *not* group
  by kind (`commands/`, `events/`).
- **Cross-context bucket: `integration/`** – policies, process managers, event handlers
  and context mappings (domain-scoped, BC-spanning).
- Inside a BC, group by consistency unit (one file per unit, per kind, or a dir per unit).
- External systems: a flat catalog `external-systems.esdm.yaml` at the domain root.
- Not enforced by the linter.

Verified example (lints clean):

```
model/
├── schemas/                       # esdm add-schema
├── domain.esdm.yaml               # domain + subdomain
├── external-systems.esdm.yaml
├── sample-reception/
│   ├── bounded-context.esdm.yaml
│   ├── actors.esdm.yaml
│   ├── sample.esdm.yaml           # aggregate + its commands + events
│   ├── sample.feature.esdm.yaml   # given-when-then next to the unit
│   └── read-models.esdm.yaml      # read model + query
├── analysis/ ...
├── integration/                   # policy, process manager, handler, mappings
└── stories/sample-intake.esdm.yaml
```

## Relevance for the LIMS (own conclusion)

Repo convention: model root = `model/`, schemas = `model/schemas/` (committed), wrapper
runs in `model/`. Modelines then read `./schemas/...` at the root and
`../schemas/...` inside BC directories. A schema bump is a separate commit:
new binary pin + `update-schema` output.
