[< CV13.E5](../index.md)

# CV13.E5.S6 — Operations Runner surface

**Status:** ✅ Done
**Epic:** CV13.E5 — Web Operations Runner
**Release target:** v0.15.0

---

## User-visible outcome

The web app exposes an Operations page where the user can inspect runnable maintenance operations, run safe operations with explicit parameters, review results, and see recent audit history.

---

## Scope

- Add an Operations tab to the web navigation.
- Render the operation catalog with clear status, risk, dry-run, and parameter information.
- Expose forms for the currently runnable operations: runtime health, database backup, and conversation journey repair.
- Keep dry-run as the default for conversation repair.
- Show operation results and errors inline.
- Show recent operation audit records from `GET /api/operations/runs`.
- Stop for manual browser validation.

---

## Non-goals

- No streaming.
- No background jobs.
- No cancellation.
- No restore/download/delete backup.
- No arbitrary operation runner.
- No low-confidence repair UI.

---

## Validation

See [test guide](test-guide.md).
