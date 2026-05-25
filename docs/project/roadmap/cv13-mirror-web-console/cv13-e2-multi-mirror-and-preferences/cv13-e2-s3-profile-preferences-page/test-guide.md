[< Story](index.md)

# Test Guide — CV13.E2.S3 Profile/preferences page

## Automated checks

```bash
uv run pytest tests/unit/memory/web/test_preferences.py tests/unit/memory/web/test_mirrors.py tests/unit/memory/web/test_server.py
uv run ruff check src/memory/web tests/unit/memory/web/test_preferences.py tests/unit/memory/web/test_mirrors.py tests/unit/memory/web/test_server.py
uv run ruff format --check src/memory/web tests/unit/memory/web/test_preferences.py tests/unit/memory/web/test_mirrors.py tests/unit/memory/web/test_server.py
node --check src/memory/web/static/app.js
git diff --check
```

## Manual browser validation

1. Open the web app and switch to Preferences.
2. Confirm the active Mirror context is visible.
3. Change display name and avatar symbol.
4. Save and confirm the header updates.
5. Reload the page and confirm the saved profile remains.
6. Switch to another Mirror and confirm preferences are scoped to that Mirror.
