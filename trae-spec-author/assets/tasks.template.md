# Tasks

- [ ] Task 1 [REQ-001][SCN-001]: {{RED_TEST_OUTCOME}}
  - **Files**: `.trae/specs/{{SLUG}}/tdd/tests/{{TEST_FILE}}`
  - **Validation**: `{{RED_COMMAND}}`
  - **Evidence**: `tdd/evidence/YYYY-MM-DD_{{SCOPE}}_red.log`

- [ ] Task 2 [REQ-001][SCN-001]: {{GREEN_IMPLEMENTATION_OUTCOME}}
  - **Files**: `{{SOURCE_PATH}}`
  - **Validation**: `{{GREEN_COMMAND}}`
  - **Evidence**: `tdd/evidence/YYYY-MM-DD_{{SCOPE}}_green.log`

- [ ] Task 3 [REQ-001][SCN-001]: Refactor and run affected plus full regression suites
  - **Validation**: `{{REGRESSION_COMMAND}}`
  - **Evidence**: `tdd/evidence/SUMMARY.md` and compact regression log

# Task Dependencies

- Task 2 depends on Task 1; Task 3 depends on Task 2.
