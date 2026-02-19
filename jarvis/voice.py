"""Voice — 11Labs TTS for Jarvis narration."""

import io
import threading

from .config import ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID

# Lazy imports — only load audio deps when actually speaking
_player_lock = threading.Lock()


def speak(text: str, block: bool = False) -> None:
    """Speak text via 11Labs TTS. Non-blocking by default."""
    if not ELEVENLABS_API_KEY:
        print(f"[JARVIS] {text}")
        return

    if block:
        _speak_sync(text)
    else:
        t = threading.Thread(target=_speak_sync, args=(text,), daemon=True)
        t.start()


def _speak_sync(text: str) -> None:
    """Synchronous TTS playback."""
    try:
        from elevenlabs import ElevenLabs

        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        audio_gen = client.text_to_speech.convert(
            voice_id=ELEVENLABS_VOICE_ID,
            text=text,
            model_id="eleven_turbo_v2_5",
        )

        # Collect audio bytes
        audio_bytes = b"".join(audio_gen)

        # Play via pygame (lightweight, no ffmpeg needed)
        with _player_lock:
            _play_audio(audio_bytes)

    except ImportError:
        print(f"[JARVIS] (elevenlabs not installed) {text}")
    except Exception as e:
        print(f"[JARVIS] (TTS error: {e}) {text}")


def _play_audio(audio_bytes: bytes) -> None:
    """Play audio bytes. Tries pygame first, falls back to saving file."""
    try:
        import pygame
        pygame.mixer.init()
        sound = pygame.mixer.Sound(io.BytesIO(audio_bytes))
        sound.play()
        while pygame.mixer.get_busy():
            pygame.time.wait(50)
    except ImportError:
        # Fallback: save and play with system player
        import subprocess
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            f.write(audio_bytes)
            tmp_path = f.name
        subprocess.run(
            ["powershell", "-Command", f"(New-Object Media.SoundPlayer '{tmp_path}').PlaySync()"],
            capture_output=True,
        )


def speak_print(text: str) -> None:
    """Print and speak — always prints, speaks if TTS available."""
    print(f"[JARVIS] {text}")
    speak(text)


if __name__ == "__main__":
    speak_print("Hello Jonathan. Jarvis online. Ready to build in Dreams.")
