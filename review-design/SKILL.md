---
name: review-design
description: Review and agree the solution's module design after grill-with-docs and before to-spec.
disable-model-invocation: true
---

# Review Design

Give the user ownership of consequential design choices before implementation.
Start from the functional outcomes agreed during `grill-with-docs`; turn them
into a solution design the user can understand, challenge, and agree with.

The route is `grill-with-docs` → `review-design` → `to-spec` → `to-tickets` →
`implement` per ticket or `implement-spec` for the whole specification. This
skill reviews the proposed solution before code exists. Keep production code
unchanged and leave specification publication, ticket creation, and execution
to their separately invoked skills.

## Establish the starting point

Read the applicable project instructions and skill workflow, when present.
Use the current conversation or supplied functional specification, including
linked issue comments, as the scope. Reuse settled requirements and constraints;
ask about missing information only where it changes the design.

Load `codebase-design` through the harness's skill mechanism. When no Skill
tool is available, read its `SKILL.md` completely. Use it as the reference for
depth, leverage, locality, interfaces, and seams throughout this review.

Inspect the relevant implementation, tests, glossary, and ADRs. Explain which
existing modules already carry the behavior and what actually needs to change,
with source links. Separate verified facts, proposals, and uncertainties. Find
environment facts yourself; bring design decisions to the user.

## Make the solution concrete

Present a compact proposal grounded in the agreed behavior:

- A small diagram of the modules and dependency direction, distinguishing
  existing modules from changed or new ones.
- Each affected module's responsibility, the state and invariants it owns,
  and the complexity callers no longer have to coordinate.
- Illustrative interface sketches and caller examples, including the ordering
  constraints, errors, and configuration callers must understand. Label sketches
  as provisional rather than production code.
- A walkthrough of a representative user action and a meaningful failure path:
  trace calls, state changes, and externally observable outcomes.
- Proposed testing seams, the behavior each verifies, and how external
  dependencies are supplied. Reuse suitable existing seams and coverage.

Scale the proposal to the change. A small change may need one interface sketch
and a short explanation. Include deployment, schema, migration, or compatibility
choices only when the feature makes them consequential, following the project's
existing delivery requirements.

Apply the `codebase-design` principles to the proposal, including the deletion
test and seam discipline. Prefer reuse and the simplest workable design. When
dependency substitution affects the design, consult that skill's `DEEPENING.md`.

## Review choices with the user

For each consequential choice with a credible alternative, compare the options
before settling it. Include the simplest viable option, concrete interface or
usage differences, the costs each imposes on callers and maintainers, and your
recommendation with its rationale. Avoid manufacturing alternatives for routine
details or presenting an already completed design as inevitable.

Ask focused rounds of independent design questions, giving a recommendation
for each. Wait for the user's answers before deciding dependent questions.
Revise the diagram, interfaces, and testing seams as choices change. Reuse
agreement already given; a recommendation, silence, or elapsed time is not
agreement. Leave routine internal implementation choices to the implementer.

If a consequential uncertainty needs runnable evidence, explain the question
and suggest a separately invoked `prototype` or `research` detour. Keep that
choice unresolved until evidence returns. If the design exposes a functional
gap, ask about that gap rather than silently changing the agreed scope.

The review is complete only when consequential choices and testing seams are
settled and the user confirms the resulting design. Until then, clearly identify
what remains proposed or unresolved and continue the discussion.

## Carry the agreement forward

Present a concise agreed-design brief in the conversation containing:

- Functional scope and constraints, referencing their existing source.
- Module responsibilities, dependency direction, and agreed interface behavior.
- Consequential decisions, their rationale, and rejected alternatives.
- Agreed testing seams and relevant delivery or migration requirements.
- Any remaining implementation latitude and assumptions to verify.

Include this instruction in the brief for the specification and implementers:
bring material deviations back to the user before implementing them. A change
to agreed module responsibilities, interface behavior, dependency direction,
state ownership, testing seams, or a consequential tradeoff requires renewed
design discussion; private helpers and equivalent internal arrangements remain
implementation choices.

The brief feeds `to-spec`'s Implementation Decisions and Testing Decisions;
illustrative sketches communicate intent, not a requirement to copy code into
the specification. Keep execution state on the configured tracker rather than
creating a parallel design register. If a decision merits an ADR or terminology
changes, load `domain-modeling` and follow the project's documentation rules.

Suggest `to-spec` as the next user invocation. Design agreement authorizes
neither implementation nor commits or external publication by itself.
