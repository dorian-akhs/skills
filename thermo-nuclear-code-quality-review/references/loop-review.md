# Review and repair workflow

Shared execution after a feature implementation or preparation of existing work.
The coordinator owns the run, classifications, decisions, and dispatch budget.

## Budget and ownership

Use at most three Matt review attempts and three structural review attempts.
Each Matt attempt contains separate Standards and Spec reviewers and counts as
one round. Count failed and incomplete dispatches too; persist each counter
before dispatch. Context, handoffs, implementation, and targeted verification
consume no review attempt. Preserve separate budgets; never restart one phase
because the other found a problem.

Matt repairs may follow each round, including round three, because the structural
phase independently reviews the resulting tree. Structural repairs may follow
attempts one and two only. Attempt three is assessment-only: remaining blockers
require a user decision before further repairs or review. Further attempts or
repair passes require an explicit user extension.

Workers return to the coordinator without starting another loop. Finish all
writers before review; parallel repair tracks must own disjoint files. Account
for capacity for the Matt reviewer's two children before dispatch. On resumption,
retain counters, collect in-flight results, and continue interrupted implementation
from its brief. Failed attempts may be retried only within their phase's remaining
budget after resolving the cause; unavailable evidence is not a repair task.

## Acceptance policy

This policy governs both phases. Matt's `code-review` supplies separate
Standards and Spec axes; [structural review standards](structural-standards.md)
supply the structural inspection criteria. Neither smell labels nor a reviewer's
priority assignment automatically authorize repairs.

Classify each evidenced finding by impact:

- **P0 — critical / blocking:** an immediate severe correctness, safety, or data
  integrity defect. Repair automatically within agreed scope.
- **P1 — high / blocking:** a failed acceptance criterion, failed required check,
  applicable mandatory-rule violation, or demonstrated serious defect or material
  structural problem. Repair automatically within agreed scope. Honor documented
  exceptions and existing tooling enforcement.
- **P2 — significant / nonblocking:** a worthwhile improvement whose impact does
  not justify blocking delivery. Explain the impact, concrete remedy, and tradeoff
  to the user; leave unchanged unless authorized. It triggers neither repairs nor
  another review round on its own.
- **P3 — minor / nonblocking:** a small readability or cleanup suggestion. Report
  briefly and leave unchanged; it triggers neither repairs nor another round.

For a structural P1, identify the unnecessary machinery or structural regression,
the material maintenance burden, a concrete simpler alternative, and evidence
that required behavior survives. A functional bug is not required; a plausible
refactoring, file-size threshold, or Fowler smell alone is insufficient. Ask
"Which machinery can disappear while preserving the agreed requirements?" before
proposing more helpers, layers, pagination, or verification machinery. Prefer
deleting complexity over redistributing it; add an abstraction only when it
makes the affected code demonstrably simpler.

The coordinator validates evidence, severity, scope, and the remedy before
execution. Record accepted and rejected findings with rationale; do not blindly
execute reviewer-assigned P1s or downgrade substantiated blockers to fit the
budget. Preserve stable IDs and originating axes (`Standards`, `Spec`, or
`Thermo-nuclear`), and keep Matt's two reports separate without a combined ranking.
A blocker closes only with verified repair evidence or an accepted evidenced
justification against its rule.

Missing acceptance evidence or incomplete required reviews leave acceptance
unproven. Missing tools are verification/review blockers, not automatic P1 code
changes. Resolve user-owned choices about behavior, compatibility, migration,
scope, and architecture before dependent repairs. Nonblocking suggestions do not
create a user-input gate for otherwise complete work. Present P2 choices at
handoff; if the user authorizes one, record its scope and apply the same budgets
and requirement checks. Authorization does not reset counters or extend limits.

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

Require this evidence appendix from every Matt and structural reviewer
alongside its prioritized structural findings:

