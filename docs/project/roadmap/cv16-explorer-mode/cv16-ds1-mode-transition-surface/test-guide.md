[< Story](index.md)

# Test Guide — CV16.DS1 Mode Transition Surface

## Automated Verification

```bash
uv run pytest \
  tests/unit/memory/surfaces/test_mode_transition.py \
  tests/unit/memory/skills/test_mirror.py \
  tests/unit/memory/cli/test_build.py \
  tests/unit/memory/cli/test_explore.py
```

Expected: all tests pass.

Lint:

```bash
uv run ruff check \
  src/memory/surfaces/mode_transition.py \
  src/memory/skills/mirror.py \
  src/memory/cli/build.py \
  src/memory/cli/explore.py \
  tests/unit/memory/surfaces/test_mode_transition.py
```

Expected: all checks pass.

## Manual Smoke

```bash
uv run python -m memory mirror load --journey explorer-mode --query "test mirror mode surface"
uv run python -m memory build load explorer-mode >/tmp/mirror-build-surface.txt
uv run python -m memory explore load explorer-mode >/tmp/mirror-explore-surface.txt
```

Expected:

- Mirror Mode output includes `◌  MIRROR MODE ACTIVE`, identity, journey when present, persona routing, and available lenses.
- Builder Mode output includes `■  BUILDER MODE ACTIVE`, active journey, project path when present, and compact briefing/path information.
- Explorer Mode output includes `△  EXPLORER MODE ACTIVE` with minimal uncertainty-preservation copy.
- Persona activation banner uses `✦ Persona:` rather than the Mirror identity symbol.

## Pass Condition

Every primary mode transition renders a compact conversational surface, and the
persona icon no longer reuses the Mirror identity symbol.
