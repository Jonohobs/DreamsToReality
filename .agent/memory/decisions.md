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

---

## Template for New Decisions

```markdown
### [Decision Title]
- **Decision**: What was decided
- **Why**: Reasoning
- **Alternatives considered**: What else was on the table
- **Outcome**: Result/status
```
