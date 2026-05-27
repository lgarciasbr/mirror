[< CV13.E6](../index.md)

# CV13.E6.S7 — Run console surface polish

**Status:** ✅ Done
**Epic:** CV13.E6 — Async Operations and Agentic Web Console
**Release target:** v2.0

---

## User-visible outcome

Starting an operation opens a dedicated run console surface: a large shell-like output area dominates the page, while compact side cards show run metadata, safety boundaries, and actions. The surface feels like watching work unfold, even though this release still uses polling rather than true streaming.

---

## Scope

- Add a run console view for an active or recent run.
- Render output, lifecycle events, and result evidence in a dominant console panel.
- Move operation metadata, run id, status, risk, and actions into side cards.
- Preserve existing operation catalog and history navigation.
- Show future agent input affordance only as bounded/disabled prototype UI.

---

## Non-goals

- No SSE/WebSocket yet.
- No arbitrary command input.
- No real interactive agent chat loop.
- No new backend capability beyond UI shaping.

---

## Validation

Focused web tests plus ruff, node syntax, diff checks, and browser validation.
