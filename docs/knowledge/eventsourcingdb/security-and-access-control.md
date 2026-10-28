---
title: EventSourcingDB security and access control
summary: Single shared bearer token, no users or roles, TLS options and network-isolation guidance for EventSourcingDB.
tags: [eventsourcingdb, security, access-control, tls]
status: draft
sources:
  - https://docs.eventsourcingdb.io/deployment-and-operations/security-and-access-control/
  - https://docs.eventsourcingdb.io/deployment-and-operations/managing-configuration-and-secrets/
  - https://docs.eventsourcingdb.io/reference/cli-overview/
  - https://docs.eventsourcingdb.io/getting-started/using-the-management-ui/
updated: 2026-10-28
---

# EventSourcingDB security and access control

## Authentication

- **One API token** (`--api-token`) for the whole API and the UI.
  `Authorization: Bearer <token>`; missing/invalid → **401**.
- Only `/api/v1/ping` is unauthenticated.
- **No users, no roles, no permissions, no read-only token** — all-or-nothing.
  Anyone with the token can write, back up, restore, switch to read-only.
- Vendor recommendation: ≥ 32 chars, mixed-case letters + digits, random;
  rotate periodically; never in URLs; do not log it.
- `POST /api/v1/verify-api-token` checks a token (200 / 401).

## Transport

- HTTPS is **on by default** (port 4000) and needs cert + key files.
- HTTP (port 3000) is off by default; for dev or behind a TLS-terminating
  proxy.
- Vendor: run only in **private networks**, never publicly exposed; if needed
  externally use a reverse proxy with auth, TLS, rate limiting.
- The v2 API (≥ 1.3) reads with the HTTP method `QUERY`; proxies must pass it.

## Secrets

- Flags only, no env-var config → inject via shell/Compose/K8s expansion.
- License file / TLS files: restrictive permissions (`chmod 600`),
  read-only mount, not baked into images.
- Signing key: confidential, ideally from a vault; only ESDB needs it.

## Management UI

Same token; "only for development and debugging, never expose to the public
internet".

## Relevance for the LIMS (own conclusions)

- 21 CFR 11.10(d)/(g) (limited access, authority checks) **cannot** be met at
  the ESDB layer. ESDB must be a backend-only component; the LIMS services own
  authN/authZ and are the only token holders.
- Separate tokens per service are impossible → one compromised service = full
  store access (incl. restore into an empty instance and read-only switch).
  Network-segment ESDB so only the write/read services can reach it.
- Token rotation means a restart with a new flag value and, with a single
  token, no overlap window → coordinated rollout of all clients.
- Operational endpoints (backup, restore, read-only) should be reachable only
  from an admin network path, enforced by the proxy.
- Never enable `--with-ui` in validated environments.
