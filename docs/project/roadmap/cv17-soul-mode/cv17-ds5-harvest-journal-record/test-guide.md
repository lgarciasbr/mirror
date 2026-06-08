[< Story](index.md)

# Test Guide — CV17.DS5 Harvest And Journal Record

## Automated

```bash
uv run pytest tests/unit/memory/cli/test_soul.py tests/unit/memory/surfaces/test_soul.py tests/unit/memory/services/test_soul.py -q
```

Expected:

- Harvested Fruit renders.
- Save requires explicit confirmation via command.
- Save creates one journal entry with Soul Mode tags.
- Decline creates no journal entry.
- Fruit state is cleared after save/decline.

## CLI Smoke

```bash
uv run python -m memory soul fruit set "Usefulness can remain a gift only when it stops being payment for belonging."
uv run python -m memory soul harvest set "Usefulness can remain a gift only when it stops being payment for belonging."
uv run python -m memory soul harvest save --journey soul-mode
```

Expected harvest surface:

```text
❦  HARVESTED FRUIT
Usefulness can remain a gift only when
it stops being payment for belonging.
save to journal?
```

## Pi Manual Validation

After Fruit In Maturation appears, say:

```text
I want to harvest this.
```

Expected: Harvested Fruit appears and asks whether to save to journal.

Then say:

```text
Yes, save it.
```

Expected: one journal entry is created. A repeated save should not create another entry.
