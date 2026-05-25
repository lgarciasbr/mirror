[< Story](index.md)

# Plan — CV13.E2.S3 Profile/preferences page

## Implementation plan

1. Extend the web preference store with a small profile payload: display name and avatar symbol.
2. Add profile serialization to `/api/shell` and a guarded `POST /api/preferences/profile` endpoint.
3. Add a Preferences tab/page to the static web shell.
4. Render active Mirror context, local storage path, and a small profile form.
5. Save profile preferences locally and update the header after save.
6. Add tests for defaults, persistence, validation, shell serialization, and endpoint behavior.

## Design boundaries

- These are web preferences, not Mirror identity layers.
- Theme stays out of S3.
- Selection/switching behavior from S2 remains unchanged.
