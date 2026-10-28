---
title: ESDM domain, subdomain and bounded context
summary: How ESDM models the domain, strategic subdomain classification and bounded contexts with a ubiquitous language, translations and rejected terms, with verified YAML.
tags: [esdm, ddd, strategic-design, bounded-context, ubiquitous-language, glossary]
status: draft
sources: [https://www.esdm.io/concepts/domain/, https://www.esdm.io/concepts/subdomain/, https://www.esdm.io/concepts/bounded-context/, https://www.esdm.io/reference/core-schema/bounded-context/, https://www.esdm.io/reference/core-schema/subdomain/, https://www.esdm.io/getting-started/running-esdm-glossary/]
updated: 2026-10-28
---

# Domain, subdomain, bounded context

- **Domain** – "what business are we in?". Exactly one per model is the intended use;
  no kind-specific fields. Content attaches by other documents' `scope`, not by lists.
- **Subdomain** – strategic classification `core | supporting | generic`, orthogonal to
  BCs (not a layer above them). Requires `scope`, `type`, `boundedContexts` (≥1).
- **Bounded context** – largest unit with one consistent vocabulary. Optional
  `ubiquitousLanguage`; if present, `language` (BCP 47) is required. One term per
  concept (no aliases); `avoid` lists rejected terms; `translations` give the same
  concept in other languages (one term per language).

Verified (excerpt from a lint-clean test model):

```yaml
apiVersion: schema.esdm.io/core/v1
kind: domain
name: lims
---
apiVersion: schema.esdm.io/core/v1
kind: subdomain
name: laboratory-operations
scope:
  domain: lims
type: core
boundedContexts: [sample-reception, analysis]
---
apiVersion: schema.esdm.io/core/v1
kind: bounded-context
name: sample-reception
scope:
  domain: lims
language: en
ubiquitousLanguage:
  - term: Sample
    definition: A physical specimen received by the laboratory, identified by its barcode.
    avoid:
      - term: Specimen
    translations:
      - language: de
        term: Probe
        definition: Ein physisches Untersuchungsobjekt, das das Labor erhält.
```

`esdm glossary --language de` then renders `### Probe` for this BC and marks terms
without a German translation with `_No translation into de._`.

Lint rules: `domain-without-bounded-context`, `bounded-context-without-content`,
`subdomain-without-bounded-context` (warnings), `duplicate-translation-language`,
`translation-into-own-language`.

## Relevance for the LIMS (own conclusion)

The `ubiquitousLanguage` block is the natural home for the LIMS glossary (currently
planned under `docs/domain/`): write it in English (code language) with `de`
translations for lab staff, and generate `esdm glossary --language de` instead of
maintaining a second glossary by hand. Cross-BC term correspondences go on context
mappings (`terms`), see [context-mapping.md](context-mapping.md).
