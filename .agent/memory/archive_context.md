# 📦 Project Context Archive

> **Status**: Archived
> **Source**: Moved from `CLAUDE.md` to reduce token usage
> **Date**: 2026-02-03
> **Description**: Original technical context and agent guidelines from the project's inception.

---

## Technical Context: Why Dreams is Hard (Original)
- Dreams uses **signed distance field (SDF) rendering**, not traditional polygons
- Limited camera control makes consistent multi-angle capture difficult
- Post-processing effects (bloom, DoF) confuse photogrammetry algorithms
- Output quality varies wildly based on the Dreams creation's complexity

## Approaches Under Consideration (Early Phase)
1. **Traditional photogrammetry** — preprocessed frames → feature matching → point cloud → mesh
2. **NeRF-based** — neural radiance fields from video (more tolerant of lighting variation)
3. **Hybrid** — combine multiple techniques based on scene characteristics

## Agent Guidelines (Early Phase)
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
