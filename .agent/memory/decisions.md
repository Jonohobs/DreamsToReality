# 📋 Decision Log

> Key decisions made across projects. Helps maintain consistency across sessions.

---

## 2026-02-06

### Infrastructure Maintenance Mode
- **Decision**: Shift focus to infrastructure maintenance when system performance degrades.
- **Why**: Antigravity UI freezing and model selector issues made complex coding tasks (like photogrammetry pipeline) inefficient.
- **Action**: Verified agent memory integrity, deprioritized heavy compute tasks.
- **Outcome**: Switched to "clean up" mode to prepare for a fresh start.

## 2026-02-03 [-- Previous entries preserved below --]

### AI Infrastructure Setup
- **Decision**: Implement memory system using markdown files in `.agent/memory/`
- **Why**: Persistent context across sessions, readable by any agent, version controlled
- **Alternatives considered**: Database, JSON files, external service
- **Outcome**: Pending

### OpenClaw Provider Strategy
- **Decision**: Start with Anthropic, add Ollama (local), Groq (fast), DeepSeek (cheap)
- **Why**: Balance of quality, speed, cost, and privacy
- **Outcome**: Anthropic configured, others pending

### Sci-Fi Writing Repo Created
- **Decision**: Create `scifi-writing/` repo for creative writing projects
- **Why**: Capture ideas from conversations (like "THE HIDDEN PROMPT" concept)
- **Location**: `dreams-to-reality/scifi-writing/` with own git history
- **Outcome**: Created, needs GitHub remote setup

### AI Agent Security Posture
- **Decision**: 75% convenience / 25% security approach
- **Why**: Perfect security is unusable; VM sandbox + common sense is "good enough"
- **Key practices**: VM isolation, no sensitive data in VM, snapshot for recovery
- **Outcome**: Documented, accepted tradeoff

### Claude Code Offloading (Exploration)
- **Decision**: Explore using Claude Code CLI to offload tasks from main conversation
- **Why**: Could save tokens by passing focused context to fresh Claude instance
- **Status**: Tested, works via `npx @anthropic-ai/claude-code --print "task"`
- **Outcome**: Promising, needs more experimentation

### Multi-Location Save Strategy (Proposed)
- **Decision**: Save to 4 locations: project git, GitHub, Claude brain folder, brain git repo
- **Why**: Redundancy, cross-session memory, general vs project-specific knowledge
- **Status**: Discussed, not yet implemented
- **Outcome**: Pending - user tired, revisit later

### Dreams Reconstruction Source
- **Decision**: Switch from local 360p video to 1080p YouTube source
- **Why**: Dreams rendering is detail-depdendent; 360p lacked feature resolution for COLMAP.
- **Trade-off**: 9x processing time for ~10x point density.
- **Outcome**: Success. 110k points vs 11k points.
- **Next Step**: Attempt Luma AI (NeRF/Gaussian Splatting) to see if it handles "soft" geometry better than photogrammetry.

### 2026-02-05: Memory Management Protocol
- **Problem**: User concerned about losing context/tools in long chats vs. performance overhead of large contexts.
- **Decision**: Adopt a "Save as we go" protocol.
- **Action**: Agent will proactively ask "Should we save this to learnings.md?" when a useful pattern or tool is discovered.
- **Benefit**: Keeps active context light while preserving long-term knowledge in `.agent/memory/`.

---

## Template for New Decisions

```markdown
### [Decision Title]
- **Decision**: What was decided
- **Why**: Reasoning
- **Alternatives considered**: What else was on the table
- **Outcome**: Result/status
```
