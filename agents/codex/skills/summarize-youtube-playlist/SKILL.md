---
name: summarize-youtube-playlist
description: Interactively collect missing inputs and safely summarize every accessible video in a YouTube creator playlist into Obsidian with the local video-summary workflow. Use when the user invokes $summarize-youtube-playlist or asks in Korean or English to scrape, summarize, prioritize, resume, or process a YouTuber channel playlist, course playlist, members-only playlist, or all videos in a named playlist. Ask for any missing channel URL, playlist URL or name, gcodex/ncodex account, browser cookie profile, usage stop threshold, and Slack preference; resolve playlist names, prevent concurrent batches, verify the named account and real model authentication, run a two-video gate, reuse cached summaries, enforce a quota stop, and report inaccessible or captionless videos.
---

# 유튜브 재생목록 요약

사용자가 기술 옵션을 외우지 않아도 필요한 값을 대화로 수집하고, 접근 가능한 재생목록 영상을 안전하게 요약한다. 결과는 기본적으로 Obsidian `Video Summaries`에 저장한다.

## 1. 입력 수집

사용자가 이미 제공한 값은 다시 묻지 않는다. 다음 값 중 빠진 것만 한 번의 짧은 질문으로 요청한다.

1. 유튜버 또는 채널 URL
2. 재생목록 URL 또는 정확한 재생목록 이름
3. 사용할 계정 명령: `gcodex` 또는 `ncodex`
4. 로그인된 브라우저 프로필: 기본 후보 `chrome:Profile 1`
5. 사용량 자동 중단 기준: 기본값 사용 75%
6. Slack 완료·오류 알림: 기본값 사용

재생목록 URL이 있으면 채널 URL은 참고 정보로만 사용한다. 이름만 받으면 캐시에서 정확한 URL을 찾는다. 사용자가 “기본값으로”라고 답하면 브라우저 프로필, 75% 중단, Slack 사용을 채택한다. 계정은 추정하지 말고 반드시 `gcodex` 또는 `ncodex` 중 하나를 받는다.

질문 예시:

> 진행에 필요한 값만 알려주세요: 채널 URL, 재생목록 URL 또는 이름, 사용할 계정(`gcodex`/`ncodex`). 브라우저는 `chrome:Profile 1`, 사용 75% 자동 중단, Slack 알림을 기본값으로 적용해도 되는지도 알려주세요.

## 2. 실행 충돌 확인

새 쓰기 작업 전에 기존 영상 배치를 확인한다.

```bash
launchctl print "gui/$(id -u)/com.miniminjae.video-summary-member-batch"
launchctl print "gui/$(id -u)" | rg 'video-summary-(member-batch|playlist)'
```

- 같은 재생목록 작업이 실행 중이면 새 작업을 만들지 말고 현재 상태와 로그 위치를 알려준다.
- 다른 영상 배치가 실행 중이면 동시에 시작하지 않는다. 우선순위를 바꾸려면 현재 작업 중단이 필요하다고 설명하고 사용자 승인을 받은 뒤에만 중단한다.
- 실행 중인 프로세스, LaunchAgent, PID 파일, 인증 파일을 자동으로 삭제하지 않는다.

## 3. 재생목록 해석

재생목록 URL이 있으면 그대로 사용한다. 이름만 있으면 먼저 기존 회원 인벤토리에서 고유하게 일치하는 URL을 찾는다.

```bash
inventory="$HOME/.obsidian/yggdrasil/3. Resource/Video Summaries/Playlists/.member-inventory.json"
jq -r '.videos[].playlists[]? | [.title, .url] | @tsv' "$inventory" | sort -u
```

- 대소문자를 무시한 정확 일치를 우선한다.
- 부분 일치가 하나면 사용자에게 찾은 제목과 URL을 보여주고 사용한다.
- 일치가 여러 개면 후보만 제시하고 선택을 요청한다.
- 캐시가 없거나 일치하지 않으면 긴 채널 전수 탐색을 임의로 시작하지 말고 재생목록 URL을 요청한다.
- 사용자가 명시적으로 최신 목록 탐색을 요청한 경우에만 `--refresh-inventory`를 사용한다.

## 4. 계정과 인증 Gate

plain `codex`로 대체하지 않는다. 사용자가 선택한 명명 래퍼만 사용한다.

1. `<account> usage`를 실행해 마스킹된 이메일, 현재 사용량, 갱신 시각을 보여준다.
2. 표시된 계정이 사용자의 의도와 다르거나 usage 조회가 실패하면 중단하고 `<account> login`을 요청한다.
3. 파일 인증을 사용할 때 account home은 700, `auth.json`은 600인지 확인한다. 인증 내용은 출력하거나 복사하지 않는다.
4. 실제 Responses 인증을 다음 최소 호출로 검증한다.

```bash
<account> exec --ephemeral --sandbox read-only \
  -c 'model_reasoning_effort="low"' --json \
  'Reply with exactly: AUTH_OK'
```

`AUTH_OK`가 아니거나 401이 발생하면 영상 요약을 시작하지 않는다. 다른 계정이나 plain `codex`로 자동 전환하지 않는다.

## 5. 2편 Gate

전체 재생목록 전에 같은 입력으로 최대 2편만 검증한다.

```bash
video-summary '<PLAYLIST_URL>' \
  --channel \
  --members-only \
  --cookies-from-browser '<BROWSER_PROFILE>' \
  --codex-command <ACCOUNT> \
  --max-videos 2 \
  --stop-at-used-percent <STOP_PERCENT> \
  --dry-run
```

dry-run 성공 후 시작 사용량을 기록하고 `--dry-run`만 제거해 실제 2편을 실행한다. 다음을 모두 확인한다.

- 실패 0건
- 요약 파일 2개 또는 유효한 기존 캐시 2개
- 재생목록 인덱스 생성
- 실행 후 사용량 확인
- 인증·쿠키·자막 오류 없음

한 편이라도 실패하면 전체 배치를 시작하지 않고 원인과 복구 명령을 보고한다. 두 편이 모두 성공하면 별도 중간 승인 없이 사용자가 요청한 전체 재생목록을 계속한다.

## 6. 전체 배치 실행

대화 세션에서 반복 폴링하지 않는다. macOS 사용자 LaunchAgent로 독립 실행하고, `video-summary`의 캐시와 사용량 안전 중단을 사용한다.

```bash
launchctl submit \
  -l 'com.miniminjae.video-summary-playlist.<SAFE_ID>' \
  -o '<LOG_PATH>' \
  -e '<LOG_PATH>' \
  -- /usr/bin/env \
  'PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin' \
  "$HOME/.local/bin/video-summary" '<PLAYLIST_URL>' \
  --channel \
  --members-only \
  --cookies-from-browser '<BROWSER_PROFILE>' \
  --codex-command "$HOME/.local/bin/<ACCOUNT>" \
  --stop-at-used-percent <STOP_PERCENT> \
  --notify-slack

launchctl kickstart \
  "gui/$(id -u)/com.miniminjae.video-summary-playlist.<SAFE_ID>"
```

`SAFE_ID`는 검증한 재생목록 ID의 영숫자·하이픈·밑줄만 사용한다. 로그는 `~/.local/state/video-summary/` 아래에 둔다. 재생목록 ID를 얻지 못하면 URL의 SHA-256 앞 12자를 사용한다.

시작 직후 한 번만 다음을 확인한다.

- LaunchAgent `state = running`
- 로그에 첫 영상 또는 캐시 항목이 나타남
- 즉시 인증 오류가 없음

그 뒤에는 활성 Codex 턴에서 주기적으로 확인하지 않는다. 완료·오류·75% 안전 중단은 Slack과 로그로 확인한다.

## 7. 결과 보고

최종 응답에는 다음만 간결하게 포함한다.

- 선택한 재생목록과 마스킹 계정
- 2편 Gate 결과와 실행 전후 사용량
- 전체 배치 LaunchAgent label과 로그 경로
- 캐시 재사용 및 사용량 중단 기준
- 접근 불가, 삭제, 자막 없음 항목의 처리 방식
- 사용자가 해야 할 일이 있으면 정확한 한 단계

## 안전 규칙

- 브라우저 쿠키 파일을 내보내거나 인증 토큰을 출력하지 않는다.
- `auth.json`, Keychain 항목, 기존 노트, 인벤토리와 로그를 자동 삭제하지 않는다.
- 동일 출력 디렉터리에 두 배치를 동시에 실행하지 않는다.
- 재생목록이 모호한 상태에서 채널 전체를 처리하지 않는다.
- 기존 요약은 캐시로 건너뛰며 `--force`는 사용자가 명시한 경우에만 쓴다.
- 사용량 자동 중단 없이 전체 재생목록을 실행하지 않는다.
- 공개 영상까지 포함하려면 `--members-only` 제거가 범위 변경임을 먼저 알리고 사용자 선택을 받는다.
