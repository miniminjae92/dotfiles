---
name: handoff-session
description: "Use when the user explicitly invokes $handoff-session or asks to create a concise Markdown handoff from the current conversation so a future agent session (any CLI, any machine) can continue the work without reading the raw session log."
---

# Handoff Session

Use this skill to create a compact handoff note for the next agent session.

## Goal

Write a Markdown file that lets a future agent session recover the current work context quickly:

- what the user is trying to accomplish
- what has already been decided
- what files changed or matter
- what commands were run and their results
- what remains to do next

This is not a full transcript archive. Prefer actionable continuity over completeness.

## Default Output

Create or update:

- `docs/conversation/handoff.md` when working inside a project repository
- `.codex/work/HANDOFF.md` when the project already uses `.codex/work`
- otherwise ask the user for a destination

If the user provides a path, use that path.

## Workflow

1. Read project guidance such as `AGENTS.md` when present.
2. Inspect `git status --short` to separate committed state, current edits, and untracked files.
3. Inspect relevant diffs with `git diff --stat` and focused `git diff -- <path>` only when needed.
4. Use the current conversation context as the primary source.
5. Write the handoff note with the template below.
6. Do not include secrets, credentials, auth tokens, private URLs, or raw logs unless the user explicitly asks and it is safe.
7. Keep the file concise enough for the next session to read before acting.

## Template

```markdown
# Agent Handoff

## Context

- Date:
- Repository:
- Branch:
- User goal:

## Current State

- What is already done:
- What is intentionally not changed:
- Important assumptions:

## Key Decisions

- Decision:
  Reason:
- Decision:
  Reason:

## Files To Read First

- `path`: why it matters
- `path`: why it matters

## Work In Progress

- Changed files:
- Untracked files:
- Known dirty state that should not be reverted:

## Verification

- Command:
  Result:
- Command:
  Result:

## Next Steps

1. ...
2. ...
3. ...

## Watch Outs

- ...
```

## Rules

- Do not invent completed work. Mark uncertain items as `확인 필요`.
- Preserve user intent and vocabulary when it affects future decisions.
- Prefer bullets over prose.
- Include exact file paths and command names.
- Include failed commands when they explain the current state.
- If the handoff concerns code, mention whether tests were run.
- If tests were not run, say why.
- Do not dump the full conversation or raw session JSON.
