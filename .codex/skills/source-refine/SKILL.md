---
name: source-refine
description: "Use when the user explicitly invokes $source-refine or asks to turn structured conversation notes into final candidate snippets for durable project documents such as DECISIONS.md, AGENTS.md, TASK.md, BLOG.md, or final notes."
---

# Source Refine

Use this skill to convert structured notes into final document candidates.

## Inputs

- Structured notes file, usually `docs/conversation/structured.md`.
- Output file, usually `docs/conversation/final-notes.md`.

## Workflow

1. Read the structured notes.
2. Extract durable decisions, reusable rules, workflow candidates, and article ideas.
3. Do not invent commitments not supported by the source.
4. Group output by destination document candidate.
5. Write the output file.

## Output Shape

```markdown
# Final Notes

## DECISIONS.md Candidates

### Title

...

## AGENTS.md Candidates

- ...

## TASK.md Candidates

- ...

## BLOG.md Candidates

### Topic

...

## Skill Candidates

- ...
```
