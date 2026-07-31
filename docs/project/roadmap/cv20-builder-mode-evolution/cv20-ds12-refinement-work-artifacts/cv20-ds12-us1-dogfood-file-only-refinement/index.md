[< CV20.DS12](../index.md)

# CV20.DS12.US1 — Dogfood File-Only Refinement

**Status:** 🟡 Planned
**Type:** User Story

---

## Outcome

The Navigator can resume real Refinement Work from `docs/project/refinement/index.md`,
select the next Change Request, and record focus and a concrete plan using project files
alone. Friction found during the exercise becomes evidence for the next DS12 decision;
it does not automatically become runtime machinery.

## Acceptance Behavior

```text
Given a fresh Builder context with no active Refinement database cursor
When the Navigator asks to continue project Refinement Work
Then the canonical index reveals the ordered backlog and current focus
And the Navigator can select one CR and record its plan in the linked files
And status and focus change in one canonical place
And no SQLite read or write is required
```

## Scope

- Start from the canonical Workbench index.
- Select CR001 as the first ordered open Change Request unless the Navigator chooses a
  different item.
- Update root focus and statuses explicitly.
- Add a concrete plan to the selected CR document without implementing that CR.
- Record observed usability friction and decide whether the document contract needs a
  small correction.

## Out Of Scope

- Implementing the selected Change Request.
- Adding a parser, CLI, database projection, synchronization, or automatic transition.
- Migrating existing CV20.DS6 Workbench records.
- Generalizing from hypothetical failures not observed during this exercise.

## Validation

A fresh file-only reading must identify the selected RS/CR, its new status, its plan,
and the remaining backlog without consulting SQLite or conversation history.

## Done Condition

One real CR has been selected and planned from the canonical documents, the root index
remains the sole status authority, observed friction is recorded, and the Navigator
confirms whether the workflow is usable enough to continue dogfooding.
