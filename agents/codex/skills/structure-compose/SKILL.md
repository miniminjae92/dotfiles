---
name: structure-compose
description: "Use when the user explicitly invokes $structure-compose or asks to reorganize raw notes and keywords into a structured document with problem, concerns, options, decisions, gaps, and next actions."
---

# Structure Compose

Use this skill to turn extracted notes into a logically ordered structured note.

## Inputs

- Raw notes file, usually `docs/conversation/raw.md`.
- Keywords file, usually `docs/conversation/keywords.md`.
- Output file, usually `docs/conversation/structured.md`.

## Workflow

1. Read the raw notes and keywords.
2. Identify the central topic.
3. Reorder scattered ideas into a clear sequence.
4. Use this structure: problem, concerns, options, decisions, gaps, next actions.
5. Mark missing or uncertain parts explicitly.
6. Write the output file.

## Output Shape

```markdown
# Structured Notes

## Central Topic

...

## 1. Problem

...

## 2. Key Concerns

- ...

## 3. Options

### Option

- ...

## 4. Decisions

- ...

## 5. Gaps

- ...

## 6. Next Actions

- ...
```
