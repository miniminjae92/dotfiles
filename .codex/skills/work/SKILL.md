---
name: work
description: "Use when the user explicitly invokes $work or asks to use the full coding workflow for a non-trivial implementation task. This skill enforces a structured cycle: clarify requirements, plan, test, implement, verify, summarize diff, and propose a commit message."
---

# Work Workflow

Use this skill only when the user explicitly invokes `$work` or asks for the full coding workflow.

## Workflow

1. Read applicable `AGENTS.md` guidance.
2. Read the task file when the user provides one, usually `.codex/work/TASK.md`.
3. Read the decisions file when present, usually `.codex/work/DECISIONS.md`.
4. Find related files in the current codebase.
5. Do not edit immediately. First propose a minimal work plan.
6. Wait for user approval before implementing when the user requested plan-first behavior or the task file asks for approval.
7. Add or update tests when the behavior can be tested.
8. Implement the approved change.
9. Run the relevant tests.
10. If a design decision was made, record it in the decisions file.
11. Summarize changed files and why they changed.
12. Summarize the final result from `git diff`.
13. Suggest a commit message.

## Rules

- Keep the plan concise and tied to verification.
- If the user asks to plan first, or the task file says to wait for approval, stop after the plan until they ask to implement.
- For bug fixes, reproduce the issue with a failing test first when practical.
- For features, add tests for the new behavior when practical.
- For refactors, verify relevant tests before and after when practical.
- If tests cannot be run, explain why and state what was checked instead.
- Keep changes surgical: do not clean up adjacent code unless the task requires it.
- Use `DECISIONS.md` only for meaningful design choices, tradeoffs, or constraints. Do not log routine implementation steps.
- Suggest the final commit message using the configured commit-message convention.
- When suggesting a commit message, read `~/.config/commit-message-conventions/korean-angularjs.md` when available.
