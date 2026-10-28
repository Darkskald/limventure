---
title: "Stakeholder: lab technician / analyst"
summary: "What bench analysts and technicians expect from a LIMS: fast sample login, guided worksheets, instrument capture, material checks, minimal re-typing."
tags: [lims, stakeholder, analyst, ux, workflow]
status: draft
sources:
  - https://store.astm.org/e1578-18.html
  - https://limswiki.org/index.php/LII:LIMSpec_2022_R2
  - https://www.limswiki.org/index.php/LII:LIMSpec/Primary_Laboratory_Workflow
  - https://www.limswiki.org/index.php/LII:LIMSpec/Maintaining_Laboratory_Workflow_and_Operations
  - https://www.limswiki.org/index.php/Laboratory_information_management_system
  - https://health.ec.europa.eu/system/files/2016-11/annex11_01-2011_en_0.pdf
  - https://astrixinc.com/wp-content/uploads/2019/04/LIMS-Survey-Summary-Report-Final.pdf
updated: 2026-10-28
---

# Stakeholder: lab technician / analyst

The largest user group, typically non-technical, hands often gloved, working at the
bench or at a shared terminal. They spend their day in the LIMS; every extra click
is multiplied by thousands of samples.

## Core expectations (from LIMSpec / ASTM E1578 functional areas)

| Area | Expectation | Source ref |
|---|---|---|
| Sample receipt | Register before or after physical collection; scan barcode; record receipt date/time; compare against sampling requirements | LIMSpec 1.1, 1.14, 1.15 |
| Labels | Pre-configured and customizable barcode labels, RFID optional | LIMSpec 1.2, 2.8 |
| Unique IDs | Each sample gets a unique, possibly customer-formatted identifier | LIMSpec 1.13 |
| Anomalies | Document unexpected sample characteristics and preparation steps | LIMSpec 1.16, 1.17 |
| Materials | Record reagents/standards used per test with lot, expiry, status; only approved, unexpired materials selectable; block materials expiring mid-test | LIMSpec 3.1–3.3 |
| Result entry | Per sample or per test, spreadsheet upload, multiple data types | LIMSpec 3.5, 3.6, 3.9 |
| Instruments | Blocked from using out-of-calibration or under-investigation instruments | LIMSpec 10.9 |
| Immediate feedback | OOS results raise alerts at entry | LIMSpec 3.12 |
| Retests | Retest workflows supported without losing the original value | LIMSpec 3.8 |
| Training gate | Only trained/qualified staff can perform a task | LIMSpec 7.7, 8.8 |
| SOP link | Each test linked to the SOP revision used | LIMSpec 7.4 |

## Regulatory touchpoints affecting the analyst's UI

- **Second check on manual entry**: for critical data entered manually, EU GMP Annex 11
  §6 expects an additional accuracy check, by a second operator or validated electronic
  means. Direct instrument capture removes this burden (Annex 11 §5, §6).
- **Reason for change**: every change of GMP-relevant data needs a documented reason
  (Annex 11 §9; LIMSpec 9.1 "prompt the user to enter a mandatory reason").
- **Attributability**: individual accounts; no shared logins (Annex 11 §12.4).

## Pain points reported (see [legacy-ux-pain-points.md](legacy-ux-pain-points.md))

- Astrix 2019 survey: nearly half of respondents said their LIMS had a net neutral
  effect or *decreased* lab efficiency; 18 % called it cumbersome.
- Transcription from instrument printouts into LIMS fields (double work, error source).
- Many screens per sample; modal dialogs; no bulk operations.

## Scenario illustration (margarine plant)

The analyst receives the sunflower-oil sample from the pneumatic tube, scans the
tube carrier/label, which auto-links to the tanker delivery. The worksheet guides:
sensory test (colour, turbidity, consistency — structured picklists, not free text),
iodine value (instrument capture), IR spectrum (file + extracted values). The
analyst never types the tanker number. See [margarine example](../../domain/examples/margarine-incoming-inspection.md).

## Own conclusions (not from sources)

- The analyst UX is "task-first": a queue of *my next work*, not a database browser.
- Touch/scan-first input, large hit targets, keyboard-only path for power users.
- Offline/degraded mode at the bench (Annex 11 §16 business continuity) should be
  considered; event sourcing makes later reconciliation of offline-captured events
  feasible but needs explicit conflict rules.
