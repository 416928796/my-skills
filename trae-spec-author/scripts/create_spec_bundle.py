#!/usr/bin/env python3
"""Create an unfilled Trae spec bundle from canonical templates."""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--title", required=True)
    args = parser.parse_args()

    if not SLUG_RE.fullmatch(args.slug):
        parser.error("slug must be lowercase kebab-case")
    root = args.project_root.resolve()
    if not root.is_dir():
        parser.error(f"project root does not exist: {root}")

    target = root / ".trae" / "specs" / args.slug
    if target.exists():
        parser.error(f"refusing to overwrite existing bundle: {target}")
    target.mkdir(parents=True)

    assets = Path(__file__).resolve().parent.parent / "assets"
    for name in ("spec", "tasks", "checklist"):
        source = assets / f"{name}.template.md"
        content = source.read_text(encoding="utf-8")
        if name == "spec":
            content = content.replace("{{TITLE}}", args.title.strip())
        content = content.replace("{{SLUG}}", args.slug)
        (target / f"{name}.md").write_text(content, encoding="utf-8", newline="\n")

    (target / "tdd" / "tests").mkdir(parents=True)
    evidence = target / "tdd" / "evidence"
    evidence.mkdir(parents=True)
    summary = (assets / "SUMMARY.template.md").read_text(encoding="utf-8")
    summary = summary.replace("{{TITLE}}", args.title.strip())
    (evidence / "SUMMARY.md").write_text(summary, encoding="utf-8", newline="\n")
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
