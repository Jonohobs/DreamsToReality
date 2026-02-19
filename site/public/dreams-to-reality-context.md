# Dreams to Reality — Pipeline Context for Claude

> Paste this into a Claude conversation to give it full context about the Dreams to Reality photogrammetry pipeline. Then ask your question.

## What Is This?

Dreams to Reality is an open-source pipeline that extracts 3D models from PlayStation Dreams. You record your Dreams sculpt, run it through the pipeline, and get a 3D model you can print, import into Blender, or use in a game engine.

**GitHub:** https://github.com/Jonohobs/DreamsToReality
**License:** MIT (free, open source)

---

## The Pipeline (5 Steps)

### Step 1: Record Your Sculpt in Dreams (PS5)

Record a video of your camera orbiting around your sculpt in Dreams. The pipeline needs multiple angles.

**Critical: Add surface texture first.** Photogrammetry needs visual detail to work. Dreams' smooth surfaces are its biggest challenge.

Three methods:
1. **Paint method (recommended):** Duplicate your sculpt, spray random X marks and speckles in contrasting colours (blue, green, red, orange, white) all over every surface. The messier, the better.
2. **Gobo method:** Use gobo spotlight projectors in Dreams to project tracking patterns onto surfaces. Limited to ~6 per scene.
3. **Two-pass workflow:** Capture the messy version for geometry, then the clean original for texture mapping.

**Camera settings (kill all post-processing):**
- Aperture: 0% (depth of field OFF — critical)
- FOV: 50-60 degrees
- Bloom: OFF
- Motion blur: OFF
- Vignette: OFF
- Film grain: OFF
- Chromatic aberration: OFF
- Lens flare: OFF
- Brightness: slightly down (makes patterns pop)
- Sharpen: tiny bit (not maxed — causes halos)
- Background: matte black

**Camera orbit:** 3 rings — high angle (45° down), eye level, low angle (30° up). ~90° keyframe intervals. Even spacing.

### Step 2: Extract Frames

```bash
python pipeline.py video.mp4 my_project/ --fps 2
```

Extracts frames from your video at 2 fps (configurable). Lazy extraction — skips if frames already exist.

### Step 3: Preprocess

