```
    ____                                  __           ____             ___ __       
   / __ \_________  ____ _____ ___  _____/ /_____     / __ \___  ____ _/ (_) /___  __
  / / / / ___/ _ \/ __ `/ __ `__ \/ ___/ __/ __ \   / /_/ / _ \/ __ `/ / / __/ / / /
 / /_/ / /  /  __/ /_/ / / / / / (__  ) /_/ /_/ /  / _, _/  __/ /_/ / / / /_/ /_/ / 
/_____/_/   \___/\__,_/_/ /_/ /_/____/\__/\____/  /_/ |_|\___/\__,_/_/_/\__/\__, /  
                                                                           /____/   
                    🎮 PlayStation Dreams → 🧊 3D Models
```

# Dreams to Reality Converter

## Vision
A photogrammetry pipeline for extracting 3D models from Dreams (PlayStation). Convert creations made in Dreams into usable 3D assets.

## Owner
Jonathan (jonat) — solo developer, also working on an improv multiplayer game, portfolio website, and AI workflow optimization.

---

## Current Status: Active Development

### What's Built
| Component | File | Status |
|-----------|------|--------|
| Frame Preprocessor | `preprocess.py` | ✅ Working |
| Dependencies | `requirements.txt` | ✅ Defined |

### Frame Preprocessor Features
- **UI overlay detection** — filters out frames with Dreams interface elements
- **Blur detection** — removes blurry/motion-blur frames (Laplacian variance)
- **Duplicate detection** — removes near-identical frames (histogram comparison)
- **CLI interface** — configurable thresholds, progress bars, statistics

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run preprocessing
python preprocess.py <input_frames_dir> <output_dir>

# Options
python preprocess.py input/ output/ --min-blur-score 150 --duplicate-threshold 0.95
```

---

## Key Data Locations
- `~/OneDrive/Desktop/DesktopFiles/ssvid.net--Dreams-Photogrammetry-Test_1080p frames/` — extracted video frames
- `~/OneDrive/Desktop/DesktopFiles/Reality scan attempt 1/` — RealityScan export data
- `~/iCloudDrive/Desktop/Dreams Bugs/` — reference images of Dreams rendering bugs

---

## Technical Context

### Why Dreams is Hard
- Dreams uses **signed distance field (SDF) rendering**, not traditional polygons
- Limited camera control makes consistent multi-angle capture difficult
- Post-processing effects (bloom, DoF) confuse photogrammetry algorithms
- Output quality varies wildly based on the Dreams creation's complexity

### Approaches Under Consideration
1. **Traditional photogrammetry** — preprocessed frames → feature matching → point cloud → mesh
2. **NeRF-based** — neural radiance fields from video (more tolerant of lighting variation)
3. **Hybrid** — combine multiple techniques based on scene characteristics

---

## Next Steps (Roadmap)
- [ ] Test preprocessor on full video capture dataset
- [ ] Integrate with photogrammetry tool (Meshroom? COLMAP?)
- [ ] Experiment with NeRF approach for comparison
- [ ] Document what works and what doesn't for Dreams-specific content

---

## Agent Guidelines

### Do
- Build quick experiments and prototypes
- Document findings, including dead ends
- Use Python for tooling
- Commit working code to the repo frequently

### Don't
- Over-engineer or build production infrastructure prematurely
- Commit to a specific photogrammetry library without discussing first
- Assume traditional photogrammetry techniques will "just work" on Dreams content

### Code Style
- Python with type hints where helpful
- Use OpenCV for image processing
- CLI tools with argparse
- Progress bars with tqdm for long operations

---

## Changelog
- **2026-02-03** — Added `preprocess.py` frame preprocessing pipeline
- **Initial** — Project setup, research phase
