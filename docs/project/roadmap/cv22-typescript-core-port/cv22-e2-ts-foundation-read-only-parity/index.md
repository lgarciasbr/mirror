[< CV22 TypeScript Core Port](../index.md)

# CV22.E2 — TS Foundation & Read-Only Command Parity

**Epic:** Stand up the real TypeScript core and reach ordered/behavioral parity for the read-only, deterministic commands, validated on real-DB copies.
**Status:** 🟢 In Progress
**Depends on:** [CV22.E1 Hybrid-Search Parity Spike](../cv22-e1-hybrid-search-parity-spike/index.md) (done), the [database-seam strangler decision](../../../decisions.md), the [CV22 scaffolding decision](../../../decisions.md#cv22-typescript-core-scaffolding-nodesqlite-single-ts-package-node-24-biome)

---

## What This Is

E1 proved the riskiest assumption — that a TS reimplementation of the hybrid
ranker, reading the same SQLite file, reproduces Python's ordered results — but
it did so in a **throwaway spike** under `spikes/ts-search-parity/`. E2 is where
the strangler proper begins: a real, durable TS package that the rest of CV22
builds on.

E2 has two halves:

1. **Foundation** — stand up the `ts/` package skeleton: the `node:sqlite` driver
   seam, toolchain (TypeScript typecheck, Biome, `node:test`), BLOB/embedding
   read, the frozen-`now` golden contract, and a CI Node job. No Mirror command
   is ported in the foundation story; it just has to compile, lint, test, and open
   a database.
2. **Read-only command parity** — port the deterministic read commands the
   strangler can validate against the Python oracle on real-DB copies: `search`,
   `detect-persona`, journeys, and memory listing. Each command becomes a tested
   TS module whose ordered/behavioral output matches Python on a synthetic golden
   corpus (CI) and on a real-`memory.db` copy (manual pre-merge gate).

The spike's learnings (`parseUtcMs`, `blobToFloat32`, ordinal lexical scoring,
MMR dedup, frozen `now`) are **promoted** into properly-structured, tested
modules here — the spike itself stays as historical evidence and is not extended.

---

## Scaffolding Decisions (settled)

Recorded in [Decisions — CV22 TypeScript core scaffolding](../../../decisions.md#cv22-typescript-core-scaffolding-nodesqlite-single-ts-package-node-24-biome):

- **Driver:** `node:sqlite` behind a thin driver seam (no native build; swap stays cheap).
- **Layout:** a single top-level `ts/` package; no workspaces until a second publishable unit exists.
- **Node floor:** 24 LTS (`engines.node >= 24`).
- **Parity net:** committed synthetic goldens in CI; real-DB parity is a manual pre-merge gate.
- **Lint/format:** Biome. **Test runner:** built-in `node:test`. **Build:** deferred; run `.ts` directly, `tsc --noEmit` for typecheck.

---

## Stories

| Code | Story | Outcome | Status |
|------|-------|---------|--------|
| [CV22.E2.S1](cv22-e2-s1-ts-package-scaffold/index.md) | TS Package Scaffold & Driver Seam | A compiling, linted, tested `ts/` package with the `node:sqlite` driver seam (read-only DB open + query) and a CI Node job; no Mirror command ported yet | ✅ Done |
| CV22.E2.S2 | Golden-Corpus Contract & Frozen-`now` Harness | The language-agnostic oracle mechanism: a Python generator drives the real ranker with frozen `now` + frozen embeddings into committed synthetic goldens; TS verifier + BLOB/embedding decode consume them | ⚪ Provisional |
| CV22.E2.S3 | `search` Command Parity | The hybrid ranker, promoted from the spike into a tested TS module, reaches ordered parity on synthetic goldens (CI) and a real-DB copy (manual) | ⚪ Provisional |
| CV22.E2.S4 | `detect-persona` Parity | TS `detect-persona` reproduces the Python routing score/threshold decision on the golden corpus | ⚪ Provisional |
| CV22.E2.S5 | Journeys & Memory Listing Parity | TS read of journeys and memory listing reproduces Python's ordered/behavioral output on the golden corpus | ⚪ Provisional |

Only **S1 is fully specified** below. S2–S5 are a provisional decomposition of the
remaining E2 done condition, risk-ordered (contract before the commands that
depend on it). They will be specified and planned as the epic progresses; the
breakdown may change as S1 lands.

---

## Done Condition

- The `ts/` package exists, compiles (`tsc --noEmit`), lints (Biome), and tests
  (`node:test`) green; CI runs the Node job alongside Python.
- The `node:sqlite` driver seam opens a SQLite file read-only and queries it,
  with no other module importing `node:sqlite` directly.
- The frozen-`now` golden contract is in place and BLOB/embedding reads decode
  correctly.
- `search`, `detect-persona`, journeys, and memory listing reach proven
  ordered/behavioral parity with the Python oracle on synthetic goldens (CI) and
  on a real-`memory.db` copy (manual).
- Existing `memory.db` files work unchanged; the schema/FTS5 compatibility
  contract holds.

---

## Non-Goals

- No Pi front door yet (CV22.E3) — E2 produces a library, not a runtime surface.
- No write commands (CV22.E4).
- No external-API commands — extraction, embeddings, consult (CV22.E5).
- No schema or semantic change; FTS5/tokenizer behavior is inherited from the
  shared file.
- No npm build/publish pipeline or package rename (CV22.E6).
- No new Python features — Python is maintenance-only from the CV21.E2.S2 baseline.

---

## See also

- [CV22 index](../index.md)
- [CV22.E1 Hybrid-Search Parity Spike](../cv22-e1-hybrid-search-parity-spike/index.md)
- [Decisions — database-seam strangler](../../../decisions.md)
- [Decisions — CV22 scaffolding](../../../decisions.md#cv22-typescript-core-scaffolding-nodesqlite-single-ts-package-node-24-biome)
- Parity harness: [`spikes/ts-search-parity/`](../../../../../spikes/ts-search-parity/)
</content>
</invoke>