The pipeline automatically:
- **Filters UI overlays** — removes frames showing Dreams interface elements
- **Detects blur** — removes blurry/motion-blur frames (Laplacian variance, threshold 2.0 for Dreams' soft render style)
- **Removes duplicates** — removes near-identical frames (histogram comparison, 0.98 threshold)

**Note:** Dreams renders with a "soft" SDF style. Standard blur detection thresholds (>100) reject 99% of valid Dreams frames. The pipeline uses 2.0 as default.

### Step 4: Segment (Background Removal)

```bash
python segment.py clean_frames/ segmented_frames/ --model u2net
```

Uses rembg (U2-Net) to isolate the subject and replace the background with solid black. Runs on CPU (~1-3 sec/frame), no GPU required.

**Available models:**
- `u2net` — general purpose, good default (~170MB)
- `u2net_human_seg` — optimised for people
- `isnet-general-use` — fast, good for objects

**Key finding:** Our segment.py background removal produces better results than RealityScan's built-in `generateAIMasks` for Dreams captures. RealityScan's AI masks cut into the actual object.

### Step 5: Reconstruct

Three options:

**Option A — RealityScan CLI (recommended, fastest)**
```bash
run_realityscan.bat <segmented_frames_dir>
```
RealityScan (formerly RealityCapture) by Capturing Reality (Slovakia, EU). Free for <$1M revenue. 10-50x faster than COLMAP.

Best batch command:
```
RealityScan.exe -addFolder <frames> -align -selectMaximalComponent -setReconstructionRegionByDensity -calculateHighModel -cleanModel -closeHoles -smooth -selectLargeTrianglesRel 10 -removeSelectedTriangles -calculateTexture -save project.rsproj
```

**Option B — COLMAP (open source, slower)**
```bash
python pipeline.py video.mp4 my_project/ --reconstruct
# Add --dense for dense reconstruction (needs ~3.5GB VRAM)
```
Good for sparse point clouds and camera poses. Dense reconstruction is very slow on consumer GPUs (~11 sec/view on GTX 1650).

**Option C — Cloud services**
```bash
python pipeline.py video.mp4 my_project/ --cloud
```
Prints instructions for uploading to cloud reconstruction services.

---

## Full Pipeline Command

```bash
# Install dependencies
pip install -r requirements.txt

# Run the full pipeline
python pipeline.py recording.mp4 my_project/ --fps 2 --reconstruct

# All options
python pipeline.py recording.mp4 my_project/ \
  --fps 2 \
  --mode meshroom \
  --sharpen \
  --denoise \
  --no-segment \
  --no-duplicate-filter \
  --segment-model u2net \
  --save-masks \
  --mask-artifacts \
  --no-auto-crop \
  --crop-padding 0.10 \
  --reconstruct \
  --dense \
  --cloud \
  --check-hardware
```

### Pipeline Flags Reference

| Flag | What it does |
|------|-------------|
| `--fps N` | Frames per second to extract (default: 2) |
| `--mode` | `meshroom`, `nerf`, or `splat` |
| `--sharpen` | Enable image sharpening |
| `--denoise` | Enable denoising |
| `--no-segment` | Skip background removal |
| `--no-duplicate-filter` | Keep near-duplicates (useful for turntable captures) |
| `--segment-model` | `u2net`, `u2net_human_seg`, or `isnet-general-use` |
| `--save-masks` | Save segmentation masks for debugging |
| `--mask-artifacts` | Zero out corner light artifacts (Dreams rendering bug) |
| `--no-auto-crop` | Skip automatic cropping |
| `--crop-padding` | Padding around crop region (default: 10%) |
| `--reconstruct` | Run COLMAP sparse reconstruction |
| `--dense` | Also run COLMAP dense MVS |
| `--cloud` | Print cloud service upload instructions |
| `--check-hardware` | Detect GPU/VRAM and recommend local vs cloud |

---

## Common Issues

### "All my frames got rejected"
Dreams' soft SDF rendering style has very low Laplacian variance (~3-5 vs >100 for normal video). The pipeline defaults to a threshold of 2.0 specifically for Dreams. If you're still losing too many frames, try `--min-blur-score 1.0`.

### "The model looks dark / colours are wrong"
Black background from segmentation can bleed into mesh colours. Try:
- White background: `python segment.py input/ output/ --bg-color 255 255 255`
- Skip segmentation entirely: `--no-segment`

### "Too many / too few frames"
Sweet spot is 100-200 segmented frames. Fewer = less matcher confusion. Adjust `--fps` or `--duplicate-threshold`.

### "Reconstruction failed / bad mesh"
Check that your sculpt has enough surface texture. Smooth, uniformly-coloured surfaces WILL fail — this is a fundamental limitation of photogrammetry, not a bug. Add paint mess or gobo patterns.

### "COLMAP is incredibly slow"
COLMAP dense reconstruction on a GTX 1650 takes ~11 sec/view. Use RealityScan instead (10-50x faster) or upload to a cloud service.

---

## Reconstruction Software (EU-preferred)

| Tool | Country | Notes |
|------|---------|-------|
| RealityScan | Slovakia (EU) | Fastest, free <$1M revenue, CLI automation |
| Meshroom | France (EU) | Open source, AliceVision, GPU recommended |
| 3DF Zephyr | Italy (EU) | Commercial, good quality |
| COLMAP | Open source | Slower but flexible, good for camera poses |

---

## Two-Pass Capture Workflow

For the best results, capture your sculpt twice:

1. **Geometry pass** — sculpt covered in paint mess or gobo patterns. This gives the reconstruction software surface detail to lock onto.
2. **Texture pass** — clean, original sculpt. This captures the real colours and surface finish.

Use RealityScan's `reprojectTexture` command to combine geometry from pass 1 with textures from pass 2.

---

## In-Dreams Scanner Build

You can build a photogrammetry capture rig inside Dreams itself:

1. **Red platform** with white boundary posts showing where to place your sculpt
2. **Gobo spotlights** projecting tracking patterns onto the sculpt surface
3. **Camera boom arm** on a keyframe orbit — 3 rings (high, eye-level, low angle)
4. **Timer sequence** that automates: emit patterns → orbit camera → destroy patterns → orbit again (clean)

Full build instructions: see BUILD_GUIDE_DREAMS.md in the GitHub repo.

---

## Tech Stack

- **Python 3** with OpenCV, rembg, tqdm, numpy
- **COLMAP** for sparse/dense reconstruction
- **RealityScan** CLI for fast reconstruction
- **FFmpeg** for frame extraction
- **React + Vite + Tailwind** for the web frontend
- **FastAPI** for the backend API

---

*Last updated: 2026-02-19 · MIT License · github.com/Jonohobs/DreamsToReality*
