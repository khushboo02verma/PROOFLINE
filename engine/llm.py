"""Optional Claude client. The engine runs fully offline; with --llm and an API key, the extractor
and writer agents call Claude with the prompts in prompts/. Every LLM output still goes through the
same deterministic verifier, so the model can propose text but cannot get an untraceable claim out."""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

MODEL = os.environ.get("CASE_ENGINE_MODEL", "claude-opus-5-5")
PROMPTS = Path(__file__).resolve().parent.parent / "prompts"


def available() -> bool:
    try:
        import anthropic  # noqa: F401
    except ImportError:
        return False
    return bool(os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN"))


def prompt(name: str) -> str:
    return (PROMPTS / f"{name}.md").read_text(encoding="utf-8")


def call(system_prompt_name: str, user_content: str, max_tokens: int = 16000) -> str:
    import anthropic

    client = anthropic.Anthropic()
    response = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=prompt(system_prompt_name),
        messages=[{"role": "user", "content": user_content}],
        output_config={"effort": "high"},
    )
    if response.stop_reason == "refusal":
        raise RuntimeError(f"Model declined the {system_prompt_name} request")
    if response.stop_reason == "max_tokens":
        raise RuntimeError(f"{system_prompt_name} output hit max_tokens; raise the limit or split the input")
    return "".join(b.text for b in response.content if b.type == "text")


def call_json(system_prompt_name: str, user_content: str, max_tokens: int = 16000):
    text = call(system_prompt_name, user_content, max_tokens)
    match = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    return json.loads(match.group(1) if match else text)
