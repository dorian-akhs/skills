---
name: auto-grill
description: "AFK grill: an adversarial sub-agent asks questions; this thread answers, decides, and accepts its recommendations until the decision tree is exhausted. Optional ticketing and implementation."
disable-model-invocation: true
---

# Auto-grill

Run `/grilling` without requiring the user to answer each round. An adversarial sub-agent asks the questions; this thread answers, decides, and continues until the decision tree is exhausted.

Optional follow-on actions:

- `task` publishes tickets using `/to-tickets`.
- `implem` implements the published tickets using `/implement`.

This auto-acceptance applies only within this skill. It does not change the human-approval gates of `/grilling`, `/to-tickets`, or `/implement` when they are run directly.

## Arguments

Parse from the end: while a token is a recognised keyword, treat it as an option. The first unrecognised token ends the suffix; everything to its left is the subject.

| Token | Effect |
| --- | --- |
| Free-form prefix | The grill subject. If empty, grill the plan already present in the conversation. If neither exists, ask for a subject and wait. This is the only allowed pause in this skill. |
| `task` | Optional. After grilling, publish tickets using `/to-tickets`. |
| `implem` | Optional. Implement the published tickets using `/implement`. Implies `task`. |
| Suffix after `implem` | Options relayed verbatim to `/implement`, if that skill supports them. |

If the parsed subject still contains `task` or `implem`, a suffix token was not recognised. Stop, show the valid `/implement` options, and do not start the chain.

Examples:

```text
/auto-grill
/auto-grill redesign the territory selector
/auto-grill task
/auto-grill redesign the territory selector task implem
```

## Process

### 1. Establish the subject

Resolve the subject using the argument rules. Explore the codebase and relevant project documentation to establish facts before asking questions. Determine where to write the report: use the project’s configured work or ticket directory; otherwise use `.scratch/<subject-slug>/`.

Record the subject, established facts, and report directory before continuing.

### 2. Run a question round

Delegate to a separate adversarial sub-agent. Give it:

- the subject;
- established facts;
- the complete decision log so far.

Ask it to apply `/grilling` and return the next round of open questions, each with a recommendation. Do not provide the conclusion you expect.

The round is complete when it returns questions or explicitly says there are no further questions.

### 3. Answer and decide

For each question, in order, record:

- recommendation;
- decision;
- one-line rationale.

When equally sound options exist, choose the most reversible default.

Mark a decision as **owner validation required** when it is a product, legal, budget, prioritisation, or user-commitment decision. Decide it anyway; the loop must not stop. List it separately so the owner can confirm or overturn it later.

### 4. Iterate

Send the subject, facts, and complete decision log back to the adversarial sub-agent for the next round.

Stop when it reports no further questions, or after five rounds. Reaching the limit means the grill is incomplete; record the open branches.

### 5. Write the report

Before any follow-on action, write `GRILL.md` in the report directory.

```markdown
# Grill — <subject>

Date: <YYYY-MM-DD> · rounds: <n> · status: <exhausted | limit reached>

## Decisions requiring owner validation

1. **<decision>** — <what it commits to and how to reverse it>

## Decided plan

<What will be built, in what order, and where the scope ends.>

## Decision log

### <n>. <question>

- **Recommendation** — <…>
- **Decision** — <…> <owner validation required, if applicable>
- **Rationale** — <…>

## Open branches

<Use “None” when exhausted. Otherwise list unresolved branches.>
```

Write for a human reader in plain English.

### 6. Optional follow-on: `task`

If `task` was requested, use `/to-tickets` with `GRILL.md` as the source.

If the project has not configured an issue tracker, stop and instruct the user to run `/setup-matt-pocock-skills`; do not guess the tracker.

Replace `/to-tickets`’ normal user quiz with one adversarial review of the proposed ticket breakdown. Ask the sub-agent to check granularity, dependencies, and whether tickets should be merged or split. Incorporate valid objections, then publish tickets without waiting for human approval.

Retain the published ticket identifiers in dependency order.

### 7. Optional follow-on: `implem`

If `implem` was requested, run `/implement` for the published ticket identifiers in dependency order, passing through supported implementation options.

Pass ticket identifiers explicitly. Do not claim arbitrary backlog work.

### 8. Failure handling

A failed stage stops the chain at that stage without rollback. Keep `GRILL.md` and any tickets already published. Do not retry downstream stages or re-grill the failure.

### 9. Summary

Provide an executive summary in this order:

1. Numbered decisions requiring owner validation.
2. The decided plan.
3. Rounds completed and whether the limit was reached.
4. Published ticket identifiers.
5. Implementation result.
6. The stage at which the chain stopped, if applicable.
