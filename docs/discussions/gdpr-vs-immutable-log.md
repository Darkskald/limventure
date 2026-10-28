---
title: "Open: GDPR erasure vs immutable event log"
summary: Personal data (analyst names, customer contacts, patient data in clinical labs) must be erasable under GDPR while events are immutable and audit-relevant.
tags: [discussion, gdpr, privacy, audit-trail]
status: draft
updated: 2026-10-28
---

# Open: GDPR erasure vs immutable event log

## Tension

- Audit regulations require attributable records retained for years (often 10+).
- GDPR Art. 17 grants erasure; retention obligations (Art. 17(3)(b)) may override it, but not
  for everything (e.g. customer marketing contacts, clinical patient data after retention).

## Options

| Option | Notes |
|---|---|
| Keep personal data out of events; reference ids only, PII in a separate erasable store | Cleanest; requires discipline in every event schema |
| Crypto-shredding (per-subject keys, delete key) | Works with immutable store; key management overhead |
| Rely on retention exemption | Valid for signer identity in GxP, not universally |

## Questions for the product owner

1. Will clinical/patient samples ever be in scope? (Changes everything.)
2. Is signer identity (name) in events acceptable given retention obligations? Likely yes.
