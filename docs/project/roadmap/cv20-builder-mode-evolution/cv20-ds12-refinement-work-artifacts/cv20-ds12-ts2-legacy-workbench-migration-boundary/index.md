[< CV20.DS12](../index.md)

# CV20.DS12.TS2 — Define Legacy Workbench Migration Boundary

**Status:** 🟡 Planned
**Type:** Technical Story

---

## Outcome

The project has one explicit decision for the existing CV20.DS6 SQLite Workbench: what
remains supported during transition, which authority is canonical, how existing data is
protected, and what evidence would justify export, deprecation, or removal.

## Acceptance Behavior

```text
Given project files now own canonical shared Refinement state
And production and TypeScript compatibility still recognize the SQLite Workbench
When the transition boundary is decided
Then files remain the sole canonical shared authority
And existing local data is neither silently migrated nor deleted
And runtime behavior during the transition is explicit
And any future migration is a separate, reversible story
```

## Scope

- Inventory the shipped SQLite tables, commands, surfaces, and TypeScript schema
  compatibility related to the Workbench.
- Distinguish current production compatibility from desired future authority.
- Compare bounded transition options: retain unchanged, freeze writes, offer explicit
  export, deprecate, or remove later.
- Record one decision, consequences, and triggers for future work.
- Capture conflicts with the document-first model as findings rather than fixing them.

## Out Of Scope

- Reading or transforming personal Workbench rows.
- Exporting, migrating, deleting, or reconciling production data.
- Removing migrations or TypeScript schema compatibility.
- Changing Builder commands, surfaces, storage, or lifecycle behavior.
- Implementing CR001, CR002, or CR004.

## Validation

A reviewer can determine from project documents which authority wins today, what legacy
behavior remains, what is prohibited, and what trigger permits a future migration.
Repository and documentation checks must remain clean; no source or database mutation is
allowed.

## Done Condition

The transition decision is explicit enough that subsequent work cannot accidentally
restore dual authority or delete legacy data, while leaving implementation for a later,
separately approved story.
