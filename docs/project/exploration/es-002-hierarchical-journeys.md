[< Project](../briefing.md)

# ES-002 — Hierarchical Journeys

**Status:** Promoted to Delivery  
**Delivery handoff:** [CV15 Cognitive Location](../roadmap/cv15-cognitive-location/index.md)  
**Source:** Ariad exploration on 2026-06-02 during Mirror Mind Builder work  
**Initial scope:** one hierarchy level

---

## Opening Premise

Hierarchy should be organizational and visual first, not deep semantic context
mixing.

A child journey remains a normal journey, with its own conversations, memories,
tasks, Builder context, and routing. The parent journey functions as a grouping
field, territory, program, or larger container of meaning. Mirror can show the
relationship, but it should not automatically mix memories or context between
parent and child without an explicit decision.

---

## Principle-Level Thickening

The Mirror should be a mirror of the user's cognition. Human adaptive cognition is symbolic, temporal, and spatial: the future place where I want to be is always combined with the present place where I am, so cognition finds itself inside a trajectory.

A journey is therefore not merely a project label. It is a structured A-to-B movement. The mind is always positioned between an origin and a destination, and those movements nest hierarchically. Writing a sentence has an A and B. That action sits inside an exploration whose B is clearer understanding. The exploration sits inside capability development whose B is a release. That development sits inside Mirror Mind as a portfolio-level project. That project sits inside the user's broader life trajectory.

The hierarchy of journeys should therefore express how cognition organizes itself across nested trajectories. The first implementation may remain organizational and visual, but the underlying principle is deeper: the Mirror should help the user see where they are, where they are going, and how the current movement belongs to larger movements.

This reframes hierarchy from a convenience feature into a cognitive model. The product question becomes not only how to group journeys, but how to preserve the user's sense of being situated inside multiple nested A-to-B trajectories without prematurely merging their memories, contexts, or operational scopes.

---

## Initial Signal

As the number of journeys grows, the flat Workspace list becomes harder to scan.
Some journeys clearly belong together: a broad domain such as Software Zen may
contain product, support, content, or consulting journeys; Mirror Mind may
contain self-update, web-console, Maestro, and runtime-hardening journeys. The
current flat list preserves independence, but it does not express this natural
shape.

The user-visible need is not yet semantic aggregation. It is orientation: seeing
which journeys belong under a wider territory without losing each journey as an
independent unit of work and memory.

---

## Thickened Story

A journey is not a folder. It is an identity artifact and continuity unit. If a
journey hierarchy is implemented too aggressively, the parent-child relation may
blur boundaries that are currently valuable:

- conversation extraction depends on a single journey association;
- memories are retrieved by journey and may affect future context;
- Builder Mode loads a specific journey and its project path;
- routing detects journeys from user language;
- Workspace uses selected journey as the center of the surface.

The first version should therefore treat hierarchy as a display and organization
relationship. A child journey should not inherit the parent's memories, tasks,
project path, or Builder context automatically. A parent journey should not
silently absorb child conversations. Any future aggregated view must be explicit
in the product surface.

---

## Emerging Language

The language of parent and child is pragmatic, but it may not carry the product meaning clearly enough. The stronger semantic pair emerging from the exploration is **scene** and **horizon**.

A scene answers: where am I now? It is the situated territory of navigation, where the user perceives current constraints, meanings, tools, actors, and next movement. A horizon answers: toward what am I moving? It replaces the abstract point B with a lived destination or direction.

In this language, the UI is not merely organizing projects. It is returning cognitive location. The product promise becomes: Mirror can show the scene the user is in, the broader scene it belongs to, and the horizon that gives the current movement direction.

The implementation question becomes sharper: how can Mirror surface cognitive location using only a simple parent-child journey relationship, without asking the user to maintain extra model data?

---

## Candidate Model

A one-level hierarchy can be represented in journey metadata:

```json
{
  "parent_journey": "softwarezen"
}
```

This preserves the existing database model. Journey identity rows remain the
source of truth, and the parent relationship stays close to other journey-level
configuration such as `project_path`, `sync_file`, `icon`, and `color`.

Candidate rules:

