---
title: EventSourcingDB licensing and limits
summary: Free-tier cap of 25,000 events, per-instance commercial pricing, offline license handling, expiry behaviour, and technical size limits.
tags: [eventsourcingdb, licensing, limits]
status: draft
sources:
  - https://docs.eventsourcingdb.io/about-eventsourcingdb/licensing/
  - https://docs.eventsourcingdb.io/blog/2026/07/23/introducing-our-new-pricing-model/
  - https://docs.eventsourcingdb.io/deployment-and-operations/limits/
  - https://docs.eventsourcingdb.io/deployment-and-operations/read-only-mode/
  - https://docs.eventsourcingdb.io/reference/cli-overview/
updated: 2026-10-28
---

# EventSourcingDB licensing and limits

## Free tier

- **Up to 25,000 stored events per instance** without a license key, in dev
  **and production**, all features enabled. Not time-limited per the docs.
- Observed in 1.2.0: without a key the server logs an auto-generated
  `evaluation` license (`maxEvents: 25000`). Its `expiresAt` is
  **process start + 1 year** with `--data-directory`, **+ 48 h** with
  `--data-directory-temporary`; regenerated on every start. The health check
  `license:remaining` reports `warn` for the 48 h variant.

## Commercial license (prices net, per instance)

| Plan | Per year | Per quarter |
|------|----------|-------------|
| Commercial | 2,500 EUR | 750 EUR |
| Individual developer | 360 EUR | 120 EUR |

- Required once an instance stores **more than 25,000 events**.
- **Bound to a single instance**; N instances = N licenses. Auto-renewing.
- Individual license only for natural persons without own company; any
  company use (incl. one-person GmbH/UG) → commercial.
- Volume licenses; reduced terms for startups/non-profits on request.
- Price does not depend on event count, seats, or cores once licensed.

## License handling

- Key file (`--license-file`) or string (`--license-string`).
- **No online activation, no phone-home** → works air-gapped.
- On expiry: database goes **read-only** for writes above the 25,000 threshold;
  all data stays readable/queryable/replayable. A restore whose backup exceeds
  the licensed capacity is rejected.
- Product is **closed-source**.

## Technical limits

| Limit | Value |
|-------|-------|
| Max events | 2^63−1 |
| Subjects / event types | no hard limit |
| Single event (as stored, incl. hash) | **64 KiB** → 400 otherwise |
| Write request body | 10 MiB |
| Read/observe/EventQL/schema/audit request body | 100 KiB |
| Restore body | unlimited (streamed) |
| Request body upload time | 5 s (408 otherwise) |
| Free disk reserve | writes refused below **1 GiB** free, resumes at 2 GiB |

Reads stream without a result-count limit; resume with `lowerBound`.

## Relevance for the LIMS (own conclusions)

- 25,000 events is enough for development, demos and CI, **not** for a real
  lab (a single sample lifecycle can easily produce 10–30 events). Budget
  2,500 EUR/year per production instance; staging/validation instances that
  hold production-like volumes need their own license.
- Air-gapped licensing is a plus for regulated on-prem labs.
- 64 KiB per event: raw instrument files, PDFs, chromatograms go to a blob
  store; events carry only references + content hashes.
- Plan monitoring on `store:eventCount` vs `store:eventCapacity` — hitting the
  cap means writes stop, which in a lab means work stops.
