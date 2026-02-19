"""Brain — Claude Opus vision for interpreting Dreams screen and deciding actions."""

import json
import re

import anthropic

from .config import ANTHROPIC_API_KEY, CLAUDE_MODEL, DREAMS_CONTEXT, MAX_TOKENS


client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def think(
    screenshot_b64: str,
    task: str = "Explore the current scene and describe what you see.",
    history: list[dict] | None = None,
) -> dict:
    """Send a screenshot to Claude and get back observations + actions.

    Returns dict with keys: observe, think, act (list of actions), say (TTS text), raw
    """
    messages = []

    # Add conversation history for continuity
    if history:
        messages.extend(history)

    # Current turn: screenshot + task
    messages.append({
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": screenshot_b64,
                },
            },
            {
                "type": "text",
                "text": f"Current task: {task}\n\nWhat do you see? What should we do? Respond with OBSERVE, THINK, ACT, SAY sections.",
            },
        ],
    })

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=MAX_TOKENS,
        system=DREAMS_CONTEXT,
        messages=messages,
    )

    raw = response.content[0].text
    return parse_response(raw)


def parse_response(text: str) -> dict:
    """Parse Claude's structured response into components."""
    result = {"observe": "", "think": "", "act": [], "say": "", "raw": text}

    # Extract sections
    sections = {"OBSERVE": "observe", "THINK": "think", "ACT": "act", "SAY": "say"}
    for label, key in sections.items():
        pattern = rf"{label}:\s*(.*?)(?=(?:OBSERVE|THINK|ACT|SAY):|$)"
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            result[key] = match.group(1).strip()

    # Parse ACT section into action list
    if isinstance(result["act"], str):
        act_text = result["act"]
        # Try to find JSON array
        bracket_start = act_text.find("[")
        bracket_end = act_text.rfind("]")
        if bracket_start != -1 and bracket_end != -1:
            try:
                result["act"] = json.loads(act_text[bracket_start : bracket_end + 1])
            except json.JSONDecodeError:
                result["act"] = []
        else:
            result["act"] = []

    return result


def observe_only(screenshot_b64: str, question: str = "What do you see on screen?") -> str:
    """Just describe what's on screen — no actions. Cheaper/simpler."""
    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=512,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": screenshot_b64,
                    },
                },
                {"type": "text", "text": question},
            ],
        }],
    )
    return response.content[0].text


if __name__ == "__main__":
    from .screen import capture_and_encode
    b64, found = capture_and_encode()
    print(f"Window found: {found}")
    desc = observe_only(b64)
    print(f"\nClaude sees:\n{desc}")
