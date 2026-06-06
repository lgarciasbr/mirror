"""Operating mode lifecycle state.

Operating modes are explicit Mirror lenses such as Builder Mode and, later,
Explorer Mode. This service stores only the active mode context. Rendering or
clearing runtime UI is a caller concern.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from memory.storage.store import Store

MODE_ICONS = {
    "Mirror Mode": "◌",
    "Builder Mode": "■",
    "Explorer Mode": "△",
}

MODE_STATE_SESSION_ID = "__global_operating_mode__"


@dataclass(frozen=True)
class OperatingModeState:
    mode: str
    journey: str | None = None

    @property
    def label(self) -> str:
        icon = MODE_ICONS.get(self.mode)
        return f"{icon} {self.mode}" if icon else self.mode


def activate_mode(store: Store, *, mode: str, journey: str | None = None) -> OperatingModeState:
    """Activate an operating mode and return the stored state."""
    normalized_mode = mode.strip()
    if not normalized_mode:
        raise ValueError("mode must not be empty")
    normalized_journey = journey.strip() if isinstance(journey, str) and journey.strip() else None
    state = OperatingModeState(mode=normalized_mode, journey=normalized_journey)
    store.upsert_runtime_session(
        MODE_STATE_SESSION_ID,
        metadata=json.dumps(
            {
                "active_mode": state.mode,
                "active_journey": state.journey,
            },
            ensure_ascii=False,
        ),
        active=True,
    )
    return state


def deactivate_mode(store: Store) -> None:
    """Deactivate the current operating mode.

    This clears only the dedicated operating-mode state row. It does not mutate
    Mirror sticky persona/journey defaults or conversation routing.
    """
    store.upsert_runtime_session(
        MODE_STATE_SESSION_ID,
        metadata=None,
        active=False,
    )


def get_active_mode(store: Store) -> OperatingModeState | None:
    """Return active operating mode state, if one exists."""
    session = store.get_runtime_session(MODE_STATE_SESSION_ID)
    if not session or not session.active or not session.metadata:
        return None
    try:
        data = json.loads(session.metadata)
    except json.JSONDecodeError:
        return None
    mode = data.get("active_mode")
    if not isinstance(mode, str) or not mode.strip():
        return None
    journey = data.get("active_journey")
    return OperatingModeState(
        mode=mode.strip(),
        journey=journey.strip() if isinstance(journey, str) and journey.strip() else None,
    )
