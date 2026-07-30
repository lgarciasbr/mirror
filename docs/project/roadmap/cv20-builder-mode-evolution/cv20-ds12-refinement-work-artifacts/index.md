[< CV20](../index.md)

# CV20.DS12 — Document-First Refinement Workbench

**Status:** 🟡 Planned — redesign approved

---

## Outcome

A project has one versioned Refinement index that states the canonical backlog and
status of Refinement Stories and Change Requests, with predictable directories for the
documents and evidence produced while that work proceeds.

The Workbench is understandable by reading the repository. It does not require a local
Mirror database, journey, conversation history, or custom handoff protocol to recover
shared meaning.

---

## Why This Exists

Delivery Work already has a roadmap and story packages that make position, status,
plans, evidence, and closure inspectable across sessions. Refinement needs the same
durability without turning small changes into Delivery Stories.

The first DS12 experiment expanded this need into filesystem authority, SQLite
projection, mutation recovery, Git coherence, and cross-clone handoff machinery. That
implementation was archived without merge after proving disproportionate to the real
workflow. The retained learning is recorded in the
[experiment retrospective](experiment-retrospective.md).

---

## Product Premises

- Project documents own canonical shared Refinement meaning.
- Git owns history, collaboration, conflict handling, and recovery.
- Journeys and runtime databases remain local context, never artifact identity.
- The canonical index must be useful to humans and agents without database access.
- Generated artifacts should be ordinary Markdown files with stable relative links.
- Validation starts structural and small; automation grows only from observed failures.
- Existing CV20.DS6 SQLite data is not removed implicitly. Migration or deprecation is
  separate, explicit work after the document contract is proven.

---

## Initial Scope

1. Define the canonical Refinement index: RS/CR identity, status vocabulary, ordering,
   active focus, and links.
2. Define the minimal directory and artifact conventions for RSs and CRs.
3. Prove that another session or clone can understand and continue Refinement work from
   project files and Git alone.
4. Add only lightweight structural validation justified by the document contract.
5. Define, but do not yet execute, the migration boundary from the existing SQLite
   Workbench.

Detailed candidate stories will be authored after the document examples and status
vocabulary are reviewed. The archived experiment's TS/US decomposition is not reused.

---

## Non-Goals

- No SQLite projection of canonical Refinement documents.
- No transactional cross-clone handoff or recipient readiness protocol.
- No application-level reconstruction of Git ancestry, publication, or conflict logic.
- No implicit commit, push, merge, publication, release, or repository configuration.
- No automatic removal or migration of the CV20.DS6 runtime Workbench.
- No claim that every transient event requires a durable file.

---

## Done Condition

DS12 is done when a collaborator or fresh agent session can open the project, read one
canonical Refinement index, identify the current RS/CR backlog state, navigate to its
artifacts, and continue the documented workflow using ordinary files and Git — without
requiring the originating journey or database.
