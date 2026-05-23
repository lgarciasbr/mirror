[< CV9.E3.S14](index.md)

# Ariad Visual Progress Experiment

This story experiments with a higher-altitude map plus a horizontal flow board.

## Visual Grammar

Taxonomy cards:

- `🟪[CV9]` for Capability Value cards
- `🟦[E3]` for Epic cards
- `🟩[S14]` for Story cards

Ariad checkpoint states:

- `✓` done
- `◉` current
- `○` pending
- `✕` blocked

Learning: in Markdown/plain text, a colored square emoji is not a container. We cannot place `CV9` inside `🟪`. The adopted compromise is the inline card pattern `🟪[CV9]`, where the color marks taxonomy level and the bracket carries the code.

## Bird's-Eye Map

```text
🟪[CV9]  Mirror Mind 1.0
  🟦[E3]   Distribution & Tooling
    🟩[S14]  Release Notes Skill Parity
```

## Ariad Stage Ribbon

```text
Ariad: ✓ Plan | ✓ Implement | ✓ Validate | ✓ Review | ✓ Coherence | ◉ Commit
Flow:   Backlog | Ready | Doing | Validate | ◉ Done
Progress: ███████░ 88%
```

## Horizontal Flow Board

```text
+---------+--------+--------------------------------+----------+--------------------------------+
| Backlog | Ready  | Doing                          | Validate | Done                           |
+---------+--------+--------------------------------+----------+--------------------------------+
| 🟩[S15] |        | 🟩[S14] Release Notes Parity   |          | 🟩[S13] Release-Aware Notices  |
| 🟩[S16] |        |                                |          | 🟩[S12] First Stable Release   |
| 🟩[S17] |        |                                |          |                                |
+---------+--------+--------------------------------+----------+--------------------------------+
```

## Story Cards

| Card | Lane | Notes |
|------|------|-------|
| Map runtime skill surfaces | Done | Identified Pi, shared `.agents`, Claude, Codex docs/help surfaces. |
| Add missing shared skill link | Done | `.agents/skills/mm-release-notes` points to Pi skill. |
| Add Claude release-notes skill | Done | Added `/mm:release-notes` wrapper for Claude Code. |
| Update help/discovery surfaces | Done | Updated Pi help, Claude help, AGENTS, and REFERENCE. |
| Validate release-note commands | Done | Latest and specific version smoke passed. |
| Close story docs | Done | Story done, epic index updated, worklog updated. |

## Visualization Notes

- The bird's-eye map gives the story a visible address before task movement starts.
- The horizontal board makes planned sequence and neighboring stories visible without turning the view into a long checklist.
- This view distinguishes roadmap flow (`S13`, `S14`, `S15`) from task flow (the cards inside S14). Maestro may need both levels: story kanban and task kanban.
- The adopted visual grammar reserves color for taxonomy (`CV`, `E`, `S`) and symbols for method state (`✓`, `◉`, `○`, `✕`). This avoids confusing lifecycle progress with roadmap level.
