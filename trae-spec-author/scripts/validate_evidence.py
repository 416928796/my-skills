#!/usr/bin/env python3
"""Validate completed TDD evidence before checklist completion."""

from __future__ import annotations

import re
import sys
from pathlib import Path

PLACEHOLDER_RE = re.compile(r"\{\{[^}]+\}\}")
LOG_RE = re.compile(r"^\d{4}-\d{2}-\d{2}_[a-z0-9][a-z0-9-]*_(red|green|refactor|regression)\.log$")
REQ_RE = re.compile(r"^### Requirement (REQ-\d{3}):", re.MULTILINE)
SCN_RE = re.compile(r"^#### Scenario (SCN-\d{3}):", re.MULTILINE)
TRACE_RE = re.compile(r"\[(REQ-\d{3})\]\[(SCN-\d{3})\]")


def spec_pairs(spec: str) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    current_req = ""
    for line in spec.splitlines():
        req = re.match(r"^### Requirement (REQ-\d{3}):", line)
        if req:
            current_req = req.group(1)
        scn = re.match(r"^#### Scenario (SCN-\d{3}):", line)
        if scn and current_req:
            pairs.append((current_req, scn.group(1)))
    return pairs


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_evidence.py <spec-directory>", file=sys.stderr)
        return 2
    bundle = Path(sys.argv[1]).resolve()
    evidence = bundle / "tdd" / "evidence"
    summary_path = evidence / "SUMMARY.md"
    errors: list[str] = []
    spec_path = bundle / "spec.md"
    tasks_path = bundle / "tasks.md"
    checklist_path = bundle / "checklist.md"
    spec = spec_path.read_text(encoding="utf-8") if spec_path.is_file() else ""
    tasks = tasks_path.read_text(encoding="utf-8") if tasks_path.is_file() else ""
    checklist_text = checklist_path.read_text(encoding="utf-8") if checklist_path.is_file() else ""
    tests_dir = bundle / "tdd" / "tests"
    tests_text = "\n".join(path.read_text(encoding="utf-8") for path in tests_dir.rglob("test_*.py")) if tests_dir.is_dir() else ""
    if not summary_path.is_file():
        errors.append("missing tdd/evidence/SUMMARY.md")
        summary = ""
    else:
        summary = summary_path.read_text(encoding="utf-8")
        if PLACEHOLDER_RE.search(summary):
            errors.append("SUMMARY.md contains unfilled placeholders")
        if "**PASS**" not in summary:
            errors.append("SUMMARY.md verdict is not PASS")
        if re.search(r"\|\s*Pending\s*\|", summary, re.IGNORECASE):
            errors.append("SUMMARY.md still contains Pending traceability rows")
        if re.search(r"\|\s*Blocked\s*\|", summary, re.IGNORECASE):
            errors.append("SUMMARY.md contains Blocked rows, so overall verdict cannot be PASS")
        if re.search(r"\|\s*Done\s*\|", summary, re.IGNORECASE):
            errors.append("SUMMARY.md uses invalid row status Done; use Pass")
        for label in ("Red", "Green", "Affected", "Full"):
            if f"| {label} |" not in summary:
                errors.append(f"SUMMARY.md missing result row: {label}")

    phases: set[str] = set()
    if evidence.is_dir():
        for log in evidence.glob("*.log"):
            match = LOG_RE.fullmatch(log.name)
            if not match:
                errors.append(f"nonconforming log filename: {log.name}")
                continue
            phases.add(match.group(1))
            text = log.read_text(encoding="utf-8", errors="replace")
            for marker in ("[NOTE]", "[DATE]", "[SPEC]", "[PHASE]", "[CMD]", "[EXIT CODE]"):
                if marker not in text:
                    errors.append(f"{log.name} missing marker {marker}")
    for required in ("red", "green", "regression"):
        if required not in phases:
            errors.append(f"missing {required} evidence log")

    pairs = spec_pairs(spec)
    if not pairs:
        errors.append("spec.md contains no traceable Requirement/Scenario pairs")
    for req_id, scn_id in pairs:
        token = f"[{req_id}][{scn_id}]"
        for surface, text in (("tasks.md", tasks), ("checklist.md", checklist_text), ("SUMMARY.md", summary), ("test docstrings", tests_text)):
            if token not in text:
                errors.append(f"missing trace pair {token} in {surface}")

    checklist = bundle / "checklist.md"
    if checklist.is_file() and re.search(r"^- \[[xX]\]", checklist_text, re.MULTILINE) and errors:
        errors.append("checklist contains completed items while evidence is incomplete")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Valid completed TDD evidence: {evidence}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
