[< Story](index.md)

# Plan — CV13.E2.S2 Switch local Mirror

## Implementation plan

1. Extend the Mirror registry with safe lookup by discovered Mirror name.
2. Keep active Mirror state inside the web handler/server session.
3. Add `POST /api/mirrors/select` accepting only `{ "name": "..." }`.
4. Reject names that are not in the discovered local Mirror registry or do not have `memory.db`.
5. Make all surface API calls resolve the current active Mirror database at request time.
6. Turn selector options into buttons that select a Mirror and reload the active surface.
7. Add tests proving switching changes shell and surface data, while arbitrary paths/names are rejected.

## Design boundaries

- The browser never submits a path.
- The server validates against filesystem discovery every time.
- The server does not create or mutate Mirror homes.
- Selection is local to the running web server unless persistence is explicitly added later.
