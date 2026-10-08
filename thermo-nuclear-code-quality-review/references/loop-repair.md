# Loop repair

Read this branch only when actionable blockers or failed requirements require
implementation. Repairs remain within the requested scope and justified
structural changes needed to resolve those findings.

## Prepare the brief

Resolve required user decisions before preparing executable tasks. A retained
brief may record pending prerequisites while an answer is outstanding.

Locate and read the model-available `handoff-implement` dependency through the
recorded catalog/configured locations. If missing or user-only without a permitted
entry point, stop with `BLOCKED_HANDOFF` and preserve unresolved findings.

Create `<run-directory>/handoff-<n>/` for Matt repairs or
`<run-directory>/handoff-final/` for final repairs. Use a fresh directory with no
active `HANDOFF-IMPLEMENT.md`; preserve unrelated briefs. Spawn a handoff writer
with that working directory, the dependency's actual path, and a Create-mode-only
assignment. Run application commands in the absolute project root.

Supply the original requirements, context and source references, decisions,
accepted answers, review reports, all outstanding finding IDs, check results,
project instructions, project root, and scope/ownership boundaries. Require the
dependency's full measured brief contract, including its execution shape,
bounded read sets, per-agent prompt contract, and verification plan. Mark new
files nonexistent with estimated sizes. Link tasks and criteria to requirement
and finding IDs.

The brief's §0 records existing execution authorization, phase, project root,
scope boundaries, and return to the coordinator without another review loop.
The writer stops when the brief is ready; it never implements. This worker stop
ends its assignment, not the coordinator's workflow.

Require the writer to return the brief path, execution shape, measured context
budget, and remaining uncertainties. Inspect the brief against the dependency's
contract. Archive it as `handoff-final.md` inside the handoff directory before
execution. An unusable brief stops the run with `BLOCKED_HANDOFF`.

## Execute and verify

With no required decision pending, dispatch a separate implementer with the
brief's working directory, absolute project root, and dependency path. State
explicitly that execution is already authorized; follow Execute mode and §0
without another routine confirmation. Standalone handoff invocations retain
their own approval behavior.

Follow the brief's measured solo-or-wave plan and exclusive file ownership.
Verify the combined tree between waves. Its solo fallback may handle unavailable
nested implementation agents; independent review still requires a separate
reviewer.

Require changed files, actual commands and outcomes, evidence mapped to finding
IDs, unmet criteria, important decisions with rationale, and limitations. Wait
for all writers, inspect the combined tree, verify claimed closures, and persist
the result. Implementation claims and the brief alone are not repair evidence.

The executor may remove its active `HANDOFF-IMPLEMENT.md` only after satisfying
the dependency's completion criteria. Keep the archive and unresolved active
briefs. An interrupted assignment resumes from its existing brief; a completed
final repair pass needs an explicit user extension before another repair dispatch.
