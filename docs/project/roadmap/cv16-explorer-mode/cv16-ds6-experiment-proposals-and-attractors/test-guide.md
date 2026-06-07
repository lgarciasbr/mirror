[< Story](index.md)

# Test Guide — CV16.DS6 Experiment Proposals and Attractors

## Automated Verification

```bash
uv run pytest \
  tests/unit/memory/services/test_explorer_story.py \
  tests/unit/memory/surfaces/test_explorer_story.py \
  tests/unit/memory/cli/test_explore.py
```

Expected: all tests pass.

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

Expected: all checks pass.

## Technical Smoke for Driver

The Driver may run CLI smoke tests after implementation, but those are not the Navigator's manual validation. They should prove only that contained operations work.

Candidate technical smoke:

```bash
uv run python -m memory explore story attractors explorer-mode \
  --attractor "External validation before internal modeling" \
  --description "The story pulls toward validating behavior in Pi before adding more internal structure."

uv run python -m memory explore story experiment explorer-mode \
  --title "Validate attractor in Pi" \
  --description "Ask for the attractor, correct it, ask for a small experiment, and request a snapshot."

uv run python -m memory explore story snapshot explorer-mode
```

Expected: outputs include `△ ATTRACTORS EMERGING`, `△ EXPERIMENT PROPOSAL`, and a snapshot containing both.

## User Validation in Pi

The Navigator validates DS6 as a user in Pi, without running internal commands.

Activate Explorer Mode:

```text
/mm-explore explorer-mode
```

Open or thicken an Exploratory Story:

```text
Vamos explorar a ideia de que o Explorer precisa apontar para experimentos pequenos antes de virar Builder.
```

Expected: the assistant renders `△ EXPLORATORY STORY OPENED` or `△ STORY THICKENED`.

Ask for the attractor:

```text
qual é o attractor dessa história?
```

Expected:

- the assistant renders `△ ATTRACTORS EMERGING`;
- attractor is tentative, e.g. “um attractor possível”;
- no Builder activation happens.

Correct the attractor:

```text
não é bem isso. O attractor é validação externa antes de modelagem interna.
```

Expected:

- the assistant updates the attractor visibly;
- it does not preserve a conflicting old attractor as if both were equally current.

Ask for an experiment:

```text
que experimento pequeno testa esse attractor?
```

Expected:

- the assistant renders `△ EXPERIMENT PROPOSAL`;
- proposal is small, concrete, and exploratory;
- it does not switch to Builder.

Ask for the field:

```text
me mostra o campo narrativo atual
```

Expected:

- the assistant renders `△ NARRATIVE FIELD SNAPSHOT`;
- snapshot includes story, attractor, and experiment proposal.

Cleanup if this was only validation:

```text
sair do modo explorador
/mm-discard
```

## Pass Condition

Explorer Mode can name and store a visible attractor, update it when corrected, propose a small experiment, and include both in the Narrative Field Snapshot without hidden detection or silent Builder promotion.
