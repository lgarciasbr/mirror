[< CV20](../index.md)

# CV20.DS4 — Story Lifecycle Runtime

**Status:** 🟢 Active

---

## Outcome

Builder can guide one Ariad story through Pull, Prepare, Plan, Implement, Validation, Review, Coherence, and Done using deterministic lifecycle gates.

---

## Candidate Stories

| Code | Story | Type | Outcome | Status |
|------|-------|------|---------|--------|
| [CV20.DS4.TS1](cv20-ds4-ts1-surface-routing-definitions/index.md) | Surface Routing Definitions | Technical Story | Ariad method data declares which surfaces roadmap inspection emits | ✅ Done |
| [CV20.DS4.TS2](cv20-ds4-ts2-lifecycle-contract-definitions/index.md) | Lifecycle Contract Definitions | Technical Story | Ariad method data declares phase-specific lifecycle contracts for runtime gates | ✅ Done |
| [CV20.DS4.US0](cv20-ds4-us0-inspect-pull-candidates/index.md) | Inspect Pull Candidates | User Story | Navigator can ask to see the roadmap and pull candidates before selecting active work | ✅ Done |
| [CV20.DS4.US1](cv20-ds4-us1-pull-and-prepare/index.md) | Pull and Prepare | User Story | Navigator can pull DS/US/TS work and see Prepare assess context, risks, rules, and granularity | ✅ Done |
| [CV20.DS4.US2](cv20-ds4-us2-plan-checkpoint-gate/index.md) | Plan checkpoint gate | User Story | Builder creates a plan surface and blocks implementation until Navigator approval | 🟡 Planned |
| CV20.DS4.US3 | Validation checkpoint | User Story | Builder runs automated checks and presents a concrete Navigator validation route | 🟡 Planned |
| CV20.DS4.US4 | Coherence and Done gate | User Story | Builder verifies traces, records history according to policy, closes the story, and recommends next Pull | 🟡 Planned |

---

## Done Condition

DS4 is done when a non-trivial story can move through the Ariad lifecycle without the Driver silently skipping checkpoints or declaring progress without required artifacts.
