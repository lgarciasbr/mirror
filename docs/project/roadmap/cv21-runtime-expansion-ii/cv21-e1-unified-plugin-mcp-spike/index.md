[< CV21](../index.md)

# CV21.E1 — Unified Plugin & MCP Spike

**Status:** 🟢 Active

---

## Outcome

The keystone decision of CV21: **we know whether packaging Mirror Mind once as a
canonical plugin plus an MCP server is real and viable across runtimes**, and we
have chosen the integration strategy before any per-runtime epic depends on it.

This is discovery work. It collapses into **decidability**, not code: a recorded
decision on convergence vs thin-adapter fallback, the canonical plugin format,
and the MCP server scope — with the per-runtime epics (E3–E10) confirmed or
adjusted against the finding.

---

## Questions To Answer

1. **Canonical plugin format.** What does a minimal Mirror Mind Claude plugin
   (`.claude-plugin/plugin.json` bundling skills + hooks + MCP) look like, and
   does `claude` load and run it equivalently to the current standalone `.claude/`?
2. **Cross-runtime import — the bet.** Is plugin import actually real?
   - `agy plugin import claude` of the Mirror plugin
   - `grok plugin import` (claude/gemini source)
   - Codex marketplace install of an equivalent package
   What survives import (skills? hooks? MCP?) and what does not?
3. **MCP feasibility.** Can a Mirror MCP server carry the command surface and,
   critically, **Mirror Mode context injection** — or is MCP tool-call only, with
   per-turn injection still needing runtime hooks?
4. **Extensions on the package.** Can user-owned `prompt-skill` extensions ride
   the canonical plugin / MCP server so every runtime inherits them, closing the
   `.agents/` exposure gap structurally?
5. **Fallback shape.** If import is unreliable, what is the thin-adapter +
   shared-MCP fallback per runtime, and how much of the foundation still pays off?

---

## Scope

- Build a throwaway Mirror Mind plugin in an isolated scratch dir; `agy plugin
  validate` and Claude load-test it. No production mirror or repo state touched.
- Empirically test cross-runtime import on the installed CLIs (`agy`, `grok`,
  `codex`) against the scratch plugin.
- Prototype-probe a minimal Mirror MCP server (or desk-check the contract) for
  command surface + context injection feasibility.
- Decide: **converge** (canonical plugin + MCP as the spine) vs **thin adapters +
  shared MCP** fallback; fix the canonical format and MCP scope.
- Record the decision in `docs/project/decisions.md` and reconcile E2–E11.

Out of scope: building the production plugin or MCP server (that is E2), and any
per-runtime implementation.

## Candidate Stories

| Code | Story | Type | Outcome | Status |
|------|-------|------|---------|--------|
| CV21.E1.S1 | Canonical plugin authoring probe | Spike | A minimal Mirror plugin validates and load-tests on Claude in an isolated dir | 🟢 Active |
| CV21.E1.S2 | Cross-runtime import probe | Spike | Empirical result of importing the Mirror plugin into `agy`, `grok`, and Codex; what survives | 🟡 Planned |
| CV21.E1.S3 | Mirror MCP server feasibility | Spike | Whether MCP can carry the command surface and Mirror Mode context injection, or only tool calls | 🟡 Planned |
| CV21.E1.S4 | Convergence decision record | Decision | `decisions.md` entry choosing converge vs fallback, fixing canonical format + MCP scope; E2–E11 reconciled | 🟡 Planned |

---

## Done Condition

E1 is done when the convergence question is answered with empirical evidence, the
integration strategy is chosen and recorded as a decision, the canonical plugin
format and MCP scope are fixed, and the per-runtime epics (E2–E11) are confirmed
or adjusted to match — with no production mirror, repo state, or runtime config
mutated by the spike.

---

## References

- [CV21 — Runtime Expansion II](../index.md)
- [Runtime Interface Contract](../../../../product/specs/runtime-interface/index.md)
- [CV8 Runtime Expansion](../../cv8-runtime-expansion/index.md)
- Claude Code plugins: <https://docs.claude.com/en/docs/claude-code/plugins>
- Antigravity CLI: <https://github.com/google-antigravity/antigravity-cli>
- Codex hooks: <https://developers.openai.com/codex/hooks>
- Grok Build: <https://x.ai/cli>
