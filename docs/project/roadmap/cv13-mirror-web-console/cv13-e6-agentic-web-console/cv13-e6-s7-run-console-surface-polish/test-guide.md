[< Story](index.md)

# Test Guide — CV13.E6.S7 Run console surface polish

```bash
uv run pytest tests/unit/memory/web tests/unit/memory/services/test_operation_runs.py tests/unit/memory/db/test_migrations.py -q
uv run ruff check .
node --check src/memory/web/static/app.js
git diff --check
```

Manual browser validation:

- Run Runtime health and confirm a dedicated console opens.
- Confirm timeline/output occupy the main page area.
- Confirm metadata/action cards sit to the side.
- Run Agent run prototype and confirm the future input affordance is visible but bounded/disabled.
