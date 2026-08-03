# 모바일 지원 계약 템플릿

프로젝트의 기존 frontmatter와 언어를 따른다. 사실·후보·가정을 섞지 않는다.

```markdown
---
status: candidate
owner:
last_reviewed:
decision_deadline:
---

# Device Support Contract

## 제품 사용 조건

- 핵심 과업:
- 역할별 기기:
- 필수 hardware/capability:
- 지원하지 않는 환경:

## 세 범위

| 범위 | OS | hardware | 상태 | 근거 |
| --- | --- | --- | --- | --- |
| 설정상 설치 자격 | | | configured | build/store config |
| 지원 약속 | | | candidate/accepted | decision |
| 이번 릴리스 검증 | | | unverified/passed/failed | evidence |

## 기기 anchor

| Anchor | 모델·OS | 역할·창 | 덮는 위험 | 필요한 검증 | 상태·증거 |
| --- | --- | --- | --- | --- | --- |
| floor-performance | | | CPU·RAM·발열 | | |
| small-layout | | | 최소 창·Dynamic Type | | |
| large/adaptive | | | 최대·분할 창 | | |
| current | | | 최신 OS·SDK | | |
| capability | | | 센서·background 등 | | |

## 환경 매트릭스

- 권한: 최초 요청 / 거부 / 설정 복구 / 제한
- 수명주기: 시작 / background / 잠금 / 종료 / 복원
- 네트워크: 정상 / offline / 손실 / 망 전환 / 제한된 망
- 접근성: VoiceOver / 최대 Dynamic Type / 대비 / 색 이외 신호
- 성능: cold launch / 메모리 압박 / 장시간 / thermal / 배터리
- 저장·업데이트: 빈 상태 / 낮은 저장 공간 / 이전 버전 upgrade / 재설치
- 배포: Debug / Release / beta / store
- 스토어 표면: iPhone / iPad / Apple Silicon Mac / Vision Pro 호환 제공 여부

## 출시 Gate

- 자동 검증:
- Simulator/Emulator:
- 실기기:
- Release beta:
- 실패 시 fallback·복구:

## 빠진 기기와 확보 계획

| 빠진 증거 | 위험 | 확보 방법 | 담당자 | 결정 시점 |
| --- | --- | --- | --- | --- |

## 재검토 조건

- 주요 OS·SDK·스토어 요구 변경
- 사용자 기기 분포 또는 지원 요청 변화
- floor 기기의 성능·thermal·배터리 실패
- 핵심 dependency의 최소 OS·ABI 변경
```

`supported`는 증거가 있는 약속에만 사용한다. 설치 가능하지만 아직 확인하지 않은 범위는 `unverified`, 기능상 제공하지 않는 조합은 `unsupported`로 쓴다.
