---
name: review-loop
description: Review existing work and repair substantiated findings within a bounded loop.
disable-model-invocation: true
---

# Review Loop

Act as coordinator. The user's invocation authorizes independent review and the
scoped repairs in this workflow. The invocation also authorizes
scoped commits, pushes, and PR creation or updates on a dedicated task branch,
unless the user explicitly limits delivery. Merging and deployment require separate authorization.

Example: `$review-loop Review <branch/change set/files/task reference>`.

1. Read [loop setup](../thermo-nuclear-code-quality-review/references/loop-setup.md).
   Establish or resume a run with `mode: REVIEW` and reconcile context until
   `CONTEXT_READY`. Identify the intended behavior of the existing work rather
   than inventing a new implementation task. Select the delivery branch using
   [loop delivery](../thermo-nuclear-code-quality-review/references/loop-delivery.md)
   before dispatching workers.
2. Record the existing work, scoped paths, accumulated changes, observed behavior,
   and available verification evidence. Label missing or stale checks explicitly.
   Preparation is read-only for application code; the first Matt review examines
   the existing implementation before any repair worker starts.
3. Read and follow the shared
   [review and repair workflow](../thermo-nuclear-code-quality-review/references/loop-review.md)
   through its completion or stopping condition. A clean run needs no implementer.
4. After `SUCCESS`, complete [loop delivery](../thermo-nuclear-code-quality-review/references/loop-delivery.md):
   commit scoped changes, push the task branch, and create or update its PR.
   Report review acceptance and PR delivery separately.

## Model routing

When the harness supports cross-provider agents, route workers as follows:

| Role | Model | Effort |
| --- | --- | --- |
| Matt reviewer and its Standards and Spec children | GPT Sol (`gpt-6.1-sol`) | high |
| Final structural reviewer | Claude Opus 5.5 (`claude-opus-5-5`) | high |
| Repair handoff writer and repair executor | GPT Sol (`gpt-6.1-sol`) | high |

Before the first dispatch, check the harness's provider, model, and effort
capabilities. In T3 Code, use `orchestrator_capabilities`, then `delegate_task`
with `target.providerInstanceId`, `target.model`, the matching `role`, and
`target.options` (`effort: "high"` for Claude or `reasoningEffort: "high"` for
Codex). If a required provider or model is unavailable, report the blocker;
request a routing decision before substituting another model.

Use `isolation: "shared"` in the integration checkout for review, handoff, and
repair workers so they see scoped uncommitted changes. Finish every writer
before reviewing the combined tree. Keep reviewers independent from repair
workers; the Matt reviewer's two axis children use Sol high too. Context
research stays on the coordinator's default. Record resolved provider, model,
and effort assignments in `state.md`; routing preserves the shared workflow's
review budget and stopping conditions.

The shared references ship with `thermo-nuclear-code-quality-review`; install or
sync that package alongside this skill. Reading its plain references does not
invoke its user-only skill. Project instructions supply tracker, domain,
worktree, validation, and delivery conventions.
