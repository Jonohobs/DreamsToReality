```
    ____                                  __           ____             ___ __       
   / __ \_________  ____ _____ ___  _____/ /_____     / __ \___  ____ _/ (_) /___  __
  / / / / ___/ _ \/ __ `/ __ `__ \/ ___/ __/ __ \   / /_/ / _ \/ __ `/ / / __/ / / /
 / /_/ / /  /  __/ /_/ / / / / / (__  ) /_/ /_/ /  / _, _/  __/ /_/ / / / /_/ /_/ / 
/_____/_/   \___/\__,_/_/ /_/ /_/____/\__/\____/  /_/ |_|\___/\__,_/_/_/\__/\__, /  
                                                                           /____/   
                    🎮 PlayStation Dreams → 🧊 3D Models
```

# Dreams to Reality 🎮➡️🗿 Converter

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
| Pipeline Automation | `pipeline.py` | ✅ V1 Implemented |
| Research Report | `research_report.md` | ✅ Complete |
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
For details on Dreams SDF rendering and photogrammetry challenges, see [DREAMS_RENDERING_FINDINGS.md](DREAMS_RENDERING_FINDINGS.md).

> [!IMPORTANT]
> **System Stability**: `colmap_out/` and `frames/` directories contain thousands of files. They MUST be excluded from the IDE via `.gitignore` to prevent file-watcher freezing. Do not remove these exclusions.

## Agent Infrastructure (Universal)

This repo includes a persistent memory and skills system in `.agent/`. **ALL AGENTS** (Claude, Gemini, ChatGPT, Local LLMs) are expected to read and utilize this system to maintain continuity.

```
.agent/
├── memory/
│   ├── context.md      # Who Jonathan is, current projects, preferences
│   ├── decisions.md    # Key decisions made across sessions
│   └── learnings.md    # What works and what doesn't
├── skills/
│   ├── research.md     # Research patterns (Ralph method, GitHub mining)
│   └── cost-routing.md # Model selection based on task complexity
├── workflows/
│   └── save-progress.md
└── ROADMAP.md          # Weekly/monthly/quarterly planning hub
```

**On session start**: Read `.agent/memory/context.md` for background.
**During work**: Update `decisions.md` and `learnings.md` as appropriate.
**Before ending**: Check ROADMAP.md and mark progress.
**For major milestones**: Add a new entry to `JOURNEY.md` to document the narrative of your contribution.

---

## Changelog
- **2026-02-03** — Optimized `preprocess.py` for Dreams' soft render style (threshold 2.0); processed 5.4k frames
- **2026-02-03** — Documented findings in `DREAMS_RENDERING_FINDINGS.md`
- **2026-02-03** — Added `pipeline.py` for automated video-to-frames workflow
- **2026-02-03** — Drafted `CHAPTER_ONE.md` for "The Hidden Prompt" in `scifi-writing/`
- **2026-02-03** — Completed Photogrammetry vs NeRF `research_report.md`
- **2026-02-03** — Added `preprocess.py` frame preprocessing pipeline
- **Initial** — Project setup, research phase
