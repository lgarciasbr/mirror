[< Story](index.md)

# Test Guide — CV13.E5.S5 Operation job history and audit evidence

## Automated checks

```bash
uv run pytest tests/unit/memory/web/test_operations.py tests/unit/memory/web/test_server.py tests/unit/memory/services/test_operation_runs.py tests/unit/memory/db/test_migrations.py
uv run ruff check src/memory tests/unit/memory/web/test_operations.py tests/unit/memory/web/test_server.py tests/unit/memory/services/test_operation_runs.py tests/unit/memory/db/test_migrations.py
uv run ruff format --check src/memory tests/unit/memory/web/test_operations.py tests/unit/memory/web/test_server.py tests/unit/memory/services/test_operation_runs.py tests/unit/memory/db/test_migrations.py
node --check src/memory/web/static/app.js
git diff --check
```

## Manual validation

Manual validation is optional for this API-only story unless a visible web surface is introduced.

If manual validation is desired:

1. Start the local web server against a disposable Mirror home.
2. Run a known operation:

   ```bash
   curl -X POST http://127.0.0.1:8765/api/operations/run \
     -H 'Content-Type: application/json' \
     -d '{"operationId":"runtime-health"}' | python -m json.tool
   ```

3. Confirm the response includes `runId`.
4. List recent runs:

   ```bash
   curl http://127.0.0.1:8765/api/operations/runs | python -m json.tool
   ```

5. Confirm the run appears with status, outcome, timestamps, sanitized parameters, summary, and result evidence.
6. Run a known operation with invalid parameters and confirm a failed run is recorded without unsafe payload fields.

## Expected result

Operation execution remains synchronous, but every known operation request leaves local audit evidence suitable for a future Operations Runner surface.
