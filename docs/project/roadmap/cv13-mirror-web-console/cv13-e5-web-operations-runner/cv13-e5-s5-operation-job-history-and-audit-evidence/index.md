[< CV13.E5](../index.md)

# CV13.E5.S5 — Operation job history and audit evidence

**Status:** ✅ Done
**Epic:** CV13.E5 — Web Operations Runner
**Release target:** v0.15.0

---

## User-visible outcome

Every web operation run leaves a local audit record with operation id, status, outcome, timestamps, sanitized parameters, summary, result evidence, and error detail when applicable.

---

## Scope

- Add persistent operation run history in the selected Mirror database.
- Record started/completed/failed timestamps for each operation request.
- Store operation id, status, outcome, sanitized parameters, summary, result payload, and error message.
- Return `runId` from `POST /api/operations/run`.
- Add a read-only API endpoint for recent operation runs.
- Record failed validation/execution attempts when an operation id is known and the request is safe to audit.
- Keep current execution synchronous.

---

## Non-goals

- No background worker.
- No streaming.
- No cancellation.
- No retry.
- No UI surface yet.
- No operation scheduling.
- No arbitrary log ingestion.

---

## Validation

See [test guide](test-guide.md).
