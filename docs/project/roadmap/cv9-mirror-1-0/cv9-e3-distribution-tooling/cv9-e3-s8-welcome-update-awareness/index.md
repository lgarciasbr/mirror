[< CV9.E3 Distribution & Tooling](../index.md)

# CV9.E3.S8 — Welcome Update Awareness

**Epic:** CV9.E3 Distribution & Tooling
**Status:** ✅ Done
**User-visible outcome:** The welcome card shows the installed Mirror Mind version, warns when local refs show an update is available, and runtime update explains what changed after installation.

---

## What Changed

- `python -m memory welcome` now shows `Version <version>`.
- The welcome renders a no-network update notice when local git refs show the checkout is behind its configured upstream.
- `python -m memory runtime update` now includes an `Installed changes` summary after a successful fast-forward update.

---

## Boundaries

- The welcome does not contact the network. Fresh remote discovery remains the job of `runtime update --check` or `runtime update`.
- The post-install summary is commit-based (`git log <previous>..<new>`) until formal release notes exist for every versioned release.
- The update notice is informational; it does not mutate files, refs, backups, migrations, or the database.

---

## Verification

```bash
PYTHONPATH=src uv run pytest tests/unit/memory/cli/test_welcome.py tests/unit/memory/cli/test_runtime.py
uv run --extra dev ruff check src/ tests/
uv run --extra dev ruff format --check src/ tests/
uv run python -m memory welcome --mirror-home /Users/alissonvale/.mirror-minds/alisson-vale
```

---

## See also

- [Welcome Card Spec](../../../../../product/specs/welcome/index.md)
- [Runtime Self-Update Reference](../../../../../../REFERENCE.md#runtime-self-update)
