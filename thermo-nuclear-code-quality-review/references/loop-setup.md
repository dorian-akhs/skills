# Loop setup

Shared preparation for `feature-loop` (`FEATURE`) and `review-loop` (`REVIEW`).
The coordinator owns requirements, evidence, decisions, dispatch, and counters.

## Runtime and dependencies

Use the harness's available worker tools. Independent review requires separate
agents; if unavailable, stop with `SETUP_BLOCKED` and name the missing capability.
Keep writers and reviewers in separate phases. Parallel repair tracks may write
disjoint files; finish every writer before reviewing the combined tree. Account
for worker capacity before a Matt reviewer dispatches its two axis reviewers.

Locate dependencies through the session skill catalog, preferring the project's
Matt Pocock `code-review` adaptation. If absent, search sibling skill directories
and configured skill locations. Record actual absolute paths. Check availability
upfront, but read bodies at their execution stage:

- `code-review`: must provide separate Standards and Spec reviews. Read its
  instructions before the first Matt dispatch and pass the resolved path to it.
- [Structural review standards](structural-standards.md): plain reference for the
  final reviewer; read at the final phase. The enclosing user-only skill is not
  invoked by either loop.
- `handoff-implement`: needed only when repairs require a brief. Locate and read
  it at that branch; a clean review may finish without this dependency installed.

Honor dependency invocation policies. Model-available supporting skills may be
delegated; a user-only dependency requires a callable plain reference or separate
explicit user authorization. Stop with `SETUP_BLOCKED` if a required dependency
or permitted entry point is missing. Name it and the searched locations rather
than substituting a generic review or handoff. Project and user instructions take
precedence over dependency defaults.

## Establish or resume the run

On resumption, read the existing `state.md`, requirements, context, decisions, and
artifacts first. Resume its recorded phase and collect any in-flight results.
Preserve consumed counters and flags; create a new run only for a new task.

For a new run:

1. Record the project root, mode, user request, applicable project instructions,
   supplied issue/document references, accepted decisions, and explicit exclusions.
   Follow the project's own worktree and delivery conventions.
2. Record scope and a fixed baseline. Resolve a user-supplied base to a commit SHA;
   otherwise use the merge base with the identifiable target branch. If no target
   is identifiable, record starting HEAD and disclose what that excludes. In
   `REVIEW` mode, resolve an ambiguous committed-change scope with the user before
   proceeding. For a named branch, identify its checkout and ensure the reviewed
   files correspond to that branch before repairs. Current files/modules are a
   valid explicit scope even with an empty diff. Non-Git work uses scoped files
   and before-edit snapshots.
3. Inventory relevant committed, staged, unstaged, and untracked changes before
   edits. Include existing task-owned work and preserve unrelated user changes.
   Record included and excluded paths; avoid resets or stashes that hide user work.
4. Create a unique `<project-root>/.agent-work/<skill-name>/<run-id>/` directory.
   Exclude run artifacts from application changes and review inputs. Preserve
   existing runs and unrelated handoff briefs.
5. Initialize `state.md` with `mode`, `phase`, scope, baseline SHA or snapshot,
   starting HEAD, dependency paths, worker assignments, artifact paths,
   `reviews_used: 0`, `max_reviews: 3`, `final_review_used: false`, and
   `final_repair_used: false`. Store numbered criteria in `requirements.md`.
   Maintain `decisions.md` with IDs, rationale, owner, and status (`DECIDED`,
   `PROPOSED`, or `NEEDS_USER_INPUT`). Persist state before dispatch and after
   every result.

## Reconcile context

Read and follow [loop context](loop-context.md). Set `CONTEXT_READY` only when its
checklist passes. Tell the user which sources informed the work, its scope and
baseline, and material assumptions before the first implementation or review
dispatch. This update is not a routine approval gate.

Preparation is complete when scope, baseline, existing-work boundaries, sourced
requirements, verification plan, decisions, and passing readiness evidence are
persisted. Context gathering consumes no review round.
