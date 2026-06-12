import pytest

from memory import MemoryClient
from memory.builder.delivery_cursor import get_delivery_cursor, set_delivery_cursor
from memory.builder.lifecycle import (
    BuilderLifecycleItem,
    prepare_lifecycle_item,
    pull_lifecycle_item,
    render_prepare_report,
    render_pull_report,
)
from memory.config import default_db_path_for_home


def _store(tmp_path):
    mirror_home = tmp_path / ".mirror" / "pati"
    db_path = default_db_path_for_home(mirror_home)
    client = MemoryClient(env="test", db_path=db_path)
    return client, client.store


def test_pull_lifecycle_item_updates_cursor_and_renders_report(tmp_path):
    _client, store = _store(tmp_path)
    set_delivery_cursor(store, journey="sandbox-pet-store", method="ariad")

    report = pull_lifecycle_item(
        store,
        journey="sandbox-pet-store",
        method="ariad",
        item=BuilderLifecycleItem(
            code="CHECKOUT-FLOW",
            title="Checkout Flow",
            level="user_story",
            why_now="next candidate capability",
        ),
    )

    cursor = get_delivery_cursor(store, "sandbox-pet-store")
    assert cursor is not None
    assert cursor.active_item == "CHECKOUT-FLOW"
    assert cursor.last_delivery_event == "pull"
    rendered = render_pull_report(report)
    assert "Ariad: ◉ Pull | ○ Prepare | ○ Plan" in rendered
    assert "DELIVERY STORY IDENTIFIED" in rendered
    assert "roadmap candidate" in rendered
    assert "roadmap placement" in rendered
    assert "🟪[CHECKOUT-FLOW] Checkout Flow" in rendered
    assert "pulled into active Delivery Work" in rendered
    assert "active item: CHECKOUT-FLOW" in rendered
    assert "Prepare" in rendered
    assert "Plan and later lifecycle work were not executed" in rendered


def test_pull_lifecycle_item_requires_existing_cursor(tmp_path):
    _client, store = _store(tmp_path)

    with pytest.raises(ValueError, match="delivery cursor"):
        pull_lifecycle_item(
            store,
            journey="sandbox-pet-store",
            method="ariad",
            item=BuilderLifecycleItem(
                code="CHECKOUT-FLOW",
                title="Checkout Flow",
                level="user_story",
                why_now="next candidate capability",
            ),
        )


def test_pull_lifecycle_item_rejects_unknown_level(tmp_path):
    _client, store = _store(tmp_path)
    set_delivery_cursor(store, journey="sandbox-pet-store", method="ariad")

    with pytest.raises(ValueError, match="item level"):
        pull_lifecycle_item(
            store,
            journey="sandbox-pet-store",
            method="ariad",
            item=BuilderLifecycleItem(
                code="CHECKOUT-FLOW",
                title="Checkout Flow",
                level="epic",
                why_now="next candidate capability",
            ),
        )


def test_prepare_lifecycle_item_updates_cursor_and_renders_report(tmp_path):
    project = tmp_path / "project"
    (project / "docs/project/roadmap").mkdir(parents=True)
    (project / "docs/process").mkdir(parents=True)
    (project / "README.md").write_text("# Project\n", encoding="utf-8")
    (project / "docs/project/roadmap/index.md").write_text("# Roadmap\n", encoding="utf-8")
    _client, store = _store(tmp_path)
    set_delivery_cursor(
        store,
        journey="sandbox-pet-store",
        method="ariad",
        active_item="CHECKOUT-FLOW",
        last_delivery_event="pull",
    )

    report = prepare_lifecycle_item(
        store,
        journey="sandbox-pet-store",
        method="ariad",
        project_path=project,
    )

    cursor = get_delivery_cursor(store, "sandbox-pet-store")
    assert cursor is not None
    assert cursor.active_item == "CHECKOUT-FLOW"
    assert cursor.last_delivery_event == "prepare"
    rendered = render_prepare_report(report)
    assert "Ariad: ✓ Pull | ◉ Prepare | ○ Plan" in rendered
    assert "PREPARE FIELD READING" in rendered
    assert "🟦[CHECKOUT-FLOW]" in rendered
    assert "✓ README.md: present" in rendered
    assert "○ docs/process/development-guide.md: missing" in rendered
    assert "story shape" in rendered
    assert "risks" in rendered
    assert "applicable rules" in rendered
    assert "Plan" in rendered
    assert "Plan was not created" in rendered


def test_prepare_lifecycle_item_requires_active_item(tmp_path):
    _client, store = _store(tmp_path)
    set_delivery_cursor(store, journey="sandbox-pet-store", method="ariad")

    with pytest.raises(ValueError, match="active item"):
        prepare_lifecycle_item(store, journey="sandbox-pet-store", method="ariad")
