# ESDM 0.15.0 cheat sheet

Authoritative: `model/schemas/core/v1.yaml`. Every core document:
`apiVersion: schema.esdm.io/core/v1`, `kind`, `name` + optional `description`,
`metadata: {labels: {k: v}, annotations: {k: v}}`. Shapes below are condensed from the schema; full examples that lint clean are in `docs/knowledge/esdm/`.

## Required fields per kind

| kind | scope | required | optional |
|---|---|---|---|
| domain | - | - | - |
| subdomain | domain | `type` core/supporting/generic, `boundedContexts[]` | |
| bounded-context | domain | - | `language` (required with UL), `ubiquitousLanguage[]` |
| aggregate | domain, boundedContext | `identifiedBy`, `state` | `invariants[]` |
| dynamic-consistency-boundary | domain, boundedContext | `identifiedBy[]`, `consults[]` | `invariants[]` |
| entity | domain, boundedContext | `schema`, `identifiedBy` (schema/static) | `invariants[]` |
| command | + aggregate or dynamicConsistencyBoundary | `data`, `publishes[]` | `actors[]`, `constraints[]` |
| event | + aggregate, or BC only (free-standing) | `data` | |
| read-model | domain, boundedContext | `projections[]`, `schema` | `paradigm` |
| query | domain, boundedContext | `readModel`, `result` | `parameters`, `paradigm`, `actors[]`, `constraints[]` |
| value-object | domain, boundedContext | `schema` | `invariants[]` |
| domain-service | domain, boundedContext | `functions[]` {name, arguments, returns} | `rules[]` per function |
| actor | domain, boundedContext | `type` human/system | `responsibilities[]`, `backedBy[]` (system only) |
| external-system | domain | `direction` inbound/outbound/bidirectional | `category`, `capabilities[]` |
| policy | domain | `deliveryGuarantee`, `handles[]`, `emits[]` | `idempotency`*, `constraints[]` |
| event-handler | domain | `deliveryGuarantee`, `handles[]`, `sideEffects[]` | `idempotency`*, `constraints[]` |
| process-manager | domain | `deliveryGuarantee`, `correlatedBy`, `state`, `startsWhen[]`, `endsWhen[]`, `reactions[]` | `idempotency`*, `timers[]`, `invariants[]`, `constraints[]` |
| context-mapping | none | `type` + role fields | `terms[]` (asymmetric, BC-BC only) |

`*` required when `deliveryGuarantee: at-least-once`. `idempotency.owner`:
self / downstream / infrastructure / none / not-required (+ `strategy` prose).

## Small shapes

```yaml
namedRule:      { name: kebab, rule: prose }           # invariants, constraints, rules
namedCondition: { name: kebab, condition: prose }      # process-manager.endsWhen only
eventRef:       { boundedContext, aggregate, event }   # or { boundedContext, event }
commandRef:     { boundedContext, aggregate, command } # or { boundedContext, dynamicConsistencyBoundary, command }
projection:     { boundedContext, aggregate, event, rule }
consult:        { boundedContext, [aggregate,] event, criteria }
aggregate.identifiedBy: { source: state, field } | { source: static, value } | { source: generated, generator: uuid }
dcb.identifiedBy[]:     { name, source: command-payload, field } | { name, source: static, value } | { name, source: generated, generator }
sideEffect:     { type: external-call, externalSystem, rule } | { type: other, rule }
timer:          { name, after: { value: 2, unit: hours } } | { name, at: <state field> }
reaction:       { when: eventRef | { timer: name }, rule, emits?, setTimers?, cancelTimers? }
endpoint:       { domain, boundedContext } | { domain, externalSystem }
```

## Context mapping types and role fields

customer-supplier: `customer`/`supplier` - conformist: `conformist`/`upstream` -
anti-corruption-layer: `downstream`/`upstream` - open-host-service: `host`/`consumer` -
published-language: `publisher`/`consumer` - shared-kernel, partnership, separate-ways:
`participants: [bc, bc]` (no external systems). `terms` keys = the role names.

## Bare vs scoped references

Bare: `publishes`, `actors`, `readModel`, `boundedContexts`, `backedBy`,
`sideEffects[].externalSystem`. Scoped triples: `handles`, `emits`, `startsWhen`,
`reactions[].when`, `projections`, `consults`.

## Given-When-Then (`schema.esdm.io/given-when-then/v1`, kind `feature`)

Scope variant via key: `aggregate` | `dynamicConsistencyBoundary` | `processManager`
(no BC) | `readModel`. Aggregate scenario: `given: [{event, data}]`,
`when: {command, data, actor?}`, `then: {events: [...]}` | `{rejection: {invariant}}`.
PM scenario: `when: eventRef+data | {timer}`, `then: {emits?, setTimers?, cancelTimers?,
state?, ended: true?}`. Read model: `when: {query, parameters}`, `then: {result} | {readModel}`.

## Domain story (`schema.esdm.io/domain-storytelling/v1`, kind `domain-story`)

`scope: {domain}`, `pointInTime` as-is/to-be, `granularity` coarse-grained/fine-grained,
`domainPurity` pure/digitalized, `sentences: [{sequenceNumber, edges: [{from: {actor|workObject},
to: {...}, label}]}]`, optional `actors[]`, `groups[]`, per-sentence `workObjects[]`.

## Lint quick reference

Clean = silent + exit 0. `--format json` -> `[{ruleId, severity, message,
location{file,line,column}, documentationUrl}]`. Catalog:
`docs/knowledge/esdm/linter-rules.md`. Frequent: `unresolved-reference`,
`unknown-field`, `event-name-with-aggregate-prefix`, `event-without-consumer`,
`cross-bounded-context-reference-without-mapping`, `orphan-actor`, `uncovered-invariant`.
