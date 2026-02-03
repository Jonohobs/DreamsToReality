import os
import subprocess
import shutil
from pathlib import Path

# Paths
BASE_DIR = Path.cwd()
VIDEO_PATH = BASE_DIR / "mushroom_house.mp4"
FRAMES_DIR = BASE_DIR / "frames"
OUTPUT_DIR = BASE_DIR / "colmap_out"
DATABASE_PATH = OUTPUT_DIR / "database.db"

# Tools (assuming they are in PATH after install)
COLMAP_BIN = BASE_DIR / "COLMAP/COLMAP-3.9.1-windows-cuda/COLMAP.bat"
FFMPEG_BIN = r"C:\Users\jonat\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin\ffmpeg.exe"

def setup_dirs():
    if not FRAMES_DIR.exists():
        FRAMES_DIR.mkdir()
    if not OUTPUT_DIR.exists():
        OUTPUT_DIR.mkdir()

def extract_frames():
    print(">>> Extracting frames...")
    # Extract at 2 FPS to get good overlap but not too many images
    cmd = [
        FFMPEG_BIN, "-i", str(VIDEO_PATH),
        "-vf", "fps=2", 
        str(FRAMES_DIR / "frame_%04d.jpg"),
        "-y"
    ]
    subprocess.run(cmd, check=True)

def run_colmap_pipeline():
    print(">>> Running COLMAP automatic reconstructor...")
    # Using the automatic reconstructor for simplicity in this test
    cmd = [
        COLMAP_BIN, "automatic_reconstructor",
        "--workspace_path", str(OUTPUT_DIR),
        "--image_path", str(FRAMES_DIR),
        "--use_gpu", "1"  # Force GPU usage
    ]
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    setup_dirs()
    extract_frames()
    run_colmap_pipeline()
    print(">>> Done! Check colmap_out/dense/0/fused.ply")
