---
name: feature-loop
description: Gather task-tracker and knowledge-base context, then coordinate feature implementation with separate agents, thermo-nuclear-code-quality-review, and handoff-implement briefs for fixes. Use when asked for an implement-review-fix loop, stopping when requirements pass and no blocking findings remain, with at most three reviews.
---

# Feature Loop

Act as coordinator. Delegate implementation and independent review; keep requirements, evidence, handoffs, and the review counter in durable files. Use the installed `thermo-nuclear-code-quality-review` and `handoff-implement` instructions, rather than reproducing their contents here.

## Authorization and dependencies

Invoking this workflow authorizes the initial implementation and the corrective implementation passes described below within the requested feature scope. Do not ask for routine confirmation between these stages. Ask for user input when a material decision cannot be resolved from the agreed requirements and constraints. This does not authorize commits, pushes, deployments, unrelated refactors, or bypassing runtime permissions.

Resolve both dependencies from the session skill catalog. If absent, search sibling skill directories and the agent's configured skill locations. Read the resolved `SKILL.md` files and give their actual absolute paths to the workers. Never hardcode another machine's home directory. If a dependency is missing, stop with its name and expected location; do not substitute a generic review or handoff.

Use the harness's available spawn, message, wait, and close tools. ACP connects the editor to the harness; this skill does not create agent tools. If separate worker agents are unavailable, stop with `SETUP_BLOCKED` and explain that the runtime needs subagent support. Do not silently replace independent review with self-review.

### Handoff stage boundaries

The handoff dependency normally stops after writing a brief and requests confirmation before executing it. In this explicitly authorized coordinator workflow:

- The handoff writer runs Create mode only and returns as soon as its brief is ready. It never implements.
- The coordinator dispatches a separate implementer with the brief and explicitly states that execution is already authorized. The implementer follows Execute mode and §0 without another confirmation question.
- These stage stops end the worker's assignment, not the coordinator's loop. Ordinary standalone handoff invocations retain their normal behavior.
- Copy a completed brief to `handoff-final.md` in its round directory before execution. The executor may remove its active `HANDOFF-IMPLEMENT.md` only after satisfying the brief, as the dependency requires. Keep the archived brief and unresolved active briefs.

## Establish the task

1. Record the project root, applicable project instructions, feature request, issue/document references, accepted decisions, and explicit exclusions. Gather and reconcile requirements through the context stage below before treating them as ready for implementation.
2. Establish a fixed review baseline: the user-specified base, or the merge base of the feature branch and its identifiable target branch. If no target can be determined, use the starting commit and disclose that scope. Record existing staged, unstaged, and untracked changes before workers edit. Preserve user work; do not reset or stash it. Existing feature edits belong in the review scope; unrelated existing changes remain excluded. For a non-Git project, preserve equivalent before-edit snapshots.
3. Create a unique run directory at `<project-root>/.agent-work/feature-loop/<run-id>/`. Store `requirements.md` and `state.md` there. Keep workflow artifacts out of the feature diff and review. Do not overwrite an existing run or an unrelated `HANDOFF-IMPLEMENT.md`.
4. Record `reviews_used: 0`, `max_reviews: 3`, the baseline, dependency paths, assigned agents, phase, and artifact paths in `state.md`. Maintain `decisions.md` with important choices, their rationale, who made them, and their status (`DECIDED`, `PROPOSED`, or `NEEDS_USER_INPUT`). Update these files before dispatch and after every result. On resumption, read them and the artifacts; never reset the counter or start another run to evade the limit. Manual acceptance checks that remain unverified prevent success.

## Gather context before implementation

Before dispatching any implementation worker, read and follow [references/context-gathering.md](references/context-gathering.md). Identify the project's known task tracker and knowledge base from the conversation, project instructions, documentation, referenced links, and available integrations. Read relevant task and documentation context through those tools; examples include Linear or Multica, and Notion or Obsidian. Tool availability alone does not identify the correct project or workspace.

Persist sourced findings, access gaps, and the readiness checklist in `context.md`; reconcile the findings into numbered acceptance criteria in `requirements.md` and decisions in `decisions.md`. Set `CONTEXT_READY` only when the checklist passes. If essential information is missing or contradictory, ask a focused question and mark `WAITING_FOR_INPUT` or `BLOCKED_CONTEXT`; continue independent read-only investigation, but do not start implementation. This preparation does not consume any of the three reviews.

Tell the user which sources informed the brief, any material assumptions, and what the feature will cover before dispatching the implementer. This is a progress update, not a routine approval gate. Recheck context after a material requirement change or resumption with potentially stale sources; preserve the review counter.

## Initial implementation

