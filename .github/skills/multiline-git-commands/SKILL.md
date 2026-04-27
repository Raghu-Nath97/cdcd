---
name: multiline-git-commands
description: >-
  Write multiline git commit messages and pull request descriptions safely.
  USE THIS SKILL when writing a git commit, composing a commit message,
  creating or editing a PR description, or any operation involving
  git commit -m, gh pr create, or gh pr edit with body text.
---

## The Problem (VS Code only)

VS Code's `run_in_terminal` tool serializes commands as JSON strings, which **mangles newlines and quoting**. These patterns ALL produce broken output in VS Code:

```bash
# BROKEN — newlines mangled
git commit -m "feat: add thing

- detail 1
- detail 2"

# BROKEN — heredoc mangled
git commit -m << 'EOF'
...

# BROKEN — python3 -c multiline string mangled
python3 -c "print('line1\nline2')" | git ...
```

This is **not** an issue in Copilot CLI or other terminal-native agents where commands run in a real shell.

## Fix for VS Code: Write to a Temp File via create_file

**Step 1** — Delete any existing temp file, then use `create_file` to write the message:

```bash
# In terminal first (one-liner, safe if file doesn't exist)
rm -f /tmp/commit_msg.txt
```

```
create_file("/tmp/commit_msg.txt", "feat: short summary\n\n- bullet 1\n- bullet 2")
```

> If you skip the `rm` and the file already exists, `create_file` will refuse to overwrite it and you'll be stuck.

**Step 2** — Reference the file in the terminal command:

```bash
# Commit
git commit -F /tmp/commit_msg.txt

# Create PR
gh pr create --title "Title here" --body-file /tmp/pr_body.txt --base main

# Edit existing PR
gh pr edit <number> --body-file /tmp/pr_body.txt
```

## Fix for Copilot CLI: printf one-liner

Copilot CLI runs in a real shell — heredocs work, but the cleanest approach is a single `printf` one-liner so no multiline quoting is needed at all:

```bash
printf 'feat: short summary\n\n- bullet 1\n- bullet 2\n' > /tmp/commit_msg.txt && git commit -F /tmp/commit_msg.txt

# PR body
printf '## Summary\n\nAdds X feature\n\n## Changes\n\n- did this\n- did that\n' > /tmp/pr_body.txt && gh pr edit 123 --body-file /tmp/pr_body.txt
```

Use `\n` inside single quotes with `printf` — this is portable and needs no escaping tricks.

## Quick Reference

| Environment | Tool available | Approach |
|---|---|---|
| VS Code | `create_file` + `run_in_terminal` | `rm -f` temp file → `create_file` → `-F`/`--body-file` |
| Copilot CLI / real shell | terminal only | `printf 'msg\n' > /tmp/file.txt` → `-F`/`--body-file` |

## Rules

- **NEVER** use `git commit -m "..."` with literal newlines inside the string (VS Code)
- **NEVER** use heredocs (`<< 'EOF'`) via VS Code's `run_in_terminal`
- **VS Code**: always `rm -f` the temp file before `create_file` — the tool refuses to overwrite
- **Copilot CLI**: use `printf` one-liner with `\n` escapes
- Temp file path: `/tmp/` prefix, descriptive name (e.g. `commit_msg.txt`, `pr_body.txt`)
