[< CV13.E3](../index.md)

# CV13.E3.S1 — Configuration overview

**Status:** ✅ Done
**Epic:** CV13.E3 — Configuration Console
**Release target:** v0.13.0

---

## User-visible outcome

The user can open a Configuration page and see a read-only, non-sensitive overview of the active local Mirror's paths and runtime defaults.

---

## Scope

- Add a read-only configuration overview model.
- Expose `/api/configuration/overview`.
- Add a Configuration tab/page to the web shell.
- Show active Mirror home, database, preferences, backups, exports, transcripts, extensions, and non-sensitive runtime defaults.
- Mark filesystem paths as found/missing where applicable.

---

## Non-goals

- No secret display.
- No environment variable inventory yet.
- No editing.
- No journey metadata inspection yet.
- No raw `.env`, YAML, or database mutation.

---

## Validation

See [test guide](test-guide.md).
