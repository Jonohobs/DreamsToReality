# 💡 Learnings

> What's worked, what hasn't, and insights gained. Prevents repeating mistakes.

---

## AI/Agent Patterns

### What Works ✅
- **Ask AI to build, then explain** — "Ask the robot to build something for you, then ask how the code works. You'll be coding in no time."
- **Opus Audit pattern** — Use cheaper models for drafting, Opus for review/reasoning
- **Writing to MD files** — Simple, version-controlled, readable memory
- **Human in the loop** — Keep humans involved for critical decisions

### What Doesn't Work ❌
- **Video editing** — "Editing not solved" (noted in research)
- **Direct cloud access** — Google Drive/iCloud require OAuth setup or MCP
- **Antigravity browser** — Currently has $HOME env var issue on this machine

---

## Tools & Services

| Tool | Verdict | Notes |
|------|---------|-------|
| OpenClaw | ✅ Works | Multi-model routing, good TUI |
| Ollama | ✅ Works | Local, private, free |
| Antigravity | ✅ Works | Good for coding, browser broken |
| Make.com | 🔍 Explore | Automation platform |
| Zapier | 🔍 Explore | More expensive, delays |
| n8n | 🔍 Explore | Self-hostable alternative |
| Meshroom | 🔍 Testing | Photogrammetry for Dreams |
| FFMPEG | 🔍 Explore | CLI media processing |

---

## Project-Specific

### Dreams to Reality
- SDF rendering in Dreams ≠ traditional polygons — complicates photogrammetry
- Post-processing effects (bloom, DoF) confuse feature matching
- May need NeRF approach for better results

### Improv Game
- WebSocket protocol modified to support custom AI prompts
- AI service uses local Ollama model

---

*Add learnings as you discover them!*
