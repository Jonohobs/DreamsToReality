"""Controller input — sends PlayStation button/stick commands via keyboard to Remote Play."""

import json
import time

import pyautogui

# PS Remote Play keyboard mappings (default)
# These map to DualSense buttons when Remote Play window is focused
BUTTON_MAP = {
    # Face buttons
    "X": "enter",         # Cross / Confirm
    "CROSS": "enter",
    "CIRCLE": "escape",   # Circle / Back
    "SQUARE": "e",        # Square (mapped via Remote Play — may need config)
    "TRIANGLE": "q",      # Triangle
    # D-pad
    "UP": "up",
    "DOWN": "down",
    "LEFT": "left",
    "RIGHT": "right",
    # Shoulders
    "L1": "1",
    "R1": "2",
    "L2": "3",
    "R2": "4",
    # System
    "OPTIONS": "backspace",
    "SHARE": "\\",
    "TOUCHPAD": "tab",
    "PS": "home",
    # Sticks
    "L3": "5",            # Left stick click
    "R3": "6",            # Right stick click
}

# WASD for left stick, IJKL for right stick (approximate — keyboard can't do analog)
STICK_KEYS = {
    "left": {"up": "w", "down": "s", "left": "a", "right": "d"},
    "right": {"up": "i", "down": "k", "left": "j", "right": "l"},
}


def _focus_remote_play(window_title: str = "PS Remote Play") -> bool:
    """Bring the Remote Play window to front."""
    try:
        windows = pyautogui.getWindowsWithTitle(window_title)
        if windows:
            windows[0].activate()
            time.sleep(0.1)
            return True
    except Exception:
        pass
    return False


def press_button(button: str, duration: float = 0.0) -> None:
    """Press a controller button. Hold if duration > 0."""
    key = BUTTON_MAP.get(button.upper())
    if not key:
        print(f"[CONTROLLER] Unknown button: {button}")
        return

    if duration > 0:
        pyautogui.keyDown(key)
        time.sleep(duration)
        pyautogui.keyUp(key)
    else:
        pyautogui.press(key)
    print(f"[CONTROLLER] {button} {'held ' + str(duration) + 's' if duration else 'pressed'}")


def move_stick(stick: str, x: float, y: float, duration: float = 0.3) -> None:
    """Simulate analog stick with keyboard keys. x/y range: -1 to 1."""
    keys = STICK_KEYS.get(stick.lower())
    if not keys:
        print(f"[CONTROLLER] Unknown stick: {stick}")
        return

    held = []
    # Determine which keys to hold based on direction
    if y < -0.3:  # Up (inverted: negative y = up)
        held.append(keys["up"])
    elif y > 0.3:
        held.append(keys["down"])
    if x < -0.3:
        held.append(keys["left"])
    elif x > 0.3:
        held.append(keys["right"])

    if not held:
        return

    for k in held:
        pyautogui.keyDown(k)
    time.sleep(duration)
    for k in held:
        pyautogui.keyUp(k)
    print(f"[CONTROLLER] Stick {stick} ({x:.1f}, {y:.1f}) for {duration}s")


def execute_actions(actions: list[dict], window_title: str = "PS Remote Play") -> None:
    """Execute a list of controller actions.

    Each action is a dict like:
      {"button": "X", "action": "press"}
      {"button": "X", "action": "hold", "duration": 0.5}
      {"stick": "left", "x": 0.5, "y": -0.3, "duration": 1.0}
      {"wait": 0.5}
    """
    _focus_remote_play(window_title)

    for action in actions:
        if "wait" in action:
            time.sleep(action["wait"])

        elif "button" in action:
            duration = action.get("duration", 0.0)
            press_button(action["button"], duration)

        elif "stick" in action:
            move_stick(
                action["stick"],
                action.get("x", 0.0),
                action.get("y", 0.0),
                action.get("duration", 0.3),
            )

        # Small delay between actions
        time.sleep(0.05)


def parse_actions(text: str) -> list[dict]:
    """Try to extract a JSON action list from Claude's response."""
    # Look for JSON array in the text
    start = text.find("[")
    end = text.rfind("]")
    if start != -1 and end != -1:
        try:
            return json.loads(text[start : end + 1])
        except json.JSONDecodeError:
            pass
    return []


if __name__ == "__main__":
    print("Controller test — pressing X in 3 seconds (focus Remote Play!)")
    time.sleep(3)
    execute_actions([
        {"button": "X", "action": "press"},
        {"wait": 0.5},
        {"button": "CIRCLE", "action": "press"},
    ])
