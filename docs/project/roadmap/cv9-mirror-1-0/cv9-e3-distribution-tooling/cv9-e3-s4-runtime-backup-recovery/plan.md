[< Story](index.md)

# Plan — Runtime Backup and Recovery Prerequisite

## Design Intent

This story makes backup/recovery explicit before any self-update command mutates code or data. The goal is not automatic rollback yet. The goal is a verified recovery route that a future update command can depend on.

The key distinction: backup creation is already implemented; backup readiness for self-update is not yet a runtime contract.

## Current Code Shape

`src/memory/cli/backup.py` already exposes `backup(...)` and `python -m memory backup`.

Current behavior:

- derives `memory.db` and backup dir from config or explicit `mirror_home`;
- creates a `memory_YYYYMMDD_HHMMSS.zip` archive;
- includes `memory.db`;
- includes `memory.db-wal` and `memory.db-shm` when present;
- removes backups older than `RETENTION_DAYS`;
- returns `None` when the database is missing.

Runtime self-update code currently lives in `src/memory/cli/runtime.py` and dry-run reports that backup is required before a future real update.

## Proposed Shape

Add a small runtime-facing backup prerequisite surface under the runtime CLI, most likely:

```bash
uv run python -m memory runtime backup --mirror-home PATH
uv run python -m memory runtime backup --verify PATH_TO_BACKUP.zip
```

Alternative: enhance `memory backup` directly and let runtime update call it later. The preferred route is to keep the existing `memory backup` command stable and add runtime-facing orchestration in `memory runtime backup`, because the self-update path belongs to runtime operations.

The runtime backup command should call the existing `backup()` implementation rather than duplicate archive creation.

## Backup Contract

A runtime backup archive for self-update contains:

- `memory.db`, always;
- `memory.db-wal`, when present;
- `memory.db-shm`, when present.

It does not contain:

- the git checkout;
- virtualenvs;
- caches;
- extension source repositories outside `MIRROR_HOME`;
- runtime session transcripts outside the database.

The command output should state this boundary clearly.

## Verification Contract

Backup verification should inspect an existing zip without extracting it into the Mirror home.

Minimum checks:

- file exists;
- file is a readable zip;
- archive contains `memory.db`;
- archive entries do not contain absolute paths or parent-directory traversal;
- optional sidecars, if present, are named `memory.db-wal` and `memory.db-shm`.

A verified backup does not prove semantic database integrity. It proves the recovery artifact is structurally usable.

## Manual Recovery Route

Document the manual route in command output or REFERENCE:

1. Stop active runtime sessions that could write to the database.
2. Move current `memory.db`, `memory.db-wal`, and `memory.db-shm` aside.
3. Extract `memory.db` and sidecars from the chosen backup zip into the Mirror home.
4. Run `uv run python -m memory runtime status --mirror-home PATH`.
5. If status is not ready, do not retry update execution before investigating.

This story should not implement automatic restore. Restore is dangerous enough to deserve a later explicit story if needed.

## Tests

Add focused tests for the new runtime backup surface, likely in `tests/unit/memory/cli/test_runtime.py` or a new `tests/unit/memory/cli/test_runtime_backup.py`.

Test cases:

- runtime backup creates a zip using explicit `mirror_home`;
- created backup verifies successfully;
- verification fails for missing file;
- verification fails for non-zip file;
- verification fails when `memory.db` is absent;
- verification rejects absolute or parent-traversal archive entries;
- missing database returns non-zero and does not create a backup directory;
- existing `memory backup` unit tests still pass.

Use temporary directories and never production `MIRROR_HOME`.

## Documentation

Update:

- `REFERENCE.md` runtime section;
- maybe `python -m memory` usage in `src/memory/__main__.py`;
- this story's `test-guide.md` with actual commands;
- `docs/process/worklog.md` after completion;
- `mirror-self-update` journey after completion.

## Risks and Boundaries

The main risk is false reassurance. Verification should be described as structural, not as proof that the database is semantically healthy.

The second risk is accidental restore behavior. This story must not overwrite a live database. Any recovery route remains manual documentation unless a future story explicitly implements restore with stronger safeguards.

The third risk is command proliferation. If implementation shows that `memory backup` can satisfy the runtime contract cleanly with small additions, prefer that over adding a redundant command. The deciding criterion is clarity for the future `runtime update` executor.
