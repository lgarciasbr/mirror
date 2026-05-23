[< CV9.E3 Distribution & Tooling](../index.md)

# CV9.E3.S17 — Fresh User Stable Update Smoke

**Epic:** CV9.E3 Distribution & Tooling  
**Status:** 🟡 Planned  
**User-visible outcome:** A fresh clone can update from an older stable release to the current stable release without manual git intervention, proving the self-update path works for a new user shape rather than only for the developer's production clone.

---

## Why

S13–S16 made stable updates release-aware, discoverable, preflighted, and promotable. The remaining proof is user-shaped: a fresh clone starting from an older stable release should be able to follow the documented stable self-update path and arrive at the new stable release safely.

This is a smoke story, not a new feature story. Its value is evidence.

## Scope

In scope:

- Define an isolated fresh-user stable update smoke procedure.
- Run it against a temporary clone and temporary Mirror home.
- Verify runtime version, channel, release notes, update check, dry-run, update execution, and post-update status where possible.
- Avoid touching the production clone or production database.
- Record findings, blockers, and exact commands.

Out of scope:

- Publishing a new release unless the Navigator explicitly decides to turn the current arc into a release candidate.
- Mutating the production clone.
- Repairing unrelated packaging or installer issues beyond small blockers required for the smoke.
- Automating a full release pipeline.

## Acceptance Criteria

- A temporary clone can be placed at an older stable release.
- The clone can be configured for the stable update channel.
- The smoke uses an isolated Mirror home and does not touch production data.
- `runtime update --check` sees the newer stable target when one exists.
- `runtime update --dry-run` explains the update path without mutation.
- `runtime update` can move the clone to the current stable release without manual git intervention when a newer stable exists.
- Post-update `runtime version`, `runtime status`, and `runtime release-notes latest` show the expected release state.
- If no newer stable release exists yet, the story records the gap and either pauses for release publication or converts into a reproducible smoke script/checklist.

## See also

- [CV9.E3.S16 Stable Promotion Execution Path](../cv9-e3-s16-stable-promotion-execution/index.md)
- [Runtime Self-Update Reference](../../../../../../REFERENCE.md#runtime-self-update)
- [Versioning](../../../../../process/versioning.md)
