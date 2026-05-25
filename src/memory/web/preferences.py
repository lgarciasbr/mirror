"""User-home preferences for the local Mirror web surface."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

Perspective = Literal["atlas", "workspace"]
ThemePreference = Literal["system", "light", "dark"]
DEFAULT_PERSPECTIVE: Perspective = "workspace"
VALID_PERSPECTIVES: tuple[Perspective, ...] = ("atlas", "workspace")
DEFAULT_THEME: ThemePreference = "system"
VALID_THEMES: tuple[ThemePreference, ...] = ("system", "light", "dark")
DEFAULT_AVATAR_SYMBOL = "◇"


@dataclass(frozen=True)
class WebProfile:
    display_name: str
    avatar_symbol: str

    def to_dict(self) -> dict[str, str]:
        return {"displayName": self.display_name, "avatarSymbol": self.avatar_symbol}


@dataclass(frozen=True)
class PreferenceRead:
    default_perspective: Perspective | None
    profile: WebProfile
    theme: ThemePreference
    warning: str | None = None


class WebPreferenceStore:
    """Persist web preferences in the user's Mirror home."""

    def __init__(self, mirror_home: str | Path | None) -> None:
        self.mirror_home = Path(mirror_home).expanduser() if mirror_home is not None else None

    @property
    def path(self) -> Path | None:
        if self.mirror_home is None:
            return None
        return self.mirror_home / "web" / "preferences.json"

    def read(self) -> PreferenceRead:
        default_profile = self._default_profile()
        path = self.path
        if path is None:
            return PreferenceRead(
                default_perspective=DEFAULT_PERSPECTIVE,
                profile=default_profile,
                theme=DEFAULT_THEME,
                warning="Mirror home is not configured; preferences cannot be persisted.",
            )
        if not path.exists():
            return PreferenceRead(
                default_perspective=DEFAULT_PERSPECTIVE,
                profile=default_profile,
                theme=DEFAULT_THEME,
            )

        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            return PreferenceRead(
                default_perspective=DEFAULT_PERSPECTIVE,
                profile=default_profile,
                theme=DEFAULT_THEME,
                warning=f"Preferences could not be read: {exc}",
            )

        value = payload.get("default_perspective") if isinstance(payload, dict) else None
        safe_payload = payload if isinstance(payload, dict) else {}
        profile = self._profile_from_payload(safe_payload)
        theme = self._theme_from_payload(safe_payload)
        if value in VALID_PERSPECTIVES:
            return PreferenceRead(default_perspective=value, profile=profile, theme=theme)
        return PreferenceRead(
            default_perspective=DEFAULT_PERSPECTIVE,
            profile=profile,
            theme=theme,
            warning="Default perspective preference is invalid; falling back to Workspace.",
        )

    def write_default_perspective(self, perspective: str) -> PreferenceRead:
        if perspective not in VALID_PERSPECTIVES:
            raise ValueError("default_perspective must be 'atlas' or 'workspace'")
        payload = self._read_payload_for_write()
        payload["default_perspective"] = perspective
        self._write_payload(payload)
        return self.read()

    def write_theme(self, theme: str) -> PreferenceRead:
        if theme not in VALID_THEMES:
            raise ValueError("theme must be 'system', 'light', or 'dark'")
        payload = self._read_payload_for_write()
        payload["theme"] = theme
        self._write_payload(payload)
        return self.read()

    def write_profile(self, display_name: str, avatar_symbol: str) -> PreferenceRead:
        display_name = display_name.strip()
        avatar_symbol = avatar_symbol.strip()
        if not display_name:
            raise ValueError("displayName is required")
        if len(display_name) > 80:
            raise ValueError("displayName must be at most 80 characters")
        if not avatar_symbol:
            avatar_symbol = DEFAULT_AVATAR_SYMBOL
        if len(avatar_symbol) > 4:
            raise ValueError("avatarSymbol must be at most 4 characters")
        payload = self._read_payload_for_write()
        payload["profile"] = {
            "display_name": display_name,
            "avatar_symbol": avatar_symbol,
        }
        self._write_payload(payload)
        return self.read()

    def _default_profile(self) -> WebProfile:
        name = self.mirror_home.name if self.mirror_home is not None else "Mirror"
        return WebProfile(display_name=name, avatar_symbol=DEFAULT_AVATAR_SYMBOL)

    def _theme_from_payload(self, payload: dict[str, Any]) -> ThemePreference:
        theme = payload.get("theme")
        return theme if theme in VALID_THEMES else DEFAULT_THEME

    def _profile_from_payload(self, payload: dict[str, Any]) -> WebProfile:
        default = self._default_profile()
        profile = payload.get("profile")
        if not isinstance(profile, dict):
            return default
        display_name = profile.get("display_name")
        avatar_symbol = profile.get("avatar_symbol")
        return WebProfile(
            display_name=display_name
            if isinstance(display_name, str) and display_name
            else default.display_name,
            avatar_symbol=avatar_symbol
            if isinstance(avatar_symbol, str) and avatar_symbol
            else default.avatar_symbol,
        )

    def _read_payload_for_write(self) -> dict[str, Any]:
        path = self.path
        if path is None:
            raise OSError("Mirror home is not configured")
        if not path.exists():
            return {}
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
        return payload if isinstance(payload, dict) else {}

    def _write_payload(self, payload: dict[str, Any]) -> None:
        path = self.path
        if path is None:
            raise OSError("Mirror home is not configured")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
