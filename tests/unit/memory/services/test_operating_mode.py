"""Tests for explicit operating mode lifecycle state."""

from memory import MemoryClient
from memory.config import default_db_path_for_home
from memory.services.operating_mode import activate_mode, deactivate_mode, get_active_mode


def test_operating_mode_can_be_activated_and_deactivated(tmp_path):
    home = tmp_path / ".mirror" / "alisson-vale"
    mem = MemoryClient(db_path=default_db_path_for_home(home))

    activate_mode(mem.store, mode="Builder Mode", journey="explorer-mode")

    state = get_active_mode(mem.store)
    assert state is not None
    assert state.mode == "Builder Mode"
    assert state.label == "■ Builder Mode"
    assert state.journey == "explorer-mode"

    deactivate_mode(mem.store)

    assert get_active_mode(mem.store) is None


def test_operating_mode_does_not_pollute_sticky_journey_defaults(tmp_path):
    home = tmp_path / ".mirror" / "alisson-vale"
    mem = MemoryClient(db_path=default_db_path_for_home(home))

    activate_mode(mem.store, mode="Builder Mode", journey="explorer-mode")

    assert mem.store.get_latest_runtime_defaults() == (None, None)
