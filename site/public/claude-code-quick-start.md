# Claude Code Quick Start — Get More Out of Every Session

> Tips for getting better results from Claude Code (Anthropic's CLI tool). Paste this into your first session, or save it as your CLAUDE.md file.

## What Is Claude Code?

Claude Code is a terminal-based AI coding assistant by Anthropic. It can read your files, edit code, run commands, search the web, and work across your entire project. It's like having a senior developer in your terminal.

**Install:** `npm install -g @anthropic-ai/claude-code`
**Run:** `claude` (in any project directory)
**Docs:** https://docs.anthropic.com/en/docs/claude-code

---

## 1. Give Claude Context (The Single Biggest Improvement)

Claude works best when it understands your project. Create a `CLAUDE.md` file in your project root:

```markdown
# CLAUDE.md

## What This Project Does
[One paragraph explaining your project]

## Tech Stack
[List your languages, frameworks, tools]

## How to Run
[Commands to build, test, run your project]

## Project Structure
[Key directories and what they contain]

## Coding Style
[Any preferences: formatting, naming, patterns]
```

Claude reads this file automatically at the start of every session. Think of it as onboarding docs for your AI pair programmer.

**Pro tip:** Add a `CLAUDE.md` in subdirectories too for context-specific guidance (e.g., `api/CLAUDE.md` for backend-specific rules).

---

## 2. Use Slash Commands

| Command | What it does |
|---------|-------------|
| `/help` | Show all available commands |
| `/compact` | Compress conversation to free up context space |
| `/clear` | Start fresh (keeps CLAUDE.md context) |
| `/model` | Switch between models (Opus, Sonnet, Haiku) |
| `/cost` | Show token usage for this session |

---

## 3. Memory Across Sessions

Claude Code doesn't remember between sessions by default. To build continuity:

**Option A — Simple (CLAUDE.md notes)**
Add a "Current Status" section to your CLAUDE.md that you update:
```markdown
## Current Status
- Working on: user authentication
- Last completed: database schema
- Known issues: login redirect broken on Safari
```

**Option B — Memory directory**
Create a `.agent/memory/` folder in your project:
```
.agent/memory/
  decisions.md    — Why you chose X over Y
  learnings.md    — What works, what doesn't
  inbox.md        — Quick notes between sessions
```

Add to your CLAUDE.md:
```markdown
## Memory
On session start, read `.agent/memory/` for context from previous sessions.
Before ending, save important decisions to `.agent/memory/decisions.md`.
```

---

## 4. Save Tokens (Get More Done Per Session)

Claude Code has usage limits. Here's how to stretch them:

- **Be specific.** "Fix the login bug in auth.ts line 42" beats "something's broken with login"
- **Use `/compact` at ~50% context.** Keeps the conversation going without losing too much history
- **Use `/clear` between unrelated tasks.** Fresh context = better results
- **Let Claude use subagents.** It can spawn lighter models (Haiku) for research tasks automatically
- **Don't re-explain.** If it's in CLAUDE.md, Claude already knows it

---

## 5. Let Claude Work Autonomously

Claude Code can chain multiple steps without asking you. To enable this:

```markdown
## Autonomy Rules (add to CLAUDE.md)
- Run builds and tests without asking
- Fix lint errors automatically
- Read any file in the project
- Only ask before: deleting files, pushing to git, installing packages
```

This prevents the constant "Should I proceed?" prompts and lets Claude flow.

---

## 6. Useful Patterns

### "Explore first, then act"
```
Read the auth module and understand how login works before making any changes.
Then fix the session timeout bug.
```

### "Check your work"
```
After making changes, run the tests and fix anything that breaks.
```

### "Learn from the codebase"
```
Look at how the other API endpoints are structured.
Follow the same pattern for the new /users endpoint.
```

### "Context dump"
```
Here's the error I'm seeing: [paste error]
Here's what I've tried: [list attempts]
The relevant file is src/auth/login.ts
```

---

## 7. CLAUDE.md Template (Copy This)

```markdown
# CLAUDE.md

## About
[Project name] — [one-line description]

## Tech Stack
- Language: [e.g., TypeScript]
- Framework: [e.g., React 19, Next.js 15]
- Styling: [e.g., Tailwind CSS]
- Database: [e.g., PostgreSQL via Prisma]
- Testing: [e.g., Vitest]

## Commands
- `npm run dev` — start dev server
- `npm test` — run tests
- `npm run build` — production build
- `npm run lint` — check linting

## Project Structure
- `src/` — application source
- `src/components/` — React components
- `src/api/` — API routes
- `tests/` — test files

## Conventions
- Use TypeScript strict mode
- Prefer named exports
- Components in PascalCase, utilities in camelCase
- Write tests for new features

## Current Status
- Working on: [current task]
- Last completed: [recent milestone]
- Blocked by: [any blockers]

## Memory
On session start, read `.agent/memory/` for previous session context.
Save important decisions and learnings before session ends.
```

---

## 8. Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Escape` | Cancel current generation |
| `Ctrl+C` | Exit Claude Code |
| `Up arrow` | Recall previous message |
| `Tab` | Accept autocomplete suggestion |

---

## 9. Skills (Power User)

Claude Code supports installable skills — pre-written prompts for common tasks:

```bash
# Install a skill pack
npx skills add anthropics/skills -y

# Use a skill
/commit          # Smart git commit
/review-pr 123   # Review a pull request
```

Browse available skills at https://skills.sh

---

## 10. One More Thing

Claude Code gets better the more context you give it. The CLAUDE.md file is the single highest-impact thing you can do. Even a 10-line version makes a huge difference compared to starting from zero every session.

Start simple. Add to it as you go. Your future self will thank you.

---

*From the Dreams to Reality project — https://dreamstoreality.app*
*Claude Code by Anthropic — https://claude.ai/code*
