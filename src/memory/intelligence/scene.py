"""Scene synthesis for cognitive-location Workspace surfaces."""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

from memory.config import EXTRACTION_MODEL
from memory.intelligence.llm_router import LLMResponse, send_to_model

SCENE_SYNTHESIS_PROMPT = """
You are writing a grounded cognitive-location orientation for Mirror Mind.

Use only the provided Scene read model. Do not invent journeys, goals, emotions,
priorities, facts, or relationships. If signals are thin, say so. Prefer meaning
over metrics. Mention whether this is a global Scene or a focused Scene.

Return JSON only with this shape:
{
  "title": "A warm, human orientation title; avoid generic labels like Global Scene Orientation or Focused Scene Orientation",
  "summary": "One or two readable paragraphs, separated with a blank line if useful.",
  "signals": ["Grounded signal used", "Another grounded signal used"],
  "next": "A gentle suggested next move, or an uncertainty statement if no next move is grounded."
}
""".strip()


def generate_scene_synthesis(
    scene: dict[str, Any],
    *,
    on_llm_call: Callable[[LLMResponse], None] | None = None,
) -> dict[str, Any]:
    """Generate a bounded structured Scene orientation from a deterministic read model."""
    prompt = (
        SCENE_SYNTHESIS_PROMPT
        + "\n\nScene read model:\n"
        + json.dumps(
            scene,
            ensure_ascii=False,
            indent=2,
        )
    )
    try:
        response = send_to_model(
            EXTRACTION_MODEL,
            [{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=700,
        )
    except Exception:
        return {}
    if on_llm_call:
        on_llm_call(response)
    content = response.content.strip()
    payload = _parse_orientation_json(content)
    return payload if payload is not None else {"summary": content}


def _parse_orientation_json(content: str) -> dict[str, Any] | None:
    """Parse model JSON even when wrapped in Markdown fences or prose."""
    cleaned = content.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()
        if cleaned.startswith("json"):
            cleaned = cleaned[4:].strip()
    candidates = [cleaned]
    first = cleaned.find("{")
    last = cleaned.rfind("}")
    if first != -1 and last != -1 and first < last:
        candidates.append(cleaned[first : last + 1])
    for candidate in candidates:
        try:
            payload = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            return payload
    return None
