[< Story](index.md)

# Test Guide — CV13.E5.S6 Operations Runner surface

## Automated checks

```bash
uv run pytest tests/unit/memory/web/test_operations.py tests/unit/memory/web/test_server.py tests/unit/memory/services/test_operation_runs.py tests/unit/memory/db/test_migrations.py
uv run ruff check src/memory tests/unit/memory/web/test_operations.py tests/unit/memory/web/test_server.py tests/unit/memory/services/test_operation_runs.py tests/unit/memory/db/test_migrations.py
uv run ruff format --check src/memory tests/unit/memory/web/test_operations.py tests/unit/memory/web/test_server.py tests/unit/memory/services/test_operation_runs.py tests/unit/memory/db/test_migrations.py
node --check src/memory/web/static/app.js
git diff --check
```

## Manual browser validation

1. Start the local web server.
2. Open the Operations tab.
3. Confirm runnable operations are visible with descriptions, risk, dry-run, parameters, and run controls.
4. Confirm future operations are visible without run controls.
5. Run Runtime health and confirm a structured result appears and recent history refreshes.
6. Run Database backup with verification enabled and confirm backup evidence appears.
7. Run Conversation journey repair with dry-run enabled and confirm it previews candidates or reports none without applying.
8. Confirm recent runs show status, outcome, timestamps, parameters, summary, and errors when present.
9. Confirm there is no arbitrary command, path, SQL, restore, delete, update, or streaming surface.
