# 📋 Decision Log

> Key decisions made across projects. Helps maintain consistency across sessions.

---

## 2026-02-03

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

---

## Template for New Decisions

```markdown
### [Decision Title]
- **Decision**: What was decided
- **Why**: Reasoning
- **Alternatives considered**: What else was on the table
- **Outcome**: Result/status
```
