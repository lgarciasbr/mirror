[< CV13.E2](../index.md)

# CV13.E2.S4 — Theme preference

**Status:** ✅ Done
**Epic:** CV13.E2 — Multi-Mirror and Preferences
**Release target:** v0.12.0

---

## User-visible outcome

The user can choose `system`, `light`, or `dark` color mode from Preferences, and the local web app applies and persists that choice for the active Mirror.

---

## Scope

- Extend web preferences with `theme`.
- Add theme to `/api/shell` and preference persistence.
- Add a guarded `POST /api/preferences/theme` endpoint.
- Add theme controls to the Preferences page.
- Apply theme immediately to the document root.
- Keep theme scoped to the active Mirror home.

---

## Non-goals

- No custom palettes.
- No per-journey themes.
- No OS integration beyond respecting `system` through CSS media queries.
- No identity/configuration mutation.

---

## Validation

See [test guide](test-guide.md).
