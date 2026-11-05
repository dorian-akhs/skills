# Loop delivery

Shared branch and PR delivery for `feature-loop` and `review-loop`. Their
invocations authorize scoped commits, pushes, and PR creation or updates unless
the user explicitly limits delivery. These instructions supply delivery authority
for the shared setup and review workflow; they do not authorize merge or deploy.

## Select the task branch during setup

Identify the repository, intended PR base, current branch, and any existing PR
for the task. Follow the project's runtime and checkout conventions. Reuse an
existing dedicated task branch, including the supplied PR's head branch; otherwise
create one from the agreed starting point before any worker writes. Avoid direct
commits or pushes to the PR base or a protected/shared integration branch.

Record the checkout, branch, remote, base, and existing PR URL in `state.md`,
alongside the fixed review baseline and existing-work boundaries. Ask if the
intended base or branch ownership is materially ambiguous. Branch selection is
complete when all workers target the recorded task checkout and scope.

## Deliver after review acceptance

After the shared workflow reaches `SUCCESS` and all writers finish:

1. Inspect the final diff and check evidence. Stage only task-owned changes;
   exclude unrelated edits, secrets, and `.agent-work/` artifacts. Commit using
   project conventions; retain existing commits and skip an empty commit when
   there are no new changes.
2. Push the dedicated task branch to its recorded remote, setting an upstream
   when needed. Preserve remote work; do not force-push or discard others' edits.
   If integration changes the verified tree, revalidate affected behavior and
   preserve the run's review counters and stopping conditions.
3. Find an open PR matching the task repository, head, and intended base. Update
   it to describe the final scope and verification, or create one if absent.
   Follow project PR conventions and the `pr` skill when available. Include the
   actual checks, remaining limitations, and applicable issue links. Reuse a clean
   existing PR even when review needed no repairs; never manufacture a diff.
4. Verify the remote head contains the scoped commits and the PR targets the
   recorded base/head. Record the commit SHA, PR URL, and delivery outcome in
   `state.md`. Use the harness's PR-linking tool when available.

Delivery is complete only when the branch is pushed and its PR is created or
updated and verified. If there is no publishable diff, report that explicitly.
If review is blocked or incomplete, preserve the branch and evidence without
claiming delivery complete. If Git, authentication, or PR tooling blocks delivery,
report the exact remaining action separately from review acceptance. Honor
explicit local-only or narrower delivery instructions without asking again.
