---
name: "mm-build"
description: Activates Builder Mode for a journey and loads project context/docs
user-invocable: true
---

# Builder Mode

Activates Builder Mode for a specific journey. Loads identity context and project docs.

## Usage

Pi and Gemini CLI:

```
/mm-build <journey-slug>
```

Codex:

```
$mm-build <journey-slug>
```

Claude Code:

```
/mm:build <journey-slug>
```

---

# Base Builder Mode Behavior

This is the default behavior for every journey, including journeys that have not
adopted Ariad or any Builder method.

## 1. Load Context (DB)

```bash
uv run python -m memory build load <slug>
```

The command:

- Activates `■ Builder Mode` in the operating-mode lifecycle
- Renders the Mode Transition Surface (`■ BUILDER MODE ACTIVE`)
- Prints identity context (soul + ego + user + journey, persona=engineer)
- Prints relevant memories
- Starts a new database conversation session
- Emits `project_path=<path>` as the last output line

## 1.1 Transition Surface

Render the `build load` transition surface visibly before continuing with project
doc loading or substantive Builder work.

For journeys without adopted Ariad, preserve original Builder behavior:

- load context;
- read project docs;
- stop at the Builder Activation Boundary;
- ask what work should be done next.

Do not render Ariad surfaces, Ariad lifecycle suggestions, roadmap snapshot,
pull candidates, cursor state, or checkpoint language for journeys that have not
adopted Ariad.

For Ariad-adopted journeys, see **Ariad Runtime Behavior** below.

Builder Mode surface should orient the user around:

- active journey
- journey path/stage, when present
- project path, when present
- compact briefing/synthesis
- boundary: `Builder executes commitment.`

## 2. Read Project Docs

Parse `project_path` from the last output line above. If `project_path` is not
set, skip this step and proceed — the journey has no associated project yet.

Use file tools to load project documentation. Prefer the project's actual
documentation structure over any fixed scaffold.

### Always read when present

- `<project_path>/README.md` — public overview, setup, and usage
- `<project_path>/REFERENCE.md` — detailed operational reference
- `<project_path>/CLAUDE.md` — project-specific operating instructions
- `<project_path>/docs/index.md` — documentation map

### Discover available docs

Run:

```bash
find <project_path>/docs -maxdepth 3 -type f -name '*.md' | sort
```

Then read the docs relevant to the current task.

For Mirror Mind, the primary docs are:

- `<project_path>/docs/getting-started.md`
- `<project_path>/docs/project/briefing.md`
- `<project_path>/docs/project/decisions.md`
- `<project_path>/docs/product/specs/runtime-interface/index.md`
- `<project_path>/docs/project/roadmap/index.md`
- `<project_path>/docs/process/development-guide.md`
- `<project_path>/docs/process/worklog.md`
- `<project_path>/docs/product/principles.md`

When working inside a CV/Epic/Story, also read the relevant:

- `index.md`
- `plan.md`
- `test-guide.md`
- `refactoring.md`, if present

## 3. Builder Activation Boundary

Activating Builder Mode or loading a journey is context setup only. After loading
the context and required docs, stop and ask what work should be done next.

Do not edit files, create tests, run implementation, start TDD, or mutate project
state until the user gives an explicit implementation or documentation
instruction, such as `implement`, `fix`, `edit`, `create`, `run tests`, or names a
specific story to execute.

Context activation is not execution consent.

## 4. Work In Builder Mode

Once the user explicitly authorizes work:

- Work from `project_path` — read, edit, and create project files normally
- Keep project docs updated as the code evolves
- Commit at the end of each session with a descriptive English commit message

## 5. Project Docs Maintenance

Follow the project's existing documentation structure. Do not create a generic
docs scaffold unless the user explicitly asks for one.

**When to update docs:**

- `README.md`: public positioning, setup, stack, or usage changes
- `REFERENCE.md`: CLI behavior, configuration, runtime contracts, or operational details change
- `docs/project/briefing.md`: stable architectural premises change
- `docs/project/decisions.md`: an incremental design decision is made
- `docs/product/specs/runtime-interface/index.md`: runtime lifecycle, hooks, skills, or extension contracts change
- `docs/project/roadmap/`: CV/Epic/Story status, plans, or verification guides change
- `docs/process/worklog.md`: a meaningful milestone is completed
- `docs/product/principles.md`: product, code, testing, or process principles change

## 6. Configure `project_path`

If the journey does not yet have an associated project:

```bash
uv run python -m memory journey set-path <slug> /path/to/project
```

## 7. Finalize Session

When the user says "End the session":

```bash
uv run python -m memory mirror log "SESSION_SUMMARY"
```

---

# Adopted Method Behavior

A journey may adopt a Builder method. Method-specific behavior applies only when
that method has been adopted for the active journey.

Currently implemented method-specific runtime: **Ariad**.

For journeys without adopted Ariad:

