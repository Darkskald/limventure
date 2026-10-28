# EventSourcingDB (local infrastructure)

Compose setup for [EventSourcingDB](https://docs.eventsourcingdb.io/), pinned to
image `thenativeweb/eventsourcingdb:1.2.0` (latest stable as of 2026-10-28).
Background: [docs/knowledge/eventsourcingdb/](../../docs/knowledge/eventsourcingdb/overview.md).

## Setup

```sh
cd infra/eventsourcingdb
cp .env.example .env
# put a random token (>= 32 chars, letters + digits) into ESDB_API_TOKEN
sed -i "s/^ESDB_API_TOKEN=.*/ESDB_API_TOKEN=$(openssl rand -hex 24)/" .env
```

`.env` is git-ignored. Never commit a real token.

## Mode A — default (persistent)

```sh
docker compose up -d
```

- Data in named volume `limventure-esdb_esdb-data` → `/var/lib/esdb`.
- No license → free tier, **max 25,000 events**.
- Plain HTTP, bound to `127.0.0.1:${ESDB_HOST_PORT:-3000}` only. No UI.
- Healthcheck: `wget` on `/api/v1/ping` (no token needed).

## Mode B — dev (throw-away, with UI)

```sh
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

- `--data-directory-temporary`: **all data is gone when the container stops.**
- Management UI at `http://localhost:3000` (login = API token).

Do not run both modes at once (same container name and port).

## Smoke test

```sh
set -a; . ./.env; set +a
curl -i http://127.0.0.1:${ESDB_HOST_PORT:-3000}/api/v1/ping
curl -i -X POST -H "Authorization: Bearer $ESDB_API_TOKEN" \
  http://127.0.0.1:${ESDB_HOST_PORT:-3000}/api/v1/verify-api-token
```

Expected: both `HTTP/1.1 200 OK`; ping returns event type
`io.eventsourcingdb.api.ping-received`, token check returns
`io.eventsourcingdb.api.api-token-verified`. Wrong token → 401.

## Stop / reset

```sh
docker compose down        # keep data
docker compose down -v     # delete the volume (all events!)
```

## Integrity tooling

```sh
H="Authorization: Bearer $ESDB_API_TOKEN"; U=http://127.0.0.1:3000/api/v1
curl -s -X POST -H "$H" $U/audit-history   # last line: latestEventId/latestEventHash
curl -s -X POST -H "$H" $U/verify-store    # last line: errors/warnings
curl -s -X POST -H "$H" $U/backup -o backup.ndjson   # check last line is not an error
```

## Optional: signing key / license

```sh
mkdir -p secrets
openssl genpkey -algorithm ED25519 -out secrets/signing-key.pem
openssl pkey -in secrets/signing-key.pem -pubout -out secrets/signing-key.pub.pem
chmod 644 secrets/signing-key.pem   # container runs as uid 100, must be readable
```

Then uncomment the `--signing-key-file` / `--license-file` lines and the
`./secrets:/etc/esdb:ro` mount in `docker-compose.yml`. Keep `secrets/` out of
git (add it to `.gitignore` before use).

## Not production-ready

For anything beyond a developer machine: enable HTTPS
(`--https-certificate-file`, `--https-private-key-file`, drop `--http-enabled`),
supply a license above 25,000 events, keep the UI off, and inject the token from
a secret store. Note the token is visible in `docker inspect` because
EventSourcingDB only accepts flags.
