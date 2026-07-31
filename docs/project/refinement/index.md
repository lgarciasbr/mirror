[< Project roadmap](../roadmap/index.md)

# Refinement Workbench

This index is the canonical project record for Refinement Story and Change Request
backlog status. Linked documents preserve context and evidence; they do not own status.
If a linked document and this index disagree, this index wins.

## Current Focus

- Refinement Story: [RS001 — Ariad Runtime Trust](rs001-ariad-runtime-trust/index.md)
- Change Request: [CR001 — Make Scope Confirmation An Honest Checkpoint](rs001-ariad-runtime-trust/cr001-scope-confirmation-checkpoint.md)

Selecting a focus is an explicit project decision. Reading this file never selects or
executes work.

## Refinement Stories

| Order | ID | Story | Status |
|------:|----|-------|--------|
| 1 | [RS001](rs001-ariad-runtime-trust/index.md) | Ariad Runtime Trust | active |

## Change Requests

Open work is ordered intentionally. Terminal history follows open work.

| Order | ID | RS | Change | Status |
|------:|----|----|--------|--------|
| 1 | [CR001](rs001-ariad-runtime-trust/cr001-scope-confirmation-checkpoint.md) | RS001 | Make scope confirmation an honest checkpoint | planned |
| 2 | [CR002](rs001-ariad-runtime-trust/cr002-cursor-sync-roadmap-selection.md) | RS001 | Refuse ambiguous roadmap selection during cursor sync | captured |
| — | [CR003](rs001-ariad-runtime-trust/cr003-surface-materialization-truth.md) | RS001 | Make artifact materialization surfaces truthful | done |

## Status Vocabulary

Refinement Story:

```text
proposed | active | parked | closed
```

Change Request:

```text
captured | planned | in_progress | blocked | validated | done | parked | rejected | promoted
```

Detailed phase history belongs in the CR document. The index records only the current
canonical status.

## Artifact Convention

- IDs are stable, project-wide `RSNNN` and `CRNNN` identifiers.
- IDs do not encode a journey, database, person, absolute path, or runtime display code.
- Existing database display codes are not imported and do not define these IDs.
- Each RS owns one directory and one `index.md`.
- Each CR is one evolving Markdown document inside its RS directory.
- Separate `artifacts/` files are optional and exist only when they add information.
- Empty files for lifecycle phases are not created.
- Git owns history, collaboration, conflict resolution, and recovery.
- No document grants commit, push, merge, publication, or release authority.
