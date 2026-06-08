[< Story](index.md)

# Plan — CV17.DS4 Fruit In Maturation

## Boundary

This story adds provisional harvest state inside an active Soul Mode rite. Mirror can render one **Fruit In Maturation** and refine it across turns, without writing to the journal.

DS4 does not finalize the fruit. DS5 owns Harvested Fruit and optional journal persistence.

## Product Behavior

Inside Self Voice or Shadow Voice, after the user has answered deeply enough, Mirror can condense the living matter into one provisional fruit:

```text
Soul Mode
╭────────────────────────────────────────╮
│   ❦  FRUIT IN MATURATION               │
│                                        │
│   Belonging cannot be bought by        │
│   becoming necessary before anyone     │
│   asks.                                │
│                                        │
│   continue if you want to mature more  │
│   or say you wish to harvest           │
╰────────────────────────────────────────╯
```

The fruit is not a summary of everything. It is the current best formulation of the living harvest. When the user continues, Mirror should rewrite or thicken the same fruit, not create several separate takeaways.

## Design

Add a Soul Mode fruit surface and a lightweight session state service.

### Surface

Add to `src/memory/surfaces/soul.py`:

```python
def render_fruit_in_maturation(fruit: str) -> str:
    ...
```

Validation:

- rejects empty fruit;
- wraps text in the existing 40-column Soul Mode card style;
- always ends with the continuation/harvest instruction.

### State

Add a small service:

```text
src/memory/services/soul.py
```

Proposed API:

```python
@dataclass(frozen=True)
class SoulFruitState:
    session_id: str
    fruit: str | None


def get_fruit_in_maturation(store, *, session_id: str | None = None) -> SoulFruitState:
    ...


def set_fruit_in_maturation(store, fruit: str, *, session_id: str | None = None) -> SoulFruitState:
    ...


def clear_fruit_in_maturation(store, *, session_id: str | None = None) -> None:
    ...
```

Use runtime session metadata rather than a new database table. The state is provisional and session-scoped. It should not create memories, journal entries, or conversation messages.

Metadata shape:

```json
{
  "soul": {
    "fruit_in_maturation": "..."
  }
}
```

The exact implementation should reuse existing runtime session metadata helpers where possible.

### CLI

Extend `memory soul`:

```bash
uv run python -m memory soul fruit set "Belonging cannot be bought by becoming necessary."
uv run python -m memory soul fruit show
uv run python -m memory soul fruit clear
```

Behavior:

- `set` stores the current fruit and renders Fruit In Maturation;
- `show` renders the current fruit if present;
- `clear` clears provisional fruit state and prints a minimal confirmation;
- all commands accept optional `--session-id` for Pi session scoping;
- no command writes to journal.

## Pi Skill Contract

Update `.pi/skills/mm-soul/SKILL.md`:

- during an active Self or Shadow rite, when the conversation yields a provisional harvest, call `uv run python -m memory soul fruit set "..."`;
- paste the Fruit In Maturation card visibly at the end of the response;
- keep exactly one fruit in maturation, rewriting it when the formulation improves;
- do not treat the fruit as final until the user asks to harvest;
- if the user says they want to mature more, continue the active rite and keep the fruit provisional;
- if the user says they wish to harvest, stop at a DS5 boundary until DS5 is implemented.

## Fruit Quality

A good fruit is:

- short enough to remember;
- phrased as living insight, not as a task;
- more distilled than a summary;
- faithful to the active voice;
- revisable.

Examples:

```text
Belonging cannot be bought by becoming necessary before anyone asks.

The rejected part is not asking to rule; it is asking not to disappear.

Usefulness can remain a gift only when it stops being a payment for belonging.
```

Bad fruits:

```text
I should stop checking messages and metrics.
```

Too behavioral; this is a task.

```text
Today I talked about anxiety, usefulness, belonging, and attention.
```

Too summarizing; this is a recap.

## Tests

Add tests for:

- `render_fruit_in_maturation()` renders the card and instruction;
- empty fruit is rejected;
- CLI `soul fruit set` stores and renders the fruit;
- CLI `soul fruit show` renders the stored fruit;
- CLI `soul fruit clear` removes it;
- setting a second fruit replaces the first rather than accumulating;
- no conversation or journal records are created by fruit commands.

## Validation Route

Automated:

```bash
uv run pytest tests/unit/memory/cli/test_soul.py tests/unit/memory/surfaces/test_soul.py tests/unit/memory/services/test_soul.py -q
```

Manual CLI smoke:

```bash
uv run python -m memory soul fruit set "Belonging cannot be bought by becoming necessary before anyone asks."
uv run python -m memory soul fruit show
uv run python -m memory soul fruit clear
```

Pi validation:

1. Enter Soul Mode.
2. Reach Possible Listenings.
3. Choose Self Voice or Shadow Voice.
4. Continue the rite until living harvest appears.
5. Confirm Mirror renders Fruit In Maturation at the end of the response.
6. Continue once more.
7. Confirm Mirror refines the same fruit rather than listing multiple fruits.
8. Confirm no journal record is created.

## Risks

### Fruit becomes summary

The fruit must be an insight formulation, not a transcript summary.

### Fruit appears too early

Do not render fruit after every answer. Render it only when something has actually condensed.

### DS4 leaks into DS5

If the user asks to harvest before DS5 is implemented, acknowledge the boundary. Do not save to journal yet.
