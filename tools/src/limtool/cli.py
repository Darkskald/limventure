"""Command-line entry point. Every command is deterministic and exits non-zero on failure."""

import argparse
import sys

from limtool import adr, docs, esdb, esdm, harness
from limtool.paths import docs_dir, repo_root


def cmd_docs_index(args: argparse.Namespace) -> int:
    root = docs_dir()
    rendered = docs.render_index(root) + "\n"
    index = root / docs.INDEX_NAME
    current = index.read_text(encoding="utf-8") if index.exists() else ""
    if args.check:
        if current != rendered:
            print("docs/INDEX.md is stale — run `limtool docs index`")
            return 1
        return 0
    index.write_text(rendered, encoding="utf-8")
    print(f"wrote {index.relative_to(repo_root())}")
    return 0


def cmd_docs_lint(args: argparse.Namespace) -> int:
    errors, warnings = docs.lint(docs_dir())
    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")
    return 1 if errors else 0


def cmd_docs_search(args: argparse.Namespace) -> int:
    hits = docs.search(docs_dir(), args.terms, args.tag)
    for score, doc in hits[: args.limit]:
        print(f"docs/{doc.rel}\t{score}\t{doc.meta.get('summary', '')}")
    return 0 if hits else 1


def cmd_adr_new(args: argparse.Namespace) -> int:
    path = adr.create(docs_dir() / "adr", args.title)
    print(path.relative_to(repo_root()))
    return 0


def cmd_esdm(args: argparse.Namespace) -> int:
    if args.esdm_args == ["install"]:
        print(esdm.install(repo_root()))
        return 0
    return esdm.run(repo_root(), args.esdm_args)


def cmd_esdb(args: argparse.Namespace) -> int:
    root = repo_root()
    if args.action == "ping":
        return esdb.ping(root)
    compose_args = {"up": ["up", "-d", "--wait"], "down": ["down"], "logs": ["logs", "--tail", "100"]}
    return esdb.compose(root, compose_args[args.action], dev=args.dev)


def cmd_harness_check(args: argparse.Namespace) -> int:
    problems = harness.check(repo_root())
    for p in problems:
        print(f"error: {p}")
    return 1 if problems else 0


def cmd_check(args: argparse.Namespace) -> int:
    """Run every repository gate; used by agents before finishing a task."""
    results = {
        "harness": cmd_harness_check(args),
        "docs lint": cmd_docs_lint(args),
        "docs index": cmd_docs_index(argparse.Namespace(check=True)),
    }
    for name, code in results.items():
        print(f"{'ok  ' if code == 0 else 'FAIL'} {name}")
    return 1 if any(results.values()) else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="limtool", description=__doc__)
    sub = parser.add_subparsers(required=True)

    p_docs = sub.add_parser("docs", help="documentation index, lint, search").add_subparsers(required=True)
    p = p_docs.add_parser("index", help="regenerate docs/INDEX.md")
    p.add_argument("--check", action="store_true", help="fail if INDEX.md is stale")
    p.set_defaults(func=cmd_docs_index)
    p_docs.add_parser("lint", help="validate frontmatter, size, links").set_defaults(func=cmd_docs_lint)
    p = p_docs.add_parser("search", help="ranked search over docs")
    p.add_argument("terms", nargs="+")
    p.add_argument("--tag")
    p.add_argument("--limit", type=int, default=10)
    p.set_defaults(func=cmd_docs_search)

    p_adr = sub.add_parser("adr", help="architecture decision records").add_subparsers(required=True)
    p = p_adr.add_parser("new", help="scaffold the next ADR")
    p.add_argument("title")
    p.set_defaults(func=cmd_adr_new)

    p = sub.add_parser("esdm", help="run pinned ESDM CLI in model/ ('install' to only download)")
    p.add_argument("esdm_args", nargs=argparse.REMAINDER)
    p.set_defaults(func=cmd_esdm)

    p = sub.add_parser("esdb", help="local EventSourcingDB via docker compose")
    p.add_argument("action", choices=["up", "down", "logs", "ping"])
    p.add_argument("--dev", action="store_true", help="use throw-away dev profile")
    p.set_defaults(func=cmd_esdb)

    p_h = sub.add_parser("harness", help="harness consistency").add_subparsers(required=True)
    p_h.add_parser("check", help="verify CLAUDE.md/AGENTS.md/skills wiring").set_defaults(func=cmd_harness_check)

    sub.add_parser("check", help="run all repository gates").set_defaults(func=cmd_check)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    sys.exit(args.func(args))
