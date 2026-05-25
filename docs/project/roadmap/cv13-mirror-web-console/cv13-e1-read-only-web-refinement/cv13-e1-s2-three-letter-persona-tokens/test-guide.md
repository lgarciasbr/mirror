[< Story](index.md)

# Test Guide — CV13.E1.S2 Three-letter persona tokens

## Automated validation

Run:

```bash
uv run pytest tests/unit/memory/surfaces/test_atlas.py
uv run ruff check src/memory/surfaces/atlas.py tests/unit/memory/surfaces/test_atlas.py
uv run ruff format --check src/memory/surfaces/atlas.py tests/unit/memory/surfaces/test_atlas.py
git diff --check
```

Expected result: all commands pass.

## Manual browser validation

Start the web app:

```bash
uv run python -m memory web
```

Open Identity:

```text
http://127.0.0.1:8765#atlas
```

Expected observations:

- persona orbit tokens show three letters;
- labels remain readable under each token;
- clicking a persona token still opens object detail.
