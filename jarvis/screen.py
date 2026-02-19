"""Screen capture — grabs frames from the PS Remote Play window."""

import base64
import io
import time

import mss
import pyautogui
from PIL import Image


def find_remote_play_window(title: str = "PS Remote Play") -> dict | None:
    """Find the PS Remote Play window and return its bounding box."""
    try:
        windows = pyautogui.getWindowsWithTitle(title)
        if not windows:
            return None
        win = windows[0]
        return {"left": win.left, "top": win.top, "width": win.width, "height": win.height}
    except Exception:
        return None


def capture_screen(bbox: dict | None = None) -> Image.Image:
    """Capture a screenshot. If bbox given, capture that region; otherwise full screen."""
    with mss.mss() as sct:
        if bbox:
            monitor = bbox
        else:
            monitor = sct.monitors[1]  # Primary monitor
        screenshot = sct.grab(monitor)
        return Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")


def image_to_base64(img: Image.Image, max_size: int = 1024) -> str:
    """Resize and encode image to base64 for Claude API."""
    # Resize to save tokens
    img.thumbnail((max_size, max_size), Image.LANCZOS)
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=80)
    return base64.standard_b64encode(buffer.getvalue()).decode("utf-8")


def capture_and_encode(window_title: str = "PS Remote Play", max_size: int = 1024) -> tuple[str, bool]:
    """Capture the Remote Play window (or full screen) and return base64 + whether window was found."""
    bbox = find_remote_play_window(window_title)
    img = capture_screen(bbox)
    b64 = image_to_base64(img, max_size)
    return b64, bbox is not None


if __name__ == "__main__":
    b64, found = capture_and_encode()
    print(f"Window found: {found}")
    print(f"Base64 length: {len(b64)}")
    # Save preview
    img_data = base64.b64decode(b64)
    with open("preview.jpg", "wb") as f:
        f.write(img_data)
    print("Saved preview.jpg")
