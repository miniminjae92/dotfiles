# Dotfiles — Agent Assets

개인 dotfiles이자 에이전트 CLI(Claude, Codex, Gemini) 운영 자산의 정본 저장소. 이 문서는 이 레포의 용어집이며, 구조 결정의 배경은 `agent-os/DECISIONS.md`(D-014), 폴더 지도는 `README.md`의 Repository Layout 절에 있다.

## Language

**설비 세팅값 (`agents/`)**:
고치면 에이전트가 다르게 일하는 실행 자산 전부(지침, 스킬, 훅, 라우팅). 전부 홈으로 심링크 설치된다.
_Avoid_: "설정 폴더", "config" (범위가 모호함)

**운전 일지, 계측 규격서 (`agent-os/`)**:
고쳐도 에이전트는 그대로인 운영 기록과 계약(결정, 상태, paths.env, schemas). 홈으로 설치되지 않는다.
_Avoid_: agents와 혼용, "에이전트 설정"

**어댑터**:
`agents/<공급자>/` — 특정 CLI만 읽는 공급자 종속 자산 폴더. 내부는 그 공급자의 홈 구조를 미러링한다(예: `agents/codex/skills/` → `~/.codex/skills/`). 폴더명은 래퍼 도구가 아니라 읽는 주체 기준(gemini이지 agy가 아님).
_Avoid_: 공급자 폴더를 레포 최상위에 두는 것

**홈 링크 0 불변식**:
`agent-os/`의 어떤 파일도 install.sh가 홈으로 심링크하지 않는다는 규칙. "이 파일 고치면 시스템에 반영되나?"를 폴더 위치만으로 판정 가능하게 한다.
_Avoid_: "참조 0"으로 오해 (bin 스크립트가 경로로 읽는 것은 허용)

**2단 규약**:
행동 변경 = DECISIONS.md 기록(결정) + agents/ 반영(승격). 반영 없는 결정은 미집행.
_Avoid_: 결정 기록만으로 에이전트가 바뀐다고 가정

**벤더링**:
upstream 스킬을 `agents/skills/`로 복사해 내 git으로 관리하는 것. 수정 권리를 얻는 대신 갱신은 수동 diff.
_Avoid_: 구독(플러그인 — 자동 갱신, 수정 불가)과 혼용

**VENDOR.md**:
벤더 스킬의 출처 기록(원본 경로, 커밋/버전, 가져온 날, 수정 여부, 갱신법). 출처는 이 파일에만 기록한다 — SKILL.md frontmatter에 넣지 않는다(스킬 파일을 upstream과 바이트 동일하게 유지해 diff를 깨끗하게).
_Avoid_: 자작/벤더 폴더 분리 (출신이 바뀔 때마다 이동을 강제함)

**라우팅 패키지**:
`agents/routing.json`(역할→모델) + `agents/models.json`(모델 별칭, 정형 태스크 라우팅). 서로 참조하는 한 시스템이다.
_Avoid_: 둘을 별개 설정으로 취급
