"""Read-only configuration overview for the local Mirror web surface."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from memory import config
from memory.cli.common import db_path_from_mirror_home
from memory.config import (
    default_backup_dir_for_home,
    default_export_dir_for_home,
    default_extensions_dir_for_home,
    default_transcript_export_dir_for_home,
)


@dataclass(frozen=True)
class ConfigurationItem:
    label: str
    value: str
    description: str
    exists: bool | None = None

    def to_dict(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "label": self.label,
            "value": self.value,
            "description": self.description,
        }
        if self.exists is not None:
            payload["exists"] = self.exists
        return payload


@dataclass(frozen=True)
class ConfigurationSection:
    id: str
    title: str
    description: str
    items: list[ConfigurationItem]

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "items": [item.to_dict() for item in self.items],
        }


@dataclass(frozen=True)
class ConfigurationOverview:
    title: str
    description: str
    sections: list[ConfigurationSection]

    def to_dict(self) -> dict[str, object]:
        return {
            "title": self.title,
            "description": self.description,
            "sections": [section.to_dict() for section in self.sections],
        }


def build_configuration_overview(mirror_home: str | Path | None) -> ConfigurationOverview:
    """Build a non-sensitive, read-only configuration summary."""

    home = Path(mirror_home).expanduser().resolve() if mirror_home else None
    db_path = db_path_from_mirror_home(home) if home else None
    backup_dir = default_backup_dir_for_home(home) if home else None
    export_dir = default_export_dir_for_home(home) if home else None
    transcript_dir = default_transcript_export_dir_for_home(home) if home else None
    extensions_dir = default_extensions_dir_for_home(home) if home else None

    sections = [
        ConfigurationSection(
            id="mirror-home",
            title="Mirror home",
            description="Local filesystem boundary for the active Mirror.",
            items=[
                _path_item("Mirror home", home, "Directory that owns this Mirror's local state."),
                _path_item("Database", db_path, "SQLite database used by the active web session."),
                _path_item(
                    "Preferences",
                    home / "web" / "preferences.json" if home else None,
                    "Web preferences scoped to this Mirror.",
                ),
            ],
        ),
        ConfigurationSection(
            id="local-dirs",
            title="Local directories",
            description="Default local directories derived from the active Mirror home.",
            items=[
                _path_item("Backups", backup_dir, "Default location for Mirror backups."),
                _path_item("Exports", export_dir, "Default location for user exports."),
                _path_item(
                    "Transcripts", transcript_dir, "Default location for transcript exports."
                ),
                _path_item(
                    "Extensions", extensions_dir, "Local extension directory for this Mirror."
                ),
            ],
        ),
        ConfigurationSection(
            id="runtime",
            title="Runtime defaults",
            description="Non-sensitive runtime defaults visible to the local web app.",
            items=[
                ConfigurationItem(
                    "Environment", config.MEMORY_ENV, "Selected Mirror runtime environment."
                ),
                ConfigurationItem(
                    "Memory search model",
                    config.EMBEDDING_MODEL,
                    "Model used to turn memories into vectors for semantic search and retrieval.",
                ),
                ConfigurationItem(
                    "Memory extraction model",
                    config.EXTRACTION_MODEL,
                    "Default model used when Mirror extracts structured memories from text.",
                ),
                ConfigurationItem(
                    "LLM audit logging",
                    "enabled" if config.LOG_LLM_CALLS else "disabled",
                    "When enabled, Mirror records LLM calls for local audit/debugging evidence.",
                ),
                ConfigurationItem(
                    "Conversation routing",
                    "enabled" if config.RECEPTION_ENABLED else "disabled",
                    "When enabled, Mirror can classify incoming turns for persona/journey routing instead of relying only on simple keyword heuristics.",
                ),
            ],
        ),
    ]
    return ConfigurationOverview(
        title="Configuration overview",
        description="Read-only, non-sensitive configuration for the active local Mirror.",
        sections=sections,
    )


def _path_item(label: str, path: Path | None, description: str) -> ConfigurationItem:
    if path is None:
        return ConfigurationItem(
            label=label, value="Not configured", description=description, exists=None
        )
    return ConfigurationItem(
        label=label,
        value=str(path),
        description=description,
        exists=path.exists(),
    )
