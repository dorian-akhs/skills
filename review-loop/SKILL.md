---
name: review-loop
description: Review existing work and repair substantiated findings within a bounded loop.
disable-model-invocation: true
---

# Review Loop

Act as coordinator. The user's invocation authorizes independent review and the
scoped repairs in this workflow. Preserve the user's delivery permissions;
commits, pushes, and deployment require their own authorization.

Example: `$review-loop Review <branch/change set/files/task reference>`.

1. Read [loop setup](../thermo-nuclear-code-quality-review/references/loop-setup.md).
   Establish or resume a run with `mode: REVIEW` and reconcile context until
   `CONTEXT_READY`. Identify the intended behavior of the existing work rather
   than inventing a new implementation task.
2. Record the existing work, scoped paths, accumulated changes, observed behavior,
   and available verification evidence. Label missing or stale checks explicitly.
   Preparation is read-only for application code; the first Matt review examines
   the existing implementation before any repair worker starts.
3. Read and follow the shared
   [review and repair workflow](../thermo-nuclear-code-quality-review/references/loop-review.md)
   through its completion or stopping condition. A clean run needs no implementer.

The shared references ship with `thermo-nuclear-code-quality-review`; install or
sync that package alongside this skill. Reading its plain references does not
invoke its user-only skill. Project instructions supply tracker, domain,
worktree, validation, and delivery conventions.
