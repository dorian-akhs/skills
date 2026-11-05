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

Resume `implement-spec`'s delivery and cleanup steps after the loop reaches
`SUCCESS`. A blocked or incomplete loop leaves parent acceptance pending;
implemented children alone do not establish completion. Preserve the user's
commit, push, and PR permissions throughout.

## Model routing

Route each worker this workflow dispatches to its role's preferred model when the
harness can spawn agents on another provider:

| Role | Model | Effort |
| --- | --- | --- |
| Implementer (step 2 or ticket workers) and repair executor | GPT Sol (`gpt-6.1-sol`) | high |
| Matt reviewer, final structural reviewer, and repair handoff writer | Claude Opus 5.5 (`claude-opus-5-5`) | high |

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
