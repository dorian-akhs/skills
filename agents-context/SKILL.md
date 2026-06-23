---
name: agents-context
description: >
  Creates and maintains AI agent context files (AGENTS.md and companion docs) for any project.
  These files inject scoped instructions into the agent's context window — only what's needed per task.
  Use this skill whenever the user wants to:
  - Set up AGENTS.md for a project (new or existing)
  - Add a gotcha, anti-pattern, or prohibition to existing agent docs
  - Update guidelines for a specific domain (frontend, backend, tests)
  - Audit or reorganize existing agent context files
  - Ask "what should I put in my AGENTS.md?", "document this project for AI", or "how do I write agent instructions?"
  Trigger when the user says "Claude keeps making this mistake", "add this to my agent context",
  "help AI understand this codebase", or anything about writing/updating AI instructions for a project.
---

## Core idea

Agent context files solve a context-window problem: if you put everything in one file, agents load
irrelevant info on every task. Split by concern, agents get only what they need.

The root AGENTS.md is the entry point — short, with pointers to deeper files. Domain-specific docs
live in `docs/`. Subdirectory AGENTS.md files load only when the agent works in that directory.

## File hierarchy

```
/AGENTS.md                        ← entry point: tech stack, commands, links to docs/
/docs/
  architecture.md                 ← folder structure, module boundaries, import rules
  global-guidelines.md            ← shared rules across the whole codebase
  frontend-guidelines.md          ← React/Vue/etc patterns, component conventions, state
  backend-guidelines.md           ← HTTP routes, API error format, auth patterns
  gotchas.md                      ← known bugs, anti-patterns, mistakes to avoid
/tests/AGENTS.md                  ← test file naming, what to mock, coverage expectations
```

For monorepos: root AGENTS.md holds shared rules + index only. Each package gets its own AGENTS.md
and docs/ if it diverges enough to warrant separate instructions.

Only create files that have real content — skip frontend-guidelines.md on a pure API project,
skip backend-guidelines.md on a React SPA.

## docs/ placement

Default to `docs/`. If the project already uses `docs/` for user-facing or API docs, check for
conflict and suggest `.claude/docs/` or ask the user where to put agent-specific files.

## Size targets

| File | Target |
|------|--------|
| Root AGENTS.md | < 100 lines |
| docs/architecture.md | free-form |
| docs/frontend-guidelines.md | < 150 lines |
| docs/backend-guidelines.md | < 150 lines |
| docs/global-guidelines.md | < 100 lines |
| docs/gotchas.md | append-only, no limit |
| tests/AGENTS.md | < 60 lines |

If a file grows beyond its target, split it rather than compress.

## What goes where

**Root AGENTS.md**
- Tech stack (language, framework versions, key libraries)
- How to run the project (`dev`, `build`, `test`, `lint` commands)
- Links to docs/ files with one-line descriptions of each
- DO NOT duplicate README.md — content extracted from README goes into the relevant docs/ file

**docs/architecture.md**
- Folder structure with purpose of each major directory
- Module boundaries and import rules ("never import from `app/` into `lib/`")
- Key data flow or request lifecycle

**docs/global-guidelines.md**
- Naming conventions (files, variables, types)
- Error handling patterns
- TypeScript/lint config implications
- Patterns that apply everywhere

**docs/frontend-guidelines.md**
- Component file structure and naming
- State management patterns (when to use local state vs. global)
- Styling approach
- Data fetching conventions

**docs/backend-guidelines.md**
- HTTP route naming and structure
- API response format (success and error shapes)
- Auth middleware patterns
- Database access patterns

**docs/gotchas.md**
- Known bugs or footguns in the codebase
- Anti-patterns the AI has gotten wrong repeatedly
- Third-party library quirks specific to this project
- Format: heading + at least one explicit `do NOT` line. Free prose for context.

**tests/AGENTS.md**
- Test file naming convention
- What to mock vs. what to hit for real
- Coverage expectations
- Test data / fixtures location

## The most effective instruction pattern

Prohibitions outperform vague positives. Prefer:

```
do NOT mock the database in integration tests — we use a real test DB via docker-compose
do NOT use `any` type — use `unknown` and narrow explicitly
do NOT import barrel files from `ui/` in `server/` — this pulls in browser globals
```

Over:
```
write clean code
keep tests realistic
manage types carefully
```

When something keeps going wrong, add it to `docs/gotchas.md` as a prohibition.

## Workflow

### Mode A: Initial setup (no existing context files)

**1. Gather context**

Check for available context-gathering tools or MCPs (e.g. a codebase graph MCP). If available,
use them. If not, fall back to:
- Read package.json / pyproject.toml / go.mod
- Read top-level directory listing
- Read README.md — extract any conventions, patterns, or rules relevant to agents into the
  appropriate docs/ files. Don't just point to README; mine it for content.
- Spot-check 2-3 key files (entry point, one route, one component) to infer patterns in use

**2. Infer, confirm, ask**

From what was observed, extract conventions (naming, error shapes, import patterns, etc.) and
confirm them with the user before writing: "I see all routes return `{ data, error }` — documenting this?"

Then ask only what the scan couldn't answer — 3-5 questions max, focused on:
- Module boundary rules (what can't import what)
- Known anti-patterns to document now
- Anything non-obvious about the structure

Do NOT ask about things that don't exist yet in the codebase.

**3. Preview then write**

Show a summary of what will be generated (file names + 1-line description of content). Wait for
confirmation, then create all files.

### Mode B: Maintenance (existing context files)

Infer the intent from the user's message:
- "Claude keeps doing X" → add to `docs/gotchas.md`
- "Update the API conventions" → edit the relevant guidelines file
- "Reorganize / it's gotten too big" → audit mode (see below)

State what you're about to do in one line, get a quick confirmation, then write.

For gotcha additions: append under a new heading with at least one `do NOT` line. Never edit
existing entries during a normal maintenance add.

### Mode C: Audit / reorganize

Triggered explicitly by the user ("audit my context files", "reorganize", "it's gotten messy").

Steps:
1. Read all existing context files
2. Check for: oversize files (suggest splits), duplicated content across files, missing files
   that should exist based on observed codebase patterns
3. Check for potentially stale gotchas — if code contradicts a documented prohibition,
   flag it: "This gotcha may be outdated — the code no longer does X. Remove?"
4. Propose changes, get confirmation, then apply

Never surface staleness outside of audit mode.

## Dos and don'ts for the generated files

**Do:**
- Use imperative, direct instructions: "use", "do NOT", "always", "never"
- Explain the *why* for non-obvious rules — agents follow reasoning, not mandates
- Cross-reference between files: "see docs/backend-guidelines.md for API error shapes"
- Keep each file focused on its domain

**Do NOT:**
- Repeat information across files
- Describe what the README already explains — extract from it instead
- Write long prose — bullets and short paragraphs load faster and stick better
- Document conventions that don't exist yet in the codebase
