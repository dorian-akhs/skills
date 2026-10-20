---
name: knowledge-maintenance
description: Coordinate knowledge-consolidation followed by knowledge-navigation on a chosen Markdown, Obsidian, Notion, or Outline scope. Use for combined knowledge-base cleanup, reducing repetition and improving discovery in one workflow. Ordinary searches or requests for only one specialty do not need this coordinator.
---

# Knowledge Maintenance

Provide one entry point for maintaining both content and navigation. Reuse the two specialist skills rather than duplicating their methods. Run their phases sequentially in the current session; separate agents are not required or authorized by this skill.

## Resolve the request once

1. Locate and read the installed `knowledge-consolidation` and `knowledge-navigation` skills using the available skill catalog or sibling skill directories. Both are required for the complete workflow. If either is unavailable, report the missing dependency before mutations; do not silently install it or claim a complete run.
2. Resolve a single write scope: folder, note set, project, collection, or page subtree. Reuse the user's stated perimeter; ask only when materially different interpretations remain. Read applicable local instructions and discover existing entry points, references, and access tools.
3. Establish whether the request is an audit, a proposal, or authorized implementation. Preserve authorization already given. A bare invocation or vague cleanup request starts with a proposal; an audit remains read-only, including plans, logs, and metadata. Creating this skill authorizes no knowledge-base edits.

## Build one combined plan

Use both specialists to inspect the same scope. Share the inventory, source evidence, coverage gaps, and existing navigation routes rather than restarting discovery for each phase. Read pages to be changed in full, as the specialists require.

Present a compact plan connecting each content change to its navigation consequences:

| Affected pages | Content consolidation | Navigation adjustment | Information and links to preserve |
|---|---|---|---|

Include proposed wording or representative before/after passages as required by the scope and local rules. Distinguish confirmed duplicates from complementary notes and unresolved contradictions. Identify any required inbound-link edits outside the write scope without silently including them.

For an audit or proposal, stop after the combined findings and next steps without writing to the base. For implementation, obtain only authorization that is still missing, including any local requirement before restructuring or removal. Approval of the combined plan covers both phases; do not request it again merely because navigation begins. A materially new change requires its own scope or authorization check.

## Phase 1: Consolidate content

Apply `knowledge-consolidation` within the agreed scope and authorization. It owns substantive rewrites, duplicate decisions, consolidation, and any approved splits or merges. Preserve its safeguards for evidence, primary records, information coverage, revisions, and affected links.

Keep orchestration here: the specialist's suggestion to run navigation is a handoff to Phase 2, not an additional nested run. Capture the resulting reference locations, changed page IDs or paths, old-to-new headings and anchors, preserved source locations, and unresolved findings. Validate the saved content before routing readers to it.

## Phase 2: Improve navigation

Apply `knowledge-navigation` to the current saved state, using Phase 1's handoff. Update entry pages, contextual links, indexes, aliases, and approved hierarchy changes so they lead to the consolidated references. Avoid copying mutable claims back into indexes.

This phase must not trigger another consolidation pass. If it uncovers a material content issue, leave that issue pending or propose a focused amendment instead of creating an unbounded loop. Do not redo work that Phase 1 already completed, including necessary link repairs.

If a content change is blocked or declined, improve independent navigation only where existing verified destinations remain valid. Do not route links toward a proposed page or present unresolved guidance as settled. Report the overall run as partial when required work remains.

## Verify and report together

- Confirm preservation of distinct claims, sources, meaningful qualifications, and structured artifacts affected by the content changes.
- Follow representative reading routes from entry points to current references and their evidence. Check links and anchors changed by either phase; distinguish intentional future links from introduced breakage.
- Respect the workspace's logging, commit, and synchronization rules for each write iteration. Combine the final user-facing report, even when local rules require separate commits or logs along the way.
- Report coverage, content changes, resulting entry points and reading paths, verification, and remaining questions. Separate proposed, applied, skipped, and blocked actions. Do not claim completion based only on shorter text or more links.
