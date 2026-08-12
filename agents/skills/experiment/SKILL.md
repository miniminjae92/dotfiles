---
name: experiment
description: "Run one decision-bound verification cycle (assumption, pre-registered hypothesis, minimal experiment, judgment) whose working doc doubles as a share-ready artifact. Use when a costly-to-reverse decision rests on an unverified assumption: '이 가정 검증하자', '실험 설계하자', '실험으로 확인하자'. Also to resume or judge a running experiment: '실험 판정하자', '실험 이어서'. 분 단위 코드 사이클은 tdd, diagnosing-bugs가 담당한다."
---

# experiment: 결정에 걸린 검증 사이클

문서가 곧 사이클의 상태 기계다. 섹션 N이 완성되기 전에는 단계 N+1로 넘어가지 않는다(게이트). 판정 기준은 결과를 보기 전에 등록하고, 등록 뒤에는 커밋이 불변성을 증명한다. 문서는 처음부터 공유 독자를 향해 쓴다: 한국어, AGENTS.md 부호 규칙, repo `CONTEXT.md` 표준어.

## 진입 기준

되돌리기 비싼 결정이 검증 안 된 하중 가정 위에 서 있을 때 연다. 사소한 판단(T0)은 그 자리에서 처리하고, 분 단위 코드 사이클은 tdd와 diagnosing-bugs로 보낸다. 이 스킬은 시간 단위 이상의 결정 실험 전용이다.

## 준비

- 문서 위치: 해당 repo의 `docs/experiments/`. agent-os 운영 실험은 `~/.dotfiles/agent-os/experiments/`. 디렉터리가 없으면 만든다.
- 파일명 `YYYY-MM-DD_슬러그.md`, 내용은 [`template.md`](template.md)를 복사해 시작한다.
- git repo 안에서 진행한다. repo가 아니면 git init을 제안한다(등록 커밋이 불변성의 집행 장치다). 사용자가 거절하면 등록 시점에 가설 전문을 대화에 남기는 약한 대체로 진행한다.
- 재진입("판정하자", "이어서"): experiments 디렉터리에서 status가 registered 또는 running인 파일을 찾아 해당 단계부터 잇는다.

## 사이클

각 단계의 산출물은 문서의 같은 번호 섹션이다. 게이트를 통과해야 다음 단계로 간다.

**1 결정.** 이 실험이 가르는 결정과 결과별 행동 매핑을 적는다. 게이트: 결과에 따라 행동이 갈라진다. 모든 결과에서 행동이 같으면 정보 가치가 0이므로 실험을 닫고 그 사실을 기록한다. 닫는 것도 이 단계의 정상 출구다.

**2 가정 지도.** 결정이 깔고 앉은 가정을 나열하고, 하중(틀리면 무너지는 범위) × 미검증 정도로 순위를 매겨 하나를 고른다. 가정 심문이 필요하면 grilling 스킬을 쓴다. 게이트: 선택 이유가 문서에 있다.

**3 가설 등록.** template의 표준형 문장을 채운다. 게이트: 지표, 임계값, 기간이 모두 관측 가능하다. 통과하면 등록한다: frontmatter의 status를 registered로, registered에 날짜를 적고, 실험 파일 하나만 커밋한다. 커밋 메시지는 repo 관례를 따르되 기본형은 `docs(experiment): <슬러그> 가설 등록`.

```bash
git add docs/experiments/<파일>.md
git commit -m "docs(experiment): <슬러그> 가설 등록" -- docs/experiments/<파일>.md
```

등록 뒤 3 섹션은 불변이다. 고치고 싶다는 요청에는 현재 실험을 판정불가(사유: 가설 재정의)로 닫고 새 실험 파일로 잇는다.

**4 설계.** 움직이는 변수 하나, 통제, 마감, 비용 검산을 적는다. 비용 검산에서 실험 비용이 정보 가치(결정을 바꿀 확률 × 바뀐 결정의 이득)를 넘으면 실험을 닫고 자료 조사나 즉시 판단을 권한다. UI나 상태 모델 질문이면 prototype 스킬이 이 단계의 실험 형태다. 게이트: judge_by에 마감이 박혀 있다. status를 running으로 바꾼다.

**5 실행과 판정.** 실험을 돌리고 결과 데이터를 적은 뒤, 3에서 등록한 기준에 기계적으로 대조한다. 판정은 셋 중 하나: 살아남음(증명이 아니라 이번 공격을 버텼다는 뜻), 반증, 판정불가(설계 결함으로 기준을 가를 수 없음). 게이트: 판정 근거가 등록된 기준의 문장과 짝지어져 있다.

**6 갱신과 요약.** 다음 행동(persevere, pivot, redesign 중 하나), 배운 것, 다음 가정을 적는다. 그다음 요약 블록을 문서 맨 위에 쓴다: 결정, 가설, 결과, 판정, 다음 행동을 한 화면에, 결론 먼저. status를 judged로 바꾸고 등록 때와 같은 방식으로 실험 파일만 판정 커밋한다.

공유 게이트(요약 작성 직후 검사, 전부 통과하면 markdown 그대로 공유 가능):

- 결론이 첫 문단에 있다.
- AGENTS.md 부호 규칙을 지켰다.
- 용어가 repo CONTEXT.md 표준어다.
- 1 결정 섹션이 배경을 모르는 독자에게 자립적이다.

Notion 게시나 HTML 변환은 요청받았을 때만 한다.

## 팀 repo

main이 보호된 팀 repo에서는 실험 브랜치에서 진행하고, 등록 커밋을 푸시해 PR을 여는 것까지가 등록이다. 결과가 나오기 전에 팀이 가설을 봤다는 증거가 PR 타임라인에 남으므로, squash merge로 커밋이 합쳐져도 유지되고 리뷰어가 지표와 임계값을 사전에 리뷰할 수 있다. 푸시와 PR 생성은 승인받고 한다.

학습이 코드 변경으로 이어지면 별도 PR로 구현한다. 실험 문서의 요약 블록이 PR 본문의 "왜"가 되고, PR은 실험 문서를 링크한다. 실험 장치 자체가 코드(플래그, variant)를 요구하면 그 PR도 같은 문서를 링크해, 등록 PR, 장치 PR, 정리 PR을 한 실험의 궤적으로 묶는다.

## 출구

- agent-os 실험이 확정 결정이 되면 `agent-os/DECISIONS.md`의 D-번호 승격을 제안하고 실험 문서를 근거로 링크한다.
- 다음 가정이 남았으면 새 실험 파일로 다음 사이클을 제안한다.
