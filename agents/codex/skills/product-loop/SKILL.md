---
name: product-loop
description: "Run a full product improvement loop when the user wants to overhaul a product, start another cycle, or move evidence through research, UX definition, design, implementation, QA, release, measurement, and the next hypothesis."
---

# Product Loop

제품 개선을 한 번의 거대한 작업이 아니라 증거가 다음 판단을 여는 **한 바퀴**로 운영한다. 한 바퀴는 여러 세션에 걸쳐도 되며, 프로젝트의 `LOOP.md`가 진행 상태의 정본이다.

현재는 Codex 전용 실험 스킬이다. 완료된 한 바퀴에서 단계 누락을 막고, 중복 문서를 만들지 않으며, 매번 다음 행동을 명확히 했다는 사용자 판단을 받은 뒤에만 provider-neutral 스킬로 승격한다.

## 시작 또는 재개

1. 저장소의 `AGENTS.md`, `CONTEXT.md`, `docs/adr/`와 제품 문서를 확인한다.
2. `docs/product-loop/**/LOOP.md`에서 `status: active`인 사이클을 찾는다.
   - 하나면 그 사이클을 재개한다.
   - 없으면 `assets/cycle.md`를 복사해 `docs/product-loop/<YYYY-MM-DD>-<problem-slug>/LOOP.md`를 만든다.
   - 둘 이상이면 가장 최근 파일을 임의 선택하지 말고 충돌을 사용자에게 알린다.
3. `current_stage`, `next_owner`, `next_action`을 읽고 지금 할 일 하나를 먼저 보여준다.
4. 현재 단계에 해당하는 `references/stage-gates.md` 절만 읽고 실행한다.

완료 기준: 활성 사이클 하나와 현재 단계 하나가 식별되고, 사용자가 해야 할 일과 에이전트가 할 일이 분리되어 있다.

## 한 단계 실행

1. 환경에서 확인할 수 있는 사실은 직접 조사하고, 사용자에게는 목적·판단·취향·관찰처럼 사용자가 소유한 것만 묻는다.
2. 현재 단계의 산출물과 반증을 `LOOP.md` 또는 그 파일이 가리키는 문서에 기록한다.
3. 단계 게이트를 실제 증거로 충족했을 때만 상태를 `passed`로 바꾸고 다음 단계를 `in_progress`로 연다.
4. 게이트가 충족되지 않으면 `current_stage`를 유지하고 `next_owner`, `next_action`, `blocker`를 구체적으로 갱신한다.
5. 되돌릴 수 있는 조사·작성·구현·검증은 이어서 수행한다. 다음 경우에는 사용자에게 넘긴다.
   - 인터뷰 응답, 취향 판단, Grill 답변 또는 프로토타입 사용 관찰이 필요함
   - 이슈 게시, 배포, 데이터 삭제처럼 외부 상태를 바꾸거나 복구 비용이 큼
   - 측정 창이 지나야 실제 결과를 얻을 수 있음

완료 기준: 현재 단계가 증거와 함께 통과했거나, 통과에 필요한 다음 행동의 소유자와 관찰 가능한 완료 조건이 한 개로 좁혀져 있다.

## 단계 순서

순서는 아래를 정본으로 사용한다. 뒤 단계에서 가정이 깨지면 깨진 증거가 처음 영향을 주는 단계로 돌아가고, 그 이유를 `LOOP.md`에 남긴다.

1. 문제 발견
2. 사용자 조사
3. UX 문제 정의
4. Grill
5. PRD
6. UX flow
7. Wireframe
8. Prototype test
9. UI design
10. Issues
11. 구현
12. Functional QA
13. Design QA
14. 출시
15. 측정
16. UX 개선 가설
17. 다음 바퀴의 문제 발견

## 기존 스킬 연결

매트 엔지니어링 체인(grill→spec→tickets→implement)은 연속 실행하지 않는다. 4~5단계와 10~11단계에 나눠 꽂고, 사이의 6~9단계 게이트를 건너뛰지 않는다 (D-018).

- Grill에서는 `grill-with-docs`를 사용한다(`grilling` 인터뷰 + 도메인어가 바뀌면 `domain-modeling`이 repo `CONTEXT.md`·`docs/adr/`에 기록).
- PRD에서는 `to-spec`으로 스펙을 합성한다. PRD 정본은 to-spec 산출물 하나이며 `LOOP.md`에는 링크만 남긴다.
- Wireframe과 Prototype test에서는 답하려는 질문이 명확할 때 `prototype`을 사용한다.
- UI design에서는 저장된 취향 근거가 필요하면 `dref-consult`를 사용한다.
- Issues에서는 `to-tickets`로 수직 슬라이스 티켓을 만든다. 외부 트래커 게시는 게이트대로 사용자 승인 뒤에만 한다.
- 구현에서는 승인된 PRD와 Issues를 입력으로 `implement`를 사용한다.
- 구현 검토는 고정점과 PRD가 있을 때 `code-review`를 사용한다.

연결된 스킬의 산출물을 `LOOP.md`에서 링크한다. 같은 내용을 여러 문서에 복사하지 않는다.

## 사이클 종료

측정값과 UX 개선 가설이 기록되면 현재 사이클을 `status: completed`로 바꾼다. 가설을 다음 사이클의 최초 증거로 복사하지 말고 링크해 출처를 보존한 뒤 새 `LOOP.md`를 만든다.

완료 기준: 출시 여부와 무관하게 결과가 측정됐고, 다음 바퀴에서 검증할 하나의 UX 개선 가설이 정해져 있다.
