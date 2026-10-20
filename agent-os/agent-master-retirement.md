# Agent Master 폐기와 Agent OS 복귀

2026-10-19 사용자 요청에 따라 Agent OS를 기본으로 유지하고, am의 콜드 환경 실행 기능을 독립시킨다. 2026-10-20 이관과 검증, am 실행 링크 두 개 제거를 완료했다. 원본 데이터는 보관한다. 결정은 D-035를 따른다.

## 실행과 기록의 위치

| 목적 | 경로 또는 명령 |
|---|---|
| 평소 작업 | `gcodex`, `ncodex`, 기존 Agent OS |
| 새 콜드 환경 | `codex-plain --account google` 또는 `naver` |
| 콜드 환경 재개 | `codex-plain resume --all`, `resume --all --list` |
| 독립 런처 원본 | `~/.dotfiles/bin/codex-plain` |
| 새 콜드 환경 상태 | `~/.local/state/codex-plain` |
| 과거 대화 검색 | `asx list`, `asx search`, `asx show` (am 레거시와 새 plain 모두 포함) |
| am 원본 상태와 산출물 | `~/.local/state/agent-master` (보존, 이 디렉터리 삭제 금지) |
| 이관 스냅샷 | `~/.local/share/agent-os/retired-agent-master/2026-10-19` |
| 작업 기록 색인 | 위 스냅샷의 `INDEX.md`, `tasks.json`, `requests.json`, `events.json` |
| 검수된 자산 조사와 미결 사항 | 위 스냅샷의 `inventory.md`, `access-paths.json`, `open-items.json` |
| 과거 지식 볼트 복사본 | 위 스냅샷의 `knowledge-vault/` |
| 과거 코드 복구본 | 위 스냅샷의 `source/` (Git 이력 포함) |

콜드 환경은 개인 전역 지침, 스킬, 플러그인, 훅, 메모리를 이어받지 않는다. 프로젝트의 지침과 설정은 유지하므로 프로젝트 `.codex/config.toml`의 MCP 등은 적용될 수 있다. 선택한 계정의 인증은 원본 파일을 링크한다. 운영체제 샌드박스나 저장소 파일을 숨기는 기능은 아니다. am의 작업 DB, 승인함, 정책 버전 관리는 새 런처에 넣지 않는다. 런처는 Python 3.11 이상을 사용한다.

별도 저장 루트를 쓰면 `CODEX_PLAIN_STATE_DIR` 환경변수를 설정한다. 런처와 asx가 같은 값을 읽는다. 런처에만 `--state-dir`를 지정한 경우 검색 시에는 `ASX_CODEX_PLAIN_STATE_DIR`로 그 경로를 알려야 한다.

## 보존 범위와 조회

최초 스냅샷에 작업 48개, 요청 31개, 이벤트 772개가 있다. 이관 도중에도 현재 am 세션 기록은 증가하므로 이 수치는 최종 상태를 뜻하지 않는다. `state-snapshot.sqlite3`는 SQLite backup API로 만들고 `integrity_check=ok`를 확인했다. `manifest.json`에 보관 파일 해시와 링크 대상을 남긴다.

작업 JSON은 am을 설치하지 않아도 읽을 수 있다. `handoffs/`, `releases/`, `tasks/`, `work/`, `proposals/`도 보관했다. 과거 인계와 승인 기록은 당시 상태의 근거이며 새 작업의 실행 승인으로 사용하지 않는다. 원본 작업 홈에는 세션과 생성 이미지, 보고서 등 고유 산출물이 남아 있어 원본 상태 전체를 유지한다. 인증 파일을 새 런처로 복사하지 않는다.

원시 대화와 DB를 자동 동기화되는 지식 볼트에 넣지 않는다. 비공개 로컬 보관 루트는 권한 0700이며 작업 기록 파일은 0600이다. 다른 기기에는 별도 am 기록이 있을 수 있으므로 이 기기의 감사 결과만으로 다른 기기 데이터를 삭제하지 않는다.

## Agent OS에 채택한 원칙

- 완료 주장은 실제 검사 근거로 설명하며 검사 통과와 사용자 만족을 구분한다.
- 세션을 넘길 때 목표, 출처가 있는 결정, 적용 상태, 검증, 미결 질문과 다음 행동만 남긴다. 재개할 때 기록과 실제 파일을 대조한다.
- 사용자의 응답이 기록돼 있다는 사실을 변경 적용 완료로 간주하지 않는다.

이 원칙은 `agents/AGENTS.md`의 기존 두 항목을 보강해 반영했다. 공통 지침은 50줄을 유지한다. 매 대화에 작업 등록, 평가 명세, 승인함을 강제하지 않으며 기존 위임 기준과 전문 스킬 체계를 유지한다.

## am 전용 스킬 이관

