"""
Dreams to Reality — API Server
Handles video uploads and runs the photogrammetry pipeline.
All processing happens locally. Nothing leaves your machine.
"""

import os
import uuid
import shutil
import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Dreams to Reality API", version="0.1.0")

# Only allow local connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Paths
BASE_DIR = Path(__file__).parent.parent
UPLOADS_DIR = BASE_DIR / "uploads"
RESULTS_DIR = BASE_DIR / "results"
UPLOADS_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

# Track processing jobs
jobs: dict[str, dict] = {}

MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB max per video
ALLOWED_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}


def validate_upload(filename: str, size: int) -> None:
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"Invalid file type: {ext}. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")
    if size > MAX_FILE_SIZE:
        raise HTTPException(400, f"File too large. Max: {MAX_FILE_SIZE // (1024*1024)}MB")


@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}


@app.post("/api/upload")
async def upload_video(
    geometry_video: UploadFile = File(...),
    texture_video: Optional[UploadFile] = File(None),
):
    """Upload one or two video recordings from Dreams capture tool."""
    job_id = str(uuid.uuid4())[:8]
    job_dir = UPLOADS_DIR / job_id
    job_dir.mkdir(parents=True)

    # Save geometry pass video
    geo_data = await geometry_video.read()
    validate_upload(geometry_video.filename or "video.mp4", len(geo_data))
    geo_ext = Path(geometry_video.filename or "video.mp4").suffix.lower()
    geo_path = job_dir / f"geometry{geo_ext}"
    geo_path.write_bytes(geo_data)

    # Save texture pass video (optional)
    tex_path = None
    if texture_video:
        tex_data = await texture_video.read()
        validate_upload(texture_video.filename or "video.mp4", len(tex_data))
        tex_ext = Path(texture_video.filename or "video.mp4").suffix.lower()
        tex_path = job_dir / f"texture{tex_ext}"
        tex_path.write_bytes(tex_data)

    jobs[job_id] = {
        "status": "uploaded",
        "step": "waiting",
        "progress": 0,
        "geometry_video": str(geo_path),
        "texture_video": str(tex_path) if tex_path else None,
        "result": None,
        "error": None,
    }

    return {"job_id": job_id, "status": "uploaded"}


@app.post("/api/process/{job_id}")
async def start_processing(job_id: str):
    """Start the photogrammetry pipeline for an uploaded job."""
    if job_id not in jobs:
        raise HTTPException(404, "Job not found")

    job = jobs[job_id]
    if job["status"] == "processing":
        raise HTTPException(409, "Already processing")

    job["status"] = "processing"
    job["step"] = "extracting_frames"
    job["progress"] = 0

    # Run pipeline in background
    asyncio.create_task(_run_pipeline(job_id))

    return {"job_id": job_id, "status": "processing"}


@app.get("/api/status/{job_id}")
async def get_status(job_id: str):
    """Check processing status for a job."""
    if job_id not in jobs:
        raise HTTPException(404, "Job not found")
    return jobs[job_id]


@app.get("/api/download/{job_id}")
async def download_result(job_id: str):
    """Download the resulting 3D model."""
    if job_id not in jobs:
        raise HTTPException(404, "Job not found")

    job = jobs[job_id]
    if job["status"] != "complete":
        raise HTTPException(400, "Processing not complete")

    result_path = Path(job["result"])
    if not result_path.exists():
        raise HTTPException(404, "Result file not found")

    return FileResponse(result_path, filename=result_path.name)


