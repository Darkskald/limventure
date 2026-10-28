"""Repository path resolution."""

from pathlib import Path


def repo_root() -> Path:
    """Walk up from the cwd until AGENTS.md (the harness anchor) is found."""
    here = Path.cwd().resolve()
    for candidate in (here, *here.parents):
        if (candidate / "AGENTS.md").is_file():
            return candidate
    raise SystemExit("limtool: not inside the repository (no AGENTS.md found)")


def docs_dir() -> Path:
    return repo_root() / "docs"
