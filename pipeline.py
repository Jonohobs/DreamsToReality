import os
import argparse
import shutil
import zipfile
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

def create_zip_archive(source_dir: Path, output_zip: Path):
    """Create a ZIP archive of the preprocessed frames."""
    print(f"Creating ZIP archive: {output_zip}...")
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in source_dir.glob("*.png"):
            zipf.write(file, arcname=file.name)
    print("ZIP archive created successfully.")

def main():
    parser = argparse.ArgumentParser(description='Dreams Photogrammetry/NeRF Pipeline')
    parser.add_argument('video_path', type=Path, help='Path to input video file')
    parser.add_argument('project_dir', type=Path, help='Project working directory')
    parser.add_argument('--mode', choices=['meshroom', 'nerf', 'splat'], default='meshroom', 
                        help='Processing mode: meshroom (detail), nerf (volumetric), or splat (AI-enhanced 3DGS)')
    parser.add_argument('--zip', action='store_true', help='Export clean frames as a ZIP archive')
    parser.add_argument('--fps', type=int, default=2, help='Frames per second to extract (default: 2)')
    parser.add_argument('--sharpen', action='store_true', help='Enable image sharpening')
    parser.add_argument('--denoise', action='store_true', help='Enable denoising')
    
    args = parser.parse_args()
    
    # 1. Setup paths
    raw_frames_dir = args.project_dir / "raw_frames"
    clean_frames_dir = args.project_dir / "clean_frames"
    
    # 2. Extract
    # Check if we already have frames extracted to save time
    existing_frames = list(raw_frames_dir.glob("*.png"))
    if len(existing_frames) > 100:
        print(f"\nFound {len(existing_frames)} existing frames in {raw_frames_dir}")
        print("Skipping extraction step (delete folder to force re-extraction).")
    else:
        # Calculate frame interval based on video FPS and target FPS
        cap = cv2.VideoCapture(str(args.video_path))
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()
        interval = max(1, int(video_fps / args.fps))
        extract_frames(args.video_path, raw_frames_dir, every_n_frames=interval)
    
    # 3. Preprocess
    print(f"\nStarting preprocessing (Mode: {args.mode})...")
    
    # Dreams-specific defaults
    # Meshroom: High threshold, needs sharp details
    # NeRF/Splat: Volumetric, more forgiving of blur
    min_blur = 3.0 if args.mode == 'meshroom' else 1.5
    duplicate_thresh = 0.98 if args.mode == 'meshroom' else 0.95
    
    # AI Enhancements:
    # Splat mode defaults to using enhancements to recover "fleck" detail
    use_sharpen = args.sharpen or (args.mode == 'splat')
    use_denoise = args.denoise or (args.mode == 'splat')
    
    # Meshroom also benefits, but we leave it optional/manual for now unless flagged
    if args.mode == 'meshroom' and (args.sharpen or args.denoise):
        print("Note: Applying AI filters for Meshroom (Experimental)")

    stats = preprocess_frames(
        input_dir=raw_frames_dir,
        output_dir=clean_frames_dir,
        skip_ui=True,
        min_blur_score=min_blur,
        duplicate_threshold=duplicate_thresh,
        sharpen=use_sharpen,
        denoise=use_denoise
    )
    
    # 4. Export ZIP
    # Splat and NeRF modes always generate a ZIP for cloud upload
    if args.zip or args.mode in ['nerf', 'splat']:
        zip_path = args.project_dir / f"clean_frames_{args.mode}.zip"
        create_zip_archive(clean_frames_dir, zip_path)
    
    print("\nPipeline Complete!")
    if args.mode == 'meshroom':
        print(f"Ready for Meshroom: {clean_frames_dir}")
    else:
        print(f"Ready for Luma AI / Polycam (3DGS): {zip_path}")

if __name__ == '__main__':
    main()
