[< Story](index.md)

# Refactoring — CV21.E2.S1 Claude plugin conversion

Deferred cleanup surfaced during the review ritual. None block S1; each has a
revisit trigger.

## Deferred

- **`read_version` duplication.** `memory.plugins.claude.read_version` reparses
  the `pyproject.toml` `version =` line, duplicating the private
  `_version_from_pyproject` in `memory.cli.runtime`. Kept separate to avoid a
  cross-layer dependency (`plugins` → `cli`) and because the two have different
  resolution semantics (build-tool reads the repo pyproject deterministically;
  runtime walks parents with an installed-metadata fallback).
  *Revisit when* a third call site appears or a shared `memory` version util is
  introduced — extract one helper then.

- **Plugin skill invocation token.** The plugin bundles skills byte-faithfully
  with `mm:`-prefixed directory names. How Claude namespaces plugin skills
  (`/mm:mirror` vs a `mirror-mind:`-prefixed token) and whether the colon dir
  name is portable (not Windows-safe) is not yet normalized. Skill *bodies*
  still self-reference `/mm:*`.
  *Revisit when* live skill discovery (manual route / a later live-session test)
  shows the effective token, or when Windows portability is in scope. Any rename
  is a deliberate, drift-guarded regeneration, not a hand edit.

## Standalone hygiene (tracked in the epic, not fixed here — `.claude/` untouched)

- `.claude/skills/mm:build` and `mm:identity` use lowercase `skill.md`
  (case-sensitive-runtime discovery risk). The plugin generator normalizes to
  `SKILL.md`, so the plugin is correct regardless.
- `.claude/skills/mm:help` references a `mm:save` command with no skill dir.
