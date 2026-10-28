---
name: breakout
description: Generate the harness for a new, non-LIMS test project on architecturekit / EventSourcingDB / ESDM from this repo — same Claude/Codex layout, docs convention, deterministic tool and tool knowledge, stripped of all LIMS content. Use when the user wants to start another project or experiment with these libraries.
---

# Breakout

All mechanics live in `limtool breakout` (manifest: `tools/breakout/manifest.yaml`,
templates: `tools/breakout/templates/`). The agent only answers questions, fixes reported
leaks and hands over.

## Procedure

1. **Ask** (one message): target directory (must be empty or not exist), kebab-case project
   name, tool name (default `devtool`), and a one-line purpose for the vision placeholder.
2. **Generate:**
   ```sh
   uv run --project tools limtool breakout <target> --name <name> [--tool <tool>]
   ```
   Exit 0 = clean. Exit 1 = leaks listed as `path:line: text` or `docs lint: …`.
3. **Fix leaks at the source, not in the target**, so the next breakout is clean too:
   - LIMS-specific conclusion in a generic doc → move it under a `## Relevance for the LIMS …`
     heading or into a `*lims*` file (both are stripped/excluded).
   - LIMS example names in tool knowledge → add a pair to `scoped_replace` in the manifest.
   - Generic wording that merely says "LIMS" → neutralize the source text.
   - New generic doc dir or skill → add it to `copy`; LIMS-only → leave it out.
   Delete the target and regenerate until clean. `tools/tests/test_breakout.py` enforces this.
4. **Verify in the target:**
   ```sh
   cd <target> && git init -q
   uv run --project tools <tool> check
   uv run --project tools pytest -q | tail -1
   cargo clippy -q --all-targets -- -D warnings && cargo test -q 2>&1 | grep 'test result'
   uv run --project tools <tool> esdm lint   # one warning expected: domain without bounded context
   ```
5. **Hand over:** fill the purpose into `AGENTS.md` (Mission) and `docs/vision/project-vision.md`
   only as far as the user stated it. Do not commit in the target unless asked.

## What the new project gets

- `AGENTS.md` (template) + `CLAUDE.md` + `.claude/skills` symlink — Claude Code and Codex.
- Skills: grill, adr, docs-curation, esdm-modeling, eventsourcingdb, upstream-feedback.
- Docs convention, harness docs, tool knowledge (architecturekit, ESDM, EventSourcingDB),
  upstream feedback log (re-verify inherited ids), generic ADRs 0001–0005.
- `tools/` renamed to `<tool>`, ESDB compose, ESDM schemas (byte-identical), Cargo workspace
  with the current exact pins and an empty `<name>-core` crate.

## Rules

- Never hand-edit the target to hide a leak that would recur — fix the manifest or source.
- Upstream pins come from this repo at generation time; run `<tool> deps outdated` in the target.
