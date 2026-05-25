[< CV13.E1](../index.md)

# CV13.E1.S2 — Three-letter persona tokens

**Status:** ✅ Done
**User-visible outcome:** Persona icons in the Identity map use stable three-letter tokens instead of shorter two-letter initials.

---

## Scope

- Generate persona token icons from the first three alphanumeric characters of the public persona label.
- Keep the existing persona orbit layout and object-detail behavior.
- Add focused surface coverage so the token contract is explicit.

---

## Non-goals

- No persona detail redesign.
- No new persona page.
- No avatar image support.
- No broader Identity chip navigation.

---

## Acceptance Criteria

- A one-word persona such as `engineer` renders `ENG`.
- A hyphenated or spaced persona label still renders a three-letter token from its public label.
- Persona object links still work through the existing token buttons.
- Focused Atlas tests pass.

---

## See also

- [Plan](plan.md)
- [Test Guide](test-guide.md)
