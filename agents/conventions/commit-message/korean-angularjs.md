# Korean AngularJS Commit Message Convention

Generate commit messages in this shape:

```text
<type>(<scope>): <subject>

<body>

<footer>
```

## Required Rules

- Use lowercase English `type`.
- Include `scope` when the changed area is clear from paths or diff content.
- Write the `subject` in Korean noun-phrase style.
- Do not use sentence endings such as `합니다`, `했다`, `함`, or `입니다` in the subject.
- Keep the subject concise, preferably 50 Korean characters or fewer.
- Do not end the subject with a period.
- Write the body in Korean when it adds useful context.
- Prefer concise bullet points in the body.
- Omit body and footer when they do not add useful context.
- Mention breaking changes in the footer as `BREAKING CHANGE: ...`.
- Return only the commit message. Do not wrap it in Markdown.

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
feat(auth): 토큰 갱신 흐름 추가
```

```text
fix(api): 빈 검색 응답 처리 오류 수정
```

```text
docs(readme): Codex 아카이브 명령 사용법 문서화
```

```text
feat(codex): Codex 작업 흐름 스킬 추가

- work 명령으로 TASK.md 기반 작업 흐름 실행
- arc 명령으로 최신 Codex 세션 아카이브 지원
- 커스텀 스킬 symlink 설치 처리
```
