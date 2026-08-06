# Korean AngularJS Commit Message Convention

Covers commit messages. The **Register by artifact** section extends to PR titles and bodies,
issue titles and bodies, and ADR titles.

## Which file owns which axis

One source per axis. Do not restate another file's rules here.

| Axis | Source of truth | Machine check |
|---|---|---|
| Punctuation (em dash, 가운뎃점, slash spacing) | mimir `20 Knowledge/좋은 글 작성 기준.md` §3 substitution table | `ko-style` (`--fix`) |
| Prose register in documents, and what makes writing read as agent-written | same file, §1, §2, §4 | none, this is a judgment call |
| README specifics | mimir `20 Knowledge/README 작성 기준.md` | `readme` skill |
| Commit, PR, and issue **form** (noun phrase vs sentence, layering, target-repo precedence) | **this file** | none yet |
| Agent tells on surfaces that are not files (session replies, commit messages) | `~/.dotfiles/agents/tell-rules.tsv` | `agent-os-tell-lint` |

Documents written for a human reader use `합니다체`, per the mimir standard §4. This file
governs the *form* of a subject line, not the prose register of a document body.

## Three layers, and what each one may override

| Layer | Examples | Whose rule wins |
|---|---|---|
| **0. Mechanical** | `type:` prefix present, no trailing period, subject length | This file. Always, every repo. |
| **1. Personal tells** | `~/.dotfiles/agents/tell-rules.tsv` (em dash, 가운데점 과다, 경어체) | Only inside repos you own. Never imposed on someone else's repo. |
| **2. Taste** | 명사형 vs 서술형, Korean vs English, scope usage, bullet vs prose | The target repository, measured. |

**A style learned in one repository does not travel.** A repo's convention is valid inside
that repo and nowhere else. Adopting its habits in your own repos is contamination, not
consistency. Measure again when you switch repos rather than carrying the last one's form
with you. This runs both ways: do not push your layer-1 tells onto a repo you are only
contributing to.

## Measure the target repo, do not eyeball it

In a repository you do not own, that repository's existing convention overrides layer 2.
Determine it by counting, not by reading the last few commits:

```sh
git log --format='%s' -30    # then classify the subject endings and take the majority
```

A handful of recent commits is not the convention. Two exceptions out of thirty are still
exceptions, and copying one produces a message that matches neither the repo nor this file.
Classify separately per artifact. A repo can use noun phrases for commit subjects and
declarative sentences for ADR titles at the same time, and usually does.

## Shape

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
- Use bullet points to enumerate what changed; use prose to explain why it changed or what
  judgment was made. Do not flatten a causal explanation into bullets, because the reasoning is
  what a future reader actually needs.
- Omit body and footer when they do not add useful context.
- Mention breaking changes in the footer as `BREAKING CHANGE: ...`.
- Return only the commit message. Do not wrap it in Markdown.

## Register by artifact

Pick the register by **whether a reader is actually being addressed**, not by artifact type.
A commit is a record; a PR description is a message to a reviewer. Same content, different
register.

| Artifact | Addressee | Register | Example |
|---|---|---|---|
| Commit subject | none | 명사형 | `feat(auth): 토큰 갱신 흐름 추가` |
| Commit body | none | 평서형 (`~한다`, `~였다`) | `적재 시점에 계산해 캐시에 굳히면 자정을 넘기지 못한다.` |
| PR title | none (it labels a change) | 명사형, same as commit subject | `feat: 만료 할인 응답에서 제외` |
| PR description | reviewer | **존댓말** (`합니다체`) | `…제외합니다. 근거는 ADR-008에 정리했습니다.` |
| Review comment | a person | **존댓말** | |
| Issue title | none | 명사형 | `TestFlight 외부 검증 빌드 배포` |
| Issue body (solo repo) | none | 평서형 | `…수직 흐름을 만든다.` |
| Issue body (asking maintainers) | maintainer | **존댓말** | |
| ADR / design doc title | none | **평서형 결정문** | `ADR-008. 종료일이 지난 할인은 요청 시점에 걸러 응답에서 뺀다` |
| ADR / design doc body | none | 평서형 | |

ADR titles are the one place a declarative sentence is correct rather than tolerated: an ADR
title *is* the decision, so `~한다`/`~둔다` carries meaning a noun phrase drops. Do not
"fix" ADR titles into noun phrases for consistency with commits. They are different genres
living in the same repo.

**Relation to `tell-rules.tsv`.** R03 (경어체 금지) applies to the `commit` surface only.
Document prose is `합니다체` by the mimir standard §4, and a PR description or review comment
addresses a person, so neither is a place to strip polite endings. The `commit` surface has
no hook feeding it yet, so commit messages are currently unchecked by machine.

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
