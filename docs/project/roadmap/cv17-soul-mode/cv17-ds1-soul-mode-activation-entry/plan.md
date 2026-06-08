[< Story](index.md)

# Plan — CV17.DS1 Soul Mode Activation And Entry Surface

## Boundary

This story adds the first visible Soul Mode behavior: explicit activation and the entry surface. It should not attempt Possible Listenings, active rites, fruit state, or journal persistence. The point is to create a safe threshold that can be validated in Pi through natural language.

## Design

Add Soul Mode as an operating lens in the existing runtime mode lifecycle:

```text
Soul Mode → ☾ Soul Mode
```

Add a contained CLI resource:

```bash
uv run python -m memory soul load [slug]
```

The command activates Soul Mode, optionally binds a journey as sticky context, and renders the entry surface:

```text
Soul Mode
╭────────────────────────────────────────╮
│   ✦  IN ORDER TO                            │
│                                        │
│   remember who you are              │
│                                        │
│   ▹  START BY ANSWERING                │
│                                        │
│   how is your day going today?               │
╰────────────────────────────────────────╯
```

The Pi skill `.pi/skills/mm-soul/SKILL.md` is a thin behavioral contract. It tells the assistant to call the CLI and render the returned surface, but not to infer a rite or write to the journal.

## Implementation Notes

- Extend `MODE_ICONS` with `Soul Mode`.
- Add `render_soul_mode_transition()` to `memory.surfaces.mode_transition`.
- Add `src/memory/cli/soul.py` with `load [slug]`.
- Add `soul` dispatch to `python -m memory`.
- Add `.pi/skills/mm-soul/SKILL.md`.
- Update focused tests for the surface and CLI activation.

## Risks

### Soul Mode activation starts too much

Activation must only set the lens and show the entry. DS2 owns recognition of living matter. DS3 owns rites. DS4 and DS5 own fruit and journal.

### Icon separation

Soul Mode uses ☾ as the mode icon, while ✦ remains the horizon icon for remembering and the Self Voice symbol. This keeps the mode distinct from the deep voice it can later invoke.

### Runtime parity

The first implementation adds the Pi skill because Pi is the validation runtime. Other runtime skill surfaces may need follow-up parity when release packaging begins.

## Validation Route

Automated:

```bash
uv run pytest tests/unit/memory/cli/test_soul.py tests/unit/memory/surfaces/test_mode_transition.py tests/unit/memory/cli/test_welcome.py -q
```

Manual smoke:

```bash
uv run python -m memory soul load soul-mode
uv run python -m memory welcome --status-line
```

Expected:

- `soul load` renders `☾ SOUL MODE ACTIVE` and the entry question.
- status line shows `Mirror Soul Mode on ☾ Soul Mode` when the journey has a display name.
- no journal entry is created.
- no rite is opened.

Pi validation:

```text
enter Soul Mode for soul-mode
```

Expected: Pi renders the Soul Mode entry surface and waits for the user's answer.
