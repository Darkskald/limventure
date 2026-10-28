---
title: Scenario-to-concept map
summary: Maps concrete customer scenarios (margarine, OH number) onto generic LIMS concepts and their extensibility tier; core-worthy is what recurs across scenarios.
tags: [domain, concepts, examples, extensibility]
status: draft
updated: 2026-10-28
---

# Scenario-to-concept map

Method (chat 2026-10-28): a concrete scenario is an **acceptance test**, not the design.
The core passes when the scenario runs on core + configuration + formulas + extensions with
**zero scenario-specific core code**. What recurs across scenarios is core; what appears once
is configuration or extension.

| Generic concept | [Margarine](examples/margarine-incoming-inspection.md) | [OH number](examples/oh-number-determination.md) | Placement | Decided in |
|---|---|---|---|---|
| Trigger | Supplier delivery notice (inbound event) | Customer/production order | Core; trigger rules tier 1 | [ADR-0016](../adr/0016-analysis-order-is-a-core-aggregate.md) |
| Analysis order | Implicit via inspection plan | Explicit | Core aggregate | ADR-0016 |
| Expected sample | Truck announced | Sample announced | Core | [ADR-0013](../adr/0013-expected-events-are-facts.md) |
| Sample, receipt, custody | Tank sample, pneumatic tube | Sample arrives | Core | [ADR-0017](../adr/0017-container-is-a-core-aggregate-separate-from-sample.md) |
| Container, label | Sample bottle / tube carrier | Sample and aliquot vials | Core aggregate | ADR-0017 |
| Derived sample | — | Aliquots | Core | ADR-0017 |
| Method (versioned, norm) | Sensory, iodine value, IR | OH number per ISO | Core engine; methods tier 1 | [ADR-0020](../adr/0020-replicates-and-acceptance-defined-by-method-version.md) |
| Replicates → reported result | Single determination | Triplicate | Core; rule tier 2 | ADR-0020 |
| Calculated result | Iodine value | OH value (+ acid value) | Tier-2 formula | [ADR-0015](../adr/0015-formula-language-rhai-behind-a-replaceable-engine-port.md), [ADR-0021](../adr/0021-calculated-results-declare-explicit-dependencies.md) |
| Specification, decision rule | Catalog | Customer/product limits | Core engine; limits tier 1 | [ADR-0018](../adr/0018-specification-pinned-at-order-creation-with-binding-and-agreed-limits.md) |
| Deviation | Imminent rejection | "Action if off" | Core aggregate | [ADR-0019](../adr/0019-out-of-spec-results-open-a-deviation.md) |
| Outcome | Disposition of goods | Report to requester | Core | ADR-0019 |
| Signatures, retention | Lab head; counter-sign on reject | — | Regulatory profile | [ADR-0003](../adr/0003-compliance-baseline-and-regulatory-profiles.md) |
| Pricing | Quality bonus | — | Tier-2 formula | [ADR-0014](../adr/0014-lims-owns-release-and-quality-pricing.md) |
| Notification | Gate, ERP | Customer, production | Published events | [ADR-0012](../adr/0012-out-of-process-extensions.md) |

## Not yet walked through

Signature and notification details, inspection-plan configuration model, a scheduled-sampling
scenario (environmental monitoring / stability) as third contrast.
