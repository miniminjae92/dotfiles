# woowacourse/spring-roomescape-member #418

[🚀 사이클1 - 미션 (테마 + 사용자 예약)] 고래(강민재) 미션 제출합니다.

- [GitHub PR](https://github.com/woowacourse/spring-roomescape-member/pull/418)
- PR 작성자: `miniminjae92`
- 머지 시각: 2026-05-12T13:35:44Z
- [API 원본](../raw/spring-roomescape-member-418.json)
- 리뷰와 댓글 54건(본문 있는 발언 44건, 본인 기록 28건)

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
> - [x] 미션의 필수 요구사항을 모두 구현했나요?
> - [x] Gradle `test`를 실행했을 때, 모든 테스트가 정상적으로 통과했나요?
> - [x] 애플리케이션이 정상적으로 실행되나요?
>
> ## 베이스 코드 선택 체크
> - [ ] 이전 미션의 내 코드에서 시작
> - [x] 이전 미션의 페어의 코드에서 시작
>
> ## 어떤 부분에 집중하여 리뷰해야 할까요?
> <!-- 리뷰어가 효과적으로 피드백할 수 있도록 중점적으로 리뷰 받고 싶은 내용을 *요약* 형태로 작성해 주세요.
> 리뷰해야 할 포인트를 요약해 강조해 주시면, 리뷰어가 코드 전체를 이 부분에 집중해 리뷰할 수 있습니다.
> 반면 특정 코드부분에 대한 피드백이 필요하다면, 이 곳에 적기 보다 해당 코드를 선택하고 코멘트를 남기는 것을 권장합니다. -->
>
> 안녕하세요, 웨지 반갑습니다.
> 8기 고래라고 합니다.
> 이번 리뷰, 잘 부탁드립니다 :)
>
> ## 그룹 규칙
>
> (If-Then) 기능 명세 또는 요구사항에 형용사와 명사가 섞여 있다면,
> → 명사를 리소스로, 형용사를 필터 또는 표현 조건으로 본다.
>
> (If-Then) 데이터에 검증이 필요하고 표현 방식이 상황에 따라 달라져야 한다면,
> → 최종 검증은 서버에서 책임지고, 표현은 클라이언트에서 책임진다.
> 응답 데이터의 표현에 관련된 처리는 생략하고, 원본 데이터를 넘긴다.
> (ex. 서버에서는 `20260504T144210`처럼 값을 넘기고, 프론트에서 `26년 5월 4일`로 표현)
>
> (If-Then) 하나의 API에서 관리자와 사용자에 대한 분기가 생기는 경우
> → API를 분리한다.
>
> (금지) 리소스 이름에 동사나 모호한 포괄적 단어를 포함하지 않는다.
>
> ## 규칙을 적용해서 변경한 코드
>
> 이번 단계에서는 테마, 예약 시간, 예약을 각각 리소스로 보고 API를 구성했습니다.
>
> - 테마: `GET /themes`, `POST /themes`, `DELETE /themes/{id}`, `GET /themes/rank`
> - 예약 시간: `GET /times`, `POST /times`, `DELETE /times/{id}`, `GET /times?themeId={themeId}&date={date}`
> - 예약: `GET /reservations`, `POST /reservations`, `DELETE /reservations/{id}`
>
> 생성 API는 모두 `201 Created`를 반환하도록 했고, 삭제 API는 본문 없이 `204 No Content`를 반환하도록 했습니다. 생성 후에는 클라이언트가 바로 다음 동작을 이어갈 수 있도록 생성된 리소스의 식별자를 응답 본문에 포함했습니다.
>
> ### 고민: 관리자와 사용자의 분리
>
> 관리자와 사용자의 엔드포인트 분리 기준을 처음에는 "분기가 생기는 경우"로 잡았습니다. 미션을 진행하면서 실제 컨트롤러 코드에서 관리자와 사용자 요청을 분기해야 하는 순간은 아직 없었기 때문에 `/admin` 계층을 별도로 만들지는 않았습니다.
>
> 다만 미션 전에는 관리자와 사용자가 액터 관점에서 목적과 관심사가 전혀 다르기 때문에 기능이 같더라도 엔드포인트를 분리해야 하지 않을까 생각했습니다. 그때 "기능이 완전히 같아도 분리해야 하는가?"라는 질문에는 명확히 답하지 못했습니다.
>
> 구현을 하면서 API는 클라이언트와 서버 사이의 규약이라는 생각이 더 강해졌습니다. 한 번 공개된 규약은 바꾸기 어렵기 때문에, 서비스가 커지기 전에 관리자와 사용자 API를 나누어 두는 편이 이후 확장에는 유리할 수 있다고 느꼈습니다.
>
> 현재 구현에서는 같은 유스케이스를 사용하는 상황이라 엔드포인트를 분리하지 않았습니다. 이후 관리자 화면에서만 필요한 응답 필드, 권한 검증, 검색 조건, 삭제 정책 등이 생긴다면 컨트롤러를 먼저 분리하고, 중복되는 유스케이스는 같은 서비스를 사용하다가 변경 이유가 달라지는 순간 서비스도 분리하는 방향이 좋겠다고 생각했습니다.
>
> ## API 설계 결정과 근거
>
> ### 테마 조회
>
> 테마 조회에서 고민했던 부분은 응답 필드였습니다.
>
> 1. `description`을 `NOT NULL`로 강제해야 하는가
> 2. 테마 id도 클라이언트에게 제공해야 하는가
> 3. 각 필드 이름에 구분 가능한 prefix를 붙여야 하는가
>
> 현재는 `description`과 `imageUrl`을 필수값으로 강제하지 않았습니다. 테마의 이름은 테마를 식별하고 노출하는 핵심 정보라 필수값으로 두었지만, 설명과 이미지는 운영 상황에 따라 비어 있을 수 있다고 판단했습니다.
>
> 테마 id는 응답에 포함했습니다. 화면에서는 이름, 설명, 이미지가 주로 보이지만 삭제, 예약 가능 시간 조회, 예약 생성처럼 후속 요청을 보내려면 식별자가 필요하기 때문입니다.
>
> 필드 이름에는 `themeName`, `themeDescription` 같은 prefix를 붙이지 않았습니다. 응답 객체가 이미 `ThemeResponse`라는 문맥을 가지고 있고, 중첩 객체로 내려가는 경우에도 `theme.name`처럼 클라이언트가 문맥을 구분할 수 있다고 판단했습니다.
>
> ### 테마 추가
>
> 테마 추가 API에서는 `200 OK`와 `201 Created` 중 무엇을 사용할지 고민했습니다. 현재는 새 리소스가 생성되는 요청이므로 `201 Created`를 반환하도록 했습니다.
>
> `Location` 헤더는 제공하지 않았습니다. 생성된 테마를 단건 조회하는 API가 아직 없고, 현재 클라이언트 흐름에서는 생성 직후 전체 목록을 다시 조회하거나 응답 본문의 id를 이용하는 방식으로 충분하다고 판단했습니다. 다만 REST 관점에서는 생성된 리소스의 위치를 제공하려면 `GET /themes/{id}`도 함께 제공하는 편이 더 자연스럽다고 생각합니다.
>
> ### 테마 삭제
>
> 삭제할 테마 id를 Path Variable에 둘지 Request Body에 둘지 고민했습니다. 현재는 `DELETE /themes/{id}`로 구현했습니다.
>
> 삭제는 특정 리소스에 대한 요청이므로 URI 자체가 삭제 대상을 나타내는 편이 명확하다고 판단했습니다. `DELETE /themes`에 id를 Body로 담아 보내면 URI만 봤을 때 모든 테마를 삭제하는 요청처럼 오해할 여지가 있다고 생각했습니다.
>
> 또한 Request Body를 사용하면 JSON을 파싱하고 요청 객체로 역직렬화하는 과정이 추가됩니다. 단순히 삭제 대상 id 하나만 필요한 요청이라면 Path Variable로 받는 편이 더 단순하다고 생각했습니다.
>
> DELETE 요청의 Body는 HTTP 표준에서 명확한 의미가 정의되어 있지 않고, 일부 클라이언트나 라이브러리, 중간 계층에서 Body를 무시할 가능성도 있다고 알고 있습니다. 그래서 단일 리소스 삭제에는 `DELETE /themes/{id}`처럼 Path Variable을 사용하는 방식이 더 적절하다고 판단했습니다.
>
> 구현에서는 테마를 실제로 삭제하지 않고 `is_deleted` 값을 변경하는 soft delete를 선택했습니다. 예약이 참조하고 있는 테마 정보를 보존해야 하고, 인기 테마 집계나 기존 예약 내역에서 과거 테마 데이터가 필요할 수 있기 때문입니다.
>
> ### 예약 가능 시간 조회
>
> 예약 가능 시간 조회에서는 다음을 고민했습니다.
>
> 1. URI 엔드포인트를 `reservations`, `times`, `themes` 중 어디에 둘 것인가
> 2. 예약 가능/불가능 전체를 제공할 것인가, 가능한 시간만 제공할 것인가
> 3. `available` 여부를 `Boolean`과 `boolean` 중 무엇으로 표현할 것인가
> 4. GET 요청 실패에 대한 예외 응답을 어떻게 처리할 것인가
>
> 현재는 `GET /times?themeId={themeId}&date={date}&available={available}`로 구현했습니다.
>
> 반환하는 주된 값이 예약 시간 목록이기 때문에 `times`에 요청하는 것이 자연스럽다고 판단했습니다. 예약 가능 여부는 "시간 목록을 어떤 날짜와 테마 조건으로 바라본 결과"라고 보았습니다.
>
> 다만 이 부분은 아직 고민이 남아 있습니다. 클라이언트 입장에서는 특정 테마를 먼저 선택한 뒤 해당 테마의 예약 가능 시간을 확인하는 흐름이기 때문에 `/themes/{themeId}/times?date={date}`가 더 자연스러울 수도 있다고 생각했습니다. 결국 어떤 리소스를 중심으로 볼지는 정답이 하나라기보다 팀 안에서 API를 바라보는 기준을 일관되게 맞추는 것이 중요하다고 느꼈습니다.
>
> 응답은 테마 정보와 시간 목록을 함께 내려주도록 했습니다. 시간 목록에는 `available` 값을 포함했고, 쿼리 파라미터 `available`을 생략하면 전체 시간, `true`를 전달하면 가능한 시간만, `false`를 전달하면 불가능한 시간만 조회할 수 있도록 했습니다.
>
> 요청 파라미터의 `available`은 `Boolean`으로 받았습니다. 원시 타입 `boolean`으로 받으면 값이 없을 때 `false`와 구분할 수 없어서, "필터 없음"과 "`false` 필터"를 구분하기 어렵기 때문입니다.
>
> 예약된 시간 id 목록은 DB에서 조회하고, 전체 예약 시간 목록과 비교해서 가능 여부를 만드는 방식으로 구현했습니다. 이 부분은 서비스에서 표현에 가까운 조합을 담당하고, DB는 예약된 시간 id를 찾는 역할만 하도록 나누었습니다.
>
> ### 예약 추가
>
> 예약 추가에서는 삭제 정책과 중복 예약 정책을 고민했습니다.
>
> 1. 예약된 건에 대한 예약 시간이나 테마를 삭제할 경우 어떻게 할 것인가
> 2. 동시에 같은 날짜, 시간, 테마로 예약한다면 어떻게 할 것인가
>
> 현재 예약 생성 전 `ReservationService`에서 같은 날짜, 테마, 시간에 이미 예약된 건이 있는지 확인하고, 이미 예약되어 있으면 `IllegalArgumentException`을 발생시키도록 했습니다.
>
> 다만 동시성까지 완전히 보장하려면 현재 서비스 검증만으로는 부족하다고 생각했습니다. 두 요청이 거의 동시에 들어오면 둘 다 예약 가능하다고 판단한 뒤 저장될 수 있기 때문입니다. 이 경우에는 DB에 `(date, time_id, theme_id)` 유니크 제약을 추가하거나 트랜잭션 격리 수준, 락 등을 함께 고려해야 할 것 같습니다.
>
> 삭제 정책은 테마와 예약 시간에서 다르게 구현했습니다. 테마는 `is_deleted`를 이용해 soft delete를 했고, 예약 시간은 실제 delete를 수행했습니다. 예약 시간이 기존 예약에서 참조 중이라면 DB 외래 키 제약으로 삭제가 실패하고, 이를 전역 예외 처리에서 "현재 다른 데이터에서 참조 중이어서 삭제할 수 없습니다."라는 응답으로 변환하도록 했습니다.
>
> 개인적으로는 삭제를 단순히 물리 삭제 또는 boolean soft delete로만 나누기보다, 테마의 상태를 `ACTIVE`, `INACTIVE`, `DELETED`처럼 표현하는 방법도 생각했습니다. 이렇게 하면 "예약 가능한 테마", "노출하지 않지만 과거 예약에서는 보존해야 하는 테마", "운영자가 임시로 비활성화한 테마"를 구분할 수 있기 때문입니다. 이번 단계에서는 요구사항과 구현 복잡도를 고려해 `is_deleted`만 사용했습니다.
>
> ### 인기 테마 조회
>
> 인기 테마 조회에서는 기존 데이터로부터 파생된 응답을 제공할 때 별도의 엔드포인트를 두어야 하는지 고민했습니다. 현재는 `GET /themes/rank?days={days}&limit={limit}`로 구현했습니다.
>
> 처음에는 인기 테마도 결국 테마 목록이므로 `GET /themes?sort=popular&days={days}&limit={limit}`처럼 쿼리 파라미터로 표현할 수 있지 않을까 생각했습니다. 하지만 인기 테마 응답은 단순히 테마 목록의 정렬만 바뀐 것이 아니라, 예약 데이터를 기준으로 집계한 결과이기도 하고, 원본 리소스인 `theme`만 조회하는 것이 아니라 `reservation` 데이터를 이용해 순위라는 새로운 의미를 만듭니다.
>
> 이런 파생 응답을 모두 쿼리 파라미터로만 표현하면 `GET /themes`가 담당하는 의미가 넓어질 수 있다고 느꼈습니다. 일반 테마 목록 조회, 이름 검색, 정렬 변경 정도라면 같은 리소스의 조회 조건으로 볼 수 있지만, 예약 수 집계와 순위 계산은 별도의 조회 목적에 가깝다고 판단했습니다. 그래서 `rank`를 테마 목록을 보는 하나의 파생 관점으로 보고 `/themes/rank` 엔드포인트를 두었습니다.
>
> 다만 `days`와 `limit`은 인기 테마라는 조회 목적 자체를 바꾸는 값이 아니라, 집계 기간과 반환 개수를 조절하는 조건이라고 보았습니다. 그래서 `/themes/rank/recent-7-days/top-10`처럼 경로에 조건을 고정하기보다 쿼리 파라미터로 열어두었습니다.
>
> 인기 테마는 DB에서 예약 수 기준으로 집계하고 정렬했습니다. 예약 수가 같은 경우에는 테마 이름 순으로 정렬했습니다. 응답에는 현재 순위와 테마 정보를 내려주고 있습니다. 미션을 작성하고나서 `from`, `to`, `count`도 함께 제공하면 클라이언트 기능확장에 더 도움이 되지 않을까 생각도 들었습니다.
>
> ## 테스트 작성이 어려웠던 코드
>
> `data.sql`을 사용했을 때 테스트에도 더미 데이터가 삽입되어 기존 테스트가 깨지는 문제가 있었습니다. 운영 실행용 더미 데이터와 테스트 데이터를 분리하기 위해 더미 데이터 파일 이름을 `dummy.sql`로 변경하고, `src/main/resources/application.properties`와 `src/test/resources/application.properties`를 각각 관리했습니다.
>
> 현재 main 설정에서는 `dummy.sql`을 로드하고, test 설정에서는 별도의 DB를 사용하면서 더미 데이터가 자동으로 들어가지 않도록 했습니다.
>
> 응답 데이터와 테스트 기대값의 타입을 맞춘다고 디버깅하기도 했습니다. 예를 들어 응답의 시간 형식은 JSON에서는 문자열로 표현되지만, 코드에서는 `LocalTime`을 사용하거나 시간에서 형식이 다르거나 해서 실제 응답 형식과 맞춰 검증하도록 했습니다.
>
> 이번 사이클에서는 잘못된 입력에 대한 에러 처리는 다음 사이클의 주제이고, 현재 사이클에서는 정상 흐름을 만드는 데 집중한다는 요구사항이 있었습니다. 그래서 의도적으로 검증 로직과 예외 케이스 테스트의 비중을 줄이고 정상 흐름을 먼저 완성하는 방향으로 진행했습니다.
>
> 다만 테스트와 검증을 줄이고 진행해보니 개인적으로는 많이 불편했습니다. 구현 속도는 빨라질 수 있었지만, 어떤 계층이 어떤 책임을 검증하고 있는지 확신하기 어려웠고, 변경 후에도 정상 흐름이 유지되는지 매번 수동으로 확인해야 하는 느낌이 있었습니다. 이번 경험을 통해 테스트가 단순히 버그를 찾기 위한 수단뿐 아니라, 내가 설계한 책임이 기대대로 동작하는지 확인하는 기준이 된다는 점을 더 크게 느꼈습니다.
>
> ## 막힌 순간
>
> 서비스 로직에서 처리할지, DB에서 처리할지 고민되는 부분에서 많이 막혔습니다.
>
> 예를 들어 예약 가능 시간 조회에서는 DB에서 조인과 계산을 모두 끝내고 `available`까지 만들어 내려줄 수도 있고, 현재 구현처럼 DB에서는 예약된 시간 id만 조회하고 서비스에서 전체 시간 목록과 비교할 수도 있습니다. 인기 테마 조회는 예약 수 기준 집계와 정렬이 핵심이라 DB에서 처리했습니다.
>
> 어떤 서비스나 레포지토리에서 다른 레포지토리를 주입받아도 되는지 고민이 있었습니다. 다른 레포나 Dao를 주입받으면 저는 의존성으로 변경의 이유가 늘어나고 문제가 발생한다고 생각했는데 페어와 이야기를 나누면서 변경하는 부분이 비슷하다고 느끼고 혼란이 왔습니다. 경험을 해보고 싶어 페어의 의견을 따라서 구현을 해봤고, 오히려 이 경험에서 막힌 부분인 서비스 로직과 DB 어디에서 처리하는 게 좋은지에 대한 고민을 할 수 있게 되는 계기가 됐습니다.
>
> 도메인과 엔티티를 둘 다 두는 것이 맞는지도 고민했습니다. 현재 구조에는 `Theme`, `ReservationTime`, `Reservation` 도메인과 repository 내부의 entity가 함께 존재합니다. 개인적으로는 도메인과 엔티티를 명확히 분리한다면 도메인은 DB 식별자인 id를 가지지 않는 편이 더 자연스럽다고 생각했습니다. 그것이 아니라면 하나만 두는 것이 맞다고 생각했었습니다. 이왕 분리할거면 나눠서 도메인은 정말 순수 도메인으로 남겨서 테스트에서 용이함을 느끼면 좋을 수 있다고 생각하기 때문입니다. 이런 새로운 구조에서 경험을 해보면서 CRUD 중심이고 도메인과 DB 구조가 거의 같은 단계라면, 엔티티와 도메인을 나누기보다 도메인 하나로 단순하게 시작하는 편이 더 단순해서 좋을 것 같다고 판단됐습니다. 도메인 규칙이 더 복잡해질 때 검토하는 편이 좋겠다고 느꼈습니다.
>
> Repository와 Dao 하나만 쓰면 안되는가?, 서비스와 레포지토리 사이에서 DTO가 필요한가? 에 대해서 의문이 있었고 전자에 대해서는 경험을 해보면서 레포지토리는 도메인, DAO는 DB라는 관심사에 접근하면 좋을 수 있겠다고 페어의 구조를 경험해보면서 이점을 느꼈습니다.
>
> DTO를 어느 계층까지 전달해도 되는지도 어려웠습니다. 서비스와 레포지토리 사이에서는 도메인을 주고받는 것이 자연스럽다고 생각해서, 별도의 DTO가 항상 필요한지는 의문이 있었습니다. 저장소가 도메인을 저장하고 복원하는 역할이라면 Service가 저장용 DTO를 만들어 Repository에 넘기는 것보다, 도메인을 넘기고 Repository가 필요한 형태로 저장하는 편이 계층 책임에 더 맞다고 느꼈습니다.
>
> 반면 Controller의 Request/Response DTO를 Service에서 직접 사용하는 것은 Service가 HTTP 요청과 응답 모양에 묶일 수 있다는 단점이 있습니다. 그래서 컨트롤러와 서비스 사이에는 필요하다면 `Command`, `Query`, `Result` 같은 애플리케이션 DTO를 둘 수 있다고 생각했습니다. 다만 이번 단계에서는 구조를 크게 바꾸기보다 현재 흐름을 유지하면서, 어떤 DTO가 꼭 필요한지와 어떤 DTO는 변환 비용만 늘리는지 고민해보는 데 집중했습니다.
>
> DB에서 조인을 할지, 서비스에서 조합할지, 정합성을 DB 제약으로 처리할지, 서비스 검증으로 처리할지도 아직 어렵습니다. 특히 날짜, 예약 시간, 테마에 대한 중복 예약은 서비스 검증으로 구현했지만 동시성까지 고려하면 DB 유니크 제약이 더 적절할 수 있다고 생각합니다.
>
> N+1 문제도 고민되었습니다. 단순히 `1:N`, `N:M` 같은 관계 종류만으로 판단하기보다 응답 모양과 쿼리 수가 데이터 개수에 비례해 증가하는지를 함께 봐야 한다고 느꼈습니다.
>
> 예를 들어 예약 목록처럼 응답 item 하나가 SQL row 하나에 대응되고, 예약마다 시간과 테마 하나씩만 붙는 평평한 목록이라면 JOIN이 적절할 수 있습니다. 반대로 부모 하나에 여러 자식 목록이 붙는 계층형 응답이라면 JOIN 후 grouping이 필요하거나 쿼리를 분리하는 편이 나을 수 있습니다. 이번 경험으로 반복문 안에서의 DB 관련된 로직이 있다면 주의깊게 살펴봐야겠다고 느꼈습니다.

