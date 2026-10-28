---
title: AI harness overview
summary: How Codex and Claude Code share instructions, skills and tools in this repository, and how to extend the harness.
tags: [harness, ai, codex, claude-code, skills]
status: accepted
updated: 2026-10-28
---

# AI harness overview

Decision: [ADR-0006](../adr/0006-dual-agent-harness.md).

## Wiring

```text
AGENTS.md                 ← single source of instructions (Codex reads natively)
CLAUDE.md                 ← "@AGENTS.md" + Claude-only notes
.agents/skills/<name>/    ← skills (Codex: repo skills dir)
.claude/skills            → symlink to ../.agents/skills (Claude Code)
tools/                    ← limtool, uv project, the deterministic toolbox
```

`uv run --project tools limtool harness check` verifies the wiring.

## Principles

1. **Deterministic before generative** — if a check or transformation can be scripted, it
   is a `limtool` subcommand with tests. See [limtool](limtool.md).
2. **Small context** — docs are atomic, indexed (`docs/INDEX.md`) and searchable; agents
   search, then read only hits.
3. **Grill** — the `grill` skill is the default reaction to new requirements.
4. **Tool-agnostic** — nothing may require a Claude-only or Codex-only feature. Extras
   (e.g. the Claude `esdb@thenativeweb` plugin) are optional conveniences.

## Skills

| Skill | Purpose |
|---|---|
| `grill` | Interrogate requirements until agreed |
| `adr` | Decision records |
| `docs-curation` | Writing, splitting, distilling docs |
| `esdm-modeling` | Domain modeling in ESDM |
| `eventsourcingdb` | Local event store operations |

## Adding a skill

1. `mkdir .agents/skills/<kebab-name>` with `SKILL.md` (frontmatter `name` = directory,
   `description` saying *when* to trigger). Body ≤ 200 lines; details into `references/`.
2. Add it to the skills table in `AGENTS.md` and here.
3. `limtool check`.

## Adding a tool

New subcommand in `tools/src/limtool/`, test in `tools/tests/`, row in
[limtool](limtool.md) and the `AGENTS.md` command table.
