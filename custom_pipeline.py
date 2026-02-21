import os
import subprocess
import cv2
import numpy as np
from pathlib import Path
import argparse

# Goals for Custom Pipeline:
# 1. Pre-processing: specialized sharpening/contrast for Dreams "flecks"
# 2. Feature Extraction: Use SIFT with very low contrast threshold
# 3. Matching: Guided matching if possible
# 4. Reconstruction: Call COLMAP mapper with custom hooks

def preprocess_for_dreams(image_path):
    """
    Apply 'Dreams-specific' enhancements:
    - Increase local contrast (CLAHE) to make flecks stand out?
    - Slight sharpening?
    """
    img = cv2.imread(str(image_path))
    if img is None:
        return None
    
    # Lab conversion for CLAHE on L channel often works better for "painting" style inputs
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    
    limg = cv2.merge((cl,a,b))
    enhanced = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    
    return enhanced

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', type=Path, required=True, help="Directory of raw frames")
    parser.add_argument('--output_dir', type=Path, required=True, help="Output workspace")
    args = parser.parse_args()
    
    print(f"Starting Custom Dreams Reconstruction Pipeline...")
    
    # 1. Pre-process steps
    processed_dir = args.output_dir / "processed_frames"
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    for img_file in args.input_dir.glob("*.jpg"):
        print(f"Processing {img_file.name}...")
        enhanced = preprocess_for_dreams(img_file)
        if enhanced is not None:
             cv2.imwrite(str(processed_dir / img_file.name), enhanced)
             
    # 2. Feature Extraction (Calling COLMAP CLI with tuned params)
    colmap_bat = Path("COLMAP/COLMAP-3.9.1-windows-cuda/COLMAP.bat").resolve()
    database_path = args.output_dir / "database.db"
    
    print(">>> Extracting Features...")
    subprocess.run([
        str(colmap_bat), "feature_extractor",
        "--database_path", str(database_path),
        "--image_path", str(processed_dir),
        "--ImageReader.single_camera", "1",
        "--SiftExtraction.peak_threshold", "0.001", # Ultra low threshold for Dreams
        "--SiftExtraction.use_gpu", "1"
    ], check=True)
    
    print(">>> Matching Features...")
    subprocess.run([
        str(colmap_bat), "exhaustive_matcher", # Exhaustive is better for small datasets
        "--database_path", str(database_path),
        "--SiftMatching.use_gpu", "1"
    ], check=True)
    
    print(">>> Running Sparse Reconstruction (Mapper)...")
    sparse_dir = args.output_dir / "sparse"
    sparse_dir.mkdir(parents=True, exist_ok=True)
    
    subprocess.run([
        str(colmap_bat), "mapper",
        "--database_path", str(database_path),
        "--image_path", str(processed_dir),
        "--output_path", str(sparse_dir)
    ], check=True)
    
    print(f"Custom pipeline sparse reconstruction complete in {sparse_dir}")
    
    # 3. Dense Reconstruction
    print(">>> Running Dense Reconstruction...")
    dense_dir = args.output_dir / "dense"
    dense_dir.mkdir(parents=True, exist_ok=True)
    
    # Undistort images
    subprocess.run([
        str(colmap_bat), "image_undistorter",
        "--image_path", str(processed_dir),
        "--input_path", str(sparse_dir / "0"),
        "--output_path", str(dense_dir),
        "--output_type", "COLMAP",
        "--max_image_size", "2000"
    ], check=True)
    
    # Patch Match Stereo
    subprocess.run([
        str(colmap_bat), "patch_match_stereo",
        "--workspace_path", str(dense_dir),
        "--workspace_format", "COLMAP",
        "--PatchMatchStereo.geom_consistency", "true",
        "--PatchMatchStereo.gpu_index", "0"
    ], check=True)
    
    # Stereo Fusion
    subprocess.run([
        str(colmap_bat), "stereo_fusion",
        "--workspace_path", str(dense_dir),
        "--workspace_format", "COLMAP",
        "--output_path", str(dense_dir / "fused.ply"),
        "--output_type", "PLY",
        "--StereoFusion.check_num_images", "15" # Lower constraint for smaller datasets
    ], check=True)
    
    print(f"Custom pipeline dense reconstruction complete at {dense_dir / 'fused.ply'}")

if __name__ == "__main__":
    main()
