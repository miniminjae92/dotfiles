# 규칙별 대화 근거

우테코 대화에서 추출한 기준과 근거를 연결한다. 실행 규칙의 정본은 [SKILL.md](../SKILL.md)이며, 이 파일은 해당 판단을 뒷받침하거나 제한하는 관찰을 보존한다. 전체 469개 발언의 빈도 통계나 인과 효과를 측정한 결과가 아니다. 여러 미션의 질문과 답변을 대조한 정성 검토다. 답변이나 수정이 있었다는 사실만으로 코멘트의 품질을 입증하지 않는다.

## 1. 질문의 대상과 현재 이해를 명확하게 한다

반영: SKILL.md의 `입력과 근거`에 용어와 범위 확인 절차를 추가했다.

- [java-blackjack #1028 질문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911126767)에서는 "애플리케이션 단위"가 무엇인지 먼저 확인했다. [본인 답변](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2917262543)으로 입력, 처리, 출력을 제어하는 유스케이스 검증을 뜻했음이 드러났다. [후속 답변](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2918464071)은 현재 이해와 궁금한 지점을 함께 알려 달라고 구체적으로 설명했다.
- [spring-roomescape-member #499 리뷰](https://github.com/woowacourse/spring-roomescape-member/pull/499#discussion_r3253748620)는 `code`를 HTTP 상태 코드까지 포함해 해석했다. [본인 답변](https://github.com/woowacourse/spring-roomescape-member/pull/499#discussion_r3253918077)에서는 응답 객체의 별도 필드를 뜻했다고 정정했다.

두 사례는 질문을 더 친절하게 쓰는 문제에 앞서, 같은 대상을 이야기하는지 확인할 필요를 보여 준다. 모든 용어를 사전처럼 설명하거나 코드로 알아낼 수 있는 사실을 작성자에게 묻는 근거는 아니다.

## 2. 설계 질문에는 왜 궁금한지 알 수 있는 관찰이 있다

반영: 기존 `설계 선택과 변경 제안` 규칙의 근거를 보강했다.

- [java-mvc #1186 본인 질문](https://github.com/woowacourse/java-mvc/pull/1186#discussion_r4181598909)은 메서드 배치 때문에 읽으며 이동한 경험을 짚고 배치 기준을 물었다. [답변](https://github.com/woowacourse/java-mvc/pull/1186#discussion_r4183034154)은 기능 분리에 집중하며 순서는 놓쳤다는 설명이었다.
- [java-http #1381 본인 질문](https://github.com/woowacourse/java-http/pull/1381#discussion_r4114505168)은 URI를 추가하면 Processor도 수정해야 하는 관계를 먼저 짚고 변경 책임을 물었다.

관찰은 독자의 불편일 수도 있고 구체적인 변경 조건일 수도 있다. 질문 전에 항상 칭찬하거나 모든 코멘트를 같은 세 문장으로 구성해야 한다는 근거는 아니다.

## 3. 현재 선택을 유지하거나 다른 해결책을 택할 여지를 남긴다

반영: 기존 `설계 선택과 변경 제안`과 `code-review`의 대안 비교 기준을 유지한다.

- [java-mvc #1136 질문](https://github.com/woowacourse/java-mvc/pull/1136#discussion_r4161801207)은 `getMethods()`를 언급했지만 허용할 메서드 범위를 물었다. [본인 답변](https://github.com/woowacourse/java-mvc/pull/1136#discussion_r4163590708)은 세 대안을 비교한 뒤 `getDeclaredMethods()`를 유지하고 public 필터를 추가하는 선택을 설명했다.
- [java-http #1200 책임 분리 질문](https://github.com/woowacourse/java-http/pull/1200#discussion_r4053159578)에 [본인 답변](https://github.com/woowacourse/java-http/pull/1200#discussion_r4056043365)은 당시 변경 부담과 분리 비용을 근거로 일부 구조를 유지하겠다고 설명했다.

두 답변 모두 즉시 제안대로 수정하는 것 이외의 판단을 드러낸다. 답변을 실제로 받아들이려면 근거와 현재 코드를 검토해야 하며, "어떻게 생각하세요?"라는 어미만으로 선택권이 생기지는 않는다.

## 4. 코멘트가 요구하는 범위와 현재 미션의 범위를 구분한다

반영: 기존 `전할 말 고르기`와 `code-review`의 계약 확인 기준에 연결한다.

- [java-http #1292 본인 답변](https://github.com/woowacourse/java-http/pull/1292#discussion_r4102240594)은 인증 정보만 새 세션에 담고, 아직 없는 비회원 데이터 이전은 확장하지 않았다고 설명했다. [후속 리뷰](https://github.com/woowacourse/java-http/pull/1292#discussion_r4106244308)는 현재 범위를 받아들이면서 세션 ID 교체와 이전 ID 제거를 확인했다.
- [java-http #1200 본인 답변](https://github.com/woowacourse/java-http/pull/1200#discussion_r4056056600)은 미지정 경로의 응답을 의도한 정상 동작이라고 승인한 것이 아니라 구현 범위를 제한한 것이라고 구분했다.

두 번째 답변 자체가 오류 응답의 안전성이나 적절성을 입증하지는 않는다. 범위 밖이라는 말로 보안 문제나 명시된 계약 위반을 면제하지 않는다. 실제 영향과 계약의 검토가 먼저다.

## 5. 재리뷰는 이전 우려의 해소 여부를 판단한다

반영: 기존 `의도가 이미 설명된 경우` 지침을 질문, 답변, 변경을 잇는 후속 리뷰 절차로 구체화했다.

- [java-http #1381 답변](https://github.com/woowacourse/java-http/pull/1381#discussion_r4114717959) 뒤의 [본인 재리뷰](https://github.com/woowacourse/java-http/pull/1381#discussion_r4115301340)는 Processor에서 구성이 빠진 점과 WAS 패키지에 구성이 남은 점을 구분했다. [다음 답변](https://github.com/woowacourse/java-http/pull/1381#discussion_r4115385719)은 애플리케이션 쪽으로 구성을 옮겼음을 설명했다.
- [java-http #1292 재리뷰](https://github.com/woowacourse/java-http/pull/1292#discussion_r4106244308)는 새 ID 발급뿐 아니라 이전 ID로 인증 상태에 접근할 수 없게 된 결과와 테스트를 짚었다.

재리뷰의 기준은 원래 제시한 구현 형태를 따랐는지가 아니라 우려가 해소됐는지다. 실제 변경을 보지 않은 상태에서는 작성자의 설명과 검증 완료를 구분해야 한다.

## 6. 칭찬은 구체적인 선택과 효과만으로 충분하다

반영: 기존 `긍정적 의견` 규칙의 근거를 보강했다.

- [java-http #1213 본인 코멘트](https://github.com/woowacourse/java-http/pull/1213#discussion_r4060093814)는 UTF-8 바이트 길이와 전송 크기의 일치를 짚었다.
- [java-http #1405 상대방 코멘트](https://github.com/woowacourse/java-http/pull/1405#discussion_r4115315380)는 서로 다른 스레드에서 종료 상태를 읽고 쓰는 조건과 변경을 연결했다. [본인 답변](https://github.com/woowacourse/java-http/pull/1405#discussion_r4115389041)은 스레드 구조를 보며 판단한 과정을 설명했다.

칭찬에 질문을 붙이지 않아도 대화가 이어지는 사례다. 모든 긍정 코멘트가 답변을 유도해야 하거나 "배워갑니다" 같은 감상을 재현해야 한다는 뜻은 아니다.

## 사용자가 선택한 말투 기준

2026-10-10 사용자는 `!`, `~!`, `?`, `네요`, 합니다체가 문장의 역할에 따라 섞이는 방식을 규칙에 넣도록 요청했다. 실행 기준은 SKILL.md의 `문장의 역할에 따른 어미와 부호`에 있다. 코퍼스 전체의 빈도나 효과를 입증한 결과가 아니라, 실제 표현을 검토한 뒤 사용자가 채택한 말투 선호다. 앞서 추출한 판단 기준은 우선 유지하고 실제 출력에서 어색하면 재검토하기로 했다.

## 규칙으로 추출하지 않은 것

- 칭찬으로 시작하기, 해요체만 쓰기, 이모지 의무 사용, 부호의 고정 배합 비율, 고정 문장 수: 원문에도 변이가 있고 적용 조건을 뒷받침하지 못한다. 역할에 따른 어미와 부호의 선택은 위의 사용자 선호를 따른다.
- 모든 지적을 질문형으로 쓰기: 확인된 오류와 선택 가능한 제안의 차이를 흐린다.
- 질문 답변을 받기 위해 RC를 사용하기: 이 자료에서 학습 효과나 상태 선택의 적절성을 일반화할 근거가 없다.
- 과거 리뷰의 기술 결론을 새 미션의 규칙으로 가져오기: 당시 계약과 코드가 다르므로 별도 검증이 필요하다.

## 검증에 사용할 변화

표현의 자연스러움을 정량 검증했다고 주장하지 않는다. 질문 대상이 달라지는 오해를 줄였는지, 해결된 쟁점을 다시 질문하지 않는지, 대안을 구현 지시로 바꾸지 않는지처럼 관찰할 수 있는 출력으로 확인한다. 구체적인 입력과 통과 조건은 [cases.md](cases.md)에 있다.
