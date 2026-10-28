from pathlib import Path

from limtool import adr, docs

GOOD = """---
title: Sample handling
summary: How samples move through the lab.
tags: [sample, lifecycle]
status: draft
updated: 2026-10-28
---

# Sample handling

See [other](other-doc.md). Aliquots matter.
"""


def write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def test_lint_clean(tmp_path: Path) -> None:
    write(tmp_path, "domain/sample-handling.md", GOOD)
    write(tmp_path, "domain/other-doc.md", GOOD.replace("other-doc.md", "sample-handling.md"))
    errors, warnings = docs.lint(tmp_path)
    assert errors == [] and warnings == []


def test_lint_reports_problems(tmp_path: Path) -> None:
    write(tmp_path, "knowledge/x/BadName.md", GOOD)
    write(tmp_path, "domain/no-meta.md", "# nothing\n")
    write(tmp_path, "domain/huge.md", GOOD.replace("other-doc.md", "huge.md") + "x\n" * 300)
    errors, _ = docs.lint(tmp_path)
    text = "\n".join(errors)
    assert "kebab-case" in text
    assert "require 'sources'" in text
    assert "broken link" in text
    assert "no-meta.md: missing frontmatter" in text
    assert "exceeds hard limit" in text


def test_index_and_search(tmp_path: Path) -> None:
    write(tmp_path, "domain/sample-handling.md", GOOD)
    index = docs.render_index(tmp_path)
    assert "[Sample handling](domain/sample-handling.md)" in index
    hits = docs.search(tmp_path, ["aliquot"])
    assert [d.rel for _, d in hits] == ["domain/sample-handling.md"]
    assert docs.search(tmp_path, ["aliquot", "nonexistent"]) == []
    assert docs.search(tmp_path, ["aliquot"], tag="billing") == []


def test_adr_numbering(tmp_path: Path) -> None:
    first = adr.create(tmp_path, "Use EventSourcingDB")
    second = adr.create(tmp_path, "Tenant isolation!")
    assert first.name == "0001-use-eventsourcingdb.md"
    assert second.name == "0002-tenant-isolation.md"
    assert "status: proposed" in second.read_text()