Only after `CONTEXT_READY`, spawn an implementer with the project root, `context.md`, `requirements.md`, `decisions.md`, relevant source links or local paths, baseline, applicable project instructions, and existing-work boundaries. Supply enough sourced context for a cold-start worker rather than assuming it shares the conversation or tracker session. Ask it to implement the feature, run appropriate checks, and return changed files, actual commands with results, unmet criteria, limitations, and important decisions or assumptions with their rationale. It must not launch a review loop itself. The coordinator owns the review count.

Wait for implementation to finish before reviewing. Implementation workers share the project working tree. Do not allow overlapping writers. Do not count an implementation or a handoff as a review.

## Review and repair loop

Run the following sequence, with **three review attempts maximum**, including the first review of the initial implementation. Count a dispatched review even if it fails or returns an incomplete report; do not run a fourth reviewer to recover from a failed attempt.

### 1. Dispatch an independent reviewer

Increment and persist `reviews_used` before dispatch. Spawn a fresh reviewer for that iteration with:

- The explicit instruction to read and apply `$thermo-nuclear-code-quality-review` at its resolved path. This is an explicit delegated invocation even if the dependency disables automatic selection.
- The project root, fixed baseline, requirements, `context.md`, `decisions.md`, relevant source references, current implementation summary, prior review reports, and current verification evidence.
- Authority to inspect the full feature diff, including relevant staged, unstaged, and newly created files, and read surrounding code. The reviewer must verify requirements as well as apply the dependency's maintainability standards.
- A read-only assignment for application code: inspect and propose concrete fixes; never implement them. If supported, use a read-only sandbox. Give the coordinator the report to persist rather than requiring application writes.

Require the reviewer to inspect source and verification evidence directly. A handoff or implementer claim alone is not proof. Review the full accumulated feature change against the same baseline on every iteration, not just the latest fixes. Recheck previous blockers and inspect for regressions introduced by repairs.

Require this report:

```text
Iteration: 1 | 2 | 3
Verdict: PASS | CHANGES_REQUIRED | INCOMPLETE
Requirements:
  - criterion ID: PASS | FAIL | UNVERIFIED; evidence
Blocking findings:
  - stable ID; file/symbol/line; evidence; impact;
    requested remedy; verification; previous-finding status
Nonblocking suggestions:
  - concise, optional improvements
Verification:
  - commands and actual outcomes; checks not performed
Important decisions:
  - decision ID; DECIDED | PROPOSED | NEEDS_USER_INPUT;
    owner; rationale; consequences; related requirement/finding IDs
Questions for the user:
  - decision ID; specific question; options and tradeoffs;
    recommendation; which work depends on the answer
Limitations:
  - missing context, failed tools, unavailable manual checks
```

Apply the review dependency's presumptive blockers and approval bar without downgrading them to hit the iteration limit. Require concrete evidence and an actionable remedy. Preserve finding IDs across rounds. A previously disputed blocker is resolved only when the reviewer accepts a clear justification or verifies a fix. Optional nits alone do not trigger another iteration.

### 2. Evaluate the result

Save the report as `review-<n>.md`. Independently verify that the report covers every acceptance criterion, contains no unresolved blocking findings, and meets the dependency's approval bar. Run the final integration commands on the combined working tree before declaring completion; use existing results only when they demonstrably cover the current tree. If a check exposes a failure, include it in the unresolved requirements and the next handoff.

At the end of **every review**, send the user a concise chat update stating the review number out of three, verdict, outstanding blockers, and important decisions made by the implementer, reviewer, or coordinator. Explain the rationale and practical consequences of material choices, including structural remedies, accepted justifications, and significant tradeoffs. Distinguish decisions already made within scope from proposals awaiting input. If there are no important decisions, say so briefly. Do not leave this information only in artifact files or defer it all to the final response.

Record decisions in `decisions.md` and carry them into subsequent handoffs. Reviewers may recommend remedies and assess justifications; they may not silently change requirements or make unresolved product, API compatibility, data migration, or scope choices for the user. Resolve routine implementation choices from existing requirements and project conventions without asking unnecessary questions.

When a material choice needs the user's input, ask a concrete question with the available options, tradeoffs, and a recommendation. Use the harness's question tool when available, otherwise ask in chat. Mark the dependent work `WAITING_FOR_INPUT` in `state.md`; do not dispatch repairs that assume an answer or declare success while that decision is unresolved. Independent work may continue. If the user has not answered when the turn ends, include the pending question in the final response. Record the answer as a user decision, update the affected criteria and handoff, and resume the same run with its existing review count. Waiting for input does not consume a review. At the three-review limit, user input does not authorize a fourth review or further repairs unless the user explicitly extends the workflow.

