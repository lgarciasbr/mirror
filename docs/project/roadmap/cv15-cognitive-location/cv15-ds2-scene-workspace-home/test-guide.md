[< Story](index.md)

# Test Guide — CV15.DS2 Scene Workspace Home

## Automated Checks

Focused checks during development:

```bash
uv run pytest tests/unit/memory/surfaces/test_workspace.py tests/unit/memory/web/test_server.py tests/unit/memory/intelligence/test_scene.py -q
uv run ruff check src/memory/surfaces/workspace.py src/memory/intelligence/scene.py src/memory/web/server.py tests/unit/memory/surfaces/test_workspace.py tests/unit/memory/web/test_server.py tests/unit/memory/intelligence/test_scene.py
uv run ruff format --check src/ tests/
node --check src/memory/web/static/app.js
```

Before release packaging:

```bash
uv run pytest -q
uv run ruff check .
uv run ruff format --check src/ tests/
node --check src/memory/web/static/app.js
uv run python -m memory runtime release-notes latest
uv run python -m memory runtime release-doctor --target v0.21.0 --stable origin/stable
```

## Deterministic Scene Validation

Create an isolated test database with:

- one parent journey;
- two child journeys;
- recent conversations on both parent and child;
- recent memories and one decision;
- at least one task.

Expected:

- Workspace payload includes a Scene model.
- Global Scene includes all top-level journeys and child journeys.
- Focused Scene includes selected journey, parent when present, children when
  present, siblings when present, and movement signals for the selected journey.
- No child conversations are counted as parent conversations unless explicitly
  represented as aggregate/nearby signals.

## LLM Synthesis Validation

With model call mocked:

- Scene synthesis prompt receives only the bounded Scene read model.
- Prompt includes no raw database dump or full transcripts.
- Successful response is parsed into structured orientation fields.
- JSON wrapped in Markdown fences is repaired before rendering.
- Failed response returns fallback state and does not break Workspace rendering.
- Saved orientation is reused and marked outdated when the Scene source hash changes.

## Manual Browser Validation

Restart the web server after web changes:

```bash
~/restart-mirror-web.sh
```

Then validate:

1. Open Workspace without selecting a journey.
2. Confirm global Current Scene appears as the central home and does not auto-select the first journey.
3. Confirm first missing global orientation may generate automatically, then persists across navigation.
4. Confirm Journey Map/navigation remains usable under Your Journeys.
5. Open Conversations and All journeys; confirm both render inside the Workspace shell without hiding the sidebar.
6. Select a parent journey.
7. Confirm Current Scene appears as the first journey tab and does not silently absorb child content as its own.
8. Select a child journey.
9. Confirm focused orientation is manual-only and can be generated from the tab.
10. Create or change movement if practical and confirm an old orientation is marked Outdated.
11. Temporarily simulate synthesis failure if practical and confirm fallback rendering.

## Safety Checks

- Scene must not mutate journeys, conversations, memories, tasks, or settings.
- Scene must not change journey assignment.
- Scene must not change Builder Mode context.
- Scene must not introduce a user-managed Scene entity.
