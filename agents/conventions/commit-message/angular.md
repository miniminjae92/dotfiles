# AngularJS Commit Message Convention

## Someone else's repository wins, but measure it rather than eyeballing it

In a repository you do not own, that repository's existing convention overrides this file.
Determine it by counting, not by reading the last few commits:

```sh
git log --format='%s' -30    # classify the subjects and take the majority
```

A handful of recent commits is not the convention. Two exceptions out of thirty are still
exceptions, and copying one produces a message that matches neither the repo nor this file.
Classify separately per artifact. A repo can use one form for commit subjects and another
for ADR or design-doc titles at the same time, and usually does.

## Shape

Generate commit messages in this shape:

```text
<type>(<scope>): <subject>

<body>

<footer>
```

## Required Rules

- Use English.
- Return only the commit message. Do not wrap it in Markdown.
- Use the imperative mood in the subject.
- Keep the subject at 72 characters or fewer when practical.
- Do not end the subject with a period.
- Use lowercase `type`.
- Include `scope` when the changed area is clear from paths or diff content.
- Omit `body` and `footer` when they do not add useful context.
- Mention breaking changes in the footer as `BREAKING CHANGE: ...`.

## Types

- `feat`: a new feature
- `fix`: a bug fix
- `docs`: documentation-only changes
- `style`: formatting, missing semicolons, whitespace, no code behavior change
- `refactor`: code change that neither fixes a bug nor adds a feature
- `perf`: performance improvement
- `test`: adding or correcting tests
- `build`: build system or external dependency changes
- `ci`: CI configuration changes
- `chore`: maintenance tasks that do not modify src or test files
- `revert`: revert a previous commit

## Examples

```text
feat(auth): add token refresh flow
```

```text
fix(api): handle empty search responses
```

```text
refactor(ui): simplify modal state handling
```
