---
title: Documentation conventions
summary: Layout, frontmatter and size rules for every markdown file under docs/.
tags: [harness, docs, conventions]
status: accepted
updated: 2026-10-28
---

# Documentation conventions

Everything that is not code lives here: ADRs, domain knowledge, distilled external
sources, open discussions. The generated index is [INDEX.md](INDEX.md) — never edit it
by hand, run `uv run --project tools limtool docs index`.

## Layout

| Directory            | Content                                                         |
|----------------------|-----------------------------------------------------------------|
| `adr/`               | Architecture Decision Records, `NNNN-kebab-title.md`            |
| `vision/`            | Product goals, guiding principles, "exotic sparks"              |
| `domain/`            | Domain: stakeholders, requirements, glossary, examples          |
| `domain/examples/`   | Concrete customer scenarios used to validate the model          |
| `knowledge/<topic>/` | Distilled knowledge from external sources (always cite sources) |
| `harness/`           | How the AI harness, tools and skills work                       |
| `discussions/`       | Open questions and unresolved debates — one file per question   |
| `upstream-feedback/` | Findings for architecturekit / EventSourcingDB / ESDM (ADR-0007) |

## Rules

1. **Atomic.** One topic per file. If you need a second `##` topic, it is a second file.
2. **Small.** Soft limit 150 lines, hard limit 250 (enforced by `limtool docs lint`). Split, don't grow.
3. **Frontmatter is mandatory** — the index and search depend on it:

   ```yaml
   ---
   title: Human-readable title
   summary: One sentence, used verbatim in INDEX.md and search results.
   tags: [lowercase, kebab-case]
   status: draft | proposed | accepted | superseded | deprecated
   sources: [https://...]   # required under knowledge/
   updated: YYYY-MM-DD
   ---
   ```

4. **Link, don't repeat.** Use relative links to other docs instead of restating them.
5. **Cite.** Anything under `knowledge/` lists its `sources`. Mark own conclusions as such.
6. **English only.** The codebase and docs are English; end-user i18n is a product feature, not a docs concern.
7. **Kebab-case file names**, no spaces, no umlauts.

## ADRs

Use the template from `limtool adr new "<title>"`. Status flow:
`proposed` → `accepted` (only after explicit agreement with the product owner) → `superseded`.
An ADR is never edited after acceptance except for its status and a `superseded-by` link.
