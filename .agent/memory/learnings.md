# 💡 Learnings

> What's worked, what hasn't, and insights gained. Prevents repeating mistakes.

---

## AI/Agent Patterns

### What Works ✅
- **Ask AI to build, then explain** — "Ask the robot to build something for you, then ask how the code works. You'll be coding in no time."
- **Opus Audit pattern** — Use cheaper models for drafting, Opus for review/reasoning
- **Writing to MD files** — Simple, version-controlled, readable memory
- **Human in the loop** — Keep humans involved for critical decisions
- **Memory Protocol** — Explicitly ask user: "Should we save this to learnings.md?" for new discoveries. Prevents context loss.
- **Consolidation**: Taking a moment to write to `.agent/memory` when the system hangs or user context switches allows for a clean "hard reset" of the session without losing valid progress.
- **High-Fidelity Saves**: Use powerful models (e.g., Gemini 1.5 Pro) when saving sessions to ensure the conversation state and subtle context are accurately captured and finalized.

### What Doesn't Work ❌
- **Video editing** — "Editing not solved" (noted in research)
- **Direct cloud access** — Google Drive/iCloud require OAuth setup or MCP
- **Antigravity browser** — Currently has $HOME env var issue on this machine
- **Heavy Compute in Antigravity** — Running intense processes (like full COLMAP pipelines) alongside the AI agent can cause UI freezing and model selector timeouts. Better to offload these to a separate terminal/runner.

---

## Tools & Services

| Tool | Verdict | Notes |
|------|---------|-------|
| OpenClaw | ✅ Works | Multi-model routing, good TUI. **Donation-based funding** (GitHub Sponsors), no equity investment. |
| Ollama | ✅ Works | Local, private, free |
| Antigravity | ✅ Works | Good for coding, browser broken |
| Make.com | 🔍 Explore | Automation platform |
| Zapier | 🔍 Explore | More expensive, delays |
| n8n | 🔍 Explore | Self-hostable alternative |
| Meshroom | 🔍 Testing | Photogrammetry for Dreams |
| COLMAP | ❌ Failed | Smeared output on Dreams content |
| Luma AI | 🔍 Testing | 3DGS approach for Dreams (promising) |
| FFMPEG | 🔍 Explore | CLI media processing |

---

## Project-Specific

### Dreams to Reality
- SDF rendering in Dreams ≠ traditional polygons — complicates photogrammetry
- Post-processing effects (bloom, DoF) confuse feature matching
- **Source Verification**: Always verify input resolution (e.g., 360p vs 1080p) before running expensive compute.
- **"Blur" Artifacts**: The "cloudiness" in point clouds from Dreams footage is a visualization artifact of the "fleck" texture, not necessarily soft geometry. Meshing is required to reveal hard edges.
- **COLMAP doesn't work** — Produces a "smear" because it relies on sharp feature matching; Dreams' soft rendering gives it nothing to lock onto
- **Gaussian Splatting (Luma AI) recommended** — 3DGS captures volumetric appearance rather than triangulating hard edges; more forgiving of Dreams' inherent softness
- Pipeline has `--mode splat` for Luma prep (lower blur threshold, auto sharpening/denoising)
- **Custom Pipeline**: `custom_pipeline.py` implements specialized CLAHE/sharpening preprocessing to help standard photogrammetry tools "see" Dreams flecks better.

### Improv Game
- WebSocket protocol modified to support custom AI prompts
- AI service uses local Ollama model

---

*Add learnings as you discover them!*
