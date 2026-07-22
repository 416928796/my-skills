#!/usr/bin/env python3
"""Create the standard TDD layout inside one Trae spec directory."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


REQUIRED_SPEC_FILES = ("spec.md", "tasks.md", "checklist.md")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec_dir", type=Path)
    parser.add_argument("--force-summary", action="store_true")
    args = parser.parse_args()

    spec_dir = args.spec_dir.resolve()
    if not spec_dir.is_dir():
        parser.error(f"spec directory does not exist: {spec_dir}")

    missing = [name for name in REQUIRED_SPEC_FILES if not (spec_dir / name).is_file()]
    if missing:
        parser.error(f"not a Trae spec directory; missing: {', '.join(missing)}")

    tests_dir = spec_dir / "tdd" / "tests"
    evidence_dir = spec_dir / "tdd" / "evidence"
    tests_dir.mkdir(parents=True, exist_ok=True)
    evidence_dir.mkdir(parents=True, exist_ok=True)

    template = Path(__file__).resolve().parent.parent / "assets" / "SUMMARY.template.md"
    summary = evidence_dir / "SUMMARY.md"
    if args.force_summary or not summary.exists():
        shutil.copyfile(template, summary)

    print(f"tests: {tests_dir}")
    print(f"evidence: {evidence_dir}")
    print(f"summary: {summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
