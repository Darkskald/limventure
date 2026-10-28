---
title: "Stakeholder: controller / billing / finance"
summary: "What controllers and billing staff expect: test price lists, invoicing for contract labs, internal cost allocation, quality-dependent price adjustments handed to ERP."
tags: [lims, stakeholder, billing, finance, erp]
status: draft
sources:
  - https://www.limswiki.org/index.php/Laboratory_information_management_system
  - https://store.astm.org/e1578-18.html
  - https://limswiki.org/index.php/LII:LIMSpec_2022_R2
  - https://help.sap.com/saphelp_46c/helpdata/en/c6/f842934afa11d182b90000e829fbfe/content.htm
  - https://aphl.org/resources/resource-detail/requirements-for-public-health-laboratory-information-management-systems
updated: 2026-10-28
---

# Stakeholder: controller / billing / finance

Finance is a secondary but recurring LIMS stakeholder. LIMSwiki describes LIMS scope as
extending "from testing and quality control to reporting and invoicing". The depth
differs strongly by lab type.

## Lab types and billing needs

| Lab type | Billing need |
|---|---|
| Contract / commercial testing lab | Quotes, price lists per customer, test packages, rush surcharges, invoicing, credit notes, customer accounts |
| Public health lab | Fee schedules, payer/billing interfaces (APHL requirements cover billing as a LIMS business process) |
| In-house QC (pharma, food) | Internal cost allocation per cost centre/product; no invoicing |
| In-house QC with supplier contracts (scenario) | Quality-dependent price adjustments (bonus/malus) passed to ERP for payment |

## Expectations

- **Billable event capture**: which tests were performed, on whose behalf, when; including
  repeats (are retests billable? usually not when caused by lab error — policy).
- **Price catalogues** with validity periods; quote → order → invoice traceability.
- **Export to ERP/accounting** rather than a LIMS-internal ledger in most in-house labs.
  SAP QM already owns the inspection lot and usage decision; financial follow-ups happen
  in SAP (see [integrations.md](integrations.md)).
- **Cost per test / lab efficiency KPIs** feeding controlling (overlaps
  [stakeholder-data-scientist.md](stakeholder-data-scientist.md)).

## Scenario illustration (margarine plant)

After release, "the final price is calculated depending on raw-material quality
(bonus for better quality) and the payment process initiated" (scenario step 8). The
LIMS provides the quality grade; the contract's bonus formula and the payment belong
to ERP/purchasing. See [margarine example](../../domain/examples/margarine-incoming-inspection.md).

## Own conclusions (not from sources)

- Keep **pricing logic out of the LIMS core**. The LIMS emits facts
  (`ReleaseDecided{grade, results}`), a pluggable *pricing policy* module or the ERP
  computes money. This keeps the validated GxP core small (GAMP: lower risk surface).
- Billing projections are a classic event-sourcing read model: replaying
  `TestCompleted` events against a price catalogue valid at the event date yields a
  reproducible invoice; corrections are compensating events, never edits.
- Contract-lab mode (invoicing) vs in-house mode (cost allocation) is a
  **per-tenant feature toggle** decision for the PO.