## 대화와 리뷰 기록

### 인라인 코멘트 3207889998: sihyung92

- 상대방 발언, 참여자
- 시각: 2026-05-08T09:56:50Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3207889998)
- 코드: `src/main/java/roomescape/global/exception/GlobalExceptionHandler.java`, 현재 줄 None, 원래 줄 19
- 소속 리뷰 ID: 4251347457

> 커스텀 예외 추천드릴게요. IllegalArgumentException는 어떤 식으로든 발생할 수 있어서, 의도하지 않은 예외메시지를 노출하는 게 보안 문제가 생길 수 있어서요.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,35 @@
+package roomescape.global.exception;
+
+import lombok.extern.slf4j.Slf4j;
+import org.springframework.dao.DataIntegrityViolationException;
+import org.springframework.http.HttpStatus;
+import org.springframework.http.ResponseEntity;
+import org.springframework.web.bind.annotation.ExceptionHandler;
+import org.springframework.web.bind.annotation.RestControllerAdvice;
+import roomescape.global.exception.dto.ErrorResponse;
+
+@Slf4j
+@RestControllerAdvice
+public class GlobalExceptionHandler {
+
+    @ExceptionHandler(IllegalArgumentException.class)
+    public ResponseEntity<ErrorResponse> handleIllegalArgumentException(IllegalArgumentException e) {
+        log.info(e.getMessage());
+        return ResponseEntity.badRequest()
+                .body(new ErrorResponse(e.getMessage()));
```

</details>

### 인라인 코멘트 3207942444: sihyung92

- 상대방 발언, 참여자
- 시각: 2026-05-08T10:07:06Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3207942444)
- 코드: `src/main/java/roomescape/reservation/repository/entity/ReservationEntity.java`, 현재 줄 None, 원래 줄 7
- 소속 리뷰 ID: 4251347457

> db 테이블 구조와 도메인 구조가 다른 아키텍처가 아닌데 entity를 도입하는 설계로 시작하시는게 이상하네요. 어떤 실익이 있나요?
> 학습 용도로 겪어보시는 게 아니라면 걷어내는 걸 권해볼게요.
>
>

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,22 @@
+package roomescape.reservation.repository.entity;
+
+import java.time.LocalDate;
+import lombok.Getter;
+
+@Getter
+public class ReservationEntity {
```

</details>

### 인라인 코멘트 3207977512: sihyung92

- 상대방 발언, 참여자
- 시각: 2026-05-08T10:13:43Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3207977512)
- 코드: `src/main/java/roomescape/reservation/repository/ReservationRepository.java`, 현재 줄 None, 원래 줄 30
- 소속 리뷰 ID: 4251347457

> 금지기술을 두 가지 섞어쓰시는 걸 보니 아찔한데요
>
> row가 늘어나는 테이블에서 findAll은 금지입니다. 규모가 어느정도 있는 프로덕션에선 바로 장애납니다.
>
> 세 도메인 모두 findAll 대신 페이징 적용해보시고요
>
> 그리고 그 내부에서 for문으로 N+1을 스스로 만들어내는 건 잘못된 설계에요.
> ORM은 여러 이점이 있지만 N+1 같은 문제를 예방하기 어렵다는 치명적인 단점을 가지고 있는데,
> 이 코드는 그 단점만 답습하고 있어요.
>
> 우선 되는 코드를 만들어야 하는게 우테코 정신인데, 성능이라는 비기능적 요구사항을 우선 충족해야죠.
> 개발자는 돈 받고 일하는 프로인데, 임금 지급하시는 분들은 DDD니 뭐니 개발자들이 떠들고 코드에 이러쿵 저러쿵하는 것에 대해 장기 유지보수성이라는 가치가 있을거라고 신뢰하고 투자하시는 거에요. 그런데 장기적으로 유익이 있을지 없을지 확실치 않은 코드 이념에 당장 기능도 안 돌아가게 만들면 임금을 받을 명목이 없습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,48 @@
+package roomescape.reservation.repository;
+
+import java.util.List;
+import lombok.RequiredArgsConstructor;
+import org.springframework.stereotype.Repository;
+import roomescape.reservation.domain.Reservation;
+import roomescape.reservation.mapper.ReservationMapper;
+import roomescape.reservation.repository.dao.ReservationDao;
+import roomescape.reservation.repository.dto.CreateReservationParams;
+import roomescape.reservation.repository.entity.ReservationEntity;
+import roomescape.theme.repository.dao.ThemeDao;
+import roomescape.theme.repository.entity.ThemeEntity;
+import roomescape.time.repository.dao.ReservationTimeDao;
+import roomescape.time.repository.entity.ReservationTimeEntity;
+
+@Repository
+@RequiredArgsConstructor
+public class ReservationRepository {
+
+    private final ReservationDao reservationDao;
+    private final ReservationTimeDao reservationTimeDao;
+    private final ThemeDao themeDao;
+
+    public List<Reservation> findAll() {
+        return reservationDao.selectAll().stream()
+                .map(reservation ->
+                        ReservationMapper.toReservation(reservation,
+                                reservationTimeDao.getByID(reservation.getTimeId()),
+                                themeDao.getById(reservation.getThemeId()))
+                ).toList();
```

</details>

### 인라인 코멘트 3208121263: sihyung92

- 상대방 발언, 참여자
- 시각: 2026-05-08T10:42:42Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3208121263)
- 코드: `src/main/java/roomescape/reservation/repository/ReservationRepository.java`, 현재 줄 None, 원래 줄 36
- 소속 리뷰 ID: 4251347457

> ID 에 대한 컨벤션이 메서드마다 상이한거 같네요. Id 쪽이 많은 것 같으니 Id로 맞춰주시죠
>
> ```suggestion
>         ReservationTimeEntity reservationTimeEntity = reservationTimeDao.getById(params.timeId());
> ```

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,48 @@
+package roomescape.reservation.repository;
+
+import java.util.List;
+import lombok.RequiredArgsConstructor;
+import org.springframework.stereotype.Repository;
+import roomescape.reservation.domain.Reservation;
+import roomescape.reservation.mapper.ReservationMapper;
+import roomescape.reservation.repository.dao.ReservationDao;
+import roomescape.reservation.repository.dto.CreateReservationParams;
+import roomescape.reservation.repository.entity.ReservationEntity;
+import roomescape.theme.repository.dao.ThemeDao;
+import roomescape.theme.repository.entity.ThemeEntity;
+import roomescape.time.repository.dao.ReservationTimeDao;
+import roomescape.time.repository.entity.ReservationTimeEntity;
+
+@Repository
+@RequiredArgsConstructor
+public class ReservationRepository {
+
+    private final ReservationDao reservationDao;
+    private final ReservationTimeDao reservationTimeDao;
+    private final ThemeDao themeDao;
+
+    public List<Reservation> findAll() {
+        return reservationDao.selectAll().stream()
+                .map(reservation ->
+                        ReservationMapper.toReservation(reservation,
+                                reservationTimeDao.getByID(reservation.getTimeId()),
+                                themeDao.getById(reservation.getThemeId()))
+                ).toList();
+    }
+
+    public Reservation save(CreateReservationParams params) {
+        Long id = reservationDao.insert(params.name(), params.date(), params.timeId(), params.themeId());
+        ReservationEntity reservationEntity = new ReservationEntity(id, params.name(), params.date(), params.timeId(), params.themeId());
+        ReservationTimeEntity reservationTimeEntity = reservationTimeDao.getByID(params.timeId());
```

</details>

### 인라인 코멘트 3208137920: sihyung92

- 상대방 발언, 참여자
- 시각: 2026-05-08T10:46:19Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3208137920)
- 코드: `src/main/resources/schema.sql`, 현재 줄 18, 원래 줄 18
- 소속 리뷰 ID: 4251347457

> 이거 DataIntegrityViolationException 핸들러 만드신거보면 unique 제약조건이 있을거라고 생각하신것 같은데요. unique 조건이 없습니다.
>
> 고민해주신 걸 보니 도메인 처리와 DB 처리 중 고민하신 게 있던데, **둘 다 해야죠**
>
> 요새는 도메인 불변식을 어플리케이션 코드에서 가져가고 DB 제약조건은 가볍게 가져가는 편이지만, 어플리케이션 코드 내에서 동시성을 해결할 수 가 없어요.
>
> DB는 예외상황에 대한 대응을 설치하는 거고요. 동시성은 드문 경우이니 대부분은 어플리케이션에서 해결한다고 가정하고, 혹시 모를 동시성을 DB에서 방어한다는 개념으로 접근해야합니다.
>
>

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,28 @@
+CREATE TABLE reservation_time
+(
+    id       BIGINT       NOT NULL AUTO_INCREMENT,
+    start_at VARCHAR(255) NOT NULL,
+    PRIMARY KEY (id)
+);
+
+CREATE TABLE theme
+(
+    id          BIGINT       NOT NULL AUTO_INCREMENT,
+    name        VARCHAR(255) NOT NULL,
+    description VARCHAR(255),
+    image_url    VARCHAR(512),
+    is_deleted BOOLEAN DEFAULT FALSE,
+    PRIMARY KEY (id)
+);
+
+CREATE TABLE reservation
```

</details>

### 인라인 코멘트 3208160445: sihyung92

- 상대방 발언, 참여자
- 시각: 2026-05-08T10:51:08Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3208160445)
- 코드: `src/main/java/roomescape/reservation/service/ReservationService.java`, 현재 줄 None, 원래 줄 1
- 소속 리뷰 ID: 4251347457

> 패키지 구조가 도메인 단위로 분리하고 내부에선 레이어드를 채용하셨는데요.
>
> 이렇게 분리하기엔 패키지간 참조가 너무 빈번하지 않던가요?
>
> 패키지는 디렉토리라는 강력한 표지(beacon) 중에 하나여서 개발자로 하여금 어떠한 기대를 하게 합니다. 그 중 하나는 '서로 자주 참조하는 클래스끼리 한 패키지에 묶는다' 는 게 있을텐데요. 지금은 패키지간 양방 참조가 빈번해서 여러 패키지로 쪼개어 관리하는 이점이 없어보이네요.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,58 @@
+package roomescape.reservation.service;
```

</details>

### 인라인 코멘트 3208194567: sihyung92

- 상대방 발언, 참여자
- 시각: 2026-05-08T10:58:36Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3208194567)
- 코드: `src/main/java/roomescape/reservation/repository/dto/CreateReservationParams.java`, 현재 줄 None, 원래 줄 9
- 소속 리뷰 ID: 4251347457

> 서비스에서 이미 검증을 위해 한번씩 fetch를 해오는 데이터인데, 왜 조회 결과를 그대로 가져오지 않나요? 등록할 때 또 조회를 하게 됩니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,11 @@
+package roomescape.reservation.repository.dto;
+
+import java.time.LocalDate;
+
+public record CreateReservationParams(
+        String name,
+        LocalDate date,
+        Long timeId,
+        Long themeId
```

</details>

### 인라인 코멘트 3208218250: sihyung92

- 상대방 발언, 참여자
- 시각: 2026-05-08T11:03:17Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3208218250)
- 코드: `src/main/java/roomescape/controller/ReservationController.java`, 현재 줄 30, 원래 줄 25
- 소속 리뷰 ID: 4251347457

> > 구현을 하면서 API는 클라이언트와 서버 사이의 규약이라는 생각이 더 강해졌습니다. 한 번 공개된 규약은 바꾸기 어렵기 때문에, 서비스가 커지기 전에 관리자와 사용자 API를 나누어 두는 편이 이후 확장에는 유리할 수 있다고 느꼈습니다.
>
> 진술은 맞는데 결론은 틀리다고 생각하는데요.
> 관리자와 사용자 API가 동일한 상황에선 어떤 클라든 이 API를 보면 되죠. 어쨌든 동일한 host에서 제공하고 있으니까요.
>
> 나중에 관리자가 추가 필드가 필요하면 그때 관리자는 어차피 프론트 코드 작업이 필요해요. 해당 기능을 반영해줄 때 새로운 엔드포인트를 그때 가서 추가하고, 엔드포인트를 알려주면 됩니다.
>
> 미리 나눠놓는 것은 누구에게도 이득이 되지 않습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,45 @@
+package roomescape.reservation.controller;
+
+import java.util.List;
+import lombok.RequiredArgsConstructor;
+import org.springframework.http.HttpStatus;
+import org.springframework.http.ResponseEntity;
+import org.springframework.web.bind.annotation.DeleteMapping;
+import org.springframework.web.bind.annotation.GetMapping;
+import org.springframework.web.bind.annotation.PathVariable;
+import org.springframework.web.bind.annotation.PostMapping;
+import org.springframework.web.bind.annotation.RequestBody;
+import org.springframework.web.bind.annotation.RequestMapping;
+import org.springframework.web.bind.annotation.RestController;
+import roomescape.reservation.controller.dto.CreateReservationRequest;
+import roomescape.reservation.controller.dto.ReservationResponse;
+import roomescape.reservation.service.ReservationService;
+
+@RestController
+@RequestMapping("/reservations")
+@RequiredArgsConstructor
+public class ReservationController {
+
+    private final ReservationService reservationService;
+
+    @GetMapping
```

</details>

### 인라인 코멘트 3208229706: sihyung92

- 상대방 발언, 참여자
- 시각: 2026-05-08T11:05:46Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3208229706)
- 코드: `src/main/java/roomescape/time/repository/dao/ReservationTimeDao.java`, 현재 줄 None, 원래 줄 70
- 소속 리뷰 ID: 4251347457

> 이건 ReservationRepository의 기능 아닐까요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,71 @@
+package roomescape.time.repository.dao;
+
+import java.time.LocalDate;
+import java.time.LocalTime;
+import java.time.format.DateTimeFormatter;
+import java.util.List;
+import java.util.Optional;
+import javax.sql.DataSource;
+import org.springframework.jdbc.core.JdbcTemplate;
+import org.springframework.jdbc.core.RowMapper;
+import org.springframework.jdbc.core.namedparam.MapSqlParameterSource;
+import org.springframework.jdbc.core.namedparam.SqlParameterSource;
+import org.springframework.jdbc.core.simple.SimpleJdbcInsert;
+import org.springframework.stereotype.Repository;
+import roomescape.time.repository.entity.ReservationTimeEntity;
+
+@Repository
+public class ReservationTimeDao {
+
+    private static final RowMapper<ReservationTimeEntity> reservationTimeRowMapper = (rs, rowNum) ->
+            new ReservationTimeEntity(
+                    rs.getLong("id"),
+                    LocalTime.parse(rs.getString("start_at"), DateTimeFormatter.ofPattern("HH:mm"))
+            );
+
+    private final JdbcTemplate jdbcTemplate;
+    private final SimpleJdbcInsert simpleJdbcInsert;
+
+    public ReservationTimeDao(JdbcTemplate jdbcTemplate, DataSource dataSource) {
+        this.jdbcTemplate = jdbcTemplate;
+        this.simpleJdbcInsert = new SimpleJdbcInsert(dataSource)
+                .withTableName("reservation_time")
+                .usingGeneratedKeyColumns("id");
+    }
+
+    public Long insert(LocalTime startAt) {
+        SqlParameterSource parameters = new MapSqlParameterSource()
+                .addValue("startAt", startAt);
+        return simpleJdbcInsert.executeAndReturnKey(parameters).longValue();
+    }
+
+    public Optional<ReservationTimeEntity> selectById(Long id) {
+        String sql = "select * from reservation_time where id = ?;";
+        return jdbcTemplate.query(sql, reservationTimeRowMapper, id)
+                .stream()
+                .findFirst();
+    }
+
+    public ReservationTimeEntity getByID(Long id) {
+        String sql = "select * from reservation_time where id = ?;";
+        return jdbcTemplate.queryForObject(sql, reservationTimeRowMapper, id);
+    }
+
+    public List<ReservationTimeEntity> selectAll() {
+        String sql = "select * from reservation_time;";
+        return jdbcTemplate.query(sql, reservationTimeRowMapper);
+    }
+
+    public int deleteById(Long id) {
+        String sql = "delete from reservation_time where id = ?;";
+        return jdbcTemplate.update(sql, id);
+    }
+
+    public List<Long> selectReservedTimeIds(Long themeId, LocalDate date) {
+        String sql = "select time_id " +
+                "from reservation " +
+                "where theme_id = ? and date = ?;";
+
+        return jdbcTemplate.queryForList(sql, Long.class, themeId, date.toString());
+    }
```

</details>

### 인라인 코멘트 3208242883: sihyung92

- 상대방 발언, 참여자
- 시각: 2026-05-08T11:08:39Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3208242883)
- 코드: `src/main/java/roomescape/time/repository/dto/CreateReservationTimeParams.java`, 현재 줄 None, 원래 줄 5
- 소속 리뷰 ID: 4251347457

> > DTO를 어느 계층까지 전달해도 되는지도 어려웠습니다. 서비스와 레포지토리 사이에서는 도메인을 주고받는 것이 자연스럽다고 생각해서, 별도의 DTO가 항상 필요한지는 의문이 있었습니다. 저장소가 도메인을 저장하고 복원하는 역할이라면 Service가 저장용 DTO를 만들어 Repository에 넘기는 것보다, 도메인을 넘기고 Repository가 필요한 형태로 저장하는 편이 계층 책임에 더 맞다고 느꼈습니다.
>
> 해당 객체처럼 구현해보고 깨달은 걸까요? 혹은 다른 얘기였을까요?
> repository dto들이 어떤 이유로 존재하는지 잘 모르겠네요

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,8 @@
+package roomescape.time.repository.dto;
+
+import java.time.LocalTime;
+
+public record CreateReservationTimeParams(
```

</details>

### 인라인 코멘트 3208255102: sihyung92

- 상대방 발언, 참여자
- 시각: 2026-05-08T11:11:22Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3208255102)
- 코드: `src/main/java/roomescape/theme/repository/dto/GetThemeRankingsInRecentDaysParams.java`, 현재 줄 None, 원래 줄 8
- 소속 리뷰 ID: 4251347457

> 정적 메서드 내부에서 now를 선언하면 테스트가 어려워져요. 인자로 수신해보면 어떨까요

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,12 @@
+package roomescape.theme.repository.dto;
+
+import java.time.LocalDate;
+
+public record GetThemeRankingsInRecentDaysParams(String startDate, String endDate, int limit) {
+
+    public static GetThemeRankingsInRecentDaysParams of(int days, int limit) {
+        LocalDate today = LocalDate.now();
```

</details>

### 인라인 코멘트 3208269057: sihyung92

- 상대방 발언, 참여자
- 시각: 2026-05-08T11:14:27Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3208269057)
- 코드: `src/main/resources/schema.sql`, 현재 줄 None, 원래 줄 4
- 소속 리뷰 ID: 4251347457

> varchar 대신 시간자료형으로 선언해서 구현해보셔요.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,28 @@
+CREATE TABLE reservation_time
+(
+    id       BIGINT       NOT NULL AUTO_INCREMENT,
+    start_at VARCHAR(255) NOT NULL,
```

</details>

### 인라인 코멘트 3208278043: sihyung92

- 상대방 발언, 참여자
- 시각: 2026-05-08T11:16:18Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3208278043)
- 코드: `src/main/java/roomescape/theme/controller/ThemeController.java`, 현재 줄 None, 원래 줄 35
- 소속 리뷰 ID: 4251347457

> 최소 최대값 정해주셔요. days=999999, limit=999999999999 같은 파라미터가 호출되면 장애가 날 수 있어요.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,53 @@
+package roomescape.theme.controller;
+
+import java.util.List;
+import lombok.RequiredArgsConstructor;
+import org.springframework.http.HttpStatus;
+import org.springframework.http.ResponseEntity;
+import org.springframework.web.bind.annotation.DeleteMapping;
+import org.springframework.web.bind.annotation.GetMapping;
+import org.springframework.web.bind.annotation.PathVariable;
+import org.springframework.web.bind.annotation.PostMapping;
+import org.springframework.web.bind.annotation.RequestBody;
+import org.springframework.web.bind.annotation.RequestMapping;
+import org.springframework.web.bind.annotation.RequestParam;
+import org.springframework.web.bind.annotation.RestController;
+import roomescape.theme.controller.dto.CreateThemeRequest;
+import roomescape.theme.controller.dto.ThemeRankResponse;
+import roomescape.theme.controller.dto.ThemeResponse;
+import roomescape.theme.service.ThemeService;
+
+@RestController
+@RequestMapping("/themes")
+@RequiredArgsConstructor
+public class ThemeController {
+
+    private final ThemeService themeService;
+
+    @GetMapping
+    public ResponseEntity<List<ThemeResponse>> getThemes() {
+        return ResponseEntity.ok(themeService.findAllThemes());
+    }
+
+    @GetMapping("/rank")
+    public ResponseEntity<List<ThemeRankResponse>> getRankedThemes(
+            @RequestParam int days,
+            @RequestParam int limit
```

</details>

### 리뷰 본문 4251347457: sihyung92

- 상대방 발언, 참여자
- 시각: 2026-05-08T11:17:55Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#pullrequestreview-4251347457)
- 리뷰 상태: `CHANGES_REQUESTED`

> 안녕하세요 고래, 리뷰어 웨지입니다.
> pr 코멘트를 보면 많은 걸 느끼신 미션 같네요. 생각을 깊게 해주신 거 같은데, 이 깨달음들이 코드에 잘 녹아든 버전을 보고 싶네요.
>
> 불편하셨던 점들과 리뷰를 반영해서 또 요청주셔요.
>

### 인라인 코멘트 3213475805: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-09T17:03:21Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3213475805)
- 코드: `src/main/java/roomescape/global/exception/GlobalExceptionHandler.java`, 현재 줄 None, 원래 줄 19
- 답변 대상: [코멘트 3207889998](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3207889998)
- 소속 리뷰 ID: 4258093045

> 네, 제가 의도하지 않은 곳에서 예외 발생하면서 민감한 정보의 노출이 생길 수 있겠네요. 수정 해볼게요.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,35 @@
+package roomescape.global.exception;
+
+import lombok.extern.slf4j.Slf4j;
+import org.springframework.dao.DataIntegrityViolationException;
+import org.springframework.http.HttpStatus;
+import org.springframework.http.ResponseEntity;
+import org.springframework.web.bind.annotation.ExceptionHandler;
+import org.springframework.web.bind.annotation.RestControllerAdvice;
+import roomescape.global.exception.dto.ErrorResponse;
+
+@Slf4j
+@RestControllerAdvice
+public class GlobalExceptionHandler {
+
+    @ExceptionHandler(IllegalArgumentException.class)
+    public ResponseEntity<ErrorResponse> handleIllegalArgumentException(IllegalArgumentException e) {
+        log.info(e.getMessage());
+        return ResponseEntity.badRequest()
+                .body(new ErrorResponse(e.getMessage()));
```

</details>

### 인라인 코멘트 3213533684: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-09T17:36:43Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3213533684)
- 코드: `src/main/java/roomescape/controller/ReservationController.java`, 현재 줄 30, 원래 줄 25
- 답변 대상: [코멘트 3208218250](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3208218250)
- 소속 리뷰 ID: 4258093045

> 오히려 오버엔지니어링이 될 수 있겠네요.
> 자연스러운 변경에 대해서 다시 생각해보게 되네요. 감사합니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,45 @@
+package roomescape.reservation.controller;
+
+import java.util.List;
+import lombok.RequiredArgsConstructor;
+import org.springframework.http.HttpStatus;
+import org.springframework.http.ResponseEntity;
+import org.springframework.web.bind.annotation.DeleteMapping;
+import org.springframework.web.bind.annotation.GetMapping;
+import org.springframework.web.bind.annotation.PathVariable;
+import org.springframework.web.bind.annotation.PostMapping;
+import org.springframework.web.bind.annotation.RequestBody;
+import org.springframework.web.bind.annotation.RequestMapping;
+import org.springframework.web.bind.annotation.RestController;
+import roomescape.reservation.controller.dto.CreateReservationRequest;
+import roomescape.reservation.controller.dto.ReservationResponse;
+import roomescape.reservation.service.ReservationService;
+
+@RestController
+@RequestMapping("/reservations")
+@RequiredArgsConstructor
+public class ReservationController {
+
+    private final ReservationService reservationService;
+
+    @GetMapping
```

</details>

### 인라인 코멘트 3213582786: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-09T17:55:16Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3213582786)
- 코드: `src/main/java/roomescape/reservation/repository/dto/CreateReservationParams.java`, 현재 줄 None, 원래 줄 9
- 답변 대상: [코멘트 3208194567](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3208194567)
- 소속 리뷰 ID: 4258093045

> 저도 불필요한 작업이라고 생각합니다. 수정 해볼게요.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,11 @@
+package roomescape.reservation.repository.dto;
+
+import java.time.LocalDate;
+
+public record CreateReservationParams(
+        String name,
+        LocalDate date,
+        Long timeId,
+        Long themeId
```

</details>

### 인라인 코멘트 3213592564: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-09T17:59:01Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3213592564)
- 코드: `src/main/java/roomescape/reservation/repository/entity/ReservationEntity.java`, 현재 줄 None, 원래 줄 7
- 답변 대상: [코멘트 3207942444](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3207942444)
- 소속 리뷰 ID: 4258093045

> 동일한 경우 도입해본 경험이 생겼습니다.
> 복잡도가 증가하고 무의미한 코드가 증가한다고 생각되네요. 수정 해볼게요.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,22 @@
+package roomescape.reservation.repository.entity;
+
+import java.time.LocalDate;
+import lombok.Getter;
+
+@Getter
+public class ReservationEntity {
```

</details>

### 인라인 코멘트 3213621173: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-09T18:09:32Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3213621173)
- 코드: `src/main/java/roomescape/reservation/service/ReservationService.java`, 현재 줄 None, 원래 줄 1
- 답변 대상: [코멘트 3208160445](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3208160445)
- 소속 리뷰 ID: 4258093045

> 처음엔 페어의 구조를 보고 신선한 충격을 받았었는데요, 패키지를 도메인 단위로 분리한다는 것 자체가 초기 프로젝트에서는 어려울 것이라고 체감할 수 있었습니다. 패키지의 본질에 대해서 생각하고 사용하도록 해야겠네요.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,58 @@
+package roomescape.reservation.service;
```

</details>

### 인라인 코멘트 3213631269: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-09T18:12:42Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3213631269)
- 코드: `src/main/java/roomescape/reservation/repository/ReservationRepository.java`, 현재 줄 None, 원래 줄 30
- 답변 대상: [코멘트 3207977512](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3207977512)
- 소속 리뷰 ID: 4258093045

> 규모가 어느정도 있다면 다른 처리없이 findAll하면 메모리 문제가 발생 하겠네요.
> row가 늘어나는 테이블에 대해서 더욱 신경쓰도록 할게요!
> N+1 만큼 DB와 네트워크가 늘어난다고 생각하면 큰 문제라고 생각되네요, 수정 해볼게요!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,48 @@
+package roomescape.reservation.repository;
+
+import java.util.List;
+import lombok.RequiredArgsConstructor;
+import org.springframework.stereotype.Repository;
+import roomescape.reservation.domain.Reservation;
+import roomescape.reservation.mapper.ReservationMapper;
+import roomescape.reservation.repository.dao.ReservationDao;
+import roomescape.reservation.repository.dto.CreateReservationParams;
+import roomescape.reservation.repository.entity.ReservationEntity;
+import roomescape.theme.repository.dao.ThemeDao;
+import roomescape.theme.repository.entity.ThemeEntity;
+import roomescape.time.repository.dao.ReservationTimeDao;
+import roomescape.time.repository.entity.ReservationTimeEntity;
+
+@Repository
+@RequiredArgsConstructor
+public class ReservationRepository {
+
+    private final ReservationDao reservationDao;
+    private final ReservationTimeDao reservationTimeDao;
+    private final ThemeDao themeDao;
+
+    public List<Reservation> findAll() {
+        return reservationDao.selectAll().stream()
+                .map(reservation ->
+                        ReservationMapper.toReservation(reservation,
+                                reservationTimeDao.getByID(reservation.getTimeId()),
+                                themeDao.getById(reservation.getThemeId()))
+                ).toList();
```

</details>

### 인라인 코멘트 3213634145: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-09T18:13:46Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3213634145)
- 코드: `src/main/java/roomescape/theme/repository/dto/GetThemeRankingsInRecentDaysParams.java`, 현재 줄 None, 원래 줄 8
- 답변 대상: [코멘트 3208255102](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3208255102)
- 소속 리뷰 ID: 4258093045

> 실행 시점마다 비결정적 상태가 되어 테스트가 사실상 불가능 하겠네요. 수정 해볼게요!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,12 @@
+package roomescape.theme.repository.dto;
+
+import java.time.LocalDate;
+
+public record GetThemeRankingsInRecentDaysParams(String startDate, String endDate, int limit) {
+
+    public static GetThemeRankingsInRecentDaysParams of(int days, int limit) {
+        LocalDate today = LocalDate.now();
```

</details>

### 인라인 코멘트 3213645588: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-09T18:17:34Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3213645588)
- 코드: `src/main/java/roomescape/time/repository/dto/CreateReservationTimeParams.java`, 현재 줄 None, 원래 줄 5
- 답변 대상: [코멘트 3208242883](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3208242883)
- 소속 리뷰 ID: 4258093045

> 저도 공감되네요. 앞으로 예측보다 정말 필요해지는 시점에 도입을 하도록 해볼려고 해요.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,8 @@
+package roomescape.time.repository.dto;
+
+import java.time.LocalTime;
+
+public record CreateReservationTimeParams(
```

</details>

### 인라인 코멘트 3213651163: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-09T18:19:16Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3213651163)
- 코드: `src/main/java/roomescape/time/repository/dao/ReservationTimeDao.java`, 현재 줄 None, 원래 줄 70
- 답변 대상: [코멘트 3208229706](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3208229706)
- 소속 리뷰 ID: 4258093045

> ReservationTimeDao는 reservation_time 테이블에 대한 데이터 접근을 캡슐화하고 책임지는 객체인데 해당 쿼리는 ReservationDao에서 해야하는 것이 올바르다고 생각되네요.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,71 @@
+package roomescape.time.repository.dao;
+
+import java.time.LocalDate;
+import java.time.LocalTime;
+import java.time.format.DateTimeFormatter;
+import java.util.List;
+import java.util.Optional;
+import javax.sql.DataSource;
+import org.springframework.jdbc.core.JdbcTemplate;
+import org.springframework.jdbc.core.RowMapper;
+import org.springframework.jdbc.core.namedparam.MapSqlParameterSource;
+import org.springframework.jdbc.core.namedparam.SqlParameterSource;
+import org.springframework.jdbc.core.simple.SimpleJdbcInsert;
+import org.springframework.stereotype.Repository;
+import roomescape.time.repository.entity.ReservationTimeEntity;
+
+@Repository
+public class ReservationTimeDao {
+
+    private static final RowMapper<ReservationTimeEntity> reservationTimeRowMapper = (rs, rowNum) ->
+            new ReservationTimeEntity(
+                    rs.getLong("id"),
+                    LocalTime.parse(rs.getString("start_at"), DateTimeFormatter.ofPattern("HH:mm"))
+            );
+
+    private final JdbcTemplate jdbcTemplate;
+    private final SimpleJdbcInsert simpleJdbcInsert;
+
+    public ReservationTimeDao(JdbcTemplate jdbcTemplate, DataSource dataSource) {
+        this.jdbcTemplate = jdbcTemplate;
+        this.simpleJdbcInsert = new SimpleJdbcInsert(dataSource)
+                .withTableName("reservation_time")
+                .usingGeneratedKeyColumns("id");
+    }
+
+    public Long insert(LocalTime startAt) {
+        SqlParameterSource parameters = new MapSqlParameterSource()
+                .addValue("startAt", startAt);
+        return simpleJdbcInsert.executeAndReturnKey(parameters).longValue();
+    }
+
+    public Optional<ReservationTimeEntity> selectById(Long id) {
+        String sql = "select * from reservation_time where id = ?;";
+        return jdbcTemplate.query(sql, reservationTimeRowMapper, id)
+                .stream()
+                .findFirst();
+    }
+
+    public ReservationTimeEntity getByID(Long id) {
+        String sql = "select * from reservation_time where id = ?;";
+        return jdbcTemplate.queryForObject(sql, reservationTimeRowMapper, id);
+    }
+
+    public List<ReservationTimeEntity> selectAll() {
+        String sql = "select * from reservation_time;";
+        return jdbcTemplate.query(sql, reservationTimeRowMapper);
+    }
+
+    public int deleteById(Long id) {
+        String sql = "delete from reservation_time where id = ?;";
+        return jdbcTemplate.update(sql, id);
+    }
+
+    public List<Long> selectReservedTimeIds(Long themeId, LocalDate date) {
+        String sql = "select time_id " +
+                "from reservation " +
+                "where theme_id = ? and date = ?;";
+
+        return jdbcTemplate.queryForList(sql, Long.class, themeId, date.toString());
+    }
```

</details>

### 리뷰 본문 4258093045: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-09T18:19:45Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#pullrequestreview-4258093045)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 3213676285: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-09T18:28:27Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3213676285)
- 코드: `src/main/resources/schema.sql`, 현재 줄 18, 원래 줄 18
- 답변 대상: [코멘트 3208137920](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3208137920)
- 소속 리뷰 ID: 4258302652

> 예외 상황을 대비한 DB의 방어선 구축이 반드시 필요하다는 점에 공감합니다. 설계 방향 짚어주셔서 감사합니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,28 @@
+CREATE TABLE reservation_time
+(
+    id       BIGINT       NOT NULL AUTO_INCREMENT,
+    start_at VARCHAR(255) NOT NULL,
+    PRIMARY KEY (id)
+);
+
+CREATE TABLE theme
+(
+    id          BIGINT       NOT NULL AUTO_INCREMENT,
+    name        VARCHAR(255) NOT NULL,
+    description VARCHAR(255),
+    image_url    VARCHAR(512),
+    is_deleted BOOLEAN DEFAULT FALSE,
+    PRIMARY KEY (id)
+);
+
+CREATE TABLE reservation
```

</details>

### 리뷰 본문 4258302652: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-09T18:28:27Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#pullrequestreview-4258302652)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 3215760143: sihyung92

- 상대방 발언, 참여자
- 시각: 2026-05-11T00:13:40Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3215760143)
- 코드: `src/main/java/roomescape/controller/dto/AvailableReservationTimeResponse.java`, 현재 줄 None, 원래 줄 1
- 소속 리뷰 ID: 4260120719

> 패키지 내 객체수가 꽤 많아졌는데, 이 패키지 안에서 묶어주실 수 있다고 생각해요.
>
> dto/reservation/...
> dto/reservationtime/...
>
> 컨트롤러에서 쓰이는 단위로 묶어주면 보기 편할거 같네요.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,12 @@
+package roomescape.controller.dto;
```

</details>

### 인라인 코멘트 3215776835: sihyung92

- 상대방 발언, 참여자
- 시각: 2026-05-11T00:21:22Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3215776835)
- 코드: `src/main/java/roomescape/controller/dto/AvailableReservationTimesQuery.java`, 현재 줄 None, 원래 줄 7
- 소속 리뷰 ID: 4260120719

> command 쪽에서는 서비스 Dto로 치환하도록 되어있는데, query 쪽은 controller DTO를 그대로 받아 쓰네요.
>
> 이건 꼭 수정해주세요. 웹 요청과 응답 객체 만큼은 분리가 필요합니다.
>
> 또 command와 query 객체들 모두 controller DTO에만 도메인 불변식 예외처리가 있고 service dto에는 없는데요.
>
> 하나에만 있어야 한다면 serviceDto와 도메인 쪽입니다.
>
> 아래 순서로 발상해야 겠죠
>
> 1. 먼저 서비스, 도메인 단에서 불변식을 설정한다.
>     - 레벨1때 뷰 단에서의 검증보다 도메인 단에서의 검증을 했듯이요.
>     - 서비스 코드는 여러 컨트롤러 로부터 재활용되는 코드이기에 그렇습니다
> 2. 추가로 필요하면 view 단에서도 미리 적절한 요청만 받는다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,31 @@
+package roomescape.controller.dto;
+
+import java.time.LocalDate;
+import java.time.format.DateTimeParseException;
+import roomescape.global.exception.InvalidReservationTimeException;
+
+public record AvailableReservationTimesQuery(
```

</details>

### 인라인 코멘트 3215779020: sihyung92

- 상대방 발언, 참여자
- 시각: 2026-05-11T00:22:57Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3215779020)
- 코드: `src/main/java/roomescape/controller/dto/ThemeRequest.java`, 현재 줄 None, 원래 줄 40
- 소속 리뷰 ID: 4260120719

> PR에서 언급해주신 것과 다른 내용이 있네요
>
> > 현재는 description과 imageUrl을 필수값으로 강제하지 않았습니다. 테마의 이름은 테마를 식별하고 노출하는 핵심 정보라 필수값으로 두었지만, 설명과 이미지는 운영 상황에 따라 비어 있을 수 있다고 판단했습니다.
>
> DB Scheme에서도 not null인데, 심경 변화가 있으셨던 건가요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,41 @@
+package roomescape.controller.dto;
+
+import roomescape.global.exception.InvalidThemeException;
+import roomescape.service.dto.CreateThemeCommand;
+
+public record ThemeRequest(
+        String name,
+        String description,
+        String imageUrl
+) {
+
+    public CreateThemeCommand toCommand() {
+        validateName();
+        validateDescription();
+        validateImageUrl();
+
+        return new CreateThemeCommand(
+                name.trim(),
+                description.trim(),
+                imageUrl.trim()
+        );
+    }
+
+    private void validateName() {
+        if (name == null || name.isBlank()) {
+            throw new InvalidThemeException("테마 이름은 필수입니다.");
+        }
+    }
+
+    private void validateDescription() {
+        if (description == null || description.isBlank()) {
+            throw new InvalidThemeException("테마 설명은 필수입니다.");
+        }
+    }
+
+    private void validateImageUrl() {
+        if (imageUrl == null || imageUrl.isBlank()) {
+            throw new InvalidThemeException("테마 이미지 URL은 필수입니다.");
+        }
+    }
```

</details>

### 인라인 코멘트 3215781715: sihyung92

- 상대방 발언, 참여자
- 시각: 2026-05-11T00:24:52Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3215781715)
- 코드: `src/main/java/roomescape/controller/dto/AvailableReservationTimesQuery.java`, 현재 줄 None, 원래 줄 15
- 소속 리뷰 ID: 4260120719

> 커스텀 예외 정의해주셨는데 아직 IllegalArgumentException을 사용하는 곳이 남아있네요

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,31 @@
+package roomescape.controller.dto;
+
+import java.time.LocalDate;
+import java.time.format.DateTimeParseException;
+import roomescape.global.exception.InvalidReservationTimeException;
+
+public record AvailableReservationTimesQuery(
+        Long themeId,
+        LocalDate date,
+        Boolean available
+) {
+
+    public static AvailableReservationTimesQuery toQuery(Long themeId, String date, Boolean available) {
+        if (themeId == null) {
+            throw new IllegalArgumentException("테마 ID는 필수입니다.");
```

</details>

### 인라인 코멘트 3215784235: sihyung92

- 상대방 발언, 참여자
- 시각: 2026-05-11T00:26:42Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3215784235)
- 코드: `src/main/resources/schema.sql`, 현재 줄 None, 원래 줄 15
- 소속 리뷰 ID: 4260120719

> soft delete를 위한 칼럼을 설계하셨지만 프로덕션에선 soft delete를 고려하고 있지 않은데요. 칼럼 제거하시고 미래에 필요한 시점에 soft delete와 hard delete에 대해서 또 고민해보시죠.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,30 @@
+CREATE TABLE reservation_time
+(
+    id       BIGINT NOT NULL AUTO_INCREMENT,
+    start_at TIME   NOT NULL,
+    PRIMARY KEY (id),
+    UNIQUE (start_at)
+);
+
+CREATE TABLE theme
+(
+    id          BIGINT       NOT NULL AUTO_INCREMENT,
+    name        VARCHAR(255) NOT NULL,
+    description VARCHAR(255) NOT NULL,
+    image_url   VARCHAR(512) NOT NULL,
+    is_deleted  BOOLEAN DEFAULT FALSE,
```

</details>

### 인라인 코멘트 3215787844: sihyung92

- 상대방 발언, 참여자
- 시각: 2026-05-11T00:28:52Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3215787844)
- 코드: `src/main/java/roomescape/controller/ReservationTimeController.java`, 현재 줄 49, 원래 줄 42
- 소속 리뷰 ID: 4260120719

> Param에 따라 다른 응답객체가 응답되고 있는데요, 프론트 입장에서 대처하기 힘든 코드가 되어요.
>
> 서로 다른 api로 분기해주셔요

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,57 @@
+package roomescape.controller;
+
+import java.util.List;
+import lombok.RequiredArgsConstructor;
+import org.springframework.http.HttpStatus;
+import org.springframework.http.ResponseEntity;
+import org.springframework.web.bind.annotation.DeleteMapping;
+import org.springframework.web.bind.annotation.GetMapping;
+import org.springframework.web.bind.annotation.PathVariable;
+import org.springframework.web.bind.annotation.PostMapping;
+import org.springframework.web.bind.annotation.RequestBody;
+import org.springframework.web.bind.annotation.RequestMapping;
+import org.springframework.web.bind.annotation.RequestParam;
+import org.springframework.web.bind.annotation.RestController;
+import roomescape.controller.dto.ReservationTimeRequest;
+import roomescape.controller.dto.AvailableReservationTimesQuery;
+import roomescape.controller.dto.ReservationTimeResponse;
+import roomescape.controller.dto.AvailableReservationTimesResponse;
+import roomescape.service.ReservationTimeService;
+
+@RestController
+@RequestMapping("/times")
+@RequiredArgsConstructor
+public class ReservationTimeController {
+
+    private final ReservationTimeService reservationTimeService;
+
+    @GetMapping
+    public ResponseEntity<List<ReservationTimeResponse>> getReservationTimes() {
+        return ResponseEntity.ok(reservationTimeService.getReservationTimes());
+    }
+
+    @GetMapping(params = {"themeId", "date"})
+    public ResponseEntity<AvailableReservationTimesResponse> getAvailableReservationTimes(
+            @RequestParam Long themeId,
+            @RequestParam String date,
+            @RequestParam(required = false) Boolean available
+    ) {
+        return ResponseEntity.ok(reservationTimeService.getAvailableReservationTimes(
+                AvailableReservationTimesQuery.toQuery(themeId, date, available)
+        ));
+    }
```

</details>

### 인라인 코멘트 3215794046: sihyung92

- 상대방 발언, 참여자
- 시각: 2026-05-11T00:32:11Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3215794046)
- 코드: `src/main/java/roomescape/controller/ReservationController.java`, 현재 줄 None, 원래 줄 28
- 소속 리뷰 ID: 4260120719

> List형 요청과 응답객체는 항상 랩핑하는 습관을 가져주셔요
> ```suggestion
>     public ResponseEntity<ReservationResponses> getReservations(
> ```
>
> Json 입장에선 {}와 []의 차이가 있는데, 서로 호환이 되는 스펙이 아니어서 api 변경이 생기면 break change, 즉 운영 배포 시점에 잠시 장애가 나야만하는 스펙이 되어 api 버저닝을 해야하는 불편함이 생깁니다.
>
> 예를들어 응답에 count 필드를 추가해야하는 경우를 생각해보세요. 그때가서 랩핑하고 배포하면 프론트가 터지지만 미리 랩핑해놨으면 프론트 터질일 없이 (배포의존성 없이) 서버가 편하게 배포할 수 있습니다.
>
> 모든 List형 요청(GET 메서드 제외)과 응답에 대한 공통 리뷰입니다

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,50 @@
+package roomescape.controller;
+
+import java.util.List;
+import lombok.RequiredArgsConstructor;
+import org.springframework.http.HttpStatus;
+import org.springframework.http.ResponseEntity;
+import org.springframework.web.bind.annotation.DeleteMapping;
+import org.springframework.web.bind.annotation.GetMapping;
+import org.springframework.web.bind.annotation.PathVariable;
+import org.springframework.web.bind.annotation.PostMapping;
+import org.springframework.web.bind.annotation.RequestBody;
+import org.springframework.web.bind.annotation.RequestMapping;
+import org.springframework.web.bind.annotation.RequestParam;
+import org.springframework.web.bind.annotation.RestController;
+import roomescape.controller.dto.ReservationPagingQuery;
+import roomescape.controller.dto.ReservationRequest;
+import roomescape.controller.dto.ReservationResponse;
+import roomescape.service.ReservationService;
+
+@RestController
+@RequestMapping("/reservations")
+@RequiredArgsConstructor
+public class ReservationController {
+
+    private final ReservationService reservationService;
+
+    @GetMapping
+    public ResponseEntity<List<ReservationResponse>> getReservations(
```

</details>

### 인라인 코멘트 3215797519: sihyung92

- 상대방 발언, 참여자
- 시각: 2026-05-11T00:33:49Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3215797519)
- 코드: `src/main/java/roomescape/global/exception/GlobalExceptionHandler.java`, 현재 줄 None, 원래 줄 40
- 소속 리뷰 ID: 4260120719

> 의도치 않은 오류는 error 레벨로 로그 하셔야합니다. 지금은 모니터링 시스템이 없지만요

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,45 @@
+package roomescape.global.exception;
+
+import lombok.extern.slf4j.Slf4j;
+import org.springframework.dao.DataIntegrityViolationException;
+import org.springframework.http.ResponseEntity;
+import org.springframework.http.converter.HttpMessageNotReadableException;
+import org.springframework.web.bind.annotation.ExceptionHandler;
+import org.springframework.web.bind.annotation.RestControllerAdvice;
+import roomescape.global.exception.dto.ErrorResponse;
+
+@Slf4j
+@RestControllerAdvice
+public class GlobalExceptionHandler {
+
+    @ExceptionHandler(RoomescapeException.class)
+    public ResponseEntity<ErrorResponse> handleRoomescapeException(RoomescapeException e) {
+        log.info(e.getMessage());
+        ErrorCode errorCode = e.getErrorCode();
+        return ResponseEntity.status(errorCode.getStatus())
+                .body(new ErrorResponse(errorCode.getCode(), e.getMessage()));
+    }
+
+    @ExceptionHandler(DataIntegrityViolationException.class)
+    public ResponseEntity<ErrorResponse> handleDataIntegrityViolationException(DataIntegrityViolationException e) {
+        log.info(e.getMessage());
+        ErrorCode errorCode = ErrorCode.REFERENCED_DATA;
+        return ResponseEntity.status(errorCode.getStatus())
+                .body(new ErrorResponse(errorCode.getCode(), "현재 다른 데이터에서 참조 중이어서 삭제할 수 없습니다."));
+    }
+
+    @ExceptionHandler(HttpMessageNotReadableException.class)
+    public ResponseEntity<ErrorResponse> handleHttpMessageNotReadableException(HttpMessageNotReadableException e) {
+        log.info(e.getMessage());
+        return ResponseEntity.badRequest()
+                .body(new ErrorResponse("INVALID_REQUEST", "요청 본문 형식이 올바르지 않습니다."));
+    }
+
+    @ExceptionHandler(Exception.class)
+    public ResponseEntity<ErrorResponse> handleException(Exception e) {
+        log.info(e.getMessage());
```

</details>

### 리뷰 본문 4260120719: sihyung92

- 상대방 발언, 참여자
- 시각: 2026-05-11T00:34:41Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#pullrequestreview-4260120719)
- 리뷰 상태: `CHANGES_REQUESTED`

> 안녕하세요 고래, 리뷰어 웨지입니다.
>
> 변화를 많이 요구하는 리뷰였는데 잘 반영해주셨어요.
> 리뷰 남겼으니 확인해주시고 또 요청주세요.

### 인라인 코멘트 3216095349: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-11T02:46:54Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3216095349)
- 코드: `src/main/java/roomescape/controller/dto/AvailableReservationTimeResponse.java`, 현재 줄 None, 원래 줄 1
- 답변 대상: [코멘트 3215760143](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3215760143)
- 소속 리뷰 ID: 4260470637

> 네, 그렇게 하면 보기 편할 것 같습니다. 추가적으로 궁금한 부분이 있습니다.
> controller, service
>
> request, command
>
> query(쿼리 파라미터), condition
>
> response(단 건), responses(리스트)
>
> 위처럼 구성하게 된다면 이름이 가독성에서 복잡한지 의견이 궁금합니다.
>

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,12 @@
+package roomescape.controller.dto;
```

</details>

### 리뷰 본문 4260470637: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-11T02:46:54Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#pullrequestreview-4260470637)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 3216167444: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-11T03:13:23Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3216167444)
- 코드: `src/main/java/roomescape/controller/dto/AvailableReservationTimesQuery.java`, 현재 줄 None, 원래 줄 7
- 답변 대상: [코멘트 3215776835](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3215776835)
- 소속 리뷰 ID: 4260548895

> 이 부분에 대해서 사실 개인적으로 고민을 많이 했습니다.
>
> 우선 서비스에서 불변식 검증을 하는 건 매우 동의해요. 수정 해볼게요.
> dto 부분에서 사실 웹환경에 종속되는 것을 알면서 방치했습니다.
> Jackson에서 예외가 발생하면 특정 데이터의 예외를 판별하지 못할 것이라고 생각해서 예외 변환을 위해서 필요하다고 생각되는 부분만 dto를 추가했습니다.
> 또한 웹환경말고 다른 클라이언트가 생긴다면 필요성의 이유가 생기니깐 그 때 추가하자라는 생각을 했습니다.
> 이러한 부분들처럼 오버엔지니어링과 아닌 것의 경계에 대해서 혼란을 느끼고 있습니다.
> 지금은 또 일관성과 웹환경, 클라이언트에 대한 의존성이 서비스까지 퍼지는 것은 변경에 큰 문제라고 생각되어서 구현하는 것이 맞다고 판단해서 그렇게 수정할 생각입니다.
> 다만 어떤 이유로 지금에 필요없지만 추후 필요해질 것을 예상이 될 때, 미리 구현할지, 알면서도 말아야할지 고민하는데 비용을 많이 소모하는 것 같습니다.
> 웨지도 이런 적이 있나요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,31 @@
+package roomescape.controller.dto;
+
+import java.time.LocalDate;
+import java.time.format.DateTimeParseException;
+import roomescape.global.exception.InvalidReservationTimeException;
+
+public record AvailableReservationTimesQuery(
```

</details>

### 리뷰 본문 4260548895: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-11T03:13:23Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#pullrequestreview-4260548895)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 3216172990: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-11T03:16:09Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3216172990)
- 코드: `src/main/java/roomescape/controller/dto/ThemeRequest.java`, 현재 줄 None, 원래 줄 40
- 답변 대상: [코멘트 3215779020](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3215779020)
- 소속 리뷰 ID: 4260554025

> 서비스 운영하는데 설명과 이미지는 필수적이라고 생각되어서 수정했습니다.
> 테마는 이름, 설명, 썸네일 이미지 URL을 가진다. 라는 문구를 해석해보면서 필수적이라고 느껴져서 수정했습니다.
> 만약 요구사항에서 다르게 명시가 되어있다면 입력한 데이터만 요청을 보내고 응답은 동일하게 없다면 null로 표현하는 식으로 수정할 것 같습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,41 @@
+package roomescape.controller.dto;
+
+import roomescape.global.exception.InvalidThemeException;
+import roomescape.service.dto.CreateThemeCommand;
+
+public record ThemeRequest(
+        String name,
+        String description,
+        String imageUrl
+) {
+
+    public CreateThemeCommand toCommand() {
+        validateName();
+        validateDescription();
+        validateImageUrl();
+
+        return new CreateThemeCommand(
+                name.trim(),
+                description.trim(),
+                imageUrl.trim()
+        );
+    }
+
+    private void validateName() {
+        if (name == null || name.isBlank()) {
+            throw new InvalidThemeException("테마 이름은 필수입니다.");
+        }
+    }
+
+    private void validateDescription() {
+        if (description == null || description.isBlank()) {
+            throw new InvalidThemeException("테마 설명은 필수입니다.");
+        }
+    }
+
+    private void validateImageUrl() {
+        if (imageUrl == null || imageUrl.isBlank()) {
+            throw new InvalidThemeException("테마 이미지 URL은 필수입니다.");
+        }
+    }
```

</details>

### 리뷰 본문 4260554025: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-11T03:16:09Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#pullrequestreview-4260554025)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 3216174204: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-11T03:16:46Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3216174204)
- 코드: `src/main/java/roomescape/controller/dto/AvailableReservationTimesQuery.java`, 현재 줄 None, 원래 줄 15
- 답변 대상: [코멘트 3215781715](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3215781715)
- 소속 리뷰 ID: 4260555149

> 감사합니다. 수정하겠습니다. 이러한 부분에서 전역적으로 검색해서 찾아보는 연습을 이번 기회에 해보겠습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,31 @@
+package roomescape.controller.dto;
+
+import java.time.LocalDate;
+import java.time.format.DateTimeParseException;
+import roomescape.global.exception.InvalidReservationTimeException;
+
+public record AvailableReservationTimesQuery(
+        Long themeId,
+        LocalDate date,
+        Boolean available
+) {
+
+    public static AvailableReservationTimesQuery toQuery(Long themeId, String date, Boolean available) {
+        if (themeId == null) {
+            throw new IllegalArgumentException("테마 ID는 필수입니다.");
```

</details>

### 리뷰 본문 4260555149: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-11T03:16:46Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#pullrequestreview-4260555149)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 3216177436: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-11T03:18:24Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3216177436)
- 코드: `src/main/resources/schema.sql`, 현재 줄 None, 원래 줄 15
- 답변 대상: [코멘트 3215784235](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3215784235)
- 소속 리뷰 ID: 4260558890

> 우선 제거하고 추후에 도입한다면 theme에 status를 Enum을 이용해서 구현해보겠습니다.
> active, inactive, deleted으로 상태를 두는 방식을 사용해보려 합니다.
> 웨지의 의견대로 추가적으로 학습하고 앞으로 필요한 경우에 도입할 수 있도록 하겠습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,30 @@
+CREATE TABLE reservation_time
+(
+    id       BIGINT NOT NULL AUTO_INCREMENT,
+    start_at TIME   NOT NULL,
+    PRIMARY KEY (id),
+    UNIQUE (start_at)
+);
+
+CREATE TABLE theme
+(
+    id          BIGINT       NOT NULL AUTO_INCREMENT,
+    name        VARCHAR(255) NOT NULL,
+    description VARCHAR(255) NOT NULL,
+    image_url   VARCHAR(512) NOT NULL,
+    is_deleted  BOOLEAN DEFAULT FALSE,
```

</details>

### 리뷰 본문 4260558890: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-11T03:18:25Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#pullrequestreview-4260558890)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 3216183480: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-11T03:21:22Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3216183480)
- 코드: `src/main/java/roomescape/controller/ReservationTimeController.java`, 현재 줄 49, 원래 줄 42
- 답변 대상: [코멘트 3215787844](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3215787844)
- 소속 리뷰 ID: 4260564495

> 이번 기회에 모호했던 기준이 덕분에 정리가 됐습니다.
> 예를 들면 테마 생성 요청에서 name, description, imageUrl 등 not null이 있다는 가정하에 선택적으로 입력했을 때마다 요청의 request body가 달라지는 것을 하나의 엔드포인트에서 처리하는데는 문제가 없는 것을 알게 됐습니다.
> 또한 하나의 api에서 응답이 달라진다면 그것은 프론트에서 대처하려면 체크가 필요해져서 어려워질 것으로 판단되어서 응답이 다른 경우 api를 분리하겠다는 기준을 추가할 수 있게 됐네요! 감사합니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,57 @@
+package roomescape.controller;
+
+import java.util.List;
+import lombok.RequiredArgsConstructor;
+import org.springframework.http.HttpStatus;
+import org.springframework.http.ResponseEntity;
+import org.springframework.web.bind.annotation.DeleteMapping;
+import org.springframework.web.bind.annotation.GetMapping;
+import org.springframework.web.bind.annotation.PathVariable;
+import org.springframework.web.bind.annotation.PostMapping;
+import org.springframework.web.bind.annotation.RequestBody;
+import org.springframework.web.bind.annotation.RequestMapping;
+import org.springframework.web.bind.annotation.RequestParam;
+import org.springframework.web.bind.annotation.RestController;
+import roomescape.controller.dto.ReservationTimeRequest;
+import roomescape.controller.dto.AvailableReservationTimesQuery;
+import roomescape.controller.dto.ReservationTimeResponse;
+import roomescape.controller.dto.AvailableReservationTimesResponse;
+import roomescape.service.ReservationTimeService;
+
+@RestController
+@RequestMapping("/times")
+@RequiredArgsConstructor
+public class ReservationTimeController {
+
+    private final ReservationTimeService reservationTimeService;
+
+    @GetMapping
+    public ResponseEntity<List<ReservationTimeResponse>> getReservationTimes() {
+        return ResponseEntity.ok(reservationTimeService.getReservationTimes());
+    }
+
+    @GetMapping(params = {"themeId", "date"})
+    public ResponseEntity<AvailableReservationTimesResponse> getAvailableReservationTimes(
+            @RequestParam Long themeId,
+            @RequestParam String date,
+            @RequestParam(required = false) Boolean available
+    ) {
+        return ResponseEntity.ok(reservationTimeService.getAvailableReservationTimes(
+                AvailableReservationTimesQuery.toQuery(themeId, date, available)
+        ));
+    }
```

</details>

### 리뷰 본문 4260564495: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-11T03:21:22Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#pullrequestreview-4260564495)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 3216185276: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-11T03:22:16Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3216185276)
- 코드: `src/main/java/roomescape/controller/ReservationController.java`, 현재 줄 None, 원래 줄 28
- 답변 대상: [코멘트 3215794046](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3215794046)
- 소속 리뷰 ID: 4260566190

> 모든 List형 요청에 대해서는 responses dto를 사용하도록 하겠습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,50 @@
+package roomescape.controller;
+
+import java.util.List;
+import lombok.RequiredArgsConstructor;
+import org.springframework.http.HttpStatus;
+import org.springframework.http.ResponseEntity;
+import org.springframework.web.bind.annotation.DeleteMapping;
+import org.springframework.web.bind.annotation.GetMapping;
+import org.springframework.web.bind.annotation.PathVariable;
+import org.springframework.web.bind.annotation.PostMapping;
+import org.springframework.web.bind.annotation.RequestBody;
+import org.springframework.web.bind.annotation.RequestMapping;
+import org.springframework.web.bind.annotation.RequestParam;
+import org.springframework.web.bind.annotation.RestController;
+import roomescape.controller.dto.ReservationPagingQuery;
+import roomescape.controller.dto.ReservationRequest;
+import roomescape.controller.dto.ReservationResponse;
+import roomescape.service.ReservationService;
+
+@RestController
+@RequestMapping("/reservations")
+@RequiredArgsConstructor
+public class ReservationController {
+
+    private final ReservationService reservationService;
+
+    @GetMapping
+    public ResponseEntity<List<ReservationResponse>> getReservations(
```

</details>

### 리뷰 본문 4260566190: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-11T03:22:16Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#pullrequestreview-4260566190)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 3216194974: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-11T03:26:33Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3216194974)
- 코드: `src/main/java/roomescape/global/exception/GlobalExceptionHandler.java`, 현재 줄 None, 원래 줄 40
- 답변 대상: [코멘트 3215797519](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3215797519)
- 소속 리뷰 ID: 4260575638

> TRACE < DEBUG < INFO < WARN < ERROR
> info와 error 로그의 차이를 확인해봤는데, error는 예외 객체까지 같이 넘겨서 stack trace를 남기는 것을 알게 됐습니다.
> 의도치 않은 오류에는 error 레벨로 로그하도록 하겠습니다.
> 추가적으로 레벨별 차이에 대해서 학습해보겠습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,45 @@
+package roomescape.global.exception;
+
+import lombok.extern.slf4j.Slf4j;
+import org.springframework.dao.DataIntegrityViolationException;
+import org.springframework.http.ResponseEntity;
+import org.springframework.http.converter.HttpMessageNotReadableException;
+import org.springframework.web.bind.annotation.ExceptionHandler;
+import org.springframework.web.bind.annotation.RestControllerAdvice;
+import roomescape.global.exception.dto.ErrorResponse;
+
+@Slf4j
+@RestControllerAdvice
+public class GlobalExceptionHandler {
+
+    @ExceptionHandler(RoomescapeException.class)
+    public ResponseEntity<ErrorResponse> handleRoomescapeException(RoomescapeException e) {
+        log.info(e.getMessage());
+        ErrorCode errorCode = e.getErrorCode();
+        return ResponseEntity.status(errorCode.getStatus())
+                .body(new ErrorResponse(errorCode.getCode(), e.getMessage()));
+    }
+
+    @ExceptionHandler(DataIntegrityViolationException.class)
+    public ResponseEntity<ErrorResponse> handleDataIntegrityViolationException(DataIntegrityViolationException e) {
+        log.info(e.getMessage());
+        ErrorCode errorCode = ErrorCode.REFERENCED_DATA;
+        return ResponseEntity.status(errorCode.getStatus())
+                .body(new ErrorResponse(errorCode.getCode(), "현재 다른 데이터에서 참조 중이어서 삭제할 수 없습니다."));
+    }
+
+    @ExceptionHandler(HttpMessageNotReadableException.class)
+    public ResponseEntity<ErrorResponse> handleHttpMessageNotReadableException(HttpMessageNotReadableException e) {
+        log.info(e.getMessage());
+        return ResponseEntity.badRequest()
+                .body(new ErrorResponse("INVALID_REQUEST", "요청 본문 형식이 올바르지 않습니다."));
+    }
+
+    @ExceptionHandler(Exception.class)
+    public ResponseEntity<ErrorResponse> handleException(Exception e) {
+        log.info(e.getMessage());
```

</details>

### 리뷰 본문 4260575638: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-11T03:26:33Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#pullrequestreview-4260575638)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 3226687415: sihyung92

- 상대방 발언, 참여자
- 시각: 2026-05-12T13:18:46Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3226687415)
- 코드: `src/main/java/roomescape/global/exception/ErrorCode.java`, 현재 줄 5, 원래 줄 5
- 소속 리뷰 ID: 4272606475

> 요 열거형은 제거 추천드려요.
>
> 이 맵핑 클래스는 에러가 새로 정의될 때마다 수정해야되는데, 반드시 컨플릭트가 나는 코드가 됩니다. 객체지향이라는게 코드를 분산해서 컨플릭트를 줄이기 위한 패턴이라고 봐도 좋아요. (하나의 이유로 코드가 수정되게 한다)
>
> 어떤 서비스들은 예외상황마다 에러코드를 따로 정의해 가져가는 경우가 있는데 (10000은 예약 불가, 10001은 테마 없음...) 이런 것의 현황판 enum이면 몰라도 단순히 400, 404, 401 등만 맵핑하기엔 무의미한거 같네요.
>
> 차라리 각 코드에 따른 부모 Exception을 정의하고, 각 클래스가 extends 하는 건 어떨까요.
>

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,29 @@
+package roomescape.global.exception;
+
+import org.springframework.http.HttpStatus;
+
+public enum ErrorCode {
```

</details>

### 인라인 코멘트 3226780192: sihyung92

- 상대방 발언, 참여자
- 시각: 2026-05-12T13:31:46Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3226780192)
- 코드: `src/main/java/roomescape/controller/dto/AvailableReservationTimesQuery.java`, 현재 줄 None, 원래 줄 7
- 답변 대상: [코멘트 3215776835](https://github.com/woowacourse/spring-roomescape-member/pull/418#discussion_r3215776835)
- 소속 리뷰 ID: 4272606475

> 예 프로그래밍 언어를 써서 하는 개발은 '언어'를 통해 결과물을 짜 올린다는 점에서 어쩌면 문학이에요. 그런데 나 혼자 쓰는게 아니라 여러 작가가 돌아가면서 고쳐야 하는, 작가 입장에서는 최악의 작문입니다.
>
> 그렇기에 이 작품을 남들이 볼 수 있는 상태로는 유지하기 위한 다양한 방법론이 동원되는거고요
>
> 하지만 문학에 정답이 있다는 얘기를 들은 적 있나요? 문장, 단어, 부호 하나도 언제 어떻게 쓰이느냐에 따라 가치가 달라질 뿐 따로 정답은 없습니다.
> 코딩도 비슷하게 정답이 없고 (문학보다는 CS라는 훨씬 Strict한 규칙이 적용되지만요) 온갖 이론이 난무하니 스스로의 주관을 세우기가 어렵고 혼란한 건 당연한데요.
>
> 정답이 없다는 걸 기억하시면서 스스로 경험과 기준을 하나씩 세워나가보세요.
>
> 답이 있는 문제라고 생각하면 내가 오답을 낼 수 있으니 마음이 어려운건데요.
> 답은 없지만 세상엔 다양한 문법을 알아갈수록 내가 만들어 낼 수 있는 문장이 가치있어진다고 생각하면 훨씬 재밌어질 거에요.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,31 @@
+package roomescape.controller.dto;
+
+import java.time.LocalDate;
+import java.time.format.DateTimeParseException;
+import roomescape.global.exception.InvalidReservationTimeException;
+
+public record AvailableReservationTimesQuery(
```

</details>

### 리뷰 본문 4272606475: sihyung92

- 상대방 발언, 참여자
- 시각: 2026-05-12T13:35:27Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-member/pull/418#pullrequestreview-4272606475)
- 리뷰 상태: `APPROVED`

> 안녕하세요 고래, 리뷰어 웨지입니다.
>
> 리뷰 반영 잘 해주셔서 이만 머지할게요. 작은 커멘트 2개 남겼으니 확인해보셔요.
