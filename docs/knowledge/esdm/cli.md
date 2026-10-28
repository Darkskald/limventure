---
title: ESDM CLI reference
summary: Every esdm 0.15.0 subcommand with its exact flags, path arguments, outputs and exit-code semantics, verified against the binary's --help.
tags: [esdm, cli, lint, tooling]
status: draft
sources: [https://www.esdm.io/reference/cli/, https://www.esdm.io/getting-started/running-esdm-lint/, https://www.esdm.io/getting-started/running-esdm-view/, https://www.esdm.io/getting-started/running-esdm-glossary/, https://www.esdm.io/getting-started/running-esdm-documentation/]
updated: 2026-10-28
---

# ESDM CLI reference (0.15.0)

`esdm --help` lists: `add-schema`, `completion`, `documentation`, `glossary`, `help`,
`lint`, `update-schema`, `version`, `view`. Every subcommand has `-h/--help`.

| Command | Flags | Notes |
|---|---|---|
| `esdm add-schema` | none | Writes embedded schemas to `./schemas/` (cwd only, no `-d`). Fails (exit 1) if `schemas/` exists. |
| `esdm update-schema` | none | Refreshes `./schemas/` (cwd only). Fails if `schemas/` missing or local revision is newer (no downgrades). Prints `schemas/ is up to date - nothing to update.` when current. |
| `esdm lint` | `-d/--directory` (default `.`), `--format human\|json`, `--color auto\|always\|never`, `--warnings-as-errors` | Recursive walk over `*.esdm.yaml`. |
| `esdm view [path]` | `-d`, `--with-details`, `--color` | Tree summary; path = `domain/bc/unit`. |
| `esdm glossary [path]` | `-d`, `--language <bcp47>` | Markdown to stdout from `ubiquitousLanguage`. Path = `domain[/bc]`. |
| `esdm documentation [path]` | `-d`, `-o/--output <dir>` (required), `--force` | Markdown tree, one page per element. |
| `esdm version` | none | Version + git revision. |
| `esdm completion` | cobra default | Shell completion script. |

## Exit codes (verified)

- `lint`: `0` = no error-severity finding (silence on a clean model; warnings are
  printed but still exit 0). `1` if any error, or any warning with
  `--warnings-as-errors`, or **no `.esdm.yaml` found** (`Error: no esdm files found`).
- `view`/`glossary`/`documentation`: non-zero only for an unresolvable model, invalid
  path, or (documentation) non-empty output dir without `--force`. Linter findings do
  not block them.
- CLI errors print a human line plus a JSON log line on stderr.

## Lint output

Human format, one block per finding:

```
warning: esdm/modeling/event-name-with-aggregate-prefix
  at sample-reception/sample.esdm.yaml:75:7
  event name "sample-received" redundantly starts with its aggregate's name "sample"; ...
  see https://www.esdm.io/reference/linter-rules/#modeling-event-name-with-aggregate-prefix
```

JSON format (`--format json`): array of
`{ruleId, severity, message, location: {file, line, column}, documentationUrl}`;
`file` is absolute when `-d` is absolute. Rule catalog: [linter-rules.md](linter-rules.md).

Recommended CI invocation (from the docs):

```sh
esdm lint --directory ./model --color never --warnings-as-errors
```

## view

```
esdm view                              # whole model
esdm view lims/sample-reception/sample # subtree
esdm view --with-details               # + identifiedBy, data fields, invariants, rules
```

Glyphs: `→` outgoing (command → event it publishes, query → read model), `←` incoming
(event ← publishing command, read model ← N events). Counts like `3 cmd · 3 evt · 1 inv
· 1 feat`. Path segments match names; if several kinds share a name, all match.

## glossary

`esdm glossary [domain[/bounded-context]] [--language de]` – one `##` section per
bounded context with a `ubiquitousLanguage`, one `###` per term, `_Avoid the term "X"._`
notes. With `--language`, untranslated terms keep their primary form and get
`_No translation into de._`. Empty model language → only `# Glossary`.

## documentation

`esdm documentation -o out [path] [--force]`. Containers (domain, bounded-context,
aggregate, DCB, process-manager, read-model) become directories with `README.md`; all
other elements become `.md` files. Names are `kind_name`, e.g.
`domain_lims/bounded-context_sample-reception/aggregate_sample/command_receive.md`.
Context mappings sit at the root. Neutral Markdown, no theme.

## Relevance for the LIMS (own conclusion)

Because `add-schema`/`update-schema` act on the **cwd**, the `limtool esdm` wrapper must
run the binary with `cwd=model/`; then `lint`, `view` etc. need no `-d` and drift
detection finds `model/schemas/`. `--format json` is the hook for a deterministic
`limtool` check; `--warnings-as-errors` belongs in `limtool check`/CI.
