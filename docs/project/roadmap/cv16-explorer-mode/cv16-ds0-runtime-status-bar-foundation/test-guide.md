[< Story](index.md)

# Test Guide — CV16.DS0 Runtime Status Bar Foundation

## Automated Verification

```bash
uv run pytest \
  tests/unit/memory/services/test_operating_mode.py \
  tests/unit/memory/cli/test_mode.py \
  tests/unit/memory/cli/test_welcome.py \
  tests/unit/memory/cli/test_build.py
```

Expected: all tests pass.

Pi extension type check:

```bash
cd .pi
npx tsc --noEmit
```

Expected: no TypeScript errors. If dependencies are missing in a fresh checkout,
run `npm install` in `.pi/` first without committing lockfile drift unless the
package graph intentionally changed.

## CLI Smoke

Use the active development Mirror home only if the current session can safely
change its active mode state. Otherwise use a disposable Mirror home.

```bash
uv run python -m memory welcome --status-line
uv run python -m memory mode status
uv run python -m memory build load explorer-mode >/tmp/mirror-build-load.txt
uv run python -m memory welcome --status-line
uv run python -m memory mode deactivate
uv run python -m memory welcome --status-line
```

Expected:

- before activation, status line is compact or reflects any already active mode;
- after `build load explorer-mode`, status line includes:

```text
Active Journey explorer-mode on ■ Builder Mode
```

- after `mode deactivate`, status line no longer includes stale `Builder Mode`
  text and returns to `Active Journey explorer-mode on ◌ Mirror Mode` when
  journey context remains active.

## Pi Manual Validation

1. Start Pi in the Mirror development repository.
2. Activate Builder Mode for a journey.
3. Let the assistant turn finish.
4. Confirm the footer status includes Mirror identity, active journey, Builder Mode, and health marker.
5. Ask Mirror to leave the active mode, or run the contained operation:

```bash
uv run python -m memory mode deactivate
```

6. Let the assistant turn finish.
7. Confirm the footer no longer includes stale Builder Mode text and returns to Mirror Mode when journey context remains active.

## Pass Condition

The active operating mode can be explicitly activated and deactivated, Builder
Mode activation sets mode state, `welcome --status-line` renders mode context
when present, and Pi refreshes the status line without replacing the built-in
footer.
