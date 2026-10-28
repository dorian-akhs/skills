---
name: knowledge-navigation
description: Improve discovery and exploration of Markdown, Obsidian, Notion, or Outline knowledge bases through meaningful links, entry pages, indexes, aliases, and reading paths. Use for hard-to-find notes, disconnected topics, confusing page hierarchies, or human and agent navigation. Content deduplication and substantive rewrites belong to knowledge-consolidation.
---

# Knowledge Navigation

Help a reader find the right page, understand its role, and follow the next useful connection without loading the whole base. Preserve the existing organization unless changing it is part of the request. Basic Memory is not required.

## Establish the boundary

- Resolve the requested folder, project, collection, page subtree, or note set and applicable local instructions. Ask when materially different scopes remain plausible.
- Identify current entry pages, indexes, aliases, folder or page hierarchy, and metadata conventions before proposing additions. Search the base for access instructions and relationships before using external services.
- Start from titles, metadata, headings, and current indexes. Read enough of both pages to justify a proposed relationship; read every page to be edited in full. Paginate remote listings and disclose incomplete coverage.
- Use available filesystem, CLI, connector, or MCP tools. Do not install dependencies, migrate platforms, mirror private content, or infer live write access from an export.

## Diagnose actual retrieval problems

Choose a few questions representative of the requested scope, for example:

- Where should someone new to this project start?
- Where is the current reference for a specific rule or decision?
- How can a reader find the supporting evidence or a related alternative?

Follow the existing routes before changing them. Identify misleading entry pages, buried authoritative pages, ambiguous titles, unlinked but useful notes, obsolete destinations, and indexes that duplicate one another.

Do not treat every unlinked note as a defect. Logs, primary records, and intentional drafts can remain outside the main reading path. In Obsidian, links to not-yet-created notes may be intentional: distinguish them from regressions introduced by an edit. Do not create empty pages to make a link checker pass.

## Prefer the smallest useful navigation change

| Need | Preferred change |
|---|---|
| Unclear starting point | Improve an existing entry page with scope, current references, and suggested next steps. |
| Useful connection missing | Add a contextual link explaining the relationship, rather than a generic list of related pages. |
| Concept has several names | Reuse existing titles and aliases; preserve natural wording with display text. |
| Topic spans several pages | Add or update a focused index with brief descriptions of each page's role. |
| Too much context needed to choose a page | Add concise orientation or a descriptive index entry; link to detail instead of copying it. |
| Hierarchy prevents discovery | Propose a scoped move or rename only after checking inbound links and child pages. |

Use meaningful concepts, tools, methods, and entities as link targets, including future concepts when that matches the base's conventions. Link the first useful occurrence in a substantial section rather than every repetition. Shared keywords alone do not establish a useful relationship. Preserve local tag vocabulary; a navigation request does not authorize taxonomy redesign.

Keep indexes primarily about discovery: short scope descriptions and links to maintained reference pages. Do not copy mutable rules into several indexes. Different readers may warrant different routes through the same pages, without duplicating those pages. Avoid arbitrary depth, page-count, or link-density targets.

## Propose or apply according to the request

For an audit, report findings without writing pages, plans, logs, or metadata. For a vague organization request, propose a scoped change first. For explicit edits or an approved plan, proceed within the authorization already given and any stricter local rules; do not ask for the same permission again.

Before bulk changes or restructuring, show the affected pages, proposed entry routes or hierarchy, moves and renames, and how old links will remain usable. Include proposed wording for new orientation text or a short rewrite. Ask for missing scope or removal authorization only where it matters. Installing this skill authorizes no knowledge-base edits.

When applying:

1. Inspect Git state or remote revisions. Preserve unrelated work and re-read pages changed concurrently; use conditional edits when available.
2. Make targeted additions or edits. Preserve metadata, existing language, page IDs, properties, child pages, attachments, permissions, and blocks outside the edit. If tools cannot preserve them, narrow the operation or prepare a proposal.
3. Resolve links using actual paths or remote IDs. Check aliases, relative links, heading and block anchors, embeds, and inbound references affected by moves or renames. Do not silently rewrite pages outside the write scope; report required follow-up or obtain authorization.
4. Read back the saved pages and follow the representative routes again. Check that each route reaches its intended reference and that orientation text accurately describes it.
5. Follow local logging, commit, and synchronization rules, isolating this iteration's changes.

## Keep the content boundary clear

This skill owns discovery, entry pages, contextual links, aliases, and navigation structure. Small scope descriptions are within its remit. Consolidating claims, deciding semantic duplicates, splitting substantive content, and resolving contradictory guidance belong to `knowledge-consolidation`.

If both kinds of work were requested and that skill is available, consolidate content first, then use its updated reference locations and old-to-new path or anchor map. A navigation-only request does not authorize merging or rewriting substantive notes. If the other skill is unavailable, finish authorized navigation work and report content findings without making them a dependency.

## Report

Provide the resulting entry points, useful reading routes, changed pages, and verification performed. Distinguish confirmed broken links from intentional future links and unverified destinations. State coverage gaps and pending content issues. Do not claim improved retrieval merely because more links were added; describe which previously difficult route now works.
