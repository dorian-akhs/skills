---
name: knowledge-consolidation
description: Clarify and consolidate knowledge-base content in Markdown, Obsidian, Notion, or Outline. Use for redundant passages, overlapping notes, scattered facts, bloated pages, contradictions, or outdated guidance. Preserve sources and meaningful distinctions. Link, index, and discovery work belongs to knowledge-navigation.
---

# Knowledge Consolidation

Give each maintained claim a clear reference location, with concise prose and enough context to remain useful. Optimize comprehension and maintenance, not minimum word count. Work with the user's existing system; Basic Memory is not required.

## Establish the boundary

- Resolve the requested folder, project, collection, page subtree, or explicit note set. Ask if materially different scopes remain plausible. A topic request permits finding related notes, not rewriting the entire workspace.
- Read applicable repository and workspace instructions. Distinguish primary records (meeting notes, transcripts, captures) from maintained reference pages, summaries, and navigation pages.
- Use the current base to find relationships and access instructions before searching external systems. Follow links outside the write scope only as needed for evidence or impact analysis; do not silently expand the write scope.
- Discover titles, aliases, metadata, and headings first. Read candidate pages in full before changing them. Paginate listings and searches, and report inaccessible pages or incomplete coverage.
- Reuse available filesystem, CLI, connector, or MCP tools. An export alone does not provide write access to its source service. Do not install connectors, migrate a base, or mirror private material elsewhere as part of curation.

## Distinguish the problems

| Finding | Appropriate response |
|---|---|
| Repeated wording within a page | State the claim once; preserve exceptions and useful examples. |
| Same maintained claim copied across pages | Choose a reference location and replace copies with short contextual links. |
| Same subject, different purpose | Keep the pages distinct and clarify their scope. A decision record and a tutorial can legitimately overlap. |
| Facts scattered across pages | Integrate them into an existing reference page before proposing another page. |
| Page covers unrelated questions | Propose a split only when separate reading or maintenance warrants it; length alone is insufficient. |
| Claims disagree | Check scope, version, date of validity, and source. Record unresolved disagreement rather than choosing a winner. |
| Guidance may be obsolete | Verify from evidence. An old timestamp or a newly imported file proves neither obsolescence nor truth. |

Compare actual claims, not just title similarity. Distinguish a duplicate from a specialization, historical state, alternate approach, or independent source supporting the same fact. Keep modest repetition when it makes a page understandable on its own.

Choose a reference location by purpose, authority, provenance, and existing use. Prefer enriching the right page over selecting the longest or newest page automatically. Preserve decision rationale, qualifications, uncertainty, dates, versions, numbers, citations, code, commands, formulas, and structured data unless changing them is part of the request.

Do not rewrite primary records into current guidance or erase their historical statements. Put current synthesis in maintained pages and link back to evidence. Mark new inferences as inferences. Do not import external facts merely to make a note look complete; verify them when the task actually calls for an update.

## Propose or apply according to the request

For an audit, return findings without writing notes, plans, logs, or metadata. For a vague cleanup request, show a scoped proposal before mutation. An explicit request to apply edits or an approved plan authorizes the specified work; do not add repeated confirmation gates. Apply stricter local instructions where relevant.

Before a bulk rewrite, split, merge, rename, or move, show a compact plan:

| Pages or passages | Finding | Proposed reference location and change | Information and links to preserve |
|---|---|---|---|

Make the change reviewable: include proposed wording for a short rewrite, or a representative before/after passage and the scope of larger edits. Separate evidence-backed corrections from unresolved questions. Obtain missing authorization for removing information, deleting pages, or expanding scope. A request to create or install this skill authorizes no knowledge-base edits.

When applying:

1. Inspect local Git state or remote revisions before writing. Preserve unrelated work. Re-read a page if its revision changed; use conditional edits or checksums when supported.
2. Change the smallest useful group of pages. Preserve language, existing metadata, aliases, and naming conventions; do not introduce a new schema or taxonomy by default.
3. For consolidation, account for each distinct claim from the affected passages: retained at a named location, preserved in a primary record, or explicitly authorized for removal. A shorter result is insufficient evidence of completeness.
4. Repair links affected by the operation, including heading and block anchors, embeds, backlinks, and remote child-page relationships where relevant. Preserve stable page IDs. Renaming a heading can break links even without moving a page.
5. Keep merged page paths or IDs useful through a clear pointer when possible. Do not assume a redirect property works natively in every application. Do not delete a page without explicit authorization.
6. Read the saved result back. Verify the new reference locations, preserved facts and sources, link destinations, and any structured artifacts actually affected. Follow the workspace's logging, commit, and synchronization rules; stage only this iteration's changes.

For Notion or Outline, use targeted content updates and preserve properties, child pages, attachments, permissions, and embedded blocks outside the edit. If available tooling cannot preserve them, prepare a proposal or narrow the operation instead of overwriting the page wholesale.

## Coordinate with navigation when needed

This skill owns semantic duplicate decisions, text rewrites, splits, and merges. Repairing the links those changes affect is part of completing the operation.

For a request that also asks to improve exploration, use `knowledge-navigation` if available after the reference locations stabilize. Pass the scope, changed titles and IDs, old-to-new paths or anchors, and unresolved findings. No second skill is required for a content-only request. If it is unavailable, complete this skill's work and report any broader navigation work left over.

## Report

State coverage, changes with page links, where consolidated information now lives, unresolved contradictions, and verification performed. Distinguish proposed, applied, and blocked work. Report size reductions only when measured, alongside information preservation; do not equate fewer words with higher quality.
