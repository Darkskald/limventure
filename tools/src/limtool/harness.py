"""Consistency checks for the dual Claude Code / Codex harness."""

from pathlib import Path

import yaml

from limtool.docs import FRONTMATTER


def check(root: Path) -> list[str]:
    problems: list[str] = []
    claude_md = root / "CLAUDE.md"
    if not claude_md.is_file() or "@AGENTS.md" not in claude_md.read_text():
        problems.append("CLAUDE.md must import @AGENTS.md")
    link = root / ".claude" / "skills"
    if not link.is_symlink() or link.resolve() != (root / ".agents" / "skills").resolve():
        problems.append(".claude/skills must be a symlink to ../.agents/skills")
    for skill in sorted((root / ".agents" / "skills").glob("*/")):
        skill_md = skill / "SKILL.md"
        if not skill_md.is_file():
            problems.append(f"{skill.name}: missing SKILL.md")
            continue
        match = FRONTMATTER.match(skill_md.read_text())
        meta = yaml.safe_load(match.group(1)) if match else None
        if not isinstance(meta, dict) or not meta.get("description"):
            problems.append(f"{skill.name}: SKILL.md needs frontmatter with description")
        elif meta.get("name") != skill.name:
            problems.append(f"{skill.name}: frontmatter name '{meta.get('name')}' != directory")
    return problems
