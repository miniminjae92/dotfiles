---
name: archive-session
description: "Use when the user explicitly invokes $archive-session or asks to archive a saved CLI agent conversation into reusable documentation assets. This skill runs the raw extraction, keyword extraction, structure composition, and source refinement workflow."
---

# Archive Session

Use this skill to turn a saved CLI agent conversation into documentation assets.

## Inputs

- Source conversation file, usually `docs/conversation/YYYY-MM-DD-*-session.md`.
- Output directory, usually `docs/conversation`.

## Outputs

- `docs/conversation/raw.md`
- `docs/conversation/keywords.md`
- `docs/conversation/structured.md`
- `docs/conversation/final-notes.md`

## Workflow

1. Read the source conversation file.
2. Create or update `raw.md`:
   - Extract meaningful sentences.
   - Remove duplicates.
   - Keep useful conversational intent.
   - Separate confirmed notes and open questions.
3. Create or update `keywords.md`:
   - Extract core concepts.
   - Extract technical keywords.
   - Extract document and artifact names.
   - Suggest searchable tags.
4. Create or update `structured.md`:
   - Reorder ideas into a logical sequence.
   - Use problem, concerns, options, decisions, gaps, and next actions.
5. Create or update `final-notes.md`:
   - Produce candidates for durable documents such as `DECISIONS.md`, `AGENTS.md`, `TASK.md`, `BLOG.md`, or future skills.
6. Summarize generated files and the most important reusable outputs.

## Rules

- Treat the transcript as raw source material, not as a finished document.
- Do not preserve sensitive secrets, tokens, credentials, or private personal details in derived outputs.
- Do not invent decisions. Mark uncertain items as gaps or open questions.
- Prefer concise bullets over long prose unless the output is a final candidate paragraph.
- Keep file paths stable unless the user asks for a different output directory.
