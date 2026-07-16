# Agent OS

이 디렉터리는 Agent OS의 현행 결정, 진행 상태, 설계 배경과 운영 자산을 관리한다.

## 문서 권위와 읽는 순서

1. `DECISIONS.md`: 현재 확정된 운영 결정의 단일 진실 공급원
2. `CHECKLIST.md`: 구현과 파일럿의 현재 진행 상태
3. `PLAN.md`: 구축 전 가정과 설계 배경을 보존한 역사 문서
4. `archive/`: 폐기되거나 대체된 이전 문서

문서가 충돌하면 `DECISIONS.md`를 우선한다. `CHECKLIST.md`는 진행 상황만 나타내며 운영 결정을 대체하지 않는다. `PLAN.md`와 `archive/`의 문서는 현재 지침으로 사용하지 않는다.

구축 과정에서 계획과 다른 결정을 내렸다면 계획서를 현재 상태에 맞춰 다시 쓰지 않는다. 의미 있는 현행 결정은 `DECISIONS.md`에 남기고, 진행 상태만 `CHECKLIST.md`에 반영해 당시 계획과 실제 변화의 이력을 보존한다.

## 주요 자산

- `hooks.json`: 전역 Codex Stop Hook 정의
- `schemas/`: 이벤트와 Run 형식
- `vault-template/`: Developer OS 볼트 초기 구조
- `ASSET-AUDIT.md`: 유지·제외·재검토할 자산 목록

