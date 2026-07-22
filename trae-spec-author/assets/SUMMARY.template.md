# TDD Evidence Summary — {{TITLE}}

## Metadata

- Spec: [spec.md](../../spec.md)
- Tasks: [tasks.md](../../tasks.md)
- Checklist: [checklist.md](../../checklist.md)
- Date/timezone: `{{DATE_TIMEZONE}}`
- Revision: `{{REVISION}}`
- Owner: `{{OWNER}}`

## Verdict

**IN PROGRESS** — `{{CONCLUSION}}`

## Requirement traceability

| Requirement / task | Test | Red evidence | Green evidence | Status |
|---|---|---|---|---|
| <a id="req-001-scn-001"></a>`[REQ-001][SCN-001]` | `{{TEST_NODE}}` | `[log]({{RED_LOG}})` | `[log]({{GREEN_LOG}})` | Pending |

Allowed row statuses: `Pending` (not yet evidenced), `Pass` (Green and relevant regression passed), `Blocked` (cannot complete; explain below). Do not use `Done`.

## TDD cycle results

| Phase | Exact command | Exit | Passed/failed/error/skipped | Artifact | Conclusion |
|---|---|---:|---|---|---|
| Red | `{{RED_COMMAND}}` | `{{RED_EXIT}}` | `{{RED_COUNTS}}` | `[log]({{RED_LOG}})` | `{{RED_CONCLUSION}}` |
| Green | `{{GREEN_COMMAND}}` | `{{GREEN_EXIT}}` | `{{GREEN_COUNTS}}` | `[log]({{GREEN_LOG}})` | `{{GREEN_CONCLUSION}}` |

## Regression

| Scope | Exact command | Exit | Passed/failed/error/skipped | Artifact |
|---|---|---:|---|---|
| Affected | `{{AFFECTED_COMMAND}}` | `{{AFFECTED_EXIT}}` | `{{AFFECTED_COUNTS}}` | `[log]({{AFFECTED_LOG}})` |
| Full | `{{FULL_COMMAND}}` | `{{FULL_EXIT}}` | `{{FULL_COUNTS}}` | `[log]({{FULL_LOG}})` |

## Deviations, risks, and remaining work

- `{{RISKS}}`
