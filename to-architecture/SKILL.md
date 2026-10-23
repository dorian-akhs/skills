---
name: to-architecture
description: Discuss and agree on architecture before implementation. Use between requirements discovery and to-spec, or to resolve architectural choices in an existing spec or ticket, with a concrete proposal, trade-offs, and user-owned decisions.
---

# To Architecture

Help the user understand, challenge, and choose the architecture before it becomes code. The agent investigates and recommends; the user owns consequential design decisions. This is a discussion and decision workflow. Do not start implementation or treat agreement on architecture as permission to build.

## Establish the context

Work from the current conversation or the supplied spec, ticket, or design question. Read referenced requirements, relevant project instructions, existing decisions, and the affected code and tests. Investigate facts yourself. Distinguish observed constraints from assumptions and preferences.

If behavior or scope is too unclear to evaluate designs, ask the specific questions that block the architecture discussion. If no codebase is available, state that limitation and base proposals on the supplied context without inventing existing modules or conventions.

Identify decisions already agreed and decisions still open. Respect the former unless new evidence warrants reopening them. Prefer fitting the existing architecture and keeping the change small; explain when a new structure earns its cost.

## Propose a design the user can assess

Lead with a recommendation, grounded in the actual feature and codebase. Explain:

- Which modules change or are introduced, what each owns, and what complexity it hides.
- Their interfaces: what callers need to know, including relevant invariants and failure behavior.
- Where state lives, who may change it, and which external dependencies are involved.
- One concrete end-to-end scenario through the proposed design, including the relevant failure path.
- Where tests exercise behavior and what evidence they provide.

Scale the explanation to the change. Use a small sketch, example interface, or diagram when it makes a decision easier to understand. Explain technical terms in context. A folder tree alone does not explain the architecture.

For consequential open choices, compare credible alternatives and recommend one with reasons. Explain the practical trade-offs, the cost of changing course, and what each option makes easier or harder. Do not manufacture alternatives for settled conventions or trivial implementation details. If the existing design already fits, say why.

## Discuss and agree

Separate consequential choices requiring the user's decision from routine details you recommend leaving to the implementer. Typical consequential choices include responsibility placement, shared interfaces, state ownership, persistence, dependency selection, and execution or failure handling when these materially affect the feature.

Present the proposal before asking the user to decide. Ask concrete questions about choices they can evaluate, with your recommendation. Wait for their answers; do not answer for them or interpret silence as agreement. Resolve prerequisite decisions before asking about dependent ones. Revise the proposal as the discussion develops.

If a consequential uncertainty needs evidence, propose a bounded investigation or prototype and explain which decision its result would resolve. Do not disguise an untested assumption as a settled choice.

Before closing, summarize the agreed design, its reasons, remaining delegated details, and any unresolved questions. Obtain explicit agreement on that summary. Do not declare the architecture ready while consequential choices remain unresolved.

## Preserve the agreement for implementation

After agreement, capture it in the existing spec's Implementation Decisions section or the project's established architecture document. Follow local writing and approval rules; if no destination is established, propose one before writing. Preserve unrelated content and do not create a new documentation hierarchy by default.

Record the chosen approach, the reasons and meaningful alternatives, affected responsibilities and interfaces, state ownership, test strategy, and the details left to the implementer. Use an ADR only for a decision that is costly to reverse, surprising without context, and the result of a real trade-off. Keep implementation decisions out of a domain glossary.

Carry these constraints into the implementation handoff:

- Link the agreed architecture and relevant decisions from the spec and tickets so a fresh implementation session can find them.
- The implementer may decide routine details within those constraints.
- If new evidence requires changing an agreed consequential decision, explain the evidence, proposed revision, and trade-offs, then wait for the user's decision before making that change. Independent work may continue.

Recommend the next step without invoking it automatically: usually `/to-spec`, then `/to-tickets` where needed, or a return to implementation when explicitly authorized. These commands are optional workflow integrations, not prerequisites for using this skill.
