[< CV13.E2](../index.md)

# CV13.E2.S2 — Switch local Mirror

**Status:** ✅ Done
**Epic:** CV13.E2 — Multi-Mirror and Preferences
**Release target:** v0.12.0

---

## User-visible outcome

The user can select another discovered local Mirror from the header selector and the web surface reloads against that Mirror's local `memory.db`, without accepting arbitrary filesystem paths.

---

## Scope

- Add a guarded web endpoint for selecting a discovered Mirror by name.
- Validate selection against the server-side Mirror registry, not browser-provided paths.
- Update the active Mirror for the running web session.
- Refresh shell, Workspace, Identity, memory category, and search requests against the selected Mirror database.
- Mark the active Mirror in the selector after switching.
- Keep switching local-only and constrained to discovered Mirror homes with `memory.db`.

---

## Non-goals

- No arbitrary path input.
- No remote Mirror selection.
- No creation, deletion, migration, backup, or repair of Mirror homes.
- No identity/profile editing.
- No theme or avatar preference.
- No persistence guarantee across server restarts unless implemented safely without expanding scope.
- No LLM calls during switching.

---

## Validation

See [test guide](test-guide.md).
