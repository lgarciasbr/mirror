[< Story](index.md)

# Plan — CV16.DS1 Mode Transition Surface

## Boundary

This story adds a visible transition surface when modes change. It does not
change mode lifecycle semantics. DS0 already owns activation, deactivation, and
status-line state.

The transition surface is conversational confirmation. The status bar is
persistent orientation.

## Implementation Direction

### Shared rendering helper

Create a small Python rendering helper for mode transition surfaces. Keep it
plain-text and runtime-neutral so skills can print it in Pi, Gemini, Codex, and
Claude Code.

Candidate module:

```text
src/memory/surfaces/mode_transition.py
```

Candidate helpers:

```text
render_mirror_mode_transition(...)
render_builder_mode_transition(...)
render_explorer_mode_transition(...)
```

Avoid a generic abstraction until duplication proves painful. The three modes
have different information needs.

### Mirror Mode data

Mirror Mode surface needs:

- identity name, from Mirror home name;
- active journey, when resolved;
- persona examples and total remaining personas.

Persona examples should be deterministic. Prefer the first few persona identity
rows ordered by key, unless a better existing ordering is available. The copy
should read:

```text
when the topic asks: persona_1, persona_2, persona_3 and N more available
```

If there are three or fewer personas, omit the remaining count.

### Builder Mode data

Builder Mode surface needs:

- active journey slug;
- journey path or stage/current focus extracted from journey identity content;
- project path when present;
- a short briefing or synthesis extracted from journey identity content.

The first implementation should use deterministic extraction, not an LLM call.
Use existing journey content sections such as `Stage`, `Description`, or
`Briefing`, and truncate the briefing to a compact paragraph.

### Explorer Mode data

Explorer Mode surface can remain minimal:

- active journey slug;
- what this mode is;
- boundary: `Explorer preserves uncertainty.`

Refine later when Explorer state, signal radar, and story thickening exist.

### Persona icon

Replace persona activation display that currently uses the Mirror identity
symbol with:

```text
✦ persona-name
```

This applies at least to Mirror Mode activation banners. Broader persona-rendering
surfaces can follow if found during implementation.

## Acceptance Behavior

```gherkin
Given Mirror Mode is activated with a resolved journey
When the load command renders
Then the output includes a Mode Transition Surface for `◌ Mirror Mode`
And it shows the active identity and active journey
And it shows persona-routing examples with an available count
```

```gherkin
Given Builder Mode is activated for a journey with project_path and briefing
When the build load command renders
Then the output includes a Mode Transition Surface for `■ Builder Mode`
And it shows the active journey, project path, and compact briefing
```

```gherkin
Given Explorer Mode is activated for a journey
When the explore load command renders
Then the output includes a minimal Mode Transition Surface for `△ Explorer Mode`
And it does not claim full Explorer persistence or story-thickening state
```

```gherkin
Given a persona is activated
When the activation banner renders
Then it uses `✦` for the persona instead of `◇`
```

## Validation Route

Automated:

```bash
uv run pytest \
  tests/unit/memory/surfaces/test_mode_transition.py \
  tests/unit/memory/skills/test_mirror.py \
  tests/unit/memory/cli/test_build.py \
  tests/unit/memory/cli/test_explore.py
```

Lint:

```bash
uv run ruff check src/memory/surfaces/mode_transition.py src/memory/skills/mirror.py src/memory/cli/build.py src/memory/cli/explore.py tests/unit/memory/surfaces/test_mode_transition.py
```

Manual smoke:

```bash
uv run python -m memory mirror load --journey explorer-mode --query "test mirror mode surface"
uv run python -m memory build load explorer-mode
uv run python -m memory explore load explorer-mode
```

Expected: each command prints the appropriate transition surface.

## Risks

### Surface too verbose

Mode transition should orient, not become a second welcome card. Keep copy compact
and mode-specific.

### Persona list noise

Showing every persona would be noisy. Show a few examples and a remaining count.

### Builder briefing extraction drift

Journey documents vary. Use tolerant section extraction and fall back to a short
content excerpt when expected headings are missing.
