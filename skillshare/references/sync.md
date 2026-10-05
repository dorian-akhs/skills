# Sync, Collect, Push & Pull

| Command | Direction | Project? |
|---------|-----------|:--------:|
| `sync` | Source → Targets | ✓ (auto) |
| `collect` | Targets → Source | ✓ (auto) |
| `push` | Source → Remote | ✗ |
| `pull` | Remote → Source → Targets | ✗ |

**Auto-detection:** `sync` and `collect` auto-detect project mode when `.skillshare/config.yaml` exists. Use `-g` to force global.

## sync

Distribute skills from source to all targets using each target's sync mode (`merge` / `copy` / `symlink`).

```bash
skillshare sync                # Execute (auto-detects mode)
skillshare sync --all          # Sync skills + extras
skillshare sync --dry-run      # Preview
skillshare sync --force        # Override conflicts
skillshare sync --json         # JSON output
skillshare sync -g             # Force global mode
```

### Sync modes (quick reference)

- `merge` (default): per-skill symlinks, preserves local target skills.
- `copy`: real-file copies with `.skillshare-manifest.json` tracking managed entries.
- `symlink`: whole target directory symlinked to source.

Copy mode note:
- `skillshare doctor` duplicate checks ignore manifest-managed copy entries (expected mirrors of source).
- Duplicate warnings in copy mode are for true local copies that collide with source skill names.

## sync extras

Sync non-skill resources (rules, commands, prompts) to arbitrary directories. Supports both global and project mode.

```bash
skillshare sync extras            # Sync all configured extras
skillshare sync extras --dry-run  # Preview
skillshare sync extras --force    # Overwrite conflicts
```

Config example:
```yaml
extras:
  - name: rules
    targets:
      - path: ~/.claude/rules
      - path: ~/.cursor/rules
        mode: copy
```

Source: `~/.config/skillshare/extras/<name>/` (global) or `.skillshare/extras/<name>/` (project). Modes: `merge` (default, per-file symlinks), `copy`, `symlink`.

For full extras management (`init`, `list`, `remove`, `collect`), see [extras.md](extras.md).

## collect

Import skills or agents from target(s) to source.

```bash
# Global
skillshare collect claude      # From specific target
skillshare collect --all       # From all targets
skillshare collect --dry-run   # Preview
skillshare collect claude --json   # JSON output; existing items still require --force to overwrite
skillshare collect agents claude   # Collect agents instead of skills

# Project (auto-detected or -p)
skillshare collect claude     # From project target
skillshare collect --all           # All project targets
skillshare collect --all --force   # Skip confirmation
skillshare collect -p --json       # Project JSON output
skillshare collect -p agents --json   # Project agent JSON output
```

## push

Git commit and push source to remote. **Global mode only.**

```bash
skillshare push                # Default message
skillshare push -m "message"   # Custom message
skillshare push --dry-run      # Preview
```

**Project mode:** Use `git push` directly on the project repo.

### Automatic completion after skill changes

The user has authorized automatic syncing and pushing of global skillshare skill changes as a standing workflow. Creating, editing, renaming, installing, updating, or removing a skill is not complete at local sync: validate the affected files, sync to configured targets, commit with a concise message, and push to the configured remote in the same task. This includes edits to these skillshare instructions. Do not ask the user to repeat the push request. An explicit request to keep changes local overrides this default.

Use `skillshare push -m "message"` when the source working tree contains only the intended changes. It stages and commits source changes automatically; if unrelated user edits are present, commit only the intended paths through Git and push the configured branch without staging the unrelated work. Inspect actual output and the remote state: a zero exit code alone does not establish that the skillshare wrapper pushed successfully.

If the remote has newer commits, fetch and integrate them while preserving both sides. Resolve every conflict before invoking `skillshare push` again: the wrapper can stage conflict markers and commit them. Check the Git conflict state, `git diff --check`, and parse modified JSON/YAML metadata before retrying. Do not force-push or discard another machine's skills. If a required check or integration fails, complete unaffected work and report the concrete blocker instead of claiming the push succeeded.

Verify that the intended commit reached the remote and report the push outcome. If remote integration changes skill content, sync the resulting source again after validation. Read-only operations such as searches and status checks do not create a new commit or push by themselves. This preference concerns the global skills repository; it does not authorize pushing unrelated application repositories.

## pull

Git pull from remote and sync to all targets. **Global mode only.**

```bash
skillshare pull                # Pull + sync
skillshare pull --dry-run      # Preview
```

**Project mode:** Use `git pull` directly, then `skillshare sync`.

## Common Workflows

**Local editing:** Edit skill anywhere → `sync` (symlinks update source automatically)

**Import local changes:** `collect <target>` → `sync`

**Cross-machine sync (global):** Machine A: `push` → Machine B: `pull`

**Team sharing (project):** Edit `.skillshare/skills/` → `git commit && git push` → Team: `git pull && skillshare install -p && skillshare sync`
