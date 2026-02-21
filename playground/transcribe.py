import argparse
import os
import whisper
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Transcribe audio files using OpenAI Whisper.")
    parser.add_argument("audio_path", help="Path to the audio file to transcribe")
    parser.add_argument("--model", default="base", help="Model size: tiny, base, small, medium, large")
    parser.add_argument("--output_dir", help="Directory to save the transcript (defaults to same as audio file)")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu", help="Device to use (cuda or cpu)")
    
    args = parser.parse_args()

    # Validate input
    audio_path = Path(args.audio_path)
    if not audio_path.exists():
        print(f"Error: File not found: {audio_path}")
        sys.exit(1)

    print(f"Loading Whisper model '{args.model}'...")
    try:
        model = whisper.load_model(args.model, device=args.device)
    except Exception as e:
        print(f"Error loading model: {e}")
        sys.exit(1)

    print(f"Transcribing {audio_path}...")
    try:
        result = model.transcribe(str(audio_path))
    except Exception as e:
        print(f"Error during transcription: {e}")
        sys.exit(1)

    # Save results
    output_dir = Path(args.output_dir) if args.output_dir else audio_path.parent
    base_name = audio_path.stem
    
    txt_path = output_dir / f"{base_name}.txt"
    srt_path = output_dir / f"{base_name}.srt"

    # Write TXT
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(result["text"])
    
    print(f"Done! Saved to:\n- {txt_path}")
    print(f"Transcription preview: {result['text'][:100]}...")

import torch # Import usually handled at top, doing here to check availability for default arg
if __name__ == "__main__":
    main()
