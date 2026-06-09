[< Story](index.md)

# Test Guide — CV19.DS2 Integration Review

## Automated Tests

Run:

```bash
uv run pytest tests/unit/memory/cli/test_soul.py tests/unit/memory/surfaces/test_soul.py -q
```

Expected:

- Integration Review renders with provided sections.
- Empty sections are omitted.
- At least one section is required.
- The review-only footer renders.
- Existing Soul Mode voice, fruit, harvest, and closing tests still pass.

## CLI Smoke

Run:

```bash
uv run python -m memory soul review \
  --journal "The fruit was already saved as journal." \
  --self "Commitment may need to belong to truth, not image management." \
  --shadow "A part fears being seen as careless without over-availability." \
  --ego "Staying late can become image management." \
  --persona "The committed professional persona may overperform availability." \
  --open "How to sustain measure under uncertain gaze."
```

Expected output includes:

```text
☾  INTEGRATION REVIEW
journal
self
shadow
ego behavior
persona
leave open
review only — no identity changed
```

Expected absence:

- no journal save;
- no identity mutation;
- no journey identity category;
- no project mutation.

## Pi Manual Validation

After Closing Rite, say naturally:

```text
sim, quero olhar o que pode permanecer
```

Expected:

- Mirror renders Integration Review.
- The review classifies material conservatively.
- Mirror does not propose an exact identity diff yet.
- Mirror does not mutate identity.
- Mirror can explain that proposal/application are later steps.
