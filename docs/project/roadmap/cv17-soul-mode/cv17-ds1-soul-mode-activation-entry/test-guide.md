[< Story](index.md)

# Test Guide — CV17.DS1 Soul Mode Activation And Entry Surface

## Automated Tests

Run:

```bash
uv run pytest tests/unit/memory/cli/test_soul.py tests/unit/memory/surfaces/test_mode_transition.py tests/unit/memory/cli/test_welcome.py -q
```

Expected:

- all tests pass;
- Soul Mode activation stores `Soul Mode` in operating mode state;
- Soul Mode status label renders as `☾ Soul Mode`;
- Soul Mode entry surface includes `IN ORDER TO`, `remember who you are`, `START BY ANSWERING`, and `how is your day going today?`;
- Pi status-line tests still pass.

## CLI Smoke

Run:

```bash
uv run python -m memory soul load soul-mode
```

Expected output includes:

```text
☾  SOUL MODE ACTIVE
✦  IN ORDER TO
remember who you are
▹  START BY ANSWERING
how is your day going today?
```

Then run:

```bash
uv run python -m memory welcome --status-line
```

Expected output includes the active Soul Mode label with the journey display name when available, for example:

```text
Mirror Soul Mode on ☾ Soul Mode
```

## Pi Manual Validation

In Pi, ask in natural language:

```text
enter Soul Mode for soul-mode
```

Expected:

- the assistant calls the Soul Mode activation resource;
- the visible response starts with the Soul Mode entry surface;
- the assistant does not open a rite;
- the assistant does not create a fruit;
- the assistant does not write to the journal;
- the next natural user answer can be treated as the beginning of Listening To The Living Field in DS2.

## Regression Checks

- Builder Mode still renders `■ Builder Mode`.
- Explorer Mode still renders `△ Explorer Mode`.
- Mirror Mode available lenses include Soul Mode.
- Status line no longer uses the `Active Journey` prefix.