```text
Phase: MATT | THERMO_NUCLEAR
Iteration: 1 | 2 | 3
Verdict: PASS | CHANGES_REQUIRED | INCOMPLETE
Requirements:
  - criterion ID: PASS | FAIL | UNVERIFIED; direct evidence
Findings:
  - stable ID; originating axis; P0 | P1 | P2 | P3; BLOCKING | NONBLOCKING;
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

Save Matt reports as `review-<n>.md` and structural reports as
`thermo-nuclear-review-<n>.md`; preserve all earlier reports. Independently check acceptance coverage and finding
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

## 3. Run the bounded structural phase

Enter after Matt passes or its third attempt and any validated Matt repairs.
Resolve required user decisions first. Read
[structural review standards](structural-standards.md) in full and pass its actual
absolute path to a fresh independent reviewer. This reads plain standards; it
does not invoke the enclosing user-only skill.

Before each dispatch, increment and persist `structural_reviews_used` (maximum
three). Supply the fixed baseline, full accumulated scope, project instructions,
requirements, context, decisions, all Matt and structural reports, unresolved IDs,
repair summaries, and current check evidence. Assign read-only inspection of the
full scoped tree, previous closures, and repair regressions. Require the evidence
appendix, impact-based priorities under the acceptance policy, and coverage of
every acceptance criterion. Inspect any missing Matt-axis coverage directly against
its standards and spec. Persist and evaluate the result through step 2.

Run required integration checks on the reviewed tree; include actionable failures
in the evaluation. Choose the next action:

- With complete coverage, verified criteria/checks, and no validated blockers,
  stop immediately with `SUCCESS`. Remaining P2/P3 findings are reported without
  repairs or another review.
- With validated blockers after structural attempt one or two, increment and persist
  `structural_repairs_used` before one pass through [loop repair](loop-repair.md).
  Include all unresolved P0/P1 findings and failed requirements, including Matt
  findings. Verify each repair and affected callers, run applicable checks, then
  dispatch a fresh independent structural reviewer over the resulting tree.
  Targeted verification alone cannot establish final acceptance after repairs.
- With blockers after attempt three, persist `FINAL_BLOCKERS_REMAIN`. Stop repairs
  and present the remaining IDs, evidence, proposed remedies, and required user
  decisions. This assessment-only attempt authorizes no further rewrite.
- For an incomplete or failed review, resolve its cause and retry only if budget
  remains. If meaningful review is impossible, or attempt three lacks usable
  coverage, stop with `BLOCKED_REVIEW`. Do not invent repairs for missing evidence.

## Completion and stopping

Declare `SUCCESS` only when every criterion is verified, every blocker has verified
closure or accepted evidenced justification, required integration checks pass on
the final tree, required user decisions are resolved, and the structural review
covers the final repaired tree. A complete review with only P2/P3 findings passes;
record them separately for the user's choice.

Use `BLOCKED_REVIEW` for unavailable or exhausted incomplete review and
`BLOCKED_VERIFICATION` for unavailable required checks. Preserve artifacts and
consumed budgets on resumption; a new run cannot evade the limits. An explicit
user extension must state which additional reviews or repairs it authorizes.

The maximum automatic path is Matt 1 → repairs → Matt 2 → repairs → Matt 3 →
repairs → structural 1 → repairs → structural 2 → repairs → structural 3.
Skip remaining attempts as soon as their phase passes. Failed dispatches consume
the same budgets. Structural attempt three never authorizes automatic repairs.

Persist final status and evidence paths. Report outcome, Matt and structural
attempts used out of three each, repairs, actual checks and results, unresolved
criteria, important decisions, pending questions, and retained briefs. Lead with
remaining blockers when acceptance was not achieved. Preserve each review's
original verdict; distinguish repair verification from the subsequent independent
review. Present P2 findings with impact, remedy, and tradeoff for user selection;
report P3 briefly. Nonblocking findings do not prevent acceptance or delivery.
