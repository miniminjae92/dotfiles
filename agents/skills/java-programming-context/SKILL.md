---
name: java-programming-context
description: Use before implementing or changing Java code or tests for this user. Apply the evidence-backed personal Java coding draft alongside the target repository's requirements and code. Skip for prose-only Java questions.
---

# Java programming context

Translate the user's intent into Java using the [personal coding draft](references/personal-java-coding-draft.md). It records observed choices and open preferences, not approved universal rules.

## Before coding

1. Identify the target repository, branch, and worktree. Read its `AGENTS.md`, `CONTEXT.md`, relevant ADRs and requirements when present, then nearby code, tests, and build configuration. A mission repository's `main` may be starter code; inspect the branch that contains the user's implementation.
2. Read the personal coding draft. Identify which decisions this task actually needs, and follow its defaults only where the current repository has no stronger requirement or convention. Name a material preference conflict before committing to a design.
3. Use the [evidence map](references/evidence-map.md) to inspect matching user-authored code, PR replies, and mission notes for those decisions. Read the old Mimir criteria only when the draft does not cover a relevant choice. A dated handoff describes its session, not a current instruction.
4. For a contested design question that benefits from other cohorts' feedback, use the [java-blackjack corpus guide](references/blackjack-prs.md) to inspect a few relevant threads and later code. Other participants' reviews are comparisons, not the user's preferences. Machine-generated candidates remain questions until the user adopts them.
5. Give the current repository's requirements, behavior, and accepted decisions precedence. Implement and run focused verification. Report the draft choices that affected the code and any unresolved preference that materially changed the result.
