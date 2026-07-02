# Mirror Mind — TypeScript Core

The TypeScript core of Mirror Mind, grown as a **database-seam strangler** of the
Python core in [`../src/memory/`](../src/memory). This package is the durable
transition state: it starts as a skeleton and dissolves the Python core one
command at a time behind a shared `memory.db`.

- Strategy: [Decisions — database-seam strangler](../docs/project/decisions.md#mirror-mind-ports-to-typescript-via-a-database-seam-strangler-not-a-rewrite)
- Scaffolding choices: [Decisions — CV22 scaffolding](../docs/project/decisions.md#cv22-typescript-core-scaffolding-nodesqlite-single-ts-package-node-24-biome)
- Roadmap: [CV22 — TypeScript Core Port](../docs/project/roadmap/cv22-typescript-core-port/index.md)

## Requirements

- **Node.js >= 24** (`engines.node`). The core relies on built-in `node:sqlite`
  (FTS5 + bm25, no native build) and Node's native TypeScript execution, so there
  is no compile step.

## Getting started

```bash
cd ts
npm ci          # install pinned dev dependencies (use `npm install` to refresh the lockfile)
npm run typecheck   # tsc --noEmit
npm run lint        # Biome check
npm test            # node:test
npm run format      # Biome format --write
```

## Conventions

- **No build step.** Source stays `.ts` and runs directly under Node. `tsconfig`
  sets `erasableSyntaxOnly`, so only erasable TypeScript is allowed (no enums,
  namespaces, or parameter properties) — this keeps native execution always valid.
- **The driver seam.** `src/db/database.ts` is the **only** module that imports
  `node:sqlite`. Everything else depends on the `Database` interface it exports,
  so swapping the driver later (e.g. `better-sqlite3`) rewrites just that file.
- **Zero runtime dependencies.** Testing uses the built-in `node:test`; SQLite is
  built in. Dev dependencies are TypeScript, `@types/node`, and Biome only.
- **Parity net.** Ported commands are validated against the Python oracle. CI runs
  parity over committed **synthetic** (PII-free) golden corpora; real-`memory.db`
  parity is a manual pre-merge gate and never enters CI.

## Layout

```
src/
  index.ts        # package entry point
  db/database.ts  # node:sqlite driver seam (read-only handle)
test/             # node:test suites
```

Seams mirror the Python core (`db`, and — as the port proceeds — `storage`,
`intelligence`, `services`, `cli`).
