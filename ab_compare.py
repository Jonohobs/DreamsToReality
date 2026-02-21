"""
Dreams to Reality: A/B Segmentation Comparison

Compares rembg (U2-Net) vs SAM (Segment Anything Model) for background
removal on Dreams frames. Generates side-by-side visual comparisons.

Usage:
    python ab_compare.py <input_dir> <output_dir> [--num-frames 20]

Output:
    - Individual segmented frames from each model
    - Side-by-side comparison grids
    - comparison_summary.txt with timing stats
"""

import argparse
import time
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from tqdm import tqdm


def sample_frames(input_dir: Path, num_frames: int = 20) -> list[Path]:
    """Evenly sample N frames from a directory."""
    extensions = {".png", ".jpg", ".jpeg"}
    frames = sorted(
        f for f in input_dir.iterdir() if f.suffix.lower() in extensions
    )
    if len(frames) <= num_frames:
        return frames

    # Evenly space across the full set
    indices = np.linspace(0, len(frames) - 1, num_frames, dtype=int)
    return [frames[i] for i in indices]


def run_rembg(frames: list[Path], output_dir: Path, model: str = "u2net") -> dict:
    """Run rembg background removal on frames."""
    from rembg import remove, new_session

    output_dir.mkdir(parents=True, exist_ok=True)
    session = new_session(model)

    results = {"times": [], "errors": 0}

    for frame_path in tqdm(frames, desc="rembg"):
        try:
            image = cv2.imread(str(frame_path))
            if image is None:
                results["errors"] += 1
                continue

            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb)

            start = time.time()
            result = remove(pil_img, session=session)
            elapsed = time.time() - start
            results["times"].append(elapsed)

            # Convert RGBA result to BGR with black background
            result_np = np.array(result)
            alpha = result_np[:, :, 3].astype(np.float32) / 255.0
            alpha_3 = np.stack([alpha] * 3, axis=-1)
            fg = cv2.cvtColor(result_np[:, :, :3], cv2.COLOR_RGB2BGR)
            bg = np.zeros_like(image)
            output = (fg * alpha_3 + bg * (1 - alpha_3)).astype(np.uint8)

            cv2.imwrite(str(output_dir / frame_path.name), output)

        except Exception as e:
            print(f"rembg error on {frame_path.name}: {e}")
            results["errors"] += 1

    return results


def run_sam(frames: list[Path], output_dir: Path, checkpoint: Path = None) -> dict:
    """Run SAM automatic segmentation on frames."""
    import torch
    from segment_anything import sam_model_registry, SamAutomaticMaskGenerator

    output_dir.mkdir(parents=True, exist_ok=True)

    # Find or use default checkpoint
    if checkpoint is None:
        checkpoint = Path(__file__).parent / "sam_vit_b_01ec64.pth"

    if not checkpoint.exists():
        raise FileNotFoundError(
            f"SAM checkpoint not found: {checkpoint}\n"
            "Download from: https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth"
        )

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"SAM device: {device}")

    sam = sam_model_registry["vit_b"](checkpoint=str(checkpoint))
    sam.to(device)

    mask_generator = SamAutomaticMaskGenerator(
        model=sam,
        points_per_side=32,
        pred_iou_thresh=0.86,
        stability_score_thresh=0.92,
        min_mask_region_area=1000,
    )

    results = {"times": [], "errors": 0}

    for frame_path in tqdm(frames, desc="SAM"):
        try:
            image = cv2.imread(str(frame_path))
            if image is None:
                results["errors"] += 1
                continue

            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            start = time.time()
            masks = mask_generator.generate(rgb)
            elapsed = time.time() - start
            results["times"].append(elapsed)

            if not masks:
                # No masks found — save black image
                cv2.imwrite(str(output_dir / frame_path.name), np.zeros_like(image))
                continue

            # Strategy: combine all masks except the largest one (assumed background)
            # Sort by area descending
            masks_sorted = sorted(masks, key=lambda m: m["area"], reverse=True)

            h, w = image.shape[:2]
            total_area = h * w

            # The largest mask that covers >50% of image is likely background
            foreground_mask = np.zeros((h, w), dtype=np.uint8)

            if masks_sorted[0]["area"] > total_area * 0.5:
                # Largest is background — combine the rest as foreground
                for m in masks_sorted[1:]:
                    foreground_mask = np.maximum(foreground_mask, m["segmentation"].astype(np.uint8) * 255)
            else:
                # No clear background — combine all masks as foreground
                for m in masks_sorted:
                    foreground_mask = np.maximum(foreground_mask, m["segmentation"].astype(np.uint8) * 255)

            # Apply mask to original image
            alpha_f = foreground_mask.astype(np.float32) / 255.0
            alpha_3 = np.stack([alpha_f] * 3, axis=-1)
            output = (image * alpha_3).astype(np.uint8)

            cv2.imwrite(str(output_dir / frame_path.name), output)

        except Exception as e:
            print(f"SAM error on {frame_path.name}: {e}")
            results["errors"] += 1

    return results


