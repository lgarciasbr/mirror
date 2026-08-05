[< RS001](index.md) · [Canonical status](../index.md#change-requests)

# CR008 — Bind Lifecycle Commands To The Active Builder Journey

## Problem

During a Builder session activated for `kia-backend` (`build load kia-backend`),
`build pull-item --method ariad` invoked **without** `--journey` resolved to a
different journey. The command emitted `DELIVERY_STORY_IDENTIFIED` claiming
`commitment: pulled into active Delivery Work / active item: CV3.DS4.TS2` — a
kia-backend roadmap item — but persisted that commitment to the **kia-desktop**
delivery cursor, overwriting its prior state. The kia-backend cursor was left
untouched, so the surfaced commitment never existed for the journey it named.

Journey resolution was also inconsistent within one session: in a single shell
chain, `prepare-item` (no `--journey`) resolved to a journey and executed, while
the immediately following `plan-item` failed with `Builder method plan requires a
journey`.

## Expected Behavior

Lifecycle commands must bind deterministically to the active Builder journey, or
refuse and ask for `--journey` — never fall back silently to another journey. The
journey a command persists to must be the journey its emitted surface speaks for;
a surface must not claim a commitment that was written elsewhere or not written at
all. Resolution must be consistent across commands within the same session.

## Impact

Silent cross-journey state corruption: one journey's resume state is clobbered
(kia-desktop lost `CV3.DS18.US4 / done_complete`), while the operating journey's
lifecycle blocks on stale state (`Prepare must be completed before Plan` against
an already-done item). Because the surfaces asserted success, the defect was only
discovered by direct storage inspection — a direct breach of the surface-trust
promise RS001 exists to protect.

## Plan Or Decision

Pending. Capture does not authorize a resolver change. First characterize where
journey fallback lives (conversation session, most-recent runtime session, or
per-command resolution) and why `prepare-item` and `plan-item` disagreed within
one chain.

## Evidence

Reproduced 2026-08-04 while operating the kia-backend journey:

```text
# pull-item without --journey — surface claimed kia-backend's item:
commitment: pulled into active Delivery Work
active item: CV3.DS4.TS2

# same output, auto-Prepare terrain read (kia-desktop's terrain — the file
# exists in kia-backend):
○ docs/process/development-guide.md: missing

# persisted cursors afterward:
__builder_delivery_cursor__:kia-desktop  → active_item CV3.DS4.TS2   (clobbered)
__builder_delivery_cursor__:kia-backend  → active_item CV3.DS2.US1   (unchanged)

# same-chain inconsistency:
prepare-item (no --journey) → executed, rendered PREPARE_FIELD_READING
plan-item    (no --journey) → "Builder method plan requires a journey"
```

Recovery: re-running `pull-item` with explicit `--journey kia-backend` persisted
correctly (verified by reading the cursor row). The kia-desktop cursor's prior
value was recovered from `backups/memory_20260804_124634.zip`
(`CV3.DS18.US4`, `done_complete`, `stepwise`) and restored with explicit
Navigator approval.

## Outcome

Pending.
