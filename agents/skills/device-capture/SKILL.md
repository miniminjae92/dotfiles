---
name: device-capture
description: "Use when data must be read off a real phone screen (iOS or Android on USB): 앱 화면 수집, 실기기 캡처, 롱스크롤 캡처, 화면 텍스트 추출, 딥링크 착지 확인, 앱 URL 스킴 조회. Drives `devcap` so the human navigates the phone and the machine captures, stitches, OCRs, and records; the agent reads text.txt, not screenshots. Trigger examples: '폰 화면 수집해줘', '요기요 쿠폰함 캡처해서 읽어', '이 딥링크가 실기기에서 어디로 가는지 확인', '아이폰/안드로이드 연결했어, 데이터 뽑자'."
---

# device-capture: 실기기 하이브리드 수집

`devcap`(`~/projects/devcap`, `devcap --help`)이 iOS와 Android의 차이를 가린다. 분업은 고정이다.

- 사람: 로그인, 화면 진입, 모달 닫기, 배달 주소 같은 계정 상태. 10초 걸리는 일이고 자동화하면 세션을 다 먹는다.
- 기계(devcap): 스크린샷, 스크롤, 스티칭, OCR 또는 접근성 트리, 번들 기록. 모델 호출 0.
- 에이전트: `text.txt`를 읽고 해석한다. 이미지는 읽지 않는다.

## 절차

1. **점검.** `devcap doctor --quick`. 종료코드 0이면(수집 가능한 기기가 하나라도 있다) 다음으로. 2면 출력의 `→` 줄(폰에서 할 일)을 사용자에게 그대로 전달하고 기다린다. 대상이 아닌 플랫폼의 ✗는 무시해도 된다. 코드→행동은 아래 표.
2. **수집.** 화면마다 캡처 id 하나가 생기면 끝이다.
   - 사람이 폰을 들고 있을 때(기본): 사용자에게 **별도 터미널 창**에서 `devcap session -p <프로젝트> --labels 홈,쿠폰함,…` 을 돌리라고 한 문장으로 안내한다(Claude Code 창에서는 대화형 입력이 안 된다). 루프 안에서 `Enter`가 한 장, `m 라벨`이 수동 롱스크롤(절반~2/3 내리고 Enter, `u` 취소, `e` 끝), `s 라벨`이 자동 롱스크롤(WDA), `q`가 종료다. 사용자가 끝났다고 할 때까지 기다린다. 모델은 이 단계에 없다.
   - 딥링크로 닿는 화면이면 에이전트가 직접: `devcap open '<url>'` (iOS는 스킴 URL이면 번들을 자동으로 찾는다, 모르면 `devcap apps --grep <앱이름>`; https 유니버설 링크는 `--app <번들>`이나 WDA가 필요) → `devcap shot -l '<라벨>'` 또는 `devcap scroll -l '<라벨>'`(iOS 자동 스크롤은 WDA 필요, [pitfalls.md](pitfalls.md)).
3. **읽기.** 세션이 끝나면 `INDEX-<시각>.md`(`devcap index --today -p X`로 재생성, 2KB 안팎)를 읽고, 필요한 화면만 `devcap show <id>`(text.txt, 기본 6000B 캡)와 `devcap grep '<정규식>' --today -p X`(`id:gy: 줄`)로 읽는다. 값이 나오거나 "없다"가 요약의 `amounts`, `keywords`, `status`로 확인되면 끝이다. `--all`은 이유를 적고 쓴다. 텍스트에 답이 없을 때만 `frame_NN.png` 한 장을 본다.
4. **기록.** 해석 결과는 호출한 프로젝트의 규약대로 넣는다(트래커는 `ingest.py`). 증거 경로는 번들의 `long.png`다. 번들은 `~/.devcap/captures/[<프로젝트>/]<날짜>/<id>/`이고 `--out`으로 옮길 수 있다.

## 읽지 않는 것

`frame_*.png`, `long.png`(축소돼 아무것도 안 보인다), `text.json`, `text.pos.txt` 통째, `tree_*.xml`, WDA `/source`, `pymobiledevice3 accessibility list-items`. 이것들은 `show`, `grep`, `ls`, INDEX로 이미 요약돼 있다.

## 다시 만들지 않는 것

이전 세션들이 스크래치패드에 매번 다시 쓰던 것이 devcap에 들어 있다.

| 예전 | 지금 |
|---|---|
| `w.py`(WDA 세션, tap, swipe, screenshot) | `devcap wda up`, `devcap tap/swipe`, `devcap shot` |
| `ocr.swift` | `~/.devcap/bin/ocr`(자동 빌드), `devcap text <png>` |
| `probe.py`(화면 텍스트 지문) | `devcap shot -l … --print-text` |
| `collect2.py`(스크롤하며 텍스트 수집) | `devcap scroll` 또는 `session`의 `m`/`s` |
| `tap.py`(딥링크 열고 OCR) | `devcap open <url>` → `devcap shot` |

## doctor 코드 → 행동

| 코드 | 뜻 | 행동 |
|---|---|---|
| `IOS_OK` / `ADB_OK` | 수집 가능 | 2단계로 |
| `WDA_DOWN` | 입력 주입 불가(한 장, 수동 스크롤, 스킴 딥링크는 됨) | 자동 스크롤이 필요할 때만 사용자에게 `devcap wda up` + 폰 허용 60초 |
| `IOS_NONE` | 아이폰 안 보임 | 사용자: 케이블 재연결, 폰에서 '신뢰' |
| `ADB_NONE_USB_SEEN` / `ADB_UNAUTHORIZED` | 안드로이드가 USB엔 있는데 adb가 못 봄 / 승인 대기 | 사용자: USB 디버깅 켜기, MTP, RSA 팝업 승인 |
| `TOOL_*_MISSING` | 맥 쪽 도구 없음 | `→` 줄의 설치 명령 |

## 번들 (디렉터리 하나 = 수집 1건)

`text.txt`(에이전트용, 위에서 아래로 한 줄 하나, 기하로 중복 제거), `summary.json`(라벨, 프레임, 줄 수, 바이트, 금액 패턴, 키워드, `status` ok/browser?/store?/gap, 경고), `long.png`와 `frame_NN.png`(사람과 파서의 증거), `meta.json`, 옵션으로 `tree_NN.xml`. 수동/자동 롱스크롤의 산출물이 같다. `status`가 `browser?`나 `store?`면 앱이 아니라 브라우저/스토어 화면을 찍은 것이니 값을 믿지 않는다.

## 같은 화면을 또 찍을 때

라벨을 같게 주면 `ls`에서 나란히 보인다. 값 비교는 두 `text.txt`의 diff로 한다.

## 막히면

WDA가 안 뜨거나, 스와이프가 널뛰거나, 딥링크가 앱스토어로 새거나, 폰이 잠기면 [pitfalls.md](pitfalls.md)를 읽는다. 실측으로 굳은 것만 적혀 있다.
