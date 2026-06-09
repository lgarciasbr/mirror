[< Story](index.md)

# Plan — CV19.DS2 Integration Review

## Boundary

This story adds a review-only surface. It can classify material as possible journal, Self, Shadow, Ego behavior, persona, or leave-open material. It must not propose a final identity diff or mutate identity.

## Design

Add a textual Soul Mode surface:

```text
Soul Mode
╭────────────────────────────────────────╮
│   ☾  INTEGRATION REVIEW                │
│                                        │
│   journal                              │
│   [...]                                │
│                                        │
│   self                                 │
│   [...]                                │
│                                        │
│   shadow                               │
│   [...]                                │
│                                        │
│   ego behavior                         │
│   [...]                                │
│                                        │
│   persona                              │
│   [...]                                │
│                                        │
│   leave open                           │
│   [...]                                │
│                                        │
│   review only — no identity changed    │
╰────────────────────────────────────────╯
```

Add CLI support:

```bash
uv run python -m memory soul review \
  --journal "..." \
  --self "..." \
  --shadow "..." \
  --ego "..." \
  --persona "..." \
  --open "..."
```

Sections are optional, but at least one section is required. Empty sections do not render.

## Post-Closing Invitation

After Closing Rite, Mirror should ask:

```text
Há material vivo que pode querer permanecer. Quer olhar comigo antes de encerrarmos?
```

If the user says yes, Mirror renders Integration Review. If the user declines, Mirror may ask whether there is another theme from the day or whether to end.

## Category Rules

- `journal`: material that belongs as record of the session.
- `self`: principle, value, inner law, or constitution.
- `shadow`: rejected protection, fear, hidden contract, or defensive need.
- `ego behavior`: operational pattern or repeated reaction.
- `persona`: public role, mask, presentation style, or social identity pattern.
- `leave open`: questions or material not ready for integration.

Journey identity is intentionally excluded.

## Validation Route

Automated:

```bash
uv run pytest tests/unit/memory/cli/test_soul.py tests/unit/memory/surfaces/test_soul.py -q
uv run ruff check src tests
uv run ruff format --check src tests
```

Manual CLI smoke:

```bash
uv run python -m memory soul review \
  --self "A principle that may belong to Self." \
  --shadow "A protection that may belong to Shadow." \
  --open "A question that should remain open."
```

Pi validation:

```text
sim, quero olhar o que pode permanecer
```

Expected:

- Integration Review renders visibly.
- Empty categories are omitted.
- The card says `review only — no identity changed`.
- No journal or identity mutation occurs.
