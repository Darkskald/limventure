from pathlib import Path

import pytest

from limtool import deps


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    (tmp_path / "Cargo.toml").write_text(
        '[workspace.dependencies]\narchitecturekit = { version = "=0.21.0" }\neventsourcingdb = "=4.0.4"\n'
    )
    compose = tmp_path / "infra" / "eventsourcingdb"
    compose.mkdir(parents=True)
    (compose / "docker-compose.yml").write_text("image: thenativeweb/eventsourcingdb:${ESDB_IMAGE_TAG:-1.2.0}\n")
    return tmp_path


def test_reads_pins(repo: Path) -> None:
    assert deps.cargo_pins(repo) == {"architecturekit": "0.21.0", "eventsourcingdb": "4.0.4"}
    assert deps.image_pin(repo) == "1.2.0"


def test_flags_outdated_and_tolerates_lookup_failure(repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(deps, "latest_crate", lambda name: {"architecturekit": "0.22.0"}.get(name, "4.0.4"))
    monkeypatch.setattr(deps, "latest_image", lambda: "1.2.0")

    def offline() -> str:
        raise OSError("offline")

    monkeypatch.setattr(deps, "latest_esdm", offline)
    pins = {p.name: p for p in deps.collect(repo)}
    assert pins["crate architecturekit"].outdated
    assert not pins["crate eventsourcingdb"].outdated
    assert not pins["image thenativeweb/eventsourcingdb"].outdated
    assert pins["cli esdm"].latest is None
