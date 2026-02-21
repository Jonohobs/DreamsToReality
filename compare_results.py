import os
from pathlib import Path

def count_lines(filepath):
    if not filepath.exists():
        return 0
    with open(filepath, 'rb') as f:
        return sum(1 for _ in f)

def get_colmap_stats(model_dir):
    """
    Parse points3D.txt or ply to get stats.
    For sparse models (TXT/BIN):
    - cameras.bin/txt
    - images.bin/txt
    - points3D.bin/txt
    """
    model_path = Path(model_dir)
    stats = {
        "cameras": 0,
        "images": 0,
        "points": 0
    }
    
    # Check for PLY (Dense)
    ply_path = model_path / "fused.ply"
    if ply_path.exists():
        # Approx count for PLY header? Or just check size
        stats["dense_ply_size_mb"] = ply_path.stat().st_size / (1024*1024)
        
    # Check for Sparse (0 folder often)
    sparse_0 = model_path / "0"
    if not sparse_0.exists():
        sparse_0 = model_path # sometimes directly in sparse/
    
    # We might need to read binary, but let's just check for existence or listdir for now
    # or rely on basic file sizes if binary
    return stats

def main():
    print("--- Reconstruction Comparison ---")
    
    pipelines = {
        "Baseline (COLMAP Auto)": Path("colmap_out_hq"),
        "Custom (Enhanced)": Path("colmap_out_custom/sparse")
    }
    
    for name, path in pipelines.items():
        print(f"\nAnalyzing {name} at {path}...")
        if not path.exists():
            print("  Path not found (yet?)")
            continue
            
        # Check for sparse reconstruction results
        sparse_sub = path / "0"
        if not sparse_sub.exists():
             sparse_sub = path # check direct
             
        points_bin = sparse_sub / "points3D.bin"
        if points_bin.exists():
            print(f"  Sparse Model: FOUND ({points_bin.stat().st_size / 1024:.1f} KB)")
        else:
            print("  Sparse Model: NOT FOUND")
            
        # Check for dense
        # Baseline puts it in `dense/0/fused.ply` usually
        dense_ply = path / "dense/0/fused.ply"
        if not dense_ply.exists():
            dense_ply = path.parent / "dense/0/fused.ply" # Check parent structure
            
        if dense_ply.exists():
             print(f"  Dense Model: FOUND ({dense_ply.stat().st_size / (1024*1024):.1f} MB)")
        else:
             print("  Dense Model: NOT FOUND")

if __name__ == "__main__":
    main()
