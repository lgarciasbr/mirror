[< CV9.DS7](../index.md)

# CV9.DS7.US2 — Apply Metadata Lifecycle Decisions Safely

**Type:** User Story  
**Status:** Active; unblocked, plan proposed  
**Parent:** [CV9.DS7 Conversation Metadata Lifecycle](../index.md)

---

## Intent

Apply accepted conversation metadata lifecycle decisions during conversation
metadata updates without creating durable weak metadata and without overriding
manual/user-edited title locks.

---

## Observable Behavior Seed

Conversation metadata updates follow lifecycle decisions for title, summary,
tags, readiness, provenance, confidence, and update source while preserving
manual locks.

---

## Pull State

Pulled after CV9.DS7.US1 and CV9.DS7.TS1 closed. D-001 triggered during the plan gate: apply/mutation behavior would grow metadata lifecycle policy and write-boundary debt inside ConversationService. [CV9.DS7.TS2](../cv9-ds7-ts2-extract-metadata-lifecycle-policy-boundary/index.md) extracted the policy boundary, so US2 is unblocked for apply implementation planning.

## Plan and Validation

- [Plan](plan.md)
- [Test Guide](test-guide.md)
