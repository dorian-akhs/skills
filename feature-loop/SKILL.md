---
name: feature-loop
description: Implement a feature with independent review and bounded repair passes.
disable-model-invocation: true
---

# Feature Loop

Act as coordinator. The user's invocation authorizes initial implementation and
the scoped repairs in this workflow. The invocation also authorizes
scoped commits, pushes, and PR creation or updates on a dedicated task branch,
unless the user explicitly limits delivery. Merging and deployment require separate authorization.

1. Read [loop setup](../thermo-nuclear-code-quality-review/references/loop-setup.md).
   Establish or resume a run with `mode: FEATURE` and reconcile context until
   `CONTEXT_READY`. Resolve material questions before implementation. Select
   the delivery branch using [loop delivery](../thermo-nuclear-code-quality-review/references/loop-delivery.md)
   before dispatching workers.
2. For a standalone run, spawn an implementer with the project root, applicable
   project instructions, `context.md`, `requirements.md`, `decisions.md`, fixed
   baseline, existing-work boundaries, and relevant source references. Supply context for an agent with
   no conversation history. Require the feature implementation, appropriate
   checks, changed files, actual command outcomes, unmet criteria, limitations,
   and important decisions with their rationale. The worker returns to the
   coordinator without launching another review loop.
3. Wait for all writers, inspect their changes, and persist the implementation
   evidence. Then read and follow the shared
   [review and repair workflow](../thermo-nuclear-code-quality-review/references/loop-review.md)
   through its completion or stopping condition.
4. After `SUCCESS`, complete [loop delivery](../thermo-nuclear-code-quality-review/references/loop-delivery.md):
   commit scoped changes, push the task branch, and create or update its PR.
   Report review acceptance and PR delivery separately.

## Composing with implement-spec

When the user requests `implement-spec using feature-loop`, the parent
`implement-spec` coordinator owns one feature-loop run for the entire supplied
specification. Complete step 1 before ticket implementation; record the parent
specification, all acceptance criteria, integration checkout, fixed baseline,
and existing-work boundaries in that run.

Use `implement-spec`'s ticket graph, isolated implementers, and integration
workflow in place of step 2. Pass each child its ticket scope and an explicit
assignment to implement, test, and return evidence to the parent without starting
feature-loop or its review/repair cycle. Keep ticket implementation and testing
requirements. Route ticket implementers using the implementation model below.

Once every ticket's changes have been integrated and all writers have finished,
run step 3 on the parent's combined integration tree in place of
`implement-spec`'s final code-review phase. Review the full accumulated feature
against the original baseline and parent specification, including committed,
staged, unstaged, and relevant untracked changes. Include interactions between
tickets and spec-wide acceptance criteria; preserve unrelated existing work.
Every review and repair round retains this parent scope and the same run's
counters, including the mandatory final structural review.

After `SUCCESS`, the parent performs step 4 once for the combined integration
branch, then resumes `implement-spec`'s cleanup. A blocked or incomplete loop
leaves parent acceptance pending; implemented children alone do not establish
completion. Preserve explicit user delivery limits throughout.

## Model routing

Route each worker this workflow dispatches to its role's preferred model when the
harness can spawn agents on another provider:

| Role | Model | Effort |
| --- | --- | --- |
| Implementer (step 2 or ticket workers) and repair executor | GPT Sol (`gpt-6.1-sol`) | high |
| Matt reviewer, its Standards and Spec children, and repair handoff writer | GPT Sol (`gpt-6.1-sol`) | high |
| Final structural reviewer | Claude Opus 5.5 (`claude-opus-5-5`) | high |

During setup, before the first dispatch, check for cross-provider delegation:
for example, T3 Code's `orchestrator_capabilities` reports
`canRunCrossProviderChildTask` with each provider's models and options. Dispatch
through that harness's tool. In T3 Code, call `delegate_task` with
`target.providerInstanceId`, `target.model`, and the effort option it lists
(Codex `reasoningEffort`, Claude `effort`) and the matching `role`. Review and
repair workers use `isolation: "shared"` in the integration checkout so they see
its uncommitted changes. Standalone implementers also use that checkout; ticket
implementers retain `implement-spec`'s checkout isolation and integration rules.
Record the resolved provider, model, and effort for each role in `state.md`.

If Claude reports exhausted subscription credits or a subscription usage limit
at setup or during the final structural review, switch that role to GPT Sol
(`gpt-6.1-sol`) with high effort (`reasoningEffort: "high"` in T3 Code) for the
rest of this run. Tell the user and record the credit failure and resolved routing
in `state.md`; pass the fallback to the final reviewer's brief. Use a fresh
independent reviewer for any permitted retry, carrying forward the same scope, evidence,
and consumed counters. A failed review still consumes its dispatch budget; this
fallback does not authorize another final review or extend the loop. If GPT Sol
high is unavailable, report the blocker instead of silently substituting another
model. Other Claude failures do not trigger this credit fallback.

The Matt reviewer's Standards and Spec children run on the reviewer's own model.
Context research stays on the coordinator's default. When cross-provider
delegation or a preferred model is unavailable, dispatch that role with the
harness's native workers, record the substitution in `state.md`, and tell the
user before the first dispatch. Routing never relaxes reviewer independence or
the dispatch budget.

The shared references ship with `thermo-nuclear-code-quality-review`; install or
sync that package alongside this skill. Reading its plain references does not
invoke its user-only skill. Project instructions supply tracker, domain,
worktree, validation, and delivery conventions.
