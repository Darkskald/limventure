"""Generate a LIMS-free harness for a new architecturekit / EventSourcingDB / ESDM project.

Driven by `tools/breakout/manifest.yaml`; templates live in `tools/breakout/templates/`.
Everything mechanical happens here; the agent only rewrites the reported leaks.
"""

import os
import re
import subprocess
from dataclasses import dataclass, field
from datetime import date
from fnmatch import fnmatch
from pathlib import Path

import yaml

from limtool import docs

NAME = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
TOOL = re.compile(r"^[a-z][a-z0-9_]*$")
HEADING = re.compile(r"^(#{1,6}) ")


@dataclass
class Report:
    files: list[str] = field(default_factory=list)
    leaks: list[str] = field(default_factory=list)


def manifest_dir(root: Path) -> Path:
    return root / "tools" / "breakout"


def load_manifest(root: Path) -> dict:
    return yaml.safe_load((manifest_dir(root) / "manifest.yaml").read_text())


def source_files(root: Path) -> list[str]:
    """Tracked plus untracked-but-not-ignored files, so fresh docs are included."""
    out = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    return sorted(p for p in out.splitlines() if (root / p).is_file() and not (root / p).is_symlink())


def matches(rel: str, globs: list[str]) -> bool:
    return any(fnmatch(rel, g) for g in globs)


def strip_sections(text: str, pattern: re.Pattern[str]) -> str:
    """Drop every markdown section whose heading matches `pattern`, including its subsections."""
    kept: list[str] = []
    skip_level = 0
    fenced = False
    for line in text.splitlines(keepends=True):
        if line.startswith("```"):
            fenced = not fenced
        heading = None if fenced else HEADING.match(line)
        if heading:
            level = len(heading.group(1))
            if skip_level and level <= skip_level:
                skip_level = 0
            if not skip_level and pattern.search(line):
                skip_level = level
        if not skip_level:
            kept.append(line)
    return "".join(kept).rstrip("\n") + "\n"


class Rewriter:
    def __init__(self, manifest: dict, name: str, tool: str) -> None:
        values = {"name": name, "tool": tool, "date": date.today().isoformat()}
        self.pairs = [(old, new.format(**values)) for old, new in manifest["replace"]]
        self.renumber = {str(k): str(v) for k, v in manifest.get("adr_renumber", {}).items()}
        self.values = values
        self.section = re.compile(manifest["strip_sections"])
        self.drop = re.compile(manifest["drop_lines"])
        self.scoped = [(rule["glob"], rule["pairs"]) for rule in manifest.get("scoped_replace", [])]

    def path(self, rel: str) -> str:
        for old, new in self.pairs:
            rel = rel.replace(old, new)
        return re.sub(
            r"(docs/adr/)(\d{4})-", lambda m: m.group(1) + self.renumber.get(m.group(2), m.group(2)) + "-", rel
        )

    def text(self, text: str, rel: str = "") -> str:
        if rel.endswith(".md"):
            text = strip_sections(text, self.section)
        for glob, pairs in self.scoped:
            if fnmatch(rel, glob):
                for old, new in pairs:
                    text = text.replace(old, new)
        text = "".join(line for line in text.splitlines(keepends=True) if not self.drop.search(line))
        for old, new in self.pairs:
            text = text.replace(old, new)
        text = re.sub(r"ADR-(\d{4})", lambda m: "ADR-" + self.renumber.get(m.group(1), m.group(1)), text)
        return re.sub(
            r"(?<=[/(])(\d{4})(-[a-z0-9-]+\.md)", lambda m: self.renumber.get(m.group(1), m.group(1)) + m.group(2), text
        )

    def template(self, text: str) -> str:
        for key, value in self.values.items():
            text = text.replace("{{" + key + "}}", value)
        return text


def write(target: Path, rel: str, data: bytes, report: Report) -> None:
    dest = target / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    report.files.append(rel)


def generate(root: Path, target: Path, name: str, tool: str) -> Report:
    if not NAME.match(name):
        raise SystemExit(f"breakout: project name '{name}' must be kebab-case")
    if not TOOL.match(tool):
        raise SystemExit(f"breakout: tool name '{tool}' must be a Python identifier")
    if target.exists() and any(target.iterdir()):
        raise SystemExit(f"breakout: {target} exists and is not empty")
    manifest = load_manifest(root)
    rw = Rewriter(manifest, name, tool)
    report = Report()

    for rel in source_files(root):
        if not matches(rel, manifest["copy"]) or matches(rel, manifest["exclude"]):
            continue
        data = (root / rel).read_bytes()
        if not matches(rel, manifest["verbatim"]):
            data = rw.text(data.decode(), rel).encode()
        write(target, rw.path(rel), data, report)

    templates = manifest_dir(root) / "templates"
    for src in sorted(p for p in templates.rglob("*") if p.is_file()):
        rel = rw.template(src.relative_to(templates).as_posix())
        write(target, rel, rw.template(src.read_text()).encode(), report)

    (target / ".claude").mkdir(exist_ok=True)
    os.symlink("../.agents/skills", target / ".claude" / "skills")
    index = docs.render_index(target / "docs") + "\n"
    for old, new in rw.pairs:
        index = index.replace(old, new)
    write(target, "docs/INDEX.md", index.encode(), report)
    report.leaks = scan(target, manifest)
    return report


def scan(target: Path, manifest: dict) -> list[str]:
    """Residual source-project references the agent must rewrite: terms, unknown ADRs, broken links."""
    terms = re.compile(manifest["leak_terms"], re.IGNORECASE)
    adrs = {p.name[:4] for p in (target / "docs" / "adr").glob("*.md")}
    leaks: list[str] = []
    for path in sorted(p for p in target.rglob("*") if p.is_file() and not p.is_symlink()):
        rel = path.relative_to(target).as_posix()
        if matches(rel, manifest["verbatim"]) or rel == "docs/INDEX.md" or rel.endswith(".lock"):
            continue
        for no, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
            unknown = [a for a in re.findall(r"ADR-(\d{4})", line) if a not in adrs]
            if terms.search(line) or unknown:
                leaks.append(f"{rel}:{no}: {line.strip()[:120]}")
    errors, _ = docs.lint(target / "docs")
    leaks += [f"docs lint: {e}" for e in errors]
    return leaks
