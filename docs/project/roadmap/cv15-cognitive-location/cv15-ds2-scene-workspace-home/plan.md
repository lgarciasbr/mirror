[< Story](index.md)

# Plan — CV15.DS2 Scene Workspace Home

## Boundary

DS2 is the interpretive layer on top of DS1. DS1 organized journeys
hierarchically; DS2 uses that hierarchy to return cognitive location.

Scene is a surface, not a new persisted object. The user still creates and edits
journeys. Mirror composes Scene from existing data.

## Product Model

```text
Data primitive: Journey
Relationship: parent_journey
Surface: Scene
Meaning: cognitive location
Synthesis: grounded orientation
```

Global Scene answers: where is my attention distributed across the whole field?

Focused Scene answers: where am I inside this selected journey, and what larger
or nearby journeys give it context?

## Design

### Deterministic read model

Add a Scene read model to Workspace rather than letting the browser infer
meaning from generic sections. The read model should be JSON-serializable and
bounded.

Candidate shape:

```json
{
  "mode": "global | focused",
  "selectedJourneyId": "mirror-mind",
  "journeyMap": [
    {
      "id": "mirror-mind",
      "title": "Mirror Mind",
      "status": "active",
      "horizon": "...",
      "children": [...],
      "movement": {
        "conversationCount": 12,
        "memoryCount": 4,
        "taskCount": 2,
        "recentConversationTitles": ["..."]
      }
    }
  ],
  "locationPath": ["mirror-mind", "mirror-web-console"],
  "nearbyJourneys": [...],
  "signals": [...],
  "synthesis": {
    "state": "generated | unavailable | missing | stale | not_run",
    "outdated": false,
    "orientation": {
      "title": "...",
      "summary": "...",
      "signals": ["..."],
      "next": "..."
    }
  }
}
```

The first implementation can live inside the existing Workspace read model under
a `scene` metadata field or a dedicated `SceneSummary` dataclass. Prefer the
smallest typed surface that keeps API and UI explicit.

### Synthesis

Add an intelligence function such as `generate_scene_synthesis(scene_model)`.
The function receives only the bounded deterministic read model. It returns a
structured orientation: title, summary, grounded signals, and next movement.

Prompt boundaries:

- Use only provided signals.
- Do not invent journeys, emotions, priorities, facts, or goals.
- Name uncertainty when signals are thin.
- Prefer meaning over metrics.
- Keep output compact.
- Mention whether the scene is global or focused.
- Return parseable JSON for the structured orientation.

Failure behavior:

- If OpenRouter/API is unavailable, return an unavailable state and deterministic
  fallback copy.
- If the model call fails, Scene still renders a manual invocation fallback.
- Saved orientations are marked outdated when the Scene source hash changes.

### Web UI

Workspace should lead with Current Scene:

- Global Current Scene appears when no journey is explicitly selected.
- Focused Current Scene appears as the first selected-journey tab.
- The existing Journey Map/sidebar remains navigation under Your Journeys.
- Your Moment contains Current Scene, Conversations, and All journeys.
- Scene shows structured orientation synthesis and grounded orientation signals.
- Conversations renders as a compact global list inside the Workspace shell.
- All journeys renders broad journey cards with parent/child status indicators.

### Existing Workspace sections

The current Briefing, Attachments, Conversations, Memories, Decisions, and
Settings sections remain available for selected journeys. DS2 should not remove
or rewrite the existing detail tabs unless necessary for the Scene home to make
sense.

## Risks

### Over-interpretation

Scene can feel magical or invasive if the LLM invents meaning. Mitigation:
bounded read model, explicit source signals, and no hidden mutation.

### Latency and cost

A synthesis call on every Workspace load could make the console slow or costly.
Mitigation: the Workspace read model never blocks on the LLM. Global Current
Scene may auto-generate only when no orientation exists; focused journey
orientations are always user-invoked. Saved orientations are reused until the
user refreshes them.

### Ambiguous global selection

The current Workspace tends to auto-select a journey. Scene needs a true global
home. Mitigation: distinguish default Workspace load from explicit journey
selection and preserve selected journey only when chosen.

## Implementation Slices

1. Scene deterministic read model with tests and no LLM.
2. Workspace UI rendering for global and focused Scene.
3. Bounded structured LLM synthesis function and tests with mocked model call.
4. Persisted orientation cache, outdated states, and fallback/manual invocation.
5. Release note/version packaging for v0.21.0 after validation.

## Validation Route

See [Test Guide](test-guide.md).
