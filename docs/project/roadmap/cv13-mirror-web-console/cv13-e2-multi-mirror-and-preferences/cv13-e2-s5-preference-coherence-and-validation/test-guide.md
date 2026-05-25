[< Story](index.md)

# Test Guide — CV13.E2.S5 Preference coherence and validation

## Automated checks

```bash
uv run pytest tests/unit/memory/web/test_preferences.py tests/unit/memory/web/test_mirrors.py tests/unit/memory/web/test_server.py
uv run ruff check src/memory/web tests/unit/memory/web/test_preferences.py tests/unit/memory/web/test_mirrors.py tests/unit/memory/web/test_server.py
uv run ruff format --check src/memory/web tests/unit/memory/web/test_preferences.py tests/unit/memory/web/test_mirrors.py tests/unit/memory/web/test_server.py
node --check src/memory/web/static/app.js
git diff --check
```

## Manual browser validation

1. Start the web app with at least two local Mirrors.
2. Confirm non-Mirror directories are absent from the selector.
3. Select Mirror A and set display name, avatar, and theme.
4. Select Mirror B and confirm Mirror A preferences do not leak.
5. Set different display name, avatar, and theme for Mirror B.
6. Switch back to Mirror A and confirm its preferences return.
7. Reload and confirm the active Mirror's preferences persist.
8. Confirm there is still no arbitrary path input or identity/configuration edit flow.
