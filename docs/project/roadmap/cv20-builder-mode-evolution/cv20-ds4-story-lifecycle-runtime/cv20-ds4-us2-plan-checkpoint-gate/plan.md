[< Story](index.md)

# Plan — CV20.DS4.US2 Plan Checkpoint Gate

## Pull

Pulled item: `CV20.DS4.US2 — Plan Checkpoint Gate`.

Why this level now: DS4.US1 implemented Pull and Prepare. The next Ariad lifecycle stage is Plan, and it is the first hard checkpoint that must block implementation until Navigator approval.

## Prepare

Context read/used:

- `/Users/alissonvale/Code/mirror-dev/docs/project/roadmap/cv20-builder-mode-evolution/cv20-ds4-story-lifecycle-runtime/index.md`
- `/Users/alissonvale/Code/mirror-dev/docs/project/roadmap/cv20-builder-mode-evolution/cv20-ds4-story-lifecycle-runtime/cv20-ds4-us1-pull-and-prepare/index.md`
- `/Users/alissonvale/Code/mirror-dev/src/memory/builder/lifecycle.py`
- `/Users/alissonvale/Code/mirror-dev/src/memory/builder/lifecycle_ribbon.py`
- `/Users/alissonvale/Code/mirror-dev/src/memory/builder/delivery_cursor.py`
- `/Users/alissonvale/Code/mirror-dev/src/memory/cli/build.py`
- `/Users/alissonvale/Code/ariad/docs/delivery/visual-grammar.md`

Story shape assessment: User Story. The observable behavior is a Navigator-facing Plan Checkpoint surface and a runtime gate that blocks implementation.

Risks:

- Plan may become implementation. It must stop at approval.
- Plan may be generated without Prepare. It should require `last_delivery_event=prepare`.
- Plan checkpoint state may be only prose. It must persist in runtime cursor.
- Approval/implementation flow can grow too large. This story should create the gate and block implementation, not execute implementation.

Applicable rules:

- Use TDD.
- Preserve Ariad visual grammar.
- Require explicit Navigator approval before implementation.
- Keep runtime state in SQLite cursor.
- Do not mutate project files for the pulled item.

## Dependency

This story depends on `CV20.DS4.TS2 — Lifecycle Contract Definitions`. Plan should render method-declared contracts rather than hardcoding implementation rules.

## Scope

Add lifecycle operation in:

`/Users/alissonvale/Code/mirror-dev/src/memory/builder/lifecycle.py`

Likely additions:

- `BuilderPlanReport`
- `plan_lifecycle_item(store, journey, method, objective=None) -> BuilderPlanReport`
- `render_plan_checkpoint(report) -> str`
- `assert_implementation_allowed(store, journey) -> None` or equivalent guard helper

Plan behavior:

- reads Ariad `plan_contract`, `implement_contract`, and validation-contract summary from the method definition;
- requires delivery cursor;
- requires `active_item`;
- requires `last_delivery_event == "prepare"`;
- updates cursor:
  - `active_checkpoint="after_plan"`;
  - `pending_confirmation="navigator_approval"`;
  - `last_delivery_event="plan"`;
- renders Plan Checkpoint with:
  - lifecycle ribbon at Plan;
  - active item;
  - objective;
  - scope stance;
  - non-goals;
  - acceptance/validation placeholder;
  - method-declared implementation contract rules;
  - E2E validation decision prompt/placeholder;
  - implementation blocked;
  - Navigator decision prompt.

Add CLI commands:

```bash
uv run python -m memory build plan-item --method ariad
```

and guard/smoke command:

```bash
uv run python -m memory build check-implementation --method ariad
```

Both support `--journey <slug>` or active Builder journey resolution.

Update skill:

`/Users/alissonvale/Code/mirror-dev/.pi/skills/mm-build/SKILL.md`

Route natural-language requests like `planeje o item puxado` to `plan-item` only for Ariad-adopted journeys.

## Non-Goals

- No project file mutation.
- No creation of story folder or `plan.md` yet.
- No approval command.
- No implementation execution.
- No validation/review/coherence/done.
- No full roadmap status transition.

## Implementation Approach

TDD first:

1. Extend `/Users/alissonvale/Code/mirror-dev/tests/unit/memory/builder/test_lifecycle.py` for Plan behavior.
2. Extend `/Users/alissonvale/Code/mirror-dev/tests/unit/memory/cli/test_build.py` for CLI Plan and implementation guard.
3. Implement lifecycle plan operation and renderer.
4. Wire CLI commands.
5. Update Pi skill.
6. Validate automated checks.
7. Stop for Navigator validation through Pi/Mirror.

## Test Strategy

Automated:

```bash
uv run pytest tests/unit/memory/builder/test_lifecycle.py tests/unit/memory/cli/test_build.py tests/unit/memory/builder/test_delivery_cursor.py tests/unit/memory/builder/test_method_adoption.py
uv run ruff check src/memory tests/unit/memory/builder tests/unit/memory/cli/test_build.py
uv run ruff format --check src/memory tests/unit/memory/builder tests/unit/memory/cli/test_build.py
uv run mypy src/memory/builder src/memory/cli/build.py
```

Navigator validation:

```text
planeje o item puxado
```

Expected:

- Plan Checkpoint surface appears.
- Ribbon shows Pull and Prepare complete, Plan current.
- Cursor records `active_checkpoint=after_plan`.
- Cursor records `pending_confirmation=navigator_approval`.
- Implementation is explicitly blocked.

## Checkpoint

Implementation must not start until the Navigator approves this plan.
