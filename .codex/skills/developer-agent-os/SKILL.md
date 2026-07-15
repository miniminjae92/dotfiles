---
name: developer-agent-os
description: "Use for non-trivial developer work (T1/T2) involving problem definition, architecture, implementation, review, technical learning, service or product design, or an unfamiliar domain when autonomous execution, measured cost, and durable records are needed. Do not use for trivial T0 answers or commands unless explicitly invoked."
---

# Developer Agent OS

Complete the work without intermediate approval when changes are reversible. Ask only before permanent data loss, irreversible external effects, or changes without a verified recovery path.

## Execute

1. Classify the task:
   - `T0`: one answer, command, or tiny edit. Work directly; create no Run unless there is a failure, decision, insight, or friction.
   - `T1`: bounded implementation, review, document, or learning task. Use the full workflow and create a concise Run.
   - `T2`: multi-module, ambiguous, unfamiliar, or high-risk work. Define explicit success, budget, stop conditions, and rollback before execution.
2. Use Architect mode only as much as needed. Establish the problem, goal, facts, assumptions, unknowns, options, decision, risks, validation, and rollback.
3. Use Builder mode to inspect, implement, test, and verify. Keep changes scoped and reversible.
4. Use `fast_worker` only for independent bounded work that saves more context than delegation consumes.
5. Use `critical_reviewer` only for consequential architecture, security, data-loss risk, difficult regressions, or final independent review.
6. Use Tutor mode at the end of learning-heavy or consequential work. Explain the core decision and defer quizzes or interview questions until implementation is complete.
7. Retrieve only notes relevant to the current project, concept, or decision. Never load the whole vault or treat `candidate` and `inferred` notes as verified facts.

## Record

- For T1/T2, create a candidate Run from `/Users/miniminjae/.obsidian/developer-os/_System/Templates/Run.md` under `40 Reviews/Runs/`.
- Run `agent-os-usage` and record only observable model, reasoning, and token data. Keep ChatGPT credits and API cost separate; never infer one from token counts.
- Preserve origin: user statements are `user`, agent output is `agent`, jointly confirmed decisions are `joint`, and unconfirmed inferences are `inferred`.
- When the user reports friction, run `agent-os-friction --origin user "..."`. Use `--origin agent` only for agent-observed friction.
- Run `agent-os-review-due` after creating a Run. If it reports due, read unreviewed Runs and friction, create one Review, and propose at most one reversible improvement experiment.
- During a monthly Review, inspect `/Users/miniminjae/.dotfiles/agent-os/ASSET-AUDIT.md`; mark unused assets as candidates but never delete them automatically.

## Finish

Report the result, verification, important decisions, rollback, observed usage, and unresolved risks. For the final tutorial or a learning gate, ask the user to explain the decision and recovery path in their own words; correct gaps afterward.
