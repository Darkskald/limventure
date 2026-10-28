---
title: ESDM modeling with an AI agent
summary: The official ESDM workflow for drafting a model with a coding agent - materialize schemas, paste the starter prompt (verbatim here), interview, write files, lint loop - and how it is adapted in this repo.
tags: [esdm, ai, agents, prompt, workflow, skill]
status: draft
sources: [https://www.esdm.io/getting-started/your-first-model-with-ai/, https://www.esdm.io/getting-started/your-first-model/, https://www.esdm.io/introduction/use-cases/]
updated: 2026-10-28
---

# ESDM modeling with an AI agent

## Why it works (per the docs)

The schemas are embedded in the binary; `esdm add-schema` writes them into the project
so an agent reads them locally. They carry vocabulary, file conventions and the
project-layout description (`x-esdm-project-layout`) – no need to teach ESDM in the
prompt. `esdm lint` closes the loop: every finding is the next conversation round.

## Steps

1. Create a model directory; `esdm add-schema` there (or `update-schema` if `schemas/`
   exists). Commit `schemas/`.
2. Open any file-capable agent (Claude Code, Codex, Copilot, ...) in that directory.
3. Paste the starter prompt below as the opening message.
4. Agent interviews, then writes `.esdm.yaml` files (one artifact per file).
5. `esdm lint` – clean = no output, exit 0. Paste findings back; repeat.
6. `esdm view` (optionally `--with-details`) to review the structure.

Suggested first domain from the docs: "I want to model a city library's cataloging side
– acquiring books and listing them." Typical first result: domain, bounded context,
aggregate, event, command, read model, query. Second BC, second aggregate and context
mappings are deliberately left for later.

## Starter prompt (verbatim, from the docs)

```
You are a Domain-Driven Design and Event Sourcing expert helping me model a
domain using ESDM (Event-Sourced Domain Modeling).

Read the ESDM schemas in the current working directory before you write
anything. They define the entire vocabulary, the file conventions, and the
project layout you must follow.

Before producing any YAML, interview me about the domain. Ask what we are
modeling, who the actors are, which events happen, where the consistency
boundaries sit, and how the things involved are identified. Ask one question
at a time and phrase the questions in the vocabulary from the schemas.

When you have enough context, propose the model following the conventions
from the schemas. After the files are written, ask me to run `esdm lint`
and we will work through any findings together.
```

The docs name four parts: **role** (DDD/ES expert, not a YAML scribe), **schema
instruction** (read the canonical source, don't guess), **interview style** (one
question at a time, schema vocabulary), **lint loop** (linter as co-author).

## Observations from a test run (own)

- Reading the core schema in full is worth it: field-level comments are the real
  documentation and are more accurate than the website (e.g. `endsWhen.condition`).
- Validation errors inside `oneOf` branches can cascade; fix the first odd field first.
- Lint is silent when clean – an agent must check the exit code, not the output.

## Adaptation in this repo (own conclusion)

Skill `.agents/skills/esdm-modeling/` turns the prompt into a repo workflow: model in
`model/`, schemas in `model/schemas/`, binary via
`uv run --project tools limtool esdm <args>` (runs in `model/`), lint after every write
(the agent runs it itself rather than asking the user), never invent fields, combine
with the `grill` skill for the interview, and record open questions in
`docs/discussions/`.
