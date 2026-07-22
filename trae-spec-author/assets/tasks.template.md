# Tasks

- [ ] Task 1 [REQ-001][SCN-001]: {{RED_TEST_OUTCOME}}
  - **Files**: `.trae/specs/{{SLUG}}/tdd/tests/{{TEST_FILE}}`
  - **Validation**: `{{RED_COMMAND}}`
  - **Evidence**: `tdd/evidence/YYYY-MM-DD_{{SCOPE}}_red.log`
  - [ ] Evidence closeout: add the Red command, exit code, counts, conclusion, and link to `tdd/evidence/SUMMARY.md`; keep status `Pending`

- [ ] Task 2 [REQ-001][SCN-001]: {{GREEN_IMPLEMENTATION_OUTCOME}}
  - **Files**: `{{SOURCE_PATH}}`
  - **Validation**: `{{GREEN_COMMAND}}`
  - **Evidence**: `tdd/evidence/YYYY-MM-DD_{{SCOPE}}_green.log`
  - [ ] Evidence closeout: add Green results and change `[REQ-001][SCN-001]` from `Pending` to `Pass` only after relevant regression passes; otherwise set `Blocked`

- [ ] Task 3 [REQ-001][SCN-001]: Refactor and run affected plus full regression suites
  - **Validation**: `{{REGRESSION_COMMAND}}`
  - **Evidence**: `tdd/evidence/SUMMARY.md` and compact regression log
  - [ ] Summary closeout: reconcile task/checklist states, remove no longer valid `Pending` rows, and keep overall Verdict `IN PROGRESS` until all required rows are `Pass`

- [ ] Task 4: Final evidence gate
  - [ ] Verify every traceability status is exactly `Pass` or `Blocked`; no `Pending` or `Done` remains
  - [ ] Set overall Verdict to `PASS` only when all required rows are `Pass` and full regression exit code is 0
  - **Validation**: `python <skill-dir>/scripts/validate_evidence.py .trae/specs/{{SLUG}}`

# Task Dependencies

- Task 2 depends on Task 1; Task 3 depends on Task 2; Task 4 depends on all implementation and regression tasks.
