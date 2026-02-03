
"""
Dreams to Reality: Automated Pipeline

1. Extracts frames from video files
2. Runs the preprocessor to filter bad frames
3. Prepares data for Meshroom
"""

import os
import argparse
from pathlib import Path
import cv2
from preprocess import preprocess_frames

def extract_frames(video_path: Path, output_dir: Path, every_n_frames: int = 1) -> int:
    """Extract frames from video file."""
    if not video_path.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")
        
    output_dir.mkdir(parents=True, exist_ok=True)
    
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {video_path}")
        
    count = 0
    saved = 0
    
    print(f"Extracting frames from {video_path.name}...")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        if count % every_n_frames == 0:
            frame_path = output_dir / f"frame_{saved:06d}.png"
            cv2.imwrite(str(frame_path), frame)
            saved += 1
            
        count += 1
        
    cap.release()
    print(f"Extracted {saved} frames.")
    return saved

def main():
    parser = argparse.ArgumentParser(description='Dreams Photogrammetry Pipeline')
    parser.add_argument('video_path', type=Path, help='Path to input video file')
    parser.add_argument('project_dir', type=Path, help='Project working directory')
    
    args = parser.parse_args()
    
    # 1. Setup paths
    raw_frames_dir = args.project_dir / "raw_frames"
    clean_frames_dir = args.project_dir / "clean_frames"
    
    # 2. Extract
    # Step 1: Extract Frames
    # Check if we already have frames extracted to save time
    existing_frames = list(raw_frames_dir.glob("*.png"))
    if len(existing_frames) > 100:
        print(f"\nExample found {len(existing_frames)} existing frames in {raw_frames_dir}")
        print("Skipping extraction step (delete folder to force re-extraction).")
    else:
        extract_frames(args.video_path, raw_frames_dir)
    
    # 3. Preprocess
    print("\nStarting preprocessing...")
    stats = preprocess_frames(
        input_dir=raw_frames_dir,
        output_dir=clean_frames_dir,
        skip_ui=True,
        min_blur_score=100.0,
        duplicate_threshold=0.98
    )
    
    print("\nPipeline Complete!")
    print(f"Ready for Meshroom: {clean_frames_dir}")

if __name__ == '__main__':
    main()
