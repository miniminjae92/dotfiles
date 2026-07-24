---
name: vsummary
description: "Use when the user gives a YouTube URL (or channel/playlist) and wants its content captured — invoked as /vsummary <URL>, $vsummary <URL>, or asks to 전사/요약/수확 a video. Default action saves the full timestamped transcript with no model call; only summarize when the user asks. Wraps the mature `video-summary` CLI (alias `vsummary`) in ~/.dotfiles/bin. Trigger examples: '/vsummary https://youtu.be/…', '이 영상 전사해줘 <URL>', '이 채널 회원영상 다 가져와'."
---

# vsummary — 유튜브 원본 수집 + 선택적 요약

목적: **원료(raw 전사)를 공짜로 보존하고, 요약은 필요할 때만.** 이도구의 90%는 요약이 아니라
자막 취득·채널 발견·회원 인증·중복 제거·옵시디언 정리 인프라다. 새로 짜지 말고 이 CLI를 쓴다.

핵심 원칙([[session-recording-harvest]]): **"기록은 공짜, 종합만 돈."**
raw 전사는 이미 받아오므로 저장은 토큰 0. 요약(Codex 호출)만 비용이 든다.

## 입력

`/video-summary <URL>` 뒤에 유튜브 영상/채널/재생목록 URL. `&t=…` 등 부가 파라미터는 그대로 둬도 됨
(도구가 video_id만 뽑는다). 여러 URL이면 각각 실행.

## 기본 동작 (URL만 준 경우)

모델 호출 없이 **raw 전사 노트만 저장**한다. 요약해 달라는 말이 없으면 절대 `--summarize`를 붙이지 않는다.

```bash
video-summary '<URL>'          # type: video-transcript, input_tokens 0
```

먼저 크기만 보고 싶으면:

```bash
video-summary '<URL>' --dry-run   # 자막 수·예상 토큰·전략만, 저장/호출 없음
```

저장 위치 기본값: `~/.obsidian/yggdrasil/3-stash/video-summaries/`
(환경변수 `VIDEO_SUMMARY_DIR`로 재정의 가능). 같은 영상 재실행은 캐시로 재사용된다.

자막 언어는 **영상 원본 언어를 자동 감지해 원문(`-orig` ASR)을 우선**한다 — 유튜브 자동번역본을 집지 않는다.
원문이 아닌 특정 언어가 필요하면 `--sub-langs en,ko`로 강제한다.

## 저장 후 · 비판적 평가 (단일 영상 기본 동작)

**단일 영상**을 저장한 뒤에는, 따로 요청이 없어도 저장된 raw 전사를 직접 읽고
**비판적 팩트 평가 + 인사이트 추출**을 대화에 바로 내놓는다. (요약 CLI가 아니라 에이전트가 판단한다.)

- 평가는 **대화로만** 전한다. **노트는 순수 raw로 유지** — 평가를 노트에 쓰지 않는다.
  단, 사용자가 "이 평가도 저장해줘"라고 하면 그때만 `## 에이전트 평가` 섹션이나 `-eval.md`로 남긴다.
- 요약 재탕이 아니라 **회의적 검증**이 목적이다. 뻔한 내용은 버리고 날을 세운다.

평가 형식(간결·직설, 이 골격을 따르되 영상에 맞게):

- **핵심 주장** — 영상이 실제로 주장하는 것 3~6개 (마케팅 문구가 아니라 실질 명제로).
- **팩트 체크** — 각 주장의 근거 강도: 탄탄 / 약함 / 과장 / 오류. 검증 가능한 사실 오류는 명시.
- **엑기스** — 비자명하고 보존 가치 있는 통찰만. 이미 아는 것·상식은 제외.
- **편향·의도** — 판매·홍보·체리피킹·과열(hype)·이해상충 신호.
- **실행** — 당장 적용할 것 1~3개 (없으면 없다고).
- **판정** — 볼 가치 있음 / 스킵 + 한 줄 이유.

전사가 아주 길면 핵심 구간 위주로 읽되, 무엇을 근거로 판단했는지 밝힌다.

## 요약까지 원할 때 (사용자가 명시적으로 요청)

`--summarize`를 붙이면 `## 전체 요약` + `## 핵심 내용`(타임스탬프 링크)을 추가한다.
**이때도 raw 전사는 같은 노트에 그대로 남는다.** raw 노트에 나중에 `--summarize`를 다시 돌리면 요약본으로 업그레이드된다.

```bash
video-summary '<URL>' --summarize                    # 표준 요약
video-summary '<URL>' --summarize --summary-mode detailed   # 밀도 높은 상세 요약
```

## 채널 / 재생목록 / 회원 전용

```bash
video-summary '<채널/재생목록 URL>' --channel                        # 공개 영상 순회
video-summary '<채널 URL>' --discover-channel-members \
  --cookies-from-browser 'chrome:Profile 1'                        # 회원 전용 발견·수집
```

- 회원 전용은 `--cookies-from-browser BROWSER[:PROFILE]`로 로그인 브라우저 쿠키를 런타임에 읽는다.
  쿠키 파일을 내보내지 않는다. **대화형 개인 명령으로만 쓰고**, 약관을 존중한다.
- 대량 첫 실행은 `--max-videos N`과 `--dry-run`으로 범위를 먼저 확인한다.
- 재생목록 인덱스는 `Playlists/` 아래 생성되고, 여러 목록에 걸친 영상도 노트는 하나만 만든다.
- 완료/주의 결과를 Slack으로 받으려면 `--notify-slack`.
- **배치는 전사만 저장하고 자동 비판 평가는 하지 않는다** (토큰 폭발 방지). 특정 영상 평가는 요청 시에만.

## 마무리

- 단일 영상: 저장 경로를 보고한 뒤, 위 형식대로 비판적 평가를 이어서 내놓는다.
- 채널 배치: 최종 JSON의 counts(summarized/transcribed/cached/failed)와 경고를 요약해 전하고,
  평가가 필요하면 어떤 영상을 볼지 물어본다.
- 요약(`--summarize`)을 했다면 토큰 사용량도 함께 보고한다.
