[< Story](index.md)

# Plan — CV17.DS3 Active Rite And Minimal Listening Lenses

## Boundary

This story begins the first active listening after Possible Listenings. When the user chooses Self Voice or Shadow Voice, Mirror renders a listening card containing what the voice says, then Mirror makes an interpretive bridge back to the ongoing conversation.

Voices are listening lenses, not conversational agents. The user always converses with Mirror.

## Product Behavior

After Possible Listenings, the user may answer naturally:

```text
I want Self Voice.
Let's hear the shadow.
Maybe the part that wants to be necessary.
Can we listen to Shadow Voice?
```

Mirror recognizes Self Voice and Shadow Voice choices, renders a voice-listening card, then interprets the utterance in relation to the user's material.

### Self Voice Listening

```text
Soul Mode
╭────────────────────────────────────────╮
│   ✦  SELF VOICE LISTENING              │
│                                        │
│   the voice says                       │
│                                        │
│   usefulness can remain a gift         │
│   only when it stops being payment     │
│   for belonging                        │
│                                        │
│   listening for                        │
│   what remains true without proof      │
╰────────────────────────────────────────╯
```

### Shadow Voice Listening

```text
Soul Mode
╭────────────────────────────────────────╮
│   ◐  SHADOW VOICE LISTENING            │
│                                        │
│   the voice says                       │
│                                        │
│   if they depend on me,                │
│   they cannot forget me                │
│                                        │
│   listening for                        │
│   the protection inside control        │
╰────────────────────────────────────────╯
```

The card is the visible state transition. The voice's symbolic utterance belongs inside the card. The prose that follows is Mirror's interpretive bridge, not the voice roleplaying as a separate speaker.

## Design

`render_active_rite()` remains the compatibility name, but DS6 usage adjustment changes its grammar to a listening-lens surface:

```python
def render_active_rite(
    voice: str,
    *,
    utterance: str | None = None,
    listening_for: str | None = None,
    question: str | None = None,  # legacy alias for utterance
) -> str:
    ...
```

Supported voices for the first release:

```text
self
shadow
```

CLI:

```bash
uv run python -m memory soul rite self \
  --says "silence is not exile" \
  --listening-for "the fact before the fear"
```

## Pi Skill Contract

- If Possible Listenings are visible and the user chooses Self Voice or Shadow Voice, call `uv run python -m memory soul rite <voice>`.
- Prefer situated `--says` and `--listening-for` copy when the conversation has clear material.
- Paste the rendered card visibly before the interpretive bridge.
- Do not prefix prose as if the voice were speaking separately.
- Self Voice listens for principles, values, internal constitution, and what must not be betrayed. Its runtime prompt is `src/memory/prompts/soul_self_voice.md`.
- Shadow Voice listens to the rejected part without punishment, asking what protection or necessity it carries.
- Do not open Wisdom Voice or Beauty Voice yet.
- Do not mature fruit, harvest, or write to journal in DS3.

## Tests

Add tests for:

- `render_active_rite("self")` renders `✦ SELF VOICE LISTENING`, `the voice says`, and the default Self utterance;
- `render_active_rite("shadow")` renders `◐ SHADOW VOICE LISTENING`, `the voice says`, and the default Shadow utterance;
- custom `utterance` and `listening_for` render and wrap correctly;
- unsupported voices are rejected;
- CLI `soul rite self` and `soul rite shadow` render the corresponding cards;
- CLI rejects unsupported voices.

## Validation Route

Automated:

```bash
uv run pytest tests/unit/memory/cli/test_soul.py tests/unit/memory/surfaces/test_soul.py -q
```

Manual CLI smoke:

```bash
uv run python -m memory soul rite self
uv run python -m memory soul rite shadow
```

Pi validation:

1. Enter Soul Mode.
2. Reach Possible Listenings.
3. Say: `I want Self Voice.`
4. Confirm the Self Voice listening card appears with `the voice says`.
5. Confirm Mirror then makes an interpretive bridge to the conversation.
6. Repeat with Shadow Voice.

## Risks

### Voice becomes a character

Do not let the user converse with the voice. The user converses with Mirror; Mirror listens through a voice.

### Shadow Voice becomes punitive

Shadow Voice must not accuse, govern, or fix the shadow. It reveals the rejected part's protection and necessity.

### DS3 leaks into DS4

The assistant may notice fruit material, but should not render Fruit In Maturation until DS4 behavior is intentionally used.
