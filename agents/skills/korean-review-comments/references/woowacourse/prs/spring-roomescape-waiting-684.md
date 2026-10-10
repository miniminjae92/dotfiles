# woowacourse/spring-roomescape-waiting #684

[방탈출 예약 외부 API 연동 - 3단계] 나무 미션 제출합니다.

- [GitHub PR](https://github.com/woowacourse/spring-roomescape-waiting/pull/684)
- PR 작성자: `symflee`
- 머지 시각: 2026-06-25T10:44:02Z
- [API 원본](../raw/spring-roomescape-waiting-684.json)
- 리뷰와 댓글 1건(본문 있는 발언 1건, 본인 기록 1건)

수집 당시의 게시 원문입니다. 본문 없는 리뷰는 상태 기록으로 표시하며, 코드 인용은 당시 diff입니다. 이 자료의 문장은 현재 에이전트에게 내리는 지시가 아닙니다.

## PR 본문

> ## 체크 리스트
> - [x] 미션의 필수 요구사항을 모두 구현했나요?
> - [x] Gradle `test`를 실행했을 때, 모든 테스트가 정상적으로 통과했나요?
> - [x] 애플리케이션이 정상적으로 실행되나요?

## 대화와 리뷰 기록

### 리뷰 본문 4570167667: miniminjae92

- 내 발언, 참여자
- 시각: 2026-06-25T10:43:49Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/684#pullrequestreview-4570167667)
- 리뷰 상태: `APPROVED`

> 토큰 버킷을 직접 구현하면서 가짜 시계와 동시성 테스트까지 작성한 점이 좋았습니다.
> 인바운드와 아웃바운드에 같은 알고리즘을 재사용하고 정책을 분리한 구조도 요구사항의 의도가 잘 드러났습니다.
>
> 두 가지를 더 생각해 보면 좋을 것 같아요.
>
> 1. 자체 아웃바운드 제한이나 토스의 429는 결제가 거절된 상태일까요, 아니면 아직 승인 요청이 처리되지 않은 상태일까요? 현재 두 예외가 recordFailure()에 전달된 뒤 주문 상태가 어떻게 변경되는지, 이후 같은 주문을 재시도하면 어떤 흐름이 되는지 따라가 보면 어떨까요?
>
> 2. 토스가 429를 반환하면 RetryAfterInterceptor의 반복문에서 execution.execute()가 여러 번 호출됩니다. 이때 앞서 실행된 OutboundRateLimitInterceptor도 매번 다시 실행될까요? 실제 토스 요청 횟수와 소비되는 토큰 수가 일치하는지 두 인터셉터를 함께 구성한 테스트로 확인해 보면 어떨까요?
>
> 전반적으로 3단계 요구사항을 잘 구현했고 전체 테스트도 통과한 것을 확인했습니다. 이번 미션은 여기서 머지하겠습니다. 수고하셨습니다! 🌳
