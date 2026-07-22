# Checklist

## Functional acceptance

- [ ] [REQ-001][SCN-001] {{OBSERVABLE_ACCEPTANCE}}

## TDD and regression

- [ ] [REQ-001][SCN-001] Red test fails for the intended missing behavior
- [ ] [REQ-001][SCN-001] Focused Green test passes
- [ ] [REQ-001][SCN-001] Affected and full regression suites pass
- [ ] [REQ-001][SCN-001] Human-readable evidence summary records commands, exit codes, counts, and conclusions
- [ ] [REQ-001][SCN-001] Requirement maps to task, test docstring, Red evidence, and Green evidence
- [ ] Traceability row status is `Pass` after Green plus regression, or `Blocked` with a documented reason; no `Pending`/`Done` remains at final validation
- [ ] Overall Verdict is `PASS` only when all required traceability rows are `Pass`
- [ ] Raw logs use date, scope, and phase filenames under this spec directory
