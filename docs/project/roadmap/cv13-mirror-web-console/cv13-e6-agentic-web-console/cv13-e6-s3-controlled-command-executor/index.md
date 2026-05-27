[< CV13.E6](../index.md)

# CV13.E6.S3 — Controlled command executor

**Status:** ✅ Done
**Epic:** CV13.E6 — Async Operations and Agentic Web Console
**Release target:** v2.0

---

## User-visible outcome

The web operations layer can run a server-owned command-like operation without exposing a browser shell. The user sees captured command evidence through the same asynchronous run and timeline model introduced in S1 and S2.

---

## Scope

- Add a controlled command executor for code-owned commands only.
- Enforce fixed argv, controlled cwd, sanitized environment, timeout, captured stdout/stderr, and bounded output.
- Add one read-only operation that uses the executor as proof of the boundary.
- Record command evidence in the existing operation result and run timeline.
- Keep operation parameters validated by the existing operation catalog.

---

## Non-goals

- No user-supplied command strings.
- No arbitrary shell access.
- No shell=True.
- No runtime update, git mutation, extension install, migration execution, or destructive command.
- No cancellation semantics.
- No approval checkpoints.
- No Pi/headless agent integration.

---

## Validation

See [test guide](test-guide.md).
