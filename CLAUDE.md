# Dreams to Reality Converter

## Vision
A photogrammetry tool/pipeline for extracting 3D models from Dreams (PlayStation). The goal is to convert creations made in Dreams into real-world-usable 3D assets.

## Owner
Jonathan (jonat) — solo developer, also working on an improv multiplayer game and AI workflow optimization.

## Current Status: Research & Experimentation

### What exists so far
- Frame extraction from Dreams gameplay footage (PNG sequences from video capture)
- RealityScan data exports (.dat files — models, metadata, color normalization, control points)
- Reference screenshots of Dreams bugs/artifacts
- No codebase yet — still exploring approaches

### Key locations (on this machine)
- `~/OneDrive/Desktop/DesktopFiles/ssvid.net--Dreams-Photogrammetry-Test_1080p frames/` — extracted video frames
- `~/OneDrive/Desktop/DesktopFiles/Reality scan attempt 1/` — RealityScan export data
- `~/iCloudDrive/Desktop/Dreams Bugs/` — reference images of Dreams rendering bugs/artifacts

## Technical Challenges
- Dreams uses a signed distance field (SDF) renderer, not traditional polygons — this makes photogrammetry from screenshots fundamentally different from real-world scanning
- Camera control in Dreams is limited, making consistent multi-angle capture difficult
- Dreams' lighting and post-processing effects can confuse photogrammetry algorithms
- Output quality depends heavily on the complexity of the Dreams creation

## Potential Approaches (to be explored)
- Traditional photogrammetry pipeline (frame extraction → feature matching → point cloud → mesh)
- Neural radiance fields (NeRF) from captured footage
- Direct SDF extraction if Dreams' data format can be reverse-engineered
- Hybrid approach combining multiple techniques

## Agent Guidelines
- This project is exploratory — don't over-engineer or build production infrastructure prematurely
- Prioritize quick experiments and prototypes over polished code
- Document findings and dead ends — knowing what doesn't work is valuable here
- Python is the likely language for tooling (photogrammetry libraries, image processing)
- Ask before committing to a specific photogrammetry library or approach — the field is moving fast
