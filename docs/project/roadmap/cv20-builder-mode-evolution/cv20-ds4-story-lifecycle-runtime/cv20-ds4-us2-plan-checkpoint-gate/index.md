[< CV20.DS4](../index.md)

# CV20.DS4.US2 — Plan Checkpoint Gate

**Status:** 🟡 Planned
**Type:** User Story

---

## Outcome

Navigator can ask Builder to plan the pulled Ariad item and receive a Plan Checkpoint surface that records a pending approval gate before implementation.

---

## Acceptance Behavior

```text
Given Builder Mode is active for an Ariad-adopted journey
And an item has been pulled and prepared
When the Navigator asks Builder to plan the active item
Then Mirror renders the Ariad Plan Checkpoint surface
And runtime cursor records active checkpoint after_plan
And runtime cursor records pending confirmation navigator_approval
And runtime cursor records last delivery event plan
And implementation remains blocked until approval
```

```text
Given a Plan checkpoint is pending approval
When the Navigator asks Builder to implement
Then Mirror refuses implementation
And explains that Navigator approval is required first
And does not mutate project files
```

---

## Scope

- Add contained Builder lifecycle operation for `plan`.
- Require Ariad adoption and runtime delivery cursor.
- Require active item and previous Prepare event.
- Render Ariad `Plan Checkpoint` visual grammar with lifecycle ribbon.
- Persist checkpoint gate in runtime cursor.
- Add a contained implementation guard/check command or helper that refuses while approval is pending.
- Update Pi Builder skill routing for natural-language Plan requests.
- Add focused tests for plan success, missing prepare, pending approval, and implementation block.

---

## Out Of Scope

- No implementation work.
- No approval command yet unless needed for guard validation.
- No code/file mutation for the pulled item.
- No automated validation execution.
- No Review, Coherence, or Done.
- No full roadmap mutation.

---

## Validation

Navigator validation through Pi/Mirror natural language:

```text
planeje o item puxado
```

Expected observation: Mirror renders `PLAN CHECKPOINT` with lifecycle ribbon at Plan, shows the active item, plan contract fields, pending approval, and says implementation remains blocked until Navigator approval.
