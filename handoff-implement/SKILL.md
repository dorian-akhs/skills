---
name: handoff-implement
description: Creates or executes an implementation-grade handoff brief for a less capable model agent. Activated explicitly via /handoff-implement.
---

# Handoff Implement

## Mode Detection

Check if `HANDOFF-IMPLEMENT.md` exists in the working directory:

- **Not found** → Create mode: generate an implementation brief from current conversation context
- **Found** → Execute mode: read it and begin implementing

---

## Create Mode

Build `HANDOFF-IMPLEMENT.md` from the current conversation context. If `HANDOFF.md` exists, use it as supplemental context only — conversation context takes priority.

Write the file with these sections, in order:

### 1. Goal
One paragraph. What needs to be built and why. No ambiguity.

### 2. Files to Touch
Explicit list of every file that needs to be created or modified. Full paths. For each file, one line describing what changes.

### 3. Step-by-Step Tasks
Numbered list. Each task must be:
- Atomic (one clear action)
- Ordered by dependency (earlier tasks unblock later ones)
- Specific enough that a model with no prior context can execute it without asking questions

### 4. Commands to Run
Exact shell commands needed: install, build, test, lint. Copy-pasteable strings only.

### 5. Acceptance Criteria
Checklist. Each item is a verifiable condition that confirms the task is complete.

### 6. Constraints & Traps
Bullet list of what NOT to do, known pitfalls, non-obvious invariants, and decisions already made that must not be revisited.

After writing `HANDOFF-IMPLEMENT.md`, **stop immediately**. Do not begin implementing. Tell the user the file is ready.

---

## Execute Mode

1. Read `HANDOFF-IMPLEMENT.md` silently
2. Tell the user: "Found implementation brief: [title from Goal section]. [1-sentence summary of what will be built]. Ready to start?"
3. If confirmed, work through the Step-by-Step Tasks in order
4. Check off acceptance criteria as tasks complete
5. When all tasks are done and all acceptance criteria pass, delete `HANDOFF-IMPLEMENT.md`, then stop
