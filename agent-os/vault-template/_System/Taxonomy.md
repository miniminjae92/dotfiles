# Taxonomy

## Type

- `project`: 진행 중인 개발 또는 서비스
- `decision`: 선택과 근거
- `concept`: 검증된 기술 개념
- `insight`: 개인 통찰
- `learning`: 학습 목표와 이해 검증
- `friction`: 수동 불편과 반복 비용
- `run`: 작업 실행 요약
- `review`: 주기적 검토
- `proposal`: 개선 실험 제안

## Origin

- `user`: 사용자가 직접 표현
- `agent`: 에이전트가 생성
- `joint`: 대화로 함께 확정
- `inferred`: 에이전트가 추론했으며 승인 필요

## Status

- `inbox`: 미분류
- `candidate`: 검토 필요
- `active`: 사용 중
- `verified`: 검증 완료
- `rejected`: 폐기 결정
- `archived`: 보관

## 승격 규칙

- `inbox`와 `candidate`는 검색 후보일 뿐 확정 지식으로 사용하지 않는다.
- 재현 가능한 근거, 실제 작업 검증, 또는 사용자의 명시적 확인이 있으면 `verified`로 승격한다.
- `inferred` 출처는 사용자 확인 전에는 `joint`나 `user`로 바꾸지 않는다.
- 프로젝트에만 유효한 결정은 개인 지식으로 일반화하지 않는다.
- 충돌하는 근거가 생기면 삭제하지 않고 `candidate`로 내린 뒤 재검토한다.
