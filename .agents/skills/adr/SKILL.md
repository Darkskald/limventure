---
name: adr
description: Create, update or supersede Architecture Decision Records in docs/adr/. Use when a design decision is proposed, agreed, changed, or when someone asks "why did we do X".
---

# ADR

1. Check existing decisions: `uv run --project tools limtool docs search <terms> --tag adr`.
2. New ADR: `uv run --project tools limtool adr new "<Decision title>"` — fills the template
   with the next number. Never hand-number.
3. Fill every section. "Alternatives considered" needs ≥2 real alternatives.
   "Consequences" must state audit/compliance and extensibility impact.
4. `status: proposed` until the product owner explicitly agrees → then `accepted`.
   Agreement in chat is enough; note the date in `updated`.
5. Accepted ADRs are immutable. To change: write a new ADR, set the old one to
   `superseded` and add `superseded-by: NNNN` to its frontmatter.
6. Keep it ≤150 lines; link knowledge docs instead of copying them.
7. Finish with `uv run --project tools limtool docs index` and `limtool check`.
