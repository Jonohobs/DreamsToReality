import subprocess
import os
from pathlib import Path

frames_dir = Path("frames_test")
frames_dir.mkdir(exist_ok=True)

cmd = f'ffmpeg -i mushroom_house_hq.mp4 -vf "fps=2" {frames_dir}/frame_%04d.jpg -y'
print(f"Running: {cmd}")
try:
    subprocess.run(cmd, shell=True, check=True)
    print("Success!")
except subprocess.CalledProcessError as e:
    print(f"Failed with code {e.returncode}")
