"""Pinned ESDM CLI installer and argument forwarder."""

import hashlib
import os
import platform
import subprocess
import sys
import urllib.request
from pathlib import Path

VERSION = "0.15.0"
BASE_URL = f"https://esdm.s3.fr-par.scw.cloud/{VERSION}"
# SHA256 as published on https://www.esdm.io/getting-started/installing-esdm/
CHECKSUMS: dict[str, str] = {
    "esdm-linux-amd64": "db76e45729e5318023120143356df461dbddfbedf2108111c0d8b7b595f42a84",
    "esdm-linux-arm64": "5076335000631e8701cf07fc610dcc86c806c7422fd86ad68eea27b212820019",
    "esdm-darwin-amd64": "b4e0009243fb5ed822fbade6e8f469395227feba95269b1e59afbe33fad14705",
    "esdm-darwin-arm64": "ea11a2629447b54a8475b67d30d01215b74fc61fe563c4715119c73d6f823f88",
    "esdm-windows-amd64.exe": "0f82f30bbe73f0c68ec6633851599f3a1cf2c1f1e663cb6815b7b13f6abda5e7",
    "esdm-windows-arm64.exe": "8cdd0a01f740e4d1833f839ad96865bf202b748c18550659b873ff77a03b39ca",
}


def target() -> str:
    system = {"Linux": "linux", "Darwin": "darwin", "Windows": "windows"}[platform.system()]
    arch = {"x86_64": "amd64", "AMD64": "amd64", "aarch64": "arm64", "arm64": "arm64"}[platform.machine()]
    return f"esdm-{system}-{arch}" + (".exe" if system == "windows" else "")


def binary_path(root: Path) -> Path:
    return root / ".tools" / "bin" / f"esdm-{VERSION}"


def install(root: Path) -> Path:
    dest = binary_path(root)
    if dest.exists():
        return dest
    name = target()
    expected = CHECKSUMS.get(name)
    if not expected:
        raise SystemExit(f"limtool: no pinned checksum for {name}; add it to limtool/esdm.py")
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(f"{BASE_URL}/{name}") as resp:
        data = resp.read()
    actual = hashlib.sha256(data).hexdigest()
    if actual != expected:
        raise SystemExit(f"limtool: checksum mismatch for {name}: {actual} != {expected}")
    tmp = dest.with_suffix(".part")
    tmp.write_bytes(data)
    tmp.chmod(0o755)
    os.replace(tmp, dest)
    return dest


def run(root: Path, args: list[str]) -> int:
    """Run esdm inside model/ so lint/view operate on the domain model."""
    exe = install(root)
    cwd = root / "model"
    cwd.mkdir(exist_ok=True)
    env = {**os.environ, "ESDM_DISABLE_UPDATE_CHECK": "true"}
    return subprocess.call([str(exe), *args], cwd=cwd, env=env, stdout=sys.stdout, stderr=sys.stderr)
