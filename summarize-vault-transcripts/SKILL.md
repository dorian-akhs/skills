---
name: summarize-vault-transcripts
description: Summarize transcript-based Obsidian source notes in this vault and, when explicitly asked to write, insert a concise French `## Résumé` section before `## Transcript`. Use when the user asks to summarize a transcript note, says "same for" a source note, asks to process notes in `_/Sources/A traiter/resumer/`, or asks for this session's source-note summary behavior.
---

# Summarize Vault Transcripts

## Overview

Produce compact French summaries for transcript notes in the Obsidian vault. The default output is a `## Résumé` section placed immediately before `## Transcript`, preserving the original note content.

## Default Target

When the user does not name a specific note or folder, process Markdown notes in:

```text
_/Sources/A traiter/resumer/
```

If the folder is empty, missing, or contains no Markdown transcript notes, say that clearly and stop.

## Workflow

1. Identify target note(s).
   - If the user links a note, process only that note.
   - If the user names a folder, process Markdown notes in that folder.
   - If no target is given, use the default `resumer` folder.

2. Read only the target note(s).
   - Do not read anything in `4 Journal` unless explicitly asked.
   - Prefer `sed`, `rg`, `find`, and `ls` for inspection.
   - If the transcript is long and tool output truncates, read the missing middle sections before summarizing.

3. Summarize the transcript in French.
   - Keep it under 100 lines unless the user asks otherwise.
   - Focus on the thesis, major arguments, practical recommendations, caveats, and conclusion.
   - Ignore sponsor segments unless they affect the content.
   - Preserve the speaker's attribution, e.g. "Theo explique..." when useful.

4. Write only when explicitly requested.
   - If the user asks to "write it in the note", "same for", "add it", or similar, insert the summary in the note.
   - Otherwise, provide the summary in chat only.

5. Insert the summary immediately before the existing `## Transcript` heading.
   - Use the heading `## Résumé`.
   - Do not change frontmatter, source metadata, embeds, transcript text, or unrelated content.
   - If `## Résumé` already exists, ask before replacing it unless the user clearly asked to update/overwrite.
   - If `## Transcript` is missing, do not guess an insertion point; ask or provide the proposed text in chat.

6. Verify the result.
   - Read the beginning of the note or the modified region.
   - Confirm that `## Résumé` appears before `## Transcript`.
   - Report the changed file path and any skipped files.

## Summary Shape

Use this structure by default:

```markdown
## Résumé

One short paragraph with the overall thesis.

### Idée centrale

Core argument in one or two paragraphs.

### [Topic]

Bullets or short paragraphs for major themes.

### Conclusion

Final takeaway and recommendation.
```

Adapt headings to the transcript content. For comparison videos, use headings for each compared tool or option. For workflow videos, use headings like "Outils", "Gestion du contexte", "Prompting", "Vérification".

## Vault Constraints

This vault is not a code project. Do not create, edit, rename, move, or delete existing notes unless the user explicitly asks. When suggesting improvements beyond the requested summary, show them in chat rather than applying them.
