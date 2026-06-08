[< Story](index.md)

# Plan — CV16.DS0 Runtime Status Bar Foundation

## Boundary

This story implements explicit mode lifecycle and visible runtime orientation,
not Explorer Mode itself.

The current Pi extension already calls:

```bash
uv run python -m memory welcome --status-line
```

and renders the result through `ctx.ui.setStatus("mirror", ...)`. Today the
status line can render a compact identity and health marker, for example:

```text
◇ alisson-vale · ◌ Mirror Mode · ✓
```

The desired next shape is:

```text
◇ alisson-vale · Journey Name on ■ Builder Mode · ✓
```

The story should extend that existing status-line path instead of replacing the
Pi footer with a custom footer. Activation and deactivation are user-visible
semantics that may be triggered by the user or by Mirror. Rendering and clearing
are internal operations behind those semantics.

## Product Model

The mode lifecycle should answer: which operating lens is active, and when has
that lens been explicitly left?

The status bar should answer: who is this Mirror, where is it currently situated,
and which operating lens is active?

```text
Mirror identity: alisson-vale
Location: active journey
Lens: ◌ Mirror Mode, ■ Builder Mode now, △ Explorer Mode later
Health: ✓ or existing warning marker
```

Builder Mode is the first concrete explicit mode because it exists today. Mirror
Mode remains the default lens when journey context is active but no explicit
operating mode is set. Explorer Mode will reuse the same lifecycle and visible
slot later.

## Design Direction

### Source of truth

Prefer a small runtime-state record over inference from conversation text.

Candidate directions to inspect before implementation:

- existing session-scoped mirror state used by `mirror load --session-id`;
- current Builder Mode command path, especially `python -m memory build load <slug>`;
- `welcome --status-line` composition path;
- Pi extension status refresh timing.

The story should choose the smallest state surface that lets Builder Mode activate:

```json
{
  "active_journey": "explorer-mode",
  "active_mode": "Builder Mode"
}
```

and explicitly deactivate that state later without starting a new session and
without requiring network calls.

### Activation and deactivation

Mode lifecycle should be explicit at the semantic layer:

```text
activate mode
  set active_mode and active_journey

deactivate mode
  leave the current operating lens and remove active mode context
```

The user may request this in natural language, and Mirror may call the contained
operation when it determines the lens should change. The product should not
expose separate user concepts for `render status` or `clear status`; those are
internal implementation effects.

### Status-line composition

`welcome --status-line` should remain cheap and cache-oriented. It should include
mode context when available and fall back to the current compact line when not.

Candidate formatting:

```text
◇ alisson-vale · Explorer Mode on ■ Builder Mode · ✓
```

If the journey has a human title available cheaply, implementation may choose
the title instead of slug, but the first implementation should prefer stable,
low-risk data over expensive lookup.

### Pi extension refresh

The Pi extension already sets the Mirror status on startup. The implementation
should inspect whether Builder Mode activation happens inside a skill response
that can refresh the status line immediately. If not, the first slice may accept
that the status updates on the next status refresh, but the validation route
should make this explicit.

## Acceptance Behavior

```gherkin
Given no Mirror operating mode is active
When `uv run python -m memory welcome --status-line` runs
Then it prints the identity, default Mirror Mode, and health marker
And it does not include stale journey or explicit mode text
```

```gherkin
Given Builder Mode has been activated for `explorer-mode`
When `uv run python -m memory welcome --status-line` runs
Then it includes `Explorer Mode on ■ Builder Mode`
And it preserves the Mirror identity prefix and health marker suffix
```

```gherkin
Given Builder Mode has been activated for `explorer-mode`
When the active mode is explicitly deactivated
And `uv run python -m memory welcome --status-line` runs
Then it no longer includes `■ Builder Mode`
And it returns to `Explorer Mode on ◌ Mirror Mode`
```

```gherkin
Given Pi is running with the Mirror logger extension
When Builder Mode is activated for a journey
Then the footer status line can show the active journey and Builder Mode
Without replacing Pi's built-in footer
```

## Risks

### Stale mode state

A status bar that keeps showing Builder Mode after the user has left the journey
would be worse than no status. The implementation needs a clear lifecycle for
explicit mode deactivation, with internal clearing as a consequence, and a
separate fallback to Mirror Mode when journey context remains active.

### Overbuilding a mode registry

Explorer Mode will need mode state, but this story should not prematurely build
a general mode subsystem. The right move is a small state record with tests and a
clear revisit path.

### Runtime coupling

Pi has a footer status API. Other runtimes do not share that surface. Keep this
story Pi-focused while making the Python status-line data reusable later.

## Validation Route

- Unit tests for status-line composition with and without active mode context.
- A targeted CLI smoke using a disposable Mirror home:

```bash
uv run python -m memory welcome --status-line --mirror-home <tmp-home>
uv run python -m memory build load explorer-mode
uv run python -m memory welcome --status-line
uv run python -m memory mode deactivate
uv run python -m memory welcome --status-line
```

- Pi manual validation after implementation:
  - start Pi in this repository;
  - activate Builder Mode for a journey;
  - confirm the footer includes Mirror identity, active journey, Builder Mode,
    and health marker;
  - explicitly deactivate the active mode;
  - confirm the footer no longer includes stale Builder Mode text and returns to
    Mirror Mode when journey context remains active.

## Documentation Updates

If implemented, update:

- `REFERENCE.md` if status-line behavior or mode-state commands become public;
- `docs/product/specs/runtime-interface/index.md` if runtime status expectations change;
- this story's `test-guide.md` with exact validation commands;
- CV16 index status when the story closes.
