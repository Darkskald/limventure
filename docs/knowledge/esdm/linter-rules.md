---
title: ESDM linter rule catalog
summary: All esdm 0.15.0 linter rule IDs for core and extensions grouped by stage and severity, with the checks that are easy to trip over when writing models.
tags: [esdm, lint, rules, quality-gate]
status: draft
sources: [https://www.esdm.io/reference/linter-rules/, https://www.esdm.io/extensions/given-when-then/reference/linter-rules/, https://www.esdm.io/extensions/domain-storytelling/reference/linter-rules/]
updated: 2026-10-28
---

# ESDM linter rule catalog

Two stages: (1) parser + resolver ("pipeline diagnostics") – YAML, `apiVersion`, schema
shape, references; (2) only if stage 1 has no error, the rule catalog runs over the
resolved model. IDs: `esdm/<category>/<name>`; categories `structure` (model contradicts
itself), `modeling` (consistent but incomplete/misleading), `system`, `gwt`. Severity is
fixed per rule; nothing is configurable.

## Pipeline diagnostics (all `error`)

`structure/yaml-syntax-error`, `structure/unknown-api-version`,
`structure/missing-required-field`, `structure/unknown-field`, `structure/type-mismatch`,
`structure/constraint-violation` (enum/pattern/minItems; suggests near matches),
`structure/duplicate-name` (same kind + name + scope), `structure/unresolved-reference`
(suggests near names), `system/rule-panic` (ESDM bug), `system/schemas-directory-drift`.

Pitfall (observed): one wrong field inside a `oneOf` branch can cascade into many
`unknown-field` errors for *valid* sibling fields – fix the first odd one and re-lint.

## Core structure rules (all `error`)

| Rule | Check |
|---|---|
| `aggregate-identified-by-field` | `identifiedBy.field` exists in `state` |
| `ambiguous-name` | aggregate/DCB/entity/value-object/domain-service names unique per BC |
| `duplicate-translation-language` | one translation per language per term |
| `dynamic-consistency-boundary-identified-by-field` | `command-payload` field exists in `data` of every triggering command |
| `entity-identified-by-field` | field exists in entity `schema` |
| `process-manager-correlated-by-field` | field exists in `data` of every consumed event |
| `process-manager-timer-at-field` | `at` field exists in PM `state` |
| `translation-into-own-language` | no translation into the BC's own `language` |

## Core modeling rules (all `warning`)

Gaps: `aggregate-without-commands`, `aggregate-without-events`,
`bounded-context-without-content`, `domain-without-bounded-context`,
`subdomain-without-bounded-context`, `event-without-publisher`,
`event-without-consumer` (consumers: handler, policy, PM, read model, DCB),
`read-model-without-query`, `orphan-actor` (not in any command/query `actors`),
`orphan-external-system` (not in `backedBy`, external-call or mapping),
`orphan-context-mapping`, `process-manager-without-event-reactions`.
Smells: `event-name-with-aggregate-prefix`,
`cross-bounded-context-reference-without-mapping`, `human-actor-with-backed-by`.
Schema-duplicating safety nets: `actor-without-type`, `aggregate-without-identified-by`,
`aggregate-without-state`, `command-without-data`, `command-without-publishes`,
`consumer-at-least-once-without-idempotency`, `domain-service-without-functions`,
`dynamic-consistency-boundary-without-consults`/`-without-identified-by`,
`entity-without-identified-by`/`-without-schema`, `event-handler-without-handles`/
`-without-side-effects`, `event-without-data`, `external-system-without-direction`,
`policy-without-emits`/`-without-handles`, `process-manager-without-ends-when`/
`-without-starts-when`, `query-without-read-model`/`-without-result`,
`read-model-without-projections`/`-without-schema`, `value-object-without-schema`.

## Given-When-Then (`esdm/gwt/...`)

Errors: `feature-references-unknown-{aggregate,dynamic-consistency-boundary,process-manager,read-model}`,
`scenario-actor-not-permitted` (actor not in command `actors`),
`scenario-references-unknown-{actor,command,event,query,timer}`,
`scenario-rejection-references-unknown-invariant`.
Warnings: `feature-without-scenarios`, `scenario-then-mismatched-feature-scope`,
`scenario-when-mismatched-feature-scope`, `scenario-without-then`,
`scenario-without-when`, `uncovered-invariant` (once a unit has a feature, every named
invariant needs a rejecting scenario).

## Domain Storytelling

Errors: `structure/story-duplicate-actor-name`, `story-duplicate-group-name`,
`story-duplicate-work-object-in-sentence`, `story-unknown-group-membership`.
Warnings: `structure/story-sentence-without-edges`, `story-without-sentences`,
`modeling/story-orphan-actor`, `story-orphan-group`, `story-orphan-work-object`.

## Relevance for the LIMS (own conclusion)

Gate with `--warnings-as-errors`: warnings such as `event-without-consumer` and
`orphan-external-system` are exactly the drift signals ADR-0002 cares about. Not
checked by ESDM: commands without actors, value-object usage, tenant/audit metadata –
candidates for a `limtool` add-on check over `lint --format json` + YAML parsing.
