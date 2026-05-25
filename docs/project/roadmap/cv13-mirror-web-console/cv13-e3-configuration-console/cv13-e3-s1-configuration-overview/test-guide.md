[< Story](index.md)

# Test Guide — CV13.E3.S1 Configuration overview

## Automated checks

```bash
uv run pytest tests/unit/memory/web/test_configuration.py tests/unit/memory/web/test_server.py
uv run ruff check src/memory/web tests/unit/memory/web/test_configuration.py tests/unit/memory/web/test_server.py
uv run ruff format --check src/memory/web tests/unit/memory/web/test_configuration.py tests/unit/memory/web/test_server.py
node --check src/memory/web/static/app.js
git diff --check
```

## Manual browser validation

1. Open the web app.
2. Open the new Configuration tab.
3. Confirm Mirror home, database, preferences, backups, exports, transcripts, and extensions appear.
4. Confirm found/missing status is clear.
5. Confirm no secrets/API keys are shown.
6. Confirm the page is read-only.
