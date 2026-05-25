[< CV13.E2](../index.md)

# CV13.E2.S3 — Profile/preferences page

**Status:** ✅ Done
**Epic:** CV13.E2 — Multi-Mirror and Preferences
**Release target:** v0.12.0

---

## User-visible outcome

The user has a dedicated Preferences page scoped to the active Mirror, showing the current local Mirror context and allowing basic web-profile preferences to be saved locally.

---

## Scope

- Add a Preferences perspective/tab to the local web shell.
- Show active Mirror name, path, and discovered Mirror count.
- Add basic web-profile preferences: display name and avatar symbol.
- Persist profile preferences in the active Mirror home under `web/preferences.json`.
- Reflect saved display name/avatar in the header without changing identity data.
- Keep theme preference for S4.

---

## Non-goals

- No identity graph/profile mutation.
- No theme preference yet.
- No remote sync or authentication.
- No arbitrary path input.
- No Mirror creation/deletion/repair.
- No LLM calls.

---

## Validation

See [test guide](test-guide.md).
