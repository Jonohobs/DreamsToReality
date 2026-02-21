"""
Dreams to Reality: COLMAP Reconstruction

Integrates COLMAP sparse and dense reconstruction into the pipeline.
Auto-detects content quality (high-detail vs soft/flecky) and adjusts
SIFT parameters accordingly — no quality choke on high-detail sculpts.

Can run locally (if COLMAP installed) or print cloud service guidance.

Usage (standalone):
    python reconstruct.py <frames_dir> <output_dir> [--dense] [--cloud]

Usage (via pipeline):
    python pipeline.py video.mp4 project/ --reconstruct [--dense] [--cloud]
"""

import argparse
import shutil
import subprocess
from pathlib import Path
from typing import Optional

import cv2
import numpy as np


def assess_detail_level(frames_dir: Path, sample_count: int = 10) -> dict:
    """Sample frames and measure Laplacian variance to assess detail level.

    High-detail sculpts (flecks not visible): variance > 15
    Medium (some softness): variance 5-15
    Low-detail / soft flecks: variance < 5

    Returns dict with avg_variance, detail_level ('high'/'medium'/'low'),
    and recommended SIFT parameters.
    """
    extensions = {".png", ".jpg", ".jpeg"}
    frames = sorted(f for f in Path(frames_dir).iterdir() if f.suffix.lower() in extensions)
    if not frames:
        return {"avg_variance": 0, "detail_level": "unknown", "sample_count": 0}

    # Sample evenly across the sequence
    step = max(1, len(frames) // sample_count)
    sample = frames[::step][:sample_count]

    variances = []
    coverages = []
    for f in sample:
        img = cv2.imread(str(f), cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        # Only measure non-black pixels (Dreams frames are mostly black background)
        mask = img > 10
        if mask.sum() < 100:
            continue
        coverages.append(mask.sum() / mask.size * 100)
        lap = cv2.Laplacian(img, cv2.CV_64F)
        # Variance of Laplacian in the object region only
        variances.append(lap[mask].var())

    if not variances:
        return {"avg_variance": 0, "detail_level": "unknown", "sample_count": 0, "coverage_pct": 0}

    avg_var = float(np.mean(variances))
    avg_coverage = float(np.mean(coverages)) if coverages else 0

    if avg_var >= 15:
        detail_level = "high"
    elif avg_var >= 5:
        detail_level = "medium"
    else:
        detail_level = "low"

    return {
        "avg_variance": round(avg_var, 2),
        "detail_level": detail_level,
        "sample_count": len(variances),
        "coverage_pct": round(avg_coverage, 1),
    }


def _get_sift_params(detail_level: str, coverage_pct: float = 100.0) -> dict:
    """Return SIFT parameters appropriate for content detail and object coverage.

    Coverage matters: a detailed object filling 6% of frame needs more aggressive
    feature extraction than one filling 80%, because there are fewer pixels to work with.

    High-detail + high coverage: standard params (best mesh quality)
    High-detail + low coverage: boost features (small object in frame)
    Low/soft: Dreams-tuned fallback (recover features from soft flecks)
    """
    # Small object coverage (<25%) — boost extraction regardless of detail
    # Proven in custom_pipeline.py: peak=0.001 + exhaustive got 110k points
    if coverage_pct < 25:
        return {
            "peak_threshold": "0.001",
            "edge_threshold": "15",
            "first_octave": "-1",
            "max_num_features": "16384",
        }

    if detail_level == "high":
        return {
            "peak_threshold": "0.004",
            "edge_threshold": "10",
            "first_octave": "0",
            "max_num_features": "8192",
        }
    elif detail_level == "medium":
        return {
            "peak_threshold": "0.002",
            "edge_threshold": "12",
            "first_octave": "-1",
            "max_num_features": "12288",
        }
    else:  # low / unknown — soft fleck fallback
        return {
            "peak_threshold": "0.001",
            "edge_threshold": "15",
            "first_octave": "-1",
            "max_num_features": "16384",
        }


def detect_gpu() -> dict:
    """Detect NVIDIA GPU via nvidia-smi. Returns specs dict."""
    result = {
        "has_nvidia": False,
        "vram_mb": 0,
        "name": "none",
        "cuda_available": False,
    }
    try:
        out = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=10,
        )
        if out.returncode == 0 and out.stdout.strip():
            line = out.stdout.strip().split("\n")[0]
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 2:
                result["has_nvidia"] = True
                result["name"] = parts[0]
                result["vram_mb"] = int(float(parts[1]))
                result["cuda_available"] = True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return result


def find_colmap() -> Optional[str]:
    """Find COLMAP binary. Checks PATH then project-relative legacy location."""
    # Check PATH
    path_bin = shutil.which("colmap")
    if path_bin:
        return path_bin

    # Check project-relative COLMAP folder — any version subfolder
    colmap_dir = Path("COLMAP").resolve()
    if colmap_dir.exists():
        for bat in sorted(colmap_dir.rglob("COLMAP.bat"), reverse=True):
            return str(bat)
        # Also check for plain colmap.exe (Linux-style extract on Windows)
        for exe in sorted(colmap_dir.rglob("colmap.exe"), reverse=True):
            return str(exe)

    return None


def reconstruct_sparse(
    frames_dir: Path,
    output_dir: Path,
    colmap_bin: str,
    mode: str,
    gpu_info: dict,
) -> dict:
    """Run COLMAP sparse reconstruction with Dreams-tuned parameters.

    Returns dict with paths and stats.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    database_path = output_dir / "database.db"
    sparse_dir = output_dir / "sparse"
    sparse_dir.mkdir(parents=True, exist_ok=True)

    use_gpu = "1" if gpu_info.get("cuda_available") else "0"

    # Auto-detect content detail level and choose SIFT params accordingly.
    # High-detail sculpts get standard aggressive params for best mesh quality.
    # Soft/flecky content gets relaxed params as a safety net.
    detail = assess_detail_level(frames_dir)
    sift = _get_sift_params(detail["detail_level"], detail.get("coverage_pct", 100))
    print(f"  Content: {detail['detail_level']} detail (variance: {detail['avg_variance']}, "
          f"coverage: {detail.get('coverage_pct', 0)}%)")
    print(f"  SIFT: peak={sift['peak_threshold']}, edge={sift['edge_threshold']}, "
          f"octave={sift['first_octave']}, max_features={sift['max_num_features']}")

    print("  [1/4] Extracting features...")
    subprocess.run([
        colmap_bin, "feature_extractor",
        "--database_path", str(database_path),
        "--image_path", str(frames_dir),
        "--ImageReader.single_camera", "1",
        "--SiftExtraction.peak_threshold", sift["peak_threshold"],
        "--SiftExtraction.edge_threshold", sift["edge_threshold"],
        "--SiftExtraction.first_octave", sift["first_octave"],
        "--SiftExtraction.max_num_features", sift["max_num_features"],
        "--SiftExtraction.use_gpu", use_gpu,
    ], check=True)

    # Always use exhaustive matching for Dreams content.
    # Sequential matching breaks the chain when feature-sparse frames can't bridge gaps,
    # producing disconnected sub-models. Exhaustive compares all pairs and finds connections
    # regardless of capture order. Proven in custom_pipeline.py (110k point cloud).
    # GPU-accelerated, ~2-5 min for 800 frames on GTX 1650.
    num_frames = len(list(Path(frames_dir).glob("*.png"))) + len(list(Path(frames_dir).glob("*.jpg")))
    print(f"  [2/4] Matching features (exhaustive, {num_frames} frames)...")
    subprocess.run([
        colmap_bin, "exhaustive_matcher",
        "--database_path", str(database_path),
        "--SiftMatching.use_gpu", use_gpu,
    ], check=True)

    # Mapper
    print("  [3/4] Running mapper (sparse reconstruction)...")
    subprocess.run([
        colmap_bin, "mapper",
        "--database_path", str(database_path),
        "--image_path", str(frames_dir),
        "--output_path", str(sparse_dir),
    ], check=True)

    # Find the largest model (most registered images) — COLMAP may produce multiple
    ply_path = output_dir / "sparse.ply"
    model_dirs = sorted(sparse_dir.iterdir()) if sparse_dir.exists() else []
    model_dirs = [d for d in model_dirs if d.is_dir() and d.name.isdigit()]

    if model_dirs:
        # Pick largest by file size of images.bin (proxy for registered camera count)
        best = max(model_dirs, key=lambda d: (d / "images.bin").stat().st_size
                   if (d / "images.bin").exists() else 0)
        print(f"  [4/4] Exporting model {best.name} ({len(model_dirs)} total) to PLY...")
        subprocess.run([
            colmap_bin, "model_converter",
            "--input_path", str(best),
            "--output_path", str(ply_path),
            "--output_type", "PLY",
        ], check=True)
    else:
        print("  [4/4] Warning: No models found — mapper may have failed")
        ply_path = None

    return {
        "sparse_dir": str(sparse_dir),
        "ply_path": str(ply_path) if ply_path else None,
        "database_path": str(database_path),
        "num_models": len(model_dirs),
    }


def reconstruct_dense(
    frames_dir: Path,
    sparse_dir: Path,
    output_dir: Path,
    colmap_bin: str,
    gpu_info: dict,
) -> dict:
    """Run COLMAP dense reconstruction (MVS).

    Requires GPU with ~3.5GB+ VRAM. Uses max_image_size=1000 as safety cap.
    Returns dict with fused PLY path.
    """
    dense_dir = output_dir / "dense"
    dense_dir.mkdir(parents=True, exist_ok=True)

    model_dir = Path(sparse_dir) / "0"
    if not model_dir.exists():
        return {"error": "No sparse model found at sparse/0", "ply_path": None}

    # Undistort
    print("  [dense 1/3] Undistorting images...")
    subprocess.run([
        colmap_bin, "image_undistorter",
        "--image_path", str(frames_dir),
        "--input_path", str(model_dir),
        "--output_path", str(dense_dir),
        "--output_type", "COLMAP",
        "--max_image_size", "1000",
    ], check=True)

    # Patch Match Stereo
    print("  [dense 2/3] Running patch match stereo...")
    subprocess.run([
        colmap_bin, "patch_match_stereo",
        "--workspace_path", str(dense_dir),
        "--workspace_format", "COLMAP",
        "--PatchMatchStereo.geom_consistency", "true",
        "--PatchMatchStereo.gpu_index", "0",
    ], check=True)

    # Stereo Fusion — adaptive check_num_images based on dataset size
    fused_ply = dense_dir / "fused.ply"
    print("  [dense 3/3] Fusing to dense point cloud...")
    fusion_cmd = [
        colmap_bin, "stereo_fusion",
        "--workspace_path", str(dense_dir),
        "--workspace_format", "COLMAP",
        "--output_path", str(fused_ply),
        "--output_type", "PLY",
    ]
    # Only lower check_num_images for small datasets (<200 frames)
    num_frames = len(list(Path(frames_dir).glob("*.png"))) + len(list(Path(frames_dir).glob("*.jpg")))
    if num_frames < 200:
        fusion_cmd.extend(["--StereoFusion.check_num_images", "15"])
    subprocess.run(fusion_cmd, check=True)

    # Poisson surface reconstruction -> actual mesh
    mesh_ply = dense_dir / "meshed.ply"
    print("  [dense +] Running Poisson surface reconstruction...")
    try:
        subprocess.run([
            colmap_bin, "poisson_mesher",
            "--input_path", str(fused_ply),
            "--output_path", str(mesh_ply),
        ], check=True)
        print(f"  Mesh saved: {mesh_ply}")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"  Poisson mesher skipped ({e}). Dense cloud still available.")
        mesh_ply = None

    return {
        "ply_path": str(fused_ply),
        "mesh_path": str(mesh_ply) if mesh_ply and mesh_ply.exists() else None,
    }


def print_cloud_guidance(zip_path: Optional[str] = None, preferred: str = "colab", mode: str = "meshroom"):
    """Print step-by-step cloud reconstruction instructions."""
    print("\n" + "=" * 60)
    print("Cloud Reconstruction Options")
    print("=" * 60)

    if zip_path:
        print(f"\nYour frames ZIP: {zip_path}")
        print("Upload this to one of the services below.\n")

    print("1. Google Colab + COLMAP (FREE — T4 GPU, 16GB VRAM)")
    print("   - Open: https://colab.research.google.com")
    print("   - Install: !apt-get install colmap")
    print("   - Upload your frames ZIP and extract")
    print("   - Run COLMAP feature_extractor → exhaustive_matcher → mapper")
    if mode == "splat":
        print("   - Then train with gsplat (Apache 2.0, pip install gsplat)")
        print("   - Or use: github.com/camenduru/gaussian-splatting-colab")
    elif mode == "nerf":
        print("   - Then train with nerfstudio (Apache 2.0, pip install nerfstudio)")
        print("   - Run: ns-process-data images --data ./frames --output-dir ./processed")
        print("   - Run: ns-train nerfacto --data ./processed")
    else:
        print("   - Download the sparse/dense PLY result")
    if preferred == "colab":
        print("   *** RECOMMENDED — free, full control ***")

    print("\n2. KIRI Engine (FREE web upload)")
    print("   - Go to: https://www.kiriengine.com")
    print("   - Upload frames (drag and drop)")
    print("   - Processes automatically, download 3D model")
    print("   - Easiest option, less control over parameters")

    print("\n3. Runpod (PAID — $5 free credits)")
    print("   - Go to: https://www.runpod.io")
    print("   - Launch a GPU pod (COLMAP + gsplat/nerfstudio pre-installable)")
    print("   - Upload frames, run full pipeline")
    print("   - Best for large datasets or repeated processing")

    print("\nNote: Luma AI has suspended 3DGS cloud processing.")
    print("=" * 60)


def find_meshroom() -> Optional[str]:
    """Find meshroom_batch CLI binary."""
    path_bin = shutil.which("meshroom_batch")
    if path_bin:
        return path_bin
    # Common Windows install location
    for candidate in [
        Path("C:/Program Files/Meshroom/meshroom_batch.exe"),
        Path("C:/Program Files/AliceVision/bin/meshroom_batch.exe"),
    ]:
        if candidate.exists():
            return str(candidate)
    return None


def reconstruct_meshroom(
    frames_dir: Path,
    output_dir: Path,
    detail_level: str = "high",
) -> dict:
    """Run full AliceVision/Meshroom pipeline via meshroom_batch CLI.

    Uses DSP-SIFT + guided matching, SGM dense stereo, Delaunay meshing,
    and multi-band texturing. Parameters adapt to content detail level.

    License: MPL-2.0 — subprocess calls require no source disclosure.
    Returns dict with mesh/texture paths.
    """
    meshroom_bin = find_meshroom()
    if meshroom_bin is None:
        return {"error": "meshroom_batch not found", "mesh_path": None}

    meshroom_dir = output_dir / "meshroom"
    meshroom_dir.mkdir(parents=True, exist_ok=True)

    # Build param overrides based on content detail level
    overrides = []

    if detail_level == "high":
        # Standard aggressive params — don't choke quality
        overrides.extend([
            "FeatureExtraction:describerTypes=dspsift",
            "FeatureExtraction:describerPreset=high",
            "FeatureMatching:guidedMatching=True",
            "DepthMap:downscale=2",
            "DepthMapFilter:minConsistentCameras=3",
        ])
    elif detail_level == "medium":
        overrides.extend([
            "FeatureExtraction:describerTypes=dspsift,akaze",
            "FeatureExtraction:describerPreset=high",
            "FeatureMatching:guidedMatching=True",
            "FeatureMatching:geometricErrorMax=5.0",
            "DepthMap:downscale=1",
            "DepthMap:sgmGammaC=8.0",
            "DepthMap:sgmGammaP=10.0",
            "DepthMapFilter:minConsistentCameras=2",
        ])
    else:  # low — soft fleck fallback
        overrides.extend([
            "FeatureExtraction:describerTypes=dspsift,akaze",
            "FeatureExtraction:describerPreset=ultra",
            "FeatureMatching:guidedMatching=True",
            "FeatureMatching:geometricErrorMax=6.0",
            "DepthMap:downscale=1",
            "DepthMap:sgmGammaC=10.0",
            "DepthMap:sgmGammaP=12.0",
            "DepthMap:sgmWSH=6",
            "DepthMapFilter:minConsistentCameras=2",
            "DepthMapFilter:minConsistentCamerasBadSimilarity=3",
        ])

    cmd = [
        meshroom_bin,
        "--input", str(frames_dir),
        "--output", str(meshroom_dir),
    ]
    for override in overrides:
        cmd.extend(["--paramOverrides", override])

    print(f"  Running Meshroom pipeline ({detail_level} detail params)...")
    subprocess.run(cmd, check=True)

    # Find output mesh
    obj_files = list(meshroom_dir.rglob("*.obj"))
    mesh_path = str(obj_files[0]) if obj_files else None

    return {"mesh_path": mesh_path, "output_dir": str(meshroom_dir)}


def _print_install_guidance():
    """Print COLMAP installation instructions."""
    print("\nCOLMAP not found. Installation options:")
    print("  Windows: Download from https://github.com/colmap/colmap/releases")
    print("           Extract and add to PATH, or place in project as:")
    print("           COLMAP/COLMAP-3.9.1-windows-cuda/COLMAP.bat")
    print("  Linux:   sudo apt-get install colmap")
    print("  macOS:   brew install colmap")
    print("  Conda:   conda install -c conda-forge colmap")


def run_reconstruction(
    frames_dir: Path,
    output_dir: Path,
    mode: str = "meshroom",
    dense: bool = False,
    cloud: bool = False,
    gpu_info: Optional[dict] = None,
    zip_path: Optional[str] = None,
) -> dict:
    """Main reconstruction dispatcher called from pipeline.py.

    Args:
        frames_dir: directory of prepared frames
        output_dir: project output directory for reconstruction artifacts
        mode: pipeline mode (meshroom/splat/nerf)
        dense: run dense MVS (meshroom mode only)
        cloud: skip local, print cloud guidance instead
        gpu_info: GPU detection result (or None to auto-detect)
        zip_path: path to frames ZIP for cloud upload guidance

    Returns:
        dict with reconstruction results
    """
    recon_dir = output_dir / "reconstruction"
    recon_dir.mkdir(parents=True, exist_ok=True)

    if gpu_info is None:
        gpu_info = detect_gpu()

    # Cloud-only path
    if cloud:
        print_cloud_guidance(zip_path=zip_path, preferred="colab", mode=mode)
        return {"mode": "cloud", "guidance_printed": True}

    # Find COLMAP
    colmap_bin = find_colmap()
    if colmap_bin is None:
        print("\n[Reconstruction] COLMAP not found locally.")
        _print_install_guidance()
        print_cloud_guidance(zip_path=zip_path, preferred="colab", mode=mode)
        return {"mode": "no_colmap", "guidance_printed": True}

    # Assess content detail level
    detail = assess_detail_level(frames_dir)

    print(f"\n[Reconstruction] Using COLMAP: {colmap_bin}")
    print(f"  GPU: {gpu_info['name']} ({gpu_info['vram_mb']}MB)" if gpu_info["has_nvidia"]
          else "  GPU: None (CPU mode)")
    print(f"  Mode: {mode}")
    print(f"  Content: {detail['detail_level']} detail (variance: {detail['avg_variance']})")

    # For meshroom mode with --dense: try AliceVision first (SGM > PatchMatch)
    # Falls back to COLMAP if meshroom_batch not installed
    if dense and mode == "meshroom":
        meshroom_bin = find_meshroom()
        if meshroom_bin:
            print(f"\n[Meshroom] Found: {meshroom_bin}")
            print("  Using AliceVision full pipeline (SfM + SGM dense + mesh + texture)")
            meshroom_result = reconstruct_meshroom(
                frames_dir=frames_dir,
                output_dir=recon_dir,
                detail_level=detail["detail_level"],
            )
            return {"mode": "meshroom", "meshroom": meshroom_result}
        else:
            print("\n  Meshroom not found — using COLMAP for dense reconstruction")

    # Sparse reconstruction (always for COLMAP path)
    print("\nRunning sparse reconstruction...")
    sparse_result = reconstruct_sparse(
        frames_dir=frames_dir,
        output_dir=recon_dir,
        colmap_bin=colmap_bin,
        mode=mode,
        gpu_info=gpu_info,
    )

    result = {"mode": "local", "sparse": sparse_result}

    # Dense reconstruction via COLMAP (fallback when Meshroom not available)
    if dense and mode == "meshroom":
        if not gpu_info.get("cuda_available"):
            print("\nSkipping dense reconstruction — requires NVIDIA GPU.")
            result["dense_skipped"] = "no_gpu"
        else:
            if gpu_info.get("vram_mb", 0) < 3000:
                print(f"\nWarning: Dense MVS needs ~3.5GB VRAM, you have {gpu_info['vram_mb']}MB.")
                print("Proceeding anyway (may fail or be very slow)...")
            else:
                print("\nRunning dense reconstruction...")
            dense_result = reconstruct_dense(
                frames_dir=frames_dir,
                sparse_dir=Path(sparse_result["sparse_dir"]),
                output_dir=recon_dir,
                colmap_bin=colmap_bin,
                gpu_info=gpu_info,
            )
            result["dense"] = dense_result
    elif dense and mode != "meshroom":
        print(f"\nDense reconstruction skipped — not applicable for '{mode}' mode.")
        print("  (splat/nerf tools handle densification natively)")
        result["dense_skipped"] = f"mode_{mode}"

    return result


def main():
    parser = argparse.ArgumentParser(
        description="COLMAP reconstruction for Dreams photogrammetry"
    )
    parser.add_argument("frames_dir", type=Path, help="Directory of prepared frames")
    parser.add_argument("output_dir", type=Path, help="Output directory")
    parser.add_argument("--mode", choices=["meshroom", "splat", "nerf"], default="meshroom",
                        help="Pipeline mode (default: meshroom)")
    parser.add_argument("--dense", action="store_true",
                        help="Also run dense MVS (meshroom mode, needs ~3.5GB VRAM)")
    parser.add_argument("--cloud", action="store_true",
                        help="Skip local, print cloud service instructions")
    parser.add_argument("--check-hardware", action="store_true",
                        help="Detect GPU and print recommendation")

    args = parser.parse_args()

    print("=" * 60)
    print("Dreams to Reality: COLMAP Reconstruction")
    print("=" * 60)

    if args.check_hardware:
        gpu = detect_gpu()
        print(f"\nGPU Detection:")
        print(f"  NVIDIA GPU: {'Yes' if gpu['has_nvidia'] else 'No'}")
        print(f"  Name: {gpu['name']}")
        print(f"  VRAM: {gpu['vram_mb']}MB")
        print(f"  CUDA: {'Available' if gpu['cuda_available'] else 'Not available'}")
        if gpu["has_nvidia"] and gpu["vram_mb"] >= 4000:
            print("\n  Recommendation: Local reconstruction should work well.")
        elif gpu["has_nvidia"]:
            print(f"\n  Recommendation: Sparse OK locally. Dense may struggle ({gpu['vram_mb']}MB < 4GB).")
            print("  Consider --cloud for dense reconstruction.")
        else:
            print("\n  Recommendation: CPU-only mode (slow). Consider --cloud for faster results.")

        colmap = find_colmap()
        print(f"\n  COLMAP: {'Found at ' + colmap if colmap else 'Not found'}")
        if not colmap:
            _print_install_guidance()
        return

    result = run_reconstruction(
        frames_dir=args.frames_dir,
        output_dir=args.output_dir,
        mode=args.mode,
        dense=args.dense,
        cloud=args.cloud,
    )

    print("\n" + "=" * 60)
    print("Reconstruction Complete!")
    print("=" * 60)
    if result.get("sparse", {}).get("ply_path"):
        print(f"Sparse PLY: {result['sparse']['ply_path']}")
    if result.get("dense", {}).get("ply_path"):
        print(f"Dense PLY: {result['dense']['ply_path']}")


if __name__ == "__main__":
    main()
