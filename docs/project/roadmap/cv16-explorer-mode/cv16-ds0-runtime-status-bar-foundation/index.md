[< CV16](../index.md)

# CV16.DS0 — Runtime Status Bar Foundation

**Status:** ✅ Done  
**Placement:** CV16 enabling story, cross-mode foundation  
**User-visible outcome:** Mirror has explicit mode activation/deactivation semantics, and the Pi footer shows the active Mirror identity, active journey, active operating mode, and health marker in one compact status line.

---

## Why This Starts the Explorer Arc

Explorer Mode needs visible mode context. If the user enters an exploratory lens,
the runtime should make that lens obvious without requiring the user to remember
which skill was invoked two turns ago.

The same need already exists for Builder Mode. The status bar is therefore not
Explorer-specific behavior, but it is a necessary foundation for Explorer: before
adding another lens, Mirror should make the current lens visible.

This story belongs at the start of CV16 as an enabling cross-mode slice. It does
not implement Explorer Mode. It prepares Mirror to activate and deactivate
operating lenses explicitly, while the runtime shell renders the currently active
lens.

---

## Desired Shape

```text
◇ alisson-vale · Active Journey xxxx on ■ Builder Mode · ✓
```

The exact copy may be refined during implementation, but the user-visible shape
should preserve four elements:

```text
mirror identity · active journey + mode icon + mode · health marker
```

---

## Scope

- Define explicit mode activation and deactivation semantics that can be triggered by the user or by Mirror.
- Extend the existing Pi status-line path so it can include active journey and active mode.
- Preserve the existing identity and health marker behavior from `welcome --status-line`.
- Make Builder Mode activate enough mode context for the status line to render `■ Builder Mode`.
- Make mode deactivation clear the explicit mode context through an internal operation while preserving journey context for `◌ Mirror Mode` when applicable.
- Keep the first implementation Pi-focused for rendering, because Pi is the runtime where the footer status line exists today.
- Avoid creating Explorer state or Explorer activation behavior in this story.

---

## Non-goals

- No Explorer Mode implementation.
- No web status bar.
- No Claude/Gemini/Codex UI parity in this slice.
- No complex mode registry unless the implementation proves it is needed.
- No user-facing render or clear commands; rendering and clearing are internal operations behind explicit activation/deactivation.
- No automatic mode inference from arbitrary prompts.

---

## Acceptance Behavior

Given Pi is running with Mirror loaded, when no journey mode is active, the footer continues to show the compact Mirror identity and health marker.

Given Builder Mode is activated for a journey, when the Pi footer refreshes, it shows the active journey and `■ Builder Mode` between the Mirror identity and health marker.

Given the active mode is explicitly deactivated while journey context remains active, when the Pi footer refreshes, it shows the active journey on `◌ Mirror Mode` instead of stale Builder text.

Given the status-line command is run directly, when mode context is available, it prints the same compact state without requiring network calls or expensive maintenance.

---

## References

- [Plan](plan.md)
- [Test Guide](test-guide.md)
- [CV16 Explorer Mode](../index.md)
- [ES-003 Explorer Mode](../../../exploration/es-003-explorer-mode.md)
