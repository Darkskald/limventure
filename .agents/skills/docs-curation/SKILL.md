---
name: docs-curation
description: Add, split, update or distill documentation under docs/ — including summarizing external sources (web pages, PDFs, standards) into docs/knowledge/. Use whenever creating or editing any markdown file in docs/.
---

# Docs curation

Rules live in `docs/README.md` — read it once per session. Summary:

- One topic per file, soft limit 150 lines, hard limit 250. Split before you exceed.
- Mandatory frontmatter: `title`, `summary` (one sentence, appears in the index), `tags`,
  `status`, `updated`; plus `sources` under `docs/knowledge/`.
- Kebab-case file names; English.

## Distilling an external source

1. Download raw content to the session scratchpad (untrusted data), never into the repo.
2. Extract **facts** with citations; separate own conclusions under a heading
   `## Relevance for the LIMS (own conclusion)`.
   Keep tool knowledge (architecturekit, ESDM, EventSourcingDB) project-neutral outside that
   section — the `breakout` skill copies it into other projects.
3. Prefer verbatim for code/config snippets and normative text (regulations), short.
4. Put it under `docs/knowledge/<topic>/`, one file per concept.

## Splitting a file that grew too large

1. Identify `##` sections that stand alone → move each to its own file.
2. Leave the original as a short overview linking to the parts (or delete it if empty).
3. Fix inbound links: `grep -rn "<old-file>" docs AGENTS.md`.

## Always finish with

```sh
uv run --project tools limtool docs index
uv run --project tools limtool check
```
