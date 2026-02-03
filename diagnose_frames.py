import cv2
import glob
import os
import time
import numpy as np
from pathlib import Path

# Path to frames
frames_dir = Path("c:/Users/jonat/dreams-to-reality/data_v1/raw_frames")
frame_files = sorted(list(frames_dir.glob("frame_*.png")))

# Sample 20 frames from across the video
sample_indices = np.linspace(0, len(frame_files)-1, 20, dtype=int)
sample_frames = [frame_files[i] for i in sample_indices]

print(f"Analyzing {len(sample_frames)} sample frames...\n")

total_time = 0

for frame_path in sample_frames:
    start_time = time.time()
    
    img = cv2.imread(str(frame_path))
    if img is None:
        continue
        
    # Check Blur (Laplacian Variance)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    # Check UI (Simple Color/Edge heuristic from preprocess.py mostly)
    # Replicating logic briefly to time it
    height, width = img.shape[:2]
    ui_roi = img[0:int(height * 0.2), :]
    edges = cv2.Canny(ui_roi, 100, 200)
    edge_ratio = np.sum(edges > 0) / edges.size
    
    end_time = time.time()
    duration = end_time - start_time
    total_time += duration
    
    print(f"Frame: {frame_path.name}")
    print(f"  Blur Score: {blur_score:.2f}")
    print(f"  UI Edge Ratio: {edge_ratio:.4f}")
    print(f"  Time: {duration:.4f}s")
    print("-" * 20)

print(f"\nAverage Time per Frame: {total_time / len(sample_frames):.4f}s")
