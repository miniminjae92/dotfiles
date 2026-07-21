# AGENTS.md

Provider-neutral instructions shared by every agent CLI (Codex, Claude, Gemini).
Only always-true guidance lives here; conditional workflows belong in skills.
Hard cap: 50 lines (D-008). If an addition exceeds it, move something to a skill.

## Language

- Respond in Korean unless the user explicitly asks for another language.
- Use the configured commit-message convention when suggesting commit messages.

## Core Behavior

- Do not assume unclear requirements silently. State assumptions when they affect the solution.
- If multiple reasonable interpretations exist, present them briefly.
- Ask only when ambiguity blocks progress or an action risks an irreversible external effect or data loss without a verified recovery path.
- Complete reversible planning, implementation, and verification without pausing for intermediate approval; batch explanations into the final summary.
- Prefer the simplest change that solves the requested problem. Do not add speculative features, abstractions, or configurability.
- Touch only files related to the request, do not refactor unrelated code, and match the existing project style.
- Mention unrelated issues separately instead of modifying them.

## Local Safety

- Do not overwrite user changes. Do not modify secrets, credentials, generated state, caches, logs, or session files unless explicitly asked.
- Ask immediately before deleting or resetting a pre-existing file, directory, untracked file, or persistent data. Temporary files created during the current task may be removed without asking.
- Never automatically delete a repository root, a large set of files, or data without a verified recovery path.
- Use `rg` or `rg --files` before slower search tools when exploring a repository.
- For dotfiles changes, check `install.sh`, `README.md`, and existing symlink patterns before editing.

## Roles and Delegation

- Model and account routing follows the logical roles in `~/.dotfiles/agents/routing.json` (planner/worker/reviewer/clerk).
- Keep tightly coupled edits and continuous design judgment in one session. Context severance, not model switching, is what breaks accuracy.
- Delegate only independent, bounded, low-risk subtasks (worker) or deliberately context-free final verification (reviewer). Do not delegate trivial single-step work or tightly coupled edits.
- When many mixed Git changes need commit grouping, prefer the read-only `git ai-commit` command and validate its output as a proposal. Never infer authorization to push.
- Escalation means reclassifying a task to a higher role after failure, not swapping models. When it happens, log it: `agent-os-friction --origin agent "escalation: <from>→<to> | <task> | <reason>"` (D-010).

## Personal Paths

- When the user says "내 옵시디언" or asks to write to Obsidian without a path, use `/Users/miniminjae/.obsidian/yggdrasil`. AI-generated reports go under `3. Resource/AI Work Reports` there.
- Agent OS runs, development knowledge, technical learning, service design, and productivity-friction notes go under `/Users/miniminjae/.obsidian/developer-os`.

## Skills

- When the user explicitly invokes a workflow skill, follow that skill instead of the default lightweight workflow.
