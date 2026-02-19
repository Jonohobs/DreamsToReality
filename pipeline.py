import os
import argparse
import shutil
import zipfile
from pathlib import Path
import cv2
import numpy as np
from preprocess import preprocess_frames
from segment import segment_frames, validate_segment_model, VALID_SEGMENT_MODELS
from reconstruct import detect_gpu, run_reconstruction

SEGMENT_MODEL_CHOICES = VALID_SEGMENT_MODELS

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

def mask_corner_artifacts(frames_dir: Path, margin: int = 80) -> int:
    """Zero out faint light artifacts in frame corners (Dreams rendering artifact)."""
    fixed = 0
    for f in sorted(frames_dir.glob("*.png")):
        img = cv2.imread(str(f))
        if img is None:
            continue
        h, w = img.shape[:2]
        roi = img[h-margin:, w-margin*3:]
        if np.any(roi > 0):
            img[h-margin:, w-margin*3:] = 0
            cv2.imwrite(str(f), img)
            fixed += 1
    return fixed

def auto_crop_frames(frames_dir: Path, padding: float = 0.10, threshold: int = 3) -> dict:
    """Crop all frames to the union bounding box of non-black content.

    Scans every frame to find the maximum extent the object reaches,
    then crops all frames to that region plus padding. Keeps dimensions
    consistent across all frames (required for photogrammetry).

    Returns dict with crop stats.
    """
    files = sorted(frames_dir.glob("*.png"))
    if not files:
        return {"cropped": 0, "skipped": True}

    # Pass 1: find union bounding box
    global_min_y, global_min_x = 99999, 99999
    global_max_y, global_max_x = 0, 0
    img_h, img_w = 0, 0

    for f in files:
        img = cv2.imread(str(f))
        if img is None:
            continue
        img_h, img_w = img.shape[:2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        coords = np.where(gray > threshold)
        if len(coords[0]) == 0:
            continue
        global_min_y = min(global_min_y, coords[0].min())
        global_max_y = max(global_max_y, coords[0].max())
        global_min_x = min(global_min_x, coords[1].min())
        global_max_x = max(global_max_x, coords[1].max())

    if global_min_y >= global_max_y or global_min_x >= global_max_x:
        return {"cropped": 0, "skipped": True}

    # Add padding
    obj_w = global_max_x - global_min_x
    obj_h = global_max_y - global_min_y
    pad_x = int(obj_w * padding)
    pad_y = int(obj_h * padding)

    x1 = max(0, global_min_x - pad_x)
    y1 = max(0, global_min_y - pad_y)
    x2 = min(img_w, global_max_x + pad_x)
    y2 = min(img_h, global_max_y + pad_y)

    crop_w, crop_h = x2 - x1, y2 - y1

    original_pixels = img_w * img_h
    cropped_pixels = crop_w * crop_h
    reduction = (original_pixels - cropped_pixels) / original_pixels

    # Pass 2: crop all frames in-place
    cropped = 0
    for f in files:
        img = cv2.imread(str(f))
        if img is None:
            continue
        cropped_img = img[y1:y2, x1:x2]
        cv2.imwrite(str(f), cropped_img)
        cropped += 1

    return {
        "cropped": cropped,
        "skipped": False,
        "original_size": f"{img_w}x{img_h}",
        "cropped_size": f"{crop_w}x{crop_h}",
        "reduction_pct": round(reduction * 100, 1),
        "crop_region": (x1, y1, x2, y2),
    }

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
    parser.add_argument('--no-segment', action='store_true', help='Skip background removal')
    parser.add_argument('--no-duplicate-filter', action='store_true',
                        help='Skip duplicate detection (needed for black-background turntable captures)')
    parser.add_argument('--segment-model', default='u2net',
                        choices=['u2net', 'u2net_human_seg', 'isnet-general-use'],
                        help='Segmentation model (default: u2net)')
    parser.add_argument('--save-masks', action='store_true', help='Save segmentation masks for debugging')
    parser.add_argument('--mask-artifacts', action='store_true',
                        help='Zero out corner light artifacts (Dreams rendering bug)')
    parser.add_argument('--no-auto-crop', action='store_true',
                        help='Skip automatic cropping to union bounding box')
    parser.add_argument('--crop-padding', type=float, default=0.10,
                        help='Padding around crop region as fraction (default: 0.10 = 10%%)')
    parser.add_argument('--reconstruct', action='store_true',
                        help='Run COLMAP sparse reconstruction after frame prep')
    parser.add_argument('--dense', action='store_true',
                        help='Also run dense MVS (meshroom mode, needs ~3.5GB VRAM)')
    parser.add_argument('--cloud', action='store_true',
                        help='Skip local reconstruction, print cloud service instructions')
    parser.add_argument('--check-hardware', action='store_true',
                        help='Detect GPU/VRAM and recommend local vs cloud')

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
    existing_clean = list(clean_frames_dir.glob("*.png"))
    if len(existing_clean) > 100:
        print(f"\nFound {len(existing_clean)} existing clean frames in {clean_frames_dir}")
        print("Skipping preprocessing (delete folder to force re-run).")
        final_frames_dir = clean_frames_dir
        # Skip to segmentation
        segmented_frames_dir = args.project_dir / "segmented_frames"
        if not args.no_segment:
            print(f"\nStarting background segmentation (model: {args.segment_model})...")
            validated_model = None
            try:
                validated_model = validate_segment_model(args.segment_model)
                seg_stats = segment_frames(
                    input_dir=clean_frames_dir,
                    output_dir=segmented_frames_dir,
                    model_name=validated_model,
                    save_masks=args.save_masks,
                )
            except ValueError as exc:
                raise SystemExit(f"Background segmentation configuration error: {exc}") from exc
            except Exception as exc:
                model_info = validated_model or args.segment_model
                raise RuntimeError(
                    f"Background segmentation failed using model '{model_info}': {exc}"
                ) from exc
            print(f"Segmented {seg_stats['processed']}/{seg_stats['total']} frames")
            final_frames_dir = segmented_frames_dir
        zip_path = None
        if args.zip or args.mode in ['nerf', 'splat']:
            zip_path = args.project_dir / f"clean_frames_{args.mode}.zip"
            create_zip_archive(final_frames_dir, zip_path)
        if args.check_hardware:
            gpu_info = detect_gpu()
            print(f"\nHardware Detection:")
            print(f"  GPU: {gpu_info['name']} ({gpu_info['vram_mb']}MB)" if gpu_info['has_nvidia']
                  else "  GPU: None detected (CPU only)")
            if gpu_info['has_nvidia'] and gpu_info['vram_mb'] >= 4000:
                print("  Recommendation: Local reconstruction should work well.")
            elif gpu_info['has_nvidia']:
                print(f"  Recommendation: Sparse OK. Dense may need --cloud ({gpu_info['vram_mb']}MB VRAM).")
            else:
                print("  Recommendation: Use --cloud for GPU-accelerated reconstruction.")
        if args.reconstruct or args.cloud:
            gpu_info = detect_gpu()
            recon_result = run_reconstruction(
                frames_dir=final_frames_dir,
                output_dir=args.project_dir,
                mode=args.mode,
                dense=args.dense,
                cloud=args.cloud,
                gpu_info=gpu_info,
                zip_path=str(zip_path) if zip_path else None,
            )
            if recon_result.get("sparse", {}).get("ply_path"):
                print(f"\nSparse point cloud: {recon_result['sparse']['ply_path']}")
            if recon_result.get("dense", {}).get("ply_path"):
                print(f"Dense point cloud: {recon_result['dense']['ply_path']}")
        print("\nPipeline Complete!")
        if args.mode == 'meshroom':
            print(f"Ready for Meshroom / COLMAP: {final_frames_dir}")
        else:
            upload_target = f" / ZIP: {zip_path}" if zip_path else ""
            print(f"Ready for KIRI Engine / Polycam / Google Colab (3DGS): {final_frames_dir}{upload_target}")
        return

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
        skip_duplicates=not args.no_duplicate_filter,
        min_blur_score=min_blur,
        duplicate_threshold=duplicate_thresh,
        sharpen=use_sharpen,
        denoise=use_denoise
    )
    
    # 3b. Mask corner artifacts
    if args.mask_artifacts:
        print("\nMasking corner light artifacts...")
        n_fixed = mask_corner_artifacts(clean_frames_dir)
        print(f"Fixed {n_fixed} frames with corner artifacts")

    # 3c. Auto-crop to minimize black space
    if not args.no_auto_crop:
        print(f"\nAuto-cropping frames (padding: {args.crop_padding*100:.0f}%)...")
        crop_stats = auto_crop_frames(clean_frames_dir, padding=args.crop_padding)
        if crop_stats.get("skipped"):
            print(f"  Auto-crop skipped (insufficient reduction)")
        else:
            print(f"  Cropped {crop_stats['cropped']} frames: "
                  f"{crop_stats['original_size']} -> {crop_stats['cropped_size']} "
                  f"({crop_stats['reduction_pct']}% reduction)")

    # 4. Background Segmentation
    segmented_frames_dir = args.project_dir / "segmented_frames"
    if not args.no_segment:
        print(f"\nStarting background segmentation (model: {args.segment_model})...")
        validated_model = None
        try:
            validated_model = validate_segment_model(args.segment_model)
            seg_stats = segment_frames(
                input_dir=clean_frames_dir,
                output_dir=segmented_frames_dir,
                model_name=validated_model,
                save_masks=args.save_masks,
            )
        except ValueError as exc:
            raise SystemExit(f"Background segmentation configuration error: {exc}") from exc
        except Exception as exc:
            model_info = validated_model or args.segment_model
            raise RuntimeError(
                f"Background segmentation failed using model '{model_info}': {exc}"
            ) from exc
        print(f"Segmented {seg_stats['processed']}/{seg_stats['total']} frames")
        final_frames_dir = segmented_frames_dir
    else:
        final_frames_dir = clean_frames_dir

    # 5. Export ZIP
    # Splat and NeRF modes always generate a ZIP for cloud upload
    zip_path = None
    if args.zip or args.mode in ['nerf', 'splat']:
        zip_path = args.project_dir / f"clean_frames_{args.mode}.zip"
        create_zip_archive(final_frames_dir, zip_path)

    # 6. Hardware check (opt-in, read-only)
    if args.check_hardware:
        gpu_info = detect_gpu()
        print(f"\nHardware Detection:")
        print(f"  GPU: {gpu_info['name']} ({gpu_info['vram_mb']}MB)" if gpu_info['has_nvidia']
              else "  GPU: None detected (CPU only)")
        if gpu_info['has_nvidia'] and gpu_info['vram_mb'] >= 4000:
            print("  Recommendation: Local reconstruction should work well.")
        elif gpu_info['has_nvidia']:
            print(f"  Recommendation: Sparse OK. Dense may need --cloud ({gpu_info['vram_mb']}MB VRAM).")
        else:
            print("  Recommendation: Use --cloud for GPU-accelerated reconstruction.")

    # 7. Reconstruction (opt-in)
    if args.reconstruct or args.cloud:
        gpu_info = detect_gpu() if not args.check_hardware else gpu_info
        recon_result = run_reconstruction(
            frames_dir=final_frames_dir,
            output_dir=args.project_dir,
            mode=args.mode,
            dense=args.dense,
            cloud=args.cloud,
            gpu_info=gpu_info,
            zip_path=str(zip_path) if zip_path else None,
        )
        if recon_result.get("sparse", {}).get("ply_path"):
            print(f"\nSparse point cloud: {recon_result['sparse']['ply_path']}")
        if recon_result.get("dense", {}).get("ply_path"):
            print(f"Dense point cloud: {recon_result['dense']['ply_path']}")

    print("\nPipeline Complete!")
    if args.mode == 'meshroom':
        print(f"Ready for Meshroom / COLMAP: {final_frames_dir}")
    else:
        upload_target = f" / ZIP: {zip_path}" if zip_path else ""
        print(f"Ready for KIRI Engine / Polycam / Google Colab (3DGS): {final_frames_dir}{upload_target}")

if __name__ == '__main__':
    main()