- preserve Base Builder Mode behavior;
- do not render Ariad surfaces;
- do not route roadmap, pull, prepare, template, cursor, or lifecycle requests to Ariad commands;
- if the user asks for Ariad behavior, explain that Ariad must be adopted first.

## Inspect Builder Method

When the user asks which Builder method governs the active journey, inspect the
current Builder method state:

```bash
uv run python -m memory build inspect-method
```

If the user names a specific journey:

```bash
uv run python -m memory build inspect-method --journey <slug>
```

Render the command output visibly. If no Builder journey is active yet, say so
plainly and ask the user to activate or name a journey. If the journey has not
adopted a Builder method yet, say so plainly. Do not infer that Ariad governs the
journey just because Ariad is available.

When the user asks what Ariad is as a Builder method, inspect the built-in method
defaults:

```bash
uv run python -m memory build inspect-method ariad
```

This is read-only inspection.

## Adopt Ariad

When the user explicitly asks to adopt Ariad for the active journey, run:

```bash
uv run python -m memory build adopt --method ariad
```

If the user names a specific journey:

```bash
uv run python -m memory build adopt --journey <slug> --method ariad
```

Render the adoption report visibly. This mutates Builder method state only. It
must not generate templates, create a delivery cursor, execute lifecycle work,
change story status, commit, push, or release.

---

# Ariad Runtime Behavior

This section applies **only when the active journey has adopted Ariad**
(`adopted_method == ariad`).

## Ariad Activation Surfaces

For Ariad-adopted journeys with no active item, `build load` can emit:

- `ROADMAP SNAPSHOT`
- `■ Ariad Pull Candidates`

For Ariad-adopted journeys with an active item or pending confirmation,
`build load` can emit:

- `■ BUILDER RESUME`

These surfaces are mandatory activation output. The final response to the user
must include them verbatim from the command output. Do not replace them with a
bullet summary, prose synthesis, or a generic "estado atual" list. If the command
output contains `ROADMAP SNAPSHOT`, the response is invalid unless the visible
reply also contains `ROADMAP SNAPSHOT` and `■ Ariad Pull Candidates`.

Preserve headings, card layout, operational fields, recommendations, and
boundaries from the command output. After rendering these surfaces, do not ask a
generic question such as "inspeção runtime, planejamento de Delivery, ou
exploração?". For an Ariad journey with no active item, ask whether the Navigator
wants to pull the recommended candidate or inspect the roadmap further.

## Prepare Ariad Templates

When the user asks to prepare Ariad templates or make the adopted journey
documentation-ready, run:

```bash
uv run python -m memory build prepare-templates --method ariad
```

If the user names a specific journey:

```bash
uv run python -m memory build prepare-templates --journey <slug> --method ariad
```

Render the report visibly. The operation may create missing method-declared
template files, but must preserve existing files and must not create a delivery
cursor, execute lifecycle work, change story status, commit, push, or release.

## Sync Delivery Cursor

When the user asks to sync the initial Builder delivery cursor for an
Ariad-adopted journey, run:

```bash
uv run python -m memory build sync-cursor --method ariad
```

If the user names a specific journey:

```bash
uv run python -m memory build sync-cursor --journey <slug> --method ariad
```

Render the cursor sync report visibly. This persists runtime resume state only.
It must not infer an active roadmap item, execute Pull/Prepare/Plan, change story
status, commit, push, or release.

## Inspect Roadmap And Pull Candidates

When the user asks to see the roadmap, inspect the roadmap, show roadmap
candidates, see what can be pulled, choose the next story, or asks "o que posso
puxar agora?", run:

```bash
uv run python -m memory build pull-candidates --method ariad
```

If the user names a specific journey, pass `--journey <slug>`. Render the
configured Ariad surfaces visibly, currently `ROADMAP SNAPSHOT` and `■ Ariad Pull
Candidates`. This is read-only: it must not pull an item, update the cursor,
execute lifecycle work, change story status, commit, push, or release.

## Pull And Prepare Ariad Work

When the user asks to pull a roadmap item into active Ariad work, run the
contained Pull command with explicit item metadata:

```bash
uv run python -m memory build pull-item --method ariad \
  --item-code <code> \
  --item-title "<title>" \
  --item-level <delivery_story|user_story|technical_story> \
  --why-now "<why this level now>"
```

If the user names a specific journey, pass `--journey <slug>`. Render the Pull
report visibly. Pull may update runtime cursor active item, but must not execute
Prepare, Plan, Implement, Validation, Review, Coherence, Done, commit, push, or
release.

When the user asks to prepare the pulled item, run:

```bash
uv run python -m memory build prepare-item --method ariad
```

If the user names a specific journey, pass `--journey <slug>`. Render the Prepare
report visibly. Prepare may update the runtime cursor last delivery event, but
must not create a Plan, approve a checkpoint, start implementation, change story
status, commit, push, or release.
