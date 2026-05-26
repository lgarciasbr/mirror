[< Story](index.md)

# Plan — CV13.E5.S5 Operation job history and audit evidence

## Implementation plan

1. Add a core migration for an `operation_runs` table in the user's Mirror database.
2. Add a small storage/service layer for creating, completing, failing, and listing operation runs.
3. Wire the service into `MemoryClient`.
4. Update `POST /api/operations/run` to create a run record before executing known operations.
5. On success, mark the run completed with outcome, summary, and result payload.
6. On failure after a known operation id is parsed, mark the run failed with sanitized parameters and error message.
7. Return `runId` in the operation response.
8. Add `GET /api/operations/runs` for recent operation history, with a bounded limit.
9. Add tests for successful run audit, failed run audit, recent run listing, and parameter/result JSON serialization.

## Design boundaries

- This story introduces audit persistence, not asynchronous execution.
- The endpoint still executes synchronously and returns the operation result immediately.
- Parameters stored in audit records must be sanitized and limited to declared operation parameters. Unsupported request fields such as `command` are rejected before execution and should not store unsafe content.
- Result payloads may include local paths and conversation ids because this is a local operator audit trail, but no secrets or environment values should be introduced.
- Failed unknown operation ids can remain unaudited because there is no operation contract to attach them to. Failed known operations should be audited when possible.
- Existing operation behavior must remain unchanged apart from returning `runId`.

## Schema sketch

`operation_runs`:

- `id` text primary key,
- `operation_id` text not null,
- `status` text not null,
- `outcome` text,
- `parameters_json` text not null,
- `summary_json` text,
- `result_json` text,
- `error` text,
- `started_at` text not null,
- `completed_at` text,
- `created_at` text not null.

## Risks and mitigations

- Risk: audit records store unsafe request payloads. Mitigation: create records only with operation-owned validated parameters or sanitized parsed input.
- Risk: audit table becomes a job system accidentally. Mitigation: status lifecycle is synchronous only: running, completed, failed.
- Risk: result payloads grow too large. Mitigation: current operations return bounded structured evidence; future job/streaming story can introduce truncation if needed.

## Verification approach

- Unit tests use a temporary Mirror database and assert records are written.
- Endpoint tests assert `runId` is returned and recent runs are listed.
- Existing operation tests stay green.
- Manual validation is not required unless a visible surface is introduced.
