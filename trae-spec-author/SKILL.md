---
name: trae-spec-author
description: Create, update, and validate complete Trae-compatible spec bundles directly under `.trae/specs` without invoking `/spec`, including `spec.md`, `tasks.md`, `checklist.md`, feature-local TDD tests, Red-Green-Refactor logs, JUnit results, and a human-readable evidence summary. Use when converting requirements or bug reports into Trae specs, performing evidence-backed TDD, repairing unrecognized spec bundles, or avoiding the `/spec` and `/skills` compatibility conflict.
---

# Trae Spec Author

Generate the artifacts that `/spec` would normally establish, but never invoke `/spec` while this Skill is active.

## Compatibility rule

Treat `/spec` and this Skill as mutually exclusive entry points. In this workflow:

- do not call, type, simulate, or require `/spec`;
- write the three canonical Markdown files and TDD evidence layout directly;
- keep them under `.trae/specs/<kebab-case-slug>/`;
- do not add custom manifests that Trae does not require;
- preserve existing spec content unless the user asks to replace it.

## Authoring workflow

1. Read repository instructions, relevant source/tests/docs, and existing `.trae/specs` bundles.
2. Determine a unique lowercase kebab-case slug. Prefer verbs such as `add-`, `fix-`, `refactor-`, `enhance-`, or `write-`.
3. If the target bundle is new, run the generator. It must create the spec files and TDD/evidence directories together:

   ```powershell
   python <skill-dir>/scripts/create_spec_bundle.py --project-root <repo> --slug <slug> --title "<title>"
   ```

4. Replace every placeholder using evidence from the repository and user request. Do not invent paths, APIs, baselines, or compatibility guarantees.
5. Write `spec.md` first and assign stable IDs: `REQ-001` for each requirement and `SCN-001` for each scenario. Never renumber existing IDs. Derive `tasks.md`, tests, `checklist.md`, and `SUMMARY.md` using those exact IDs.
6. Read [references/trae-spec-format.md](references/trae-spec-format.md) and [references/evidence-standard.md](references/evidence-standard.md). Enforce both contracts.
7. Run the bundle validator before implementation. Fix every error:

   ```powershell
   python <skill-dir>/scripts/validate_spec_bundle.py <repo>/.trae/specs/<slug>
   ```

8. Execute every behavior change using Red-Green-Refactor. Put new spec-specific tests only in `tdd/tests/`; keep established project tests in their existing directory for regression.
9. Save compact raw logs in `tdd/evidence/`, update `SUMMARY.md` after every phase, and optionally emit JUnit XML.
10. Run the evidence validator before checking off completion items:

   ```powershell
   python <skill-dir>/scripts/validate_evidence.py <repo>/.trae/specs/<slug>
   ```

11. Re-open all generated files and verify UTF-8 rendering, links, test counts, exit codes, checkbox state, and bidirectional ID traceability.

## Content rules

- `spec.md`: explain motivation, scoped changes, impact, and testable requirements. Use `SHALL` for normative statements and Scenario blocks with `WHEN`, `THEN`, and optional `AND`.
- `tasks.md`: use `- [ ] Task N:` items, concrete files/actions/validation, implementation order, and `# Task Dependencies`.
- `checklist.md`: use only observable acceptance statements, grouped when useful; initialize every item as `- [ ]`.
- Map every requirement to at least one task and checklist item. Include negative/error/boundary scenarios when relevant.
- Put `[REQ-NNN][SCN-NNN]` in each TDD task, test docstring, checklist item, and summary traceability row. Treat missing, duplicate, or unknown IDs as errors.
- In `spec.md`, include `- **TEST**` with the planned pytest node ID and `- **EVIDENCE**` with the summary anchor for every scenario.
- Separate ADDED, MODIFIED, and REMOVED requirements. Omit MODIFIED/REMOVED sections when they do not apply; never put speculative scope there.
- Always describe Red test, minimal Green implementation, Refactor, affected/full regression, and evidence capture for code behavior changes.
- Always create `tdd/tests/` and `tdd/evidence/SUMMARY.md` with a new bundle. Do not scatter feature tests or evidence at repository root.
- Name tests `test_<module>.py`, functions `test_<behavior>_<condition>`, and add concise Chinese docstrings explaining assertion intent.
- Start each Chinese test docstring with its trace IDs, following the form `[REQ-001][SCN-001] <Chinese assertion intent>`.
- Use `pytest -q --tb=short` for Red and `pytest -q --tb=no` for Green/refactor/regression.
- Never mark a behavior checklist item complete without linked Red, Green, and relevant regression evidence.

## Required bundle

```text
.trae/specs/<slug>/
|-- spec.md
|-- tasks.md
|-- checklist.md
`-- tdd/
    |-- tests/
    |   `-- test_<module>.py
    `-- evidence/
        |-- SUMMARY.md
        |-- YYYY-MM-DD_<scope>_red.log
        |-- YYYY-MM-DD_<scope>_green.log
        |-- YYYY-MM-DD_<scope>_refactor.log
        |-- YYYY-MM-DD_<scope>_regression.log
        `-- YYYY-MM-DD_<scope>_results.xml
```

## Existing bundles

Before modifying an existing bundle, inspect its checkbox state. Do not reset completed items or rewrite historical claims. Add or amend only the requested scope, and keep headings/terminology consistent with that bundle.

## Completion report

Return the bundle path, generated files, requirement/task/checklist counts, focused and regression counts, both validator results, evidence summary path, assumptions, and unresolved decisions. State explicitly that `/spec` was not invoked.
