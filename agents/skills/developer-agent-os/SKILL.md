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
4. Delegate to the `worker` role (Codex: `fast_worker` agent; Claude: a low-effort subagent) only for independent bounded work that saves more context than delegation consumes.
5. Use the `reviewer` role (Codex: `critical_reviewer` agent; Claude: a context-free review subagent) only for consequential architecture, security, data-loss risk, difficult regressions, or final independent review. Roles are declared in `~/.dotfiles/agents/routing.json`.
6. For learning-heavy or consequential work, select the user's required understanding with the Tutor rules below. Do not pause reversible implementation for lessons; teach at a consequential decision gate or after the work is complete.
7. Retrieve only notes relevant to the current project, concept, or decision. Never load the whole vault or treat `candidate` and `inferred` notes as verified facts.

## Tutor

- Base the learning scope on the decisions the user owns, the result they must validate, and the failure they must absorb. Job titles such as CEO, CTO, or developer are explanatory lenses, not the scope rule.
- Choose the smallest sufficient target depth:
  - `L0`: recognize the terms and overall map.
  - `L1`: explain the operating mechanism.
  - `L2`: compare options and tradeoffs.
  - `L3`: validate the result and explain failure and recovery.
  - `L4`: implement and debug directly.
- Increase required depth with user ownership, failure impact, and irreversibility. Delegated execution normally requires decision-grade understanding, not every implementation detail; deepen it when the user must approve the work without another qualified reviewer.
- Keep three learning lanes distinct:
  - `required`: needed now for a decision, validation, risk, or recovery.
  - `strategic`: recurring or transferable knowledge worth learning later.
  - `curiosity`: optional depth the user wants when time permits.
- Keep the delivery lane moving. Explain only the required depth during the task, and preserve strategic and curiosity topics as follow-up candidates rather than forcing a lesson.
- When the user explicitly asks to study, use the learning lane and go deeper than the immediate project risk requires.

## Record

- For T1/T2, create a candidate Run from `/Users/miniminjae/.obsidian/developer-os/_System/Templates/Run.md` under `40 Reviews/Runs/`.
- When Tutor mode applies, record the user's responsibility, target depth, selection reason, delegated details, and required, strategic, or curiosity follow-up candidates in the Run. Use only `pending`, `passed`, `needs_review`, or `not_required` for `understanding_status`.
- Run `agent-os-usage` and record only observable model, reasoning, and token data. Keep ChatGPT credits and API cost separate; never infer one from token counts.
- Preserve origin: user statements are `user`, agent output is `agent`, jointly confirmed decisions are `joint`, and unconfirmed inferences are `inferred`.
- When the user reports friction, run `agent-os-friction --origin user "..."`. Use `--origin agent` only for agent-observed friction.
- Run `agent-os-review-due` after creating a Run. If it reports due, read unreviewed Runs and friction, create one Review, and propose at most one reversible improvement experiment.
- During a monthly Review, inspect `/Users/miniminjae/.dotfiles/agent-os/ASSET-AUDIT.md`; mark unused assets as candidates but never delete them automatically.

## Finish

Report the result, verification, important decisions, rollback, observed usage, and unresolved risks. Teach only to the selected depth. For `L3` or `L4`, or another explicit learning gate, ask the user to explain the decision, validation, and recovery path in their own words; correct gaps afterward.
