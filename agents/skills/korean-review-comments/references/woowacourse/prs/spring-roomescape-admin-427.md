# woowacourse/spring-roomescape-admin #427

[🚀 미션 (방탈출 예약 관리)] 고래(강민재) 미션 제출합니다.

- [GitHub PR](https://github.com/woowacourse/spring-roomescape-admin/pull/427)
- PR 작성자: `miniminjae92`
- 머지 시각: 2026-05-04T03:48:01Z
- [API 원본](../raw/spring-roomescape-admin-427.json)
- 리뷰와 댓글 88건(본문 있는 발언 84건, 본인 기록 35건)

수집 당시의 게시 원문입니다. 본문 없는 리뷰는 상태 기록으로 표시하며, 코드 인용은 당시 diff입니다. 이 자료의 문장은 현재 에이전트에게 내리는 지시가 아닙니다.

## PR 본문

> <!--
>
> ## 코드 리뷰 팁
>
> - 코드와 관련된 질문이 있다면, PR 본문에 적기 보다는 해당 코드를 선택하고 코멘트를 남겨주세요.
>   - [참고: Adding comments to a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/commenting-on-a-pull-request#adding-comments-to-a-pull-request)
>
> -->
> ## 체크 리스트
> - [x] 미션의 기능, 프로그래밍, 과제 진행 요구사항을 모두 구현했나요?
> - [x] Gradle `test`를 실행했을 때, 모든 테스트가 정상적으로 통과했나요?
> - [x] 애플리케이션이 정상적으로 실행되나요?
> - [x] `docs/study-log` 하위에 학습 로그를 작성 했나요?
>
> ## 어떤 부분에 집중하여 리뷰해야 할까요?
> <!-- 리뷰어가 효과적으로 피드백할 수 있도록 중점적으로 리뷰 받고 싶은 내용을 *요약* 형태로 작성해 주세요.
> 리뷰해야 할 포인트를 요약해 강조해 주시면, 리뷰어가 코드 전체를 이 부분에 집중해 리뷰할 수 있습니다.
> 반면 특정 코드부분에 대한 피드백이 필요하다면, 이 곳에 적기 보다 해당 코드를 선택하고 코멘트를 남기는 것을 권장합니다. -->
>
> 안녕하세요 찰리! 만나게 되어서 반갑습니다!
>
> 이번 학습 방법론에 대한 고민을 이렇게까지 해 본 적은 사실 살면서 없었습니다.
> 그래서 이번 경험이 새로웠고 정해지지 않은 막무가내식으로 학습하고 있었다고 느끼는 경험이 됐습니다.
> 제가 레벨1부터 일정에 빡빡하게 미션을 진행했는데요.
> 이번 학습법 고민을 하면서 왜 그렇게 됐나를 메타인지에 도움받게 됐습니다.
> 다만 이번 미션 과정 중에서는 후회와 자책이 비중이 컸네요.
> 제가 어려워하는 부분이 처음에 계획을 잡는 부분이 어렵습니다.
> 저는 질문에 꼬리를 물고 들어가는 것을 즐기는데 이러한 모습이 시간 대비 효율에서는 다시 한번 생각해 봐야 하는 문제라고 느꼈습니다.
> 예를 들어서 핵심 요구 사항에 관한 부분은 꼭 테스트로 보장해야 한다고 깨달았었습니다.
> 그래서 테스트해야 할 것과 안 해도 될 것을 먼저 판단했었는데 학습도 깊이?라고 해야 할까요? 주제의 성격에 따라서 전략적으로 다가갈 필요가 있다고 느껴졌습니다.
> 찰리는 한정된 시간(시간이 넉넉한 경우, 부족한 경우)에 낯선 것을 배울 때 어떻게 하시는지 궁금합니다.
>
> ### 📌 리뷰 가이드라인 (지우지 마세요)
> - 기능 요구사항 구현 과정에서 발생한 프레임워크의 사용, 구현에 대한 피드백을 받는다.
>     - 이해되지 않는 부분이 있거나, 고민이 있는 경우, 질문하고 피드백을 받는다.
> - 학습 과정에 대한 피드백을 받는다.
>     - 학습로그 변천사를 알려주고, 학습 방식에 대한 피드백을 받아본다.
> - 학습 도구에 대한 피드백을 받는다.
>     - 학습 도구가 어떤 문제를 해결하려고 했는지, 학습 도구가 실제로 도움이 되는지, 다른 방법은 없을지, 리뷰어에게 피드백을 받는다.
>

## 대화와 리뷰 기록

### 인라인 코멘트 3167768084: Gomding

- 상대방 발언, 참여자
- 시각: 2026-04-30T12:07:23Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167768084)
- 코드: `docs/study-log/README.md`, 현재 줄 1, 원래 줄 1
- 소속 리뷰 ID: 4204932312

> > 제가 어려워하는 부분이 처음에 계획을 잡는 부분이 어렵습니다.
> > 저는 질문에 꼬리를 물고 들어가는 것을 즐기는데 이러한 모습이 시간 대비 효율에서는 다시 한번 생각해 봐야 하는 문제라고 느꼈습니다.
> > 예를 들어서 핵심 요구 사항에 관한 부분은 꼭 테스트로 보장해야 한다고 깨달았었습니다.
> > 그래서 테스트해야 할 것과 안 해도 될 것을 먼저 판단했었는데 학습도 깊이?라고 해야 할까요? 주제의 성격에 따라서 전략적으로 다가갈 필요가 있다고 느껴졌습니다.
> > 찰리는 한정된 시간(시간이 넉넉한 경우, 부족한 경우)에 낯선 것을 배울 때 어떻게 하시는지 궁금합니다.
>
> 한정된 시간이라면 정말 구현에 필요한 지식만 일단 학습할 것 같아요!
> 실무라면 더더욱 그렇구요
> 그 외 호기심은 따로 시간 여유로울때 학습을 하는것이 좋다고 생각해요 ㅎㅎ
> 일단 사용하면서 나오는 인사이트도 분명 있을거예요 :)
> 추가로 생기는 질문들도 있을것이구요. 그런것들을 정리해놨다가 나중에 정리하는거죠.
>
> 아래 글도 참고해볼 수 있겠네요!
> - https://brunch.co.kr/@mystoryg/229#:~:text=%EB%AC%B4%EC%97%87%EC%9D%84%20%EB%A7%8C%EB%93%A4%EC%A7%80%20%EC%A0%95%ED%96%88%EB%8B%A4%EB%A9%B4%20%EA%B7%B8%EA%B2%83%EC%9D%84%20%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0%20%EC%9C%84%ED%95%B4%EC%84%9C%20%ED%95%84%EC%9A%94%ED%95%9C%20%EB%B6%80%EB%B6%84%EB%A7%8C%20%EC%B0%BE%EC%95%84%EC%84%9C%20%EC%A0%81%EC%9A%A9%ED%95%98%EB%8A%94%20%EA%B2%83%EC%9D%B4%EB%8B%A4.
>
>
> > 다만 이번 미션 과정 중에서는 후회와 자책이 비중이 컸네요.
>
> 현재는 후회와 자책을 할 필요는 없다고 생각해요 ㅎㅎ
> 학습하는 과정에서 실패는 당연한것이고 현재는 가장 값싸게 실패할 수 있는 기회이니 마음껏 실패해볼 수 있는 시간이라 봅니다 ㅋㅋ
> 어떤게 효과적이었고 유효한 학습법인지 냉정하게 판단만 하셔도 좋아요!
> 실패조차도 성장의 발판입니다~

### 인라인 코멘트 3167814007: Gomding

- 상대방 발언, 참여자
- 시각: 2026-04-30T12:14:55Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167814007)
- 코드: `docs/study-log/log-01.md`, 현재 줄 21, 원래 줄 21
- 소속 리뷰 ID: 4204932312

> 앞으로 단계에서 계속 가까워질 기회는 있을거예요 ㅎㅎ
> 이제 스프링을 사용하는 첫 미션인데 스프링을 처음 접했다면 벌써 깊어질 수는 없겠죠 😄
> 짧은 시간인데 구현한것만 해도 유효했다고 생각합니다!
>
> 학습은 리뷰 요청해놓고 계속 하시면 되죠! 😔

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,68 @@
+## 학습 로그 #1
+
+**시간**: 04/29 16:00 ~ 23:59 (약 480분)
+**학습 범위**: 1단계 MVC
+
+### 1. 막힌 것의 종류
+이번에 막힌 것은 어떤 종류의 어려움이었는가? (해당하는 것에 체크)
+- [x] 개념 자체를 모르겠다 (예: "스프링 빈이 뭔지 모르겠다")
+- [ ] 개념은 알겠는데 코드로 어떻게 쓰는지 모르겠다 (예: "JdbcTemplate 문법을 모르겠다")
+- [ ] 코드는 돌아가는데 이게 맞는 건지 모르겠다 (예: "계층 분리를 이렇게 해도 되나?")
+- [ ] 기타: ___
+
+### 2. 이번 타임의 학습 전략
+- 이전에 바꾸기로 한 전략은 무엇이었고, 실행했는가?
+- 실제로 어떻게 학습했는지 디테일한 과정을 써보세요.
+
+먼저 바꾸기로 한 전략의 핵심은 학습 목표를 분명히 하고, 바운더리를 정하는 것이었습니다. 그리고 예측을 해본 뒤, 다양한 인풋을 통해 제 생각과의 차이를 느껴보는 것이었습니다. 마지막으로 백지상태에서 아웃풋을 해보는 것이었습니다.
+
+전체적으로 실패했습니다. 그 이유는 스프링 관련 책을 읽다가 중간에 내려놓고 이번 학습법을 적용했어야 했는데, 그러지 못했기 때문입니다. 또한 책을 덮은 뒤에는 마감 시간의 압박감 때문에 학습 목표를 분명하게 세우지 못한 채 AI를 통한 키워드 학습에 들어갔습니다. 다방면으로(Resourceful) 인풋을 채우고 싶었지만, 대부분의 인풋을 AI에 의존하게 되었습니다. 결과적으로 가장 중요한 아웃풋(Output) 단계는 진행하지 못했습니다.
+
+책을 통해 스프링 프레임워크의 개념과 가까워지는 시간을 가졌지만, 깊이 이해했냐고 묻는다면 여전히 부족함을 느낍니다. 빠르게 읽어내려갔고, 학습 테스트나 방탈출 예약 관리 미션을 진행하지 않은 채로 읽었기 때문에 코드를 대하는 관점 자체에 차이가 있었다고 이제서야 느낍니다. 책을 읽는 시간이 가장 길었고, 그 후 학습 테스트 MVC 1, 2를 쫓기듯 진행하게 되면서 공식 문서나 핵심 원리에 대해서는 깊게 학습하지 못한 채 사용법만 간략하게 익히는 데 그쳤습니다.
```

</details>

### 인라인 코멘트 3167826647: Gomding

- 상대방 발언, 참여자
- 시각: 2026-04-30T12:17:07Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167826647)
- 코드: `docs/study-log/log-02.md`, 현재 줄 37, 원래 줄 37
- 소속 리뷰 ID: 4204932312

> 👍 👍

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,64 @@
+## 학습 로그 #2
+
+**시간**: 04/30 06:30 ~ 08:30 (약 120분)
+**학습 범위**: 2단계 DB 연동 (H2 인메모리 DB 설정 및 JdbcTemplate CRUD 전환)
+
+### 1. 막힌 것의 종류
+이번에 막힌 것은 어떤 종류의 어려움이었는가? (해당하는 것에 체크)
+- [ ] 개념 자체를 모르겠다 (예: "스프링 빈이 뭔지 모르겠다")
+- [x] 개념은 알겠는데 코드로 어떻게 쓰는지 모르겠다 (예: "JdbcTemplate 문법을 모르겠다")
+- [ ] 코드는 돌아가는데 이게 맞는 건지 모르겠다 (예: "계층 분리를 이렇게 해도 되나?")
+- [ ] 기타: ___
+
+### 2. 이번 타임의 학습 전략
+
+#### 이전에 바꾸기로 한 전략은 무엇이었고, 실행했는가?
+
+책부터 읽는 완벽주의를 버리고, 주어진 시간에 맞춰 계획을 세운 뒤 돌아가는 최소 기능 코드를 먼저 작성하는 전략이었습니다.
+이번에는 이론서를 덮고 미션 코드를 바로 마주하며 실행했습니다.
+
+#### 실제로 어떻게 학습했는지 디테일한 과정을 써보세요.
+
+미션 2단계 요구사항에 맞춰 환경 설정(build.gradle, application.properties, schema.sql)을 바로 시도했습니다.
+그 과정에서 발생한 작은 의문들이 있었습니다. 예를 들면 IDE의 데이터 소스 경고 or 환경 설정하고 직접 접속하는 방법들을 AI를 이용해서 직접 해보면서 해결했습니다.
+
+기존 List와 AtomicLong을 JdbcTemplate으로 전환하면서 KeyHolder와 JdbcTemplate 사용법 등 낯선 문법을 마주했습니다. 다행히 토비의 스프링 책에서 본 경험이 도움이 조금 되었습니다. 예를 들면 템플릿이라는 용어가 저만의 추상화로 이력서의 경우를 책을 읽으면서 생각해볼 수 있었는데 그러한 도움으로 query, update, keyHolder 들을 사용해가면서 jdbcTemplate가 어떤 형태로 해주겠네?라는 추측을 하는데 도움을 받았습니다.
+
+jdbcTemplate.query(sql, (rs, rowNum) -> ...)의 정체 (RowMapper)
+AtomicLong vs KeyHolder의 본질적 차이 (주도권의 이동)
+prepareStatement(sql, new String[]{"id"})의 역할
+jdbcTemplate.update의 파라미터 흐름 등을 필요한 순간마다 학습을 했습니다.
+
+### 3. 전략 평가
+
+#### 효과적이었던 것과 그 이유
+
+최소 기능 코드 먼저 작성하는 것이 효과적이었습니다.
+코드를 일단 작성하고 에러나 낯선 문법을 눈으로 직접 확인하니 당장에 필요한 부분이 무엇인지, 다음에 학습해야 할 것은 무엇인지, 어디까지 학습하면 되는지 이러한 부분들에 도움을 받았습니다.
```

</details>

### 인라인 코멘트 3167840810: Gomding

- 상대방 발언, 참여자
- 시각: 2026-04-30T12:19:04Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167840810)
- 코드: `docs/study-log/log-02.md`, 현재 줄 42, 원래 줄 42
- 소속 리뷰 ID: 4204932312

