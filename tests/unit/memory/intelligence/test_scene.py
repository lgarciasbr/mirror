from memory.intelligence.llm_router import LLMResponse
from memory.intelligence.scene import generate_scene_synthesis


def test_generate_scene_synthesis_parses_structured_json(monkeypatch) -> None:
    captured = {}

    def fake_send(model, messages, temperature, max_tokens):
        captured["messages"] = messages
        return LLMResponse(
            model=model,
            content="""{
              "title": "A warmer moment",
              "summary": "The scene is grounded.",
              "signals": ["Recent conversation"],
              "next": "Validate the surface."
            }""",
        )

    monkeypatch.setattr("memory.intelligence.scene.send_to_model", fake_send)

    result = generate_scene_synthesis(
        {"mode": "global", "signals": [{"title": "Recent conversation"}]}
    )

    assert result == {
        "title": "A warmer moment",
        "summary": "The scene is grounded.",
        "signals": ["Recent conversation"],
        "next": "Validate the surface.",
    }
    prompt = captured["messages"][0]["content"]
    assert "Use only the provided Scene read model" in prompt
    assert "Recent conversation" in prompt


def test_generate_scene_synthesis_parses_json_wrapped_in_markdown(monkeypatch) -> None:
    def fake_send(model, messages, temperature, max_tokens):
        return LLMResponse(
            model=model,
            content="""```json
{"title":"Wrapped","summary":"Readable summary.","signals":[],"next":"Continue."}
```""",
        )

    monkeypatch.setattr("memory.intelligence.scene.send_to_model", fake_send)

    result = generate_scene_synthesis({"mode": "focused"})

    assert result["title"] == "Wrapped"
    assert result["summary"] == "Readable summary."


def test_generate_scene_synthesis_returns_empty_payload_on_failure(monkeypatch) -> None:
    def fake_send(model, messages, temperature, max_tokens):
        raise RuntimeError("offline")

    monkeypatch.setattr("memory.intelligence.scene.send_to_model", fake_send)

    assert generate_scene_synthesis({"mode": "global"}) == {}
