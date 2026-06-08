[< Story](index.md)

# Plan — CV17.DS2 Living Field And Possible Listenings

## Boundary

This story adds the first conversational transition after Soul Mode entry. The user answers the entry question in natural language. Mirror listens to the living field, recognizes when enough ritual matter has appeared, and renders a situated Possible Listenings surface.

This story does not implement active rite behavior. Choosing a listening is allowed to be recognized only enough to prepare DS3. DS3 owns opening Self Voice and Shadow Voice.

## Product Behavior

After Soul Mode entry, the user answers:

```text
how is your day going today?
```

Mirror should treat the response as free conversation, not as a form field. It may ask a follow-up when the answer is still only a report. When the user’s material becomes dense enough, Mirror marks the threshold with a phrase like:

```text
this already has matter for a listening.
```

Then it renders Possible Listenings at the end of the response:

```text
Soul Mode
╭────────────────────────────────────────╮
│   ✧  POSSIBLE LISTENINGS               │
│                                        │
│   ✦ Self Voice                         │
│     recognize the principle that wants │
│     to be preserved                    │
│                                        │
│   ◐ Shadow Voice                       │
│     listen to the part that wants to   │
│     be necessary                       │
│                                        │
│   ☉ Wisdom Voice                       │
│     be crossed by an idea about value  │
│     and recognition                    │
╰────────────────────────────────────────╯
```

## Design

Add a Soul Mode service that can produce a Possible Listenings proposal from a bounded input model.

First slice recommendation:

```python
@dataclass(frozen=True)
class SoulListeningOption:
    voice: str
    label: str
    description: str

@dataclass(frozen=True)
class SoulListeningProposal:
    living_matter: str
    threshold_phrase: str
    options: list[SoulListeningOption]
```

The first implementation can be deterministic and explicit. It does not need hidden LLM classification. The assistant remains responsible for interpreting the conversation and passing situated descriptions to the contained renderer. That preserves product behavior without pretending the Python core understands inner life yet.

Add a contained CLI resource:

```bash
uv run python -m memory soul listen \
  --matter "the desire to be necessary" \
  --self "recognize the principle that wants to be preserved" \
  --shadow "listen to the part that wants to be necessary" \
  --wisdom "be crossed by an idea about value and recognition"
```

The command renders the Possible Listenings surface. It should not update fruit state, open a rite, or write to the journal.

## Surface

Add `render_possible_listenings()` under a Soul-specific surface module or the existing mode surface module if the slice remains small. Prefer a new module if the grammar starts to grow:

```text
src/memory/surfaces/soul.py
```

The renderer should support two to four options. For the first release, the canonical voices are:

```text
✦ Self Voice
◐ Shadow Voice
☉ Wisdom Voice
❀ Beauty Voice
```

DS2 should allow rendering Wisdom and Beauty as options, but DS3 only needs to implement active behavior for Self Voice and Shadow Voice.

## Pi Skill Contract

Update `.pi/skills/mm-soul/SKILL.md`:

- after activation, treat the next user answer as Listening To The Living Field;
- do not show Possible Listenings when the answer is still thin;
- when living matter appears, call the contained `soul listen` renderer with situated option descriptions;
- render the surface visibly at the end of the response;
- do not open a rite until the user chooses a listening.

## Maturity Markers

Possible Listenings may appear when the user moves from reporting events to naming an inner contract or referring to an internal tension, conflict, or discomfort, such as:

```text
fear
wound
desire
compulsion
threatened sense of belonging
center touched
shadow emerging
value threatened
search for clarity
request for beauty or meaning
strong dispersion
phrase with more weight than the rest
```

The product rule remains:

```text
show Possible Listenings when the user moves from event report into living inner matter, and there is enough material for at least two plausible listenings or one dominant listening is very clear.
```

## Tests

Add focused tests for:

- rendering Possible Listenings with situated descriptions;
- CLI `soul listen` renders the surface;
- `soul listen` supports at least Self and Shadow;
- `soul listen` can include Wisdom and Beauty options;
- `soul listen` rejects empty option sets or empty descriptions.

## Validation Route

Automated:

```bash
uv run pytest tests/unit/memory/cli/test_soul.py tests/unit/memory/surfaces/test_soul.py -q
```

Manual CLI smoke:

```bash
uv run python -m memory soul listen \
  --matter "the desire to be necessary" \
  --self "recognize the principle that wants to be preserved" \
  --shadow "listen to the part that wants to be necessary" \
  --wisdom "be crossed by an idea about value and recognition"
```

Expected: output renders `✧ POSSIBLE LISTENINGS` with the provided situated descriptions.

Pi validation:

1. Enter Soul Mode.
2. Answer with a thin day report.
3. Confirm Mirror asks or reflects without showing Possible Listenings too early.
4. Answer with denser material.
5. Confirm Mirror renders Possible Listenings at the end of the response.

## Risks

### Renderer becomes fake intelligence

The contained command only renders a surface from situated material. It does not claim to detect the user’s state. That is acceptable for the first slice because the assistant carries the interpretive behavior.

### Possible Listenings becomes a menu

The descriptions must be situated. Generic descriptions should fail product review even if tests pass.

### DS2 accidentally opens DS3

DS2 stops at the invitation. Opening Self Voice or Shadow Voice belongs to DS3.
