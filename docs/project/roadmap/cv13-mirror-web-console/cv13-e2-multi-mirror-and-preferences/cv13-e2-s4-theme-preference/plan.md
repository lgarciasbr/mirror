[< Story](index.md)

# Plan — CV13.E2.S4 Theme preference

## Implementation plan

1. Add `theme` to `WebPreferenceStore` with valid values `system`, `light`, and `dark`.
2. Serialize theme through `/api/shell`.
3. Add `POST /api/preferences/theme` validation and persistence.
4. Apply theme to `document.documentElement.dataset.theme`.
5. Add theme radio controls to Preferences.
6. Add tests for defaults, persistence, invalid values, shell serialization, and endpoint behavior.

## Design boundaries

- `system` means no forced light/dark override; CSS media query decides.
- Theme is a web preference only.
- Preferences remain scoped to the active Mirror home.
