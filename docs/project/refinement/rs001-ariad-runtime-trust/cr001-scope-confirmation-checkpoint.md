[< RS001](index.md) · [Canonical status](../index.md#change-requests)

# CR001 — Make Scope Confirmation An Honest Checkpoint

## Problem

Under checkpoint cadence, `plan-delivery-story` has emitted a scope-confirmation surface
phrased as a pre-plan question and then materialized the plan in the same invocation.
The checkpoint appears to gate an action that has already happened.

## Expected Behavior

Either scope confirmation stops before plan artifacts are written, or the surface is
explicitly non-gating and does not ask a precondition question after materialization.
Cadence semantics and visible language must agree.

## Impact

A checkpoint that does not checkpoint weakens trust in every other Ariad stop condition.

## Plan Or Decision

Pending. Evaluate the smallest correction only when this CR is selected. Candidate
routes are a separate confirmation step or cadence-aware non-gating wording; neither is
chosen by capture alone.

## Evidence

The original dogfooding observation is
[AF-004](../../roadmap/cv20-builder-mode-evolution/ariad-dogfooding-ledger.md#af-004--scope-confirmation-checkpoint-collapses-into-plan-materialization).

## Outcome

Pending.
