---
name: commit
description: >
  Interactive commit workflow: inspects staged (or unstaged) changes, drafts a
  terse Conventional Commits message, shows it to the user, and commits only
  after explicit confirmation. Trigger when the user types "/commit", "commit
  this", "make a commit", "write a commit", or any phrasing asking to commit
  current changes — with or without extra guidance. Always use this skill
  instead of running git commit directly, even when the user just says "commit".
---

## Workflow

### 1. Inspect changes

Run these in parallel:

```bash
git diff --staged
git status --short
```

If nothing is staged (`git diff --staged` is empty), also run `git diff` to see
unstaged changes and mention to the user that nothing is staged yet.

### 2. Draft the commit message

Follow the caveman-commit rules below. If the user provided additional
instructions (e.g. "/commit fix the auth bug description"), weave them in.

**Never include:**
- ADR references, story IDs, ticket numbers, sprint names, epic names, or any
  project-management identifiers — even if they appear in branch names or file
  paths
- Any git commit trailer or extra author line (~/.claude/CLAUDE.md Git rules)
- "This commit does X", "I", "we", "now", "currently"

### 3. Show and wait

Present the message in a code block, then ask for confirmation. Do not commit
yet. Example:

> Here's the commit message:
>
> ```
> feat(auth): validate token expiry on refresh
>
> Expiry check used `<` instead of `<=`, allowing tokens exactly
> at the boundary to slip through.
> ```
>
> Confirm to commit ("ok", "go", "agreed", "commit", "yes", "do it", "lgtm",
> "looks good", or similar), or tell me what to change.

### 4. Commit on confirmation

When the user confirms, run:

```bash
git commit -m "$(cat <<'EOF'
<subject line>

<body if any>
EOF
)"
```

No `--no-verify`. No force flags. If the hook fails, report the error and stop.

---

## Commit message rules (caveman-commit style)

**Subject line:**
- `<type>(<scope>): <imperative summary>` — scope optional
- Types: `feat`, `fix`, `refactor`, `perf`, `docs`, `test`, `chore`, `build`,
  `ci`, `style`, `revert`
- Imperative mood: "add", "fix", "remove" — not "added", "adds"
- ≤50 chars preferred, hard cap 72
- No trailing period

**Body (only when needed):**
- Only for: non-obvious *why*, breaking changes, migration notes, issue refs
- Skip entirely when subject is self-explanatory
- Wrap at 72 chars, bullets with `-`
- Issue refs at end: `Closes #42`, `Refs #17`

**Always include a body for:** breaking changes, security fixes, data
migrations, reverts — future debuggers need the context.
