# AGENTS.md — limventure

Event-sourced, extensible LIMS (laboratory information management system) in Rust on
EventSourcingDB + architecturekit, domain modeled in ESDM. This file is the single source
of agent instructions for **Codex and Claude Code** (`CLAUDE.md` only imports it).

## Mission (non-negotiable)

1. Pleasant UX for every stakeholder — analysts, lab heads, QA, data scientists, controllers.
2. Audit-trail readiness — every fact is an attributable, immutable event.
3. Extensibility — customer customization without forking the core.

Details: [docs/vision/product-vision.md](docs/vision/product-vision.md).

**Second purpose:** this repo is a realistic test case for EventSourcingDB, architecturekit and
ESDM ([ADR-0007](docs/adr/0007-dogfood-architecturekit-and-eventsourcingdb.md)). Use them
directly and idiomatically — no wrapper layers. Every gap, bug, papercut or doc mismatch you hit
goes into `docs/upstream-feedback/<tool>.md` (id, repro, workaround), and code workarounds carry
a `// upstream: AK-nnn` comment. Ask "should this be upstream?" before building around a gap.

## Working agreement: grill, don't guess

The product owner explicitly wants pushback. Before implementing anything non-trivial:

- Restate the requirement and its **consequences** (audit, multi-tenancy, extensibility, UX).
- Ask until ambiguities are gone; one focused question at a time beats a questionnaire.
- Never silently pick an architecturally relevant option — propose an ADR (`status: proposed`)
  and get explicit agreement before marking it `accepted`.
- Record unresolved questions in `docs/discussions/` (one file per question).
- Skill: `.agents/skills/grill/`.

## Repository map

| Path                     | Purpose                                                     |
|--------------------------|-------------------------------------------------------------|
| `docs/`                  | All docs, ADRs, knowledge. Start at `docs/INDEX.md`         |
| `model/`                 | ESDM domain model (`*.esdm.yaml`), schemas in `model/schemas/` |
| `crates/`                | Rust workspace members                                      |
| `infra/eventsourcingdb/` | docker compose for EventSourcingDB                          |
| `tools/`                 | `limtool` — deterministic Python tooling (uv project)       |
| `.agents/skills/`        | Agent skills (Codex reads here; `.claude/skills` symlinks here) |

## Finding knowledge — don't load everything

Docs are atomic and indexed. Do **not** read whole directories.

```sh
uv run --project tools limtool docs search <terms> [--tag t]   # ranked hits with summaries
```

Then read only the hits. `docs/INDEX.md` lists every doc with a one-line summary.

## Deterministic tools first

Prefer `limtool` over ad-hoc LLM reasoning for anything mechanical. If you do a task twice,
build a `limtool` subcommand (with tests) instead of doing it a third time.

| Command                                         | Does                                          |
|-------------------------------------------------|-----------------------------------------------|
| `limtool check`                                 | All gates: harness, docs lint, index freshness |
| `limtool docs index` / `lint` / `search`        | Docs maintenance                              |
| `limtool adr new "<title>"`                     | Scaffold next ADR                             |
| `limtool esdm <args>`                           | Pinned ESDM CLI, runs in `model/` (`lint`, `view`, …) |
| `limtool esdb up [--dev]` / `down` / `ping`     | Local EventSourcingDB                         |
| `limtool deps outdated`                         | Upstream pins vs latest releases (ADR-0008)   |

Prefix: `uv run --project tools`. Tool docs: [docs/harness/limtool.md](docs/harness/limtool.md).

## Rules

- **English** for code, identifiers, docs, commits. End-user i18n is a product feature.
- **Docs**: follow [docs/README.md](docs/README.md) — frontmatter, ≤150 lines, one topic per file,
  cite sources under `docs/knowledge/`. Run `limtool docs index` after adding/renaming docs.
- **Events are facts**: past tense, never mutated, never deleted. Corrections are new events.
- **Every event is attributable**: tenant, actor, reason where regulation requires it.
  See [ADR-0003](docs/adr/0003-compliance-baseline-and-regulatory-profiles.md).
- **Integration events** are persisted and audited like domain events, but kept in a
  separate namespace. See [ADR-0005](docs/adr/0005-integration-events-are-persisted.md).
- **No personal data in event payloads** — people are opaque ids; names live in the erasable
  person registry ([ADR-0010](docs/adr/0010-no-personal-data-in-event-payloads.md)).
- **Published vs internal events**: only published integration events and the command API are
  public contracts (versioned `.vN`, additive changes only) — [ADR-0012](docs/adr/0012-out-of-process-extensions.md).
- **Tenancy** is explicit everywhere ([ADR-0004](docs/adr/0004-multi-tenancy-from-day-one.md)).
- **Rust**: `cargo fmt`, `cargo clippy --all-targets -- -D warnings`, `cargo test` must pass.
- **Python tools**: `uv run --project tools pytest` and `ruff check` must pass.
- No secrets in git. `infra/eventsourcingdb/.env` is local only.

## Known traps (verified 2026-10-28)

- **EventSourcingDB docs describe the unreleased 1.3 (`preview`)**; we run the pinned 1.2.0.
  No `/api/v2`, hash v1 only. Verify every documented feature against the pinned image.
- **architecturekit is 0.x with breaking releases several times a day** — pinned `=0.21.0`. All upstream pins are exact; an upgrade is its own commit plus an entry in
  `docs/upstream-feedback/upgrade-log.md` ([ADR-0008](docs/adr/0008-exact-version-pins-with-deliberate-upgrades.md)).
  It writes no actor/reason metadata: every event embeds `lims_kernel::Audit`.
  Its `Schema` derive rejects enums, `tag`/`flatten`/`with` — use plain structs in event payloads.
- **ESDB numbers are f64** — integers > 2^53 as strings. Events ≤ 64 KiB: files go to a blob
  store, events carry reference + hash.
- **ESDM**: `model/schemas/` must stay byte-identical to the binary (lint aborts on drift);
  upgrade only via `limtool esdm update-schema`. The website lags the schema — the schema wins.

## Definition of done

1. `uv run --project tools limtool check` passes.
2. Rust/Python checks pass for touched code.
3. Domain changes are reflected in `model/` and `limtool esdm lint` is clean.
4. Decisions are captured as ADRs; open points as `docs/discussions/`.
5. Tool friction you hit is logged in `docs/upstream-feedback/`.

## Skills

| Skill               | Use when                                                  |
|---------------------|-----------------------------------------------------------|
| `grill`             | Any new requirement, feature or design question           |
| `adr`               | Writing or changing an architecture decision              |
| `docs-curation`     | Adding/splitting/indexing docs, distilling external sources |
| `esdm-modeling`     | Changing the domain model in `model/`                     |
| `eventsourcingdb`   | Running/inspecting the local event store                  |
| `upstream-feedback` | Remarks/friction about architecturekit, ESDB, ESDM        |

Claude Code additionally has the `esdb@thenativeweb` plugin skills (read/write events, EventQL).
