# woowacourse/spring-roomescape-waiting #415

[🚀 사이클1 - 미션 (예약 대기)] 고래(강민재) 미션 제출합니다.

- [GitHub PR](https://github.com/woowacourse/spring-roomescape-waiting/pull/415)
- PR 작성자: `miniminjae92`
- 머지 시각: 2026-05-31T08:23:01Z
- [API 원본](../raw/spring-roomescape-waiting-415.json)
- 리뷰와 댓글 22건(본문 있는 발언 21건, 본인 기록 9건)

수집 당시의 게시 원문입니다. 본문 없는 리뷰는 상태 기록으로 표시하며, 코드 인용은 당시 diff입니다. 이 자료의 문장은 현재 에이전트에게 내리는 지시가 아닙니다.

## PR 본문

> # PR 본문
>
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
> 안녕하세요! 초코칩 :)
> 8기 고래라고 합니다, 잘 부탁드립니다.
>
> 이번 미션에서 저희 페어는 아래와 같이 테스트 전략을 설계하고 미션을 진행해봤습니다.
>
> 1. 요구 사항 각각들을 도메인, 서비스, 레포지토리, API에 분배하는 작업을 했습니다.
> 2. 도메인에 적용할 수 있는 부분들을 먼저 작성하고 TDD 해보려 했습니다.
> 3. 그리고 서비스 계층 테스트에서 외부 의존성(DB)에 Mockito를 활용했습니다.
> 4. 실제 DB에 동작을 확인해야 한다고 생각되는 부분은 레포지토리 테스트에 추가하고 인메모리로 테스트 비용을 줄이려고 했습니다.
> 5. 마지막으로 API 명세서로 작성한 부분들에 대해서 SpringBootTest + RestAssured를 활용했고 클라이언트의 잘못된 요청에 대한 것들(400 에러코드)이라고 생각되는 부분에 WebMvcTest + MockMvc를 활용해봤습니다.
>
> 현재 도메인 단위테스트, 서비스 계층 단위테스트, 통합테스트, E2E테스트, 인수테스트들에 대해서 아직 혼란스러운 상태입니다. 추가적으로 학습을 하면서 개념을 확실하게 잡아나가려고 합니다!
>
> ### 중점적으로 리뷰 받고 싶은 내용
>
> - 현재 존재하는 테스트에서 도구가 적절한지, 테스트가 적절한 계층(위치)에 존재하고 있는지가 궁금합니다.
> - 부족한 테스트가 무엇인지에 대해서 집중해서 리뷰를 받아보고 싶습니다.
> - 더미 테스트 데이터, 테스트 픽스처, 테스트 환경설정에서 부족한 부분들에 대해서 궁금합니다.
>
> ## 참고해야 하는 사항
> <img width="493" height="206" alt="image" src="https://github.com/user-attachments/assets/ab82537d-75c6-43d8-821b-c056c9c7d5ca" />
>
> 관리자 페이지로 들어가기 위해서는 localhost:8080 접속 후, 관리자 탭을 누른 후에
> 다음 토큰을 입력해주시면 됩니다!
>
> ```
> sanwhale0192
> ```

## 대화와 리뷰 기록

### 인라인 코멘트 3319515100: Chocochip101

- 상대방 발언, 참여자
- 시각: 2026-05-28T17:14:02Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/415#discussion_r3319515100)
- 코드: `src/main/java/roomescape/domain/reservation/ReservationService.java`, 현재 줄 None, 원래 줄 86
- 소속 리뷰 ID: 4383159021

