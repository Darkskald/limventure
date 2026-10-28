---
title: "ADR-0006: One harness for Codex and Claude Code"
summary: AGENTS.md is the single instruction source, CLAUDE.md imports it; skills live in .agents/skills with .claude/skills as symlink; mechanical work goes through the limtool CLI.
tags: [adr, harness, ai, codex, claude-code]
status: accepted
updated: 2026-10-28
---

# ADR-0006: One harness for Codex and Claude Code

## Decision

- `AGENTS.md` (read natively by Codex) is the only instruction file with content.
- `CLAUDE.md` contains `@AGENTS.md` plus Claude-only notes.
- Skills in `.agents/skills/<name>/SKILL.md` (Agent Skills format, read by Codex);
  `.claude/skills` is a symlink to it.
- Deterministic work is done by `limtool` (uv project in `tools/`), not by LLM reasoning.
- `limtool harness check` enforces the wiring.

## Consequences

- Tool-specific features (Claude plugins, Codex config) are optional extras, never required.
- Details: [harness overview](../harness/overview.md).
