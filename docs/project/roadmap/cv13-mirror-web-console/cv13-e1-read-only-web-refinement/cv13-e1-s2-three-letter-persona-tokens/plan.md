[< Story](index.md)

# Plan — CV13.E1.S2 Three-letter persona tokens

## Design

Persona orbit buttons already render the token from `card.metadata.icon`. The clean boundary is therefore the Atlas surface read model, not the web renderer.

Change `src/memory/surfaces/atlas.py` so `_initials()` becomes a three-letter token generator:

- derive from the public label, not the raw key;
- ignore spaces, hyphens, punctuation, and symbols;
- uppercase the first three alphanumeric characters;
- if fewer than three characters exist, return the available uppercase token or `?` for empty labels.

This keeps persona-token rendering unchanged while making the read-model contract explicit.

## Tests

Update `tests/unit/memory/surfaces/test_atlas.py` to assert `Engineer` renders `ENG` and add a compact assertion for a hyphenated persona key.

## Risk

Low. Existing CSS already supports wider persona tokens, and current personal Mirror validation showed the orbit can visually hold three-letter tokens.
