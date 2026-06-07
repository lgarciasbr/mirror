[< CV16](../index.md)

# CV16.DS6 — Experiment Proposals and Attractors

**Status:** ✅ Done

**Placement:** CV16 exploratory direction story

**User-visible outcome:** A thickened Exploratory Story can name attractors and propose a small experiment while remaining in Explorer Mode, without silently becoming Builder delivery.

---

## Why This Exists

DS5 made the Exploratory Story visible through opening, thickening, and snapshot surfaces. The next question is direction: once a story has thickened, what is it pulling toward, and what small experiment could test that direction?

Attractors are not decisions. They are directional pulls inside an exploration. Experiment proposals are not Builder plans. They are small tests that keep uncertainty alive while making the next learning move concrete.

```text
Attractor names the pull.
Experiment proposal tests the pull.
Builder executes only after confirmation.
```

---

## Scope

- Extend the in-session Exploratory Story state with attractors and an experiment proposal.
- Store attractors inside the current Explorer Story runtime payload, associated with the current journey story.
- Render visible surfaces for attractors and experiment proposals.
- Support explicit user requests such as “qual é o attractor?” and “que experimento testa isso?”.
- Allow the assistant to propose an attractor conversationally when the story is mature, but only store it when surfaced visibly.
- Keep attractor status explicit, initially `proposed` or `accepted` if the user confirms or edits it.

---

## Non-goals

- No autonomous hidden attractor detection.
- No LLM classifier in the Python core.
- No durable Explorer archive or new schema.
- No multiple Exploratory Stories.
- No Builder activation.
- No Builder handoff document. DS7 owns handoff.
- No web console surface.

---

## Acceptance Behavior

Given an Exploratory Story exists, when the user asks for the attractor, Mirror renders `△ ATTRACTORS EMERGING` and stores the surfaced attractor in the current story state.

Given the assistant proposes an attractor without explicit user request, it renders the proposal visibly and stores it only because it was made visible.

Given the user corrects an attractor, Mirror updates the stored attractor rather than accumulating a hidden competing interpretation.

Given the user asks for a small experiment, Mirror renders `△ EXPERIMENT PROPOSAL` and stores the proposed experiment in the current story state.

Given an experiment proposal exists, Narrative Field Snapshot includes story, attractors, and experiment proposal.

Given DS6 runs, no Builder mode activation happens.

---

## References

- [Plan](plan.md)
- [Test Guide](test-guide.md)
- [CV16 Explorer Mode](../index.md)
