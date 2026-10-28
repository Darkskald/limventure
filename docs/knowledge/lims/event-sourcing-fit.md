---
title: "Event sourcing fit for LIMS: natural fits and challenges"
summary: "Where an event-sourced design naturally satisfies LIMS/GxP expectations (audit trail, amendments, temporal queries) and where it is hard (GDPR erasure, retention deletion, e-signature binding, corrections, replay side effects, schema evolution)."
tags: [lims, event-sourcing, audit-trail, gdpr, e-signature, architecture]
status: draft
sources:
  - https://martinfowler.com/eaaDev/EventSourcing.html
  - https://www.infoq.com/news/2018/02/retroactive-future-event-sourced
  - https://www.axoniq.io/blog/protect-sensitive-data-in-an-event-sourced-application
  - https://eur-lex.europa.eu/eli/reg/2016/679/oj
  - https://www.law.cornell.edu/cfr/text/21/11.10
  - https://www.law.cornell.edu/cfr/text/21/11.70
  - https://health.ec.europa.eu/system/files/2016-11/annex11_01-2011_en_0.pdf
  - https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/687246/MHRA_GxP_data_integrity_guide_March_edited_Final.pdf
  - https://law.resource.org/pub/us/cfr/ibr/inc/iec/iec.17025.2017.pdf
updated: 2026-10-28
---

# Event sourcing fit for LIMS

Fowler: event sourcing captures all changes to application state as a sequence of
events, enabling complete rebuild, **temporal query** and event replay. Retroactive
events carry two dates — when it happened and when it was recorded (InfoQ, DDD Europe
2018). Mapping below is mostly **own analysis** against cited requirements.

## Natural fits

| Requirement | Why events fit |
|---|---|
| Audit trail who/what/when/why, previous values kept (11.10(e); Annex 11 §9; MHRA 6.13) | The event log *is* the history; nothing is overwritten |
| Amendments traceable, original + amended retained (ISO 17025 7.5.2) | Correction = new event referencing the old one |
| Printouts showing changes since entry (Annex 11 §8.2) | Diff of stream up to print time |
| Reconstruct "state at release time" (MHRA raw-data definition) | Temporal query / replay to a position |
| Impact assessment (bad calibration, recalled reagent lot) | Query/projection across streams by reference |
| Process mining, TAT, SLA | Timestamps on every transition |
| Validation regression | Replay recorded streams against new release |

Caveat: a domain event log is **not automatically** a compliant audit trail. It needs
authenticated principal, server timestamp, reason, protection from alteration, and a
human-readable rendering (Annex 11 §9 "generally intelligible form").

## Challenges

### 1. GDPR erasure vs immutable log
- GDPR Art. 17 right to erasure; Art. 17(3)(b),(e) exempt processing needed for a legal
  obligation or legal claims — GxP retention duties usually override erasure for
  regulated records, but not for all personal data (e.g. portal user profiles).
- Practitioner patterns: **crypto-shredding** (per-subject key, destroy key) or keep
  PII out of events and reference a mutable PII store (AxonIQ). Legal sufficiency of
  crypto-shredding is not settled by regulators (see sources' caveats).

### 2. Deletion at end of retention
Retention expiry requires deletion of whole record sets; needs stream-level archival/
deletion with a recorded deletion certificate — conflicts with "append-only forever".

### 3. E-signature binding (11.70; Annex 11 §14)
Signature must be inseparable from the exact record state. Signature event should
contain stream ID, version/position signed, content hash, meaning, signer, time,
authentication evidence. Any later event on that stream invalidates or supersedes the
signature status unless rules say otherwise.

### 4. Corrections and retroactive facts
"Wrong value entered" vs "value later found invalid" vs "late-arriving event with
earlier business time" are different event types; projections must handle bitemporal
ordering.

### 5. Side effects on replay
Notifications (gate, ERP posting, e-mail) must not fire on rebuild — use outbox and
idempotent integration events.

### 6. Schema evolution over decades
Retention up to ≥ 10 years (GMP, pathology) ⇒ events must stay readable; upcasting
strategies and archived schema registry required (Annex 11 §17 retrieval after
system changes).

### 7. Configuration as of event time
MHRA: retain configuration settings specific to each record ⇒ events reference config
versions; config itself event-sourced.

### 8. Multi-tenancy
Tenant ID in every event, per-tenant encryption keys (also enables crypto-shredding of a
whole tenant on contract end), per-tenant stores for high-isolation customers.

### 9. Tamper evidence
Append-only is a property of the software, not proof; hash-chaining streams or
periodic signed checkpoints give evidence that history was not rewritten by a DBA.

## Own conclusions

Event sourcing is a strong fit for the GxP core; the risk lies in PII handling,
retention deletion and long-term schema evolution. These should be decided in ADRs
before the first production event is written.
