벤더링 원본: https://gist.github.com/geoffreylitt/a29df1b5f9865506e8952488eac3d524 (Geoffrey Litt, `explain-diff-html.md`)
revision: 126e7fe9eecaafadfe1ac8bb183d135812b608f2 (2026-08-06)
가져온 날: 2026-08-06 · 출처 강연: "Understanding is the new bottleneck" (AI Engineer, 2026-07-10)

로컬 수정 있음(무수정 사본 아님). 원본 본문은 그대로 두고 아래를 덧붙였다:

- 대상 미지정 시 staged diff 를 기본 대상으로 삼는 한 줄
- `## 로컬 규약` 절 전체: 한국어 산문, `$EXPLAIN_DIFF_DIR` 저장(경로 계약 D-012),
  `explain-diff-gate ack` 호출 의무, 보고 형식, 분량 조절

갱신법: 위 gist 를 다시 받아 `## 로컬 규약` 위쪽만 교체한다. gist 는 태그가 없으므로
revision 해시로 대조한다: `gh api gists/a29df1b5f9865506e8952488eac3d524 --jq '.history[0].version'`

원본에는 Notion 변형(`explain-diff-notion.md`)도 있으나 벤더링하지 않았다. 커밋마다 쌓이는
일회성 산출물을 Notion 에 올릴 이유가 없고, 로컬 HTML 이 오프라인에서 그대로 열린다.
