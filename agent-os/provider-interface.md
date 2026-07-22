# Provider Interface Surface

에이전트를 **인터페이스**로, Codex·Claude·Gemini(agy)를 그 인터페이스의 **구체 클래스**로 보는
관점에서, 계약이 provider마다 어긋나는 지점을 기록한다. 공급자 중립 자산(공통 core·훅 스크립트)을
어디까지 그대로 이식할 수 있고 어디서 어댑터가 필요한지의 경계를 명시하는 것이 목적이다.

배경 결정: [DECISIONS.md](DECISIONS.md) D-003(기록 계층), routing.json의
`without_claude` 정책("claude_* 참조를 제거해도 시스템이 성립해야 한다")이 이 인터페이스 지향의 씨앗.

## 계약 표면 (drop-in provider가 만족해야 하는 축)

한 provider를 다른 provider로 교체하려면 아래 6개 축이 일치하거나, 그 차이를 얇은 어댑터로 흡수해야 한다.

1. **설정 파일 위치 & 스키마** — 훅을 어디에 어떤 JSON 모양으로 선언하는가
2. **이벤트 이름 집합 & 표기** — 어떤 라이프사이클 이벤트를, 어떤 대소문자로 노출하는가
3. **stdin 페이로드** — 훅이 받는 컨텍스트 필드
4. **stdout → 컨텍스트 주입** — 훅 출력이 모델 컨텍스트로 들어가는가 (agent-os-core-check가 의존하는 축)
5. **차단(blocking)** — exit code로 진행을 막을 수 있는가
6. **matcher** — 이벤트 하위 필터(예: source=startup) 지원 여부

## 어긋나는 지점

`✓` 검증됨 · `?` 미검증(문서/실측 확인 필요) · `—` 해당 없음/미사용

| 축 | Claude Code | Codex CLI | Gemini (agy) |
|---|---|---|---|
| 설정 파일 | `~/.claude/settings.json` (`claude/settings-fragment.json`에서 병합) | `~/.codex/hooks.json` (+ `config.toml`의 `[hooks.state]` 레지스트리) | `~/.gemini/config/hooks.json` |
| 최상위 스키마 | `hooks.{Event}[].hooks[]` (중첩) `✓` | `hooks.{Event}[].hooks[]` (중첩, Claude와 동일) `✓` | `{그룹명}.{Event}[]` (**평면·`hooks` 래퍼 없음**, 임의 그룹명 예: `macos-notification`) `✓` |
| 명령 엔트리 | `{type,command,timeout,matcher?}` | `{type,command,statusMessage?,timeout}` | `{type,command,timeout}` |
| 이벤트 표기 | PascalCase `✓` | PascalCase (`config.toml` 상태키는 소문자로 정규화) `✓` | PascalCase `✓` |
| 이벤트 집합 | SessionStart·Stop·SubagentStop·UserPromptSubmit·Notification·PreCompact·PreToolUse·PostToolUse·SessionEnd `✓` | SessionStart·Stop 확인 `✓` / 그 외 Codex 문서 참조 `?` | Stop만 사용 확인 `✓` / SessionStart 지원 여부 `?` |
| stdin 페이로드 | session_id·transcript_path·cwd·hook_event_name·source·model·agent_type?·session_title? `✓` | session_id·transcript_path·cwd·hook_event_name·model·permission_mode·source `✓` | `?` (미검증 — agent-notify는 stdin 미사용) |
| stdout→컨텍스트 주입 | plain stdout **또는** `hookSpecificOutput.additionalContext` `✓` | plain stdout **또는** `additionalContext` (Claude와 동일) `✓` | `?` (**미검증** — 현재 훅은 side-effect뿐이라 규약 미행사) |
| 차단(exit 2) | 지원 (PreToolUse deny 등) `✓` | `?` | `?` |
| matcher | 지원 `✓` | 지원 (`startup\|resume\|clear\|compact`) `✓` | `?` |

## 결과 (이식성 경계)

- **Claude ↔ Codex는 사실상 동형.** SessionStart 계약(중첩 스키마 + stdout 주입 + 유사 페이로드)이 일치해,
  `agent-os-core-check` 같은 계기(instrument)를 **같은 스크립트 + 라벨 인자**만으로 양쪽에 붙일 수 있다.
  이것이 2026-07-22 core-drift 탐지 훅을 두 CLI에 동시에 얹을 수 있었던 이유.
- **agy(Gemini)는 두 겹으로 어긋난다.** (1) 설정 스키마가 평면형이라 Claude/Codex 훅 JSON을 그대로 못 쓰고,
  (2) stdout→컨텍스트 주입 규약이 미검증이다. 그래서 core-check를 agy에는 **의도적으로 안 붙였다.**
  agy는 현재 side-effect 훅(Stop→알림)만 담당하는 clerk 역할이라 core drift 인지가 불필요하다는 판단과도 정합적
  (routing.json: clerk는 정적 유지).

## 열린 경계 (검증하면 이 표를 갱신)

- [ ] Codex의 전체 이벤트 집합과 exit-code 차단 규약 (Codex hooks 공식 문서)
- [ ] agy(Gemini)가 SessionStart 계열 이벤트를 지원하는지, 지원 시 stdout→컨텍스트 주입 여부
- [ ] agy 평면 스키마 ↔ 중첩 스키마 어댑터가 필요해질 시점(agy에 컨텍스트 주입 훅을 붙이려 할 때)

이 세 항목이 닫히면 "clerk도 core 인지 대상에 넣을지"를 실측 근거로 재검토할 수 있다(D-004/D-009).
