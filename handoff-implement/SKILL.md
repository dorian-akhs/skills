---
name: handoff-implement
description: Creates or executes an implementation-grade handoff brief for a less capable model agent, including a measured context budget and a binding sub-agent orchestration plan. Activated explicitly via /handoff-implement.
---

# Handoff Implement

## Mode Detection

Check if `HANDOFF-IMPLEMENT.md` exists in the working directory:

- **Not found** → Create mode: generate an implementation brief from current conversation context
- **Found** → Execute mode: read it and follow its §0 execution plan

---

## Create Mode

Build `HANDOFF-IMPLEMENT.md` from the current conversation context. If `HANDOFF.md` exists, use it as supplemental context only — conversation context takes priority.

The brief is read by agents that start cold. Every section must survive being read with no memory of this conversation.

### Measure before you plan

Do this before writing anything. It decides the shape of the whole brief.

1. Size every file in the touch list: `wc -cl <files>`. Estimate tokens as **bytes ÷ 3.6**.
2. Sum them — that is the **reading surface**. Note separately any single file above **~15k tokens** (~55 KB): those must never be read whole.
3. For each such file, locate the regions the work actually touches (`grep -n` for the symbols) and record line anchors.
4. Group tasks into **tracks by file ownership, not by topic**. A track is the set of tasks that write the same files. Two tracks that write the same file belong in different waves — or the boundary is wrong.

### Choose the execution shape

- Reading surface under ~25k tokens and ≤3 files touched → **one agent, no orchestration**. Say so explicitly in §0. Do not invent waves for small jobs.
- Otherwise → **waves**. Tracks with disjoint ownership run in parallel in the same wave. A track that deletes from, renames, or depends on the final API of another runs in a later wave. Put the largest, most cross-cutting track **last and alone**.
- Keep each agent's read set under roughly 40% of its window, leaving room for edits, test output, and iteration. If a track can't fit, split it and sequence the halves.

### Sections, in order

**§0. How to run this brief — binding**
The execution plan, first thing an executing agent reads. State whether it implements directly or acts as orchestrator; the wave order; that it verifies with real commands between waves; and what it must relay to the user at the end. Include the per-agent prompt contract (below) and a solo fallback if sub-agents are unavailable or declined.

**§1. Goal**
One paragraph. What needs to be built and why. No ambiguity.

**§2. Files to Touch**
Every file created or modified, full paths, one line each describing the change. For any file too large to read whole, add its line anchors plus a "re-grep before editing, line numbers shift" caveat.

**§3. Step-by-Step Tasks**
Numbered, grouped by track. Each task atomic, ordered by dependency, and specific enough to execute with no prior context. Record decisions the user already made as decided — name them as such so no agent reopens them.

**§4. Commands to Run**
Exact copy-pasteable strings: install, build, test, lint, typecheck. Separate the cheap per-track loop from the slow full gate, and name anything expensive that must *not* be run.

**§5. Acceptance Criteria**
Checklist of verifiable conditions, each with the command or grep that proves it. Mark any criterion that no command can verify (a judgement call, a manual UI check, something to relay to the user) as such — those are the ones that get silently skipped.

**§6. Constraints & Traps**
What NOT to do, known pitfalls, non-obvious invariants, out-of-scope neighbours, and decisions that must not be revisited. Include commit/PR conventions if the work will be committed.

**§7. Agent split and context budget**
A table per wave: agent label, track, **files owned exclusively**, what to read, estimated context. State the reading surface and the per-file token estimates you measured, so the executor can sanity-check its own budget. Explain in one line why each sequenced track cannot run in parallel.

### Per-agent prompt contract

§0 must require that every dispatched agent is told to:

- read only §0, §4, §6, its own track in §3, and its own row in §7;
- treat its §7 file list as exclusive — editing another track's file is a bug to report, not fix;
- never read an oversized file whole: `grep -n` for the symbol, then `sed -n '<start>,<end>p'`;
- run the per-track commands from §4 on its own files and paste the results, not a claim;
- report what it changed, what it deliberately did not, and anything it could not do.

Also require that agents share one working tree (ownership is disjoint by design, so isolation would only create merges), unless the brief says otherwise.

After writing `HANDOFF-IMPLEMENT.md`, **stop immediately**. Do not begin implementing. Tell the user the file is ready, and summarise the execution shape you chose — waves, agent count, and measured context per agent — so they can adjust before anything runs.

---

## Execute Mode

1. Read `HANDOFF-IMPLEMENT.md` silently.
2. Tell the user: "Found implementation brief: [title from Goal section]. [1-sentence summary]. [Execution shape from §0 — solo, or N agents across M waves]. Ready to start?"
3. If confirmed, follow **§0** — it overrides the default of working through §3 yourself.
4. Between waves, verify with the §4 commands yourself. A green agent plus a green agent is not a green tree. Commit per track if the brief says to.
5. Check off acceptance criteria with commands, never from an agent's claim. Relay every criterion §5 marks as unverifiable-by-command to the user.
6. When all tasks are done and all acceptance criteria pass, delete `HANDOFF-IMPLEMENT.md`, then stop. If anything remains, leave the file in place and say exactly what.
