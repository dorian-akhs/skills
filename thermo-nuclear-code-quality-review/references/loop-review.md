# Review and repair workflow

Shared execution after a feature implementation or preparation of existing work.
The coordinator owns the run, classifications, decisions, and dispatch budget.

## Budget and ownership

Use at most three Matt rounds, one final structural review, repairs after each
Matt round when needed, and one final repair pass. A Matt round contains separate
Standards and Spec reviewers and counts as one round. Count every dispatched
review, including failed or incomplete attempts; persist counters before dispatch.
Context, handoffs, implementation, and targeted verification consume no review
round. Further full reviews or corrective implementation passes require an
explicit user extension.

Workers return to the coordinator without starting another loop. Finish all
writers before review; parallel repair tracks must own disjoint files. Account
for capacity for the Matt reviewer's two children before dispatch. On resumption,
retain counters and final-phase flags, collect in-flight results, and continue
interrupted implementation from its brief. A consumed final review without a
usable result stops with `BLOCKED_REVIEW`. A completed final repair pass does not
authorize another repair dispatch.

## Acceptance policy

This workflow supplies the blocking policy; Matt's `code-review` supplies its
separate Standards and Spec axes:

- Failed acceptance criteria or required checks block completion. Unverified
  criteria and incomplete required reviews leave acceptance unproven.
- A documented-standard violation blocks when the rule is mandatory and
  applicable. Cite the rule and conflicting code; honor documented exceptions
  and tooling's existing enforcement.
- A correctness, safety, compatibility, or maintainability finding blocks when
  it demonstrates a concrete defect or material structural regression in scope.
  State its impact and an actionable remedy.
- Substantiated, actionable Fowler smells require improvement even without a
  correctness defect. Name the smell, cite code, and propose the simplest scoped
  remedy. A label alone is insufficient: reject false positives or record an
  applicable exception. Unresolved actionable smells are blocking quality repairs.
- The final structural review applies the presumptive blockers and approval bar
  in [structural review standards](structural-standards.md). Keep those findings
  distinct from Matt's heuristic smells.

Preserve stable finding IDs and originating axes (`Standards`, `Spec`, or
`Thermo-nuclear`). Keep the two Matt reports separate, without a combined ranking.
A blocker closes only with verified repair evidence or a recorded, evidenced
justification accepted against its rule. Budget pressure cannot downgrade a
finding. Optional suggestions alone trigger neither repairs nor extra Matt rounds.

Prefer deleting duplication, branches, or unnecessary layers. Add an abstraction
only when it demonstrably simplifies the affected code. Keep fixes in scope and
verify preserved behavior; a smell label is not a prescription for new modules,
interfaces, or types.

## 1. Dispatch a Matt reviewer

Before the first Matt dispatch, read the resolved `code-review` instructions and
confirm separate Standards and Spec coverage. When `reviews_used < 3`, increment
and persist the counter, then spawn a fresh independent reviewer with:

- The model-available `code-review` path and an explicit instruction to apply its
  separate Standards and Spec sub-agent reviews. Honor invocation boundaries
  established in [loop setup](loop-setup.md).
- Project root and instructions, fixed baseline, recorded scope, `requirements.md`
  as the supplied spec, context, decisions, relevant source references, work
  inventory or implementation/repair summary, prior reports, and check evidence.
- Exact review inputs: all accumulated scoped committed, staged, and unstaged
  changes against the fixed baseline, plus relevant untracked files. Supply the
  same inputs to both axes. Explicitly override committed-only defaults; exclude
  unrelated user edits and run artifacts.
- For explicit current-file/module or non-Git review, the scoped contents and
  snapshots. This supplied scope replaces diff-only inputs and empty-diff
  rejection; report that current contents are being reviewed.
- The known project's standards and tracker guidance. The supplied spec and
  gathered sources satisfy discovery; neither axis may silently skip coverage
  or require installing/configuring a tracker.
- The acceptance policy and a read-only assignment for application code. Inspect
  source and affected callers directly, assess evidence, and return findings and
  remedies to the coordinator.

Review the full accumulated scope each round, recheck previous blockers, and
inspect for repair regressions. Preserve separate `## Standards` and `## Spec`
reports and their per-axis word limits. Put exhaustive evidence in an appendix
outside those concise reports; word limits cannot omit required findings or
acceptance coverage. Implementation claims and briefs are not proof.

Require this evidence appendix from every Matt review and from the final reviewer
alongside its prioritized structural findings:

```text
Phase: MATT | THERMO_NUCLEAR
Iteration: 1 | 2 | 3 | FINAL
Verdict: PASS | CHANGES_REQUIRED | INCOMPLETE
Requirements:
  - criterion ID: PASS | FAIL | UNVERIFIED; direct evidence
Findings:
  - stable ID; originating axis; BLOCKING | NONBLOCKING;
    documented violation | judgment call; file/symbol/line;
    evidence; concrete impact; requested remedy; verification;
    previous-finding status
Verification:
  - commands and actual outcomes; checks not performed
Important decisions:
  - decision ID; DECIDED | PROPOSED | NEEDS_USER_INPUT;
    owner; rationale; consequences; related requirement/finding IDs
Questions for the user:
  - decision ID; specific question; options and tradeoffs;
    recommendation; dependent work
Limitations:
  - missing context, failed tools, unavailable manual checks
```

