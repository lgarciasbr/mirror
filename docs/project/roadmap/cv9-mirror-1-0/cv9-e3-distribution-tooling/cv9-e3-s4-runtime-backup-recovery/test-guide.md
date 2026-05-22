[< Story](index.md)

# Test Guide — Runtime Backup and Recovery Prerequisite

## Automated Verification

Focused tests:

```bash
uv run pytest tests/unit/memory/cli/test_backup.py tests/unit/memory/cli/test_runtime.py
```

Full verification before closeout:

```bash
uv sync --extra dev
uv run pytest tests/unit/ tests/integration/ -m "not live"
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/
uv run mypy src/memory/cli/runtime.py
git diff --check
```

## Manual Validation Route

Use a temporary Mirror home only. Do not run this manual route against production during implementation.

```bash
TMP_HOME=$(mktemp -d)
printf 'demo db' > "$TMP_HOME/memory.db"
uv run python -m memory runtime backup --mirror-home "$TMP_HOME"
ls "$TMP_HOME/backups"
```

Verify the archive:

```bash
BACKUP_ZIP=$(ls "$TMP_HOME"/backups/memory_*.zip | tail -1)
uv run python -m memory runtime backup --verify "$BACKUP_ZIP"
```

Expected observations:

- backup archive is created under the temporary home;
- archive contains `memory.db`;
- verification is read-only;
- output explains the manual recovery route;
- no production database or production backup directory is touched.
