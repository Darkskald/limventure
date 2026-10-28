import re
from pathlib import Path

import pytest

from limtool import breakout, harness

REPO = Path(__file__).resolve().parents[2]


def test_strip_sections_removes_subsections_but_not_fenced_headings() -> None:
    text = "# T\n\n## Keep\na\n\n## Relevance for the LIMS\nb\n### Sub\nc\n## Next\n```\n## LIMS in code\n```\n"
    out = breakout.strip_sections(text, re.compile(r"LIMS"))
    assert "Relevance" not in out and "Sub" not in out and "b\n" not in out
    assert "## Keep\na" in out and "## Next" in out and "## LIMS in code" in out


def test_rewriter_renumbers_adrs_and_renames() -> None:
    manifest = {
        "replace": [["limtool", "{tool}"]],
        "adr_renumber": {"0007": "0004"},
        "strip_sections": "LIMS",
        "drop_lines": "^lims-",
    }
    rw = breakout.Rewriter(manifest, "demo", "devtool")
    assert rw.path("docs/adr/0007-dogfood.md") == "docs/adr/0004-dogfood.md"
    assert rw.path("tools/src/limtool/cli.py") == "tools/src/devtool/cli.py"
    text = rw.text("See [ADR-0007](../adr/0007-dogfood.md), run limtool.\nlims-kernel = 1\n", "x.md")
    assert text == "See [ADR-0004](../adr/0004-dogfood.md), run devtool.\n"


def test_rejects_non_empty_target(tmp_path: Path) -> None:
    (tmp_path / "file").write_text("x")
    with pytest.raises(SystemExit):
        breakout.generate(REPO, tmp_path, "demo", "devtool")


def test_breakout_of_this_repo_is_clean(tmp_path: Path) -> None:
    """Regression gate: new LIMS content in generic docs must be stripped, renamed or excluded."""
    target = tmp_path / "demo"
    report = breakout.generate(REPO, target, "demo-shop", "devtool")
    assert report.leaks == []
    assert harness.check(target) == []
    assert (target / "tools" / "src" / "devtool" / "cli.py").is_file()
    assert not (target / "tools" / "src" / "devtool" / "breakout.py").exists()
    assert (target / "model" / "schemas").is_dir()
