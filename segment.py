"""
Dreams to Reality: Background Segmentation

Removes background from preprocessed frames to isolate the subject.
This dramatically improves photogrammetry reconstruction by preventing
the engine from trying to map background clutter as geometry.

Uses rembg (U2-Net / RMBG) for automatic foreground detection.
No GPU required — runs on CPU, ~1-3 sec per frame.

Usage:
    python segment.py <input_dir> <output_dir> [--model u2net]

Models:
    u2net       - General purpose, good default (~170MB)
    u2net_human_seg - Optimized for people
    isnet-general-use - Fast, good for objects
"""

import argparse
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from tqdm import tqdm

VALID_SEGMENT_MODELS = ["u2net", "u2net_human_seg", "isnet-general-use"]


def remove_background(
    image: np.ndarray,
    session=None,
    bg_color: tuple = (0, 0, 0),
    return_mask: bool = False,
) -> np.ndarray | tuple:
    """
    Remove background from a single frame.

    Args:
        image: BGR numpy array (from cv2)
        session: rembg session (reuse across frames for speed)
        bg_color: replacement background color (default black)
        return_mask: if True, also return the alpha mask

    Returns:
        BGR image with background replaced, or (image, mask) tuple
    """
    from rembg import remove, new_session

    if session is None:
        session = new_session("u2net")

    # cv2 is BGR, rembg expects RGB via PIL
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb)

    # Remove background — returns RGBA PIL image
    result = remove(pil_img, session=session)
    result_np = np.array(result)

    # Extract alpha channel as mask
    alpha = result_np[:, :, 3]

    # Create output with solid background color
    bg = np.full_like(image, bg_color, dtype=np.uint8)
    fg = cv2.cvtColor(result_np[:, :, :3], cv2.COLOR_RGB2BGR)

    # Blend using alpha
    alpha_f = alpha.astype(np.float32) / 255.0
    alpha_3 = np.stack([alpha_f] * 3, axis=-1)
    output = (fg * alpha_3 + bg * (1 - alpha_3)).astype(np.uint8)

    if return_mask:
        return output, alpha
    return output


def validate_segment_model(model_name: str) -> str:
    """Ensure the requested rembg model is one we support."""
    if model_name not in VALID_SEGMENT_MODELS:
        raise ValueError(
            f"Unsupported segmentation model '{model_name}'. Supported: {', '.join(VALID_SEGMENT_MODELS)}."
        )
    return model_name


def segment_frames(
    input_dir: Path,
    output_dir: Path,
    model_name: str = "u2net",
    bg_color: tuple = (0, 0, 0),
    save_masks: bool = False,
    verbose: bool = True,
) -> dict:
    """
    Remove background from all frames in a directory.

    Args:
        input_dir: directory of preprocessed frames
        output_dir: where to save segmented frames
        model_name: rembg model to use
        bg_color: background replacement color
        save_masks: also save alpha masks (useful for debugging)
        verbose: show progress bar

    Returns:
        dict with processing stats
    """
    from rembg import new_session

    model_name = validate_segment_model(model_name)

    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if save_masks:
        mask_dir = output_dir / "masks"
        mask_dir.mkdir(exist_ok=True)

    extensions = {".png", ".jpg", ".jpeg"}
    frames = sorted(
        f for f in input_dir.iterdir() if f.suffix.lower() in extensions
    )

    stats = {"total": len(frames), "processed": 0, "errors": 0}

    if verbose:
        print(f"Segmenting {len(frames)} frames (model: {model_name})")
        print(f"Background color: {bg_color}")

    # Create session once — reused for all frames (big speed win)
    session = new_session(model_name)

    for frame_path in tqdm(frames, disable=not verbose, desc="Segmenting"):
        try:
            image = cv2.imread(str(frame_path))
            if image is None:
                stats["errors"] += 1
                continue

            if save_masks:
                result, mask = remove_background(
                    image, session=session, bg_color=bg_color, return_mask=True
                )
                cv2.imwrite(str(mask_dir / frame_path.name), mask)
            else:
                result = remove_background(
                    image, session=session, bg_color=bg_color
                )

            cv2.imwrite(str(output_dir / frame_path.name), result)
            stats["processed"] += 1

        except Exception as e:
            if verbose:
                print(f"Error on {frame_path.name}: {e}")
            stats["errors"] += 1

    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Remove background from frames for photogrammetry"
    )
    parser.add_argument(
        "input_dir", type=Path, help="Directory of preprocessed frames"
    )
    parser.add_argument(
        "output_dir", type=Path, help="Output directory for segmented frames"
    )
    parser.add_argument(
        "--model",
        default="u2net",
        choices=VALID_SEGMENT_MODELS,
        help="Segmentation model (default: u2net)",
    )
    parser.add_argument(
        "--bg-color",
        nargs=3,
        type=int,
        default=[0, 0, 0],
        metavar=("B", "G", "R"),
        help="Background color in BGR (default: 0 0 0 = black)",
    )
    parser.add_argument(
        "--save-masks",
        action="store_true",
        help="Also save alpha masks for debugging",
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Dreams to Reality: Background Segmentation")
    print("=" * 60)

    stats = segment_frames(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        model_name=args.model,
        bg_color=tuple(args.bg_color),
        save_masks=args.save_masks,
    )

    print("\n" + "=" * 60)
    print("Segmentation Complete!")
    print("=" * 60)
    print(f"Total frames:  {stats['total']}")
    print(f"Processed:     {stats['processed']}")
    print(f"Errors:        {stats['errors']}")
    print("=" * 60)
    print(f"\nSegmented frames saved to: {args.output_dir}")


if __name__ == "__main__":
    main()