> 요즘은 AI 가 코드 작성을 잘 해주기 때문에 직접 작성하는 일은 드물긴해요 ㅎㅎ..
> 물론 직접 작성하는 재미도 있죠! 😄
>
> 중요한건 AI 가 작성해준 코드를 `충분히 이해했는가`, `AI가 작성한 코드에 고래의 의도가 들어가 있는가`, `누군가에게 코드 구조 구현 이유를 설명할 수 있는가` 이런것들을 만족해야한다고 생각해요!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,64 @@
+## 학습 로그 #2
+
+**시간**: 04/30 06:30 ~ 08:30 (약 120분)
+**학습 범위**: 2단계 DB 연동 (H2 인메모리 DB 설정 및 JdbcTemplate CRUD 전환)
+
+### 1. 막힌 것의 종류
+이번에 막힌 것은 어떤 종류의 어려움이었는가? (해당하는 것에 체크)
+- [ ] 개념 자체를 모르겠다 (예: "스프링 빈이 뭔지 모르겠다")
+- [x] 개념은 알겠는데 코드로 어떻게 쓰는지 모르겠다 (예: "JdbcTemplate 문법을 모르겠다")
+- [ ] 코드는 돌아가는데 이게 맞는 건지 모르겠다 (예: "계층 분리를 이렇게 해도 되나?")
+- [ ] 기타: ___
+
+### 2. 이번 타임의 학습 전략
+
+#### 이전에 바꾸기로 한 전략은 무엇이었고, 실행했는가?
+
+책부터 읽는 완벽주의를 버리고, 주어진 시간에 맞춰 계획을 세운 뒤 돌아가는 최소 기능 코드를 먼저 작성하는 전략이었습니다.
+이번에는 이론서를 덮고 미션 코드를 바로 마주하며 실행했습니다.
+
+#### 실제로 어떻게 학습했는지 디테일한 과정을 써보세요.
+
+미션 2단계 요구사항에 맞춰 환경 설정(build.gradle, application.properties, schema.sql)을 바로 시도했습니다.
+그 과정에서 발생한 작은 의문들이 있었습니다. 예를 들면 IDE의 데이터 소스 경고 or 환경 설정하고 직접 접속하는 방법들을 AI를 이용해서 직접 해보면서 해결했습니다.
+
+기존 List와 AtomicLong을 JdbcTemplate으로 전환하면서 KeyHolder와 JdbcTemplate 사용법 등 낯선 문법을 마주했습니다. 다행히 토비의 스프링 책에서 본 경험이 도움이 조금 되었습니다. 예를 들면 템플릿이라는 용어가 저만의 추상화로 이력서의 경우를 책을 읽으면서 생각해볼 수 있었는데 그러한 도움으로 query, update, keyHolder 들을 사용해가면서 jdbcTemplate가 어떤 형태로 해주겠네?라는 추측을 하는데 도움을 받았습니다.
+
+jdbcTemplate.query(sql, (rs, rowNum) -> ...)의 정체 (RowMapper)
+AtomicLong vs KeyHolder의 본질적 차이 (주도권의 이동)
+prepareStatement(sql, new String[]{"id"})의 역할
+jdbcTemplate.update의 파라미터 흐름 등을 필요한 순간마다 학습을 했습니다.
+
+### 3. 전략 평가
+
+#### 효과적이었던 것과 그 이유
+
+최소 기능 코드 먼저 작성하는 것이 효과적이었습니다.
+코드를 일단 작성하고 에러나 낯선 문법을 눈으로 직접 확인하니 당장에 필요한 부분이 무엇인지, 다음에 학습해야 할 것은 무엇인지, 어디까지 학습하면 되는지 이러한 부분들에 도움을 받았습니다.
+
+#### 비효과적이었던 것과 그 이유s
+
+구현 과정에서 AI가 제공하는 코드나 설명에 대한 의존도가 여전히 높았습니다.
+스스로 공식 문서나 기술 블로그(레퍼런스)를 검색하여 코드를 조립해 보는 '날 것의 아웃풋' 과정이 생략되었기 때문에, 온전히 내 힘으로 문법을 작성하는 훈련은 부족했습니다.
```

</details>

### 인라인 코멘트 3167857224: Gomding

- 상대방 발언, 참여자
- 시각: 2026-04-30T12:21:40Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167857224)
- 코드: `docs/study-log/log-03.md`, 현재 줄 61, 원래 줄 61
- 소속 리뷰 ID: 4204932312

> 👍 👍 👍

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,70 @@
+## 학습 로그 #N
+
+**시간**: 04/30 13:00 ~ 14:30 (약 90분)
+**학습 범위**: 3단계 시간 관리
+
+### 1. 막힌 것의 종류
+이번에 막힌 것은 어떤 종류의 어려움이었는가? (해당하는 것에 체크)
+- [ ] 개념 자체를 모르겠다 (예: "스프링 빈이 뭔지 모르겠다")
+- [x] 개념은 알겠는데 코드로 어떻게 쓰는지 모르겠다 (예: "JdbcTemplate 문법을 모르겠다")
+- [x] 코드는 돌아가는데 이게 맞는 건지 모르겠다 (예: "객체와 DB의 부모-자식 관계가 반대로 느껴진다", "테스트가 깨지는데 내 설계가 틀린 건가?")
+- [ ] 기타: ___
+
+### 2. 이번 타임의 학습 전략
+
+[데이터 모델링] FK의 이해: 테이블의 time_id가 어떻게 자바의 ReservationTime 객체로 치환되는지 그 과정을 이해한다.
+[SQL] JOIN의 숙달: 평면적인 reservation 테이블을 JOIN을 통해 입체적인 객체 구조로 복원하는 쿼리 작성에 집중한다.
+[객체지향] 객체 그래프 탐색: Reservation이 ReservationTime을 필드로 가짐으로써 발생하는 '객체 간의 협력' 구조를 익힌다.
+
+- 가지치기(제외할 것):
+  - 새로운 테스트 프레임워크 학습 (제공된 것만 사용)
+  - 복잡한 예외 처리 로직 (ID 미존재 등 최소한의 예외만 처리)
+  - LocalDate 등 시간 타입 고도화 (요구사항대로 String 기반으로 우선 연동)
+
+- 공식문서 타겟팅 참고:
+  - Spring Framework: RowMapper와 INNER JOIN 매핑 규약 (이름 충돌 방지를 위한 SQL Alias 사용, 내부 객체 먼저 조립 -> 외부 객체 조립)
+  - H2 Database: FOREIGN KEY 문법과 예외 처리 (DataIntegrityViolationException)
+  - Jackson: Java 14+의 record 타입 자동 직렬화 지원 확인.
+
+#### 이전에 바꾸기로 한 전략은 무엇이었고, 실행했는가?
+
+학습 프레임워크(고결근: 고민/결정/근거)를 바탕으로, 공식 문서를 처음부터 읽는 대신 코드를 먼저 작성하고 의문이 드는 지점(RowMapper 매핑 방식, record 직렬화)에서만 공식 문서의 예제 코드를 검색하여 확인하는 전략을 실행함.
+
+#### 실제로 어떻게 학습했는지 디테일한 과정을 써보세요.
+
+1. `schema.sql`에 부모 테이블(`reservation_time`)을 먼저 생성하고, 자식 테이블(`reservation`)에 `time_id` FK를 설정함. 도메인은 불변 객체인 `record`로 구성.
+2. 단순 매핑이던 `RowMapper`를 `INNER JOIN` 쿼리에 맞춰 `ReservationTime` 객체를 먼저 조립하고 이를 `Reservation`에 주입함.
+3. `query`와  `queryForObject`의 차이를 학습함.
+4. 객체지향에서는 예약이 예약시간을 포함(Has-A)하여 부모처럼 보였으나, 데이터베이스는 반대로 생명주기 독립성에 따라 예약시간이 부모(PK 제공), 예약이 자식(FK 보유)임을 인지함.
+5. 이전 단계의 테스트 코드가 변경된 스키마(FK 제약 조건)를 위반하여 `DataIntegrityViolationException` 발생. 설계의 오류가 아닌 테스트 데이터 부재임을 파악하고, 테스트 실행 전 부모 데이터를 먼저 생성하도록 테스트를 수정함.
+
+### 3. 전략 평가
+
+#### 효과적이었던 것과 그 이유
+
+시간을 정하고 해당 시간에 맞춰서 무엇에 집중해서 학습할지 먼저 생각했다.
+그리고 그 내용중 공식문서를 참고할 것들을 AI에게 요청을 하여 당장 필요한 개념들에 대해서 학습을 집중적으로 할 수 있었다.
+
+구현을 하면서 객체의 연결과 데이터베이스의 연결에 대해서 시행착오를 겪으면서 글로 학습하는 것보다 더 강렬하게 학습할 수 있었다.
+#### 비효과적이었던 것과 그 이유
+
+초기 예상 시간 60분을 초과하여 90분이 소요됨. 객체와 관계형 DB의 패러다임 불일치(Impedance Mismatch)로 인한 인지적 충돌을 해소하는 시간과, 스키마 변경으로 인해 과거 작성된 레거시 테스트 코드가 연쇄적으로 깨지는 것을 복구하는 시간이 초기 계획에 누락되어 있었음.
+
+#### 막힌 것의 종류(1번)와 전략의 궁합은 어땠는가?
+
+좋았다. 목표 시간 설정과 목표 학습 주제를 전체적인 관점에서 먼저 진행을 하고 했음에도 시간이 오버되는 예외적인 상황이 발생했는데, 그래도 앞서 진행한 계획으로 인해 빠르게 해결할 수 있었다고 생각한다.
+### 4. AI 피드백
+
+#### 자신의 학습 전략에 대해 AI 학습 전문가에게 피드백을 요청하고, 유용했던 제안 1가지 이상 기록
+
+- **객체-관계 패러다임 불일치(Impedance Mismatch)의 이해**: 방향성이 역전된 것처럼 보이는 현상(자바는 예약->시간 포함, DB는 예약->시간 매달림)이 자연스러운 아키텍처적 충돌임을 인지하게 된 것이 가장 유용했음.
+- **통합 테스트의 본질 이해**: 테스트 환경에서 터진 FK 위반 에러(`DataIntegrityViolationException`)가 내 설계의 실패가 아니라, 데이터베이스의 방어막이 정상적으로 작동하고 있다는 증거임을 확인받아 설계에 대한 확신을 가질 수 있었음.
```

</details>

### 인라인 코멘트 3167870317: Gomding

- 상대방 발언, 참여자
- 시각: 2026-04-30T12:24:03Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167870317)
- 코드: `src/main/java/roomescape/controller/ReservationController.java`, 현재 줄 17, 원래 줄 16
- 소속 리뷰 ID: 4204932312

> `@Controller` 와 `@RestController` 의 차이점은 무엇일까요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,41 @@
+package roomescape.controller;
+
+import java.util.List;
+import org.springframework.http.ResponseEntity;
+import org.springframework.web.bind.annotation.DeleteMapping;
+import org.springframework.web.bind.annotation.GetMapping;
+import org.springframework.web.bind.annotation.PathVariable;
+import org.springframework.web.bind.annotation.PostMapping;
+import org.springframework.web.bind.annotation.RequestBody;
+import org.springframework.web.bind.annotation.RequestMapping;
+import org.springframework.web.bind.annotation.RestController;
+import roomescape.domain.Reservation;
+import roomescape.dto.ReservationRequest;
+import roomescape.service.ReservationService;
+
+@RestController
```

</details>

### 인라인 코멘트 3167875754: Gomding

- 상대방 발언, 참여자
- 시각: 2026-04-30T12:25:01Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167875754)
- 코드: `src/main/java/roomescape/dao/ReservationTimeDao.java`, 현재 줄 None, 원래 줄 25
- 소속 리뷰 ID: 4204932312

> ReservationDao 에서는 rowMapper 를 필드로 만드셨던데
> 여기는 그렇지 않으셨군요!
>
> 이유가 있었을까요? 😄

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,54 @@
+package roomescape.dao;
+
+import java.sql.PreparedStatement;
+import java.util.List;
+import java.util.Objects;
+import org.springframework.jdbc.core.JdbcTemplate;
+import org.springframework.jdbc.support.GeneratedKeyHolder;
+import org.springframework.jdbc.support.KeyHolder;
+import org.springframework.stereotype.Repository;
+import roomescape.domain.ReservationTime;
+
+@Repository
+public class ReservationTimeDao {
+    private final JdbcTemplate jdbcTemplate;
+
+    public ReservationTimeDao(JdbcTemplate jdbcTemplate) {
+        this.jdbcTemplate = jdbcTemplate;
+    }
+
+    public List<ReservationTime> findAll() {
+        String sql = "SELECT id, start_at FROM reservation_time";
+        return jdbcTemplate.query(sql, (rs, rowNum) -> new ReservationTime(
+                rs.getLong("id"),
+                rs.getString("start_at")
+        ));
```

</details>

### 인라인 코멘트 3167878729: Gomding

- 상대방 발언, 참여자
- 시각: 2026-04-30T12:25:32Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167878729)
- 코드: `src/main/java/roomescape/dao/ReservationDao.java`, 현재 줄 None, 원래 줄 17
- 소속 리뷰 ID: 4204932312

> [NamedParameterJdbcTemplate](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/jdbc/core/namedparam/NamedParameterJdbcTemplate.html) 도 학습해보셨을까요? 😃

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,70 @@
+package roomescape.dao;
+
+import java.sql.PreparedStatement;
+import java.util.List;
+import java.util.Objects;
+import org.springframework.jdbc.core.JdbcTemplate;
+import org.springframework.jdbc.core.RowMapper;
+import org.springframework.jdbc.support.GeneratedKeyHolder;
+import org.springframework.jdbc.support.KeyHolder;
+import org.springframework.stereotype.Repository;
+import roomescape.domain.Reservation;
+import roomescape.domain.ReservationTime;
+import roomescape.dto.ReservationRequest;
+
+@Repository
+public class ReservationDao {
+    private final JdbcTemplate jdbcTemplate;
```

</details>

### 인라인 코멘트 3167881423: Gomding

- 상대방 발언, 참여자
- 시각: 2026-04-30T12:26:01Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167881423)
- 코드: `src/main/java/roomescape/dao/ReservationDao.java`, 현재 줄 None, 원래 줄 53
- 소속 리뷰 ID: 4204932312

> SimpleJdbcInsert 도 학습해보시죠!
>
> - https://hyeon9mak.github.io/easy-insert-with-simplejdbcinsert/

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,70 @@
+package roomescape.dao;
+
+import java.sql.PreparedStatement;
+import java.util.List;
+import java.util.Objects;
+import org.springframework.jdbc.core.JdbcTemplate;
+import org.springframework.jdbc.core.RowMapper;
+import org.springframework.jdbc.support.GeneratedKeyHolder;
+import org.springframework.jdbc.support.KeyHolder;
+import org.springframework.stereotype.Repository;
+import roomescape.domain.Reservation;
+import roomescape.domain.ReservationTime;
+import roomescape.dto.ReservationRequest;
+
+@Repository
+public class ReservationDao {
+    private final JdbcTemplate jdbcTemplate;
+
+    private final RowMapper<Reservation> rowMapper = (rs, rowNum) -> {
+        ReservationTime time = new ReservationTime(
+                rs.getLong("time_id"),
+                rs.getString("start_at")
+        );
+        return new Reservation(
+                rs.getLong("reservation_id"),
+                rs.getString("name"),
+                rs.getString("date"),
+                time
+        );
+    };
+
+    public ReservationDao(JdbcTemplate jdbcTemplate) {
+        this.jdbcTemplate = jdbcTemplate;
+    }
+
+    public List<Reservation> findAll() {
+        String sql = """
+                SELECT
+                    r.id as reservation_id,
+                    r.name,
+                    r.date,
+                    t.id as time_id,
+                    t.start_at
+                FROM reservation as r
+                INNER JOIN reservation_time as t
+                  ON r.time_id = t.id
+                """;
+        return jdbcTemplate.query(sql, rowMapper);
+    }
+
+    public Long save(ReservationRequest request) {
+        String sql = "INSERT INTO reservation (name, date, time_id) VALUES (?, ?, ?)";
+        KeyHolder keyHolder = new GeneratedKeyHolder();
```

</details>

### 인라인 코멘트 3167891353: Gomding

- 상대방 발언, 참여자
- 시각: 2026-04-30T12:27:40Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167891353)
- 코드: `src/main/java/roomescape/domain/Reservation.java`, 현재 줄 None, 원래 줄 4
- 소속 리뷰 ID: 4204932312

> record 는 가지고 있는 모든 값으로 동등성을 비교하는데요
> 도메인에서 Entity 라는 개념이 있어요 (DB 의 Entity 와 다른겁니다)
> 도메인 Entity 는 id 를 기준으로 동등성을 비교합니다.
> 예를들면 `주민등록번호` 를 보면 개명을 해도 똑같은 사람이라 판단하죠?
> 도메인 Entity 도 비슷한 개념입니다. id 를 기준으로 판단하는 객체입니다
>
> `도메인 Entity vs Value Object` 키워드로 학습해보시면 좋겠어요!
> 둘은 왜 구분을 하는가? 라는 관점에서도 학습해볼 수 있어요~

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,9 @@
+package roomescape.domain;
+
+public record Reservation(
+        Long id,
```

</details>

### 인라인 코멘트 3167906721: Gomding

- 상대방 발언, 참여자
- 시각: 2026-04-30T12:30:22Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167906721)
- 코드: `src/main/java/roomescape/service/ReservationService.java`, 현재 줄 None, 원래 줄 26
- 소속 리뷰 ID: 4204932312

> 과거 날짜로 예약을 생성하려고 하면 어떻게 처리하는게 좋을까요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,35 @@
+package roomescape.service;
+
+import java.util.List;
+import org.springframework.stereotype.Service;
+import roomescape.dao.ReservationDao;
+import roomescape.dao.ReservationTimeDao;
+import roomescape.domain.Reservation;
+import roomescape.domain.ReservationTime;
+import roomescape.dto.ReservationRequest;
+
+@Service
+public class ReservationService {
+    private final ReservationDao reservationDao;
+    private final ReservationTimeDao reservationTimeDao;
+
+    public ReservationService(ReservationDao reservationDao, ReservationTimeDao reservationTimeDao) {
+        this.reservationDao = reservationDao;
+        this.reservationTimeDao = reservationTimeDao;
+    }
+
+    public List<Reservation> findAllReservations() {
+        return reservationDao.findAll();
+    }
+
+    public Reservation createReservation(ReservationRequest request) {
+        Long generatedId = reservationDao.save(request);
```

</details>

### 인라인 코멘트 3167908186: Gomding

- 상대방 발언, 참여자
- 시각: 2026-04-30T12:30:36Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167908186)
- 코드: `src/main/java/roomescape/service/ReservationService.java`, 현재 줄 None, 원래 줄 26
- 소속 리뷰 ID: 4204932312

