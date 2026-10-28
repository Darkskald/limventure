---
title: EventSourcingDB integrity, signatures and auditing
summary: Exact hash-chain algorithm (v1/v2), Ed25519 response signatures, audit-history and verify-store endpoints, and what they do and do not prove.
tags: [eventsourcingdb, integrity, signatures, audit, compliance]
status: draft
sources:
  - https://docs.eventsourcingdb.io/deployment-and-operations/verifying-event-signatures/
  - https://docs.eventsourcingdb.io/deployment-and-operations/auditing-the-event-store/
  - https://docs.eventsourcingdb.io/deployment-and-operations/verifying-store-integrity/
  - https://docs.eventsourcingdb.io/best-practices/event-signatures-and-validation/
  - https://docs.eventsourcingdb.io/fundamentals/cloud-events/
  - https://docs.eventsourcingdb.io/reference/cli-overview/
updated: 2026-10-28
---

# EventSourcingDB integrity, signatures and auditing

Three independent mechanisms. All verified against image `1.2.0`.

## 1. Hash chain (always on)

Every event has `hash` (SHA-256, lowercase hex) and `predecessorhash` = hash of
the **previous event in the whole store** (first event: 64 × `0`). Chain is
store-wide, not per subject. Hashes are **persisted** and key-independent.

**v1** (unprefixed; written by ≤ 1.2.x):
1. `meta = specversion|id|predecessorhash|time|source|subject|type|datacontenttype`
   (pipe, no spaces; `time` = string as returned) → `h_meta = sha256(meta)`.
2. `h_data = sha256(data bytes exactly as in the response)` — never re-serialize.
3. `hash = sha256(hex(h_meta) + hex(h_data))`. Does **not** cover trace fields.

Reproduced locally in Python against a 1.2.0 response: match.

**v2** (prefix `esdb:hash:v2:`, written since 1.3, old events keep v1):
lines joined by `\n` (no trailing newline): `esdb:hash:v2:`, `specversion`,
`id`, `predecessorhash`, `time`, `source`, `subject`, `type`,
`datacontenttype`, `traceparent`, `tracestate`, `data` (missing field = `-`);
`hash = "esdb:hash:v2:" + hex(sha256(...))`. Unknown prefix version →
"unsupported", not "tampered".

## 2. Signatures (optional, `--signing-key-file`)

- Key: Ed25519, PKCS#8 PEM (`openssl genpkey -algorithm ED25519`). Server
  needs only the private key; distribute the public key **out of band** (no
  endpoint for it).
- Format: `esdb:signature:v1:` + hex Ed25519 signature over the **text of the
  `hash` field** (prefix included, characters not decoded bytes).
- Signed on every route returning events (write, read, observe); otherwise
  `signature: null`.
- **Signatures are not stored**; computed on the fly with the current key.
  After key rotation old signatures are unverifiable; re-fetch to re-sign.
- Proves: the event was served by an instance holding the key, content
  matches hash. Does **not** prove who (which user) wrote it.
- Verified: `openssl pkeyutl -verify -rawin` on hash text → success.

## 3. Server-side checks

`POST /api/v1/audit-history` — walks the hash chain.
- Body optional: `{latestEventId, latestEventHash}` from the last audit; the
  server checks that this event still has this hash and the chain continues.
- NDJSON with heartbeats; last line `{"type":"result","payload":
  {"latestEventId":"…","latestEventHash":"…"}}` (`{}` if empty store) or
  `{"type":"error",…}`. **Status is 200 before the result → only the last line
  counts.** Covers events up to the latest at start; writes continue.

`POST /api/v1/verify-store` — full recomputation of all hashes, data
consistency and **all indexes**. Result `{"errors":[],"warnings":[]}`;
reports up to 100 issues per check; chain checking stops at the first break.
Resource-intensive; run off-peak. Same last-line rule.

Both verified on 1.2.0 (`audit-history` returned id/hash of last event,
`verify-store` returned empty errors/warnings).

## Relevance for the LIMS (own conclusions)

- **21 CFR 11.10(e)/(c), ISO 17025 7.5/7.11**: immutability (no update/delete
  API) + hash chain give a strong technical audit-trail basis. Still required
  in the application: user identity, action time, reason for change, and
  **e-signature records (11.50/11.70)** inside `data` — ESDB's signature is a
  server/transport signature, not a user signature.
- The chain is self-referential: anyone with filesystem write access could
  rewrite the store and recompute all hashes. Mitigation: **anchor**
  `latestEventHash` externally (scheduled audit → store result in a separate
  WORM/system, sign it, optionally RFC 3161 timestamp).
- Do not rely solely on the server's own `audit-history` for evidence;
  implement an independent verifier (Rust SDK `verify_hash`) over a backup.
- Signatures are ephemeral → never archive them as proof; archive hashes.
- Plan the v1 → v2 hash transition in validation (verifier must support both).
