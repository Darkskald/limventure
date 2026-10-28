---
name: upstream-feedback
description: Record, verify and curate feedback on architecturekit, EventSourcingDB (server + Rust SDK) or ESDM in docs/upstream-feedback/. Use when the user remarks on an API, bug, missing feature, doc mismatch or papercut in these tools ("feedback:", "this should…", "I stumbled upon…"), or when you hit such friction yourself while working.
---

# Upstream feedback

Policy: `docs/adr/0007-dogfood-architecturekit-and-eventsourcingdb.md`. This repo is a
realistic test case for the tools; the feedback log is a deliverable the tool author reads.
Quality bar: every entry is **verified against the pinned version** and states a verdict.

## Files

| Tool | File | Id prefix |
|---|---|---|
| architecturekit | `docs/upstream-feedback/architecturekit.md` | `AK-` |
| EventSourcingDB server + Rust SDK | `docs/upstream-feedback/eventsourcingdb.md` | `ESDB-` |
| ESDM language / schemas / CLI | `docs/upstream-feedback/esdm.md` | `ESDM-` |
| Version bumps | `docs/upstream-feedback/upgrade-log.md` | — |

## Procedure

1. **Split** the remark into atomic findings — one id per finding.
2. **Check for duplicates**: `uv run --project tools limtool docs search <terms> --tag upstream-feedback`.
   Extend an existing row instead of adding a near-duplicate.
3. **Verify against the pinned source**, not memory or the website:
   - Pinned versions: `Cargo.toml` (`=x.y.z`), compose image tag, `tools/src/limtool/esdm.py`.
   - Rust sources: `~/.cargo/registry/src/*/architecturekit-<ver>/src`,
     `~/.cargo/registry/src/*/eventsourcingdb-<ver>/src` (run `cargo fetch` if missing).
   - Server behavior: `limtool esdb up --dev` and try it. ESDM: `limtool esdm …` in a scratch model.
   - Cite `file:line` of the pinned version.
4. **Verdict** — be honest, the user wants pushback, not applause:
   - `confirmed` — the premise holds; say why it matters (correctness > ergonomics > perf).
   - `partially confirmed` — say which part holds and which doesn't (e.g. "allocation cost is
     negligible, but the signature is still too rigid").
   - `rejected` — premise is wrong or already solved; point to the existing API. Do **not**
     log rejected items in the table; tell the user and, if useful, add a knowledge note.
5. **Write the row**: origin (`*PO.*` for the product owner, nothing for agent findings),
   what + minimal repro or code location, a concrete wish (what API would fix it), our
   workaround, `open — <verdict>`.
6. **Link code workarounds**: comment `// upstream: AK-nnn` at the workaround site.
7. Finish: `uv run --project tools limtool docs index && uv run --project tools limtool check`.
8. **Report back** in a short table: id, verdict, one-line reason.

## States

`open` → `reported` (passed to the author; add date/link) → `fixed in <version>` (remove the
workaround, note it in the upgrade log) or `wontfix` (keep the reason).

## Don'ts

- No speculative entries ("might be slow") without a measurement or a concrete failure.
- No filing GitHub issues or contacting anyone unless the user explicitly asks.
- Don't soften a confirmed finding because the author is known to the user.
