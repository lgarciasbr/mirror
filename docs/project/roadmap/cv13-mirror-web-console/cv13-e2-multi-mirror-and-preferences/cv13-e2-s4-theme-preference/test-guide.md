[< Story](index.md)

# Test Guide — CV13.E2.S4 Theme preference

## Automated checks

```bash
uv run pytest tests/unit/memory/web/test_preferences.py tests/unit/memory/web/test_mirrors.py tests/unit/memory/web/test_server.py
uv run ruff check src/memory/web tests/unit/memory/web/test_preferences.py tests/unit/memory/web/test_mirrors.py tests/unit/memory/web/test_server.py
uv run ruff format --check src/memory/web tests/unit/memory/web/test_preferences.py tests/unit/memory/web/test_mirrors.py tests/unit/memory/web/test_server.py
node --check src/memory/web/static/app.js
git diff --check
```

## Manual browser validation

1. Open Preferences.
2. Select Dark and confirm the page switches to dark immediately.
3. Select Light and confirm the page switches to light immediately.
4. Select System and confirm the forced override is removed.
5. Reload and confirm the selected theme persists.
6. Switch Mirrors and confirm theme is scoped per Mirror.
