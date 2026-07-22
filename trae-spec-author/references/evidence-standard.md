# TDD evidence standard

Make `SUMMARY.md` sufficient for normal human review; retain compact logs and optional JUnit XML for diagnosis and automation.

## Cycle integrity

- Red must fail because target behavior is missing or wrong, not because of import, syntax, fixture, or environment errors.
- Green must pass after the smallest production change.
- Refactor must preserve behavior and rerun focused tests.
- Run affected and full project regression suites before completion.
- If Red unexpectedly passes, strengthen the test or record that behavior already existed. Never fabricate historical Red evidence.

## Evidence naming and commands

Use `YYYY-MM-DD_<scope>_<phase>.log`, where phase is `red`, `green`, `refactor`, or `regression`.

- Red: `pytest -q --tb=short`
- Green/refactor/regression: `pytest -q --tb=no`
- Optional structured output: `--junitxml=tdd/evidence/YYYY-MM-DD_<scope>_results.xml`

Prefix every log with:

```text
[NOTE] <purpose>
[DATE] <ISO-8601 timestamp with timezone>
[SPEC] <relative spec directory>
[PHASE] red|green|refactor|regression
[CMD] <exact command>
[EXIT CODE] <integer>
```

Record subprocess exit codes directly. Do not combine different commands under one preamble or edit failing logs into passing logs.

## Summary requirements

Keep these sections current:

1. Metadata and revision.
2. Verdict: `IN PROGRESS`, `PASS`, or `BLOCKED`.
3. Requirement/task/test/Red/Green traceability using exact `REQ-NNN` and `SCN-NNN` IDs.
4. Exact commands, exit codes, pass/fail/error/skip counts, artifacts, conclusions.
5. Affected and full regression results.
6. Deviations, skipped tests, environment limits, risks, and remaining work.

Use relative Markdown links. Redact tokens, credentials, authorization headers, personal data, and sensitive payloads. Do not dump repetitive PASSED lines, full HTTP bodies, binary output, or caches.

## Checklist gate

Keep a checklist item unchecked until the same `[REQ-NNN][SCN-NNN]` pair exists in the spec, task, test docstring, summary row, genuine Red evidence, Green evidence, and relevant regression evidence. The summary is the primary review surface; raw logs are attachments.