## 2. Evaluate the result and choose the next phase

Save Matt reports as `review-<n>.md` and the final report as
`thermo-nuclear-review.md`. Independently check acceptance coverage and finding
evidence. Missing coverage or contradictory findings make a report `INCOMPLETE`
despite a claimed `PASS`; Matt reports must contain both axes. Persist unresolved
findings and checks in state, update decisions, and carry accepted answers into
handoffs.

After each attempt, send a concise conversation update with round/phase, verdict,
blockers, and important decisions with rationale and consequences. Distinguish
decided remedies from proposals awaiting input.

Reviewers may assess remedies and justifications, but unresolved product behavior,
compatibility, migrations, scope, and architecture commitments remain user-owned
decisions. Resolve routine implementation choices from agreed requirements and
project conventions. Ask concrete questions with options, tradeoffs, and a
recommendation for material unresolved choices. Persist `WAITING_FOR_INPUT` for
dependent work, preserve counters, and continue independent work where possible.
Record answers before resuming.

For a Matt result:

- `PASS` with verified criteria and no blockers advances to the final phase;
  it is not workflow success.
- Actionable blockers or failed requirements enter [loop repair](loop-repair.md),
  including after round three. Read that branch only when a repair is needed.
  After repairs, dispatch the next Matt round if budget remains; otherwise enter
  the final phase.
- Failed or incomplete attempts may be retried within the remaining budget after
  resolving their cause. Missing evidence or unavailable tools are not invented
  implementation tasks. If essential context/tooling prevents meaningful review,
  stop with `BLOCKED_REVIEW`. At the limit, carry remaining coverage gaps to the
  final reviewer.

After round three, persist `MATT_LIMIT_REACHED` and notify the user that the
three-round budget is exhausted, any required repairs remain, and the final
structural review follows. Include unresolved IDs and pending decisions. The
limit does not skip the mandatory final phase or establish acceptance.

## 3. Run the single final structural review

Enter after Matt passes or its third attempt and any actionable Matt repairs.
Resolve required user decisions first. Read
[structural review standards](structural-standards.md) in full and pass its actual
absolute path to a fresh independent reviewer. This reads plain standards; it
does not invoke the enclosing user-only skill.

Persist `final_review_used: true` before dispatch. Supply the fixed baseline,
full accumulated scope, project instructions, requirements, context, decisions,
Matt reports, unresolved findings, repair summaries, and current check evidence.
Assign read-only review of application code against the structural standards and
approval bar. Require the evidence appendix, direct verification of unresolved
Matt findings, and coverage of every acceptance criterion. Any missing Matt-axis
coverage must be inspected directly against its standards and spec before
acceptance. Persist and report the result through step 2. An incomplete final
report stops with `BLOCKED_REVIEW`; it does not authorize another full review.

Run required integration checks on the reviewed tree. Add actionable failures to
the unresolved criteria. If blockers remain, persist `final_repair_used: true`
before executing one final pass through [loop repair](loop-repair.md). Its brief
covers all unresolved blockers and failed requirements, including remaining Matt
findings. Honor structural presumptive blockers unless an evidenced justification
is accepted. The pass may have planned waves; it is not an open-ended repair loop.

After the final review and any repairs, perform targeted verification of every
blocker, inspect repaired code and affected callers for regressions, recheck every
criterion, and run required integration checks on the combined current tree.
Reuse earlier results only when they demonstrably cover that tree. This is repair
verification, not another full structural review or a fourth Matt round.

## Completion and stopping

Declare `SUCCESS` only when every criterion is verified, every blocker has verified
closure or accepted evidenced justification, required integration checks pass on
the final tree, required user decisions are resolved, and the mandatory final
review is complete with coverage gaps resolved. Keep a pre-repair
`CHANGES_REQUIRED` verdict intact and record repair verification separately.

Use `BLOCKED_REVIEW` for failed/incomplete final review and
`BLOCKED_VERIFICATION` for unavailable required checks. If the final repair pass
or its verification leaves actionable blockers, persist `FINAL_BLOCKERS_REMAIN`,
retain a brief documenting remaining work, and notify the user immediately. Report
missing manual checks and unresolved decisions explicitly. Preserve all artifacts
and consumed budget on resumption; another run cannot evade the limits.

The maximum path is Matt 1 → repairs → Matt 2 → repairs → Matt 3 → repairs →
final structural review → final repairs → targeted verification and integration
checks. Early Matt acceptance skips remaining Matt rounds, then runs the final
phase.

Persist the final status and evidence paths. Report outcome, Matt rounds used out
of three, final review/repair usage, scoped behavior and fixes, actual checks and
results, unresolved criteria, important decisions, pending questions, and any
retained brief. Lead with remaining blockers when acceptance was not achieved.
Distinguish the final review's original verdict from post-fix targeted
verification; fixes after that review did not receive another full independent
review. Keep optional findings separate from acceptance blockers.