> 예약 저장 후 deleteById가 실패하면  같은 슬롯에 예약이 2개 생기겠네요. 이를 어떻게 해결해볼 수 있을까요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -58,13 +62,29 @@ public void deleteReservation(Long id) {

     public List<ReservationResponse> getReservationsByName(String name) {
         return reservationRepository.findByName(name).stream()
-            .map(ReservationResponse::from)
-            .toList();
+                .map(ReservationResponse::from)
+                .toList();
     }

     public void cancelReservation(Long id) {
         Reservation reservation = findById(id);
         validateModifiable(reservation);
+
+        Optional<WaitingReservation> waitingReservationOpt = waitingReservationRepository.findOldestBySlot(
+                reservation.getDate().getId(),
+                reservation.getTime().getId(),
+                reservation.getTheme().getId()
+        );
+        if (waitingReservationOpt.isPresent()) {
+            WaitingReservation waitingReservation = waitingReservationOpt.get();
+            reservationRepository.save(Reservation.createWithoutId(
+                    waitingReservation.getName(),
+                    waitingReservation.getDate(),
+                    waitingReservation.getTime(),
+                    waitingReservation.getTheme()
+            ));
+            waitingReservationRepository.deleteById(waitingReservation.getId());
```

</details>

### 인라인 코멘트 3319537208: Chocochip101

- 상대방 발언, 참여자
- 시각: 2026-05-28T17:18:39Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/415#discussion_r3319537208)
- 코드: `src/main/java/roomescape/domain/waitingreservation/WaitingReservationService.java`, 현재 줄 80, 원래 줄 75
- 소속 리뷰 ID: 4383159021

> 존재하지 않는 ID로 삭제 요청해도 204를 반환하네요.
> 클라이언트가 잘못된 ID를 보내도 알 방법이 없으니 404를 던지는 게 어떤가요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,84 @@
+package roomescape.domain.waitingreservation;
+
+import java.time.Clock;
+import java.time.LocalDateTime;
+import java.util.List;
+import lombok.RequiredArgsConstructor;
+import lombok.extern.slf4j.Slf4j;
+import org.springframework.stereotype.Service;
+import roomescape.domain.reservation.ReservationRepository;
+import roomescape.domain.reservationdate.ReservationDate;
+import roomescape.domain.reservationdate.ReservationDateService;
+import roomescape.domain.reservationtime.ReservationTime;
+import roomescape.domain.reservationtime.ReservationTimeService;
+import roomescape.domain.theme.Theme;
+import roomescape.domain.theme.ThemeService;
+import roomescape.domain.waitingreservation.dto.WaitingReservationCreationRequest;
+import roomescape.domain.waitingreservation.dto.WaitingReservationCreationResponse;
+import roomescape.domain.waitingreservation.dto.WaitingReservationWithRankResponse;
+import roomescape.support.exception.RoomescapeException;
+import roomescape.support.exception.WaitingReservationErrorCode;
+
+@Slf4j
+@Service
+@RequiredArgsConstructor
+public class WaitingReservationService {
+
+    private final WaitingReservationRepository waitingReservationRepository;
+    private final ReservationRepository reservationRepository;
+    private final ReservationDateService reservationDateService;
+    private final ReservationTimeService reservationTimeService;
+    private final ThemeService themeService;
+    private final Clock clock;
+
+    public WaitingReservationCreationResponse createWaitingReservation(WaitingReservationCreationRequest request) {
+        validateDuplicationOfWaitingReservation(request);
+        ReservationDate date = reservationDateService.findById(request.dateId());
+        ReservationTime time = reservationTimeService.findById(request.timeId());
+        Theme theme = themeService.findById(request.themeId());
+        validateNotPast(date, time);
+        validateSlotIsReserved(request);
+
+        WaitingReservation waitingReservation = request.toEntity(date, time, theme, LocalDateTime.now(clock));
+        WaitingReservation savedWaitingReservation = waitingReservationRepository.save(waitingReservation);
+        return WaitingReservationCreationResponse.from(savedWaitingReservation);
+    }
+
+    private void validateDuplicationOfWaitingReservation(WaitingReservationCreationRequest request) {
+        if (waitingReservationRepository.existsByNameAndDateIdAndTimeIdAndThemeId(request.name(), request.dateId(), request.timeId(), request.themeId())) {
+            throw new RoomescapeException(WaitingReservationErrorCode.DUPLICATE_WAITING_RESERVATION);
+        }
+    }
+
+    private void validateSlotIsReserved(WaitingReservationCreationRequest request) {
+        boolean reserved = reservationRepository.existsByDateIdAndTimeIdAndThemeId(
+            request.dateId(),
+            request.timeId(),
+            request.themeId()
+        );
+        if (!reserved) {
+            throw new RoomescapeException(WaitingReservationErrorCode.AVAILABLE_SLOT_NOT_WAITABLE);
+        }
+    }
+
+    private void validateNotPast(ReservationDate date, ReservationTime time) {
+        LocalDateTime reservationDateTime = LocalDateTime.of(date.getPlayDay(), time.getStartAt());
+        if (reservationDateTime.isBefore(LocalDateTime.now(clock))) {
+            throw new RoomescapeException(WaitingReservationErrorCode.PAST_TIME_NOT_ALLOWED);
+        }
+    }
+
+    public void cancelWaitingReservation(Long id) {
+        int deletedCount = waitingReservationRepository.deleteById(id);
+        if (deletedCount == 0) {
+            log.warn("이미 삭제된 예약 대기 삭제 요청이 들어왔습니다. reservationId={}", id);
+        }
```

</details>

### 인라인 코멘트 3319573624: Chocochip101

- 상대방 발언, 참여자
- 시각: 2026-05-28T17:25:32Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/415#discussion_r3319573624)
- 코드: `src/main/java/roomescape/domain/waitingreservation/WaitingReservationService.java`, 현재 줄 None, 원래 줄 44
- 소속 리뷰 ID: 4383159021

> 존재하지 않는 dateId로 요청이 오면 중복 체크 쿼리가 먼저 실행되고(무의미한 DB hit), 이후 date 존재 확인에서 404가 납니다. `date/time/theme` 존재 확인 후 중복 체크 순서가 더 자연스러워보이네요.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,84 @@
+package roomescape.domain.waitingreservation;
+
+import java.time.Clock;
+import java.time.LocalDateTime;
+import java.util.List;
+import lombok.RequiredArgsConstructor;
+import lombok.extern.slf4j.Slf4j;
+import org.springframework.stereotype.Service;
+import roomescape.domain.reservation.ReservationRepository;
+import roomescape.domain.reservationdate.ReservationDate;
+import roomescape.domain.reservationdate.ReservationDateService;
+import roomescape.domain.reservationtime.ReservationTime;
+import roomescape.domain.reservationtime.ReservationTimeService;
+import roomescape.domain.theme.Theme;
+import roomescape.domain.theme.ThemeService;
+import roomescape.domain.waitingreservation.dto.WaitingReservationCreationRequest;
+import roomescape.domain.waitingreservation.dto.WaitingReservationCreationResponse;
+import roomescape.domain.waitingreservation.dto.WaitingReservationWithRankResponse;
+import roomescape.support.exception.RoomescapeException;
+import roomescape.support.exception.WaitingReservationErrorCode;
+
+@Slf4j
+@Service
+@RequiredArgsConstructor
+public class WaitingReservationService {
+
+    private final WaitingReservationRepository waitingReservationRepository;
+    private final ReservationRepository reservationRepository;
+    private final ReservationDateService reservationDateService;
+    private final ReservationTimeService reservationTimeService;
+    private final ThemeService themeService;
+    private final Clock clock;
+
+    public WaitingReservationCreationResponse createWaitingReservation(WaitingReservationCreationRequest request) {
+        validateDuplicationOfWaitingReservation(request);
+        ReservationDate date = reservationDateService.findById(request.dateId());
+        ReservationTime time = reservationTimeService.findById(request.timeId());
+        Theme theme = themeService.findById(request.themeId());
+        validateNotPast(date, time);
+        validateSlotIsReserved(request);
+
+        WaitingReservation waitingReservation = request.toEntity(date, time, theme, LocalDateTime.now(clock));
+        WaitingReservation savedWaitingReservation = waitingReservationRepository.save(waitingReservation);
+        return WaitingReservationCreationResponse.from(savedWaitingReservation);
```

</details>

### 인라인 코멘트 3319597649: Chocochip101

- 상대방 발언, 참여자
- 시각: 2026-05-28T17:29:48Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/415#discussion_r3319597649)
- 코드: `src/main/java/roomescape/domain/waitingreservation/JdbcWaitingReservationRepository.java`, 현재 줄 None, 원래 줄 36
- 소속 리뷰 ID: 4383159021

> 해당 코드가 쓰이나요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,191 @@
+package roomescape.domain.waitingreservation;
+
+import java.sql.PreparedStatement;
+import java.sql.Statement;
+import java.sql.Timestamp;
+import java.time.LocalDate;
+import java.time.LocalTime;
+import java.util.List;
+import java.util.Optional;
+import lombok.RequiredArgsConstructor;
+import org.springframework.jdbc.core.JdbcTemplate;
+import org.springframework.jdbc.core.RowMapper;
+import org.springframework.jdbc.support.GeneratedKeyHolder;
+import org.springframework.jdbc.support.KeyHolder;
+import org.springframework.stereotype.Repository;
+import roomescape.domain.reservationdate.ReservationDate;
+import roomescape.domain.reservationtime.ReservationTime;
+import roomescape.domain.theme.Theme;
+import roomescape.domain.waitingreservation.dto.WaitingReservationWithRank;
+
+@Repository
+@RequiredArgsConstructor
+public class JdbcWaitingReservationRepository implements WaitingReservationRepository {
+
+    private static final String INSERT_SQL = "insert into waiting_reservation(name, date_id, time_id, theme_id, created_at) values (?, ?, ?, ?, ?)";
+
+    private static final String EXIST_BY_NAME_DATE_TIME_THEME_SQL =
+            """
+                    select exists(
+                    select 1
+                    from waiting_reservation
+                    where name = ? and date_id = ? and time_id = ? and theme_id = ?
+                    );
+                    """;
+
+    private static final String FIND_OLDEST_SQL =
```

</details>

### 인라인 코멘트 3319672617: Chocochip101

- 상대방 발언, 참여자
- 시각: 2026-05-28T17:45:03Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/415#discussion_r3319672617)
- 코드: `src/main/java/roomescape/domain/reservation/ReservationService.java`, 현재 줄 None, 원래 줄 73
- 소속 리뷰 ID: 4383159021

> cancelReservation은 대기자 승격 로직이 있는데updateReservation은 없네요. 의도된 동작인가요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -58,13 +62,29 @@ public void deleteReservation(Long id) {

     public List<ReservationResponse> getReservationsByName(String name) {
         return reservationRepository.findByName(name).stream()
-            .map(ReservationResponse::from)
-            .toList();
+                .map(ReservationResponse::from)
+                .toList();
     }

     public void cancelReservation(Long id) {
         Reservation reservation = findById(id);
         validateModifiable(reservation);
+
+        Optional<WaitingReservation> waitingReservationOpt = waitingReservationRepository.findOldestBySlot(
```

</details>

### 인라인 코멘트 3319744161: Chocochip101

- 상대방 발언, 참여자
- 시각: 2026-05-28T17:58:38Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/415#discussion_r3319744161)
- 코드: `src/test/java/roomescape/domain/waitingreservation/JdbcWaitingReservationRepositoryTest.java`, 현재 줄 None, 원래 줄 23
- 소속 리뷰 ID: 4383159021

> `@JdbcTest` 내부에 `@Transactional`이 포함되어 있어서 `@Sql("/truncate.sql")`가 불필요해보이네요.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,188 @@
+package roomescape.domain.waitingreservation;
+
+import static org.assertj.core.api.Assertions.assertThat;
+import static org.assertj.core.api.Assertions.assertThatThrownBy;
+
+import java.time.LocalDate;
+import java.time.LocalDateTime;
+import java.time.LocalTime;
+import java.util.List;
+import org.junit.jupiter.api.BeforeEach;
+import org.junit.jupiter.api.Test;
+import org.springframework.beans.factory.annotation.Autowired;
+import org.springframework.boot.test.autoconfigure.jdbc.JdbcTest;
+import org.springframework.dao.DuplicateKeyException;
+import org.springframework.jdbc.core.JdbcTemplate;
+import org.springframework.test.context.jdbc.Sql;
+import roomescape.domain.reservationdate.ReservationDate;
+import roomescape.domain.reservationtime.ReservationTime;
+import roomescape.domain.theme.Theme;
+import roomescape.domain.waitingreservation.dto.WaitingReservationWithRank;
+
+@JdbcTest
+@Sql("/truncate.sql")
```

</details>

### 인라인 코멘트 3319809672: Chocochip101

- 상대방 발언, 참여자
- 시각: 2026-05-28T18:10:52Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/415#discussion_r3319809672)
- 코드: `src/test/java/roomescape/domain/waitingreservation/WaitingReservationControllerTest.java`, 현재 줄 16, 원래 줄 18
- 소속 리뷰 ID: 4383159021

> 셋 어노테이션은 각 어떤 역할을 하나요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,122 @@
+package roomescape.domain.waitingreservation;
+
+import static org.hamcrest.Matchers.is;
+
+import io.restassured.RestAssured;
+import io.restassured.http.ContentType;
+import java.util.HashMap;
+import java.util.Map;
+import org.junit.jupiter.api.BeforeEach;
+import org.junit.jupiter.api.Test;
+import org.springframework.boot.test.context.SpringBootTest;
+import org.springframework.boot.test.web.server.LocalServerPort;
+import org.springframework.test.annotation.DirtiesContext;
+import org.springframework.test.context.jdbc.Sql;
+
+@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
+@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_CLASS)
+@Sql({"/truncate.sql", "/waiting-reservation-test-data.sql"})
```

</details>

### 인라인 코멘트 3319819286: Chocochip101

- 상대방 발언, 참여자
- 시각: 2026-05-28T18:12:51Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/415#discussion_r3319819286)
- 코드: `src/test/java/roomescape/domain/waitingreservation/WaitingReservationControllerTest.java`, 현재 줄 None, 원래 줄 105
- 소속 리뷰 ID: 4383159021

> 픽스처의 첫 번째 id가 1이라는 가정에 의존하고 있네요. truncate로 초기화하면 AUTO_INCREMENT가 리셋되지만, DB 구현에 따라 다를 수 있어요. 어떻게 개선해보는게 좋을까요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,122 @@
+package roomescape.domain.waitingreservation;
+
+import static org.hamcrest.Matchers.is;
+
+import io.restassured.RestAssured;
+import io.restassured.http.ContentType;
+import java.util.HashMap;
+import java.util.Map;
+import org.junit.jupiter.api.BeforeEach;
+import org.junit.jupiter.api.Test;
+import org.springframework.boot.test.context.SpringBootTest;
+import org.springframework.boot.test.web.server.LocalServerPort;
+import org.springframework.test.annotation.DirtiesContext;
+import org.springframework.test.context.jdbc.Sql;
+
+@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
+@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_CLASS)
+@Sql({"/truncate.sql", "/waiting-reservation-test-data.sql"})
+class WaitingReservationControllerTest {
+
+    @LocalServerPort
+    private int port;
+
+    @BeforeEach
+    void setUp() {
+        RestAssured.port = this.port;
+    }
+
+    @Test
+    void 사용자는_예약_대기를_신청한다() {
+        Map<String, Object> params = new HashMap<>();
+        params.put("name", "고래");
+        params.put("dateId", 1);
+        params.put("timeId", 1);
+        params.put("themeId", 4);
+
+        RestAssured.given().log().all()
+                .contentType(ContentType.JSON)
+                .body(params)
+                .when()
+                .post("/waiting-reservations")
+                .then().log().all()
+                .statusCode(201)
+                .body("name", is("고래"))
+                .body("theme.name", is("코미디테마"));
+    }
+
+    @Test
+    void 중복_예약_대기_신청을_하면_409를_반환한다() {
+        Map<String, Object> params = new HashMap<>();
+        params.put("name", "기존대기자");
+        params.put("dateId", 1);
+        params.put("timeId", 1);
+        params.put("themeId", 1);
+
+        RestAssured.given().log().all()
+                .contentType(ContentType.JSON)
+                .body(params)
+                .when()
+                .post("/waiting-reservations")
+                .then().log().all()
+                .statusCode(409);
+    }
+
+    @Test
+    void 예약_가능한_시간에_대기_신청하면_409을_반환한다() {
+        Map<String, Object> params = new HashMap<>();
+        params.put("name", "고래");
+        params.put("dateId", 1);
+        params.put("timeId", 2);
+        params.put("themeId", 1);
+
+        RestAssured.given().log().all()
+                .contentType(ContentType.JSON)
+                .body(params)
+                .when()
+                .post("/waiting-reservations")
+                .then().log().all()
+                .statusCode(409);
+    }
+
+    @Test
+    void 존재하지_않는_슬롯에_대기_신청을_하면_404을_반환한다() {
+        Map<String, Object> params = new HashMap<>();
+        params.put("name", "고래");
+        params.put("dateId", 999);
+        params.put("timeId", 999);
+        params.put("themeId", 999);
+
+        RestAssured.given().log().all()
+                .contentType(ContentType.JSON)
+                .body(params)
+                .when()
+                .post("/waiting-reservations")
+                .then().log().all()
+                .statusCode(404);
+
+    }
+
+    @Test
+    void 사용자는_예약_대기를_취소한다() {
+        RestAssured.given().log().all()
+            .contentType(ContentType.JSON)
+            .when()
+            .delete("/waiting-reservations/" + 1)
```

</details>

### 리뷰 본문 4383159021: Chocochip101

- 상대방 발언, 참여자
- 시각: 2026-05-28T18:13:18Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/415#pullrequestreview-4383159021)
- 리뷰 상태: `CHANGES_REQUESTED`

> 안녕하세요, 고래! 만나서 반갑습니다. 리뷰어 초코칩이라고 합니다🍪
> 요구사항에 맞게 잘 구현해주셨네요 👍🏻
> 리뷰 남겼으니 확인해보시고 재요청주세요!

### 인라인 코멘트 3329572855: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-31T01:43:38Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/415#discussion_r3329572855)
- 코드: `src/main/java/roomescape/domain/reservation/ReservationService.java`, 현재 줄 None, 원래 줄 86
- 답변 대상: [코멘트 3319515100](https://github.com/woowacourse/spring-roomescape-waiting/pull/415#discussion_r3319515100)
- 소속 리뷰 ID: 4396245681

> 맞습니다. 예약 취소와 대기자 승격은 하나의 작업으로 처리되어야 하는데, 현재 트랜잭션이 없어 중간 실패 시 정합성이 깨질 수 있겠네요. `cancelReservation`에 `@Transactional`을 적용해 승격 예약 저장, 대기 삭제, 기존 예약 삭제가 함께 커밋/롤백되도록 수정하겠습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -58,13 +62,29 @@ public void deleteReservation(Long id) {

     public List<ReservationResponse> getReservationsByName(String name) {
         return reservationRepository.findByName(name).stream()
-            .map(ReservationResponse::from)
-            .toList();
+                .map(ReservationResponse::from)
+                .toList();
     }

     public void cancelReservation(Long id) {
         Reservation reservation = findById(id);
         validateModifiable(reservation);
+
+        Optional<WaitingReservation> waitingReservationOpt = waitingReservationRepository.findOldestBySlot(
+                reservation.getDate().getId(),
+                reservation.getTime().getId(),
+                reservation.getTheme().getId()
+        );
+        if (waitingReservationOpt.isPresent()) {
+            WaitingReservation waitingReservation = waitingReservationOpt.get();
+            reservationRepository.save(Reservation.createWithoutId(
+                    waitingReservation.getName(),
+                    waitingReservation.getDate(),
+                    waitingReservation.getTime(),
+                    waitingReservation.getTheme()
+            ));
+            waitingReservationRepository.deleteById(waitingReservation.getId());
```

</details>

### 인라인 코멘트 3329576447: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-31T01:48:23Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/415#discussion_r3329576447)
- 코드: `src/main/java/roomescape/domain/reservation/ReservationService.java`, 현재 줄 None, 원래 줄 73
- 답변 대상: [코멘트 3319672617](https://github.com/woowacourse/spring-roomescape-waiting/pull/415#discussion_r3319672617)
- 소속 리뷰 ID: 4396245681

> 의도된 동작은 아니고, 수정으로 기존 슬롯이 비는 경우를 미처 고려하지 못했습니다.
> 예약의 날짜/시간이 실제로 변경되어 기존 슬롯이 비는 경우에는 해당 슬롯의 가장 오래된 대기자를 승격하도록 수정하겠습니다. 다만 슬롯이 변경되지 않는 수정 요청에서는 승격이 일어나지 않도록 조건을 분리해보겠습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -58,13 +62,29 @@ public void deleteReservation(Long id) {

     public List<ReservationResponse> getReservationsByName(String name) {
         return reservationRepository.findByName(name).stream()
-            .map(ReservationResponse::from)
-            .toList();
+                .map(ReservationResponse::from)
+                .toList();
     }

     public void cancelReservation(Long id) {
         Reservation reservation = findById(id);
         validateModifiable(reservation);
+
+        Optional<WaitingReservation> waitingReservationOpt = waitingReservationRepository.findOldestBySlot(
```

</details>

### 인라인 코멘트 3329609390: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-31T02:30:50Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/415#discussion_r3329609390)
- 코드: `src/main/java/roomescape/domain/waitingreservation/JdbcWaitingReservationRepository.java`, 현재 줄 None, 원래 줄 36
- 답변 대상: [코멘트 3319597649](https://github.com/woowacourse/spring-roomescape-waiting/pull/415#discussion_r3319597649)
- 소속 리뷰 ID: 4396245681

> 쿼리 변경하면서 삭제를 놓쳤네요! 감사합니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,191 @@
+package roomescape.domain.waitingreservation;
+
+import java.sql.PreparedStatement;
+import java.sql.Statement;
+import java.sql.Timestamp;
+import java.time.LocalDate;
+import java.time.LocalTime;
+import java.util.List;
+import java.util.Optional;
+import lombok.RequiredArgsConstructor;
+import org.springframework.jdbc.core.JdbcTemplate;
+import org.springframework.jdbc.core.RowMapper;
+import org.springframework.jdbc.support.GeneratedKeyHolder;
+import org.springframework.jdbc.support.KeyHolder;
+import org.springframework.stereotype.Repository;
+import roomescape.domain.reservationdate.ReservationDate;
+import roomescape.domain.reservationtime.ReservationTime;
+import roomescape.domain.theme.Theme;
+import roomescape.domain.waitingreservation.dto.WaitingReservationWithRank;
+
+@Repository
+@RequiredArgsConstructor
+public class JdbcWaitingReservationRepository implements WaitingReservationRepository {
+
+    private static final String INSERT_SQL = "insert into waiting_reservation(name, date_id, time_id, theme_id, created_at) values (?, ?, ?, ?, ?)";
+
+    private static final String EXIST_BY_NAME_DATE_TIME_THEME_SQL =
+            """
+                    select exists(
+                    select 1
+                    from waiting_reservation
+                    where name = ? and date_id = ? and time_id = ? and theme_id = ?
+                    );
+                    """;
+
+    private static final String FIND_OLDEST_SQL =
```

</details>

### 인라인 코멘트 3329611965: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-31T02:34:01Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/415#discussion_r3329611965)
- 코드: `src/main/java/roomescape/domain/waitingreservation/WaitingReservationService.java`, 현재 줄 None, 원래 줄 44
- 답변 대상: [코멘트 3319573624](https://github.com/woowacourse/spring-roomescape-waiting/pull/415#discussion_r3319573624)
- 소속 리뷰 ID: 4396245681

> 동의합니다. 존재하지 않는 슬롯 구성 요소에 대해 중복 여부를 먼저 조회하는 것은 불필요하고 검증 순서도 어색하네요.
> 존재 확인을 먼저 수행한 뒤 유효한 슬롯에 대해서만 중복 대기 여부를 검사하도록 순서를 변경하겠습니다!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,84 @@
+package roomescape.domain.waitingreservation;
+
+import java.time.Clock;
+import java.time.LocalDateTime;
+import java.util.List;
+import lombok.RequiredArgsConstructor;
+import lombok.extern.slf4j.Slf4j;
+import org.springframework.stereotype.Service;
+import roomescape.domain.reservation.ReservationRepository;
+import roomescape.domain.reservationdate.ReservationDate;
+import roomescape.domain.reservationdate.ReservationDateService;
+import roomescape.domain.reservationtime.ReservationTime;
+import roomescape.domain.reservationtime.ReservationTimeService;
+import roomescape.domain.theme.Theme;
+import roomescape.domain.theme.ThemeService;
+import roomescape.domain.waitingreservation.dto.WaitingReservationCreationRequest;
+import roomescape.domain.waitingreservation.dto.WaitingReservationCreationResponse;
+import roomescape.domain.waitingreservation.dto.WaitingReservationWithRankResponse;
+import roomescape.support.exception.RoomescapeException;
+import roomescape.support.exception.WaitingReservationErrorCode;
+
+@Slf4j
+@Service
+@RequiredArgsConstructor
+public class WaitingReservationService {
+
+    private final WaitingReservationRepository waitingReservationRepository;
+    private final ReservationRepository reservationRepository;
+    private final ReservationDateService reservationDateService;
+    private final ReservationTimeService reservationTimeService;
+    private final ThemeService themeService;
+    private final Clock clock;
+
+    public WaitingReservationCreationResponse createWaitingReservation(WaitingReservationCreationRequest request) {
+        validateDuplicationOfWaitingReservation(request);
+        ReservationDate date = reservationDateService.findById(request.dateId());
+        ReservationTime time = reservationTimeService.findById(request.timeId());
+        Theme theme = themeService.findById(request.themeId());
+        validateNotPast(date, time);
+        validateSlotIsReserved(request);
+
+        WaitingReservation waitingReservation = request.toEntity(date, time, theme, LocalDateTime.now(clock));
+        WaitingReservation savedWaitingReservation = waitingReservationRepository.save(waitingReservation);
+        return WaitingReservationCreationResponse.from(savedWaitingReservation);
```

</details>

### 인라인 코멘트 3329623933: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-31T02:50:03Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/415#discussion_r3329623933)
- 코드: `src/main/java/roomescape/domain/waitingreservation/WaitingReservationService.java`, 현재 줄 80, 원래 줄 75
- 답변 대상: [코멘트 3319537208](https://github.com/woowacourse/spring-roomescape-waiting/pull/415#discussion_r3319537208)
- 소속 리뷰 ID: 4396245681

> 사실 저 또한 초코칩의 의견대로 진행을 했었는데 이번에 페어와 의견을 나누면서 새로운 방법도 시도해본 결과입니다.
> 아래와 같은 이유로 그대로 진행을 했습니다.
>
> DELETE를 멱등하게 보고 존재하지 않는 ID에 대해서도 204를 반환하는 선택도 가능하다고 생각했습니다. 특히 현재는 hard delete라서 이미 삭제된 요청과 처음부터 잘못된 ID 요청을 명확히 구분하기 어렵다고 생각합니다.
> 또한 이번에 내부 로그로도 추적할 수 있는 것을 처음 보아 신기했고, 다른 부분들에도 동일하게 되어 있는 점, 일관성도 고려했습니다.
>
> 다만 이 API는 사용자의 예약 대기 취소 요청이므로, 클라이언트가 잘못된 ID를 보내고 있다면 상태 불일치를 빠르게 인지하는 것이 더 중요하다고 생각이 바뀌었습니다. 따라서 존재하지 않는 예약, 예약 대기 취소에 대해서도 예외를 반환하도록 수정하겠습니다.
> 더불어 삭제 예외를 처리를 하며 고민이 생겼습니다.
> 레포지토리 deleteById에서 예외를 던지는 경우와 서비스 레이어에서 int 값을 판단해서 던지는 것 중 고민을 했습니다.
> 삭제 실패에도 여러 가지 다른 이유라고 판단되고 그 이유들을 레포지토리에서 아는 것이 어색하다고 생각했습니다.
> 그러므로 서비스에서 세부적으로 예외를 던지는 것으로 수정해보겠습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,84 @@
+package roomescape.domain.waitingreservation;
+
+import java.time.Clock;
+import java.time.LocalDateTime;
+import java.util.List;
+import lombok.RequiredArgsConstructor;
+import lombok.extern.slf4j.Slf4j;
+import org.springframework.stereotype.Service;
+import roomescape.domain.reservation.ReservationRepository;
+import roomescape.domain.reservationdate.ReservationDate;
+import roomescape.domain.reservationdate.ReservationDateService;
+import roomescape.domain.reservationtime.ReservationTime;
+import roomescape.domain.reservationtime.ReservationTimeService;
+import roomescape.domain.theme.Theme;
+import roomescape.domain.theme.ThemeService;
+import roomescape.domain.waitingreservation.dto.WaitingReservationCreationRequest;
+import roomescape.domain.waitingreservation.dto.WaitingReservationCreationResponse;
+import roomescape.domain.waitingreservation.dto.WaitingReservationWithRankResponse;
+import roomescape.support.exception.RoomescapeException;
+import roomescape.support.exception.WaitingReservationErrorCode;
+
+@Slf4j
+@Service
+@RequiredArgsConstructor
+public class WaitingReservationService {
+
+    private final WaitingReservationRepository waitingReservationRepository;
+    private final ReservationRepository reservationRepository;
+    private final ReservationDateService reservationDateService;
+    private final ReservationTimeService reservationTimeService;
+    private final ThemeService themeService;
+    private final Clock clock;
+
+    public WaitingReservationCreationResponse createWaitingReservation(WaitingReservationCreationRequest request) {
+        validateDuplicationOfWaitingReservation(request);
+        ReservationDate date = reservationDateService.findById(request.dateId());
+        ReservationTime time = reservationTimeService.findById(request.timeId());
+        Theme theme = themeService.findById(request.themeId());
+        validateNotPast(date, time);
+        validateSlotIsReserved(request);
+
+        WaitingReservation waitingReservation = request.toEntity(date, time, theme, LocalDateTime.now(clock));
+        WaitingReservation savedWaitingReservation = waitingReservationRepository.save(waitingReservation);
+        return WaitingReservationCreationResponse.from(savedWaitingReservation);
+    }
+
+    private void validateDuplicationOfWaitingReservation(WaitingReservationCreationRequest request) {
+        if (waitingReservationRepository.existsByNameAndDateIdAndTimeIdAndThemeId(request.name(), request.dateId(), request.timeId(), request.themeId())) {
+            throw new RoomescapeException(WaitingReservationErrorCode.DUPLICATE_WAITING_RESERVATION);
+        }
+    }
+
+    private void validateSlotIsReserved(WaitingReservationCreationRequest request) {
+        boolean reserved = reservationRepository.existsByDateIdAndTimeIdAndThemeId(
+            request.dateId(),
+            request.timeId(),
+            request.themeId()
+        );
+        if (!reserved) {
+            throw new RoomescapeException(WaitingReservationErrorCode.AVAILABLE_SLOT_NOT_WAITABLE);
+        }
+    }
+
+    private void validateNotPast(ReservationDate date, ReservationTime time) {
+        LocalDateTime reservationDateTime = LocalDateTime.of(date.getPlayDay(), time.getStartAt());
+        if (reservationDateTime.isBefore(LocalDateTime.now(clock))) {
+            throw new RoomescapeException(WaitingReservationErrorCode.PAST_TIME_NOT_ALLOWED);
+        }
+    }
+
+    public void cancelWaitingReservation(Long id) {
+        int deletedCount = waitingReservationRepository.deleteById(id);
+        if (deletedCount == 0) {
+            log.warn("이미 삭제된 예약 대기 삭제 요청이 들어왔습니다. reservationId={}", id);
+        }
```

</details>

### 인라인 코멘트 3329747303: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-31T05:17:44Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/415#discussion_r3329747303)
- 코드: `src/test/java/roomescape/domain/waitingreservation/WaitingReservationControllerTest.java`, 현재 줄 None, 원래 줄 105
- 답변 대상: [코멘트 3319819286](https://github.com/woowacourse/spring-roomescape-waiting/pull/415#discussion_r3319819286)
- 소속 리뷰 ID: 4396245681

> `truncate.sql`에 의존하지 않도록 테스트 기본 데이터 로드를 끄고, 테스트가 필요한 fixture를 직접 준비하는 방향으로 정리해보겠습니다!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,122 @@
+package roomescape.domain.waitingreservation;
+
+import static org.hamcrest.Matchers.is;
+
+import io.restassured.RestAssured;
+import io.restassured.http.ContentType;
+import java.util.HashMap;
+import java.util.Map;
+import org.junit.jupiter.api.BeforeEach;
+import org.junit.jupiter.api.Test;
+import org.springframework.boot.test.context.SpringBootTest;
+import org.springframework.boot.test.web.server.LocalServerPort;
+import org.springframework.test.annotation.DirtiesContext;
+import org.springframework.test.context.jdbc.Sql;
+
+@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
+@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_CLASS)
+@Sql({"/truncate.sql", "/waiting-reservation-test-data.sql"})
+class WaitingReservationControllerTest {
+
+    @LocalServerPort
+    private int port;
+
+    @BeforeEach
+    void setUp() {
+        RestAssured.port = this.port;
+    }
+
+    @Test
+    void 사용자는_예약_대기를_신청한다() {
+        Map<String, Object> params = new HashMap<>();
+        params.put("name", "고래");
+        params.put("dateId", 1);
+        params.put("timeId", 1);
+        params.put("themeId", 4);
+
+        RestAssured.given().log().all()
+                .contentType(ContentType.JSON)
+                .body(params)
+                .when()
+                .post("/waiting-reservations")
+                .then().log().all()
+                .statusCode(201)
+                .body("name", is("고래"))
+                .body("theme.name", is("코미디테마"));
+    }
+
+    @Test
+    void 중복_예약_대기_신청을_하면_409를_반환한다() {
+        Map<String, Object> params = new HashMap<>();
+        params.put("name", "기존대기자");
+        params.put("dateId", 1);
+        params.put("timeId", 1);
+        params.put("themeId", 1);
+
+        RestAssured.given().log().all()
+                .contentType(ContentType.JSON)
+                .body(params)
+                .when()
+                .post("/waiting-reservations")
+                .then().log().all()
+                .statusCode(409);
+    }
+
+    @Test
+    void 예약_가능한_시간에_대기_신청하면_409을_반환한다() {
+        Map<String, Object> params = new HashMap<>();
+        params.put("name", "고래");
+        params.put("dateId", 1);
+        params.put("timeId", 2);
+        params.put("themeId", 1);
+
+        RestAssured.given().log().all()
+                .contentType(ContentType.JSON)
+                .body(params)
+                .when()
+                .post("/waiting-reservations")
+                .then().log().all()
+                .statusCode(409);
+    }
+
+    @Test
+    void 존재하지_않는_슬롯에_대기_신청을_하면_404을_반환한다() {
+        Map<String, Object> params = new HashMap<>();
+        params.put("name", "고래");
+        params.put("dateId", 999);
+        params.put("timeId", 999);
+        params.put("themeId", 999);
+
+        RestAssured.given().log().all()
+                .contentType(ContentType.JSON)
+                .body(params)
+                .when()
+                .post("/waiting-reservations")
+                .then().log().all()
+                .statusCode(404);
+
+    }
+
+    @Test
+    void 사용자는_예약_대기를_취소한다() {
+        RestAssured.given().log().all()
+            .contentType(ContentType.JSON)
+            .when()
+            .delete("/waiting-reservations/" + 1)
```

</details>

### 인라인 코멘트 3329749920: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-31T05:21:16Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/415#discussion_r3329749920)
- 코드: `src/test/java/roomescape/domain/waitingreservation/JdbcWaitingReservationRepositoryTest.java`, 현재 줄 None, 원래 줄 23
- 답변 대상: [코멘트 3319744161](https://github.com/woowacourse/spring-roomescape-waiting/pull/415#discussion_r3319744161)
- 소속 리뷰 ID: 4396245681

> 네, 확인해보니 '@JdbcTest' 내부에 트랜잭셔널이 있는 것을 확인했습니다!
> `@JdbcTest`의 트랜잭션 롤백으로 테스트 간 데이터 격리가 가능하므로 `truncate.sql` 초기화는 불필요하다고 판단됐고 테스트 환경에 대한 세팅을 새로 고민을 해봤습니다.
> 테스트는 테스트 전용 DB를 사용하도록 하고 각 테스트가 필요한 테스트 데이터를 직접 준비하는 것이 테스트 격리면에서 좋다고 판단되어서   `@Sql("/truncate.sql")`은 제거하고 새롭게 수정해보겠습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,188 @@
+package roomescape.domain.waitingreservation;
+
+import static org.assertj.core.api.Assertions.assertThat;
+import static org.assertj.core.api.Assertions.assertThatThrownBy;
+
+import java.time.LocalDate;
+import java.time.LocalDateTime;
+import java.time.LocalTime;
+import java.util.List;
+import org.junit.jupiter.api.BeforeEach;
+import org.junit.jupiter.api.Test;
+import org.springframework.beans.factory.annotation.Autowired;
+import org.springframework.boot.test.autoconfigure.jdbc.JdbcTest;
+import org.springframework.dao.DuplicateKeyException;
+import org.springframework.jdbc.core.JdbcTemplate;
+import org.springframework.test.context.jdbc.Sql;
+import roomescape.domain.reservationdate.ReservationDate;
+import roomescape.domain.reservationtime.ReservationTime;
+import roomescape.domain.theme.Theme;
+import roomescape.domain.waitingreservation.dto.WaitingReservationWithRank;
+
+@JdbcTest
+@Sql("/truncate.sql")
```

</details>

### 인라인 코멘트 3329758843: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-31T05:30:43Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/415#discussion_r3329758843)
- 코드: `src/test/java/roomescape/domain/waitingreservation/WaitingReservationControllerTest.java`, 현재 줄 16, 원래 줄 18
- 답변 대상: [코멘트 3319809672](https://github.com/woowacourse/spring-roomescape-waiting/pull/415#discussion_r3319809672)
- 소속 리뷰 ID: 4396245681

> 확인해보니 각 어노테이션의 역할은 다음과 같았습니다.
>
> `@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)`는 스프링 애플리케이션 컨텍스트를 로드하고, 내장 웹 서버를 사용 가능한 랜덤 포트로 실행하는 설정이었습니다. 그래서 MockMvc처럼 컨트롤러만 호출하는 방식이 아니라, RestAssured 등을 통해 실제 HTTP 요청을 보내는 테스트가 가능해집니다.
>
> `@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_CLASS)`는 테스트 클래스 실행이 끝난 뒤 해당 테스트에서 사용한 ApplicationContext를 테스트 컨텍스트 캐시에서 제거하도록 표시하는 설정이었습니다. 처음에는 단순히 메모리를 정리하는 용도라고 생각했는데, 정확히는 이후 테스트에서 같은 컨텍스트를 재사용하지 않도록 만드는 기능이었습니다.
>
> `@Sql({"/truncate.sql", "/waiting-reservation-test-data.sql"})`은 지정한 SQL 스크립트를 테스트 실행 과정에서 실행하는 설정이었습니다. 클래스 레벨에 붙이고 별도 executionPhase를 지정하지 않으면 기본적으로 각 테스트 메서드마다 모두 실행 전에 SQL이 순서대로 실행됩니다.
>
> 위의 셋 어노테이션을 공부하면서 지금 불필요한 비용이 발생하는 것을 느낄 수 있었습니다! 해당 부분들을 고쳐보도록 하겠습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,122 @@
+package roomescape.domain.waitingreservation;
+
+import static org.hamcrest.Matchers.is;
+
+import io.restassured.RestAssured;
+import io.restassured.http.ContentType;
+import java.util.HashMap;
+import java.util.Map;
+import org.junit.jupiter.api.BeforeEach;
+import org.junit.jupiter.api.Test;
+import org.springframework.boot.test.context.SpringBootTest;
+import org.springframework.boot.test.web.server.LocalServerPort;
+import org.springframework.test.annotation.DirtiesContext;
+import org.springframework.test.context.jdbc.Sql;
+
+@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
+@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_CLASS)
+@Sql({"/truncate.sql", "/waiting-reservation-test-data.sql"})
```

</details>

### 리뷰 본문 4396245681: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-05-31T05:40:02Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/415#pullrequestreview-4396245681)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 3329892974: Chocochip101

- 상대방 발언, 참여자
- 시각: 2026-05-31T07:57:11Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/415#discussion_r3329892974)
- 코드: `src/main/resources/schema.sql`, 현재 줄 47, 원래 줄 47
- 소속 리뷰 ID: 4396554015

> 만약에 운영 환경에서 기존 테이블에 ALTER TABLE로 `UNIQUE (name, date_id, time_id, theme_id)`를 추가하면 어떤 문제가 발생할 수 있을까요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -29,6 +29,22 @@ CREATE TABLE IF NOT EXISTS reservation
     time_id  BIGINT NOT NULL,
     theme_id BIGINT NOT NULL,
     PRIMARY KEY (id),
+    UNIQUE (date_id, time_id, theme_id),
+    FOREIGN KEY (time_id) REFERENCES reservation_time (id),
+    FOREIGN KEY (date_id) REFERENCES reservation_date (id),
+    FOREIGN KEY (theme_id) REFERENCES theme (id)
+);
+
+CREATE TABLE IF NOT EXISTS waiting_reservation
+(
+    id       BIGINT       NOT NULL AUTO_INCREMENT,
+    name     VARCHAR(255) NOT NULL,
+    date_id  BIGINT NOT NULL,
+    time_id  BIGINT NOT NULL,
+    theme_id BIGINT NOT NULL,
+    created_at TIMESTAMP NOT NULL,
+    PRIMARY KEY (id),
+    UNIQUE (name, date_id, time_id, theme_id),
```

</details>

### 인라인 코멘트 3329904886: Chocochip101

- 상대방 발언, 참여자
- 시각: 2026-05-31T08:09:16Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/415#discussion_r3329904886)
- 코드: `src/main/java/roomescape/domain/waitingreservation/JdbcWaitingReservationRepository.java`, 현재 줄 59, 원래 줄 59
- 소속 리뷰 ID: 4396554015

> ROW_NUMBER() OVER를 사용해주셨네요.
> 순번을 서버에서 계산하는 방식, 디비에서 계산하는 방식, 순번 자체를 칼럼으로 저장하는 방식이 있었을텐데 각자 어떤 장단점이 있나요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,177 @@
+package roomescape.domain.waitingreservation;
+
+import java.sql.PreparedStatement;
+import java.sql.Statement;
+import java.sql.Timestamp;
+import java.time.LocalDate;
+import java.time.LocalTime;
+import java.util.List;
+import java.util.Optional;
+import lombok.RequiredArgsConstructor;
+import org.springframework.jdbc.core.JdbcTemplate;
+import org.springframework.jdbc.core.RowMapper;
+import org.springframework.jdbc.support.GeneratedKeyHolder;
+import org.springframework.jdbc.support.KeyHolder;
+import org.springframework.stereotype.Repository;
+import roomescape.domain.reservationdate.ReservationDate;
+import roomescape.domain.reservationtime.ReservationTime;
+import roomescape.domain.theme.Theme;
+import roomescape.domain.waitingreservation.dto.WaitingReservationWithRank;
+
+@Repository
+@RequiredArgsConstructor
+public class JdbcWaitingReservationRepository implements WaitingReservationRepository {
+
+    private static final String INSERT_SQL = "insert into waiting_reservation(name, date_id, time_id, theme_id, created_at) values (?, ?, ?, ?, ?)";
+
+    private static final String EXIST_BY_NAME_DATE_TIME_THEME_SQL =
+            """
+                    select exists(
+                    select 1
+                    from waiting_reservation
+                    where name = ? and date_id = ? and time_id = ? and theme_id = ?
+                    );
+                    """;
+
+    private static final String FIND_OLDEST_BY_SLOT_SQL =
+            """
+                    select wr.id, wr.name, wr.created_at,
+                           rd.id as date_id, rd.play_day,
+                           rt.id as time_id, rt.start_at,
+                           th.id as theme_id, th.name as theme_name, th.content as theme_content, th.url as theme_url
+                    from waiting_reservation wr
+                    join reservation_date rd on wr.date_id = rd.id
+                    join reservation_time rt on wr.time_id = rt.id
+                    join theme th on wr.theme_id = th.id
+                    where wr.date_id = ? and wr.time_id = ? and wr.theme_id = ?
+                    order by wr.created_at asc, wr.id asc
+                    limit 1
+                    """;
+
+    private static final String FIND_ALL_BY_NAME_WITH_RANK_SQL =
+            """
+                    select ranked.id, ranked.name, ranked.created_at, ranked.waiting_rank,
+                           rd.id as date_id, rd.play_day,
+                           rt.id as time_id, rt.start_at,
+                           th.id as theme_id, th.name as theme_name, th.content as theme_content, th.url as theme_url
+                    from (
+                        select wr.id, wr.name, wr.date_id, wr.time_id, wr.theme_id, wr.created_at,
+                               row_number() over (
```

</details>

### 인라인 코멘트 3329911372: Chocochip101

- 상대방 발언, 참여자
- 시각: 2026-05-31T08:15:17Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/415#discussion_r3329911372)
- 코드: `src/test/java/roomescape/domain/reservation/ReservationCancellationIntegrationTest.java`, 현재 줄 24, 원래 줄 24
- 소속 리뷰 ID: 4396554015

> 여긴 여전히 세개의 어노테이션이 남아있네요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,150 @@
+package roomescape.domain.reservation;
+
+import static org.assertj.core.api.Assertions.assertThat;
+
+import java.time.LocalDate;
+import java.time.LocalDateTime;
+import java.time.LocalTime;
+import org.junit.jupiter.api.BeforeEach;
+import org.junit.jupiter.api.Test;
+import org.springframework.beans.factory.annotation.Autowired;
+import org.springframework.boot.test.context.SpringBootTest;
+import org.springframework.jdbc.core.JdbcTemplate;
+import org.springframework.test.annotation.DirtiesContext;
+import org.springframework.test.context.jdbc.Sql;
+import roomescape.domain.reservation.dto.ReservationUpdateRequest;
+import roomescape.domain.reservationdate.ReservationDate;
+import roomescape.domain.reservationtime.ReservationTime;
+import roomescape.domain.theme.Theme;
+import roomescape.domain.waitingreservation.WaitingReservation;
+import roomescape.domain.waitingreservation.WaitingReservationRepository;
+
+@SpringBootTest
+@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_CLASS)
+@Sql("/truncate.sql")
```

</details>

### 리뷰 본문 4396554015: Chocochip101

- 상대방 발언, 참여자
- 시각: 2026-05-31T08:22:53Z
- [게시 원문](https://github.com/woowacourse/spring-roomescape-waiting/pull/415#pullrequestreview-4396554015)
- 리뷰 상태: `APPROVED`

> 안녕하세요, 고래!
> 빠르게 수정해주셔서 감사합니다 🙇🏻
> 요구사항을 모두 만족해서 Approve&Merge하겠습니다.
> 작은 커맨트들 남겨놨는데, 추가 질문이나 답변이 있다면 다음 사이클 PR에 남기셔도 좋을 것 같네요.
> 다음 사이클에서 뵈어요 ✋🏻