def create_comparison_grid(
    frames: list[Path],
    rembg_dir: Path,
    sam_dir: Path,
    output_path: Path,
    cols: int = 4,
    thumb_width: int = 400,
):
    """Create a side-by-side comparison grid image."""
    rows_per_frame = 1
    total_frames = len(frames)
    grid_rows = (total_frames + cols - 1) // cols

    # Each cell has 3 images side by side: original | rembg | SAM
    cell_w = thumb_width * 3 + 20  # 10px gap between each
    cell_h = None  # determined by first frame

    # Load first frame to get aspect ratio
    sample = cv2.imread(str(frames[0]))
    aspect = sample.shape[0] / sample.shape[1]
    thumb_h = int(thumb_width * aspect)
    cell_h = thumb_h + 30  # 30px for label

    # Create canvas
    canvas_w = cols * cell_w + 20
    canvas_h = grid_rows * cell_h + 60  # header
    canvas = np.full((canvas_h, canvas_w, 3), 30, dtype=np.uint8)  # dark gray bg

    # Header
    cv2.putText(canvas, "Original", (thumb_width // 2, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
    cv2.putText(canvas, "rembg (U2-Net)", (thumb_width + thumb_width // 3, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 255, 100), 2)
    cv2.putText(canvas, "SAM (vit_b)", (thumb_width * 2 + thumb_width // 3, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 255), 2)

    for idx, frame_path in enumerate(frames):
        row = idx // cols
        col = idx % cols

        x_offset = col * cell_w + 10
        y_offset = row * cell_h + 50

        # Load original
        orig = cv2.imread(str(frame_path))
        orig_thumb = cv2.resize(orig, (thumb_width, thumb_h))

        # Load rembg result
        rembg_path = rembg_dir / frame_path.name
        if rembg_path.exists():
            rembg_img = cv2.imread(str(rembg_path))
            rembg_thumb = cv2.resize(rembg_img, (thumb_width, thumb_h))
        else:
            rembg_thumb = np.zeros((thumb_h, thumb_width, 3), dtype=np.uint8)

        # Load SAM result
        sam_path = sam_dir / frame_path.name
        if sam_path.exists():
            sam_img = cv2.imread(str(sam_path))
            sam_thumb = cv2.resize(sam_img, (thumb_width, thumb_h))
        else:
            sam_thumb = np.zeros((thumb_h, thumb_width, 3), dtype=np.uint8)

        # Place in canvas
        canvas[y_offset:y_offset + thumb_h, x_offset:x_offset + thumb_width] = orig_thumb
        canvas[y_offset:y_offset + thumb_h, x_offset + thumb_width + 5:x_offset + thumb_width * 2 + 5] = rembg_thumb
        canvas[y_offset:y_offset + thumb_h, x_offset + thumb_width * 2 + 10:x_offset + thumb_width * 3 + 10] = sam_thumb

        # Label
        cv2.putText(canvas, frame_path.stem, (x_offset, y_offset + thumb_h + 18),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (150, 150, 150), 1)

    cv2.imwrite(str(output_path), canvas)
    print(f"Comparison grid saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="A/B comparison: rembg vs SAM segmentation"
    )
    parser.add_argument("input_dir", type=Path, help="Directory of frames to test")
    parser.add_argument("output_dir", type=Path, help="Output directory for results")
    parser.add_argument("--num-frames", type=int, default=20, help="Number of frames to sample")
    parser.add_argument("--sam-checkpoint", type=Path, default=None, help="Path to SAM checkpoint")
    parser.add_argument("--rembg-model", default="u2net", help="rembg model name")
    parser.add_argument("--skip-rembg", action="store_true", help="Skip rembg (reuse existing)")
    parser.add_argument("--skip-sam", action="store_true", help="Skip SAM (reuse existing)")

    args = parser.parse_args()

    print("=" * 60)
    print("Dreams to Reality: A/B Segmentation Comparison")
    print("=" * 60)

    # 1. Sample frames
    frames = sample_frames(args.input_dir, args.num_frames)
    print(f"\nSampled {len(frames)} frames from {args.input_dir}")

    rembg_dir = args.output_dir / "rembg"
    sam_dir = args.output_dir / "sam"

    # 2. Run rembg
    if not args.skip_rembg:
        print(f"\n--- rembg ({args.rembg_model}) ---")
        rembg_results = run_rembg(frames, rembg_dir, model=args.rembg_model)
        rembg_avg = np.mean(rembg_results["times"]) if rembg_results["times"] else 0
        print(f"rembg avg: {rembg_avg:.2f}s/frame, errors: {rembg_results['errors']}")
    else:
        rembg_results = {"times": [], "errors": 0}
        rembg_avg = 0
        print("\nSkipping rembg (--skip-rembg)")

    # 3. Run SAM
    if not args.skip_sam:
        print(f"\n--- SAM (vit_b) ---")
        try:
            sam_results = run_sam(frames, sam_dir, checkpoint=args.sam_checkpoint)
            sam_avg = np.mean(sam_results["times"]) if sam_results["times"] else 0
            print(f"SAM avg: {sam_avg:.2f}s/frame, errors: {sam_results['errors']}")
        except FileNotFoundError as e:
            print(f"\n{e}")
            print("Run with --skip-sam to compare rembg only, or download the checkpoint first.")
            sam_results = {"times": [], "errors": 0}
            sam_avg = 0
        except ImportError:
            print("\nSAM not installed. Install with: pip install segment-anything")
            sam_results = {"times": [], "errors": 0}
            sam_avg = 0
    else:
        sam_results = {"times": [], "errors": 0}
        sam_avg = 0
        print("\nSkipping SAM (--skip-sam)")

    # 4. Create comparison grid
    print("\n--- Generating comparison grid ---")
    grid_path = args.output_dir / "comparison_grid.png"
    try:
        create_comparison_grid(frames, rembg_dir, sam_dir, grid_path)
    except Exception as e:
        print(f"Grid generation error: {e}")

    # 5. Summary
    summary = f"""
{'=' * 60}
A/B Segmentation Comparison Summary
{'=' * 60}

Frames tested: {len(frames)}
Source: {args.input_dir}

rembg ({args.rembg_model}):
  Avg time/frame: {rembg_avg:.2f}s
  Errors: {rembg_results['errors']}
  Total time: {sum(rembg_results['times']):.1f}s

SAM (vit_b):
  Avg time/frame: {sam_avg:.2f}s
  Errors: {sam_results['errors']}
  Total time: {sum(sam_results['times']):.1f}s

Speed ratio: SAM is {sam_avg / rembg_avg:.1f}x {'slower' if sam_avg > rembg_avg else 'faster'} than rembg
{'' if rembg_avg == 0 else ''}
Output:
  rembg results: {rembg_dir}
  SAM results:   {sam_dir}
  Comparison:    {grid_path}
{'=' * 60}
"""
    print(summary)

    summary_path = args.output_dir / "comparison_summary.txt"
    summary_path.write_text(summary)
    print(f"Summary saved: {summary_path}")


if __name__ == "__main__":
    main()
