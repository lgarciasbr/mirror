[< CV20.DS12](../index.md)

# CV20.DS12.US2 — Route Builder To Canonical Refinement Files

**Status:** 🟡 Planned
**Type:** User Story

---

## Outcome

When a trusted project contains `docs/project/refinement/index.md`, Builder treats that
file as the Refinement entry point and does not route ordinary Refinement requests to
the SQLite Workbench. Projects without the file retain the shipped legacy behavior.

## Acceptance Behavior

```text
Given a trusted project with docs/project/refinement/index.md
When the Navigator asks to inspect, capture, select, or continue Refinement Work
Then Builder reads and follows the canonical project documents
And it does not invoke SQLite Workbench commands for that request

Given a project without the canonical index
When the same request is made
Then existing legacy Workbench guidance remains available
```

## Scope

- Define file-first versus legacy routing in the Builder skill contract.
- Update operational reference documentation to describe the authority check.
- Preserve explicit Navigator control over file mutations and lifecycle transitions.
- Validate natural-language inspection and one bounded file-first action without SQLite.
- Keep routing based on the explicit canonical relative path, not prose discovery.

## Out Of Scope

- Changing Python or TypeScript Workbench commands, storage, schemas, or migrations.
- Reading, exporting, reconciling, freezing, or deleting legacy rows.
- Dual-writing files and SQLite.
- Adding a parser, watcher, projection, synchronization, or handoff protocol.
- Implementing CR001, CR002, or CR004.

## Validation

In a project with the canonical index, Builder can inspect the backlog and explain the
next file-first action without touching SQLite. In a fixture/project without the index,
the existing legacy route remains documented and available.

## Done Condition

The routing contract and user-facing reference agree, the file-enabled project follows
its canonical Workbench, legacy compatibility is preserved elsewhere, and no runtime or
data migration is introduced.