If the third review leaves any blockers or unmet requirements, **notify the user immediately in chat**: "Review limit reached (3/3). Blocking issues remain; the feature has not passed review." List the remaining finding/requirement IDs with a short impact description, report any pending user decisions, and explain that a final repair handoff will be retained. Notify and persist `REVIEW_LIMIT_REACHED` before handling pending questions or generating the handoff, so neither waiting for input nor a failed handoff can hide the exhausted review budget. Notify through the current conversation, not email, Slack, or another external service.

Declare `SUCCESS` only when the latest completed review says `PASS`, every requirement is verified, there are no blockers or unresolved required user decisions, and required integration checks pass. An empty, interrupted, contradictory, or incomplete review is not approval. If the reviewer approved the code but verification remains unavailable, report `BLOCKED_VERIFICATION` unless another permitted implementation/review pass can resolve it.

### 3. Generate a repair handoff

For `CHANGES_REQUIRED`, or an actionable unmet criterion discovered during verification, spawn a handoff writer. Give it the original requirements, `context.md`, relevant source references, latest report, outstanding finding IDs, `decisions.md`, accepted decisions, pending questions, actual check results, project root, and scope boundaries. Include the relevant sourced constraints directly in the brief so a cold-start executor does not need to rediscover them. Resolve required user decisions before preparing executable repair tasks. At the review limit, a final handoff may document unresolved choices as explicit prerequisites; do not invent an answer or make those tasks executable before the user decides.

Create a fresh `<run-directory>/handoff-<n>/` with no active `HANDOFF-IMPLEMENT.md`, so the dependency selects Create mode. Tell the writer to use that directory as its working directory and explicitly read `$handoff-implement` at its resolved path. The brief must refer to absolute project paths, and commands must run in the project root rather than the handoff directory.

Require all dependency sections §0–§7, measured file sizes and token estimates, bounded reads for oversized files, file ownership, verification commands, and cold-start context. Measure existing files with `wc -cl`; mark new files as nonexistent with estimated size instead of pretending they were measured. Scope fixes to the feature and justified structural changes necessary to satisfy its review. Put requirement IDs and finding IDs in the tasks and acceptance criteria so an executor can trace every requested repair.

§0 must state that execution is authorized within this workflow, name the round and project root, require the dependency's per-agent prompt contract, and return results to the coordinator without starting another review. Follow the dependency's measured solo-versus-wave decision: small repairs use one implementer, larger repairs use disjoint file ownership and dependency-ordered waves. Waves share the project working tree and verify it between waves. Include the solo fallback for unavailable nested subagents; independent review still belongs to the coordinator.

The writer returns only the brief path, execution shape, context budget, and remaining uncertainties. Archive the generated brief before dispatching an executor. If it cannot produce a usable brief, stop with `BLOCKED_HANDOFF`; do not invent or execute missing instructions. If the review limit was already reached, retain `REVIEW_LIMIT_REACHED` as the primary status and report the handoff failure alongside the remaining blockers.

### 4. Execute or stop at the limit

- If `reviews_used < 3` and no required user decision is pending, dispatch an implementer to execute the generated brief using `$handoff-implement`. Supply its working directory, project root, resolved skill path, and existing authorization. It follows §0, verifies the combined tree between waves, and reports changed files, command results, resolved finding IDs, unmet criteria, important decisions and their rationale, and anything it could not do. Wait for all writers to finish, update state, then return to review step 1.
- If `reviews_used == 3`, retain the final repair brief for the user and stop with `REVIEW_LIMIT_REACHED`. Do not dispatch another implementer or reviewer: edits after the last review would leave an unreviewed final tree. Report the unresolved findings and criteria explicitly.
- If a review fails or is incomplete without actionable code findings, another review attempt is allowed only within the same three-attempt budget and after resolving the missing context/tool issue when possible. Do not manufacture a code-repair task. If meaningful progress is impossible, stop with the concrete blocker.

The maximum successful path is: initial implementation → review 1 → handoff/fixes → review 2 → handoff/fixes → review 3. Stop early whenever the completion gate passes.

## Final response

Persist the final status and evidence paths in `state.md`. Report the outcome, reviews used out of three, implemented behavior, checks and their results, unresolved requirements or blockers, important decisions with their rationale, pending questions for the user, and the final repair brief path when one remains. When the review budget is exhausted with blockers, lead with the explicit review-limit notification and unresolved issues; do not present the feature as complete. State any manual verification still required. Never claim success because the budget expired, a worker said "done," or blockers were relabeled. Retain run artifacts for inspection and resumption.
