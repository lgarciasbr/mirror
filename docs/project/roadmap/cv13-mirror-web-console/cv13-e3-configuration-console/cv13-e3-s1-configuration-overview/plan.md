[< Story](index.md)

# Plan — CV13.E3.S1 Configuration overview

## Implementation plan

1. Add a read-only web configuration overview model.
2. Keep S1 non-sensitive: paths and runtime defaults only, no secret/env inventory.
3. Expose `/api/configuration/overview` for the active Mirror.
4. Add a Configuration tab to the web shell.
5. Render sections and path found/missing status.
6. Add focused tests for model and route serialization.

## Design boundaries

- S1 is read-only.
- Secrets are excluded, not masked; masking belongs to S2.
- Editing belongs to later E3 stories.
