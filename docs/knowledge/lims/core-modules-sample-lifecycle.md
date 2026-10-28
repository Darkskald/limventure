---
title: "Core module: sample lifecycle, chain of custody, containers and labels"
summary: "Expected LIMS functions from sample registration to disposal: login modes, unique IDs, receipt checks, chain of custody, aliquots/sub-samples, containers, storage locations, labels."
tags: [lims, module, sample, chain-of-custody, aliquot, label, storage]
status: draft
sources:
  - https://www.limswiki.org/index.php/LII:LIMSpec/Primary_Laboratory_Workflow
  - https://www.limswiki.org/index.php/Laboratory_information_management_system
  - https://law.resource.org/pub/us/cfr/ibr/inc/iec/iec.17025.2017.pdf
  - https://store.astm.org/e1578-18.html
  - https://eur-lex.europa.eu/eli/reg/2002/178/oj
updated: 2026-10-28
---

# Core module: sample lifecycle

LIMSwiki summarises the classic LIMS core as five phases: sample reception and login
(with customer data); assignment, scheduling and tracking of samples and workload;
processing and QC of samples, equipment and inventory; storage of analysis data;
inspection, approval and compilation for reporting.

## Typical lifecycle states

`planned/pre-logged → collected → in transit → received → (rejected at receipt) →
in progress → testing complete → reviewed → approved/released | rejected → reported →
retained → disposed/returned`. (Own synthesis from LIMSpec 1, 2, 5.)

## Registration (LIMSpec §1)

- Register before or after physical collection (1.1); automated triggers by schedule,
  web request or API (1.4); single, multiple or ad-hoc login from templates (1.8).
- Unique ID per sample, incrementing or user-defined format (1.13).
- Metadata: lot, patient, sampling point, etc. (1.5); collection details: container,
  collector, temperature, storage location (1.9).
- Receipt date/time (1.14); received samples checked against sampling requirements
  (1.15); unexpected characteristics documented (1.16).
- Linking records by sample/lot/patient/family IDs (1.20).

## Chain of custody

- Chain of custody for every distribution step inside the lab (LIMSpec 1.18) and for
  external transfers of regulated samples (1.19); also for standards/reagents (2.1).
- ISO/IEC 17025 7.4.1: procedure for transport, receipt, handling, protection,
  storage, retention, disposal/return; 7.4.4 storage conditions monitored and recorded.
- LIMSwiki: chain-of-custody assignments may restrict access to instrument data.

## Identification, sub-division, containers

- ISO/IEC 17025 7.4.2: unambiguous identification retained while under lab
  responsibility; must accommodate **sub-division** of items and transfers.
- LIMSwiki: location tracking down to freezer/shelf/rack/box/row/column; freeze-thaw
  cycles; aliquoting.
- LIMSpec 2.7–2.9: grouping by metadata, barcode/RFID, inventory amounts and status.

## Labels

Pre-configured and customizable labels with barcode support (LIMSpec 1.2). Label
printers (e.g. ZPL) and 1D/2D symbologies are common integration points.

## Disposition

Final disposition recorded incl. disposal method, location, responsible person
(LIMSpec 5.1). Retained samples (reference/retention samples) have their own
retention periods (see [core-modules-reporting-scheduling-retention.md](core-modules-reporting-scheduling-retention.md)).

## Scenario illustration (margarine plant)

Delivery notice (supplier DESADV) → **pre-logged** inspection sample; tanker arrival
triggers "collected" with vehicle and compartment; pneumatic-tube transfer is a
chain-of-custody step (sender station, receiver station, timestamps); receipt in the
lab completes custody. EU Reg. 178/2002 traceability links supplier lot ↔ delivery ↔
sample ↔ release. See [margarine example](../../domain/examples/margarine-incoming-inspection.md).

## Own conclusions (not from sources)

- Sample = aggregate/stream; aliquots are **child streams** with a parent reference
  (`AliquotCreated{parent, volume}`), not rows in the parent.
- Custody transfers are events with *from-holder / to-holder / location / condition*;
  the current location is a projection — no "location" field is ever overwritten.
- Physical objects (container, tube carrier) and logical samples must be modelled
  separately; one container can hold several samples over time (re-used carrier).
- Configurable sample types per tenant (fields, ID format, lifecycle variants) are a
  primary extensibility need.
