# AGENTS.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## Language

- Respond in Korean unless the user explicitly asks for another language.
- Use the configured commit-message convention when suggesting commit messages.

## Core Behavior

- Do not assume unclear requirements silently. State assumptions when they affect the solution.
- If multiple reasonable interpretations exist, present them briefly.
- Ask only when ambiguity blocks progress or could cause a risky change.
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
- Use `rg` or `rg --files` before slower search tools when exploring a repository.
- For dotfiles changes, check `install.sh`, `README.md`, and existing symlink patterns before editing.
- Prefer official documentation for OpenAI/Codex behavior and cite it when answering setup questions.

## Personal Paths

- When the user says "내 옵시디언" or asks to write to Obsidian without a path, use `/Users/miniminjae/.obsidian/yggdrasil`.
- AI-generated reports and handoff notes should go under `/Users/miniminjae/.obsidian/yggdrasil/3. Resource/AI Work Reports` unless the user asks for a different location.

## Skills

- When the user explicitly invokes a workflow skill, follow that skill instead of the default lightweight workflow.
