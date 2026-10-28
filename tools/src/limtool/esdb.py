"""Thin wrappers around the EventSourcingDB docker compose setup."""

import json
import os
import subprocess
import urllib.error
import urllib.request
from pathlib import Path


def compose_dir(root: Path) -> Path:
    return root / "infra" / "eventsourcingdb"


def compose(root: Path, args: list[str], dev: bool = False) -> int:
    cmd = ["docker", "compose", "-f", "docker-compose.yml"]
    if dev:
        cmd += ["-f", "docker-compose.dev.yml"]
    return subprocess.call([*cmd, *args], cwd=compose_dir(root))


def env(root: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    env_file = compose_dir(root) / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                key, _, value = line.partition("=")
                values[key.strip()] = value.strip().strip('"')
    values.update({k: v for k, v in os.environ.items() if k.startswith("ESDB_")})
    return values


def ping(root: Path) -> int:
    values = env(root)
    url = values.get("ESDB_URL", f"http://localhost:{values.get('ESDB_HOST_PORT', '3000')}")
    token = values.get("ESDB_API_TOKEN", "")
    checks = [("ping", "GET", "/api/v1/ping", None)]
    if token:
        checks.append(("verify-api-token", "POST", "/api/v1/verify-api-token", {"Authorization": f"Bearer {token}"}))
    failed = 0
    for name, method, path, headers in checks:
        req = urllib.request.Request(url + path, method=method, headers=headers or {})
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                body = resp.read().decode()
                print(f"{name}: {resp.status} {json.loads(body).get('type', body) if body else ''}")
        except (urllib.error.URLError, OSError) as exc:
            print(f"{name}: FAILED {exc}")
            failed += 1
    return 1 if failed else 0
