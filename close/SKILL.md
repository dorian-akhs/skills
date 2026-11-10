---
name: close
description: Merge a reviewed PR after approving its commit message, clean up its branches and worktree, then settle the conversation.
disable-model-invocation: true
---

## Resolve the work

Read repository instructions for merge strategy, commit conventions, retained
artifacts, and workspace lifecycle. Default to squash unless the user requests
another strategy or the repository requires one (for example, release promotions).

Identify the runtime, repository, main checkout, Git common directory, current
worktree and branch. Resolve the session's PR and read its live GitHub state,
base/head repositories and branches, head SHA, diff, checks, and review status.
Use available host or GitHub tools; otherwise use the authenticated GitHub CLI.
Treat conversation claims of a merge as a cue to verify GitHub.

If the PR is missing or ambiguous, ask for its URL before merging or deleting
anything. If closed without merging, ask what the user wants to retain or remove.
Do not create a PR as part of closing.

Completion: one verified PR is associated with the intended local work, and its
state, merge rules, and exact cleanup targets are known.

## Merge an open PR

Start from the PR title and description, reconcile them with the actual diff,
and follow repository commit conventions. Present the PR URL, target branch,
strategy, exact commit subject, and **always a detailed commit body**. Explain
the changes, their purpose, and validation actually performed; identify untested
paths without inventing results. Use repository language rules.

Ask the user to approve this concrete proposal. Approval covers the shown merge
and subsequent cleanup; do not ask again for routine cleanup. Bind approval to
the PR, base branch, head SHA, strategy, and exact message. Changed commits,
target, strategy, or message require a fresh proposal and approval.

Check current merge eligibility before merging. Wait for running checks through
the host's PR-following mechanism when available. Follow its continuation rules;
otherwise use a bounded status check and report pending work. Failed checks,
conflicts, or missing required approval block closing: report them, preserve the
workspace, and leave the conversation active. Do not bypass requirements or fix
code as part of this skill.

After approval, merge with the approved subject and body and an atomic expected
head guard. With `gh pr merge`, use `--match-head-commit`, `--subject`, and
`--body-file`, plus the selected strategy. Write the body through a file or
structured argument to preserve newlines and literal text. Keep branch deletion
separate from merging: `--delete-branch` also touches local branches.

Auto-merge registration or queue admission is still pending work. Follow the PR
until GitHub reports it merged, without bypassing the queue. If a queue cannot
honor the approved strategy or message, resolve that before proceeding.

Completion: GitHub confirms the approved PR is merged, with its merge commit
recorded. A successful command or an enabled auto-merge is insufficient.

## Clean up a merged PR

For an already merged PR, skip merge approval and inspect its merged head and
merge commit. Recheck GitHub state and every deletion target before cleanup.
Invocation authorizes removal of the merged worktree and local/remote working
branches, subject to these preservation checks.

- Verify the local branch and worktree correspond to the merged PR. Preserve
  additional local commits or changes on a remote branch that advanced after
  merging. A matching branch name alone is insufficient.
- Check tracked modifications and non-ignored untracked files. If any remain,
  keep the worktree and local branch and report the files; do not stash, commit,
  reset, or discard them automatically.
- Review ignored files under repository retention rules. Move required evidence
  and deliverables outside the worktree before removing it. Dependencies,
  caches, and disposable development data may be removed. If a file's value is
  uncertain, ask and suspend cleanup; keep secrets out of the report.
- Identify processes by worktree ownership and working directory, then stop only
  those belonging to the worktree being removed.

For a dedicated worktree, run cleanup from a surviving checkout. If the host
owns the checkout or binds a conversation to it, discover its supported lifecycle
procedure before removal. Use that procedure to preserve a valid conversation
binding. If unavailable, report cleanup as pending and retain the checkout;
filesystem removal does not establish host cleanup. For ordinary Git worktrees,
use Git's worktree removal after preservation checks, without forced removal.

For the main checkout, preserve the directory. When clean, switch to the PR's
base branch, respecting its existing worktree bindings, before deleting the
merged working branch. Report a blocked switch instead of forcing it.

Delete only verified merged working branches; preserve base, default, protected,
and other sessions' branches. Verify the remote repository, ref, and current SHA
against the merged PR head before deleting remotely; guard against concurrent
ref changes. A remote branch already deleted needs no further action. Preserve
fork branches when ownership or deletion authority cannot be established.

A squash merge does not make the working branch an ancestor of the base branch.
If safe local branch deletion is refused for that reason, deletion with `-D` is
allowed only after verifying the local tip exactly matches the merged PR head,
the PR is merged, the worktree is removed or switched away, and no other worktree
uses that branch. Otherwise preserve it and report the mismatch.

Completion: the worktree is removed or the main checkout safely retained, required
artifacts survive, its owned processes are stopped, and both working branches
are absent or explicitly retained under a repository protection rule. Any other
pending cleanup keeps the conversation active. Repeated invocation safely skips
operations already completed.

## Finish the conversation

Report the PR URL, merge strategy and commit, removed branches/worktree, retained
artifacts, and anything still pending. Distinguish merged from queued and partial
cleanup from complete cleanup. Release any PR watch when the workflow is finished.

Only after every required operation succeeds, use the host's conversation
`settle` action. In T3, discover `t3_thread_organize` and call it with
`action: "settle"` for the current thread. Archive instead only when explicitly
requested. Settling applies at turn end; an error or queued message can keep the
thread active. Outside T3, use an equivalent supported action if available;
otherwise report that Git cleanup completed and settling is unavailable.

Completion: the final report accurately covers every operation and the supported
conversation action has been requested, or its unavailability is explicit.
