"""Architecture Decision Record scaffolding."""

import re
from datetime import date
from pathlib import Path

TEMPLATE = """---
title: "ADR-{num:04d}: {title}"
summary: TODO one sentence stating the decision.
tags: [adr]
status: proposed
updated: {today}
---

# ADR-{num:04d}: {title}

## Context

What forces are at play? Link requirements (REQ-xxx) and knowledge docs.

## Decision

What we do. Active voice, unambiguous.

## Alternatives considered

| Option | Pros | Cons |
|---|---|---|

## Consequences

Positive, negative, and what becomes harder. Audit/compliance impact explicitly.

## Open points

Anything not yet agreed with the product owner.
"""


def slugify(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def next_number(adr_dir: Path) -> int:
    nums = [int(m.group(1)) for p in adr_dir.glob("*.md") if (m := re.match(r"(\d{4})-", p.name))]
    return max(nums, default=0) + 1


def create(adr_dir: Path, title: str) -> Path:
    num = next_number(adr_dir)
    path = adr_dir / f"{num:04d}-{slugify(title)}.md"
    path.write_text(TEMPLATE.format(num=num, title=title, today=date.today().isoformat()), encoding="utf-8")
    return path
