# Trae spec format

This contract is distilled from the reference bundles under `E:\Code\001-漏洞排查\.trae\specs`.

## Bundle identity

```text
.trae/specs/<lowercase-kebab-slug>/
|-- spec.md
|-- tasks.md
`-- checklist.md
```

Use UTF-8 Markdown and exact lowercase filenames. The directory name is the bundle identifier.

## `spec.md`

Use this order:

1. `# <clear title> Spec`
2. `## Why`
3. `## What Changes`
4. `## Impact`
5. `## ADDED Requirements`
6. Optional `## MODIFIED Requirements`
7. Optional `## REMOVED Requirements`

For each requirement:

```markdown
### Requirement REQ-001: <name>

系统 SHALL <one testable normative behavior>。

#### Scenario SCN-001: <observable case>

- **WHEN** <precondition or event>
- **THEN** <observable result>
- **AND** <additional result>
- **TEST** `tdd/tests/test_<module>.py::test_<behavior>_<condition>`
- **EVIDENCE** `tdd/evidence/SUMMARY.md#req-001-scn-001`
```

Use one behavior per requirement where practical. Avoid implementation-only requirements unless architecture itself is in scope. Make Impact identify affected code/specs/output and compatibility or breaking effects.

## `tasks.md`

Start with `# Tasks`. Use sequential task IDs and unchecked boxes:

```markdown
- [ ] Task 1: <outcome>
  - [ ] SubTask 1.1: <action>
  - **Files**: `<real path>`
  - **Validation**: `<command or observable check>`

# Task Dependencies

- Task 2 depends on Task 1 because <reason>.
```

Tasks must be implementable, ordered, and traceable to requirements. For behavior changes, encode Red before Green and finish with focused plus full regression evidence.

## `checklist.md`

Start with `# Checklist`. Group by requirement or priority if useful. Each item must be binary and observable. Do not pre-check new work.

Good: `- [ ] 无效 CVE ID 返回 exit code 1 且不写输出文件`

Weak: `- [ ] 代码质量良好`

Include compatibility, regression, documentation, and evidence checks when applicable.

## Traceability

Verify before completion:

- each ADDED/MODIFIED requirement has at least one Scenario;
- every Scenario has a globally unique `SCN-NNN` ID, planned pytest node ID, and evidence anchor;
- every Requirement has a unique `REQ-NNN` ID;
- every Requirement and Scenario ID appears in `tasks.md`, `checklist.md`, and `SUMMARY.md`;
- implemented test docstrings contain the corresponding `[REQ-NNN][SCN-NNN]` pair;
- every requirement has at least one checklist assertion;
- task paths match the inspected repository;
- no completed checkbox is claimed without execution evidence;
- the three files describe the same scope and terminology.

Never reuse an ID for different behavior or renumber IDs after implementation begins. When adding scope, continue from the highest existing number.
