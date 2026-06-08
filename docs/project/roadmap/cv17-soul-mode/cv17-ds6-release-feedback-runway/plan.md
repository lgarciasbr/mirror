[< Story](index.md)

# Plan — CV17.DS6 Pre-release Usage Adjustments, Packaging, And Feedback Runway

## Phase 1 — Usage Adjustment Pass

Use real Pi sessions to tune the first Soul Mode ritual before release.

Adjustment areas:

- Soul Mode activation and entry microcopy;
- living-field threshold for Possible Listenings;
- Self Voice depth and non-advisory behavior;
- Shadow Voice depth and non-punitive behavior;
- voice markers and rite surfaces;
- Fruit In Maturation timing and formulation quality;
- Harvested Fruit confirmation and journal-save boundary;
- Pi skill contract compliance for all required surfaces;
- Soul → Builder operational boundary for implementation, code, docs mutation, and release packaging requests.

Boundary: adjustment may change prompts, skill contracts, surface copy, renderer behavior, and tests. It should not expand scope into full Wisdom Voice, full Beauty Voice, Passagem curation, Return To Center, multi-fruit state, or rich UI.

Exit criterion:

```text
The full ritual can be completed in Pi without the Navigator needing to explain the grammar.
```

## Phase 2 — Packaging

After usage adjustments:

- mark CV17 stories done;
- update docs and command reference;
- update worklog;
- create release notes for `v0.24.0 — Soul Mode First Ritual`;
- bump version;
- run automated validation;
- run final Pi smoke route;
- document the post-release Closing Rite and psyche-enrichment runway;
- commit with a release-focused message.

## Validation Route

Automated:

```bash
uv run pytest tests/unit/memory/cli/test_soul.py tests/unit/memory/surfaces/test_soul.py tests/unit/memory/services/test_soul.py tests/unit/memory/surfaces/test_mode_transition.py tests/unit/memory/cli/test_welcome.py -q
uv run ruff check src/memory/cli/soul.py src/memory/surfaces/soul.py src/memory/services/soul.py tests/unit/memory/cli/test_soul.py tests/unit/memory/surfaces/test_soul.py tests/unit/memory/services/test_soul.py
git diff --check
```

Manual Pi smoke:

```text
enter Soul Mode for soul-mode
answer the day question
reach Possible Listenings
choose Self Voice
continue until Fruit In Maturation
harvest
save to journal
```

Expected: every required surface appears, one journal entry is created only after confirmation, and no deferred voice is implied as fully implemented.

## Future Runway To Preserve

After `v0.24.0`, Soul Mode should explore a Closing Rite that reviews harvested material for possible psyche-layer enrichment. The first release saves the fruit to journal; the future rite asks what of the harvest wants to become part of the Mirror's living psyche.

Candidate future work:

```text
CV18 — Soul Mode Integration And Psyche Enrichment
CV18.DS1 — Closing Rite And Integration Review
CV18.DS2 — Self Layer Enrichment Proposal
CV18.DS3 — Shadow Layer Enrichment Proposal
CV18.DS4 — Ego Behavior And Persona Integration
CV18.DS5 — Confirmation And Safe Identity Mutation
```

Guardrail:

```text
No automatic psyche mutation.
```

All identity enrichment must be proposed with visible diff and applied only after explicit confirmation.
