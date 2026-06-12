"""Contained Ariad lifecycle operations for Builder Mode."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from memory.builder.delivery_cursor import (
    BuilderDeliveryCursor,
    get_delivery_cursor,
    set_delivery_cursor,
)
from memory.builder.lifecycle_ribbon import render_lifecycle_ribbon
from memory.storage.store import Store

_ALLOWED_PULL_LEVELS = ("delivery_story", "user_story", "technical_story")


@dataclass(frozen=True)
class BuilderLifecycleItem:
    code: str
    title: str
    level: str
    why_now: str


@dataclass(frozen=True)
class BuilderPullReport:
    journey: str
    method: str
    item: BuilderLifecycleItem
    cursor: BuilderDeliveryCursor
    next_event: str = "prepare"


@dataclass(frozen=True)
class BuilderPrepareReport:
    journey: str
    method: str
    active_item: str
    context_summary: tuple[str, ...]
    story_shape_assessment: str
    risks: tuple[str, ...]
    applicable_rules: tuple[str, ...]
    cursor: BuilderDeliveryCursor
    next_event: str = "plan"


def pull_lifecycle_item(
    store: Store,
    *,
    journey: str,
    method: str,
    item: BuilderLifecycleItem,
) -> BuilderPullReport:
    """Pull an item into active runtime cursor state without executing Prepare."""
    normalized_journey = _normalize_required(journey, "journey")
    normalized_method = _normalize_required(method, "method")
    normalized_item = _normalize_item(item)
    existing = get_delivery_cursor(store, normalized_journey)
    if existing is None:
        raise ValueError("delivery cursor is required before pull")
    cursor = set_delivery_cursor(
        store,
        journey=normalized_journey,
        method=normalized_method,
        active_item=normalized_item.code,
        active_checkpoint=None,
        pending_confirmation=None,
        last_delivery_event="pull",
    )
    return BuilderPullReport(
        journey=normalized_journey,
        method=normalized_method,
        item=normalized_item,
        cursor=cursor,
    )


def prepare_lifecycle_item(
    store: Store,
    *,
    journey: str,
    method: str,
    project_path: Path | None = None,
) -> BuilderPrepareReport:
    """Prepare the pulled item and stop before Plan."""
    normalized_journey = _normalize_required(journey, "journey")
    normalized_method = _normalize_required(method, "method")
    existing = get_delivery_cursor(store, normalized_journey)
    if existing is None:
        raise ValueError("delivery cursor is required before prepare")
    if not existing.active_item:
        raise ValueError("active item is required before prepare")

    cursor = set_delivery_cursor(
        store,
        journey=normalized_journey,
        method=normalized_method,
        active_item=existing.active_item,
        active_checkpoint=None,
        pending_confirmation=None,
        last_delivery_event="prepare",
    )
    return BuilderPrepareReport(
        journey=normalized_journey,
        method=normalized_method,
        active_item=existing.active_item,
        context_summary=_context_summary(project_path),
        story_shape_assessment=(
            "Pulled item is treated as an implementable Ariad work item. "
            "Granularity remains conservative until Plan confirms scope."
        ),
        risks=(
            "Scope may expand during Plan if the item mixes product and technical work.",
            "Implementation remains blocked until the Plan checkpoint is approved.",
        ),
        applicable_rules=(
            "Pull selects active work; Prepare reads terrain.",
            "Plan is the next event and requires Navigator approval before implementation.",
            "No Plan, Implement, Validation, Review, Coherence, or Done work is executed here.",
        ),
        cursor=cursor,
    )


def render_pull_report(report: BuilderPullReport) -> str:
    """Render an Ariad Pull report using Delivery Story Identified grammar."""
    code_parts = report.item.code.split(".")
    cv_code = code_parts[0] if code_parts else report.item.code
    ds_code = code_parts[-1] if len(code_parts) > 1 else report.item.code
    title = _title_leaf(report.item.title)
    return (
        "\n".join(
            [
                "Delivery",
                render_lifecycle_ribbon("pull"),
                "",
                "╭────────────────────────────────────────────────────────╮",
                "│        🟪■  DELIVERY STORY IDENTIFIED                  │",
                "│                                                        │",
                _card_text(title),
                "│                                                        │",
                _card_text("source"),
                _card_text("roadmap candidate"),
                "│                                                        │",
                _card_text("roadmap placement"),
                _card_text(f"🟪[{cv_code}] {_cv_title(report.item.title)}"),
                _card_text(f"  └─ 🟦[{ds_code}] {title}"),
                "│                                                        │",
                _card_text("intent"),
                *_card_wrapped(report.item.why_now),
                "│                                                        │",
                _card_text("commitment"),
                _card_text("pulled into active Delivery Work"),
                _card_text(f"active item: {report.cursor.active_item or 'none'}"),
                "│                                                        │",
                _card_text("next event"),
                _card_text(report.next_event.title()),
                "│                                                        │",
                _card_text("boundary"),
                _card_text("Prepare was not executed automatically."),
                _card_text("Plan and later lifecycle work were not executed."),
                "╰────────────────────────────────────────────────────────╯",
            ]
        )
        + "\n"
    )


def render_prepare_report(report: BuilderPrepareReport) -> str:
    """Render an Ariad Prepare report using field-reading grammar."""
    return (
        "\n".join(
            [
                "Delivery",
                render_lifecycle_ribbon("prepare"),
                "",
                "╭────────────────────────────────────────────────────────╮",
                "│        🧭  PREPARE FIELD READING                       │",
                "│                                                        │",
                _card_text("active item"),
                _card_text(f"🟦[{report.active_item}]"),
                "│                                                        │",
                _card_text("terrain read"),
                *_card_context_items(report.context_summary),
                "│                                                        │",
                _card_text("story shape"),
                *_card_wrapped(report.story_shape_assessment),
                "│                                                        │",
                _card_text("risks"),
                *_card_prefixed(report.risks, "✕"),
                "│                                                        │",
                _card_text("applicable rules"),
                *_card_prefixed(report.applicable_rules, "✓"),
                "│                                                        │",
                _card_text("next event"),
                _card_text(report.next_event.title()),
                "│                                                        │",
                _card_text("boundary"),
                _card_text("Plan was not created."),
                _card_text("Implementation remains blocked."),
                "╰────────────────────────────────────────────────────────╯",
            ]
        )
        + "\n"
    )


def _normalize_item(item: BuilderLifecycleItem) -> BuilderLifecycleItem:
    code = _normalize_required(item.code, "item code")
    title = _normalize_required(item.title, "item title")
    level = _normalize_required(item.level, "item level")
    why_now = _normalize_required(item.why_now, "why now")
    if level not in _ALLOWED_PULL_LEVELS:
        raise ValueError(f"item level must be one of {', '.join(_ALLOWED_PULL_LEVELS)}")
    return BuilderLifecycleItem(code=code, title=title, level=level, why_now=why_now)


def _context_summary(project_path: Path | None) -> tuple[str, ...]:
    if project_path is None:
        return ("No project path is configured; Prepare used runtime journey state only.",)
    root = project_path.expanduser().resolve()
    checks = (
        "README.md",
        "docs/project/roadmap/index.md",
        "docs/process/development-guide.md",
    )
    return tuple(f"{path}: {'present' if (root / path).exists() else 'missing'}" for path in checks)


def _format_list(items: tuple[str, ...]) -> list[str]:
    return [f"- {item}" for item in items] if items else ["none"]


def _card_text(text: str) -> str:
    width = 54
    return f"│ {text[:width]:<{width}} │"


def _card_context_items(items: tuple[str, ...]) -> list[str]:
    if not items:
        return [_card_text("none")]
    lines: list[str] = []
    for item in items:
        marker = "✓" if "present" in item else "○"
        lines.append(_card_text(f"{marker} {item}"))
    return lines


def _card_prefixed(items: tuple[str, ...], prefix: str) -> list[str]:
    if not items:
        return [_card_text("none")]
    lines: list[str] = []
    for item in items:
        wrapped = _card_wrapped(item)
        for index, line in enumerate(wrapped):
            content = line[2:56].rstrip()
            lines.append(_card_text(f"{prefix if index == 0 else ' '} {content}"))
    return lines


def _card_wrapped(text: str) -> list[str]:
    width = 54
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) > width and current:
            lines.append(_card_text(current))
            current = word
        else:
            current = candidate
    if current:
        lines.append(_card_text(current))
    return lines or [_card_text("none")]


def _title_leaf(title: str) -> str:
    return title.split("/")[-1].strip()


def _cv_title(title: str) -> str:
    return title.split("/")[0].strip()


def _normalize_required(value: str, field_name: str) -> str:
    normalized = value.strip() if isinstance(value, str) else ""
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized
