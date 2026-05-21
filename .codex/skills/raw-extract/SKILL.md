---
name: raw-extract
description: "Use when the user explicitly invokes $raw-extract or asks to extract useful raw material from a saved CLI agent conversation into a cleaner raw notes file."
---

# Raw Extract

Use this skill to turn a saved CLI conversation transcript into a cleaned raw source note.

## Inputs

- Source conversation file, usually `docs/conversation/YYYY-MM-DD-*-session.md`.
- Output file, usually `docs/conversation/raw.md`.

## Workflow

1. Read the source conversation file.
2. Extract only meaningful user concerns, questions, decisions, constraints, and useful assistant conclusions.
3. Remove obvious duplicates.
4. Preserve some conversational wording when it carries intent.
5. Separate confirmed statements from open questions.
6. Write the output file.

## Output Shape

```markdown
# Raw Source

## User Concerns

- ...

## Confirmed Notes

- ...

## Open Questions

- ...

## Deduplicated Memos

- ...
```
