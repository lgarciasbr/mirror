[< RS001](index.md) · [Canonical status](../index.md#change-requests)

# CR004 — Preserve Authored Story Index During Plan Materialization

## Problem

`build plan-item` replaced a hand-authored story `index.md` with its generic generated
scaffold. This happened while planning both CV20.DS12.TS1 and CV20.DS12.US1. In each
case the authored outcome, boundaries, and acceptance details had to be restored
manually after the command.

## Expected Behavior

Plan materialization preserves an existing authored story index. It may create a missing
index or update only explicitly runtime-owned fields, but it must not replace authored
content with a generic template.

## Impact

The Plan command can silently destroy the very project context it is meant to preserve.
Repeated manual restoration also makes the generated `updated story index` surface
technically true while the operation remains undesirable.

## Plan Or Decision

Pending. Before changing code, characterize create-versus-existing behavior and identify
which, if any, fields are genuinely runtime-owned. Prefer insert-if-absent or a
no-clobber policy over Markdown merging.

## Evidence

Observed twice during document-first DS12 dogfooding and recorded in the
[US1 Debt Review](../../roadmap/cv20-builder-mode-evolution/cv20-ds12-refinement-work-artifacts/cv20-ds12-us1-dogfood-file-only-refinement/review.md).

## Outcome

Pending.
