[< Story](index.md)

# Test Guide — CV13.E2.S2 Switch local Mirror

## Automated checks

```bash
uv run pytest tests/unit/memory/web/test_mirrors.py tests/unit/memory/web/test_server.py
uv run ruff check src/memory/web tests/unit/memory/web/test_mirrors.py tests/unit/memory/web/test_server.py
uv run ruff format --check src/memory/web tests/unit/memory/web/test_mirrors.py tests/unit/memory/web/test_server.py
node --check src/memory/web/static/app.js
git diff --check
```

## Manual browser validation

1. Start the local web server with at least two local Mirrors containing `memory.db`.
2. Open the Mirror selector.
3. Select another Mirror.
4. Confirm the selector marks the new Mirror as active.
5. Confirm Workspace/Identity content changes to the selected Mirror.
6. Confirm non-Mirror directories such as `backups` are absent.
7. Confirm there is no arbitrary path input.
8. Refresh the page and confirm the running session still reflects the selected Mirror if in-scope; otherwise confirm the non-persistence is explicit.
