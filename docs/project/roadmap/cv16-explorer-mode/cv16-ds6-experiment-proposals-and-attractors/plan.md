[< Story](index.md)

# Plan — CV16.DS6 Experiment Proposals and Attractors

## Boundary

This story adds directional structure to an existing Exploratory Story. It does not detect attractors invisibly, does not call an LLM from Python, does not create durable Explorer persistence, and does not activate Builder.

Attractors and experiments are stored only when they are surfaced in the conversation through contained operations. The assistant may infer them conversationally, but the persistence boundary is visibility: if it was not shown to the user, it should not be stored.

## State Model

Extend `src/memory/services/explorer_story.py` with small value objects:

```python
@dataclass(frozen=True)
class ExplorerAttractor:
    label: str
    description: str | None = None
    status: str = "proposed"

@dataclass(frozen=True)
class ExplorerExperimentProposal:
    title: str
    description: str | None = None
    status: str = "proposed"
```

Extend `ExplorerStory`:

```python
attractors: tuple[ExplorerAttractor, ...] = ()
experiment_proposal: ExplorerExperimentProposal | None = None
```

Store them in the existing runtime-session metadata payload for `__explorer_story__:<journey>`. No migration is needed because the payload is JSON metadata.

Status values for DS6:

```text
proposed
accepted
```

Avoid `rejected` unless needed. Correction can replace the proposed attractor.

## Service Operations

Add or extend service functions:

```python
set_explorer_attractors(store, journey, attractors: list[ExplorerAttractor]) -> ExplorerStory
set_explorer_experiment_proposal(store, journey, proposal: ExplorerExperimentProposal) -> ExplorerStory
```

Semantics:

- Attractors replace the current attractor list for DS6. This avoids hidden accumulation.
- Experiment proposal replaces the current proposal.
- Existing story, summary, and last card are preserved.
- Missing story state can still accept attractors, but the surface should make clear that no story text exists yet.
- JSON reads tolerate older DS4 payloads with no attractor fields.

## CLI Operations

Extend `python -m memory explore story`:

```bash
uv run python -m memory explore story attractors explorer-mode \
  --attractor "External validation" \
  --description "The story is pulling toward validating behavior in Pi, not only CLI." \
  --status proposed

uv run python -m memory explore story experiment explorer-mode \
  --title "Validate DS5 in Pi" \
  --description "Open and thicken a story using natural language, then request a snapshot." \
  --status proposed
```

Keep the CLI minimal. Multi-attractor support can repeat `--attractor` and pair descriptions by order, or DS6 can support one attractor first. Prefer one attractor first unless implementation remains simple with repeated flags.

## Surfaces

Extend `src/memory/surfaces/explorer_story.py` with:

```python
render_attractors_emerging(story: ExplorerStory) -> str
render_experiment_proposal(story: ExplorerStory) -> str
```

Update `render_narrative_field_snapshot()` to include attractors and experiment proposal when present.

Surface copy should preserve uncertainty:

```text
△ ATTRACTORS EMERGING
possible attractor
...
status
proposed
```

```text
△ EXPERIMENT PROPOSAL
small experiment
...
boundary
This is not Builder delivery until confirmed.
```

## Skill Contract

Update `.pi/skills/mm-explore/SKILL.md`:

- when the user asks for attractors, name a possible attractor, call `story attractors`, and render the returned surface;
- when the assistant sees a strong directional pull, it may propose one visibly with humble language;
- when the user corrects the attractor, replace it through `story attractors`;
- when the user asks “what experiment tests this?”, call `story experiment` and render the returned surface;
- do not promote to Builder in DS6.

## Tests

Add or extend service tests:

- older story payload with no attractors still loads;
- setting attractors preserves story fields;
- setting experiment proposal preserves attractors and story fields;
- replacing attractors avoids hidden accumulation;
- attractor and proposal status validation rejects unknown statuses if validation is implemented.

Add surface tests:

- attractors surface includes title, attractor label, description, and status;
- experiment proposal surface includes title, description, status, and no-Builder boundary;
- snapshot includes attractors and experiment when present.

Extend CLI tests:

- `story attractors` stores and renders attractor surface;
- `story experiment` stores and renders experiment surface;
- neither operation changes active mode to Builder.

## Validation Route

Automated:

```bash
uv run pytest \
  tests/unit/memory/services/test_explorer_story.py \
  tests/unit/memory/surfaces/test_explorer_story.py \
  tests/unit/memory/cli/test_explore.py
```

Lint:

```bash
uv run ruff check \
  src/memory/services/explorer_story.py \
  src/memory/surfaces/explorer_story.py \
  src/memory/cli/explore.py \
  tests/unit/memory/services/test_explorer_story.py \
  tests/unit/memory/surfaces/test_explorer_story.py \
  tests/unit/memory/cli/test_explore.py
```

## User Validation in Pi

The Navigator validates DS6 as a user in Pi, without running internal commands.

Start Explorer Mode:

```text
/mm-explore explorer-mode
```

Open or use an existing Exploratory Story:

```text
Vamos explorar a ideia de que o Explorer precisa apontar para experimentos pequenos antes de virar Builder.
```

Expected: `△ EXPLORATORY STORY OPENED` or `△ STORY THICKENED`.

Ask for the attractor:

```text
qual é o attractor dessa história?
```

Expected:

- assistant renders `△ ATTRACTORS EMERGING`;
- attractor is phrased as possible/proposed, not truth;
- no Builder activation happens.

Correct the attractor:

```text
não é bem isso. O attractor é validação externa antes de modelagem interna.
```

Expected:

- assistant renders `△ ATTRACTORS EMERGING` again or clearly updates the attractor;
- it does not accumulate a conflicting hidden attractor.

Ask for an experiment:

```text
que experimento pequeno testa esse attractor?
```

Expected:

- assistant renders `△ EXPERIMENT PROPOSAL`;
- proposal is small and exploratory;
- it explicitly does not switch to Builder.

Ask for the field:

```text
me mostra o campo narrativo atual
```

Expected:

- assistant renders `△ NARRATIVE FIELD SNAPSHOT`;
- snapshot includes current story, attractor, and experiment proposal.

Cleanup if the session was only validation:

```text
sair do modo explorador
/mm-discard
```

## Risks

### Attractor becomes a decision

Attractors are directional pulls, not commitments. Keep status visible and language tentative.

### Experiment becomes Builder planning

The experiment should be a learning move. DS7 owns Builder handoff after explicit confirmation.

### Too many attractors too soon

Start with one attractor if repeated flags make the interface noisy. Multiple attractors can follow once the single-attractor behavior proves useful.
