[< Story](index.md)

# Test Guide — CV23.DS8

## Aggregate Validation

1. Focused TDD proves same-directory, one-parent, multi-parent, confined
   directory, canonical escape, absolute, URI-like, backslash, symlink escape,
   missing target, and last-valid preservation cases.
2. An isolated fixture reproduces the Nautilus CV package linking a root-level
   Delivery Story and rebuilds through the public source CLI.
3. Existing Operational schema, exact golden, publication, refresh, and
   subprocess concurrency tests remain green.
4. Current Nautilus source compiles read-only without modifying its projection.
5. Immutable consumer-kit hashes and all 16 self-tests remain unchanged.
6. After explicit release authorization, central CI, installed-runtime rebuild,
   manifest inspection, and Operational snapshot advancement open the return
   gate.

## Child Work Packages

- CV23.DS8.TS1

## Navigator Validation

The Nautilus agent runs its unchanged repository-baseline/rebuild route against
the installed patch. Pass means the command exits zero, `operational.json`
advances to current Ariad truth, manifest inspection names the new snapshot, and
TD-001 can close. Any stale snapshot, unbounded path acceptance, altered source,
or workaround link rewrite fails validation.

## Validation Evidence

Source implementation evidence complete:

- 31 focused Operational compiler tests pass, including the full confinement
  matrix, directory symlink escape, and missing-target last-valid preservation.
- Public isolated `rebuild-operational` regression passes through the guarded
  CLI fixture.
- 117 projection/CLI unit and subprocess integration tests pass.
- The complete Python suite passes.
- Ruff over `src` and `tests`, format, focused mypy, docs links, and diff checks
  pass. A repository-wide Ruff invocation additionally reports four unrelated
  pre-existing findings under `spikes/ts-search-parity/`; release scope does not
  absorb that spike debt.
- Current Nautilus Harness source compiles read-only as three roots (`CV-001`,
  `CV-002`, `CV-003`) with source revision
  `sha256:bb06244597f3d4f78815f0195d5cfa233932dcefc37d61488aebaed03baa2645`;
  consumer projection files and worktree remain unchanged.
- Consumer-kit hashes remain unchanged and all 16 self-tests pass.

Pending hard gates: release authorization, central CI, stable installation,
unchanged Nautilus rebuild/inspection, snapshot advancement, and consumer-owned
TD-001 closure.