- `parent_journey` is optional.
- The parent must be an existing journey.
- A journey cannot be its own parent.
- Only one level is supported in the first slice.
- A parent may still be a normal selectable journey.
- A child remains directly selectable and routable.
- No conversations, memories, tasks, or attachments are migrated when a parent is set.
- No automatic context expansion from parent to child or child to parent happens in the first slice.

---

## Product Questions

The main unresolved question is what selecting a parent journey should show.
There are two plausible modes:

### Parent as its own journey

Clicking the parent shows only the parent's own conversations, memories, tasks,
briefing, and settings. Child journeys appear visually under it in the sidebar,
but the parent surface is not an aggregate.

This is safer and matches the opening premise.

### Parent as panorama

Clicking the parent shows a broader view that may include child-journey counts,
recent child conversations, or child summaries. This is useful but must be
labeled as an aggregate. It should not masquerade as the parent journey's own
memory/context.

This is likely a later slice.

---

## Candidate Direction

The exploration has enough shape to form a Delivery candidate.

**Candidate:** Scene as the Workspace home for cognitive location.

Scene becomes both the default Workspace home and the home shown when the user clicks a specific journey. Journey remains the operational primitive. A simple one-level `parent_journey` relation gives the structural map. Scene is the composed surface that answers "where am I now?" from the journey tree, recent movement, horizons, and a grounded LLM synthesis.

The LLM synthesis should enter from the beginning because cognitive location is interpretive, not only structural. The synthesis must be bounded: it receives a deterministic read model and uses only existing signals. It should not invent journeys, goals, emotions, priorities, or semantic relationships. The deterministic Journey Map remains useful if synthesis fails.

---

## First Slice Candidate

The smallest coherent implementation appears to be:

- Add `parent_journey` support to journey metadata validation.
- Add an optional parent journey selector to the New journey flow.
- Add an optional parent journey selector to Journey Settings.
- Render Workspace journeys grouped by one parent level.
- Replace the default Workspace home with a Scene surface.
- Render the selected-journey home as a focused Scene surface.
- Add bounded LLM synthesis from a deterministic Scene read model.
- Keep parent and child operational semantics unchanged: conversations, memories, routing, Builder context, and extraction remain journey-specific.
- Add tests for parent validation, grouped read model, synthesis prompt boundaries, fallback behavior, and UI payload shape.

This would let users organize journeys hierarchically without changing memory,
routing, extraction, Builder context, or search semantics.

---

## Conscious Non-Goals for First Slice

- No recursive hierarchy.
- No multiple parents.
- No automatic aggregate context loading.
- No parent-child memory inheritance.
- No automatic migration of conversations, memories, tasks, attachments, or project paths.
- No journey slug rename.
- No deletion cascade.
- No semantic inference that assigns a child based on parent context.

---

## Validation Seed

Create a parent journey and two child journeys in an isolated test database.
Verify that:

- each journey remains selectable by its own slug;
- children appear visually under the parent in Workspace;
- the parent does not show child conversations as its own conversation cards;
- assigning a conversation to a child associates it only with the child;
- Builder/journey status still loads the child independently;
- metadata validation rejects self-parenting and unknown parent ids.

---

## Delivery Handoff

**Promoted placement:** [CV15 Cognitive Location](../roadmap/cv15-cognitive-location/index.md)

The exploration promotes into two separate delivery stories and release intents:

1. **Hierarchical Journey Organization**: add `parent_journey`, allow parent assignment, and render journeys hierarchically across web and textual Mirror surfaces. Release intent: `v0.20.0`.
2. **Scene Workspace Home**: make Scene the Workspace home and selected-journey home, using hierarchical journeys, movement signals, horizons, and bounded LLM synthesis to return cognitive location. Release intent: `v0.21.0`.

The split is intentional. Hierarchical journeys organize the field. Scene interprets the field.

---

## Carry Forward Notes

The guiding boundary is: hierarchy organizes attention; it does not merge
identity.

If later we want parent-level aggregation, it should be introduced as a named
surface, for example a parent panorama, not as an implicit change to journey
context semantics. The user should always be able to tell whether they are
looking at one journey's own context or a roll-up of related journeys.
