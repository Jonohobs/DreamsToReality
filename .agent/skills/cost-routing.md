# 💰 Cost-Based Model Routing

> Use the right model for the right task. Save money on simple stuff, splurge on complex reasoning.

---

## Model Tiers

### Tier 1: Complex Reasoning ($$$$)
**Use for**: Architecture decisions, debugging subtle bugs, code review, planning
- Claude Opus / Claude 3.5 Sonnet
- GPT-4o
- Gemini Ultra

### Tier 2: Standard Coding ($$$)
**Use for**: Feature implementation, refactoring, documentation
- Claude Sonnet
- GPT-4o-mini
- Gemini Pro

### Tier 3: Fast & Cheap ($$)
**Use for**: Quick questions, formatting, simple generation
- Groq (Llama 3) — extremely fast
- DeepSeek — very cheap, good quality
- Fireworks AI

### Tier 4: Free/Local ($)
**Use for**: Sensitive data, high volume, experimentation
- Ollama (local Llama)
- Self-hosted models

---

## The Opus Audit Pattern

```
1. Draft with Sonnet (cheaper, faster)
2. Review with Opus (catches subtle issues)
3. Ship with confidence
```

This is what we're doing right now — Sonnet for implementation, Opus for critical review.

---

## OpenClaw Cost Reference

From your configured providers:
| Model | Context | Cost (in/out) |
|-------|---------|---------------|
| DeepSeek V3 | 128K | $0.90/$0.90 |
| DeepSeek R1 | 128K | $0.90/$8.00 |
| Llama 3.1 70B | 131K | $0.90/$0.90 |
| Llama 3.1 8B | 131K | $0.20/$0.20 |
| Qwen 2.5 72B | 32K | $0.90/$0.90 |
| Mixtral 8x22B | 65K | $1.20/$1.20 |
| Sonar Pro | 200K | $3.00/$15.00 |

---

## Quick Decision Matrix

| Task Type | Recommended | Why |
|-----------|-------------|-----|
| "Help me understand X" | DeepSeek/Llama | Fast, cheap |
| "Write this function" | Sonnet | Good balance |
| "Review my architecture" | Opus | Catches subtleties |
| "Process 1000 items" | Local Ollama | Free, parallel |
| "Sensitive company code" | Local Ollama | Private |
