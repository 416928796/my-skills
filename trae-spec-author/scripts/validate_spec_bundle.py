#!/usr/bin/env python3
"""Validate the structural contract of a completed Trae spec bundle."""

from __future__ import annotations

import re
import sys
from pathlib import Path

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PLACEHOLDER_RE = re.compile(r"\{\{[^}]+\}\}")
REQ_RE = re.compile(r"^### Requirement (REQ-\d{3}):", re.MULTILINE)
SCN_RE = re.compile(r"^#### Scenario (SCN-\d{3}):", re.MULTILINE)
TRACE_RE = re.compile(r"\[(REQ-\d{3})\]\[(SCN-\d{3})\]")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_spec_bundle.py <spec-directory>", file=sys.stderr)
        return 2
    bundle = Path(sys.argv[1]).resolve()
    errors: list[str] = []
    if not bundle.is_dir():
        errors.append(f"bundle directory does not exist: {bundle}")
    if not SLUG_RE.fullmatch(bundle.name):
        errors.append("bundle directory name must be lowercase kebab-case")

    texts: dict[str, str] = {}
    for filename in ("spec.md", "tasks.md", "checklist.md"):
        path = bundle / filename
        if not path.is_file():
            errors.append(f"missing {filename}")
            continue
        text = path.read_text(encoding="utf-8")
        texts[filename] = text
        if PLACEHOLDER_RE.search(text):
            errors.append(f"{filename} contains unfilled template placeholders")

    spec = texts.get("spec.md", "")
    positions = [spec.find(h) for h in ("## Why", "## What Changes", "## Impact", "## ADDED Requirements")]
    if any(p < 0 for p in positions) or positions != sorted(positions):
        errors.append("spec.md lacks required headings in canonical order")
    req_ids = REQ_RE.findall(spec)
    scn_ids = SCN_RE.findall(spec)
    if not req_ids or not scn_ids:
        errors.append("spec.md requires ID-bearing Requirement and Scenario headings")
    if len(req_ids) != len(set(req_ids)):
        errors.append("spec.md contains duplicate Requirement IDs")
    if len(scn_ids) != len(set(scn_ids)):
        errors.append("spec.md contains duplicate Scenario IDs")
    for marker in ("**WHEN**", "**THEN**", "SHALL"):
        if marker not in spec:
            errors.append(f"spec.md missing normative marker: {marker}")
    if spec.count("**TEST**") < len(scn_ids) or spec.count("**EVIDENCE**") < len(scn_ids):
        errors.append("every Scenario must declare TEST and EVIDENCE links")

    tasks = texts.get("tasks.md", "")
    if not tasks.startswith("# Tasks") or "- [ ] Task " not in tasks:
        errors.append("tasks.md must start with # Tasks and contain unchecked tasks")
    if "# Task Dependencies" not in tasks:
        errors.append("tasks.md missing # Task Dependencies")
    checklist = texts.get("checklist.md", "")
    if not checklist.startswith("# Checklist") or "- [ ] " not in checklist:
        errors.append("checklist.md must start with # Checklist and contain unchecked items")
    if re.search(r"^- \[[xX]\]", tasks + "\n" + checklist, re.MULTILINE):
        errors.append("new bundle contains pre-completed checkboxes")

    tests_dir = bundle / "tdd" / "tests"
    summary = bundle / "tdd" / "evidence" / "SUMMARY.md"
    summary_text = ""
    if not tests_dir.is_dir():
        errors.append("missing tdd/tests directory")
    if not summary.is_file():
        errors.append("missing tdd/evidence/SUMMARY.md")
    else:
        summary_text = summary.read_text(encoding="utf-8")
        for heading in ("## Metadata", "## Verdict", "## Requirement traceability", "## TDD cycle results", "## Regression"):
            if heading not in summary_text:
                errors.append(f"SUMMARY.md missing heading: {heading}")

    known_reqs, known_scns = set(req_ids), set(scn_ids)
    for req_id in req_ids:
        if req_id not in tasks or req_id not in checklist or req_id not in summary_text:
            errors.append(f"Requirement ID is not traced across tasks/checklist/SUMMARY: {req_id}")
    for scn_id in scn_ids:
        if scn_id not in tasks or scn_id not in checklist or scn_id not in summary_text:
            errors.append(f"Scenario ID is not traced across tasks/checklist/SUMMARY: {scn_id}")
    for filename, text in (("tasks.md", tasks), ("checklist.md", checklist), ("SUMMARY.md", summary_text)):
        for req_id, scn_id in TRACE_RE.findall(text):
            if req_id not in known_reqs or scn_id not in known_scns:
                errors.append(f"{filename} contains unknown trace pair [{req_id}][{scn_id}]")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Valid Trae spec bundle: {bundle}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
