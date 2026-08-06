---
name: term
description: "Use when the user invokes /term or $term with terms, or asks what a word just used in this session actually means. Explains the essential meaning each term carries in the current context. Explanation only — never writes files."
---

# Term

`/term <용어들>` — 각 용어가 **이 컨텍스트에서 본질적으로 무슨 의미로 쓰였는지** 한 블록씩, 서론, 맺음말 없이 즉답한다.

```
**<용어>** — 이 맥락에서 쓰인 본질적 의미 한 줄
  ⚠ 혼동하기 쉬운 것과의 차이 한 줄   ← 필요할 때만
```

- 사전적 정의가 아니라 "지금 여기서 무엇을 가리켰나"를 잡는다. 일반 용법과 다르게 쓴 말은 그 차이를 밝히고, 불확실하면 추측 대신 표시한다.
- 파일을 쓰지 않는다. 용어의 합의, 정착은 매트 포컷 스킬 몫이다 — `domain-modeling`/`grill-with-docs`가 repo `CONTEXT.md` + `docs/adr/`에 기록한다.
