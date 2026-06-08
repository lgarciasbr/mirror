[< Story](index.md)

# Plan — CV17.DS5 Harvest And Journal Record

## Boundary

This story closes the provisional Fruit In Maturation into one Harvested Fruit and adds explicit journal persistence only after user confirmation.

## Design

Add to `src/memory/surfaces/soul.py`:

```python
def render_harvested_fruit(fruit: str) -> str
```

Add to `src/memory/services/soul.py`:

```python
def harvest_fruit(store, *, fruit: str | None = None, session_id: str | None = None) -> SoulFruitState
```

Harvest uses the current fruit in maturation unless an explicit fruit is supplied, stores it as `harvested_fruit`, and clears `fruit_in_maturation`.

Extend CLI:

```bash
uv run python -m memory soul harvest show
uv run python -m memory soul harvest save [--journey slug]
uv run python -m memory soul harvest decline
```

Also support:

```bash
uv run python -m memory soul harvest set "final fruit"
```

Behavior:

- `harvest set` closes the fruit and renders Harvested Fruit;
- `harvest show` renders current harvested fruit;
- `harvest save` creates exactly one journal entry and clears harvested state;
- repeated `harvest save` after state is cleared fails cleanly, preventing duplicate saves;
- `harvest decline` clears harvested state without saving.

Journal entry content is structured Markdown composed from the harvested fruit and, when available, the originating conversation transcript. Use explicit classification fields to avoid an LLM call:

```python
title=<first sentence of harvested fruit>
content=<markdown entry with fruit, origin link, and conversation material>
layer="self"
tags=["soul-mode", "harvested-fruit"]
conversation_id=<originating conversation id when available>
metadata={"format": "markdown", "origin": {"mode": "soul", ...}}
```

## Tests

- Harvested Fruit renders with `❦ HARVESTED FRUIT` and `save to journal?`.
- Empty harvest is rejected.
- `harvest set` renders and clears fruit in maturation.
- `harvest save` creates exactly one journal entry and clears harvested state.
- A second save does not create a duplicate.
- `harvest decline` creates no journal entry and clears state.

## Pi Contract

When the user asks to harvest, call `memory soul harvest set` with the final fruit or call `memory soul harvest show` if already harvested. Paste the Harvested Fruit surface visibly. Do not save until the user confirms. When the user confirms, call `memory soul harvest save`; when they decline, call `memory soul harvest decline`.
