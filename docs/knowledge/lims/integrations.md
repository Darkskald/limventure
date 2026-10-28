---
title: "Integrations: ERP/SAP QM, MES, instruments/CDS, SDMS, ELN, logistics/gate"
summary: "External systems a LIMS typically exchanges data with, the established interface standards (SAP QM-IDI, SiLA 2, OPC UA LADS, AnIML, Allotrope, GS1 DESADV, HL7/FHIR) and validation implications."
tags: [lims, integration, erp, sap-qm, mes, instruments, sdms, eln, gs1, sila, opc-ua]
status: draft
sources:
  - https://help.sap.com/saphelp_46c/helpdata/en/c6/f842934afa11d182b90000e829fbfe/content.htm
  - https://help.sap.com/doc/1a04c453f57eb44ce10000000a174cb4/2.6/en-US/6440b853dcfcb44ce10000000a174cb4.html
  - https://www.labware.com/about/partners/sap
  - https://blogs.sap.com/2019/08/12/qm-open-notice-4-rfc-function-modules-for-downloading-uploading-and-record-types/
  - https://en.wikipedia.org/wiki/Standardization_in_Lab_Automation
  - https://reference.opcfoundation.org/LADS/v100/docs
  - https://ispe.org/pharmaceutical-engineering/ispeak/laboratory-automation-plug-and-play-lapp-framework-case-0
  - https://gs1.org/docs/tl/GS1Standards_DeliveryManagement.pdf
  - https://hl7.org/fhir/R4/diagnosticreport.html
  - https://store.astm.org/e1578-18.html
  - https://health.ec.europa.eu/system/files/2016-11/annex11_01-2011_en_0.pdf
  - https://astrixinc.com/wp-content/uploads/2019/04/LIMS-Survey-Summary-Report-Final.pdf
updated: 2026-10-28
---

# Integrations

ASTM E1578 frames LIMS within a wider laboratory informatics landscape (LIMS, ELN,
SDMS, CDS, LES). Astrix 2019: LIMS deployments are typically only "moderately"
integrated with instruments and other systems — a top source of dissatisfaction.

## ERP / SAP QM

- SAP QM-IDI (Inspection Data Interface) is an open interface for exchanging
  inspection data with external systems (SAP Help).
- Typical flow: goods receipt in SAP creates an **inspection lot** → transferred to
  LIMS → LIMS tests, records results and valuation → results (and optionally the
  **usage decision**) returned to SAP (LabWare SAP partner page).
- RFC function modules (QIRF_* family) and record types (e.g. Q88 usage decision,
  Q83/Q84 inspection point confirmation/valuation); check current S/4HANA notes, as
  some QM-IDI modules are restricted there (SAP Note 2505222, per SAP community blog).
- Who makes the usage decision (SAP or LIMS) is a per-customer design choice.

## MES / production

Receives release status, may send in-process samples; in the scenario the plant's
production schedule consumes "oil released for use".

## Instruments, CDS, SDMS

| Standard | Purpose |
|---|---|
| SiLA 2 | Instrument control/communication, HTTP/2 + Protocol Buffers, plug-and-play |
| OPC UA LADS (OPC 30500) | Device-agnostic information model for lab/analytical devices (OPCF, SPECTARIS, VDMA) |
| AnIML (ASTM) | XML format for analytical data at rest |
| Allotrope (ADF/ASM) | Semantic data format (HDF5 + ontology; JSON-based ASM more open) |
| File/serial/CSV parsers | Still the dominant legacy path (balances, titrators via RS-232) |

- CDS (chromatography data systems) usually own raw data and processing; LIMS gets
  results plus a link. SDMS stores raw files and makes them searchable.
- ISPE LAPP framework case: plug-and-play lab automation built on these standards.

## ELN / LES

ELN for experiments/R&D, LES for procedural execution; overlap with LIMS worksheets.

## Logistics, supplier, gate

- GS1 Despatch Advice (EDIFACT DESADV; ANSI X12 856 "ASN") announces shipment
  content; SSCC identifies logistic units. → scenario step 1 (delivery notice).
- Gate / yard management receives release/reject; scenario step 11 "without delay".
- Pneumatic tube systems may expose station/transport events (vendor-specific).

## Clinical

HL7 v2 / FHIR (`ServiceRequest`, `Specimen`, `Observation`, `DiagnosticReport`).

## Validation

Annex 11 §5 built-in checks for electronic data exchange; ISO 17025 7.11.2 validate
interfaces; 7.11.6 data transfers checked systematically.

## Own conclusions (not from sources)

- Integrations are **adapters subscribed to the event stream** (outbox pattern) plus
  inbound anti-corruption layers that turn external messages into commands. This keeps
  the core free of SAP/vendor specifics and makes adapters per-tenant pluggable.
- Inbound messages are stored verbatim (original record!) before mapping; mapping
  version recorded.
- Outbound delivery must be at-least-once with idempotency keys; replays of the event
  store must not re-trigger outbound calls.
- Instrument integration is a product in itself; prefer a separate edge agent
  (on-prem, also for SaaS tenants) speaking SiLA 2/LADS/files to instruments and
  HTTPS to the LIMS.
