[< Story](index.md)

# Test Guide — CV13.E6.S3 Controlled command executor

## Automated validation

```bash
uv run pytest tests/unit/memory/web tests/unit/memory/services/test_operation_runs.py tests/unit/memory/db/test_migrations.py -q
uv run ruff check .
node --check src/memory/web/static/app.js
git diff --check
```

## Behavioral checks

- The executor accepts only code-owned argv lists, not user command strings.
- Commands run with `shell=False`.
- Commands use explicit cwd and sanitized environment.
- Timeout returns bounded failure evidence.
- Stdout and stderr are captured and truncated to configured limits.
- The `runtime-diagnose` operation is allowlisted, read-only, and runnable.
- Running `runtime-diagnose` creates an async operation run and returns command evidence through the run result.
- Future operation ids and unsupported parameters remain rejected.
- No browser API accepts raw command, cwd, env, shell, SQL, git, update, or migration input.

## Manual validation

If browser validation is requested:

- Open Operations.
- Run `Runtime diagnosis`.
- Confirm it queues, completes, shows command evidence, and records a timeline.
- Confirm there is no field for arbitrary command text.

## Acceptance evidence

Record automated results, browser observations if any, and the exact command boundary introduced.
