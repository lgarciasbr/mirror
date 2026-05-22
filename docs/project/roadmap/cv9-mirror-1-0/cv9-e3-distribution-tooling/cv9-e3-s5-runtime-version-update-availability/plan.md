[< Story](index.md)

# Plan - CV9.E3.S5 Runtime Version and Update Availability

## Design Direction

This story separates local version visibility from explicit remote discovery.

Local version visibility should be cheap and offline. Remote update availability should be an intentional network-facing operation, not something hidden inside `runtime status` or normal Mirror opening.

The command shape:

```bash
uv run python -m memory runtime version
uv run python -m memory runtime update --check
```

`runtime version` answers what is installed now. `runtime update --check` asks the configured remote whether a newer commit is available without fetching, changing refs, touching files, or touching the database.

## Boundary

`runtime update --dry-run` remains local-only. It uses local git refs and produces a plan from what the checkout already knows.

`runtime update --check` may contact the remote, but must remain read-only:

- no `git fetch`;
- no ref updates;
- no checkout/pull;
- no backup;
- no migrations;
- no database writes.

Use `git ls-remote`, not `git fetch`, for branch availability.

## Version Source

Use the existing runtime version logic as the installed version source:

- package metadata when installed;
- fallback to `pyproject.toml` through `package_version()`.

Render the installed version in `runtime version` and include git branch/commit when available. This gives both product version and exact source position.

## Update Availability Source

For this story, detect branch update availability from the configured upstream branch.

Implementation route:

1. Reuse `inspect_git_update_plan()` or its upstream resolution pieces to find the upstream name.
2. Resolve the upstream remote and branch:
   - `origin/main` -> remote `origin`, branch `main`.
   - if upstream shape is unexpected, report blocked/unknown.
3. Read remote URL:
   - `git config --get remote.<remote>.url`.
4. Query remote head without fetching:
   - `git ls-remote <remote> refs/heads/<branch>`.
5. Compare returned commit to local `HEAD`.

Classify:

- `up_to_date`: remote commit equals local commit.
- `update_available`: remote commit differs and local branch is not already ahead/diverged by local refs.
- `local_ahead`: local refs show ahead of upstream.
- `diverged`: local refs show ahead and behind.
- `no_upstream`: no upstream branch.
- `unknown`: remote query failed or output was not parseable.

This is intentionally branch-based, not release-based. GitHub releases or tags can be a later product layer once release publication is stable.

## Models

Add small dataclasses, likely in `memory.cli.runtime`:

```python
@dataclass(frozen=True)
class RuntimeVersionReport:
    version: str
    git: GitStatus

@dataclass(frozen=True)
class RuntimeUpdateAvailability:
    version: str
    upstream: str | None
    local_commit: str | None
    remote_commit: str | None
    status: str
    note: str | None = None
```

## Rendering

`runtime version`:

```text
Mirror runtime version

Version: 0.7.0
Repository: /path/to/mirror
Git branch: main
Git commit: abc1234
```

`runtime update --check` when up to date:

```text
Mirror runtime update check

Version: 0.7.0
Current: main @ abc1234
Upstream: origin/main @ abc1234
Availability: up to date

Next: no update needed
```

When remote differs:

```text
Mirror runtime update check

Version: 0.7.0
Current: main @ abc1234
Upstream: origin/main @ def5678
Availability: update available

Preview:
uv run python -m memory runtime update --dry-run
```

If blocked:

```text
Availability: blocked
Reason: branch has no upstream tracking branch
```

## Tests

Use monkeypatching for `_run_git`, not real network.

Targeted tests:

- `runtime version` renders version and git state.
- `runtime update --check` uses `ls-remote` and returns up to date when remote commit equals local commit.
- `runtime update --check` returns update available when remote commit differs and local refs are not ahead.
- no upstream blocks update check.
- ahead/diverged local refs block update check.
- malformed `ls-remote` output returns unknown.
- command dispatch exits 0 for up-to-date and update-available states, non-zero for blocked/unknown.

## Documentation

Update:

- `REFERENCE.md` command table and runtime section.
- `docs/project/roadmap/cv9-mirror-1-0/cv9-e3-distribution-tooling/index.md` status.
- `docs/process/worklog.md` after implementation.

## Open Follow-Up

Showing version on the normal Mirror opening surface is part of the acceptance criteria, but it may require touching the welcome/opening path. If that surface is more invasive than expected, split it into a follow-up inside the same story or explicitly record it as deferred before marking done.
