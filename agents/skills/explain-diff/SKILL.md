---
name: explain-diff
description: Use when the user asks for a rich explanation of a code change, diff, branch, or PR, or when the explain-diff-gate hook blocks a commit and asks for an explainer. Produces a self-contained HTML explainer (background, intuition, literate diff, quiz).
---

# Explain Diff

Please make me a rich, interactive explanation of the specified code change.

대상이 지정되지 않았으면 지금 커밋하려는 변경(staged diff, 없으면 `git diff HEAD`)이 대상이다.

It should have these sections:

- Background: Explain the existing system relevant to this change. (You should broadly explore surrounding code for this.) We don't know how much the reader already knows, so include a deep background for beginners (note that it can be skipped if the reader is already familiar), and then a more narrow background directly relevant to the change.
- Intuition: Explain the core intuition for the code change. The focus here is to explain the essence, not the full details. Use concrete examples with toy data. Use figures and diagrams liberally.
- Code: Do a high-level walkthrough of the changes to the code. Group/order the changes in an understandable way.
- Quiz: Come up with five questions that test the reader's knowledge of this PR. This should be medium difficulty, difficult enough that you actually need to understand the substance of the PR to answer them, but not gotchas. The goal is to help the reader make sure that they've actually understood. These should be presented as interactive multiple-choice questions, and when the user clicks, it tells them whether they were correct and gives feedback.

Format:

- Output a single self-contained HTML file which includes CSS and JavaScript. Make the whole thing one long page with section headers and a table of contents. Don't use tabs for the top-level structure. Basic responsive styling so you can view it on a phone is nice too. Put the file in a global place on my computer outside of the code repo, and make sure the filename always starts with today's date in `YYYY-MM-DD-` format, because it helps keep the files time-sorted and out of version control. For example: / tmp/2026-01-12-explanation-<slug>.html
- Please write with the clarity and flow of Martin Kleppmann, making it engaging and written in classic style. Transitions between sections should be smooth.
- Some tips on diagrams. Ideally, you should pick a small number of diagram families that can be reused throughout the explanation to explain various cases. Some useful kinds of diagrams:
  - A very simplified version of the UI that the user sees in the app, to explain UI changes.
  - A system diagram showing data flow or communication between components. Make sure to include example data here!
- Don't use ASCII diagrams. Always use simple HTML designs for your diagrams, HTML lists for lists of things, etc.
  - For code blocks, always use `<pre>` tags. If you use a custom styled div instead, it **must** have
    `white-space: pre-wrap` in its CSS, or the browser will collapse all newlines into a single line.
    Before saving the file, scan each code block in the HTML source and confirm its CSS includes
    `white-space: pre` or `pre-wrap`.
- Use callouts for key concepts or definitions, important edge cases, etc.

## 로컬 규약 (원본에 대한 추가, D-027)

- **위임**: 메인 세션에서 직접 쓰지 않는다. stage 직후 서브에이전트에 백그라운드로
  맡기고, 그 사이 커밋 메시지 작성 같은 남은 일을 한다. 서브에이전트는 이 문서 전체를
  따르고 `ack` 까지 마친 뒤 파일 경로만 돌려준다. 이유는 둘이다.
  (1) 메인 세션은 매 턴 누적 컨텍스트를 통째로 다시 읽어, 세션이 길수록 같은 설명서가
  비싸진다. 서브에이전트는 세션 길이와 무관하게 일정하다.
  (2) 코드를 짠 에이전트는 왜 맞는지 이미 확신이 서 있어서, diff 만으로 설명이
  성립하는지 검증하지 못한다. 위임하면 작성자와 설명자가 갈려 D-027 약점 1
  (설명서와 퀴즈를 같은 에이전트가 만들면 오류가 상관된다) 이 부분적으로 풀린다.
- **언어**: 산문은 한국어로 쓴다. 코드, 식별자, 기술 용어 원어는 그대로 둔다.
- **저장 위치**: `$EXPLAIN_DIFF_DIR` (경로 계약 D-012, 기본 `~/.local/state/explain-diff/`)
  아래 `YYYY-MM-DD-explanation-<slug>.html`. repo 안에도 볼트에도 쓰지 않는다. 커밋마다
  쌓이는 일회성 산출물이라 버전 관리와 볼트 양쪽을 오염시킨다.
- **저장 후**: 반드시 기록한다. 이걸 빼먹으면 게이트가 같은 커밋을 다시 막는다.

  ```sh
  explain-diff-gate ack --path <생성한 HTML 경로>
  ```

- **퀴즈 기록**: 퀴즈를 넣었으면 `agents/skills/explain-diff/quiz-record.html` 의 내용을
  `</body>` 직전에 그대로 붙인다(수정하지 않는다). 응답이 localStorage 에 남고
  [기록 저장] 이 떨군 JSON 을 `explain-diff-gate quiz --ingest` 가 수거한다. 마크업 계약은
  `.q` 컨테이너, 그 안의 `.opt` 버튼, 클릭 뒤 붙는 `right`/`wrong` 클래스 셋뿐이다.
- **보고**: 사용자에게 파일 경로와 이 변경의 핵심 3줄을 대화로 전한다. 퀴즈는 문서 안에
  두되 풀라고 요구하지 않는다. 통과 의무는 없다(게이트로 쓰지 않기로 한 결정).
  기록은 읽었다는 증거일 뿐 통과 조건이 아니다.
- **분량**: 본문 줄 수가 diff 줄 수를 넘지 않는 것을 목표로 한다. 고정 오버헤드인
  CSS 와 퀴즈 스니펫은 세지 않는다. 초과하는 첫 번째 원인은 Background 를 부풀리는
  것이니 거기부터 줄인다. 설명서가 diff 보다 길어질수록 읽히지 않는다.
  단 하한이 있다. 배경 한 문단과 퀴즈를 담으려면 본문 80줄쯤은 필요하므로, 작은
  diff 에는 이 상한을 적용하지 않는다. 상한은 부풀리기를 잡는 장치이지 최소 분량을
  깎는 장치가 아니다.
