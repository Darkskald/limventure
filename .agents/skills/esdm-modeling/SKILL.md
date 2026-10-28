---
name: esdm-modeling
description: Create, extend, review or fix the ESDM domain model in model/ (*.esdm.yaml files - domains, bounded contexts, aggregates, commands, events, read models, policies, process managers, context mappings, given-when-then features, domain stories). Use whenever a domain change, new requirement, event, integration or business rule must be reflected in the model, when the user asks to "model" something, or when `limtool esdm lint` reports findings.
---

# ESDM modeling

Adapts the official ESDM "first model with AI" workflow to this repo. Knowledge:
`docs/knowledge/esdm/` (start with `overview.md`; use `limtool docs search esdm <term>`,
don't read the whole directory). Cheat sheet: [references/cheat-sheet.md](references/cheat-sheet.md).

## Ground rules

- **Model root:** `model/`. **Schemas:** `model/schemas/{core,given-when-then,domain-storytelling}/v1.yaml`
  (written by `esdm add-schema`, committed, never edited - any byte change makes
  `esdm lint` abort with `esdm/system/schemas-directory-drift`).
- **Binary:** always `uv run --project tools limtool esdm <args>`. The wrapper pins
  esdm 0.15.0, verifies its SHA256, installs into `.tools/bin/`, and runs **inside
  `model/`** - so pass no `-d`, and paths are relative to `model/`. Never download or
  call another `esdm` binary.
- **The schema is the contract.** Before writing a kind you have not written in this
  session, read its `if kind: <kind>` block in `model/schemas/core/v1.yaml` (or the
  extension schema). The inline comments there are the real documentation and beat
  the website (example: `process-manager.endsWhen` entries are `{name, condition}`).
- **Never invent fields.** Unknown keys are errors (`unevaluatedProperties: false`).
  If the schema has no field for something (tenant, signature, versioning, ...), say
  so, use prose (`description`, `rule`) or `metadata.labels`/`annotations`, and raise
  it with the user - do not fake structure.
- **One artifact per document, one concern per file.** Multi-document files (`---`)
  are allowed only to keep a consistency unit together (aggregate + its commands +
  events). Every document starts with its schema modeline.
- **Lint after every write.** You run it yourself; the user does not.
- English names; kebab-case `^[a-z][a-z0-9-]*$`; domain language from the bounded
  context's `ubiquitousLanguage`.

## Layout (from the schema's `x-esdm-project-layout`, not enforced by the linter)

```
model/
├── schemas/                      # add-schema output, committed
├── domain.esdm.yaml              # domain (+ subdomains)
├── external-systems.esdm.yaml    # flat catalog of external systems
├── <bounded-context>/            # one directory per BC - never per kind
│   ├── bounded-context.esdm.yaml # incl. ubiquitousLanguage (English only, no translations)
│   ├── actors.esdm.yaml
│   ├── <unit>.esdm.yaml          # aggregate or DCB + its commands + events
│   ├── <unit>.feature.esdm.yaml  # given-when-then next to its unit
│   └── <read-model>.esdm.yaml    # read model + its queries
├── integration/                  # domain-scoped: policies, process managers,
│                                 # event handlers, context mappings
└── stories/                      # domain-storytelling discovery stories
```

Modeline per document, relative to the file:
`# yaml-language-server: $schema=./schemas/core/v1.yaml` at `model/` root,
`../schemas/core/v1.yaml` one level down; extensions use
`../schemas/given-when-then/v1.yaml` / `../schemas/domain-storytelling/v1.yaml`.

## Procedure

1. **Setup check.** If `model/schemas/` is missing: `limtool esdm add-schema`.
   After a binary upgrade: `limtool esdm update-schema` (separate commit).
   `limtool esdm install` only fetches/verifies the binary.
2. **Orient.** `limtool esdm view` (add `<domain>/<bc>[/<unit>]` and/or
   `--with-details` to zoom). Read only the files you will touch.
3. **Interview - one question at a time** (combine with the `grill` skill; use its
   `Q: … - Recommendation: … - Cost: …` format). Phrase questions in schema
   vocabulary. Cover, as relevant:
   - which bounded context; its terms (canonical term, rejected terms; English only, no translations);
   - actors (`human`/`system`) and which commands each may issue / queries each may run;
   - events (past tense facts) and the commands that publish them;
   - the consistency boundary: aggregate (one id, lifecycle) or DCB (rule spans ids
     given by the command); how things are identified (`identifiedBy`);
   - invariants (state rules) vs authorization (`actors`) - never mix them;
   - reactions: stateless "do next" = policy, "tell the world" = event handler,
     memory/deadlines/multiple events = process manager with timers;
   - external systems, direction, and the context-mapping pattern (ACL inbound,
     published-language outbound);
   - audit lens: who/why/signature - and where ESDM cannot express it.
   Stop when the user confirms a restated summary.
4. **Propose before writing.** List the artifacts (kind, name, file) and get a go.
5. **Write.** Follow the cheat sheet shapes; copy field names from the schema.
   - Events: bare past tense (`received`, not `order-received`); add
     `metadata.annotations.cloudevents.type`.
   - Commands: bare imperative (`receive`); `data` required (`{}` if none).
   - Cross-BC policy/read model/handler => add or reuse a context mapping.
   - Every named invariant of a unit with a feature needs a rejecting scenario.
6. **Lint.** `uv run --project tools limtool esdm lint --warnings-as-errors`.
   Clean = **no output, exit 0** - check the exit code. Use `--format json` when
   parsing. Fix the *first* odd finding first: an error in a `oneOf` branch cascades
   into many `unknown-field` errors for valid siblings. Repeat until clean. Never
   "fix" a finding by deleting meaning (e.g. dropping an invariant) without asking.
7. **Review.** `limtool esdm view --with-details <path>` and show the user the
   relevant subtree. Optionally `limtool esdm glossary --language de`.
8. **Record.** Architecturally relevant modeling choices => `adr` skill (proposed).
   Unresolved questions => `docs/discussions/` (one file per question). Run
   `uv run --project tools limtool check` before declaring done.

## Repo conventions on top of ESDM (LIMS)

- Domain name: `lims`. CloudEvents types always end in `.v<N>` (ADR-0023):
  `io.limventure.<bounded-context>.<aggregate>-<event>.v1` for aggregate events,
  `io.limventure.<bounded-context>.<event>.v1` for free-standing (DCB) events,
  `io.limventure.integration.<partner>.<event>.v1` for integration events. A breaking
  change is a new ESDM event `<event>-v2` with type `.v2` plus an upcaster.
- Integration events are real events of dedicated aggregates (e.g. `inbound-message`,
  `outbound-message`); inbound translation = policy (ACL), outbound delivery = event
  handler with `external-call`, at-least-once, `idempotency.owner: downstream`.
- Expected future events: model the expectation as a fact (`announced` with
  `expectedAt`), a process manager timer (`at: <state field>` or `after`), and an
  explicit overdue event. See `docs/knowledge/esdm/lims-mapping.md`.
- Tenant/user/reason are not ESDM concepts: follow the event envelope convention
  from ADR-0003/0004; do not invent schema fields for them.
- Refer to model elements from docs/ADRs with `esdm:` URIs, e.g.
  `esdm:domain=lims/bounded-context=sample-reception/aggregate=sample/event=received`.

## Don'ts

- No directories per kind (`commands/`, `events/`).
- No `version` field on events - a changed event is a new event (`...-v2`).
- No `backedBy` on human actors; no authorization as invariant.
- No hand-edits to `model/schemas/`; no ESDM binary outside the wrapper.
- No `-d` flag through the wrapper unless the user asks for a subdirectory.
