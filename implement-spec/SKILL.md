---
name: implement-spec
description: "Implement a specification, preparing missing tickets before building the dependency graph."
disable-model-invocation: true
---

Implement the supplied specification on one integration branch. Prepare its
child tickets before implementation when their coverage is missing or incomplete.

The issue tracker should have been provided to you. If not, tell the user to run `/setup-matt-pocock-skills`.

The goal is the entire spec implemented on a single **integration branch**, with every ticket resolved the way the issue tracker closes work.

The tickets are not a list of steps. They are a **task graph** with blocking relationships between them. This means there is always a **frontier** of tickets which are ready to be grabbed.

Communication to and from subagents should be sparse. Communicate primarily through **context pointers**: to the spec, tickets, research notes, and previous commits. Don't duplicate information already available via pointers.

**Implementer subagents** should be run in the background where possible for maximum concurrency.

## Prepare the ticket graph

Read the complete specification, relevant comments, and existing child tickets.
Check that their acceptance criteria cover the specification and their blocking
edges describe the implementation dependencies. Reuse a complete graph directly.
When coverage is missing or incomplete, read the adjacent global
[to-tickets](../to-tickets/SKILL.md) and follow its preparation mode to publish
the missing tickets. This invocation authorizes that composition and ticket
publication without a separate breakdown approval. Use the adjacent file so
preparation follows the user's global workflow when a project has a skill with
the same name.

Resolve open product decisions with the user before publishing affected tickets.
For settled requirements, report the prepared graph and continue directly to
the implementation steps. Preparation is complete when every acceptance
criterion is covered and all blocking references resolve to existing tickets.

## Composing with feature-loop

When the user requests `implement-spec using feature-loop`, read the adjacent
global [feature-loop](../feature-loop/SKILL.md) and follow its composition rules.
Prepare the graph before dispatching ticket workers. The parent owns one loop
over the entire specification and integrated changes. Use that loop's review,
repair, and delivery phases in place of steps 7–8, then perform step 9.

## PR target and rebase

Before creating a PR, including the early draft in step 3, and before marking
it ready for review, identify its exact target repository, remote, and branch
from the user's instructions and project conventions. Ask if the target remains
ambiguous. Use that same target explicitly when creating the PR; for an existing
PR, read its current base.

Pause integration writers and wait for active merges to finish. Preserve any
uncommitted work, fetch the target branch from its remote, and rebase the
integration branch onto the fetched tip. Resolve conflicts while preserving all
integrated ticket work, then rerun applicable checks on the rebased result.
Verify `git merge-base --is-ancestor <fetched-target-tip> HEAD` succeeds before
pushing and creating the PR or marking it ready. If the rebase rewrites an
already-pushed branch, use `--force-with-lease` pinned to its verified remote
head. Reconcile unexpected remote changes before retrying. Resume workers from
the updated integration tip.

This gate also applies when feature-loop owns delivery. Report the target and
fetched commit used for the rebase with the PR delivery result.

## Steps

1. Use the prepared specification and ticket graph to select the ready frontier.

2. (optional) Use an **exploration subagent** to conduct any exploration required by the tickets - relevant codebase files or external documentation. Ensure the exploration subagent can save files - it should save its markdown notes in a directory outside the repo, accessible by all future subagents. This lets **implementer subagents** focus on implementation rather than exploration.

3. Create the integration branch. If the issue tracker closes work through PRs, or the user asks for one, open a draft PR after the first merge in step 5 (a branch with no commits ahead of the PR target can't open one), marked as closing the spec and tickets.

4. Use **implementer subagents** to implement each ticket, each in its own worktree on its own branch. Each implementer subagent:
   - confirms its worktree is based on the integration branch before starting, and resets onto it if not;
   - calls the Skill tool with `tdd` to build the ticket;
   - merges the integration branch tip into its own branch before reporting done

5. Once an **implementer subagent** completes, merge its work to the integration branch with a **merger subagent**.

6. If this changes the **frontier** of available tickets, kick off more **implementer subagents** to work on the new tickets. This allows for maximum concurrency.

7. Once all tickets are complete, call the Skill tool with `code-review` on the integration branch. Fix all issues raised by the code review in a single **implementer subagent**.

8. If a draft PR exists, mark it ready for review. Otherwise, resolve each ticket the way the issue tracker closes work, and report the integration branch.

9. Clean up all **implementer subagent** worktrees.
