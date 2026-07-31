[< Project](../briefing.md)

# ES-004 Windows Desktop Frame (mirror.exe)

**Status:** Open — Experiment 1 in progress
**Source:** Windows adoption work that produced the native installer (PR #26), plus a Builder/Explorer conversation on 2026-07-31 that converged on a desktop frame design ("Fusão A+C")
**Current attractor:** A native Windows desktop app that makes Mirror + Pi adoption effortless — install, understand, converse — without changing Mirror core
**Delivery handoff:** not yet — promotion to a Capability Value is the exit condition of this story

---

## Initial Signal

Mirror's hardest adoption barrier on Windows is not conversation quality — it is
everything before the first conversation:

1. **Installing** — solved by the native installer (PR #26, Inno Setup).
2. **Starting** — creating the OpenRouter account, connecting model
   subscriptions (Pi `/login`), choosing models (`/model`). Users get lost here.
3. **Understanding** — modes (Mirror, Builder, Explorer, Soul) and personas
   (engineer, coach, therapist…) are invisible until discovered by accident.

The installer removed barrier 1. Barriers 2 and 3 remain, and they are
experience problems, not runtime problems.

## Thickened Story

The proposed answer is a thin native Windows frame ("Fusão A+C") around the
existing Pi terminal experience:

- **A single window with tabs** (Warp-like). Each tab is a real Pi TUI session
  running under ConPTY, launched exactly as `installer/launcher/mirror.cmd`
  launches it today (same cwd, PATH, UTF-8 environment). Tabs map naturally to
  journeys — multi-project work becomes a native concept.
- **First run opens a guided wizard as the initial tab** (identity → OpenRouter
  key → subscription connect → personas tour → first conversation). The wizard
  reuses `installer/configure.ps1` and `installer/health-check.ps1`; the Inno
  installer keeps installing bits, the frame takes over data collection.
- **A Setup surface** rendered as traffic lights over the real health checks,
  with actions that only ever call existing CLI commands (allowlisted argv,
  following the `command_executor.py` pattern). Pi-owned flows (`/login`,
  `/model`) are orchestrated in a terminal tab, never reimplemented.
- **A living glossary** of modes and personas, generated from the user's own
  database (`memory identity list/get`), with a "try it" box backed by
  `memory detect-persona`.

The frame is orchestration only. Mirror core does not change.

## Premises (Navigator-set, non-negotiable)

1. **Fully Windows compatible** — CI-enforced upstream (windows-latest, Pester,
   path-safety tests); the frame adds ConPTY (Win10 1809+).
2. **Ships through the existing installer** — the frame joins `mirror.iss` as a
   component; per-user, no admin.
3. **Native updates without reinstall** — Mirror updates via
   `memory runtime update` (git checkout preserved by design), Pi via
   `npm install -g @earendil-works/pi-coding-agent@latest`. The frame is the
   only layer without native update, acceptable because it is thin and rarely
   changes.
4. **Maximum test coverage, TDD, plus executable simulators** for known use
   cases (mold: ShadowAIGuard/RansomGuard) — every non-trivial story gets
   `plan.md` + `test-guide.md` before implementation; use-case simulators live
   under `spikes/` and exit 0 on green.
5. **Base = latest upstream stable** (v0.31.5 at exploration start); the end
   goal is an upstream PR, so everything follows upstream structure and
   conventions.

## Feasibility Evidence (from code reading, 2026-07-31)

- Multi-process SQLite access is the designed case: WAL + `busy_timeout=30s`
  (`src/memory/db/connection.py`). Multiple tabs are multiple processes of a
  kind Mirror already supports.
- The Pi→Mirror logging contract (`.pi/extensions/mirror-logger.ts`) spawns
  `uv run python` detached with cwd-based `.env` discovery — preserved as long
  as the frame launches sessions like `mirror.cmd` does.
- `installer/bootstrap.ps1` states the update invariant explicitly: the product
  is a git clone *"required so `runtime update` keeps working"*.
- **Known gap:** the DB bootstrap lock uses `fcntl` (POSIX) and degrades to a
  no-op on Windows. Frame mitigation: serialized warm-up (`runtime status`)
  before opening tabs. Definitive fix: a small upstream PR using
  `msvcrt.locking` — a good early, standalone contribution.
- Frame rules derived from risk analysis: update only with zero open sessions;
  `.env` edits apply to new sessions; UTF-8 no BOM everywhere; graceful
  session shutdown (Ctrl+C) before kill.

## Experiment 1 — Public functional mockup (first delivery)

A fully navigable, simulated prototype of the Fusão A+C experience, published
publicly on Vercel, to collect Navigator-level feedback (Alisson, Vinicius)
before any construction:

- Wizard: all six steps clickable with simulated states.
- Frame: tabs, scripted Pi conversation showing persona activation and mode
  context, status bar.
- Setup: interactive traffic lights mirroring real health-check items.
- Glossary: modes + personas with a simulated detect-persona "try it".
- Location: `spikes/windows-frame-mockup/` (static, no build step required).
- Exit condition: feedback captured back into this story (thickening), decision
  to promote, pivot, or drop.

## Delivery Hypothesis (post-promotion shape)

If promoted, a new CV ("Windows Desktop Frame") with epics roughly:

| Epic | Slice | Content |
|------|-------|---------|
| E0 | Spike | ConPTY + xterm.js hosting real Pi+Mirror; 2 concurrent sessions; abrupt kill; warm-up; Tauri vs Electron decision |
| E1 | Frame v0 | Window + one embedded session tab |
| E2 | First-run wizard | configure.ps1 orchestration, onboarding |
| E3 | Setup surface | health-check traffic lights + actions |
| E4 | Living glossary | identity list / detect-persona integration |
| E5 | Multi-tab | sessions ↔ journeys |
| E6 | Update UX | runtime update + Pi npm update, gated on zero sessions |
| E7 | Installer | frame as a `mirror.iss` component |
| E8 | Hardening + PR | test-guides complete, CI, upstream PR |

Each story follows upstream practice: `plan.md` + `test-guide.md` before code,
TDD, and use-case simulators under `spikes/`.

## Open Decisions

- Frame stack: Tauri vs Electron — decided by E0 spike, not by preference.
- Mockup language: PT-BR first (presentation audience); EN before upstream PR.
- Commit trailer convention for this fork (RansomGuard ADR-15 forbids AI
  trailers; upstream has no stated rule) — Navigator to confirm.
- Code signing for public distribution — deferred, testers first.
