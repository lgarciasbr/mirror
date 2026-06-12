[< Story](index.md)

# Test Guide — CV20.DS4.US2 Plan Checkpoint Gate

## Automated Validation

```bash
uv run pytest tests/unit/memory/builder/test_lifecycle.py tests/unit/memory/cli/test_build.py tests/unit/memory/builder/test_delivery_cursor.py tests/unit/memory/builder/test_method_adoption.py
uv run ruff check src/memory tests/unit/memory/builder tests/unit/memory/cli/test_build.py
uv run ruff format --check src/memory tests/unit/memory/builder tests/unit/memory/cli/test_build.py
uv run mypy src/memory/builder src/memory/cli/build.py
```

## Navigator Validation Through Pi/Mirror

With `sandbox-pet-store` reset, activate Builder Mode, pull `CV2.DS1`, prepare it, then run:

```text
planeje o item puxado
```

Pass condition:

- Output includes `PLAN CHECKPOINT`.
- Ribbon shows `✓ Pull | ✓ Prepare | ◉ Plan`.
- Active item is `CV2.DS1`.
- Pending confirmation is `navigator_approval`.
- The surface says implementation remains blocked until approval.

Fail condition:

- Builder starts implementation.
- Builder mutates project files.
- Plan renders without Prepare having happened first.
- Runtime cursor does not record the checkpoint/pending confirmation.
