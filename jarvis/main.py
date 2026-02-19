"""Jarvis main loop — Observe → Think → Act → Speak.

Usage:
    # Watch-only mode (no controller actions sent)
    python -m jarvis.main --watch

    # Full control mode
    python -m jarvis.main --task "Sculpt a mushroom house"

    # Single observation (screenshot + describe)
    python -m jarvis.main --once
"""

import argparse
import json
import time
import sys

from .screen import capture_and_encode
from .brain import think, observe_only
from .controller import execute_actions
from .voice import speak_print
from .config import ANTHROPIC_API_KEY, CAPTURE_INTERVAL


def run_loop(task: str, watch_only: bool = False, interval: float = CAPTURE_INTERVAL) -> None:
    """Main Jarvis loop."""
    if not ANTHROPIC_API_KEY:
        print("ERROR: Set ANTHROPIC_API_KEY in jarvis/.env")
        print("Copy .env.example to .env and fill in your keys.")
        sys.exit(1)

    speak_print(f"Jarvis online. {'Watch mode' if watch_only else 'Control mode'}.")
    if task:
        speak_print(f"Task: {task}")

    history: list[dict] = []
    step = 0

    try:
        while True:
            step += 1
            print(f"\n{'='*60}")
            print(f"Step {step} | {time.strftime('%H:%M:%S')}")
            print(f"{'='*60}")

            # 1. CAPTURE
            b64, window_found = capture_and_encode()
            if not window_found:
                print("[SCREEN] Remote Play window not found — capturing full screen")

            # 2. THINK
            result = think(b64, task=task, history=history[-6:])  # Keep last 3 exchanges

            print(f"\n[OBSERVE] {result['observe']}")
            print(f"[THINK]   {result['think']}")
            print(f"[ACT]     {json.dumps(result['act'], indent=2) if result['act'] else 'No actions'}")
            print(f"[SAY]     {result['say']}")

            # 3. SPEAK
            if result["say"]:
                speak_print(result["say"])

            # 4. ACT (only in control mode)
            if not watch_only and result["act"]:
                print("\n[EXECUTING ACTIONS...]")
                execute_actions(result["act"])
            elif result["act"]:
                print("\n[WATCH MODE — actions not sent]")

            # 5. Update history for context continuity
            history.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": f"Task: {task}"},
                    {
                        "type": "image",
                        "source": {"type": "base64", "media_type": "image/jpeg", "data": b64},
                    },
                ],
            })
            history.append({
                "role": "assistant",
                "content": result["raw"],
            })

            # Wait before next cycle
            print(f"\n[NEXT CYCLE in {interval}s — Ctrl+C to stop]")
            time.sleep(interval)

    except KeyboardInterrupt:
        speak_print("Jarvis going offline. Good session, Jonathan.")


def run_once(task: str = "What do you see on screen?") -> None:
    """Single observation — capture, describe, done."""
    if not ANTHROPIC_API_KEY:
        print("ERROR: Set ANTHROPIC_API_KEY in jarvis/.env")
        sys.exit(1)

    b64, found = capture_and_encode()
    print(f"Window found: {found}")
    desc = observe_only(b64, task)
    print(f"\n{desc}")
    speak_print(desc[:200])  # Speak first 200 chars


def main():
    parser = argparse.ArgumentParser(description="Jarvis — AI copilot for Dreams")
    parser.add_argument("--task", default="Explore and describe what you see in Dreams.",
                        help="What should Jarvis help with")
    parser.add_argument("--watch", action="store_true",
                        help="Watch-only mode — no controller actions sent")
    parser.add_argument("--once", action="store_true",
                        help="Single observation, then exit")
    parser.add_argument("--interval", type=float, default=CAPTURE_INTERVAL,
                        help=f"Seconds between cycles (default: {CAPTURE_INTERVAL})")
    args = parser.parse_args()

    if args.once:
        run_once(args.task)
    else:
        run_loop(args.task, watch_only=args.watch, interval=args.interval)


if __name__ == "__main__":
    main()