작업 `de8ba1da501b`의 `rdd-skill/`에 있던 `rdd`, `object-calisthenics`를 `agents/skills/`로 원문 그대로 복사했다. 각 `SKILL.md`와 `agents/openai.yaml`, 총 4개 파일의 SHA256이 원본과 같다. 이관 내역은 로컬 보관 폴더의 `skill-migration.json`에 남겼다. Codex와 Claude에 각각 링크했고 Google/Naver Codex 홈은 기존 공용 skills 링크를 통해 같은 원본을 읽는다. 다른 작업에 이 스킬을 강제하는 공통 규칙은 추가하지 않았다.

스킬을 사용하는 작업에서는 프로젝트 지침과 사용자의 현재 요구를 우선한다. 특히 `rdd`의 테스트 우선 흐름을 이관을 이유로 모든 작업에 적용하지 않는다. 기존 `testing`, Java 문맥 스킬의 내용은 바꾸지 않았다. 스킬 본문은 이관 자산 검토를 위해 읽었으며 이번 환경 정리 작업에 실행하지 않았다.

## MCP와 접근 경로 이관

2026-10-20 재검수에서 am 홈 `naver/a1d611405f98`의 `notion`, `posthog` MCP를 확인했다. 초기 조사 보고의 MCP 누락을 정정했다. Notion URL을 공유 설정으로 이관했다가 같은 날 철회했다. `ww-project/.codex/config.toml`의 기존 `notion` stdio 설정과 같은 이름으로 병합되어 `url is not supported for stdio` 오류를 일으켰다. 이번에 추가한 전역 URL 항목만 제거했고 기존 프로젝트 설정은 유지했다. 원본 URL은 보관본에 남아 있다. OAuth 인증값은 읽거나 옮기지 않았다. 전역 재등록은 프로젝트별 동명 설정과 전송 방식을 대조하기 전에는 하지 않는다.

PostHog는 기존 `posthog-discount`와 같은 프로젝트 및 읽기 전용 설정이다. 도구 선택 쿼리는 달라 기존 설정을 유지하고 중복 서버를 추가하지 않았다. 원래 설정은 비공개 보관본 `am-mcp-original.json`, 대응 내역은 `mcp-migration.json`에 남겼다. 같은 프로젝트라는 사실이 모든 기능의 동등성을 뜻하지 않는다. am 홈의 별도 플러그인 설정은 발견하지 못했다.

am 홈의 대화 파일은 재검수 시점 113개다. 다른 Codex 계정의 세션 합계와 구분한다. 작업 48개의 메모, 목표, 결과에서 얻은 접근 경로 후보는 `access-paths.json`, 아직 처리되지 않은 작업 22개와 요청 6개(pending 5, deferred 1)는 `open-items.json`에서 찾는다. 과거 요청을 자동 승인하거나 실행하지 않는다. 전체 외부 서비스의 연결 상태나 다른 기기 데이터까지 감사한 것은 아니다.

## 설치와 최종 정리

`install.sh`는 기존 `bin/*` 설치 규칙으로 새 런처를 링크한다. 전체 설치는 다른 설정과 잡까지 건드리므로 이번 이관에서는 해당 링크만 전환한다. `psync` 매니페스트의 `!agent-master`는 자동 clone/pull/adopt 대상에서 제외하며 로컬 저장소를 삭제하지 않는다. `.zshrc`의 am 실행 별칭은 제거했다.

사용자의 최종 마무리 요청에 따라 `~/.local/bin/am`, `~/.local/bin/agent-master`의 기존 실행 링크 두 개를 제거했다. 저장소와 상태, 원래 볼트는 즉시 삭제 대상에서 제외한다. 복구용 CLI 원본과 작업 홈은 보관한다. 이전 작업 홈에서 대화를 재개하면 이전 am 지침이 다시 적용될 수 있다. 새 작업은 Agent OS에서 시작하고 필요한 기록만 읽는다.

## 복구

새 콜드 실행 링크를 이전 `~/projects/agent-master/bin/codex-plain` 대상으로 되돌리면 기존 실행기로 복귀한다. 제거한 실행 링크는 `am`과 `agent-master` 모두 `~/projects/agent-master/bin/agent-master`를 가리켰다. 저장소를 나중에 보관 이동할 경우 스냅샷 `source/`에서 복원하되 같은 경로의 새 파일을 덮어쓰지 않는다.

Notion 이관을 되돌릴 때는 공유 config의 이번 `mcp_servers.notion` 항목만 제거한다. 변경 전 파일은 로컬 보관본 `codex-config-before-notion.toml`에 있지만 이후 설정을 잃지 않도록 파일 전체를 덮어쓰지 않는다. 새 스킬은 원본과 링크를 별도 보관한 뒤 이번 설치 항목만 해제한다.

정책은 이번에 수정한 공통 지침 두 항목과 D-035, README의 이관 안내, 매니페스트의 해당 항목만 되돌린다. `.zshrc`, `DECISIONS.md`, 스킬들과 asx에는 작업 전 사용자 변경이 있으므로 파일 전체에 `git restore`를 실행하지 않는다. 원본 am 상태는 실행 중 변경될 수 있으므로 과거 스냅샷 DB로 덮어쓰지 않는다.
