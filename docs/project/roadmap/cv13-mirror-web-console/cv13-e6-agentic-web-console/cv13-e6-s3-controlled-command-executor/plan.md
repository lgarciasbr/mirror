[< Story](index.md)

# Plan — CV13.E6.S3 Controlled command executor

## Intent

Introduce the command-shaped execution substrate needed by future operations and agent runs while preserving the central boundary: the browser never supplies commands. Code owns every argv, cwd, environment choice, timeout, and output policy.

## Implementation outline

- Add a small `ControlledCommand` / `CommandResult` module under the web operations boundary.
- Execute with `subprocess.run(..., shell=False)` and a fixed argv supplied by server code.
- Use a sanitized environment allowlist and an explicit cwd.
- Enforce timeout and output truncation.
- Add tests proving successful capture, timeout/failure behavior, output bounding, and no shell-string interface.
- Add a read-only `runtime-diagnose` operation that runs `python -m memory runtime diagnose` for the selected Mirror home through the executor.
- Surface command evidence through existing operation result cards/raw evidence and lifecycle timeline.

## Risks

- The executor name can suggest a generic web terminal. Keep API internal and code-owned.
- Captured output may leak too much environment detail. Use a conservative command and bounded output.
- Runtime diagnosis may return non-zero when attention is needed; the operation should treat that as captured diagnostic evidence, not necessarily a web server failure.

## Documentation impact

- Mark S3 done after validation.
- Update E6 epic story table.
- Add a worklog entry after validation.
