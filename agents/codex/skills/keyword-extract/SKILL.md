---
name: keyword-extract
description: "Use when the user explicitly invokes $keyword-extract or asks to extract concepts, technical keywords, document names, and searchable tags from conversation notes."
---

# Keyword Extract

Use this skill to turn raw conversation notes into searchable keywords and tags.

## Inputs

- Source raw notes file, usually `docs/conversation/raw.md`.
- Output file, usually `docs/conversation/keywords.md`.

## Workflow

1. Read the source raw notes.
2. Extract core concepts and define them briefly.
3. Extract technical keywords.
4. Extract document or artifact names.
5. Create suggested tags for later search.
6. Write the output file.

## Output Shape

```markdown
# Keywords

## Core Keywords

- Term: short definition

## Technical Keywords

- ...

## Documents And Artifacts

- ...

## Suggested Tags

- #tag
```
