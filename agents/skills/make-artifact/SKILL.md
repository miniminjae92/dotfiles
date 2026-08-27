---
name: make-artifact
description: "사용자가 $make-artifact 또는 make_artifact로 호출하면 Artifact Spec과 Workflow에 따라 결과물을 설계, 작성, 저장한다. 일반 문서 작성 요청에는 자동으로 사용하지 않는다."
---

# make_artifact

Artifact Compiler의 기준과 절차를 실행하는 사용자 호출 전용 진입점이다.

## 정본

이 `SKILL.md`가 있는 디렉터리를 Artifact Compiler 정본으로 사용한다.

시작할 때 다음 파일을 확인한다.

- [출력 설정](references/artifact-compiler.yaml)
- `references/specs/`
- `references/workflows/`

정본을 찾을 수 없으면 임의의 양식으로 대체하지 않고 사용자에게 경로를 요청한다.

## 실행

1. 사용자가 만들려는 아티팩트와 요청을 확인한다.
2. `references/specs/`와 `references/workflows/`에서 해당 아티팩트의 Spec과 Workflow를 찾아 모두 읽는다.
3. Workflow가 정한 순서대로 대화한다. 사용자가 명시적으로 가져오라고 한 자료만 초기 컨텍스트로 사용한다.
4. 문제 정의, 완료 기준, 가설, 대안 선택, 칸반 단위처럼 사용자가 소유하는 판단은 제안과 확정을 구분한다.
5. Workflow가 요구하는 승인 시점 전에는 결과물을 확정하거나 작업을 실행하지 않는다.
6. 승인된 결과물은 `references/artifact-compiler.yaml`의 출력 설정에 따라 저장한다. 사용자가 다른 위치를 지정하면 그 위치를 우선한다.
7. 같은 파일이 이미 있으면 자동으로 덮어쓰지 않고, 기존 기록의 갱신인지 새 기록인지 확인한다.

## 아티팩트 선택

현재 요청과 이름이 일치하는 Spec이 하나면 바로 선택한다. 여러 Spec이 일치하거나 이름이 없으면 결과물의 목적을 한 질문으로 확인한다.

해당 아티팩트의 Spec이 아직 없으면 결과물을 임의 양식으로 만들지 않는다. 사용자와 Artifact Spec을 먼저 설계할지 확인한다.

## 완료

다음을 모두 만족하면 한 번의 생성 주기가 끝난다.

- 사용자가 필요한 판단을 직접 선택하거나 수정했다.
- 결과물이 선택한 Spec의 Evaluation을 통과했다.
- 승인된 결과물이 설정된 정본 위치에 저장됐다.
- 저장 위치와 아직 실행하지 않은 작업이 사용자에게 명시됐다.
