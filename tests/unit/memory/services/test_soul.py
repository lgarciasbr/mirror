"""Tests for Soul Mode provisional state."""

from memory import MemoryClient
from memory.config import default_db_path_for_home
from memory.services.soul import (
    clear_fruit_in_maturation,
    clear_harvested_fruit,
    get_fruit_in_maturation,
    get_harvested_fruit,
    harvest_fruit,
    set_fruit_in_maturation,
)


def _mem(tmp_path):
    mirror_home = tmp_path / ".mirror" / "alisson-vale"
    return MemoryClient(db_path=default_db_path_for_home(mirror_home))


def test_fruit_in_maturation_defaults_to_empty(tmp_path):
    mem = _mem(tmp_path)

    state = get_fruit_in_maturation(mem.store)

    assert state.session_id == "__global_soul_mode__"
    assert state.fruit is None


def test_set_fruit_in_maturation_stores_provisional_fruit(tmp_path):
    mem = _mem(tmp_path)

    state = set_fruit_in_maturation(
        mem.store,
        "Belonging cannot be bought by becoming necessary.",
    )

    assert state.fruit == "Belonging cannot be bought by becoming necessary."
    assert get_fruit_in_maturation(mem.store).fruit == state.fruit


def test_set_fruit_replaces_previous_fruit(tmp_path):
    mem = _mem(tmp_path)

    set_fruit_in_maturation(mem.store, "First fruit.")
    set_fruit_in_maturation(mem.store, "Second fruit.")

    assert get_fruit_in_maturation(mem.store).fruit == "Second fruit."


def test_clear_fruit_in_maturation_removes_provisional_fruit(tmp_path):
    mem = _mem(tmp_path)
    set_fruit_in_maturation(mem.store, "A fruit.")

    clear_fruit_in_maturation(mem.store)

    assert get_fruit_in_maturation(mem.store).fruit is None


def test_fruit_in_maturation_can_be_session_scoped(tmp_path):
    mem = _mem(tmp_path)

    set_fruit_in_maturation(mem.store, "Global fruit.")
    set_fruit_in_maturation(mem.store, "Session fruit.", session_id="pi-session")

    assert get_fruit_in_maturation(mem.store).fruit == "Global fruit."
    assert get_fruit_in_maturation(mem.store, session_id="pi-session").fruit == "Session fruit."


def test_harvest_fruit_closes_fruit_in_maturation(tmp_path):
    mem = _mem(tmp_path)
    set_fruit_in_maturation(mem.store, "A provisional fruit.")

    state = harvest_fruit(mem.store)

    assert state.fruit == "A provisional fruit."
    assert get_harvested_fruit(mem.store).fruit == "A provisional fruit."
    assert get_fruit_in_maturation(mem.store).fruit is None


def test_harvest_fruit_can_use_explicit_final_fruit(tmp_path):
    mem = _mem(tmp_path)
    set_fruit_in_maturation(mem.store, "A provisional fruit.")

    state = harvest_fruit(mem.store, fruit="A final fruit.")

    assert state.fruit == "A final fruit."
    assert get_harvested_fruit(mem.store).fruit == "A final fruit."


def test_clear_harvested_fruit_removes_final_fruit(tmp_path):
    mem = _mem(tmp_path)
    harvest_fruit(mem.store, fruit="A final fruit.")

    clear_harvested_fruit(mem.store)

    assert get_harvested_fruit(mem.store).fruit is None
