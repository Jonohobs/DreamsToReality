# Technical Findings: PlayStation Dreams Rendering & Pipeline

## Date: 2026-02-03

## Context
During the initial attempt to build a photogrammetry pipeline for PlayStation Dreams video exports, we discovered specific properties of the Dreams rendering engine that impact standard computer vision algorithms.

## Findings

### 1. "Soft" Rendering & Blur Detection
**Observation**: The default Laplacian variance method for blur detection (standard in libraries like OpenCV) fails on Dreams footage.
- **Standard Footage**: Sharp frames typically have a variance > 100.0.
- **Dreams Footage**: Even "sharp" frames average a variance of **3.0 - 5.0**.
- **Cause**: Dreams uses a Signed Distance Field (SDF) hybrid rendering engine. It has a "painterly" soft look, often with built-in temporal anti-aliasing (TAA) and depth-of-field effects that eliminate hard, pixel-perfect edges.
- **Impact**: Standard filters reject >99% of valid frames.
- **Solution**: Adjusted `min_blur_score` threshold to **2.0** for this specific content.

### 2. UI Overlay Inteference
**Observation**: Dreams UI elements (Imps, menus) are high-contrast and sharp.
- **Risk**: Photogrammetry software (Meshroom) may latch onto stationary UI elements rather than the rotating model, causing camera tracking failures.
- **Solution**: The `preprocess.py` script includes a UI detector that checks the top 20% of the screen for high-frequency edges and specific UI colors (blue/orange).

### 3. Pipeline Performance
- **Bottleneck**: `shutil.copy2` and `compareHist` (duplicate detection) are the primary slowdowns.
- **Optimization**: "Lazy" extraction added to `pipeline.py` to avoid re-running FFmpeg if frames exist.

## Current State
- **Pipeline**: Automated (`pipeline.py`) -> Extract -> Preprocess -> Ready for Meshroom.
- **Status**: Pipeline COMPUTED successfully with adjusted thresholds (blur=2.0).
- **Data**: 
  - `data_v1/raw_frames`: 5448 frames
  - `data_v1/clean_frames`: ~5448 frames (Processed and ready)

## Next Steps (If Resuming)
- Evaluate if Photogrammetry is truly viable given the "softness" of the source. NeRF (Neural Radiance Fields) might actually handle the "fleck" style better as it is volumetric by nature, whereas Meshroom relies on feature point matching which requires distinct, sharp features.
- If continuing with Meshroom: Finish the preprocessing run.
- If pivoting to NeRF: The `raw_frames` are already extracted and ready for `ns-process-data` (Nerfstudio).
