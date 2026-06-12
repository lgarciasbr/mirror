[< CV20.DS4](../index.md)

# CV20.DS4.US4 — Validation Checkpoint

**Status:** 🟡 Planned
**Type:** User Story

---

## Outcome

After implementation, Builder presents a deterministic Validation Checkpoint that combines automated evidence, E2E decision/evidence, and a concrete Navigator validation route.

---

## Context

Plan defines validation obligations. Ariad requires User Stories to remain Navigator-visible; automated tests support but do not replace validation for user-visible behavior.

---

## Acceptance Behavior

```text
Given an active item has an approved Plan and implementation changes exist
When Builder reaches Validation
Then Builder renders a Validation Checkpoint surface
And shows required automated checks and results
And shows whether E2E was required, run, skipped, or explicitly waived
And provides a Navigator-visible validation route with expected observation, pass condition, and fail condition
```

```text
Given required validation evidence is missing
When Builder attempts to move past Validation
Then Builder blocks progression
And names the missing evidence or required Navigator decision
```

---

## Scope

- Add Validation lifecycle operation and deterministic surface.
- Read validation obligations from Plan package/method contracts.
- Record validation evidence in runtime state and/or story package.
- Support E2E required/waived evidence language.
- Stop for Navigator validation acceptance.

---

## Out Of Scope

- Debt Review.
- Coherence.
- Done/history recording.
- Accelerated/autonomous cadence bypass behavior.

---

## Validation

Focused tests plus Pi/Mirror natural-language validation against sandbox-pet-store.
