---
name: feature-loop
description: Implement a feature with independent review and bounded repair passes.
disable-model-invocation: true
---

# Feature Loop

Act as coordinator. The user's invocation authorizes initial implementation and
the scoped repairs in this workflow. Preserve the user's delivery permissions;
commits, pushes, and deployment require their own authorization.

1. Read [loop setup](../thermo-nuclear-code-quality-review/references/loop-setup.md).
   Establish or resume a run with `mode: FEATURE` and reconcile context until
   `CONTEXT_READY`. Resolve material questions before implementation.
2. Spawn an implementer with the project root, applicable project instructions,
   `context.md`, `requirements.md`, `decisions.md`, fixed baseline, existing-work
   boundaries, and relevant source references. Supply context for an agent with
   no conversation history. Require the feature implementation, appropriate
   checks, changed files, actual command outcomes, unmet criteria, limitations,
   and important decisions with their rationale. The worker returns to the
   coordinator without launching another review loop.
3. Wait for all writers, inspect their changes, and persist the implementation
   evidence. Then read and follow the shared
   [review and repair workflow](../thermo-nuclear-code-quality-review/references/loop-review.md)
   through its completion or stopping condition.

The shared references ship with `thermo-nuclear-code-quality-review`; install or
sync that package alongside this skill. Reading its plain references does not
invoke its user-only skill. Project instructions supply tracker, domain,
worktree, validation, and delivery conventions.
