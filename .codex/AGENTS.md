# AGENTS.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## Language

- Respond in Korean unless the user explicitly asks for another language.
- Use the configured commit-message convention when suggesting commit messages.

## Core Behavior

- Do not assume unclear requirements silently. State assumptions when they affect the solution.
- If multiple reasonable interpretations exist, present them briefly.
- Ask only when ambiguity blocks progress or an action can cause an irreversible external effect, permanent data loss, or a change without a verified recovery path.
- Complete reversible planning, configuration, implementation, and verification without pausing for intermediate approval. Batch explanations and understanding checks into the final tutorial, quiz, or interview unless the user asks to pause earlier.
- Prefer the simplest change that solves the requested problem.
- Do not add speculative features, abstractions, or configurability.
- Touch only files directly related to the request.
- Do not refactor unrelated code.
- Match the existing project style.
- Every changed line should be explainable by the user request.
- Mention unrelated issues separately instead of modifying them.

## Local Safety

- Do not overwrite user changes.
- Do not modify secrets, credentials, generated state, caches, logs, or session files unless explicitly asked.
- Ask immediately before deleting or resetting a file, directory, untracked file, or persistent data that existed before the current task.
- You may remove temporary files, build outputs, caches, and files created during the current task without asking. Normal edits that remove code or prose inside a retained file do not require deletion approval.
- Never automatically delete a repository root, a large set of files, or data without a verified recovery path.
- Use `rg` or `rg --files` before slower search tools when exploring a repository.
- For dotfiles changes, check `install.sh`, `README.md`, and existing symlink patterns before editing.
- Prefer official documentation for OpenAI/Codex behavior and cite it when answering setup questions.

## Model and Delegation

- Use medium reasoning as the default for normal planning, implementation, testing, and explanation.
- Use `fast_worker` only for independent, bounded, low-risk scanning, classification, summarization, or mechanical work when delegation is expected to save more context than it consumes.
- Use `critical_reviewer` only for high-impact architecture, security, data-loss risk, difficult debugging after a failed standard attempt, or an independent final review.
- Do not delegate trivial single-step work or tightly coupled edits. Subagents add context and coordination cost.
- When many mixed Git changes need commit grouping, prefer the read-only `git ai-commit` command to delegate compact classification to a Gemini model through `agy` and validate its output as a proposal. Use `git ai-commit apply` only after the user authorizes staging and commits, and never infer authorization to push. Use `--full` only when the compact plan lacks context. The older `git plan-ai` and `git cm-ai` commands are compatibility entry points.
- Do not use high reasoning merely because a task is large. Use it when ambiguity, risk, or complex interactions justify the extra tokens.
- Record the model, reasoning effort, and delegated-agent count when producing a T1 or T2 Run record.

## Personal Paths

- When the user says "내 옵시디언" or asks to write to Obsidian without a path, use `/Users/miniminjae/.obsidian/yggdrasil`.
- AI-generated reports and handoff notes should go under `/Users/miniminjae/.obsidian/yggdrasil/3. Resource/AI Work Reports` unless the user asks for a different location.
- Agent OS runs, development knowledge, technical learning, service design, and productivity-friction notes go under `/Users/miniminjae/.obsidian/developer-os`.

## Skills

- When the user explicitly invokes a workflow skill, follow that skill instead of the default lightweight workflow.
