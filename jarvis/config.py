"""Jarvis configuration — loads from .env or environment variables."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from jarvis directory
load_dotenv(Path(__file__).parent / ".env")

# API Keys
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "pNInz6obpgDQGcFmaJgB")  # Default: Adam

# Screen capture
REMOTE_PLAY_WINDOW_TITLE = "PS Remote Play"  # Window title to capture
CAPTURE_INTERVAL = 2.0  # Seconds between captures

# Claude vision
CLAUDE_MODEL = "claude-opus-4-20250514"
MAX_TOKENS = 1024

# Controller mode: "keyboard" (pyautogui to window) or "vgamepad" (virtual controller)
CONTROLLER_MODE = "keyboard"

# Dreams-specific
DREAMS_CONTEXT = """You are Jarvis, an AI assistant controlling a PlayStation 5 running Dreams.
Dreams is a game creation engine. You can sculpt, paint, animate, and build logic.

Current task context will be provided each loop. You see the screen via screenshots.
Respond with:
1. OBSERVE: What you see on screen (brief)
2. THINK: What you should do next and why
3. ACT: The specific controller actions to take (as a JSON list)
4. SAY: A brief Jarvis-style narration (1-2 sentences, spoken via TTS)

Controller actions use this format:
{"button": "X", "action": "press"} — tap a button
{"button": "X", "action": "hold", "duration": 0.5} — hold a button
{"stick": "left", "x": 0.5, "y": -0.3, "duration": 1.0} — move stick (range -1 to 1)
{"wait": 0.5} — pause between actions
"""
