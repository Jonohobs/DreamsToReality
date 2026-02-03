"""
Dreams to Reality: Frame Preprocessing

Prepares Dreams gameplay footage for photogrammetry by:
1. Filtering frames with UI overlays
2. Detecting and removing near-duplicate frames
3. Optionally removing background for cleaner feature detection
4. Quality checks (blur detection, etc.)

Usage:
    python preprocess.py <input_dir> <output_dir> [--remove-bg]
"""

import os
import sys
import shutil
import argparse
from pathlib import Path

import cv2
import numpy as np
from tqdm import tqdm


def detect_ui_overlay(image: np.ndarray, threshold: float = 0.15) -> bool:
    """
    Detect if a frame has Dreams UI elements.
    
    Dreams UI typically appears in the top portion of the screen with
    distinctive button icons and text. We check for high-contrast
    elements in the top 20% of the frame.
    """
    height = image.shape[0]
    top_region = image[:int(height * 0.2), :]
    
    # Convert to grayscale and check for UI elements (high contrast text/icons)
    gray = cv2.cvtColor(top_region, cv2.COLOR_BGR2GRAY)
    
    # UI elements tend to have sharp edges and high contrast
    edges = cv2.Canny(gray, 100, 200)
    edge_ratio = np.sum(edges > 0) / edges.size
    
    # Also check for the characteristic UI colors (blues, oranges from Dreams UI)
    hsv = cv2.cvtColor(top_region, cv2.COLOR_BGR2HSV)
    
    # Dreams UI button colors (approximate ranges)
    blue_mask = cv2.inRange(hsv, (100, 100, 100), (130, 255, 255))
    orange_mask = cv2.inRange(hsv, (10, 100, 100), (25, 255, 255))
    
    ui_color_ratio = (np.sum(blue_mask > 0) + np.sum(orange_mask > 0)) / blue_mask.size
    
    # Frame has UI if it has significant edges AND UI-colored regions in top area
    return edge_ratio > threshold or ui_color_ratio > 0.05


def calculate_blur_score(image: np.ndarray) -> float:
    """
    Calculate a blur score using Laplacian variance.
    Higher values = sharper image.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    return laplacian.var()


def calculate_frame_similarity(frame1: np.ndarray, frame2: np.ndarray) -> float:
    """
    Calculate similarity between two frames using histogram comparison.
    Returns value between 0 (different) and 1 (identical).
    """
    # Resize for faster comparison
    size = (256, 256)
    f1 = cv2.resize(frame1, size)
    f2 = cv2.resize(frame2, size)
    
    # Convert to HSV for better color comparison
    hsv1 = cv2.cvtColor(f1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(f2, cv2.COLOR_BGR2HSV)
    
    # Calculate histograms
    hist1 = cv2.calcHist([hsv1], [0, 1], None, [50, 60], [0, 180, 0, 256])
    hist2 = cv2.calcHist([hsv2], [0, 1], None, [50, 60], [0, 180, 0, 256])
    
    # Normalize
    cv2.normalize(hist1, hist1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    cv2.normalize(hist2, hist2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    
    # Compare using correlation
    return cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)


def preprocess_frames(
    input_dir: Path,
    output_dir: Path,
    skip_ui: bool = True,
    skip_duplicates: bool = True,
    min_blur_score: float = 100.0,
    duplicate_threshold: float = 0.98,
    verbose: bool = True
) -> dict:
    """
    Process all frames in input directory and copy valid ones to output.
    
    Returns dict with statistics about processing.
    """
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get all image files
    extensions = {'.png', '.jpg', '.jpeg'}
    frames = sorted([
        f for f in input_dir.iterdir()
        if f.suffix.lower() in extensions
    ])
    
    stats = {
        'total': len(frames),
        'ui_filtered': 0,
        'blur_filtered': 0,
        'duplicate_filtered': 0,
        'kept': 0,
        'errors': 0
    }
    
    if verbose:
        print(f"Processing {len(frames)} frames from {input_dir}")
    
    previous_frame = None
    kept_frames = []
    
    for frame_path in tqdm(frames, disable=not verbose):
        try:
            # Read frame
            image = cv2.imread(str(frame_path))
            if image is None:
                stats['errors'] += 1
                continue
            
            # Check for UI overlay
            if skip_ui and detect_ui_overlay(image):
                stats['ui_filtered'] += 1
                continue
            
            # Check blur
            blur_score = calculate_blur_score(image)
            if blur_score < min_blur_score:
                stats['blur_filtered'] += 1
                continue
            
            # Check for near-duplicates
            if skip_duplicates and previous_frame is not None:
                similarity = calculate_frame_similarity(image, previous_frame)
                if similarity > duplicate_threshold:
                    stats['duplicate_filtered'] += 1
                    continue
            
            # Frame passed all checks - copy to output
            output_path = output_dir / frame_path.name
            shutil.copy2(frame_path, output_path)
            
            stats['kept'] += 1
            kept_frames.append(frame_path.name)
            previous_frame = image
            
        except Exception as e:
            if verbose:
                print(f"Error processing {frame_path.name}: {e}")
            stats['errors'] += 1
    
    # Write manifest of kept frames
    manifest_path = output_dir / 'frames_manifest.txt'
    with open(manifest_path, 'w') as f:
        f.write(f"# Preprocessed frames for photogrammetry\n")
        f.write(f"# Total: {stats['kept']} frames\n")
        f.write(f"# UI filtered: {stats['ui_filtered']}\n")
        f.write(f"# Blur filtered: {stats['blur_filtered']}\n")
        f.write(f"# Duplicate filtered: {stats['duplicate_filtered']}\n\n")
        for frame in kept_frames:
            f.write(f"{frame}\n")
    
    return stats


def main():
    parser = argparse.ArgumentParser(
        description='Preprocess Dreams footage for photogrammetry'
    )
    parser.add_argument(
        'input_dir',
        type=Path,
        help='Directory containing extracted frames'
    )
    parser.add_argument(
        'output_dir',
        type=Path,
        help='Output directory for processed frames'
    )
    parser.add_argument(
        '--no-ui-filter',
        action='store_true',
        help='Disable UI overlay detection'
    )
    parser.add_argument(
        '--no-duplicate-filter',
        action='store_true',
        help='Keep near-duplicate frames'
    )
    parser.add_argument(
        '--min-blur-score',
        type=float,
        default=100.0,
        help='Minimum blur score (higher = sharper required)'
    )
    parser.add_argument(
        '--duplicate-threshold',
        type=float,
        default=0.98,
        help='Similarity threshold for duplicate detection (0-1)'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Dreams to Reality: Frame Preprocessor")
    print("=" * 60)
    
    stats = preprocess_frames(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        skip_ui=not args.no_ui_filter,
        skip_duplicates=not args.no_duplicate_filter,
        min_blur_score=args.min_blur_score,
        duplicate_threshold=args.duplicate_threshold
    )
    
    print("\n" + "=" * 60)
    print("Processing Complete!")
    print("=" * 60)
    print(f"Total frames:      {stats['total']}")
    print(f"UI filtered:       {stats['ui_filtered']}")
    print(f"Blur filtered:     {stats['blur_filtered']}")
    print(f"Duplicate filtered: {stats['duplicate_filtered']}")
    print(f"Errors:            {stats['errors']}")
    print(f"Frames kept:       {stats['kept']}")
    print("=" * 60)
    print(f"\nProcessed frames saved to: {args.output_dir}")


if __name__ == '__main__':
    main()
