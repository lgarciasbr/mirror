[< Story](index.md)

# Plan — CV19.DS3 Psyche Enrichment Proposal

## Boundary

Proposal is not mutation. This story renders a possible identity enrichment, but does not apply it.

## Design

Command:

```bash
uv run python -m memory soul propose self \
  --origin "Soul Mode harvest ..." \
  --current "current identity excerpt or none" \
  --proposed "proposed identity content" \
  --why "why this may belong"
```

Targets:

- `self` → default key `soul`
- `shadow` → default key `profile`
- `ego` → default key `behavior`
- `persona` → requires `--key`

Surface footer:

```text
proposal only — no identity changed
```

Before rendering a proposal, Mirror should load the current target identity when possible. The proposed content must be the exact target content to write, not an informal summary. If the target identity is a longer document, the proposal should contain a full replacement or explicit additive section so DS4 does not accidentally overwrite the whole layer with a fragment.

Layer language:

- Self: first-person principle adopted as practice, allowing good and bad days.
- Shadow: first-person recognition of a protective part without shame.
- Ego: operational behavior pattern.
- Persona: public-role or presentation pattern, not essence.

## Validation

```bash
uv run pytest tests/unit/memory/cli/test_soul.py tests/unit/memory/surfaces/test_soul.py -q
```
