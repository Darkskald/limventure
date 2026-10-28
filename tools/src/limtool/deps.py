"""Compare exact upstream pins (ADR-0008) with the latest published releases."""

import json
import re
import tomllib
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from limtool import esdm

USER_AGENT = "limventure-limtool (deps outdated)"
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


@dataclass
class Pin:
    name: str
    pinned: str
    latest: str | None

    @property
    def outdated(self) -> bool:
        return self.latest is not None and self.latest != self.pinned


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.load(resp)


def cargo_pins(root: Path) -> dict[str, str]:
    deps = tomllib.loads((root / "Cargo.toml").read_text())["workspace"]["dependencies"]
    pins = {}
    for crate in ("architecturekit", "eventsourcingdb"):
        spec = deps[crate]
        version = spec["version"] if isinstance(spec, dict) else spec
        pins[crate] = version.removeprefix("=")
    return pins


def image_pin(root: Path) -> str:
    compose = (root / "infra" / "eventsourcingdb" / "docker-compose.yml").read_text()
    match = re.search(r"thenativeweb/eventsourcingdb:\$\{ESDB_IMAGE_TAG:-([^}]+)\}", compose)
    if not match:
        raise SystemExit("limtool: cannot find pinned eventsourcingdb image tag in docker-compose.yml")
    return match.group(1)


def latest_crate(crate: str) -> str:
    return fetch_json(f"https://crates.io/api/v1/crates/{crate}")["crate"]["max_stable_version"]


def latest_image() -> str:
    url = "https://hub.docker.com/v2/repositories/thenativeweb/eventsourcingdb/tags?page_size=50"
    tags = [t["name"] for t in fetch_json(url)["results"] if SEMVER.match(t["name"])]
    return max(tags, key=lambda v: tuple(int(p) for p in v.split(".")))


def latest_esdm() -> str:
    return fetch_json("https://www.esdm.io/version.json")["version"]


def collect(root: Path) -> list[Pin]:
    crates = cargo_pins(root)
    sources = [
        *((f"crate {name}", version, lambda n=name: latest_crate(n)) for name, version in crates.items()),
        ("image thenativeweb/eventsourcingdb", image_pin(root), latest_image),
        ("cli esdm", esdm.VERSION, latest_esdm),
    ]
    pins = []
    for name, pinned, lookup in sources:
        try:
            latest = lookup()
        except (OSError, KeyError, ValueError):
            latest = None
        pins.append(Pin(name, pinned, latest))
    return pins
