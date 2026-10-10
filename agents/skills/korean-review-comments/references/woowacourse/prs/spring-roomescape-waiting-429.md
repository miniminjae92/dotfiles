# woowacourse/spring-roomescape-waiting #429

[🚀 사이클2 - 미션 (예약 대기)] 고래(강민재) 미션 제출합니다.

- [GitHub PR](https://github.com/woowacourse/spring-roomescape-waiting/pull/429)
- PR 작성자: `miniminjae92`
- 머지 시각: 2026-06-03T16:07:48Z
- [API 원본](../raw/spring-roomescape-waiting-429.json)
- 리뷰와 댓글 16건(본문 있는 발언 13건, 본인 기록 5건)

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
> 초코칩 안녕하세요.
>
> 이번 미션에서는 예약 대기를 자동으로 예약으로 전환하는 흐름을 구현하면서, 어떤 작업을 하나의 트랜잭션으로 묶을지에 집중했습니다.
> 또한 각 계층이 무엇을 보장하면 좋을지 생각해보는 시간을 가져봤습니다.
>
> 이번 사이클2도 잘 부탁드립니다 🙂
>
> ## 미션 중 기록
>
> - 규칙을 적용해서 변경한 코드: '컨트롤러 계층의 테스트는 클라이언트의 요청/응답을 검증한다'의 규칙을 참고하여 수정했습니다.
> - 테스트 작성이 어려웠던 코드: 테스트 더블 기법에 대해서 낯설어서 AI를 활용해 코드를 보고 학습을 하는 방식을 시도했습니다.
> - 막힌 순간:
> - 대기 순번을 별도의 DB 컬럼으로 다룰지 조회 시 계산할지 생각하는 부분에서 막혔습니다.
> - 예약 변경/취소를 했을 시 승격에 해당하는 예약 대기가 취소 요청이 있을 경우, 예약 변경/취소가 성공하는 것이 사용자 경험에서 좋을 것으로 판단되는데 해당 부분을 어떻게 구현할지 고민을 하는데 막혔습니다.
> - 트랜잭션 경계에 따라서 커넥션 유지가 달라지고 여러 락을 가질 수 있는 것에 대해서 몰라서 머릿속으로 잘 그려지지않아서 막혔습니다.
> - 비용과 데이터의 정합성을 저울질이 중요한 것인가에 대해서 고민을 하면서 막힘을 경험했습니다. 예를 들어서 조회수같은 것과 달리 예약 대기 순번은 정합성이 상당히 중요하다고 느껴지는데 이런식으로 비즈니스에 따라서 함께 묶을건지 말건지 연관이 있는 것인가?에 대한 고민이 이어지고 있습니다.
> - 전반적으로 함께 묶는다면 근거가 무엇인가에 대한 질문이 어려웠습니다. 솔직히 지금은 생각을 할 때마다 기준이 바뀌고 있고 혼란스럽긴한데, 지금은 서비스 로직에서 'transactional'에 대해서 묶는 것을 생각했을 땐 '롤백'을 우선적으로 관점으로 잡아서 진행했습니다.

## 대화와 리뷰 기록

### 인라인 코멘트 3342644853: Chocochip101

- 상대방 발언, 참여자
- 시각: 2026-06-02T16:03:53Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/429#discussion_r3342644853)
- 코드: `src/main/java/roomescape/domain/waitingreservation/WaitingReservationService.java`, 현재 줄 None, 원래 줄 50
- 소속 리뷰 ID: 4411469492

> Service → Repository 직접 의존으로 변경하면서 이 getReservationDate, getReservationTime, getTheme 메서드가  중복되네요. 중복을 줄여볼 수 있을까요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -45,6 +47,21 @@ public WaitingReservationCreationResponse createWaitingReservation(WaitingReserv
         return WaitingReservationCreationResponse.from(savedWaitingReservation);
     }

+    private ReservationDate getReservationDate(Long id) {
```

</details>

### 인라인 코멘트 3342684148: Chocochip101

- 상대방 발언, 참여자
- 시각: 2026-06-02T16:10:18Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/429#discussion_r3342684148)
- 코드: `src/main/java/roomescape/domain/reservation/ReservationSlot.java`, 현재 줄 None, 원래 줄 37
- 소속 리뷰 ID: 4411469492

> 기존 validateNotPast는 날짜+시간 기준(과거 시간이면 막음)이었는데,   isOnOrBeforeToday는 날짜만 비교해서 오늘의 모든 예약이 막히네요. 의도된 정책인건가요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -32,7 +34,7 @@ && timeId().equals(other.timeId())
                 && themeId().equals(other.themeId());
     }

-    public ReservationSchedule schedule() {
-        return new ReservationSchedule(date, time);
+    public boolean isOnOrBeforeToday(Clock clock) {
```

</details>

### 인라인 코멘트 3342735515: Chocochip101

- 상대방 발언, 참여자
- 시각: 2026-06-02T16:18:58Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/429#discussion_r3342735515)
- 코드: `src/test/java/roomescape/domain/reservation/AdminReservationControllerTest.java`, 현재 줄 26, 원래 줄 26
- 소속 리뷰 ID: 4411469492

> `@WebMvcTest`는 어떻게 작동할까요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -1,128 +1,87 @@
 package roomescape.domain.reservation;

-import static org.hamcrest.Matchers.is;
+import static org.mockito.ArgumentMatchers.any;
+import static org.mockito.Mockito.doThrow;
+import static org.mockito.Mockito.verify;
+import static org.mockito.Mockito.when;
+import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
+import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
+import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
+import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

-import io.restassured.RestAssured;
-import java.sql.PreparedStatement;
-import java.sql.Statement;
+import jakarta.servlet.http.HttpServletRequest;
 import java.time.LocalDate;
-import java.util.Objects;
-import org.junit.jupiter.api.BeforeEach;
-import org.junit.jupiter.api.DisplayName;
+import java.time.LocalTime;
+import java.util.List;
 import org.junit.jupiter.api.Test;
 import org.springframework.beans.factory.annotation.Autowired;
-import org.springframework.boot.test.context.SpringBootTest;
-import org.springframework.boot.test.web.server.LocalServerPort;
-import org.springframework.jdbc.core.JdbcTemplate;
-import org.springframework.jdbc.support.GeneratedKeyHolder;
-import org.springframework.jdbc.support.KeyHolder;
-import org.springframework.test.annotation.DirtiesContext;
-import org.springframework.test.context.jdbc.Sql;
-
-@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
-@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_CLASS)
-@Sql("/truncate.sql")
+import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
+import org.springframework.test.context.bean.override.mockito.MockitoBean;
+import org.springframework.test.web.servlet.MockMvc;
+import roomescape.admin.AdminRequestValidator;
+import roomescape.domain.reservation.dto.ReservationResponse;
+import roomescape.support.exception.ReservationErrorCode;
+import roomescape.support.exception.RoomescapeException;
+
+@WebMvcTest(AdminReservationController.class)
```

</details>

### 인라인 코멘트 3342779073: Chocochip101

- 상대방 발언, 참여자
- 시각: 2026-06-02T16:26:09Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/429#discussion_r3342779073)
- 코드: `src/test/java/roomescape/domain/reservation/ReservationServiceIntegrationTest.java`, 현재 줄 211, 원래 줄 208
- 소속 리뷰 ID: 4411469492

> "이산이 비어있다"는 두 가지 경우를 구분하지 못하네요.
> - promote가 실행됐다가 롤백된 경우
> - promoteOldestWaiting 자체가 아예 실행 안 된 경우
>
> 지금 검증만으로는 `@Transactional` 롤백이 동작했는지가 아니라 단순히 최종 상태만 확인하는 셈입니다.
>
>
> verify(reservationRepository).save(...)로 promote의 INSERT가 실제로 호출됐음을 함께 검증해보는건 어떤가요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,273 @@
+package roomescape.domain.reservation;
+
+import static org.assertj.core.api.Assertions.assertThat;
+import static org.assertj.core.api.Assertions.assertThatThrownBy;
+import static org.mockito.Mockito.doThrow;
+
+import java.time.LocalDate;
+import java.time.LocalDateTime;
+import java.time.LocalTime;
+import org.junit.jupiter.api.BeforeEach;
+import org.junit.jupiter.api.Test;
+import org.springframework.beans.factory.annotation.Autowired;
+import org.springframework.boot.test.context.SpringBootTest;
+import org.springframework.jdbc.core.JdbcTemplate;
+import org.springframework.test.context.bean.override.mockito.MockitoSpyBean;
+import org.springframework.test.context.jdbc.Sql;
+import roomescape.domain.reservation.dto.ReservationUpdateRequest;
+import roomescape.domain.reservationdate.ReservationDate;
+import roomescape.domain.reservationtime.ReservationTime;
+import roomescape.domain.theme.Theme;
+import roomescape.domain.waitingreservation.WaitingReservation;
+import roomescape.domain.waitingreservation.WaitingReservationRepository;
+import roomescape.domain.waitingreservation.dto.WaitingReservationWithRank;
+
+@SpringBootTest
+@Sql("/truncate.sql")
+class ReservationServiceIntegrationTest {
+
+    @Autowired
+    private ReservationService reservationService;
+
+    @Autowired
+    private ReservationRepository reservationRepository;
+
+    @MockitoSpyBean
+    private WaitingReservationRepository waitingReservationRepository;
+
+    @Autowired
+    private JdbcTemplate jdbcTemplate;
+
+    private Slot cancelledSlot;
+
+    @BeforeEach
+    void setUp() {
+        cancelledSlot = insertSlot(
+            101L, LocalDate.now().plusDays(2),
+            201L, LocalTime.of(10, 0),
+            301L, "공포"
+        );
+    }
+
+    @Test
+    void 사용자가_본인의_예약을_취소하면_같은_슬롯의_1순위_대기가_예약으로_승격된다() {
+        Reservation cancelledReservation = reservationRepository.save(
+            Reservation.createWithoutId(
+                "테스터",
+                cancelledSlot.date(),
+                cancelledSlot.time(),
+                cancelledSlot.theme()
+            )
+        );
+        Slot otherSlot = insertSlot(
+            102L, LocalDate.now().plusDays(3),
+            202L, LocalTime.of(11, 0),
+            302L, "스릴러"
+        );
+        WaitingReservation otherSlotOldest = waitingReservationRepository.save(
+            waiting("다른슬롯", otherSlot, LocalDateTime.of(2026, 5, 5, 10, 0))
+        );
+        WaitingReservation firstWaiting = waitingReservationRepository.save(
+            waiting("이산", cancelledSlot, LocalDateTime.of(2026, 5, 6, 10, 0))
+        );
+        waitingReservationRepository.save(
+            waiting("고래", cancelledSlot, LocalDateTime.of(2026, 5, 7, 10, 0))
+        );
+
+        reservationService.cancelReservation(cancelledReservation.getId());
+
+        assertThat(reservationRepository.findById(cancelledReservation.getId())).isEmpty();
+        assertThat(reservationRepository.findByName("이산")).hasSize(1);
+        assertThat(reservationRepository.findByName("다른슬롯")).isEmpty();
+        assertThat(waitingReservationRepository.findById(firstWaiting.getId())).isEmpty();
+        assertThat(waitingReservationRepository.findById(otherSlotOldest.getId())).isPresent();
+    }
+
+    @Test
+    void 사용자가_본인의_예약을_취소하면_남은_예약_대기_순번이_재계산된다() {
+        Reservation cancelledReservation = reservationRepository.save(
+            Reservation.createWithoutId(
+                "테스터",
+                cancelledSlot.date(),
+                cancelledSlot.time(),
+                cancelledSlot.theme()
+            )
+        );
+        waitingReservationRepository.save(
+            waiting("이산", cancelledSlot, LocalDateTime.of(2026, 5, 6, 10, 0))
+        );
+        waitingReservationRepository.save(
+            waiting("고래", cancelledSlot, LocalDateTime.of(2026, 5, 7, 10, 0))
+        );
+
+        reservationService.cancelReservation(cancelledReservation.getId());
+
+        assertThat(waitingReservationRepository.findAllByNameWithRank("고래"))
+            .singleElement()
+            .extracting(WaitingReservationWithRank::rank)
+            .isEqualTo(1L);
+    }
+
+    @Test
+    void 사용자가_본인의_예약을_수정하면_기존_슬롯의_1순위_대기가_예약으로_승격된다() {
+        Reservation updatedReservation = reservationRepository.save(
+            Reservation.createWithoutId(
+                "테스터",
+                cancelledSlot.date(),
+                cancelledSlot.time(),
+                cancelledSlot.theme()
+            )
+        );
+        Slot newSlot = insertSlot(
+            102L, LocalDate.now().plusDays(3),
+            202L, LocalTime.of(11, 0),
+            302L, "스릴러"
+        );
+        WaitingReservation firstWaiting = waitingReservationRepository.save(
+            waiting("이산", cancelledSlot, LocalDateTime.of(2026, 5, 6, 10, 0))
+        );
+        waitingReservationRepository.save(
+            waiting("고래", cancelledSlot, LocalDateTime.of(2026, 5, 7, 10, 0))
+        );
+
+        reservationService.updateReservation(
+            updatedReservation.getId(),
+            new ReservationUpdateRequest(
+                newSlot.date().getId(),
+                newSlot.time().getId()
+            )
+        );
+
+        Reservation movedReservation = reservationRepository.findById(updatedReservation.getId()).orElseThrow();
+        Reservation promotedReservation = reservationRepository.findByName("이산").getFirst();
+        assertThat(movedReservation.getDate().getId()).isEqualTo(newSlot.date().getId());
+        assertThat(movedReservation.getTime().getId()).isEqualTo(newSlot.time().getId());
+        assertThat(promotedReservation.getDate().getId()).isEqualTo(cancelledSlot.date().getId());
+        assertThat(promotedReservation.getTime().getId()).isEqualTo(cancelledSlot.time().getId());
+        assertThat(waitingReservationRepository.findById(firstWaiting.getId())).isEmpty();
+    }
+
+    @Test
+    void 사용자가_본인의_예약을_수정하면_남은_예약_대기_순번이_재계산된다() {
+        Reservation updatedReservation = reservationRepository.save(
+            Reservation.createWithoutId(
+                "테스터",
+                cancelledSlot.date(),
+                cancelledSlot.time(),
+                cancelledSlot.theme()
+            )
+        );
+        Slot newSlot = insertSlot(
+            102L, LocalDate.now().plusDays(3),
+            202L, LocalTime.of(11, 0),
+            302L, "스릴러"
+        );
+        waitingReservationRepository.save(
+            waiting("이산", cancelledSlot, LocalDateTime.of(2026, 5, 6, 10, 0))
+        );
+        waitingReservationRepository.save(
+            waiting("고래", cancelledSlot, LocalDateTime.of(2026, 5, 7, 10, 0))
+        );
+
+        reservationService.updateReservation(
+            updatedReservation.getId(),
+            new ReservationUpdateRequest(
+                newSlot.date().getId(),
+                newSlot.time().getId()
+            )
+        );
+
+        assertThat(waitingReservationRepository.findAllByNameWithRank("고래"))
+            .singleElement()
+            .extracting(WaitingReservationWithRank::rank)
+            .isEqualTo(1L);
+    }
+
+    @Test
+    void 예약_취소_중_승격된_예약_대기_삭제가_실패하면_예약_취소와_승격을_롤백한다() {
+        Reservation cancelledReservation = reservationRepository.save(
+            Reservation.createWithoutId(
+                "테스터",
+                cancelledSlot.date(),
+                cancelledSlot.time(),
+                cancelledSlot.theme()
+            )
+        );
+        WaitingReservation firstWaiting = waitingReservationRepository.save(
+            waiting("이산", cancelledSlot, LocalDateTime.of(2026, 5, 6, 10, 0))
+        );
+        doThrow(new IllegalStateException("예약 대기 삭제 실패"))
+            .when(waitingReservationRepository)
+            .deleteById(firstWaiting.getId());
+
+        assertThatThrownBy(() -> reservationService.cancelReservation(cancelledReservation.getId()))
+            .isInstanceOf(IllegalStateException.class);
+
+        assertThat(reservationRepository.findById(cancelledReservation.getId())).isPresent();
+        assertThat(reservationRepository.findByName("이산")).isEmpty();
+        assertThat(waitingReservationRepository.findById(firstWaiting.getId())).isPresent();
```

</details>

### 인라인 코멘트 3344417305: Chocochip101

- 상대방 발언, 참여자
- 시각: 2026-06-02T21:05:37Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/429#discussion_r3344417305)
- 코드: `docs/README.md`, 현재 줄 3, 원래 줄 3
- 소속 리뷰 ID: 4411469492

> 잘 구현해주셔서 다음 요청 때 머지할 수 있을 것 같네요 👍🏻

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,223 @@
+# Domain
+
+## 예약 대기
```

</details>

### 리뷰 본문 4411469492: Chocochip101

- 상대방 발언, 참여자
- 시각: 2026-06-02T21:05:41Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/429#pullrequestreview-4411469492)
- 리뷰 상태: `CHANGES_REQUESTED`

> 안녕하세요, 고래 :)
> 사이클 2도 잘 구현해주셨네요.
> 커맨트 확인해보시고 재요청 주세요!

### 인라인 코멘트 3346845781: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-06-03T08:00:32Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/429#discussion_r3346845781)
- 코드: `src/main/java/roomescape/domain/reservation/ReservationSlot.java`, 현재 줄 None, 원래 줄 37
- 답변 대상: [코멘트 3342684148](https://github.com/woowacourse/spring-roomescape-waiting/pull/429#discussion_r3342684148)
- 소속 리뷰 ID: 4416600450

> 비즈니스적으로 정책을 머릿속으로만 모호하게 관리하다가 휴먼에러가 발생했네요.
> 정책으로 방탈출 시작 시간 10분 전부터 마감되도록 정책을 명확히 정리하고 시도해봤습니다.
>
> 그 과정에서 추가적으로 사용자 예약, 예약 대기 조회의 기준도 고민하게 됐습니다.
> 고민 결과 사용자가 본인의 예약 / 예약 대기를 조회할 때는 앞으로 이용할 항목을 보는 것이 자연스럽다고 판단해, 기본 조회에서는 예약 시작 시각이 지난 항목을 제외하도록 반영해봤습니다.
> 기존 메서드를 고치는 방향보다 새롭게 추가해서, 전체 내역이 필요한 경우 또한 고려해봤습니다.
>

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -32,7 +34,7 @@ && timeId().equals(other.timeId())
                 && themeId().equals(other.themeId());
     }

-    public ReservationSchedule schedule() {
-        return new ReservationSchedule(date, time);
+    public boolean isOnOrBeforeToday(Clock clock) {
```

</details>

### 인라인 코멘트 3347077382: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-06-03T08:42:28Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/429#discussion_r3347077382)
- 코드: `src/main/java/roomescape/domain/waitingreservation/WaitingReservationService.java`, 현재 줄 None, 원래 줄 50
- 답변 대상: [코멘트 3342644853](https://github.com/woowacourse/spring-roomescape-waiting/pull/429#discussion_r3342644853)
- 소속 리뷰 ID: 4416600450

> 이 중복은 단순 메서드 중복이라기보다, id를 기반으로 예약 슬롯 도메인 객체를 해석하고 조립하는 책임이 여러 서비스에 흩어진 문제라고 판단했습니다.
> 그래서 `ReservationSlotResolver`를 추가해 `dateId`, `timeId`, `themeId`를 받아 `ReservationSlot`을 반환하도록 분리했습니다.
>
> 이 과정에서 고민이 생겼습니다.
> 예약 생성과 달리 예약 변경의 경우에서 테마 객체는 기존 예약의 테마를 유지하므로 오버로딩을 이용해서 구현했었습니다.
> 하지만 가독성을 위해서 메서드명을 분리를 하는 것이 더 이해하기 좋겠다고 생각되어 변경해봤습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -45,6 +47,21 @@ public WaitingReservationCreationResponse createWaitingReservation(WaitingReserv
         return WaitingReservationCreationResponse.from(savedWaitingReservation);
     }

+    private ReservationDate getReservationDate(Long id) {
```

</details>

### 인라인 코멘트 3347360417: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-06-03T09:28:50Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/429#discussion_r3347360417)
- 코드: `src/test/java/roomescape/domain/reservation/ReservationServiceIntegrationTest.java`, 현재 줄 211, 원래 줄 208
- 답변 대상: [코멘트 3342779073](https://github.com/woowacourse/spring-roomescape-waiting/pull/429#discussion_r3342779073)
- 소속 리뷰 ID: 4416600450

> 이번 미션에서는 각 계층의 책임과 역할에 해당하는 부분을 어디에서 보장할지에 집중해서 테스트를 작성해보려 했습니다.
>
> 그 과정에서 `verify`에 대해서도 고민이 있었습니다. 객체지향적으로 코드를 작성할 때는 항상 what을 드러내고 how는 캡슐화해서 변경에 용이하게 만들려고 의식하고 있습니다. 그래서 테스트에서도 repository 메서드 호출 여부를 `verify`하는 방식은 how, 즉 세부 구현에 의존하게 만들 수 있다고 생각해 최대한 자제하려 했습니다. 대신 어떤 행위가 필요하다면 해당 계층의 테스트에서 결과로 보장하는 쪽이 더 낫다고 생각했습니다.
>
> 그래서 정상 승격 테스트에서는 1순위 예약 대기가 실제 예약으로 승격되는 결과를 검증했고, 롤백 테스트에서는 최종 DB 상태가 롤백되는지를 검증했습니다.
>
> 다만 초코칩의 피드백 덕분에 다른 관점으로 생각 또한  하게 됐습니다. 롤백 테스트만 단독으로 보면 promote가 실행됐다가 롤백된 경우와 promote 자체가 실행되지 않은 경우를 구분하지 못해 하나의 테스트에서 완전성?에서 부족함을 저도 느끼게 됐습니다 . 특히 이 테스트의 목적이 단순 결과 검증이 아니라 “승격 insert가 시도된 뒤 이후 작업 실패로 함께 롤백되었는지”를 확인하는 것이라면, 해당 전제 조건을 명확히 드러낼 필요가 있다고 판단했습니다.
>
> 그래서 이번 케이스에서는 `verify`를 일반적인 구현 세부 검증이 아니라 트랜잭션 롤백 테스트의 전제 조건을 보강하는 제한적인 행위 검증으로 보고 추가했습니다. 다만 여전히 정상 승격 테스트에서 승격 결과가 이미 보장되고 있다면 롤백 테스트에서 `verify`까지 필요한지에 대한 고민은 남아 있습니다.
>
> 이 답변을 작성하면서 뒤늦게 또 다른 의견이 생겼습니다.
> 저는 각 계층에서 필요한 테스트를 보장하려고 하다 보니 같은 사례에 대해서 중복으로 보이는 테스트가 많아졌는데 하지만 각 계층마다 보장하는 성격?이라고 할까요? 그러한 부분들에서 차이를 느꼈고 모두 필요하다고 느꼈습니다.
> 그래서 해당 롤백 테스트에서 초코칩이 집어주신 부분을 verify로 체크하는 것이 추가되어야 해당 테스트만으로도 완전해지고, 현재 테스트 목적에도 부합된다고 느껴집니다.
> DB에서 해당 부분을 보장했다고 중복으로 여기고 세부 구현에 의존된다고 착각한 것 같습니다.
> verify로 확인한 부분도 시나리오에서 핵심인 what으로 느껴지기도 하네요.
> 이 부분에 대해서 한번 초코칩의 의견도 들어보고 싶네요!
>

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,273 @@
+package roomescape.domain.reservation;
+
+import static org.assertj.core.api.Assertions.assertThat;
+import static org.assertj.core.api.Assertions.assertThatThrownBy;
+import static org.mockito.Mockito.doThrow;
+
+import java.time.LocalDate;
+import java.time.LocalDateTime;
+import java.time.LocalTime;
+import org.junit.jupiter.api.BeforeEach;
+import org.junit.jupiter.api.Test;
+import org.springframework.beans.factory.annotation.Autowired;
+import org.springframework.boot.test.context.SpringBootTest;
+import org.springframework.jdbc.core.JdbcTemplate;
+import org.springframework.test.context.bean.override.mockito.MockitoSpyBean;
+import org.springframework.test.context.jdbc.Sql;
+import roomescape.domain.reservation.dto.ReservationUpdateRequest;
+import roomescape.domain.reservationdate.ReservationDate;
+import roomescape.domain.reservationtime.ReservationTime;
+import roomescape.domain.theme.Theme;
+import roomescape.domain.waitingreservation.WaitingReservation;
+import roomescape.domain.waitingreservation.WaitingReservationRepository;
+import roomescape.domain.waitingreservation.dto.WaitingReservationWithRank;
+
+@SpringBootTest
+@Sql("/truncate.sql")
+class ReservationServiceIntegrationTest {
+
+    @Autowired
+    private ReservationService reservationService;
+
+    @Autowired
+    private ReservationRepository reservationRepository;
+
+    @MockitoSpyBean
+    private WaitingReservationRepository waitingReservationRepository;
+
+    @Autowired
+    private JdbcTemplate jdbcTemplate;
+
+    private Slot cancelledSlot;
+
+    @BeforeEach
+    void setUp() {
+        cancelledSlot = insertSlot(
+            101L, LocalDate.now().plusDays(2),
+            201L, LocalTime.of(10, 0),
+            301L, "공포"
+        );
+    }
+
+    @Test
+    void 사용자가_본인의_예약을_취소하면_같은_슬롯의_1순위_대기가_예약으로_승격된다() {
+        Reservation cancelledReservation = reservationRepository.save(
+            Reservation.createWithoutId(
+                "테스터",
+                cancelledSlot.date(),
+                cancelledSlot.time(),
+                cancelledSlot.theme()
+            )
+        );
+        Slot otherSlot = insertSlot(
+            102L, LocalDate.now().plusDays(3),
+            202L, LocalTime.of(11, 0),
+            302L, "스릴러"
+        );
+        WaitingReservation otherSlotOldest = waitingReservationRepository.save(
+            waiting("다른슬롯", otherSlot, LocalDateTime.of(2026, 5, 5, 10, 0))
+        );
+        WaitingReservation firstWaiting = waitingReservationRepository.save(
+            waiting("이산", cancelledSlot, LocalDateTime.of(2026, 5, 6, 10, 0))
+        );
+        waitingReservationRepository.save(
+            waiting("고래", cancelledSlot, LocalDateTime.of(2026, 5, 7, 10, 0))
+        );
+
+        reservationService.cancelReservation(cancelledReservation.getId());
+
+        assertThat(reservationRepository.findById(cancelledReservation.getId())).isEmpty();
+        assertThat(reservationRepository.findByName("이산")).hasSize(1);
+        assertThat(reservationRepository.findByName("다른슬롯")).isEmpty();
+        assertThat(waitingReservationRepository.findById(firstWaiting.getId())).isEmpty();
+        assertThat(waitingReservationRepository.findById(otherSlotOldest.getId())).isPresent();
+    }
+
+    @Test
+    void 사용자가_본인의_예약을_취소하면_남은_예약_대기_순번이_재계산된다() {
+        Reservation cancelledReservation = reservationRepository.save(
+            Reservation.createWithoutId(
+                "테스터",
+                cancelledSlot.date(),
+                cancelledSlot.time(),
+                cancelledSlot.theme()
+            )
+        );
+        waitingReservationRepository.save(
+            waiting("이산", cancelledSlot, LocalDateTime.of(2026, 5, 6, 10, 0))
+        );
+        waitingReservationRepository.save(
+            waiting("고래", cancelledSlot, LocalDateTime.of(2026, 5, 7, 10, 0))
+        );
+
+        reservationService.cancelReservation(cancelledReservation.getId());
+
+        assertThat(waitingReservationRepository.findAllByNameWithRank("고래"))
+            .singleElement()
+            .extracting(WaitingReservationWithRank::rank)
+            .isEqualTo(1L);
+    }
+
+    @Test
+    void 사용자가_본인의_예약을_수정하면_기존_슬롯의_1순위_대기가_예약으로_승격된다() {
+        Reservation updatedReservation = reservationRepository.save(
+            Reservation.createWithoutId(
+                "테스터",
+                cancelledSlot.date(),
+                cancelledSlot.time(),
+                cancelledSlot.theme()
+            )
+        );
+        Slot newSlot = insertSlot(
+            102L, LocalDate.now().plusDays(3),
+            202L, LocalTime.of(11, 0),
+            302L, "스릴러"
+        );
+        WaitingReservation firstWaiting = waitingReservationRepository.save(
+            waiting("이산", cancelledSlot, LocalDateTime.of(2026, 5, 6, 10, 0))
+        );
+        waitingReservationRepository.save(
+            waiting("고래", cancelledSlot, LocalDateTime.of(2026, 5, 7, 10, 0))
+        );
+
+        reservationService.updateReservation(
+            updatedReservation.getId(),
+            new ReservationUpdateRequest(
+                newSlot.date().getId(),
+                newSlot.time().getId()
+            )
+        );
+
+        Reservation movedReservation = reservationRepository.findById(updatedReservation.getId()).orElseThrow();
+        Reservation promotedReservation = reservationRepository.findByName("이산").getFirst();
+        assertThat(movedReservation.getDate().getId()).isEqualTo(newSlot.date().getId());
+        assertThat(movedReservation.getTime().getId()).isEqualTo(newSlot.time().getId());
+        assertThat(promotedReservation.getDate().getId()).isEqualTo(cancelledSlot.date().getId());
+        assertThat(promotedReservation.getTime().getId()).isEqualTo(cancelledSlot.time().getId());
+        assertThat(waitingReservationRepository.findById(firstWaiting.getId())).isEmpty();
+    }
+
+    @Test
+    void 사용자가_본인의_예약을_수정하면_남은_예약_대기_순번이_재계산된다() {
+        Reservation updatedReservation = reservationRepository.save(
+            Reservation.createWithoutId(
+                "테스터",
+                cancelledSlot.date(),
+                cancelledSlot.time(),
+                cancelledSlot.theme()
+            )
+        );
+        Slot newSlot = insertSlot(
+            102L, LocalDate.now().plusDays(3),
+            202L, LocalTime.of(11, 0),
+            302L, "스릴러"
+        );
+        waitingReservationRepository.save(
+            waiting("이산", cancelledSlot, LocalDateTime.of(2026, 5, 6, 10, 0))
+        );
+        waitingReservationRepository.save(
+            waiting("고래", cancelledSlot, LocalDateTime.of(2026, 5, 7, 10, 0))
+        );
+
+        reservationService.updateReservation(
+            updatedReservation.getId(),
+            new ReservationUpdateRequest(
+                newSlot.date().getId(),
+                newSlot.time().getId()
+            )
+        );
+
+        assertThat(waitingReservationRepository.findAllByNameWithRank("고래"))
+            .singleElement()
+            .extracting(WaitingReservationWithRank::rank)
+            .isEqualTo(1L);
+    }
+
+    @Test
+    void 예약_취소_중_승격된_예약_대기_삭제가_실패하면_예약_취소와_승격을_롤백한다() {
+        Reservation cancelledReservation = reservationRepository.save(
+            Reservation.createWithoutId(
+                "테스터",
+                cancelledSlot.date(),
+                cancelledSlot.time(),
+                cancelledSlot.theme()
+            )
+        );
+        WaitingReservation firstWaiting = waitingReservationRepository.save(
+            waiting("이산", cancelledSlot, LocalDateTime.of(2026, 5, 6, 10, 0))
+        );
+        doThrow(new IllegalStateException("예약 대기 삭제 실패"))
+            .when(waitingReservationRepository)
+            .deleteById(firstWaiting.getId());
+
+        assertThatThrownBy(() -> reservationService.cancelReservation(cancelledReservation.getId()))
+            .isInstanceOf(IllegalStateException.class);
+
+        assertThat(reservationRepository.findById(cancelledReservation.getId())).isPresent();
+        assertThat(reservationRepository.findByName("이산")).isEmpty();
+        assertThat(waitingReservationRepository.findById(firstWaiting.getId())).isPresent();
```

</details>

### 인라인 코멘트 3347637408: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-06-03T10:15:43Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/429#discussion_r3347637408)
- 코드: `src/test/java/roomescape/domain/reservation/AdminReservationControllerTest.java`, 현재 줄 26, 원래 줄 26
- 답변 대상: [코멘트 3342735515](https://github.com/woowacourse/spring-roomescape-waiting/pull/429#discussion_r3342735515)
- 소속 리뷰 ID: 4416600450

> 초코칩의 질문 덕분에 `@WebMvcTest` 어노테이션 정의와 문서를 직접 따라가 보면서 추가로 학습해봤습니다.
>
> 아직 어노테이션과 스프링 테스트 컨텍스트가 익숙하진 않지만, 큰 틀에서는 `@WebMvcTest`를 전체 애플리케이션 컨텍스트를 띄우는 테스트가 아니라, MVC 계층만 슬라이스로 띄워 컨트롤러가 HTTP 요청을 HTTP 응답으로 바꾸는 과정을 검증하는 테스트로 이해했습니다.
>
> 내부적으로는 `@OverrideAutoConfiguration(enabled = false)`로 전체 자동 설정을 막고, `WebMvcTypeExcludeFilter`를 통해 웹 계층과 관련 없는 `Service`, `Repository` 같은 빈을 제외하는 것으로 이해했습니다. 대신 `@AutoConfigureWebMvc`, `@AutoConfigureMockMvc` 등을 통해 MVC 테스트에 필요한 설정과 `MockMvc`를 구성한다고 이해했습니다.
>
> 그래서 `@WebMvcTest`에서는 실제 서버를 띄우지 않고 `MockMvc`가 만든 요청이 `DispatcherServlet`, `Filter`, `Interceptor`, `ArgumentResolver`, `Controller`, `ControllerAdvice`, `HttpMessageConverter` 등의 MVC 흐름을 타면서 응답으로 변환되는지를 확인할 수 있다고 이해했습니다.
>
> 이번 테스트에서 `ReservationService`를 mock으로 둔 이유도, 이 테스트의 목적이 서비스나 레포지토리 동작을 검증하는 것이 아니라 관리자 예약 컨트롤러의 URL 매핑, HTTP Method, 응답 상태 코드, JSON 응답, 예외 응답 변환, 서비스 호출 위임을 검증하는 것이기 때문이라고 정리했습니다.
>
> 질문을 왜 주셨을까도 생각해봤는데, 페어 코드에서 토큰 개념이 들어와 있고 관리자 인터셉터가 함께 동작하다 보니, 제가 `@WebMvcTest`로 정확히 어떤 범위까지 검증하고 있는지 이해하고 있는 지를 확인해보려는 의도였다고 생각했습니다. 덕분에 컨트롤러 테스트에서 무엇을 검증하고, 무엇은 별도 단위 테스트나 통합 테스트로 분리해야 하는지 생각해보는 계기가 되어서 도움이 많이 됐습니다.
>
> 혹시 초코칩은 다른 의도로 던진 질문인데, 제가 캐치 못 했을까요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -1,128 +1,87 @@
 package roomescape.domain.reservation;

-import static org.hamcrest.Matchers.is;
+import static org.mockito.ArgumentMatchers.any;
+import static org.mockito.Mockito.doThrow;
+import static org.mockito.Mockito.verify;
+import static org.mockito.Mockito.when;
+import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
+import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
+import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
+import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

-import io.restassured.RestAssured;
-import java.sql.PreparedStatement;
-import java.sql.Statement;
+import jakarta.servlet.http.HttpServletRequest;
 import java.time.LocalDate;
-import java.util.Objects;
-import org.junit.jupiter.api.BeforeEach;
-import org.junit.jupiter.api.DisplayName;
+import java.time.LocalTime;
+import java.util.List;
 import org.junit.jupiter.api.Test;
 import org.springframework.beans.factory.annotation.Autowired;
-import org.springframework.boot.test.context.SpringBootTest;
-import org.springframework.boot.test.web.server.LocalServerPort;
-import org.springframework.jdbc.core.JdbcTemplate;
-import org.springframework.jdbc.support.GeneratedKeyHolder;
-import org.springframework.jdbc.support.KeyHolder;
-import org.springframework.test.annotation.DirtiesContext;
-import org.springframework.test.context.jdbc.Sql;
-
-@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
-@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_CLASS)
-@Sql("/truncate.sql")
+import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
+import org.springframework.test.context.bean.override.mockito.MockitoBean;
+import org.springframework.test.web.servlet.MockMvc;
+import roomescape.admin.AdminRequestValidator;
+import roomescape.domain.reservation.dto.ReservationResponse;
+import roomescape.support.exception.ReservationErrorCode;
+import roomescape.support.exception.RoomescapeException;
+
+@WebMvcTest(AdminReservationController.class)
```

</details>

### 리뷰 본문 4416600450: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-06-03T10:15:50Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/429#pullrequestreview-4416600450)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 3350081200: Chocochip101

- 상대방 발언, 참여자
- 시각: 2026-06-03T16:06:46Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/429#discussion_r3350081200)
- 코드: `src/test/java/roomescape/domain/reservation/ReservationServiceIntegrationTest.java`, 현재 줄 211, 원래 줄 208
- 답변 대상: [코멘트 3342779073](https://github.com/woowacourse/spring-roomescape-waiting/pull/429#discussion_r3342779073)
- 소속 리뷰 ID: 4420429880

> 저는 이 경우엔 verify가 필요하다고 생각해요.
>
> 두 테스트가 검증하는 게 달라서인데요.
> - 정상 승격 테스트: "promote가 올바르게 동작하는가?"
> - 롤백 테스트: "promote 도중 예외가 발생했을 때 전체가 롤백되는가?"
>
> verify 없이 최종 DB 상태만 보면, "promote가 실행됐다가 롤백된 경우"와 "promote 자체가 아예 호출되지 않은 경우"를 구분할 수 없어요. 실수로 promote 로직이 사라져도 테스트가 통과해버리죠.
>
> 여기서 verify는 구현 세부사항을 검증하는 게 아니라, 이 테스트가 의도한 시나리오(promote 시도 → 실패 → 롤백)가 실제로 재현됐음을 보장하는 역할이에요. 그래서 정상 승격 테스트와 중복이 아니고, 롤백 테스트에서만 필요한 검증이라고 생각이 드네요.
>
> 고래가 스스로 결론까지 잘 정리해주셨네요!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,273 @@
+package roomescape.domain.reservation;
+
+import static org.assertj.core.api.Assertions.assertThat;
+import static org.assertj.core.api.Assertions.assertThatThrownBy;
+import static org.mockito.Mockito.doThrow;
+
+import java.time.LocalDate;
+import java.time.LocalDateTime;
+import java.time.LocalTime;
+import org.junit.jupiter.api.BeforeEach;
+import org.junit.jupiter.api.Test;
+import org.springframework.beans.factory.annotation.Autowired;
+import org.springframework.boot.test.context.SpringBootTest;
+import org.springframework.jdbc.core.JdbcTemplate;
+import org.springframework.test.context.bean.override.mockito.MockitoSpyBean;
+import org.springframework.test.context.jdbc.Sql;
+import roomescape.domain.reservation.dto.ReservationUpdateRequest;
+import roomescape.domain.reservationdate.ReservationDate;
+import roomescape.domain.reservationtime.ReservationTime;
+import roomescape.domain.theme.Theme;
+import roomescape.domain.waitingreservation.WaitingReservation;
+import roomescape.domain.waitingreservation.WaitingReservationRepository;
+import roomescape.domain.waitingreservation.dto.WaitingReservationWithRank;
+
+@SpringBootTest
+@Sql("/truncate.sql")
+class ReservationServiceIntegrationTest {
+
+    @Autowired
+    private ReservationService reservationService;
+
+    @Autowired
+    private ReservationRepository reservationRepository;
+
+    @MockitoSpyBean
+    private WaitingReservationRepository waitingReservationRepository;
+
+    @Autowired
+    private JdbcTemplate jdbcTemplate;
+
+    private Slot cancelledSlot;
+
+    @BeforeEach
+    void setUp() {
+        cancelledSlot = insertSlot(
+            101L, LocalDate.now().plusDays(2),
+            201L, LocalTime.of(10, 0),
+            301L, "공포"
+        );
+    }
+
+    @Test
+    void 사용자가_본인의_예약을_취소하면_같은_슬롯의_1순위_대기가_예약으로_승격된다() {
+        Reservation cancelledReservation = reservationRepository.save(
+            Reservation.createWithoutId(
+                "테스터",
+                cancelledSlot.date(),
+                cancelledSlot.time(),
+                cancelledSlot.theme()
+            )
+        );
+        Slot otherSlot = insertSlot(
+            102L, LocalDate.now().plusDays(3),
+            202L, LocalTime.of(11, 0),
+            302L, "스릴러"
+        );
+        WaitingReservation otherSlotOldest = waitingReservationRepository.save(
+            waiting("다른슬롯", otherSlot, LocalDateTime.of(2026, 5, 5, 10, 0))
+        );
+        WaitingReservation firstWaiting = waitingReservationRepository.save(
+            waiting("이산", cancelledSlot, LocalDateTime.of(2026, 5, 6, 10, 0))
+        );
+        waitingReservationRepository.save(
+            waiting("고래", cancelledSlot, LocalDateTime.of(2026, 5, 7, 10, 0))
+        );
+
+        reservationService.cancelReservation(cancelledReservation.getId());
+
+        assertThat(reservationRepository.findById(cancelledReservation.getId())).isEmpty();
+        assertThat(reservationRepository.findByName("이산")).hasSize(1);
+        assertThat(reservationRepository.findByName("다른슬롯")).isEmpty();
+        assertThat(waitingReservationRepository.findById(firstWaiting.getId())).isEmpty();
+        assertThat(waitingReservationRepository.findById(otherSlotOldest.getId())).isPresent();
+    }
+
+    @Test
+    void 사용자가_본인의_예약을_취소하면_남은_예약_대기_순번이_재계산된다() {
+        Reservation cancelledReservation = reservationRepository.save(
+            Reservation.createWithoutId(
+                "테스터",
+                cancelledSlot.date(),
+                cancelledSlot.time(),
+                cancelledSlot.theme()
+            )
+        );
+        waitingReservationRepository.save(
+            waiting("이산", cancelledSlot, LocalDateTime.of(2026, 5, 6, 10, 0))
+        );
+        waitingReservationRepository.save(
+            waiting("고래", cancelledSlot, LocalDateTime.of(2026, 5, 7, 10, 0))
+        );
+
+        reservationService.cancelReservation(cancelledReservation.getId());
+
+        assertThat(waitingReservationRepository.findAllByNameWithRank("고래"))
+            .singleElement()
+            .extracting(WaitingReservationWithRank::rank)
+            .isEqualTo(1L);
+    }
+
+    @Test
+    void 사용자가_본인의_예약을_수정하면_기존_슬롯의_1순위_대기가_예약으로_승격된다() {
+        Reservation updatedReservation = reservationRepository.save(
+            Reservation.createWithoutId(
+                "테스터",
+                cancelledSlot.date(),
+                cancelledSlot.time(),
+                cancelledSlot.theme()
+            )
+        );
+        Slot newSlot = insertSlot(
+            102L, LocalDate.now().plusDays(3),
+            202L, LocalTime.of(11, 0),
+            302L, "스릴러"
+        );
+        WaitingReservation firstWaiting = waitingReservationRepository.save(
+            waiting("이산", cancelledSlot, LocalDateTime.of(2026, 5, 6, 10, 0))
+        );
+        waitingReservationRepository.save(
+            waiting("고래", cancelledSlot, LocalDateTime.of(2026, 5, 7, 10, 0))
+        );
+
+        reservationService.updateReservation(
+            updatedReservation.getId(),
+            new ReservationUpdateRequest(
+                newSlot.date().getId(),
+                newSlot.time().getId()
+            )
+        );
+
+        Reservation movedReservation = reservationRepository.findById(updatedReservation.getId()).orElseThrow();
+        Reservation promotedReservation = reservationRepository.findByName("이산").getFirst();
+        assertThat(movedReservation.getDate().getId()).isEqualTo(newSlot.date().getId());
+        assertThat(movedReservation.getTime().getId()).isEqualTo(newSlot.time().getId());
+        assertThat(promotedReservation.getDate().getId()).isEqualTo(cancelledSlot.date().getId());
+        assertThat(promotedReservation.getTime().getId()).isEqualTo(cancelledSlot.time().getId());
+        assertThat(waitingReservationRepository.findById(firstWaiting.getId())).isEmpty();
+    }
+
+    @Test
+    void 사용자가_본인의_예약을_수정하면_남은_예약_대기_순번이_재계산된다() {
+        Reservation updatedReservation = reservationRepository.save(
+            Reservation.createWithoutId(
+                "테스터",
+                cancelledSlot.date(),
+                cancelledSlot.time(),
+                cancelledSlot.theme()
+            )
+        );
+        Slot newSlot = insertSlot(
+            102L, LocalDate.now().plusDays(3),
+            202L, LocalTime.of(11, 0),
+            302L, "스릴러"
+        );
+        waitingReservationRepository.save(
+            waiting("이산", cancelledSlot, LocalDateTime.of(2026, 5, 6, 10, 0))
+        );
+        waitingReservationRepository.save(
+            waiting("고래", cancelledSlot, LocalDateTime.of(2026, 5, 7, 10, 0))
+        );
+
+        reservationService.updateReservation(
+            updatedReservation.getId(),
+            new ReservationUpdateRequest(
+                newSlot.date().getId(),
+                newSlot.time().getId()
+            )
+        );
+
+        assertThat(waitingReservationRepository.findAllByNameWithRank("고래"))
+            .singleElement()
+            .extracting(WaitingReservationWithRank::rank)
+            .isEqualTo(1L);
+    }
+
+    @Test
+    void 예약_취소_중_승격된_예약_대기_삭제가_실패하면_예약_취소와_승격을_롤백한다() {
+        Reservation cancelledReservation = reservationRepository.save(
+            Reservation.createWithoutId(
+                "테스터",
+                cancelledSlot.date(),
+                cancelledSlot.time(),
+                cancelledSlot.theme()
+            )
+        );
+        WaitingReservation firstWaiting = waitingReservationRepository.save(
+            waiting("이산", cancelledSlot, LocalDateTime.of(2026, 5, 6, 10, 0))
+        );
+        doThrow(new IllegalStateException("예약 대기 삭제 실패"))
+            .when(waitingReservationRepository)
+            .deleteById(firstWaiting.getId());
+
+        assertThatThrownBy(() -> reservationService.cancelReservation(cancelledReservation.getId()))
+            .isInstanceOf(IllegalStateException.class);
+
+        assertThat(reservationRepository.findById(cancelledReservation.getId())).isPresent();
+        assertThat(reservationRepository.findByName("이산")).isEmpty();
+        assertThat(waitingReservationRepository.findById(firstWaiting.getId())).isPresent();
```

</details>

### 리뷰 본문 4420429880: Chocochip101

- 상대방 발언, 참여자
- 시각: 2026-06-03T16:06:46Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/429#pullrequestreview-4420429880)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 3350083323: Chocochip101

- 상대방 발언, 참여자
- 시각: 2026-06-03T16:07:05Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/429#discussion_r3350083323)
- 코드: `src/test/java/roomescape/domain/reservation/AdminReservationControllerTest.java`, 현재 줄 26, 원래 줄 26
- 답변 대상: [코멘트 3342735515](https://github.com/woowacourse/spring-roomescape-waiting/pull/429#discussion_r3342735515)
- 소속 리뷰 ID: 4420432473

> 학습을 의도로 던진 질문이었어요 :) `@WebMvcTest`가 어디까지 컨텍스트를 구성하는지, 그 범위를 이해하고 쓰고 있는지 확인하고 싶었습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -1,128 +1,87 @@
 package roomescape.domain.reservation;

-import static org.hamcrest.Matchers.is;
+import static org.mockito.ArgumentMatchers.any;
+import static org.mockito.Mockito.doThrow;
+import static org.mockito.Mockito.verify;
+import static org.mockito.Mockito.when;
+import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
+import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
+import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
+import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

-import io.restassured.RestAssured;
-import java.sql.PreparedStatement;
-import java.sql.Statement;
+import jakarta.servlet.http.HttpServletRequest;
 import java.time.LocalDate;
-import java.util.Objects;
-import org.junit.jupiter.api.BeforeEach;
-import org.junit.jupiter.api.DisplayName;
+import java.time.LocalTime;
+import java.util.List;
 import org.junit.jupiter.api.Test;
 import org.springframework.beans.factory.annotation.Autowired;
-import org.springframework.boot.test.context.SpringBootTest;
-import org.springframework.boot.test.web.server.LocalServerPort;
-import org.springframework.jdbc.core.JdbcTemplate;
-import org.springframework.jdbc.support.GeneratedKeyHolder;
-import org.springframework.jdbc.support.KeyHolder;
-import org.springframework.test.annotation.DirtiesContext;
-import org.springframework.test.context.jdbc.Sql;
-
-@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
-@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_CLASS)
-@Sql("/truncate.sql")
+import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
+import org.springframework.test.context.bean.override.mockito.MockitoBean;
+import org.springframework.test.web.servlet.MockMvc;
+import roomescape.admin.AdminRequestValidator;
+import roomescape.domain.reservation.dto.ReservationResponse;
+import roomescape.support.exception.ReservationErrorCode;
+import roomescape.support.exception.RoomescapeException;
+
+@WebMvcTest(AdminReservationController.class)
```

</details>

### 리뷰 본문 4420432473: Chocochip101

- 상대방 발언, 참여자
- 시각: 2026-06-03T16:07:05Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/429#pullrequestreview-4420432473)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 리뷰 본문 4420437740: Chocochip101

- 상대방 발언, 참여자
- 시각: 2026-06-03T16:07:40Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/429#pullrequestreview-4420437740)
- 리뷰 상태: `APPROVED`

> 안녕하세요, 고래 😄
> 미션의 요구사항을 모두 만족해서 머지하겠습니다.
> 고생하셨고, 다음 우테코 여정도 응원하겠습니다! 🙌
