# Evidence standard

## Purpose

Make `SUMMARY.md` sufficient for normal review while retaining raw artifacts for diagnosis and audit.

## Naming

Use `YYYY-MM-DD_<scope>_<phase>.log`, where `<scope>` is a short kebab-case task or behavior and phase is `red`, `green`, `refactor`, or `regression`. Never use ambiguous names such as `tdd_green_phase.log`.

## Required `SUMMARY.md` sections

1. Metadata: feature/spec, date and timezone, author/agent, repository revision if available.
2. Verdict: `IN PROGRESS`, `PASS`, or `BLOCKED`, plus one sentence.
3. Requirement traceability table: requirement/task, test node ID or file, Red artifact, Green artifact, status.
4. Cycle results: phase, exact command, exit code, passed/failed/error/skipped counts, duration if available, artifact link, conclusion.
5. Regression: affected suite and full suite results.
6. Deviations and risks: retries, unexpected passes, skipped tests, environmental limitations, remaining work.

Use relative Markdown links from `SUMMARY.md` to logs and XML.

## Log preamble

Prefix captured logs with:

```text
[NOTE] <why this command was run>
[DATE] <ISO-8601 timestamp with timezone>
[SPEC] <relative spec directory>
[PHASE] red|green|refactor|regression
[CMD] <exact command>
[EXIT CODE] <integer>
```

Append the tool output after the preamble. Preserve encoding as UTF-8.

## Noise control

- Red: use `-q --tb=short` and retain the relevant failed assertion.
- Green/refactor/regression: use `-q --tb=no`; avoid one `PASSED` line per test.
- Generate JUnit XML when automation or exact machine-readable counts add value.
- Do not dump full HTTP responses, cache files, binary output, or repetitive traces.
- Redact secrets before writing. If safe redaction cannot be guaranteed, do not persist the raw output; record the omission and reason.

## Integrity rules

- Record the subprocess exit code directly.
- Do not edit a failing log into a passing one or merge output from different commands under one preamble.
- Do not manufacture a Red result after implementation. If code predates the cycle, record a characterization test and explicitly label the deviation.
- Keep failed harness/setup attempts only when they explain a meaningful deviation; otherwise summarize them without presenting them as behavioral Red evidence.
- Update `checklist.md` only after its evidence links and result are present.
