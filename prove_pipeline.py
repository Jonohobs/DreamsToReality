import os
import subprocess
import shutil
from pathlib import Path

# Paths
BASE_DIR = Path.cwd()
VIDEO_PATH = Path("mushroom_house_hq.mp4")
FRAMES_DIR = Path("frames_hq")
OUTPUT_DIR = Path("colmap_out_hq")
DATABASE_PATH = OUTPUT_DIR / "database.db"

# Tools (assuming they are in PATH after install)
COLMAP_BIN = BASE_DIR / "COLMAP/COLMAP-3.9.1-windows-cuda/COLMAP.bat"
FFMPEG_BIN = "ffmpeg"

def setup_dirs():
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def extract_frames():
    print(">>> Extracting frames...")
    # Ensure paths use forward slashes for the shell command
    vid_path = str(VIDEO_PATH).replace('\\', '/')
    out_pattern = (str(FRAMES_DIR) + "/frame_%04d.jpg").replace('\\', '/')
    cmd_str = f'"{FFMPEG_BIN}" -i "{vid_path}" -vf "fps=2" "{out_pattern}" -y'
    subprocess.run(cmd_str, shell=True, check=True)

def run_colmap_pipeline():
    print(">>> Running COLMAP automatic reconstructor...")
    # Using the automatic reconstructor for simplicity in this test
    cmd = [
        str(COLMAP_BIN), "automatic_reconstructor",
        "--workspace_path", str(OUTPUT_DIR),
        "--image_path", str(FRAMES_DIR),
        "--use_gpu", "1",
        "--FeatureExtraction.use_gpu", "1",
        "--FeatureMatching.use_gpu", "1",
        "--ImageReader.single_camera", "1",  # Consistency for single video source
        "--SiftExtraction.peak_threshold", "0.004",  # Lower threshold for soft Dreams flecks
        "--SiftExtraction.edge_threshold", "15"      # More lenient edge threshold
    ]
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    setup_dirs()
    extract_frames()
    run_colmap_pipeline()
    print(">>> Done! Check colmap_out/dense/0/fused.ply")
