[< Story](index.md)

# Test Guide — CV17.DS3 Active Rite And Minimal Listening Lenses

## Automated Tests

Run:

```bash
uv run pytest tests/unit/memory/cli/test_soul.py tests/unit/memory/surfaces/test_soul.py -q
```

Expected:

- Self Voice listening renders with `✦ SELF VOICE LISTENING`;
- Shadow Voice listening renders with `◐ SHADOW VOICE LISTENING`;
- cards include `the voice says` and `listening for`;
- custom utterance and listening focus render correctly;
- unsupported voices are rejected;
- no fruit, harvest, or journal surfaces appear.

## CLI Smoke

Run:

```bash
uv run python -m memory soul rite self
uv run python -m memory soul rite shadow
```

Expected Self output includes:

```text
✦  SELF VOICE LISTENING
the voice says
usefulness can remain a gift
listening for
what remains true without proof
```

Expected Shadow output includes:

```text
◐  SHADOW VOICE LISTENING
the voice says
if they depend on me, they cannot forget me
listening for
the protection inside control
```

Expected absence:

```text
FRUIT IN MATURATION
HARVESTED FRUIT
save to journal?
```

## Pi Manual Validation

Start from DS2:

```text
enter Soul Mode for soul-mode
```

Answer until Possible Listenings appears. Then choose Self Voice naturally:

```text
I want Self Voice.
```

Expected:

- Mirror renders the Self Voice listening card visibly;
- the card contains what the voice says;
- after the card, Mirror makes an interpretive bridge to the conversation;
- Mirror does not roleplay Self Voice as a separate interlocutor;
- Mirror does not render Fruit In Maturation yet unless DS4 is intentionally invoked.

Repeat with Shadow Voice:

```text
Let's hear the shadow.
```

Expected:

- Mirror renders the Shadow Voice listening card visibly;
- the card contains what the voice says;
- after the card, Mirror connects the utterance to the rejected part's protection;
- Mirror does not punish, diagnose, or govern the shadow.

## Regression Checks

- Soul Mode entry still works.
- Possible Listenings still ends with the instruction to choose a voice or continue conversation.
- Wisdom Voice and Beauty Voice do not open active listening surfaces in this story.