> 존재하지 않는 timeId 로 요청이 온다면 어떻게 처리해야할까요!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,35 @@
+package roomescape.service;
+
+import java.util.List;
+import org.springframework.stereotype.Service;
+import roomescape.dao.ReservationDao;
+import roomescape.dao.ReservationTimeDao;
+import roomescape.domain.Reservation;
+import roomescape.domain.ReservationTime;
+import roomescape.dto.ReservationRequest;
+
+@Service
+public class ReservationService {
+    private final ReservationDao reservationDao;
+    private final ReservationTimeDao reservationTimeDao;
+
+    public ReservationService(ReservationDao reservationDao, ReservationTimeDao reservationTimeDao) {
+        this.reservationDao = reservationDao;
+        this.reservationTimeDao = reservationTimeDao;
+    }
+
+    public List<Reservation> findAllReservations() {
+        return reservationDao.findAll();
+    }
+
+    public Reservation createReservation(ReservationRequest request) {
+        Long generatedId = reservationDao.save(request);
```

</details>

### 인라인 코멘트 3167913320: Gomding

- 상대방 발언, 참여자
- 시각: 2026-04-30T12:31:28Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167913320)
- 코드: `src/main/java/roomescape/service/ReservationService.java`, 현재 줄 59, 원래 줄 34
- 소속 리뷰 ID: 4204932312

> 멱등성을 고려한다면 그냥 삭제해도 상관없지만
>
> 존재하지 않는 Reservation 에 대해서 삭제하려고 할 때
> 예외를 던져서 이미 삭제됐다는것을 알려줄 수도 있을것 같아요.
> 고래는 어떻게 생각하시나요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,35 @@
+package roomescape.service;
+
+import java.util.List;
+import org.springframework.stereotype.Service;
+import roomescape.dao.ReservationDao;
+import roomescape.dao.ReservationTimeDao;
+import roomescape.domain.Reservation;
+import roomescape.domain.ReservationTime;
+import roomescape.dto.ReservationRequest;
+
+@Service
+public class ReservationService {
+    private final ReservationDao reservationDao;
+    private final ReservationTimeDao reservationTimeDao;
+
+    public ReservationService(ReservationDao reservationDao, ReservationTimeDao reservationTimeDao) {
+        this.reservationDao = reservationDao;
+        this.reservationTimeDao = reservationTimeDao;
+    }
+
+    public List<Reservation> findAllReservations() {
+        return reservationDao.findAll();
+    }
+
+    public Reservation createReservation(ReservationRequest request) {
+        Long generatedId = reservationDao.save(request);
+        ReservationTime time = reservationTimeDao.findById(request.timeId());
+
+        return request.toEntity(generatedId, time);
+    }
+
+    public void deleteReservation(Long id) {
+        reservationDao.deleteById(id);
+    }
```

</details>

### 인라인 코멘트 3167915470: Gomding

- 상대방 발언, 참여자
- 시각: 2026-04-30T12:31:51Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167915470)
- 코드: `src/main/java/roomescape/service/ReservationService.java`, 현재 줄 None, 원래 줄 25
- 소속 리뷰 ID: 4204932312

> `@Transactional` 에 대해서 학습해보셨을까요? 😃

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,35 @@
+package roomescape.service;
+
+import java.util.List;
+import org.springframework.stereotype.Service;
+import roomescape.dao.ReservationDao;
+import roomescape.dao.ReservationTimeDao;
+import roomescape.domain.Reservation;
+import roomescape.domain.ReservationTime;
+import roomescape.dto.ReservationRequest;
+
+@Service
+public class ReservationService {
+    private final ReservationDao reservationDao;
+    private final ReservationTimeDao reservationTimeDao;
+
+    public ReservationService(ReservationDao reservationDao, ReservationTimeDao reservationTimeDao) {
+        this.reservationDao = reservationDao;
+        this.reservationTimeDao = reservationTimeDao;
+    }
+
+    public List<Reservation> findAllReservations() {
+        return reservationDao.findAll();
+    }
+
+    public Reservation createReservation(ReservationRequest request) {
```

</details>

### 인라인 코멘트 3167917794: Gomding

- 상대방 발언, 참여자
- 시각: 2026-04-30T12:32:16Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167917794)
- 코드: `src/test/http/api-test.http`, 현재 줄 1, 원래 줄 1
- 소속 리뷰 ID: 4204932312

> api 테스트를 잘 해주셨네요 💯 💯 💯
>

### 인라인 코멘트 3167921754: Gomding

- 상대방 발언, 참여자
- 시각: 2026-04-30T12:32:54Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167921754)
- 코드: `src/main/java/roomescape/domain/Reservation.java`, 현재 줄 None, 원래 줄 3
- 소속 리뷰 ID: 4204932312

> 레벨1처럼 객체가 생성될 떄 값들에 대해서 검증하지 않아도 괜찮을까요?
> - null 검사 같은..
> Reservation 객체에서 필수값은 무엇인가요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,9 @@
+package roomescape.domain;
+
+public record Reservation(
```

</details>

### 인라인 코멘트 3167926841: Gomding

- 상대방 발언, 참여자
- 시각: 2026-04-30T12:33:47Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167926841)
- 코드: `src/main/java/roomescape/service/ReservationTimeService.java`, 현재 줄 None, 원래 줄 22
- 소속 리뷰 ID: 4204932312

> 동일한 타임슬롯을 생성할 수 있을까요?
>
> 13:00 이라는 데이터를 가진 ReservationTime 이 2개 존재해도 되는지?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,29 @@
+package roomescape.service;
+
+import java.util.List;
+import org.springframework.stereotype.Service;
+import roomescape.dao.ReservationTimeDao;
+import roomescape.domain.ReservationTime;
+import roomescape.dto.ReservationTimeRequest;
+
+@Service
+public class ReservationTimeService {
+    private final ReservationTimeDao reservationTimeDao;
+
+    public ReservationTimeService(ReservationTimeDao reservationTimeDao) {
+        this.reservationTimeDao = reservationTimeDao;
+    }
+
+    public List<ReservationTime> findAll() {
+        return reservationTimeDao.findAll();
+    }
+
+    public ReservationTime create(ReservationTimeRequest request) {
+        Long generatedId = reservationTimeDao.save(request.startAt());
```

</details>

### 인라인 코멘트 3167929683: Gomding

- 상대방 발언, 참여자
- 시각: 2026-04-30T12:34:16Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167929683)
- 코드: `src/main/java/roomescape/controller/ReservationTimeController.java`, 현재 줄 None, 원래 줄 32
- 소속 리뷰 ID: 4204932312

> ResponseEntity 사용 👍 👍 👍
> 다른 방법도 있을것 같은데 ResponseEntity 의 장점은 무엇일까요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,42 @@
+package roomescape.controller;
+
+import java.util.List;
+import org.springframework.http.ResponseEntity;
+import org.springframework.web.bind.annotation.DeleteMapping;
+import org.springframework.web.bind.annotation.GetMapping;
+import org.springframework.web.bind.annotation.PathVariable;
+import org.springframework.web.bind.annotation.PostMapping;
+import org.springframework.web.bind.annotation.RequestBody;
+import org.springframework.web.bind.annotation.RequestMapping;
+import org.springframework.web.bind.annotation.RestController;
+import roomescape.domain.ReservationTime;
+import roomescape.dto.ReservationTimeRequest;
+import roomescape.service.ReservationTimeService;
+
+@RestController
+@RequestMapping("/times")
+public class ReservationTimeController {
+
+    private final ReservationTimeService reservationTimeService;
+
+    public ReservationTimeController(ReservationTimeService reservationTimeService) {
+        this.reservationTimeService = reservationTimeService;
+    }
+
+    @GetMapping
+    public List<ReservationTime> read() {
+        return reservationTimeService.findAll();
+    }
+
+    @PostMapping
+    public ResponseEntity<ReservationTime> create(@RequestBody ReservationTimeRequest request) {
```

</details>

### 인라인 코멘트 3167934430: Gomding

- 상대방 발언, 참여자
- 시각: 2026-04-30T12:35:08Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167934430)
- 코드: `src/main/java/roomescape/service/ReservationService.java`, 현재 줄 17, 원래 줄 12
- 소속 리뷰 ID: 4204932312

> 지금은 Service 테스트가 없는데요
> 특별한 검증이 없어서 구현하지 않았다고 생각되네요!
> 코멘트에 대해 반영하다보면 몇가지 검증할 것들이 생길것 같네요 :)

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,35 @@
+package roomescape.service;
+
+import java.util.List;
+import org.springframework.stereotype.Service;
+import roomescape.dao.ReservationDao;
+import roomescape.dao.ReservationTimeDao;
+import roomescape.domain.Reservation;
+import roomescape.domain.ReservationTime;
+import roomescape.dto.ReservationRequest;
+
+@Service
+public class ReservationService {
```

</details>

### 리뷰 본문 4204932312: Gomding

- 상대방 발언, 참여자
- 시각: 2026-04-30T12:36:11Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#pullrequestreview-4204932312)
- 리뷰 상태: `CHANGES_REQUESTED`

> 안녕하세요 고래!
> 방탈출 예약 관리 미션 함께하게된 찰리입니다 🙇
> 학습로그 잘 작성해주셨네요 👍
> 몇가지 의견 남겼으니 함께 고민해보면 좋겠어요~
>
> 궁금한 점 있으면 언제든 DM 이나 코멘트 남겨주세요!

### 인라인 코멘트 3171514464: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-01T00:20:22Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3171514464)
- 코드: `docs/study-log/README.md`, 현재 줄 1, 원래 줄 1
- 답변 대상: [코멘트 3167768084](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167768084)
- 소속 리뷰 ID: 4209307700

> "성장에 집착하는 순간 성장은 더 이상 성장이 아니다. 그것은 곧 불행이고 괴로움이 된다. 그럼에도 불구하고 우리는 해야만 할 때가 있다." 글이 좋네요! 도움이 됐습니다. 헬퍼스 하이를 자주 느낄 수 있도록 해봐야겠어요~

### 리뷰 본문 4209307700: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-01T00:20:22Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#pullrequestreview-4209307700)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 3171523255: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-01T00:22:21Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3171523255)
- 코드: `docs/study-log/log-01.md`, 현재 줄 21, 원래 줄 21
- 답변 대상: [코멘트 3167814007](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167814007)
- 소속 리뷰 ID: 4209317379

> 마음이 급했나 봅니다. 조언 감사합니다!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,68 @@
+## 학습 로그 #1
+
+**시간**: 04/29 16:00 ~ 23:59 (약 480분)
+**학습 범위**: 1단계 MVC
+
+### 1. 막힌 것의 종류
+이번에 막힌 것은 어떤 종류의 어려움이었는가? (해당하는 것에 체크)
+- [x] 개념 자체를 모르겠다 (예: "스프링 빈이 뭔지 모르겠다")
+- [ ] 개념은 알겠는데 코드로 어떻게 쓰는지 모르겠다 (예: "JdbcTemplate 문법을 모르겠다")
+- [ ] 코드는 돌아가는데 이게 맞는 건지 모르겠다 (예: "계층 분리를 이렇게 해도 되나?")
+- [ ] 기타: ___
+
+### 2. 이번 타임의 학습 전략
+- 이전에 바꾸기로 한 전략은 무엇이었고, 실행했는가?
+- 실제로 어떻게 학습했는지 디테일한 과정을 써보세요.
+
+먼저 바꾸기로 한 전략의 핵심은 학습 목표를 분명히 하고, 바운더리를 정하는 것이었습니다. 그리고 예측을 해본 뒤, 다양한 인풋을 통해 제 생각과의 차이를 느껴보는 것이었습니다. 마지막으로 백지상태에서 아웃풋을 해보는 것이었습니다.
+
+전체적으로 실패했습니다. 그 이유는 스프링 관련 책을 읽다가 중간에 내려놓고 이번 학습법을 적용했어야 했는데, 그러지 못했기 때문입니다. 또한 책을 덮은 뒤에는 마감 시간의 압박감 때문에 학습 목표를 분명하게 세우지 못한 채 AI를 통한 키워드 학습에 들어갔습니다. 다방면으로(Resourceful) 인풋을 채우고 싶었지만, 대부분의 인풋을 AI에 의존하게 되었습니다. 결과적으로 가장 중요한 아웃풋(Output) 단계는 진행하지 못했습니다.
+
+책을 통해 스프링 프레임워크의 개념과 가까워지는 시간을 가졌지만, 깊이 이해했냐고 묻는다면 여전히 부족함을 느낍니다. 빠르게 읽어내려갔고, 학습 테스트나 방탈출 예약 관리 미션을 진행하지 않은 채로 읽었기 때문에 코드를 대하는 관점 자체에 차이가 있었다고 이제서야 느낍니다. 책을 읽는 시간이 가장 길었고, 그 후 학습 테스트 MVC 1, 2를 쫓기듯 진행하게 되면서 공식 문서나 핵심 원리에 대해서는 깊게 학습하지 못한 채 사용법만 간략하게 익히는 데 그쳤습니다.
```

</details>

### 리뷰 본문 4209317379: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-01T00:22:22Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#pullrequestreview-4209317379)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 3173295615: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-01T13:18:06Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3173295615)
- 코드: `src/main/java/roomescape/controller/ReservationController.java`, 현재 줄 17, 원래 줄 16
- 답변 대상: [코멘트 3167870317](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167870317)
- 소속 리뷰 ID: 4211266115

> #### 공부하기 전 내 예측
>
> 컨트롤러 용어의 의미가 클라이언트가 요청하면 서버가 응답하는 창구라고 생각합니다.
> REST는 Representational State Transfer의 약어로 알고 있습니다.
> Representational은 표현으로 HTML이나 JSON 등 애플리케이션을 표현할 수 있는 데이터라고 생각하고, State Trnasfer는 애플리케이션의 상태를 Representation을 요청/응답하면서 전이하는 구조라고 생각합니다.
> 스프링에서의 `@Controller와` `@RestController`는 학습 테스트를 통해서 경험을 했습니다.
> `@Controller`일 때는 클라이언트의 요청에 HTML을 반환했습니다.
> `@RestController`의 경우 반환으로 객체로 응답했는데 그 객체를 Jackson 라이브러리가 JSON으로 직렬화한다고 들었습니다. 또한 RestController는 Controller + ResponseBody라고 들었습니다.
> 알고있는 지식으로 예측을 해보자면 RestController는 기존 Controller에서 ResponseBody 기능이 추가된 것으로 예측이 됩니다.
> ResponseBody가 무엇일까? 생각해보면 HTTP 응답의 Representation의 body를 자동으로 채워주는 기능이지 않을까 예측됩니다.
> `@Controller`는 완성된 HTML을 서버에서 응답하는 SSR인 경우에 사용하고 `@RestController`는 필요한 데이터만을 제공할 때 사용한다고 예측됩니다.
>
> #### 학습 후 답변
>
> `@ResponseBody` 어노테이션의 기본 적용 여부입니다.
> 그로 인해 응답으로 뷰(HTML) or Representation(JSON, XML 등)을 선택할 수 있습니다.
>
> `@Controller`는 주로 뷰를 반환할 때 사용됩니다. 컨트롤러 메서드에서 String(뷰 이름)을 반환하면, DispatcherServlet이 이를 전달받아 ViewResolver를 호출합니다. 이후 템플릿 엔진을 통해 HTML 뷰가 렌더링되어 응답됩니다.
>
> 반면 `@RestController`는 클래스 레벨에 `@ResponseBody`가 결합된 어노테이션으로, 주 목적은 객체 데이터를 직접 반환하는 것입니다. 이 경우 DispatcherServlet은 ViewResolver를 우회하고, 응답 처리를 HttpMessageConverter에게 위임합니다. 반환된 자바 객체는 클라이언트 요청의 HTTP Accept 헤더와 메서드의 반환 타입을 기반으로 적절한 Converter를 찾아 변환됩니다.
>
> 예를 들어 클라이언트가 application/json을 요구할 경우, MappingJackson2HttpMessageConverter가 개입하여 Jackson 라이브러리를 통해 자바 객체를 JSON으로 직렬화한 뒤 HTTP 응답 본문에 담아 반환합니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,41 @@
+package roomescape.controller;
+
+import java.util.List;
+import org.springframework.http.ResponseEntity;
+import org.springframework.web.bind.annotation.DeleteMapping;
+import org.springframework.web.bind.annotation.GetMapping;
+import org.springframework.web.bind.annotation.PathVariable;
+import org.springframework.web.bind.annotation.PostMapping;
+import org.springframework.web.bind.annotation.RequestBody;
+import org.springframework.web.bind.annotation.RequestMapping;
+import org.springframework.web.bind.annotation.RestController;
+import roomescape.domain.Reservation;
+import roomescape.dto.ReservationRequest;
+import roomescape.service.ReservationService;
+
+@RestController
```

</details>

### 인라인 코멘트 3173510054: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-01T14:15:57Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3173510054)
- 코드: `src/main/java/roomescape/controller/ReservationTimeController.java`, 현재 줄 None, 원래 줄 32
- 답변 대상: [코멘트 3167929683](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167929683)
- 소속 리뷰 ID: 4211266115

> #### 공부하기 전 내 예측
>
> `@GetMapping`에는 객체를 반환했습니다. 여기서 의문이 생기는데요.
> `@ResponseBody`로 인해 JSON으로 직렬화해서 body를 생성할텐데, 응답코드는 어떻게 되는걸까요?
> ResponseEntity는 응답 엔티티일텐데, 응답 내용에 대해서 수동 조작이 필요한 경우에 사용할 수 있는 장점이 있을 것 같습니다.
> 다른 방법은 떠오르질 않네요.
> #### 학습 후 답변
>
> 별도의 설정이나 예외 발생이 없다면, HTTP 상태코드는 200 OK로 설정되어 반환되는 것을 학습했습니다.
> 컨트롤러의 메서드가 예외 없이 정상적으로 마쳤다면 RequestResponseBodyMethodProcessor가 추가적인 지시인 ResponseEntity or ResponseStatus가 없는지 확인합니다.
> 지시가 없다면 Tomcat이 처음 생성한 HttpServletResponse.SC_OK, 200 OK 그대로 사용합니다.
>
> ResponseEntity를 사용하면 3가지를 동적으로 제어할 수 있습니다.
> 1. Status code
> 2. Header
> 3. Response body
>
> POST의 경우 성공 시 created 메서드를 사용해서 URI 정보를 응답 정보에 담을 수 있습니다.
> 자유로운 수동 조작이 가능하기 때문에 조건에 따른 동적 응답이 가능합니다.
> 로직에 따라서 응답 형태를 수동 조작할 수 있는 장점이 있습니다.
>
> 궁금한 부분이 생겼습니다.
> 미션 안내사항에서 아래의 사진과 같이 API 명세서가 명시되어 있는데, 이러한 경우에는 응답 코드는 아직 정해지지 않은건지 모르겠습니다.
>
> <img width="650" height="229" alt="Image" src="https://github.com/user-attachments/assets/d199e32e-eb79-446b-a1cf-622cf9c5527c" />
>
> 그리고 아래의 지금 다시 확인해보니 예시라고 되어있어 이러한 부분들은 제가 판단해서 바꿨어도 괜찮았는지 궁금합니다. 제 생각은 요구사항이 아니라 예시이기 때문에 변경했어도 좋았을 것이라고 판단됩니다.
> 하지만 `요구사항에서 RestAssured가 주어진 경우 그대로 사용하되, 그 위에 새 테스트 기법을 쌓지 않는다.`때문에 200 OK를 사용을 했는데 이러한 부분에서 고민이 됩니다.
>
> ```http
> POST /reservations HTTP/1.1
> Content-Type: application/json
>
> {
>     "date": "2023-08-05",
>     "name": "브라운",
>     "timeId": 1
> }
>
> HTTP/1.1 200
> Content-Type: application/json
>
> {
>     "id": 1,
>     "name": "브라운",
>     "date": "2023-08-05",
>     "time": {
>         "id": 1,
>         "startAt": "10:00"
>     }
> }
>
> ```
>
> 미션 테스트를 지켜야 해서 200 OK를 사용해야 한다면
> `@ResponseStatus`를 사용해서 정적으로 설정하는 방법
> ResponseEntity를 사용하지 않고 객체를 반환하는 방법
> 두 가지 추가적인 방법이 떠올랐습니다.
>
> IETF(국제 인터넷 표준화 기구) RFC 9110에서 아래의 내용을 확인했습니다.
>
> ### 1. RFC 9110 - Section 9.3.3. POST (POST 요청의 처리 결과)
>
> > "If one or more resources has been created on the origin server as a result of successfully processing a POST request, the origin server SHOULD send a 201 (Created) response containing a Location header field..."
>
> 해석: POST 요청을 성공적으로 처리한 결과로 서버에 하나 이상의 리소스가 생성된 경우, 서버는 `Location` 헤더 필드가 포함된 201 (Created) 응답을 보내야 합니다(SHOULD).
>
> ### 2. RFC 9110 - Section 15.3.2. 201 Created (201 상태 코드의 정의)
>
> > "The 201 (Created) status code indicates that the request has been fulfilled and has resulted in one or more new resources being created. The primary resource created by the request is identified by either a Location header field in the response or, if no Location field is received, by the effective request URI."
>
> 해석: `201 (Created)` 상태 코드는 요청이 성공적으로 처리되었으며, 그 결과로 새로운 리소스가 생성되었음을 나타냅니다. 생성된 리소스의 식별자(위치)는 응답의 `Location` 헤더를 통해 알려줍니다.
>
> 위의 내용에 맞춰서 아래처럼 수정하는 것이 적절한건지, 아니면 다른 방법이 있는지 궁금합니다.
>
> ```java
> URI location = URI.create("/times/" + time.getId());
> return ResponseEntity.created(location).body(time);
> ```
>

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,42 @@
+package roomescape.controller;
+
+import java.util.List;
+import org.springframework.http.ResponseEntity;
+import org.springframework.web.bind.annotation.DeleteMapping;
+import org.springframework.web.bind.annotation.GetMapping;
+import org.springframework.web.bind.annotation.PathVariable;
+import org.springframework.web.bind.annotation.PostMapping;
+import org.springframework.web.bind.annotation.RequestBody;
+import org.springframework.web.bind.annotation.RequestMapping;
+import org.springframework.web.bind.annotation.RestController;
+import roomescape.domain.ReservationTime;
+import roomescape.dto.ReservationTimeRequest;
+import roomescape.service.ReservationTimeService;
+
+@RestController
+@RequestMapping("/times")
+public class ReservationTimeController {
+
+    private final ReservationTimeService reservationTimeService;
+
+    public ReservationTimeController(ReservationTimeService reservationTimeService) {
+        this.reservationTimeService = reservationTimeService;
+    }
+
+    @GetMapping
+    public List<ReservationTime> read() {
+        return reservationTimeService.findAll();
+    }
+
+    @PostMapping
+    public ResponseEntity<ReservationTime> create(@RequestBody ReservationTimeRequest request) {
```

</details>

### 인라인 코멘트 3173611086: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-01T14:44:03Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3173611086)
- 코드: `src/main/java/roomescape/dao/ReservationDao.java`, 현재 줄 None, 원래 줄 17
- 답변 대상: [코멘트 3167878729](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167878729)
- 소속 리뷰 ID: 4211266115

> 오, 좋은 클래스네요! 적용해보겠습니다.
>
> ```java
> // SQL 쿼리
> String sql = "INSERT INTO reservation (name, date, time_id) VALUES (?, ?, ?)";
>
> // Java 바인딩 코드
> ps.setString(1, request.name());
> ps.setString(2, request.date());
> ps.setLong(3, request.timeId());
> ```
>
> ```java
> // SQL 쿼리
> String sql = "INSERT INTO reservation (name, date, time_id) VALUES (:name, :date, :timeId)";
>
> // Java 바인딩 코드 (순서가 뒤죽박죽이어도 상관없음)
> SqlParameterSource parameters = new MapSqlParameterSource()
>         .addValue("timeId", request.timeId()) // 3번째 값을 제일 먼저 넣음
>         .addValue("name", request.name())     // 1번째 값을 두 번째로 넣음
>         .addValue("date", request.date());    // 2번째 값을 마지막에 넣음
> ```
>
> 안그래도 이번 미션을 진행하다가 순서로 인해서 디버깅과 해결 시간이 오래 걸렸습니다.
>
> 이 방법을 사용하면 가독성 또한 좋아질 것 같습니다.
>
> '왜 Map말고 SqlParameterSource을 사용하면 좋은걸까?' 의문이 생겼습니다.
> null 처리 안정성을 확인했는데 다른 이점도 있을까요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,70 @@
+package roomescape.dao;
+
+import java.sql.PreparedStatement;
+import java.util.List;
+import java.util.Objects;
+import org.springframework.jdbc.core.JdbcTemplate;
+import org.springframework.jdbc.core.RowMapper;
+import org.springframework.jdbc.support.GeneratedKeyHolder;
+import org.springframework.jdbc.support.KeyHolder;
+import org.springframework.stereotype.Repository;
+import roomescape.domain.Reservation;
+import roomescape.domain.ReservationTime;
+import roomescape.dto.ReservationRequest;
+
+@Repository
+public class ReservationDao {
+    private final JdbcTemplate jdbcTemplate;
```

</details>

### 인라인 코멘트 3173616372: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-01T14:45:36Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3173616372)
- 코드: `src/main/java/roomescape/dao/ReservationDao.java`, 현재 줄 None, 원래 줄 53
- 답변 대상: [코멘트 3167881423](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167881423)
- 소속 리뷰 ID: 4211266115

> INSERT 쿼리 문자열도, KeyHolder 객체 생성도, PreparedStatementCreator 람다식도 모두 사라지는 효과가 있네요!
> 이 부분도 적용해보겠습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,70 @@
+package roomescape.dao;
+
+import java.sql.PreparedStatement;
+import java.util.List;
+import java.util.Objects;
+import org.springframework.jdbc.core.JdbcTemplate;
+import org.springframework.jdbc.core.RowMapper;
+import org.springframework.jdbc.support.GeneratedKeyHolder;
+import org.springframework.jdbc.support.KeyHolder;
+import org.springframework.stereotype.Repository;
+import roomescape.domain.Reservation;
+import roomescape.domain.ReservationTime;
+import roomescape.dto.ReservationRequest;
+
+@Repository
+public class ReservationDao {
+    private final JdbcTemplate jdbcTemplate;
+
+    private final RowMapper<Reservation> rowMapper = (rs, rowNum) -> {
+        ReservationTime time = new ReservationTime(
+                rs.getLong("time_id"),
+                rs.getString("start_at")
+        );
+        return new Reservation(
+                rs.getLong("reservation_id"),
+                rs.getString("name"),
+                rs.getString("date"),
+                time
+        );
+    };
+
+    public ReservationDao(JdbcTemplate jdbcTemplate) {
+        this.jdbcTemplate = jdbcTemplate;
+    }
+
+    public List<Reservation> findAll() {
+        String sql = """
+                SELECT
+                    r.id as reservation_id,
+                    r.name,
+                    r.date,
+                    t.id as time_id,
+                    t.start_at
+                FROM reservation as r
+                INNER JOIN reservation_time as t
+                  ON r.time_id = t.id
+                """;
+        return jdbcTemplate.query(sql, rowMapper);
+    }
+
+    public Long save(ReservationRequest request) {
+        String sql = "INSERT INTO reservation (name, date, time_id) VALUES (?, ?, ?)";
+        KeyHolder keyHolder = new GeneratedKeyHolder();
```

</details>

### 인라인 코멘트 3173678118: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-01T15:00:10Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3173678118)
- 코드: `src/main/java/roomescape/dao/ReservationTimeDao.java`, 현재 줄 None, 원래 줄 25
- 답변 대상: [코멘트 3167875754](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167875754)
- 소속 리뷰 ID: 4211266115

> 다른 이유는 없습니다! 수정 하겠습니다~!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,54 @@
+package roomescape.dao;
+
+import java.sql.PreparedStatement;
+import java.util.List;
+import java.util.Objects;
+import org.springframework.jdbc.core.JdbcTemplate;
+import org.springframework.jdbc.support.GeneratedKeyHolder;
+import org.springframework.jdbc.support.KeyHolder;
+import org.springframework.stereotype.Repository;
+import roomescape.domain.ReservationTime;
+
+@Repository
+public class ReservationTimeDao {
+    private final JdbcTemplate jdbcTemplate;
+
+    public ReservationTimeDao(JdbcTemplate jdbcTemplate) {
+        this.jdbcTemplate = jdbcTemplate;
+    }
+
+    public List<ReservationTime> findAll() {
+        String sql = "SELECT id, start_at FROM reservation_time";
+        return jdbcTemplate.query(sql, (rs, rowNum) -> new ReservationTime(
+                rs.getLong("id"),
+                rs.getString("start_at")
+        ));
```

</details>

### 인라인 코멘트 3174178265: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-01T16:52:14Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3174178265)
- 코드: `src/main/java/roomescape/domain/Reservation.java`, 현재 줄 None, 원래 줄 4
- 답변 대상: [코멘트 3167891353](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167891353)
- 소속 리뷰 ID: 4211266115

> JPA를 사용하지 않는다면 사이드 이펙트 방지 부분에서 유리할 것으로 생각했는데, 이번 기회로 도메인 엔티티의 의미에 대해서 깊게 생각해 볼 수 있어 도움이 많이 됐습니다, 감사합니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,9 @@
+package roomescape.domain;
+
+public record Reservation(
+        Long id,
```

</details>

### 인라인 코멘트 3174463193: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-01T18:01:58Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3174463193)
- 코드: `src/main/java/roomescape/domain/Reservation.java`, 현재 줄 None, 원래 줄 3
- 답변 대상: [코멘트 3167921754](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167921754)
- 소속 리뷰 ID: 4211266115

> 객체는 항상 유효한 상태를 보장해야 한다고 생각합니다. 만약 생성 시점에 값들을 검증하지 않으면, 이 객체를 사용하는 모든 계층에서 반복적으로 Null 체크를 수행해야 하는 비용과 누락의 위험이 발생합니다.
> 따라서 Reservation 객체는 생성 시점에 필수 값들을 검증하여 빠른 실패를 유도하는 것이 안전한 설계라고 판단했습니다.
>
> 필수 값의 기준은 다음과 같습니다.
>
> 이름, 날짜, 시간: 도메인 규칙상 결여될 수 없는 핵심 정보이므로 반드시 검증합니다.
>
> id: DB에 Insert된 이후에 데이터베이스가 발급하기 때문에, 도메인 객체 생성 시점의 필수 검증에서는 제외했습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,9 @@
+package roomescape.domain;
+
+public record Reservation(
```

</details>

### 인라인 코멘트 3174603529: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-01T18:35:57Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3174603529)
- 코드: `src/main/java/roomescape/service/ReservationService.java`, 현재 줄 None, 원래 줄 26
- 답변 대상: [코멘트 3167906721](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167906721)
- 소속 리뷰 ID: 4211266115

> 예약 객체 생성 시 검증하도록 수정했습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,35 @@
+package roomescape.service;
+
+import java.util.List;
+import org.springframework.stereotype.Service;
+import roomescape.dao.ReservationDao;
+import roomescape.dao.ReservationTimeDao;
+import roomescape.domain.Reservation;
+import roomescape.domain.ReservationTime;
+import roomescape.dto.ReservationRequest;
+
+@Service
+public class ReservationService {
+    private final ReservationDao reservationDao;
+    private final ReservationTimeDao reservationTimeDao;
+
+    public ReservationService(ReservationDao reservationDao, ReservationTimeDao reservationTimeDao) {
+        this.reservationDao = reservationDao;
+        this.reservationTimeDao = reservationTimeDao;
+    }
+
+    public List<Reservation> findAllReservations() {
+        return reservationDao.findAll();
+    }
+
+    public Reservation createReservation(ReservationRequest request) {
+        Long generatedId = reservationDao.save(request);
```

</details>

### 인라인 코멘트 3174694418: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-01T18:54:32Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3174694418)
- 코드: `src/main/java/roomescape/service/ReservationService.java`, 현재 줄 None, 원래 줄 26
- 답변 대상: [코멘트 3167908186](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167908186)
- 소속 리뷰 ID: 4211266115

> 잘못된 외래 키(FK) 참조로 인해 DB 인프라 에러가 터지기 전에 service 계층에서 예외 처리하도록 수정했습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,35 @@
+package roomescape.service;
+
+import java.util.List;
+import org.springframework.stereotype.Service;
+import roomescape.dao.ReservationDao;
+import roomescape.dao.ReservationTimeDao;
+import roomescape.domain.Reservation;
+import roomescape.domain.ReservationTime;
+import roomescape.dto.ReservationRequest;
+
+@Service
+public class ReservationService {
+    private final ReservationDao reservationDao;
+    private final ReservationTimeDao reservationTimeDao;
+
+    public ReservationService(ReservationDao reservationDao, ReservationTimeDao reservationTimeDao) {
+        this.reservationDao = reservationDao;
+        this.reservationTimeDao = reservationTimeDao;
+    }
+
+    public List<Reservation> findAllReservations() {
+        return reservationDao.findAll();
+    }
+
+    public Reservation createReservation(ReservationRequest request) {
+        Long generatedId = reservationDao.save(request);
```

</details>

### 인라인 코멘트 3174732102: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-01T19:04:57Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3174732102)
- 코드: `src/main/java/roomescape/service/ReservationService.java`, 현재 줄 59, 원래 줄 34
- 답변 대상: [코멘트 3167913320](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167913320)
- 소속 리뷰 ID: 4211266115

> 미션 API 명세를 따르는 것이 중요하다고 생각했습니다.
> 다만 찰리의 의견을 듣고 고민을 해봤습니다.
> 멱등성을 지켰을 때의 장점은 네트워크 재시도에 강하고, 클라이언트 로직의 단순화를 생각해볼 수 있었습니다.
> 처리를 했을 때의 장점은 프론트엔드 웹 부분에서 버그가 있을 수 있는데 예외를 던져줌으로써 디버깅에 용이할 것으로 생각됩니다. 또한 프론트엔드와 백엔드의 상태가 동기화되는 장점으로 혼선 방지와 혹시 모를 사이드 이펙트 방지에 도움이 될 것 같습니다.
>
> 그래서 결론은 '이 API를 누가, 어떻게 사용하는가'에 집중해서 선택하겠습니다.
> 방탈출 예약관리앱은 사용자가 직접 조작하기 때문에 친절한 예외를 던지는 것이 좋다고 생각합니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,35 @@
+package roomescape.service;
+
+import java.util.List;
+import org.springframework.stereotype.Service;
+import roomescape.dao.ReservationDao;
+import roomescape.dao.ReservationTimeDao;
+import roomescape.domain.Reservation;
+import roomescape.domain.ReservationTime;
+import roomescape.dto.ReservationRequest;
+
+@Service
+public class ReservationService {
+    private final ReservationDao reservationDao;
+    private final ReservationTimeDao reservationTimeDao;
+
+    public ReservationService(ReservationDao reservationDao, ReservationTimeDao reservationTimeDao) {
+        this.reservationDao = reservationDao;
+        this.reservationTimeDao = reservationTimeDao;
+    }
+
+    public List<Reservation> findAllReservations() {
+        return reservationDao.findAll();
+    }
+
+    public Reservation createReservation(ReservationRequest request) {
+        Long generatedId = reservationDao.save(request);
+        ReservationTime time = reservationTimeDao.findById(request.timeId());
+
+        return request.toEntity(generatedId, time);
+    }
+
+    public void deleteReservation(Long id) {
+        reservationDao.deleteById(id);
+    }
```

</details>

### 인라인 코멘트 3174753265: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-01T19:10:15Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3174753265)
- 코드: `src/main/java/roomescape/service/ReservationService.java`, 현재 줄 17, 원래 줄 12
- 답변 대상: [코멘트 3167934430](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167934430)
- 소속 리뷰 ID: 4211266115

> ⚠️ 새로운 테스트 도구나 기법(Spring Boot Test, Mock, RestAssured 추가 활용 등)을 도입하지 않고 레벨1에서 학습했던 JUnit만 활용한 단위 테스트에 집중한다. 요구사항에서 RestAssured가 주어진 경우 그대로 사용하되, 그 위에 새 테스트 기법을 쌓지 않는다.
>
> 위의 요구사항으로 도메인 테스트를 추가해봤습니다.
> service test에 대해서는 추가 학습을 해서 반영하도록 해보겠습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,35 @@
+package roomescape.service;
+
+import java.util.List;
+import org.springframework.stereotype.Service;
+import roomescape.dao.ReservationDao;
+import roomescape.dao.ReservationTimeDao;
+import roomescape.domain.Reservation;
+import roomescape.domain.ReservationTime;
+import roomescape.dto.ReservationRequest;
+
+@Service
+public class ReservationService {
```

</details>

### 인라인 코멘트 3174799105: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-01T19:21:50Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3174799105)
- 코드: `src/main/java/roomescape/service/ReservationTimeService.java`, 현재 줄 None, 원래 줄 22
- 답변 대상: [코멘트 3167926841](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167926841)
- 소속 리뷰 ID: 4211266115

> 13:00에 예약이 중복으로 확정된다면 서비스라고 생각해볼 때 끔찍하다고 생각됐습니다.
> Unique할 수 있도록 처리해보겠습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,29 @@
+package roomescape.service;
+
+import java.util.List;
+import org.springframework.stereotype.Service;
+import roomescape.dao.ReservationTimeDao;
+import roomescape.domain.ReservationTime;
+import roomescape.dto.ReservationTimeRequest;
+
+@Service
+public class ReservationTimeService {
+    private final ReservationTimeDao reservationTimeDao;
+
+    public ReservationTimeService(ReservationTimeDao reservationTimeDao) {
+        this.reservationTimeDao = reservationTimeDao;
+    }
+
+    public List<ReservationTime> findAll() {
+        return reservationTimeDao.findAll();
+    }
+
+    public ReservationTime create(ReservationTimeRequest request) {
+        Long generatedId = reservationTimeDao.save(request.startAt());
```

</details>

### 리뷰 본문 4211266115: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-01T19:27:29Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#pullrequestreview-4211266115)
- 리뷰 상태: `COMMENTED`

> 찰리, 좋은 피드백 감사합니다!
>
> 집어주신 내용 하나하나가 큰 도움이 됐습니다.
> 아직 집어주신 부분들도 추가적인 이해와 고민들이 필요하다고 느껴집니다.
> 정말 고민되는 부분들을 정리해서 DM을 보내도 괜찮을까요?
> 다음 피드백도 잘 부탁드립니다!

### 인라인 코멘트 3175934196: Gomding

- 상대방 발언, 참여자
- 시각: 2026-05-02T02:34:17Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3175934196)
- 코드: `src/main/java/roomescape/controller/ReservationController.java`, 현재 줄 17, 원래 줄 16
- 답변 대상: [코멘트 3167870317](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167870317)
- 소속 리뷰 ID: 4214211032

> 크.. 학습하기 전 추론을 통해 생각해보는 과정이 멋지네요 👍 👍 👍

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,41 @@
+package roomescape.controller;
+
+import java.util.List;
+import org.springframework.http.ResponseEntity;
+import org.springframework.web.bind.annotation.DeleteMapping;
+import org.springframework.web.bind.annotation.GetMapping;
+import org.springframework.web.bind.annotation.PathVariable;
+import org.springframework.web.bind.annotation.PostMapping;
+import org.springframework.web.bind.annotation.RequestBody;
+import org.springframework.web.bind.annotation.RequestMapping;
+import org.springframework.web.bind.annotation.RestController;
+import roomescape.domain.Reservation;
+import roomescape.dto.ReservationRequest;
+import roomescape.service.ReservationService;
+
+@RestController
```

</details>

### 인라인 코멘트 3175945025: Gomding

- 상대방 발언, 참여자
- 시각: 2026-05-02T02:40:49Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3175945025)
- 코드: `src/main/java/roomescape/dao/ReservationDao.java`, 현재 줄 None, 원래 줄 17
- 답변 대상: [코멘트 3167878729](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167878729)
- 소속 리뷰 ID: 4214211032

> > '왜 Map말고 SqlParameterSource을 사용하면 좋은걸까?' 의문이 생겼습니다.
> > null 처리 안정성을 확인했는데 다른 이점도 있을까요?
>
> 실제로 `NamedParameterJdbcTemplate` 의 update 메서드를 보면 Map을 인자로 받고있기도 하죠~
> 해당 의문은 SqlParameterSource 의 다른 구현체들을 살펴보면 좋을 것 같네요 :)
> SqlParameterSource 의 여러 구현체중에 Map 은 편의성 측면에서 좀 더 강화된 버전 정도로 생각하고
> 결국 인터페이스를 통해 여러 구현체를 유연하게 교체 사용하기 위함 이라는 장점을 살릴 수 있곘네요
>
> +) MapSqlParameterSource 은 사용해주신것처럼 메서드 체이닝을 통해 값 추가를 더 간결하게 사용할 수 있다는 장점도 있어요 😄
>
> 스프링 코드에서 javadoc 은 많은 정보를 제공해주니
> 읽어보시면 학습에 많은 도움이 될거예요
> 그들의 구현 철학을 알 수도 있구요 ㅎㅎ
>
> <img width="733" height="409" alt="image" src="https://github.com/user-attachments/assets/b5e37139-5434-4d9a-a531-74120d0d3405" />
>

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,70 @@
+package roomescape.dao;
+
+import java.sql.PreparedStatement;
+import java.util.List;
+import java.util.Objects;
+import org.springframework.jdbc.core.JdbcTemplate;
+import org.springframework.jdbc.core.RowMapper;
+import org.springframework.jdbc.support.GeneratedKeyHolder;
+import org.springframework.jdbc.support.KeyHolder;
+import org.springframework.stereotype.Repository;
+import roomescape.domain.Reservation;
+import roomescape.domain.ReservationTime;
+import roomescape.dto.ReservationRequest;
+
+@Repository
+public class ReservationDao {
+    private final JdbcTemplate jdbcTemplate;
```

</details>

### 인라인 코멘트 3175949762: Gomding

- 상대방 발언, 참여자
- 시각: 2026-05-02T02:43:11Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3175949762)
- 코드: `src/main/java/roomescape/service/ReservationService.java`, 현재 줄 59, 원래 줄 34
- 답변 대상: [코멘트 3167913320](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167913320)
- 소속 리뷰 ID: 4214211032

> > 멱등성을 지켰을 때의 장점은 네트워크 재시도에 강하고, 클라이언트 로직의 단순화를 생각해볼 수 있었습니다.
>
> 요렇게 클라이언트도 함께 고려하는것 좋네요!! 💯 💯 💯
>
> > 그래서 결론은 '이 API를 누가, 어떻게 사용하는가'에 집중해서 선택하겠습니다.
> 방탈출 예약관리앱은 사용자가 직접 조작하기 때문에 친절한 예외를 던지는 것이 좋다고 생각합니다.
>
> 좋은 판단이라 생각해요! 의견 감사합니다 ㅎㅎ

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,35 @@
+package roomescape.service;
+
+import java.util.List;
+import org.springframework.stereotype.Service;
+import roomescape.dao.ReservationDao;
+import roomescape.dao.ReservationTimeDao;
+import roomescape.domain.Reservation;
+import roomescape.domain.ReservationTime;
+import roomescape.dto.ReservationRequest;
+
+@Service
+public class ReservationService {
+    private final ReservationDao reservationDao;
+    private final ReservationTimeDao reservationTimeDao;
+
+    public ReservationService(ReservationDao reservationDao, ReservationTimeDao reservationTimeDao) {
+        this.reservationDao = reservationDao;
+        this.reservationTimeDao = reservationTimeDao;
+    }
+
+    public List<Reservation> findAllReservations() {
+        return reservationDao.findAll();
+    }
+
+    public Reservation createReservation(ReservationRequest request) {
+        Long generatedId = reservationDao.save(request);
+        ReservationTime time = reservationTimeDao.findById(request.timeId());
+
+        return request.toEntity(generatedId, time);
+    }
+
+    public void deleteReservation(Long id) {
+        reservationDao.deleteById(id);
+    }
```

</details>

### 인라인 코멘트 3175965182: Gomding

- 상대방 발언, 참여자
- 시각: 2026-05-02T02:48:39Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3175965182)
- 코드: `src/main/java/roomescape/controller/ReservationTimeController.java`, 현재 줄 None, 원래 줄 32
- 답변 대상: [코멘트 3167929683](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167929683)
- 소속 리뷰 ID: 4214211032

> 해당 부분은 `클라이언트와 어떻게 스펙을 합의했냐` 에 따라 다를 수 있어요!
> 201 응답으로 생성된 리소스의 위치를 바로 알려주면 더 편해질 수 있구요
> 굳이 필요없는 케이스도 있겠죠 :)
>
> Created(201) 로 보낼때는 Location 을 담아준다~ 라는 정보만 알고 계시면 좋을 것 같습니다 😄
>
> 국제 표준을 따르면 당연히 좋다고 생각은 해요!
> 다만 상황과 팀의 의견에 따라 유연하게 달라질 수 있다고 봐요
> 국제의 규칙이 어쨋든 결국 중요한건 함께 일하는 팀의 규칙이니까요 ㅎㅎ
> (팀의 규칙을 만드는데는 이런 국제 표준을 중심으로 토론을 해야하겠지만요~ 상황에 따라 유연하게 하자 입니다!)

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,42 @@
+package roomescape.controller;
+
+import java.util.List;
+import org.springframework.http.ResponseEntity;
+import org.springframework.web.bind.annotation.DeleteMapping;
+import org.springframework.web.bind.annotation.GetMapping;
+import org.springframework.web.bind.annotation.PathVariable;
+import org.springframework.web.bind.annotation.PostMapping;
+import org.springframework.web.bind.annotation.RequestBody;
+import org.springframework.web.bind.annotation.RequestMapping;
+import org.springframework.web.bind.annotation.RestController;
+import roomescape.domain.ReservationTime;
+import roomescape.dto.ReservationTimeRequest;
+import roomescape.service.ReservationTimeService;
+
+@RestController
+@RequestMapping("/times")
+public class ReservationTimeController {
+
+    private final ReservationTimeService reservationTimeService;
+
+    public ReservationTimeController(ReservationTimeService reservationTimeService) {
+        this.reservationTimeService = reservationTimeService;
+    }
+
+    @GetMapping
+    public List<ReservationTime> read() {
+        return reservationTimeService.findAll();
+    }
+
+    @PostMapping
+    public ResponseEntity<ReservationTime> create(@RequestBody ReservationTimeRequest request) {
```

</details>

### 인라인 코멘트 3175971925: Gomding

- 상대방 발언, 참여자
- 시각: 2026-05-02T02:51:02Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3175971925)
- 코드: `src/main/java/roomescape/service/ReservationService.java`, 현재 줄 17, 원래 줄 12
- 답변 대상: [코멘트 3167934430](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167934430)
- 소속 리뷰 ID: 4214211032

> 앗 Spring Boot Test 도 포함이었군요 😱

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,35 @@
+package roomescape.service;
+
+import java.util.List;
+import org.springframework.stereotype.Service;
+import roomescape.dao.ReservationDao;
+import roomescape.dao.ReservationTimeDao;
+import roomescape.domain.Reservation;
+import roomescape.domain.ReservationTime;
+import roomescape.dto.ReservationRequest;
+
+@Service
+public class ReservationService {
```

</details>

### 인라인 코멘트 3175976930: Gomding

- 상대방 발언, 참여자
- 시각: 2026-05-02T02:53:38Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3175976930)
- 코드: `src/main/java/roomescape/domain/Reservation.java`, 현재 줄 None, 원래 줄 39
- 소속 리뷰 ID: 4214211032

> 해당 예외가 발생했을 떄 api 응답이 500 으로 날아가고 에러 메시지도 유실되는것 같네요 😢
> 클라이언트는 뭐때문에 api 가 실패했는지 알 수 없을것 같아요!
> 어떻게 처리하면 좋을까요~
>
> ```http
> {
>     "timestamp": "2026-05-02T02:52:10.572+00:00",
>     "status": 500,
>     "error": "Internal Server Error",
>     "path": "/reservations"
> }
> ```

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,72 @@
+package roomescape.domain;
+
+import java.time.LocalDate;
+import java.util.Objects;
+
+public class Reservation {
+    private Long id;
+    private final String name;
+    private final LocalDate date;
+    private final ReservationTime time;
+
+    public Reservation(Long id, String name, LocalDate date, ReservationTime time) {
+        validateName(name);
+        validateDate(date);
+        validateTime(time);
+
+        this.id = id;
+        this.name = name;
+        this.date = date;
+        this.time = time;
+    }
+
+    public void setId(Long id) {
+        this.id = id;
+    }
+
+    private void validateName(String name) {
+        if (name == null || name.isBlank()) {
+            throw new IllegalArgumentException("이름은 필수입니다.");
+        }
+    }
+
+    private void validateDate(LocalDate date) {
+        if (date == null) {
+            throw new IllegalArgumentException("날짜는 필수입니다.");
+        }
+        if (date.isBefore(LocalDate.now())) {
+            throw new IllegalArgumentException("과거 날짜는 예약할 수 없습니다.");
+        }
```

</details>

### 인라인 코멘트 3175992257: Gomding

- 상대방 발언, 참여자
- 시각: 2026-05-02T03:04:02Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3175992257)
- 코드: `src/main/java/roomescape/domain/Reservation.java`, 현재 줄 None, 원래 줄 14
- 소속 리뷰 ID: 4214211032

> Reservation 은 기존에 DB에 저장된 객체도 조회가 가능해야하는데
> validateDate 내부에서는 과거 날짜 예약까지 검증하고 있군요 :)
>
> 새로 생성하는것과 기존에 있던 영속화된 객체를 가져오는것에 규칙의 차이점이 있어보이네요
> 어떻게 분리하면 좋을까요~

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,72 @@
+package roomescape.domain;
+
+import java.time.LocalDate;
+import java.util.Objects;
+
+public class Reservation {
+    private Long id;
+    private final String name;
+    private final LocalDate date;
+    private final ReservationTime time;
+
+    public Reservation(Long id, String name, LocalDate date, ReservationTime time) {
+        validateName(name);
+        validateDate(date);
```

</details>

### 인라인 코멘트 3175993398: Gomding

- 상대방 발언, 참여자
- 시각: 2026-05-02T03:04:57Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3175993398)
- 코드: `src/main/java/roomescape/service/ReservationTimeService.java`, 현재 줄 12, 원래 줄 12
- 소속 리뷰 ID: 4214211032

> `@Transactional(readOnly = true)` 클래스레벨에 요걸 사용하신 이유가 궁금해요~
>
> 그리고 `readOnly=true` 설정은 어떤 이유로 사용해주신걸까요!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,39 @@
+package roomescape.service;
+
+import java.util.List;
+import org.springframework.stereotype.Service;
+import org.springframework.transaction.annotation.Transactional;
+import roomescape.dao.ReservationTimeDao;
+import roomescape.domain.ReservationTime;
+import roomescape.service.dto.ReservationTimeCreateCommand;
+
+@Service
+@Transactional(readOnly = true)
+public class ReservationTimeService {
```

</details>

### 인라인 코멘트 3175995307: Gomding

- 상대방 발언, 참여자
- 시각: 2026-05-02T03:06:38Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3175995307)
- 코드: `src/main/java/roomescape/dao/ReservationDao.java`, 현재 줄 None, 원래 줄 24
- 소속 리뷰 ID: 4214211032

> ReservationTimeDao 에 있는 매핑과 겹지는 부분이 있는데
> ReservationTime 에 수정사항이 있다면 관리해야하는 곳이 여러곳이 되겠네요 😢
> 중복을 어떻게 관리하면 좋을까요~

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,68 @@
+package roomescape.dao;
+
+import java.time.LocalDate;
+import java.time.LocalTime;
+import java.util.List;
+import javax.sql.DataSource;
+import org.springframework.jdbc.core.RowMapper;
+import org.springframework.jdbc.core.namedparam.MapSqlParameterSource;
+import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
+import org.springframework.jdbc.core.namedparam.SqlParameterSource;
+import org.springframework.jdbc.core.simple.SimpleJdbcInsert;
+import org.springframework.stereotype.Repository;
+import roomescape.domain.Reservation;
+import roomescape.domain.ReservationTime;
+
+@Repository
+public class ReservationDao {
+    private final NamedParameterJdbcTemplate jdbcTemplate;
+    private final SimpleJdbcInsert simpleJdbcInsert;
+    private final RowMapper<Reservation> rowMapper = (rs, rowNum) -> {
+        ReservationTime time = new ReservationTime(
+                rs.getLong("time_id"),
+                rs.getObject("start_at", LocalTime.class)
+        );
```

</details>

### 인라인 코멘트 3175999994: Gomding

- 상대방 발언, 참여자
- 시각: 2026-05-02T03:11:11Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3175999994)
- 코드: `src/main/java/roomescape/dto/ReservationRequest.java`, 현재 줄 14, 원래 줄 14
- 소속 리뷰 ID: 4214211032

> 파싱할 수 없는 date 가 온다면 어떤 응답이 클라이언트에게 가고있을까요?
> `2026-05-ㄱ` 이런 요청값이 왔을 때 어떻게 응답해주는게 좋을까요 :)

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,18 @@
+package roomescape.dto;
+
+import java.time.LocalDate;
+import roomescape.service.dto.ReservationCreateCommand;
+
+public record ReservationRequest(
+        String date,
+        String name,
+        Long timeId
+) {
+    public ReservationCreateCommand toCommand() {
+        return new ReservationCreateCommand(
+                this.name,
+                LocalDate.parse(this.date),
```

</details>

### 인라인 코멘트 3176001318: Gomding

- 상대방 발언, 참여자
- 시각: 2026-05-02T03:12:28Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3176001318)
- 코드: `src/main/java/roomescape/domain/Reservation.java`, 현재 줄 None, 원래 줄 37
- 소속 리뷰 ID: 4214211032

> `LocalDate.now()` 와 같이 제어할 수 없는 값은 테스트할 때 불편함을 줄 수도 있을것 같은데
> 어떻게 처리하면 좋을까요? 🤔

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,72 @@
+package roomescape.domain;
+
+import java.time.LocalDate;
+import java.util.Objects;
+
+public class Reservation {
+    private Long id;
+    private final String name;
+    private final LocalDate date;
+    private final ReservationTime time;
+
+    public Reservation(Long id, String name, LocalDate date, ReservationTime time) {
+        validateName(name);
+        validateDate(date);
+        validateTime(time);
+
+        this.id = id;
+        this.name = name;
+        this.date = date;
+        this.time = time;
+    }
+
+    public void setId(Long id) {
+        this.id = id;
+    }
+
+    private void validateName(String name) {
+        if (name == null || name.isBlank()) {
+            throw new IllegalArgumentException("이름은 필수입니다.");
+        }
+    }
+
+    private void validateDate(LocalDate date) {
+        if (date == null) {
+            throw new IllegalArgumentException("날짜는 필수입니다.");
+        }
+        if (date.isBefore(LocalDate.now())) {
```

</details>

### 리뷰 본문 4214211032: Gomding

- 상대방 발언, 참여자
- 시각: 2026-05-02T03:13:27Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#pullrequestreview-4214211032)
- 리뷰 상태: `CHANGES_REQUESTED`

> 안녕하세요 고래!
> 학습하는 과정이 인상깊네요 👍 👍
> 추가로 코멘트 남겼으니 확인부탁드려요 😄
>
> 궁금한 점 있으면 언제든 DM 이나 코멘트 남겨주세요~

### 인라인 코멘트 3177638325: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-03T04:44:22Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3177638325)
- 코드: `src/main/java/roomescape/domain/Reservation.java`, 현재 줄 None, 원래 줄 14
- 답변 대상: [코멘트 3175992257](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3175992257)
- 소속 리뷰 ID: 4215886675

> 말씀하신 대로 Reservation 엔티티 내부에서 과거 날짜를 검증하게 되면, DB에서 과거 데이터를 조회하여 객체로 재구성할 때 모순이 발생한다는 점을 깨달았습니다.
> 그리고 해당 규칙은 예약 생성이라는 특정 유스케이스의 비즈니스 규칙에 가깝다고 판단이 되어 ReservationService의 createReservation에서 검증하는 것으로 분리해보겠습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,72 @@
+package roomescape.domain;
+
+import java.time.LocalDate;
+import java.util.Objects;
+
+public class Reservation {
+    private Long id;
+    private final String name;
+    private final LocalDate date;
+    private final ReservationTime time;
+
+    public Reservation(Long id, String name, LocalDate date, ReservationTime time) {
+        validateName(name);
+        validateDate(date);
```

</details>

### 인라인 코멘트 3177676428: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-03T05:31:10Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3177676428)
- 코드: `src/main/java/roomescape/domain/Reservation.java`, 현재 줄 None, 원래 줄 37
- 답변 대상: [코멘트 3176001318](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3176001318)
- 소속 리뷰 ID: 4215886675

> 맞습니다.
> 처음에는 컨트롤러 호출 시점의 시간을 주입하는 식으로 처리하려 했습니다.
> AI와 대화 중 다른 방법은 없는지 확인을 했고 그 과정에서 java.time.Clock 빈(Bean) 주입 방식에 대해서 듣게 됐습니다.
> 그 후 생각을 해보니 command 객체에 담게 된다면 사용자의 입력값과 시스템의 상태값이 하나의 객체에 섞이게 되어 객체의 의미가 약간 오염된다고 생각되어서 Clock 빈을 사용하는 식으로 처리해보겠습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,72 @@
+package roomescape.domain;
+
+import java.time.LocalDate;
+import java.util.Objects;
+
+public class Reservation {
+    private Long id;
+    private final String name;
+    private final LocalDate date;
+    private final ReservationTime time;
+
+    public Reservation(Long id, String name, LocalDate date, ReservationTime time) {
+        validateName(name);
+        validateDate(date);
+        validateTime(time);
+
+        this.id = id;
+        this.name = name;
+        this.date = date;
+        this.time = time;
+    }
+
+    public void setId(Long id) {
+        this.id = id;
+    }
+
+    private void validateName(String name) {
+        if (name == null || name.isBlank()) {
+            throw new IllegalArgumentException("이름은 필수입니다.");
+        }
+    }
+
+    private void validateDate(LocalDate date) {
+        if (date == null) {
+            throw new IllegalArgumentException("날짜는 필수입니다.");
+        }
+        if (date.isBefore(LocalDate.now())) {
```

</details>

### 인라인 코멘트 3177693845: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-03T05:52:44Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3177693845)
- 코드: `src/main/java/roomescape/domain/Reservation.java`, 현재 줄 None, 원래 줄 39
- 답변 대상: [코멘트 3175976930](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3175976930)
- 소속 리뷰 ID: 4215886675

> 예외를 낚아채서, 도메인 문맥에 맞는 예외로 전환해서 던져주는 방식으로 처리해보겠습니다.
> 위치는 컨트롤러 아래에 위치하는 것이 좋다고 생각합니다.
> 그 이유는 웹 계층이 데이터베이스 예외를 직접 알게 하는 방식은 계층 분리 원칙에 어긋난다고 생각하기 때문입니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,72 @@
+package roomescape.domain;
+
+import java.time.LocalDate;
+import java.util.Objects;
+
+public class Reservation {
+    private Long id;
+    private final String name;
+    private final LocalDate date;
+    private final ReservationTime time;
+
+    public Reservation(Long id, String name, LocalDate date, ReservationTime time) {
+        validateName(name);
+        validateDate(date);
+        validateTime(time);
+
+        this.id = id;
+        this.name = name;
+        this.date = date;
+        this.time = time;
+    }
+
+    public void setId(Long id) {
+        this.id = id;
+    }
+
+    private void validateName(String name) {
+        if (name == null || name.isBlank()) {
+            throw new IllegalArgumentException("이름은 필수입니다.");
+        }
+    }
+
+    private void validateDate(LocalDate date) {
+        if (date == null) {
+            throw new IllegalArgumentException("날짜는 필수입니다.");
+        }
+        if (date.isBefore(LocalDate.now())) {
+            throw new IllegalArgumentException("과거 날짜는 예약할 수 없습니다.");
+        }
```

</details>

### 인라인 코멘트 3177770219: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-03T07:14:11Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3177770219)
- 코드: `src/main/java/roomescape/dto/ReservationRequest.java`, 현재 줄 14, 원래 줄 14
- 답변 대상: [코멘트 3175999994](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3175999994)
- 소속 리뷰 ID: 4215886675

> 2026-05-ㄱ과 같은 잘못된 요청이 오더라도 서버가 500 에러를 던지지 않고, 400 Bad Request 상태 코드와 함께 {"message": "입력 형식이 올바르지 않습니다. (예: 2026-05-03)"}이라는 JSON 응답을 내려주도록 처리했습니다.
> 여기서 고민이 있었는데
> 1. DTO에서 try catch하는 예외 전환 방법
> 2. 글로벌예외핸들러에  @ExceptionHandler(DateTimeParseException.class) 추가하는 법
> 3. 스프링 프레임워크에 위임하는 법을 고민을 했습니다.
> 3번으로 HttpMessageNotReadableException을 처리하게 되면 다른 필드의 변환에 문제가 생겼을 때 처리가 어려울 것으로 보아서 제외했습니다.
> DTO에 예외를 전환하는 것이 있는 것이 데이터 전달의 책임인 DTO와 어울리지 않는다고 생각했습니다.
> 글로벌 핸들러에서 DateTimeParseException을 처리하도록 수정해봤습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,18 @@
+package roomescape.dto;
+
+import java.time.LocalDate;
+import roomescape.service.dto.ReservationCreateCommand;
+
+public record ReservationRequest(
+        String date,
+        String name,
+        Long timeId
+) {
+    public ReservationCreateCommand toCommand() {
+        return new ReservationCreateCommand(
+                this.name,
+                LocalDate.parse(this.date),
```

</details>

### 인라인 코멘트 3177790803: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-03T07:37:08Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3177790803)
- 코드: `src/main/java/roomescape/service/ReservationTimeService.java`, 현재 줄 12, 원래 줄 12
- 답변 대상: [코멘트 3175993398](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3175993398)
- 소속 리뷰 ID: 4215886675

> 클래스 레벨에서 사용함으로써 하나의 작업 단위인 유스케이스(public method)의 transaction 설정을 놓치는 실수를 방지할 수 있습니다.
> readOnly=true를 디폴트 옵션으로 설정하면 JPA 환경에서 더티 체킹을 생략해서  성능에 이점이 있습니다.
>

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,39 @@
+package roomescape.service;
+
+import java.util.List;
+import org.springframework.stereotype.Service;
+import org.springframework.transaction.annotation.Transactional;
+import roomescape.dao.ReservationTimeDao;
+import roomescape.domain.ReservationTime;
+import roomescape.service.dto.ReservationTimeCreateCommand;
+
+@Service
+@Transactional(readOnly = true)
+public class ReservationTimeService {
```

</details>

### 인라인 코멘트 3177821766: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-03T08:07:35Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3177821766)
- 코드: `src/main/java/roomescape/dao/ReservationDao.java`, 현재 줄 None, 원래 줄 24
- 답변 대상: [코멘트 3175995307](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3175995307)
- 소속 리뷰 ID: 4215886675

> DAO는 DB 스키마를 투영하는 Entity 객체를 반환하도록 수정했습니다. 이를 통해 도메인 객체 조립 책임을 서비스 계층으로 분리했습니다. 향후 도메인 수정 시 서비스의 변환 로직만 관리하면 되도록 개선해봤는데, 중간 계층을 하나 더 도출하는 것도 고민이 됐습니다. 예를 들면 Repository, Dao 를 두어서 도메인 조립을 레포지토리에서 하는 것을 생각해봤는데 이 부분은 추가적으로 학습해보겠습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,68 @@
+package roomescape.dao;
+
+import java.time.LocalDate;
+import java.time.LocalTime;
+import java.util.List;
+import javax.sql.DataSource;
+import org.springframework.jdbc.core.RowMapper;
+import org.springframework.jdbc.core.namedparam.MapSqlParameterSource;
+import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
+import org.springframework.jdbc.core.namedparam.SqlParameterSource;
+import org.springframework.jdbc.core.simple.SimpleJdbcInsert;
+import org.springframework.stereotype.Repository;
+import roomescape.domain.Reservation;
+import roomescape.domain.ReservationTime;
+
+@Repository
+public class ReservationDao {
+    private final NamedParameterJdbcTemplate jdbcTemplate;
+    private final SimpleJdbcInsert simpleJdbcInsert;
+    private final RowMapper<Reservation> rowMapper = (rs, rowNum) -> {
+        ReservationTime time = new ReservationTime(
+                rs.getLong("time_id"),
+                rs.getObject("start_at", LocalTime.class)
+        );
```

</details>

### 리뷰 본문 4215886675: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-03T08:09:17Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#pullrequestreview-4215886675)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 일반 댓글 4365722452: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-03T08:10:38Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#issuecomment-4365722452)

> 찰리 피드백 해주신다고 고생이 많습니다!
> 피드백 반영이 늦어서 아쉽습니다.
> 이번 PR도 잘 부탁드립니다!

### 인라인 코멘트 3177968253: Gomding

- 상대방 발언, 참여자
- 시각: 2026-05-03T10:25:28Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3177968253)
- 코드: `src/main/java/roomescape/domain/Reservation.java`, 현재 줄 None, 원래 줄 14
- 답변 대상: [코멘트 3175992257](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3175992257)
- 소속 리뷰 ID: 4216177636

> 정적 팩토리 메서드로 표현해보는것과 비교는 해보셨을까요?
>
> ```java
> public static Reservation createNew(...) {
>     validateDate();
>     new Reservation(...);
> }
> ```
>
> 비교해보셨다면 유스케이스의 비즈니스 규칙에 가깝다고 판단한 근거도 궁금해요~ 😃

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,72 @@
+package roomescape.domain;
+
+import java.time.LocalDate;
+import java.util.Objects;
+
+public class Reservation {
+    private Long id;
+    private final String name;
+    private final LocalDate date;
+    private final ReservationTime time;
+
+    public Reservation(Long id, String name, LocalDate date, ReservationTime time) {
+        validateName(name);
+        validateDate(date);
```

</details>

### 인라인 코멘트 3177970471: Gomding

- 상대방 발언, 참여자
- 시각: 2026-05-03T10:27:41Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3177970471)
- 코드: `src/main/java/roomescape/controller/ReservationTimeController.java`, 현재 줄 None, 원래 줄 13
- 소속 리뷰 ID: 4216177636

> "/times" 요건 미션 요구사항에 예제로 나와있었던것 같은데요~
>
> `/times` 라고만 한다면 무엇의 시간인가? 라는 의문이 남지 않을까요 :)
> 고래가 Time 이 아닌 ReservationTime 이라고 표현하신것은 어떤 이유가 있었을거라 생각해요
>

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,39 @@
+package roomescape.controller;
+
+import java.util.List;
+import org.springframework.http.ResponseEntity;
+import org.springframework.web.bind.annotation.*;
+import roomescape.domain.ReservationTime;
+import roomescape.dto.ReservationTimeRequest;
+import roomescape.dto.ReservationTimeResponse;
+import roomescape.service.ReservationTimeService;
+
+@RestController
+@RequestMapping("/times")
+public class ReservationTimeController {
```

</details>

### 인라인 코멘트 3177972547: Gomding

- 상대방 발언, 참여자
- 시각: 2026-05-03T10:29:44Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3177972547)
- 코드: `src/main/java/roomescape/domain/Reservation.java`, 현재 줄 None, 원래 줄 39
- 답변 대상: [코멘트 3175976930](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3175976930)
- 소속 리뷰 ID: 4216177636

> 예외를 전환해서 던져주는것 좋네요! 💯 💯 💯

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,72 @@
+package roomescape.domain;
+
+import java.time.LocalDate;
+import java.util.Objects;
+
+public class Reservation {
+    private Long id;
+    private final String name;
+    private final LocalDate date;
+    private final ReservationTime time;
+
+    public Reservation(Long id, String name, LocalDate date, ReservationTime time) {
+        validateName(name);
+        validateDate(date);
+        validateTime(time);
+
+        this.id = id;
+        this.name = name;
+        this.date = date;
+        this.time = time;
+    }
+
+    public void setId(Long id) {
+        this.id = id;
+    }
+
+    private void validateName(String name) {
+        if (name == null || name.isBlank()) {
+            throw new IllegalArgumentException("이름은 필수입니다.");
+        }
+    }
+
+    private void validateDate(LocalDate date) {
+        if (date == null) {
+            throw new IllegalArgumentException("날짜는 필수입니다.");
+        }
+        if (date.isBefore(LocalDate.now())) {
+            throw new IllegalArgumentException("과거 날짜는 예약할 수 없습니다.");
+        }
```

</details>

### 인라인 코멘트 3177973899: Gomding

- 상대방 발언, 참여자
- 시각: 2026-05-03T10:31:04Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3177973899)
- 코드: `src/main/java/roomescape/service/ReservationTimeService.java`, 현재 줄 12, 원래 줄 12
- 답변 대상: [코멘트 3175993398](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3175993398)
- 소속 리뷰 ID: 4216177636

> JPA 환경이 아닌데 현재 상황에서는 이점이 아닐것 같네요 🤔 🤔 🤔
>
> > 클래스 레벨에서 사용함으로써 하나의 작업 단위인 유스케이스(public method)의 transaction 설정을 놓치는 실수를 방지할 수 있습니다.
>
> 💯
> 해당 부분은 더 자세히 설명해주실 수 있을까요?
> 어떤 상황을 예상하셨는지 궁금해요 😄

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,39 @@
+package roomescape.service;
+
+import java.util.List;
+import org.springframework.stereotype.Service;
+import org.springframework.transaction.annotation.Transactional;
+import roomescape.dao.ReservationTimeDao;
+import roomescape.domain.ReservationTime;
+import roomescape.service.dto.ReservationTimeCreateCommand;
+
+@Service
+@Transactional(readOnly = true)
+public class ReservationTimeService {
```

</details>

### 인라인 코멘트 3177975585: Gomding

- 상대방 발언, 참여자
- 시각: 2026-05-03T10:32:39Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3177975585)
- 코드: `src/main/java/roomescape/dao/ReservationDao.java`, 현재 줄 None, 원래 줄 24
- 답변 대상: [코멘트 3175995307](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3175995307)
- 소속 리뷰 ID: 4216177636

> ReservationDao 에서 ReservationTimeDao 의 RowMapper 를 의존할 수 있도록 설계하는것은 어떻게 생각하시나요 :)

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,68 @@
+package roomescape.dao;
+
+import java.time.LocalDate;
+import java.time.LocalTime;
+import java.util.List;
+import javax.sql.DataSource;
+import org.springframework.jdbc.core.RowMapper;
+import org.springframework.jdbc.core.namedparam.MapSqlParameterSource;
+import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
+import org.springframework.jdbc.core.namedparam.SqlParameterSource;
+import org.springframework.jdbc.core.simple.SimpleJdbcInsert;
+import org.springframework.stereotype.Repository;
+import roomescape.domain.Reservation;
+import roomescape.domain.ReservationTime;
+
+@Repository
+public class ReservationDao {
+    private final NamedParameterJdbcTemplate jdbcTemplate;
+    private final SimpleJdbcInsert simpleJdbcInsert;
+    private final RowMapper<Reservation> rowMapper = (rs, rowNum) -> {
+        ReservationTime time = new ReservationTime(
+                rs.getLong("time_id"),
+                rs.getObject("start_at", LocalTime.class)
+        );
```

</details>

### 인라인 코멘트 3177976926: Gomding

- 상대방 발언, 참여자
- 시각: 2026-05-03T10:34:08Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3177976926)
- 코드: `src/main/java/roomescape/dao/entity/ReservationTimeEntity.java`, 현재 줄 None, 원래 줄 5
- 소속 리뷰 ID: 4216177636

> ReservationTime 과 어떤 차이가 있는 객체인가요?
> ReservationTime 을 그대로 사용할 수 없는 상황이 있었을까요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,6 @@
+package roomescape.dao.entity;
+
+import java.time.LocalTime;
+
+public record ReservationTimeEntity(Long id, LocalTime startAt) {
```

</details>

### 인라인 코멘트 3177979824: Gomding

- 상대방 발언, 참여자
- 시각: 2026-05-03T10:36:49Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3177979824)
- 코드: `src/main/java/roomescape/service/ReservationService.java`, 현재 줄 17, 원래 줄 12
- 답변 대상: [코멘트 3167934430](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3167934430)
- 소속 리뷰 ID: 4216177636

> 요거는 단위테스트의 관점에서 본다면
> 테스트 더블의 Fake 객체를 직접 구현하는 방법도 있을 것 같아요~
>
>
> ```java
> public class FakeReservationDao extends ReservationDao {
>   // 필요한 구현
> }
>
> // ReservationServiceTest
> ReservationService reservationService = new ReservationService(new FakeReservationDao(...), ...생략);
> ```

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,35 @@
+package roomescape.service;
+
+import java.util.List;
+import org.springframework.stereotype.Service;
+import roomescape.dao.ReservationDao;
+import roomescape.dao.ReservationTimeDao;
+import roomescape.domain.Reservation;
+import roomescape.domain.ReservationTime;
+import roomescape.dto.ReservationRequest;
+
+@Service
+public class ReservationService {
```

</details>

### 인라인 코멘트 3177980353: Gomding

- 상대방 발언, 참여자
- 시각: 2026-05-03T10:37:25Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3177980353)
- 코드: `src/test/java/roomescape/domain/ReservationTest.java`, 현재 줄 None, 원래 줄 24
- 소속 리뷰 ID: 4216177636

> 테스트 추가 👍 👍
>
> 도메인 단위 테스트에 DB 개념은 들어가지 않는게 좋다고 생각해요!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,42 @@
+package roomescape.domain;
+
+import static org.assertj.core.api.Assertions.assertThatThrownBy;
+import static org.assertj.core.api.Assertions.assertThatCode;
+
+import java.time.LocalDate;
+import java.time.LocalTime;
+import org.junit.jupiter.api.DisplayName;
+import org.junit.jupiter.api.Test;
+
+class ReservationTest {
+
+    @Test
+    @DisplayName("이름이 비어있으면 예외가 발생한다.")
+    void validateName() {
+        ReservationTime time = new ReservationTime(1L, LocalTime.of(10, 0));
+
+        assertThatThrownBy(() -> new Reservation(1L, "", LocalDate.now(), time))
+                .isInstanceOf(IllegalArgumentException.class)
+                .hasMessage("이름은 필수입니다.");
+    }
+
+    @Test
+    @DisplayName("DB에서 조회한 과거 날짜 데이터로 객체를 생성할 때는 예외가 발생하지 않는다.")
```

</details>

### 인라인 코멘트 3177981132: Gomding

- 상대방 발언, 참여자
- 시각: 2026-05-03T10:38:16Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3177981132)
- 코드: `src/main/java/roomescape/controller/advice/GlobalExceptionHandler.java`, 현재 줄 10, 원래 줄 10
- 소속 리뷰 ID: 4216177636

> `RestControllerAdvice` 사용 👍 👍 👍

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,23 @@
+package roomescape.controller.advice;
+
+import java.time.format.DateTimeParseException;
+import org.springframework.http.ResponseEntity;
+import org.springframework.http.converter.HttpMessageNotReadableException;
+import org.springframework.web.bind.annotation.ExceptionHandler;
+import org.springframework.web.bind.annotation.RestControllerAdvice;
+import roomescape.dto.ErrorResponse;
+
+@RestControllerAdvice
```

</details>

### 인라인 코멘트 3177982155: Gomding

- 상대방 발언, 참여자
- 시각: 2026-05-03T10:39:18Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3177982155)
- 코드: `src/main/java/roomescape/controller/advice/GlobalExceptionHandler.java`, 현재 줄 11, 원래 줄 11
- 소속 리뷰 ID: 4216177636

> 고래가 예측하지 못한 예외는 핸들링하지 않아도 괜찮을까요?
> 500 응답으로 나가긴하지만 스프링의 기본 에러 응답 형태로 나갈것 같네요 :)
> ErrorResponse 도 만들어주셨으니 핸들링의 필요가 있지않을까요!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,23 @@
+package roomescape.controller.advice;
+
+import java.time.format.DateTimeParseException;
+import org.springframework.http.ResponseEntity;
+import org.springframework.http.converter.HttpMessageNotReadableException;
+import org.springframework.web.bind.annotation.ExceptionHandler;
+import org.springframework.web.bind.annotation.RestControllerAdvice;
+import roomescape.dto.ErrorResponse;
+
+@RestControllerAdvice
+public class GlobalExceptionHandler {
```

</details>

### 인라인 코멘트 3177982595: Gomding

- 상대방 발언, 참여자
- 시각: 2026-05-03T10:39:42Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3177982595)
- 코드: `src/main/java/roomescape/dto/ErrorResponse.java`, 현재 줄 3, 원래 줄 3
- 소속 리뷰 ID: 4216177636

> 단순 String 을 반환하지않고 에러 응답용 객체를 만들어주셨군요!
> 어떤 고민에 의해 탄생한건지 궁금해요!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,4 @@
+package roomescape.dto;
+
+public record ErrorResponse(String message) {
```

</details>

### 인라인 코멘트 3177985753: Gomding

- 상대방 발언, 참여자
- 시각: 2026-05-03T10:42:41Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3177985753)
- 코드: `src/main/java/roomescape/service/ReservationService.java`, 현재 줄 None, 원래 줄 46
- 소속 리뷰 ID: 4216177636

> findById 에서 Optional 을 반환하도록 하는것도 고려해보셨을까요? 😃
> 에러를 바깥에서 알아서 처리하라는것은 reservationTimeDao 의 세부사항을 모르면 처리하기가 힘들 수 있어요.
> 특히 다른개발자가 예외처리를 하지않을 수도 있구요
>
> EmptyResultDataAccessException 이라는 세부 예외 클래스를 service 계층에서 알아버린다는 단점도 있구요!
>
> Optional 을 사용한다면 다른 개발자에게 뭔가 처리해야한다는 의도를 전달할 수 있고
> 다른 개발자는 어떤 상황에 Optional 이 비어서 오는지 체크하게 만들수도 있어요.
> 결국 중요한건 메서드의 반환타입으로 고래의 의도를 충분히 전달할 수 있는가? 입니다 😄

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,88 @@
+package roomescape.service;
+
+import java.time.Clock;
+import java.time.LocalDate;
+import java.util.List;
+import org.springframework.dao.EmptyResultDataAccessException;
+import org.springframework.stereotype.Service;
+import org.springframework.transaction.annotation.Transactional;
+import roomescape.dao.ReservationDao;
+import roomescape.dao.ReservationTimeDao;
+import roomescape.dao.entity.ReservationTimeEntity;
+import roomescape.domain.Reservation;
+import roomescape.domain.ReservationTime;
+import roomescape.dto.ReservationJoinDto;
+import roomescape.service.dto.ReservationCreateCommand;
+
+@Service
+@Transactional(readOnly = true)
+public class ReservationService {
+    private final ReservationDao reservationDao;
+    private final ReservationTimeDao reservationTimeDao;
+    private final Clock clock;
+
+    public ReservationService(ReservationDao reservationDao, ReservationTimeDao reservationTimeDao, Clock clock) {
+        this.reservationDao = reservationDao;
+        this.reservationTimeDao = reservationTimeDao;
+        this.clock = clock;
+    }
+
+    public List<Reservation> findAllReservations() {
+        List<ReservationJoinDto> dtos = reservationDao.findAll();
+        return dtos.stream()
+                .map(this::toDomain)
+                .toList();
+    }
+
+    @Transactional
+    public Reservation createReservation(ReservationCreateCommand command) {
+        validateReservationDate(command.date());
+
+        ReservationTimeEntity timeEntity;
+        try {
+            timeEntity = reservationTimeDao.findById(command.timeId());
+        } catch (EmptyResultDataAccessException e) {
+            throw new IllegalArgumentException("존재하지 않는 예약 시간입니다.");
+        }
```

</details>

### 인라인 코멘트 3177986919: Gomding

- 상대방 발언, 참여자
- 시각: 2026-05-03T10:43:49Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3177986919)
- 코드: `src/main/java/roomescape/config/TimeConfig.java`, 현재 줄 13, 원래 줄 13
- 소속 리뷰 ID: 4216177636

> 시간을 다루는 테스트에서 시간을 제어하기위해 사용하신것으로 보이네요 👍 👍 👍 👍
> 유연한 구조가 됐다고 생각해요!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,14 @@
+package roomescape.config;
+
+import java.time.Clock;
+import org.springframework.context.annotation.Bean;
+import org.springframework.context.annotation.Configuration;
+
+@Configuration
+public class TimeConfig {
+
+    @Bean
+    public Clock clock() {
+        return Clock.systemDefaultZone();
+    }
```

</details>

### 리뷰 본문 4216177636: Gomding

- 상대방 발언, 참여자
- 시각: 2026-05-03T10:46:41Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#pullrequestreview-4216177636)
- 리뷰 상태: `CHANGES_REQUESTED`

> 안녕하세요 고래!
> 고민과 함께 잘 수정해주셨네요~
> 추가로 코멘트 남겼으니 확인부탁드려요 :)
> 궁금한 점 있으면 언제든 DM 이나 코멘트 남겨주세요!

### 인라인 코멘트 3178014568: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-03T11:09:01Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3178014568)
- 코드: `src/main/java/roomescape/controller/advice/GlobalExceptionHandler.java`, 현재 줄 11, 원래 줄 11
- 답변 대상: [코멘트 3177982155](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3177982155)
- 소속 리뷰 ID: 4216218541

> 찰리가 집어주신 부분이 혹시 제가 예상치 못한 부분에서 발생하는 예외들(Exception.class)을 글로벌예외핸들러에서 처리해주면 좋을 것 같다라고 느꼈는데 맞나요?
>
> 제가 생각하는 이유는 기본 에러 JSON 포맷으로 나가게 된다면 프론트엔드에서 파싱할 때 문제가 있고 불필요한 서버 내부 정보까지 노출되는 문제때문이라고 보여지는데 처리해보겠습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,23 @@
+package roomescape.controller.advice;
+
+import java.time.format.DateTimeParseException;
+import org.springframework.http.ResponseEntity;
+import org.springframework.http.converter.HttpMessageNotReadableException;
+import org.springframework.web.bind.annotation.ExceptionHandler;
+import org.springframework.web.bind.annotation.RestControllerAdvice;
+import roomescape.dto.ErrorResponse;
+
+@RestControllerAdvice
+public class GlobalExceptionHandler {
```

</details>

### 인라인 코멘트 3178021416: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-03T11:15:35Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3178021416)
- 코드: `src/main/java/roomescape/dto/ErrorResponse.java`, 현재 줄 3, 원래 줄 3
- 답변 대상: [코멘트 3177982595](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3177982595)
- 소속 리뷰 ID: 4216218541

> 정상 응답에서 application/json으로 응답하고, 예외 응답에서 text/plain으로 처리되면 프론트엔드(클라이언트) 코드의 파싱(Parsing) 에러와 로직 파편화가 발생할 수 있을 것으로 보입니다.
> 또한 추후 유연하게 추가 정보를 확장할 수 있게 되는 장점으로 시도해봤습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,4 @@
+package roomescape.dto;
+
+public record ErrorResponse(String message) {
```

</details>

### 인라인 코멘트 3178029646: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-03T11:23:33Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3178029646)
- 코드: `src/main/java/roomescape/controller/ReservationTimeController.java`, 현재 줄 None, 원래 줄 13
- 답변 대상: [코멘트 3177970471](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3177970471)
- 소속 리뷰 ID: 4216218541

> RESTful API에서 URI는 자원(Resource)을 명확하게 표현해야 하는데 요구 사항을 무조건적으로 받아들이기보다 비판적으로 바라볼 필요를 강하게 느끼는 계기가 됐습니다.
> 적절한 REST API 네이밍을 주도적으로 제안하고 다듬어 나가야 함을 알게 됐습니다.
>
> `/times -> /reservation-times`로 변경하겠습니다.
>
> 혹시 실무에서는 이러한 변경으로 API 호환성이 깨지게 될텐데 그러한 경우에는 소통을 통해서 변경하는 식으로 진행하나요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,39 @@
+package roomescape.controller;
+
+import java.util.List;
+import org.springframework.http.ResponseEntity;
+import org.springframework.web.bind.annotation.*;
+import roomescape.domain.ReservationTime;
+import roomescape.dto.ReservationTimeRequest;
+import roomescape.dto.ReservationTimeResponse;
+import roomescape.service.ReservationTimeService;
+
+@RestController
+@RequestMapping("/times")
+public class ReservationTimeController {
```

</details>

### 인라인 코멘트 3178049710: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-03T11:37:15Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3178049710)
- 코드: `src/main/java/roomescape/domain/Reservation.java`, 현재 줄 None, 원래 줄 14
- 답변 대상: [코멘트 3175992257](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3175992257)
- 소속 리뷰 ID: 4216218541

> 정적 팩토리를 가장 먼저 떠올렸습니다.
> DB에 있는 과거의 예약 데이터를 객체로 변환하다가 제가 착각을 했습니다.
> 예약이라는 의미 자체가 사실상 예약을 과거의 시간에 하는 게 말이 안되는 것이라 예약 도메인에서 가져야 할 검증인데 오해를했습니다.
> 다시 수정하겠습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,72 @@
+package roomescape.domain;
+
+import java.time.LocalDate;
+import java.util.Objects;
+
+public class Reservation {
+    private Long id;
+    private final String name;
+    private final LocalDate date;
+    private final ReservationTime time;
+
+    public Reservation(Long id, String name, LocalDate date, ReservationTime time) {
+        validateName(name);
+        validateDate(date);
```

</details>

### 인라인 코멘트 3178070509: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-03T11:55:31Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3178070509)
- 코드: `src/main/java/roomescape/dao/entity/ReservationTimeEntity.java`, 현재 줄 None, 원래 줄 5
- 답변 대상: [코멘트 3177976926](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3177976926)
- 소속 리뷰 ID: 4216218541

> 찰리의 질문을 계기로 Entity를 언제 분리해야 하는지 생각해보게 되었습니다!
> 순수한 도메인에서 식별자(id)를 제거하여 관심사를 분리하면, 클래스가 변경되어야 할 이유를 줄일 수 있다는 점을 이해했습니다. 실제로 도메인 객체에 id가 포함되어 있으면 순수 비즈니스 로직을 테스트할 때 불필요한 데이터가 필요할수도 있다고 생각합니다.
> ReservationTime에만 Entity를 사용했고 Entity를 사용하면서 ReservationTime에 id가 있는 모습을 보면서 잘 모르면서 사용했다는 것을 깨달았습니다.
> ReservationEntity 추가와 도메인 id 제거와 정적메서드 사용을 두고 고민했습니다.
> 다만, 현재 요구사항 규모에서는 Entity를 물리적으로 분리하는 것이 다소 오버 엔지니어링이 될 수 있다고 판단하여, 이번 단계에서는 객체 생성의 의도를 명확히 나눌 수 있는 정적 팩토리 메서드를 도입하는 방향으로 수정해 보겠습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,6 @@
+package roomescape.dao.entity;
+
+import java.time.LocalTime;
+
+public record ReservationTimeEntity(Long id, LocalTime startAt) {
```

</details>

### 인라인 코멘트 3178092379: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-03T12:13:57Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3178092379)
- 코드: `src/main/java/roomescape/service/ReservationService.java`, 현재 줄 None, 원래 줄 46
- 답변 대상: [코멘트 3177985753](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3177985753)
- 소속 리뷰 ID: 4216218541

> "결국 중요한건 메서드의 반환타입으로 고래의 의도를 충분히 전달할 수 있는가? 입니다 😄"
> 위의 문구가 저에게 큰 영감을 줬습니다. 감사합니다.
> EmptyResultDataAccessException 이라는 세부 예외 클래스를 service 계층에서 알아버린다는 단점도 크다고 생각하여 수정해보겠습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,88 @@
+package roomescape.service;
+
+import java.time.Clock;
+import java.time.LocalDate;
+import java.util.List;
+import org.springframework.dao.EmptyResultDataAccessException;
+import org.springframework.stereotype.Service;
+import org.springframework.transaction.annotation.Transactional;
+import roomescape.dao.ReservationDao;
+import roomescape.dao.ReservationTimeDao;
+import roomescape.dao.entity.ReservationTimeEntity;
+import roomescape.domain.Reservation;
+import roomescape.domain.ReservationTime;
+import roomescape.dto.ReservationJoinDto;
+import roomescape.service.dto.ReservationCreateCommand;
+
+@Service
+@Transactional(readOnly = true)
+public class ReservationService {
+    private final ReservationDao reservationDao;
+    private final ReservationTimeDao reservationTimeDao;
+    private final Clock clock;
+
+    public ReservationService(ReservationDao reservationDao, ReservationTimeDao reservationTimeDao, Clock clock) {
+        this.reservationDao = reservationDao;
+        this.reservationTimeDao = reservationTimeDao;
+        this.clock = clock;
+    }
+
+    public List<Reservation> findAllReservations() {
+        List<ReservationJoinDto> dtos = reservationDao.findAll();
+        return dtos.stream()
+                .map(this::toDomain)
+                .toList();
+    }
+
+    @Transactional
+    public Reservation createReservation(ReservationCreateCommand command) {
+        validateReservationDate(command.date());
+
+        ReservationTimeEntity timeEntity;
+        try {
+            timeEntity = reservationTimeDao.findById(command.timeId());
+        } catch (EmptyResultDataAccessException e) {
+            throw new IllegalArgumentException("존재하지 않는 예약 시간입니다.");
+        }
```

</details>

### 인라인 코멘트 3178108264: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-03T12:27:44Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3178108264)
- 코드: `src/main/java/roomescape/service/ReservationTimeService.java`, 현재 줄 12, 원래 줄 12
- 답변 대상: [코멘트 3175993398](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3175993398)
- 소속 리뷰 ID: 4216218541

> 클레스 레벨에서 Transactional을 사용하지 않고 public method에 어노테이션을 깜박한 경우 하나의 쿼리가 하나의 트랜잭션으로 작동하게 됩니다. 그랬을 경우 해당 메서드에서 두 개 이상의 쿼리가 있는 하나의 작업인데 중간에 실패할 경우 데이터의 정합성 깨지는 경우가 발생할 수 있다고 예상해봤습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,39 @@
+package roomescape.service;
+
+import java.util.List;
+import org.springframework.stereotype.Service;
+import org.springframework.transaction.annotation.Transactional;
+import roomescape.dao.ReservationTimeDao;
+import roomescape.domain.ReservationTime;
+import roomescape.service.dto.ReservationTimeCreateCommand;
+
+@Service
+@Transactional(readOnly = true)
+public class ReservationTimeService {
```

</details>

### 리뷰 본문 4216218541: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-03T12:35:27Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#pullrequestreview-4216218541)
- 리뷰 상태: `COMMENTED`

> 찰리 주말인데 자세한 피드백 감사합니다!
> 덕분에 이번에도 많이 배웠습니다!

### 인라인 코멘트 3178202507: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-03T13:48:44Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3178202507)
- 코드: `src/main/java/roomescape/dao/ReservationDao.java`, 현재 줄 None, 원래 줄 24
- 답변 대상: [코멘트 3175995307](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3175995307)
- 소속 리뷰 ID: 4216376680

> 앗, 이전 코멘트에서 RowMapper 의존에 대한 답변을 누락했네요! 😅
>
> 말씀대로 ReservationTimeDao의 RowMapper를 의존하여 맵핑 코드를 재사용하는 방법도 초기에 구현하고 고민해 보았습니다.
>
> 다만 그렇게 된다면 ReservationTime과 관련하여 변경이 있어 ReservationTimeDao의 RowMapper에 변경이 생기면 ReservationDao의 RowMapper도 변경해야 하는 의존성이 생기기때문에 맵핑 코드의 중복을 허용하더라도, 각 DAO의 쿼리와 맵핑 로직이 다른 DAO의 내부 구현에 의존하지 않도록 독립성을 보장하는 것이 유지보수에 더 유리하다고 판단했습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,68 @@
+package roomescape.dao;
+
+import java.time.LocalDate;
+import java.time.LocalTime;
+import java.util.List;
+import javax.sql.DataSource;
+import org.springframework.jdbc.core.RowMapper;
+import org.springframework.jdbc.core.namedparam.MapSqlParameterSource;
+import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
+import org.springframework.jdbc.core.namedparam.SqlParameterSource;
+import org.springframework.jdbc.core.simple.SimpleJdbcInsert;
+import org.springframework.stereotype.Repository;
+import roomescape.domain.Reservation;
+import roomescape.domain.ReservationTime;
+
+@Repository
+public class ReservationDao {
+    private final NamedParameterJdbcTemplate jdbcTemplate;
+    private final SimpleJdbcInsert simpleJdbcInsert;
+    private final RowMapper<Reservation> rowMapper = (rs, rowNum) -> {
+        ReservationTime time = new ReservationTime(
+                rs.getLong("time_id"),
+                rs.getObject("start_at", LocalTime.class)
+        );
```

</details>

### 리뷰 본문 4216376680: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-03T13:48:44Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#pullrequestreview-4216376680)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 3179256476: Gomding

- 상대방 발언, 참여자
- 시각: 2026-05-04T03:28:17Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3179256476)
- 코드: `src/main/java/roomescape/service/ReservationTimeService.java`, 현재 줄 12, 원래 줄 12
- 답변 대상: [코멘트 3175993398](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3175993398)
- 소속 리뷰 ID: 4217290596

> 오호 그럼
>
> > transaction 설정을 놓치는 실수를 방지할 수 있습니다.
>
> 실수가 발생한 것은 어떻게 인지할 수 있을까요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,39 @@
+package roomescape.service;
+
+import java.util.List;
+import org.springframework.stereotype.Service;
+import org.springframework.transaction.annotation.Transactional;
+import roomescape.dao.ReservationTimeDao;
+import roomescape.domain.ReservationTime;
+import roomescape.service.dto.ReservationTimeCreateCommand;
+
+@Service
+@Transactional(readOnly = true)
+public class ReservationTimeService {
```

</details>

### 인라인 코멘트 3179260117: Gomding

- 상대방 발언, 참여자
- 시각: 2026-05-04T03:30:26Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3179260117)
- 코드: `src/main/java/roomescape/dao/ReservationDao.java`, 현재 줄 None, 원래 줄 24
- 답변 대상: [코멘트 3175995307](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3175995307)
- 소속 리뷰 ID: 4217290596

> > 다만 그렇게 된다면 ReservationTime과 관련하여 변경이 있어 ReservationTimeDao의 RowMapper에 변경이 생기면 ReservationDao의 RowMapper도 변경해야 하는 의존성이 생기기때문에
>
> ReservationDao  ReservationTimeDao의 RowMapper 에 의존하고 있으면
> ReservationDao의 RowMapper 는 오히려 수정이 없어야하지 않을까요? 🤔
> (ReservationTimeDao 의 RowMapper 에만 수정이 존재하고 ReservationDao 는 그냥 RowMapper 를 가져다 사용하고 있을테니까요)
> 변경 전파가 어떻게 이뤄진다는것인지 이해하지 못했어요.. 😢

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,68 @@
+package roomescape.dao;
+
+import java.time.LocalDate;
+import java.time.LocalTime;
+import java.util.List;
+import javax.sql.DataSource;
+import org.springframework.jdbc.core.RowMapper;
+import org.springframework.jdbc.core.namedparam.MapSqlParameterSource;
+import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
+import org.springframework.jdbc.core.namedparam.SqlParameterSource;
+import org.springframework.jdbc.core.simple.SimpleJdbcInsert;
+import org.springframework.stereotype.Repository;
+import roomescape.domain.Reservation;
+import roomescape.domain.ReservationTime;
+
+@Repository
+public class ReservationDao {
+    private final NamedParameterJdbcTemplate jdbcTemplate;
+    private final SimpleJdbcInsert simpleJdbcInsert;
+    private final RowMapper<Reservation> rowMapper = (rs, rowNum) -> {
+        ReservationTime time = new ReservationTime(
+                rs.getLong("time_id"),
+                rs.getObject("start_at", LocalTime.class)
+        );
```

</details>

### 인라인 코멘트 3179264247: Gomding

- 상대방 발언, 참여자
- 시각: 2026-05-04T03:33:11Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3179264247)
- 코드: `src/main/java/roomescape/controller/advice/GlobalExceptionHandler.java`, 현재 줄 11, 원래 줄 11
- 답변 대상: [코멘트 3177982155](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3177982155)
- 소속 리뷰 ID: 4217290596

> 맞습니다~
> 에러 응답의 형태가 일관되지 않으니 클라이언트 쪽에서 호출할 때 문제가 되겠죠!
> 클라이언트 코드도 복잡해질테구요 ㅎㅎ..

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,23 @@
+package roomescape.controller.advice;
+
+import java.time.format.DateTimeParseException;
+import org.springframework.http.ResponseEntity;
+import org.springframework.http.converter.HttpMessageNotReadableException;
+import org.springframework.web.bind.annotation.ExceptionHandler;
+import org.springframework.web.bind.annotation.RestControllerAdvice;
+import roomescape.dto.ErrorResponse;
+
+@RestControllerAdvice
+public class GlobalExceptionHandler {
```

</details>

### 인라인 코멘트 3179267385: Gomding

- 상대방 발언, 참여자
- 시각: 2026-05-04T03:34:57Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3179267385)
- 코드: `src/main/java/roomescape/dto/ErrorResponse.java`, 현재 줄 3, 원래 줄 3
- 답변 대상: [코멘트 3177982595](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3177982595)
- 소속 리뷰 ID: 4217290596

> 👍 👍 👍
>
> 아래 글도 참고해보면 좋습니다! ㅎㅎ
> 글에서는 json string 이 아닌 json array 를 말하고있지만 결국 방향은 동일하다고 생각해요~
> - https://maltzj.com/posts/avoiding-json-arrays

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,4 @@
+package roomescape.dto;
+
+public record ErrorResponse(String message) {
```

</details>

### 인라인 코멘트 3179274476: Gomding

- 상대방 발언, 참여자
- 시각: 2026-05-04T03:38:33Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3179274476)
- 코드: `src/main/java/roomescape/controller/ReservationTimeController.java`, 현재 줄 None, 원래 줄 13
- 답변 대상: [코멘트 3177970471](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3177970471)
- 소속 리뷰 ID: 4217290596

> 넵 클라이언트와 소통하여 변경하는 식으로 진행합니다!
>
> 만약 신규 api 가 아니라 기존에 존재하는 api 에서 스펙을 수정하는 상황에는요..
> 클라이언트와 서버 배포가 동시에 이뤄지지않는다면
> 일시적으로 클라이언트와 서버간에 버전이 맞지않아 에러가 발생할 수는 있는데
> 요거는 몇가지 전략을 사용해서 극복할 수 있습니다 😄

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,39 @@
+package roomescape.controller;
+
+import java.util.List;
+import org.springframework.http.ResponseEntity;
+import org.springframework.web.bind.annotation.*;
+import roomescape.domain.ReservationTime;
+import roomescape.dto.ReservationTimeRequest;
+import roomescape.dto.ReservationTimeResponse;
+import roomescape.service.ReservationTimeService;
+
+@RestController
+@RequestMapping("/times")
+public class ReservationTimeController {
```

</details>

### 인라인 코멘트 3179287519: Gomding

- 상대방 발언, 참여자
- 시각: 2026-05-04T03:45:06Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3179287519)
- 코드: `src/main/java/roomescape/dao/entity/ReservationTimeEntity.java`, 현재 줄 None, 원래 줄 5
- 답변 대상: [코멘트 3177976926](https://github.com/woowacourse/spring-roomescape-admin/pull/427#discussion_r3177976926)
- 소속 리뷰 ID: 4217290596

> DB Entity 객체 와 도메인 Entity 객체 를 구분해야할 이유가 있을까요~
> 둘을 분리했을 떄 어떤 장점이 있는지 궁금합니다!
>
> 도메인 Entity 를 그대로 Repository 에 영속화 하는것은 자연스러운 것이라 생각해서요~
> Repository 라는 개념도 결국 도메인 Entity 를 영속화하는 저장소라는 것입니다 😄
> 저는 둘을 분리하려면 거기서 오는 장점이 확실해야한다고 생각해요
> 분리했을 때 복잡도가 높아지거든요!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,6 @@
+package roomescape.dao.entity;
+
+import java.time.LocalTime;
+
+public record ReservationTimeEntity(Long id, LocalTime startAt) {
```

</details>

### 리뷰 본문 4217290596: Gomding

- 상대방 발언, 참여자
- 시각: 2026-05-04T03:47:51Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-admin/pull/427#pullrequestreview-4217290596)
- 리뷰 상태: `APPROVED`

> 안녕하세요 고래!
> 레벨2 첫 미션 진행하느라 고생하셨어요 👍
> 요구사항은 다 만족한 상태라 이만 머지하겠습니다 ㅎㅎ
> 추가로 남긴 코멘트는 고민해보시면 좋겠어요 🤗
>
> 앞으로 레벨2 미션들도 화이팅입니다 🎉
> 궁금한 점 있으면 언제든 DM 남겨주세요!
