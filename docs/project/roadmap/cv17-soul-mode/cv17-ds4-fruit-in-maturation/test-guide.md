[< Story](index.md)

# Test Guide — CV17.DS4 Fruit In Maturation

## Automated Tests

Run:

```bash
uv run pytest tests/unit/memory/cli/test_soul.py tests/unit/memory/surfaces/test_soul.py tests/unit/memory/services/test_soul.py -q
```

Expected:

- Fruit In Maturation renders with `❦ FRUIT IN MATURATION`;
- card includes the provisional fruit text;
- card ends with `continue if you want to mature more / or say you wish to harvest`;
- empty fruit is rejected;
- `soul fruit set` stores and renders the current fruit;
- `soul fruit show` renders stored fruit;
- setting another fruit replaces the previous one;
- `soul fruit clear` clears provisional state;
- no journal entry or conversation record is created.

## CLI Smoke

Run:

```bash
uv run python -m memory soul fruit set "Belonging cannot be bought by becoming necessary before anyone asks."
uv run python -m memory soul fruit show
uv run python -m memory soul fruit clear
```

Expected set/show output includes:

```text
❦  FRUIT IN MATURATION
Belonging cannot be bought by
becoming necessary before anyone asks.
continue if you want to mature more
or say you wish to harvest
```

Expected absence:

```text
HARVESTED FRUIT
save to journal?
journal entry created
```

## Pi Manual Validation

Start from DS3:

```text
enter Soul Mode for soul-mode
```

Reach Possible Listenings, choose Self Voice, and continue with material such as:

```text
O que fica claro é que eu não quero deixar de ser útil. Eu quero deixar de usar utilidade como prova de que eu ainda pertenço.
```

Expected:

- Mirror responds through the active voice;
- Mirror renders Fruit In Maturation at the end when the insight condenses;
- the fruit is short, memorable, and not a task.

Then continue:

```text
Sim. Talvez o ponto seja que a utilidade pode continuar existindo, mas não como pagamento antecipado para não ser esquecido.
```

Expected:

- Mirror refines the same fruit;
- Mirror does not list several separate fruits;
- Mirror does not harvest or write to journal yet.

## Regression Checks

- Soul Mode entry still works.
- Possible Listenings still works.
- Self Voice and Shadow Voice active rite cards still work.
- Voice listening cards still use visible titles (`✦ SELF VOICE LISTENING`, `◐ SHADOW VOICE LISTENING`).
