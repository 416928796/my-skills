---
name: trae-spec-tdd
description: Drive feature development through Trae's `/spec` workflow and strict Red-Green-Refactor TDD while co-locating executable tests, raw logs, structured results, and concise human-readable evidence beside each Trae spec's `spec.md`, `tasks.md`, and `checklist.md`. Use when implementing or changing code from a Trae spec, turning requirements into tests, recording auditable TDD evidence, resuming a spec task, or organizing `.trae` test artifacts for review.
---

# Trae Spec TDD

Use Trae `/spec` as the source-of-truth workflow. Do not silently replace it with an ad-hoc plan.

## Workflow

1. Inspect repository instructions and `.trae/specs/`. Identify exactly one spec directory.
2. Invoke Trae `/spec` for the requested change. If `/spec` is unavailable in the current client, stop before implementation and ask the user to run or expose it; do not fabricate its output.
3. Read that directory's `spec.md`, `tasks.md`, and `checklist.md`. Resolve requirement/test traceability before editing production code.
4. Run `scripts/init_tdd_layout.py <spec-dir>` to create the feature-local TDD layout and summary from the bundled template.
5. Record the baseline environment and relevant pre-existing test result in `tdd/evidence/SUMMARY.md`.
6. Execute each task as a small Red-Green-Refactor cycle:
   - Red: add the smallest behavioral test first; run it with a short traceback; confirm failure for the intended reason.
   - Green: make the smallest production change; rerun the focused test quietly.
   - Refactor: improve design without changing behavior; rerun focused and affected regression tests.
7. Save every evidence-producing command, exit code, counts, and conclusion. Update checklist items only after their linked evidence exists.
8. Run the full project regression suite. Finish only when the spec, tasks, checklist, tests, evidence summary, and implementation agree.

## Required layout

Keep all tests introduced specifically for a spec inside its matching directory:

```text
.trae/specs/<spec-slug>/
|-- spec.md
|-- tasks.md
|-- checklist.md
`-- tdd/
    |-- tests/
    |   |-- conftest.py              # only when required
    |   `-- test_<module>.py
    `-- evidence/
        |-- SUMMARY.md               # primary human review surface
        |-- YYYY-MM-DD_<scope>_red.log
        |-- YYYY-MM-DD_<scope>_green.log
        |-- YYYY-MM-DD_<scope>_refactor.log
        |-- YYYY-MM-DD_<scope>_regression.log
        `-- YYYY-MM-DD_<scope>_results.xml  # optional JUnit
```

Never create a top-level `test/` directory. Never duplicate a spec-local test in project `tests/`. Existing project tests remain where they are and are included in regression runs.

## Test rules

- Name files `test_<module>.py` and tests `test_<behavior>_<condition>`.
- Add a concise Chinese docstring describing the assertion intent.
- Test public behavior and requirement boundaries, including positive, negative, missing-value, conflict, and regression cases where applicable.
- Keep tests deterministic, offline by default, and isolated with mocks/fakes for network, clock, filesystem, and external services.
- Make spec-local imports work through test configuration, not copied application code.
- Link each test or test group to a requirement/task in `SUMMARY.md`.

Read [references/evidence-standard.md](references/evidence-standard.md) before producing evidence.

## Commands

Adapt the interpreter and paths to the repository, while preserving output intent.

```powershell
# Red: retain the useful assertion and short stack
python -m pytest .trae/specs/<spec-slug>/tdd/tests/test_<module>.py -q --tb=short

# Green/refactor: compact output
python -m pytest .trae/specs/<spec-slug>/tdd/tests -q --tb=no

# Optional structured result
python -m pytest .trae/specs/<spec-slug>/tdd/tests -q --tb=no --junitxml=.trae/specs/<spec-slug>/tdd/evidence/YYYY-MM-DD_<scope>_results.xml

# Regression: include both established and feature-local suites
python -m pytest tests .trae/specs/<spec-slug>/tdd/tests -q --tb=no
```

Capture output without losing the actual process exit code. Do not claim success from log text alone.

## Evidence gate

Treat `SUMMARY.md` as the review entry point and raw logs/XML as attachments. Before marking a checklist item complete, require:

- a test mapped to its requirement;
- a genuine Red failure caused by missing/incorrect behavior, not syntax, import, fixture, or environment failure;
- a Green pass after implementation;
- affected regression results;
- exact command, timestamp with timezone, exit code, pass/fail/error/skip counts, and a one-sentence conclusion;
- no secrets, tokens, authorization headers, personal data, or oversized payload dumps.

If Red unexpectedly passes, investigate whether behavior already exists or the test is weak. If Red fails for the wrong reason, fix the test harness and rerun; preserve only diagnostically useful attempts and explain them in the summary.

## Completion report

Report the spec path, requirements completed, files changed, focused and regression counts, unresolved risks, and a link/path to `tdd/evidence/SUMMARY.md`. Never describe a checklist as complete when evidence is missing or tests are skipped without justification.