async def _run_pipeline(job_id: str):
    """Run the full photogrammetry pipeline."""
    import sys
    sys.path.insert(0, str(BASE_DIR))

    job = jobs[job_id]
    job_dir = UPLOADS_DIR / job_id
    result_dir = RESULTS_DIR / job_id
    result_dir.mkdir(parents=True, exist_ok=True)

    try:
        geo_video = Path(job["geometry_video"])

        # Step 1: Extract frames
        job["step"] = "extracting_frames"
        job["progress"] = 10
        raw_dir = job_dir / "raw_frames"
        raw_dir.mkdir(exist_ok=True)

        await asyncio.to_thread(
            _extract_frames, geo_video, raw_dir, every_n=5
        )

        # Step 2: Preprocess (blur detection, UI removal, dedup)
        job["step"] = "preprocessing"
        job["progress"] = 30
        clean_dir = job_dir / "clean_frames"
        clean_dir.mkdir(exist_ok=True)

        await asyncio.to_thread(
            _preprocess, raw_dir, clean_dir
        )

        # Step 3: Background segmentation
        job["step"] = "segmenting"
        job["progress"] = 50
        seg_dir = job_dir / "segmented_frames"
        seg_dir.mkdir(exist_ok=True)

        await asyncio.to_thread(
            _segment, clean_dir, seg_dir
        )

        # Step 4: Reconstruction (COLMAP)
        job["step"] = "reconstructing"
        job["progress"] = 70

        model_path = await asyncio.to_thread(
            _reconstruct, seg_dir, result_dir
        )

        job["status"] = "complete"
        job["step"] = "done"
        job["progress"] = 100
        job["result"] = str(model_path)

    except Exception as e:
        job["status"] = "error"
        job["error"] = str(e)
        job["step"] = "failed"


def _extract_frames(video_path: Path, output_dir: Path, every_n: int = 5):
    """Extract frames from video."""
    import cv2

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {video_path}")

    count = 0
    saved = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if count % every_n == 0:
            frame_path = output_dir / f"frame_{saved:06d}.png"
            cv2.imwrite(str(frame_path), frame)
            saved += 1
        count += 1

    cap.release()
    return saved


def _preprocess(input_dir: Path, output_dir: Path):
    """Run Dreams-tuned preprocessing."""
    try:
        from preprocess import preprocess_frames
        preprocess_frames(
            input_dir=input_dir,
            output_dir=output_dir,
            skip_ui=True,
            min_blur_score=2.0,
            duplicate_threshold=0.95,
        )
    except ImportError:
        # Fallback: just copy frames if preprocess module not available
        import shutil
        for f in sorted(input_dir.glob("*.png")):
            shutil.copy2(f, output_dir / f.name)


def _segment(input_dir: Path, output_dir: Path):
    """Run background segmentation."""
    try:
        from segment import segment_frames
        segment_frames(
            input_dir=input_dir,
            output_dir=output_dir,
            model_name="u2net",
        )
    except ImportError:
        # Fallback: copy frames unsegmented
        import shutil
        for f in sorted(input_dir.glob("*.png")):
            shutil.copy2(f, output_dir / f.name)


def _write_colmap_missing(frames_dir: Path, output_dir: Path) -> Path:
    """Create a structured placeholder when COLMAP is unavailable."""
    frames = sorted(frames_dir.glob("*.png"))
    payload = {
        "status": "missing_dependency",
        "missing": "colmap",
        "frames_ready": str(frames_dir),
        "total_frames": len(frames),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "instructions": "Install COLMAP (https://colmap.github.io/install.html) and re-run the pipeline.",
    }
    placeholder = output_dir / "colmap_missing.json"
    placeholder.write_text(json.dumps(payload, indent=2))
    return placeholder


def _reconstruct(frames_dir: Path, output_dir: Path) -> Path:
    """Run COLMAP reconstruction."""
    colmap_bin = shutil.which("colmap")

    if not colmap_bin:
        return _write_colmap_missing(frames_dir, output_dir)

    # Run COLMAP automatic reconstructor
    db_path = output_dir / "database.db"
    sparse_dir = output_dir / "sparse"
    sparse_dir.mkdir(exist_ok=True)

    # Feature extraction
    os.system(
        f'"{colmap_bin}" feature_extractor '
        f"--database_path {db_path} "
        f"--image_path {frames_dir} "
        f"--ImageReader.single_camera 1"
    )

    # Feature matching
    os.system(
        f'"{colmap_bin}" sequential_matcher '
        f"--database_path {db_path}"
    )

    # Sparse reconstruction
    os.system(
        f'"{colmap_bin}" mapper '
        f"--database_path {db_path} "
        f"--image_path {frames_dir} "
        f"--output_path {sparse_dir}"
    )

    # Export as PLY
    ply_path = output_dir / "model.ply"
    os.system(
        f'"{colmap_bin}" model_converter '
        f"--input_path {sparse_dir}/0 "
        f"--output_path {ply_path} "
        f"--output_type PLY"
    )

    if ply_path.exists():
        return ply_path

    return sparse_dir


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
