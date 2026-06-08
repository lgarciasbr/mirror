[< Story](index.md)

# Test Guide — CV17.DS2 Living Field And Possible Listenings

## Automated Tests

Run:

```bash
uv run pytest tests/unit/memory/cli/test_soul.py tests/unit/memory/surfaces/test_soul.py -q
```

Expected:

- all tests pass;
- Possible Listenings renders with `✧ POSSIBLE LISTENINGS`;
- Self Voice, Shadow Voice, Wisdom Voice, and Beauty Voice render with their icons when supplied;
- descriptions are passed through from situated input;
- empty option descriptions are rejected.

## CLI Smoke

Run:

```bash
uv run python -m memory soul listen \
  --matter "the desire to be necessary" \
  --self "recognize the principle that wants to be preserved" \
  --shadow "listen to the part that wants to be necessary" \
  --wisdom "be crossed by an idea about value and recognition"
```

Expected output includes:

```text
✧  POSSIBLE LISTENINGS
✦ Self Voice
recognize the principle that wants to be preserved
◐ Shadow Voice
listen to the part that wants to be necessary
☉ Wisdom Voice
be crossed by an idea about value and recognition
Say if you want to hear one of these voices now, or just continue the conversation.
```

Expected absence:

```text
SELF VOICE LISTENING
SHADOW VOICE LISTENING
FRUIT IN MATURATION
HARVESTED FRUIT
save to journal?
```

## Pi Manual Validation

Start from DS1:

```text
enter Soul Mode for soul-mode
```

When the entry surface appears, answer with a thin report:

```text
My day is a little strange. I started well but got tired after lunch.
```

Expected:

- Mirror does not force Possible Listenings yet;
- Mirror asks or reflects to find what in the day carries weight.

Then answer with denser material:

```text
I think I got tired because I noticed I am still trying to prove I am necessary.
```

Expected:

- Mirror marks the threshold in natural language;
- Mirror renders Possible Listenings at the end of the response;
- the card descriptions are situated in this material;
- the card ends by telling the user they can hear one of these voices now or just continue the conversation;
- Mirror does not open a rite until the user chooses a listening.

## Regression Checks

- Soul Mode entry from DS1 still works.
- Status line still shows `☾ Soul Mode`.
- No journal entry is created by `soul listen`.
- No fruit state is created by `soul listen`.
