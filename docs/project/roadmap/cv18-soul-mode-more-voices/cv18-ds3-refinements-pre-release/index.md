[< CV18](../index.md)

# CV18.DS3 — Refinements Pre-Release

**Status:** ⏭️ Cancelled

**Placement:** Pre-release tuning after Wisdom Voice and Beauty Voice are usable

**User-visible outcome:** The expanded Soul Mode voice constellation is tuned through real use before packaging.

---

## Why This Exists

The first Soul Mode release showed that ritual behavior needs validation in Pi, not only unit tests. Adding Wisdom and Beauty changes the feel of Possible Listenings, the voice-selection grammar, and the user's expectations.

This story reserved space for the small corrections discovered once the new voices were used in a real ritual flow. It was cancelled before implementation because all necessary tuning was completed during DS1 and DS2 validation: Wisdom Voice and Beauty Voice were refined directly inside the voice delivery stories, and no separate pre-release refinement pass remained necessary.

---

## Scope

- Validate Wisdom Voice and Beauty Voice in Pi using natural language.
- Tune microcopy, icons, voice labels, or threshold guidance if usage shows friction.
- Fix small edge cases discovered during manual validation.
- Update docs and test guides to match the final behavior.
- Keep changes bounded to refinement of the expanded voice release.

---

## Non-goals

- No new major voice.
- No rich UI.
- No identity integration.
- No journal model expansion.
- No unrelated roadmap cleanup.
- No broad architecture refactor unless required to stabilize the release.

---

## Acceptance Behavior

Given DS1 and DS2 are implemented, the user can run a full Soul Mode smoke flow in Pi and hear Wisdom Voice and Beauty Voice without confusion about who is speaking or what to do next.

Given refinements are needed, they are captured as small, testable changes and documented before release packaging.

Given a request would expand scope beyond release tuning, it is deferred to a later CV or radar item.

---

## References

- [CV18 — Soul Mode More Voices](../index.md)
- [CV18.DS1 — Wisdom Voice](../cv18-ds1-wisdom-voice/index.md)
- [CV18.DS2 — Beauty Voice](../cv18-ds2-beauty-voice/index.md)
