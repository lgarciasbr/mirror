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

- Self: principle I want to practice, phrased in first person without demanding perfection. Example: `Meu compromisso verdadeiro nasce da verdade do trabalho, não da gestão da imagem.`
- Shadow: protective part I need to recognize, phrased without shame or command. Example: `Uma parte minha tenta comprar segurança oferecendo disponibilidade excessiva quando teme ser julgada como descuidada.`
- Ego: operational behavior I tend to execute under tension. Example: `Quando temo julgamento, posso compensar permanecendo disponível além da medida real.`
- Persona: public presentation pattern or role-mask, not essence. Example: `Minha persona profissional pode confundir confiabilidade com disponibilidade visível em excesso.`

## Validation

```bash
uv run pytest tests/unit/memory/cli/test_soul.py tests/unit/memory/surfaces/test_soul.py -q
```
