"""Soul Mode provisional session state."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any

from memory.storage.store import Store

SOUL_STATE_SESSION_ID = "__global_soul_mode__"
SOUL_METADATA_KEY = "soul"
FRUIT_METADATA_KEY = "fruit_in_maturation"
HARVEST_METADATA_KEY = "harvested_fruit"


@dataclass(frozen=True)
class SoulFruitState:
    session_id: str
    fruit: str | None = None


def resolve_soul_session_id(explicit_session_id: str | None = None) -> str:
    if explicit_session_id and explicit_session_id.strip():
        return explicit_session_id.strip()
    env_session = os.environ.get("MIRROR_SESSION_ID", "").strip()
    return env_session or SOUL_STATE_SESSION_ID


def get_fruit_in_maturation(
    store: Store,
    *,
    session_id: str | None = None,
) -> SoulFruitState:
    resolved_session_id = resolve_soul_session_id(session_id)
    session = store.get_runtime_session(resolved_session_id)
    metadata = _decode_metadata(session.metadata if session else None)
    soul = metadata.get(SOUL_METADATA_KEY)
    fruit = soul.get(FRUIT_METADATA_KEY) if isinstance(soul, dict) else None
    return SoulFruitState(
        session_id=resolved_session_id,
        fruit=fruit.strip() if isinstance(fruit, str) and fruit.strip() else None,
    )


def set_fruit_in_maturation(
    store: Store,
    fruit: str,
    *,
    session_id: str | None = None,
) -> SoulFruitState:
    normalized_fruit = fruit.strip()
    if not normalized_fruit:
        raise ValueError("fruit must not be empty")

    resolved_session_id = resolve_soul_session_id(session_id)
    session = store.get_runtime_session(resolved_session_id)
    metadata = _decode_metadata(session.metadata if session else None)
    soul = metadata.get(SOUL_METADATA_KEY)
    if not isinstance(soul, dict):
        soul = {}
    soul[FRUIT_METADATA_KEY] = normalized_fruit
    metadata[SOUL_METADATA_KEY] = soul
    store.upsert_runtime_session(
        resolved_session_id,
        metadata=json.dumps(metadata, ensure_ascii=False),
        active=True,
    )
    return SoulFruitState(session_id=resolved_session_id, fruit=normalized_fruit)


def clear_fruit_in_maturation(
    store: Store,
    *,
    session_id: str | None = None,
) -> None:
    _clear_soul_key(store, key=FRUIT_METADATA_KEY, session_id=session_id)


def get_harvested_fruit(
    store: Store,
    *,
    session_id: str | None = None,
) -> SoulFruitState:
    resolved_session_id = resolve_soul_session_id(session_id)
    session = store.get_runtime_session(resolved_session_id)
    metadata = _decode_metadata(session.metadata if session else None)
    soul = metadata.get(SOUL_METADATA_KEY)
    fruit = soul.get(HARVEST_METADATA_KEY) if isinstance(soul, dict) else None
    return SoulFruitState(
        session_id=resolved_session_id,
        fruit=fruit.strip() if isinstance(fruit, str) and fruit.strip() else None,
    )


def harvest_fruit(
    store: Store,
    *,
    fruit: str | None = None,
    session_id: str | None = None,
) -> SoulFruitState:
    resolved_session_id = resolve_soul_session_id(session_id)
    final_fruit = fruit.strip() if isinstance(fruit, str) and fruit.strip() else None
    if final_fruit is None:
        final_fruit = get_fruit_in_maturation(store, session_id=resolved_session_id).fruit
    if not final_fruit:
        raise ValueError("harvested fruit must not be empty")

    session = store.get_runtime_session(resolved_session_id)
    metadata = _decode_metadata(session.metadata if session else None)
    soul = metadata.get(SOUL_METADATA_KEY)
    if not isinstance(soul, dict):
        soul = {}
    soul[HARVEST_METADATA_KEY] = final_fruit
    soul.pop(FRUIT_METADATA_KEY, None)
    metadata[SOUL_METADATA_KEY] = soul
    store.upsert_runtime_session(
        resolved_session_id,
        metadata=json.dumps(metadata, ensure_ascii=False),
        active=True,
    )
    return SoulFruitState(session_id=resolved_session_id, fruit=final_fruit)


def clear_harvested_fruit(
    store: Store,
    *,
    session_id: str | None = None,
) -> None:
    _clear_soul_key(store, key=HARVEST_METADATA_KEY, session_id=session_id)


def _clear_soul_key(store: Store, *, key: str, session_id: str | None) -> None:
    resolved_session_id = resolve_soul_session_id(session_id)
    session = store.get_runtime_session(resolved_session_id)
    if not session:
        return
    metadata = _decode_metadata(session.metadata)
    soul = metadata.get(SOUL_METADATA_KEY)
    if isinstance(soul, dict):
        soul.pop(key, None)
        if soul:
            metadata[SOUL_METADATA_KEY] = soul
        else:
            metadata.pop(SOUL_METADATA_KEY, None)
    store.upsert_runtime_session(
        resolved_session_id,
        metadata=json.dumps(metadata, ensure_ascii=False) if metadata else None,
    )


def _decode_metadata(raw: str | None) -> dict[str, Any]:
    if not raw:
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}
