# 개인 Java 코딩 기준, 근거 기반 초안

상태: 2026-09-25 초안. 사용자가 항목별로 승인한 전역 컨벤션은 아니다. 여기서 **기본값**은 새 Java 코드를 쓸 때 먼저 시도할 표현이고, **상황 판단**은 현재 요구사항과 기존 코드에 맞춰 고르는 선택이다. 블랙잭부터 예약 대기까지 본인 코드와 PR 답변을 대조했다. `java-http`는 사용자가 이번 기준의 대상에서 제외했다.

## 적용 순서

1. 현재 저장소의 요구사항, `AGENTS.md`, `CONTEXT.md`, ADR, 언어 버전, 근처 코드와 테스트를 확인한다.
2. 사용자 요구를 성공 동작, 실패 조건, 바뀌는 상태로 풀어 말한다. 용어가 모호해 코드 구조가 달라질 때만 질문한다.
3. 아래에서 이번 변경과 관련된 기준을 적용하고, 예시 코드는 그대로 복제하지 말고 그 선택 이유를 재사용한다.
4. 현재 코드와 초안이 충돌하면 현재 저장소의 합의된 계약을 따른다. 사용자가 이번 대화에서 표현한 선호는 이 초안보다 우선한다. 반복 충돌은 사용자에게 드러내고 기준 수정 후보로 남긴다.

## 1. 코드를 시작하는 순서

**기본값:** 기능 하나의 입력, 핵심 행위, 관찰 가능한 결과를 먼저 연결한다. 그 과정에서 드러난 규칙의 주인을 정하고, 테스트를 작성하거나 보강하면서 객체를 분리한다. 설계도를 먼저 완성하느라 동작 확인을 늦추지 않는다.

- 실패할 수 있는 경우를 정상 흐름과 함께 적는다. 존재하지 않는 참조, 중복, 상태 전이 불가, 경계 시각처럼 실제로 달라지는 결과부터 잡는다.
- 한 변경의 이름은 기술 작업보다 사용자나 도메인의 행위를 말한다. `cancelReservation`, `changeSchedule`, `promoteOldestWaiting`처럼 읽으면 어떤 일이 일어나는지 드러나게 한다.
- 중복된 코드 한 줄보다 반복되는 **판단이나 조립 책임**을 먼저 찾는다. 날짜, 시간, 테마를 여러 서비스가 조회해 조립하는 문제를 `ReservationSlotResolver`로 회수한 것이 예다.
- 새 타입은 이름, 소유할 규칙, 사용처를 설명할 수 있을 때 만든다. 추상화와 패턴은 변경이나 테스트의 실제 불편을 해결할 때 쓴다.

**근거:** [waiting #429 답변](https://github.com/woowacourse/spring-roomescape-waiting/pull/429), `spring-roomescape-waiting`의 `ReservationSlotResolver`; [blackjack #1094 답변](https://github.com/woowacourse/java-blackjack/pull/1094).

## 2. 객체가 맡는 책임과 상태

**기본값:** 상태를 가진 객체에 그 상태의 유효성 검사와 행위를 둔다. Service는 여러 객체, 저장소, 시간, 인증 문맥을 조합한다. Controller는 전송 계약을 다룬다.

- 공개 생성 경로에서 유효한 상태를 보장한다. 이후 변경은 공개 Setter보다 `cancel()`, `changeSchedule(...)`, `draw(...)`처럼 허용된 행위로 드러낸다.
- 객체가 자기 규칙을 검사하게 하되, 다른 저장소나 현재 인증 사용자를 알아야 하는 검사는 유스케이스 경계에서 조합한다. DB가 최종 보장할 중복은 DB 제약도 확인한다.
- 상태 전이에서 기존 객체를 바꿀지 새 객체를 돌려줄지는 모델의 수명과 사용 방식을 보고 고른다. `member`의 `Reservation.cancel()`은 새 객체를 반환하고, 블랙잭 `Hand.add()`는 게임 중 상태를 변경한다.
- 내부 컬렉션과 표현을 외부에 직접 넘기지 않는다. 호출자가 필요한 질문이나 동작을 제공하고, 목록이 필요하면 방어적 복사 또는 불변 뷰의 의미를 정한다.
- 상위 타입에 하위 구현 이름을 새기거나 `instanceof`로 분기하기 전에, 다형적 행위가 그 책임을 표현할 수 있는지 본다. 상태 패턴도 실제 분기 복잡도가 줄어드는지 확인한다.
- 일급 컬렉션은 단순 포장이 아니라 중복, 개수, 순서, 집계 같은 자기 규칙을 가질 때 쓴다. `Iterable`은 순회 공개가 캡슐화를 깨지 않는지 보고 선택한다.

**근거:** `spring-roomescape-member` `dd94d1b:src/main/java/roomescape/domain/Reservation.java`; `java-blackjack` `1dbbdec:src/main/java/domain/participant/Hand.java`, `Players.java`; [janggi #269 답변](https://github.com/woowacourse/java-janggi/pull/269), [blackjack #1028 답변](https://github.com/woowacourse/java-blackjack/pull/1028).

## 3. 생성, 값, 경계 타입

**기본값:** 생성 표현은 상태와 의도를 알려준다. `createNew`와 저장소 복원용 `from`처럼 생성 이유가 다르면 이름을 나눈다. 한 가지 명확한 생성 방법만 있으면 생성자도 자연스럽다.

- 값 자체가 동등성을 정의하고 상태가 바뀌지 않을 때 `record`를 검토한다. `Bet`, `Profit`, `ReservationSlot`은 값과 정책을 함께 표현한다. 식별성과 수명주기가 중요한 객체에 형식만 보고 `record`를 쓰지 않는다.
- 동등성은 식별 기준을 먼저 정한다. 같은 이름의 플레이어를 중복으로 보지 않으려면 `equals`와 `hashCode`가 함께 그 기준을 구현해야 한다. DB 식별자가 있는 객체의 동등성은 현재 저장소의 계약을 확인한다.
- 돈과 비율의 십진 계산은 `BigDecimal` 같은 정확한 표현과 반올림, 단위를 함께 정한다. 블랙잭의 베팅 하한과 오류 문구에는 불일치가 있으므로 과거 상수를 규칙으로 복제하지 않는다.
- 문자열 파싱과 HTTP 형식은 도메인에 들이기 전에 변환한다. 전송 DTO, 유스케이스 입력, 도메인 값은 변경 이유가 실제로 다를 때 분리한다. DB 행을 위한 별도 타입도 매핑 이득이 있을 때 도입한다.
- 컬렉션을 보관할 때 외부 참조를 통한 변경이 문제라면 `List.copyOf`처럼 생성 시 복사한다. 반환 시 불변 뷰만 제공하면 내부 변경은 계속 관찰될 수 있으므로 둘의 의미를 구분한다.
- 시간과 난수는 정책 입력일 때 제어 가능한 경계로 둔다. `Clock`, 이미 계산한 시각, `ShuffleStrategy` 중 가장 작은 방식을 택한다.

**근거:** [blackjack #1028 답변](https://github.com/woowacourse/java-blackjack/pull/1028), [blackjack #1094 답변](https://github.com/woowacourse/java-blackjack/pull/1094); `spring-roomescape-auth` `85c1974:src/main/java/roomescape/domain/Member.java`; `spring-roomescape-waiting` `03c112e:src/main/java/roomescape/domain/reservation/ReservationSlot.java`.

## 4. 메서드와 제어 흐름의 표현

**기본값:** 메서드는 한 가지 판단이나 행위를 읽을 수 있는 길이로 유지한다. 길이 제한 자체를 목표로 쪼개지 않는다.

- 실패 조건은 앞에서 검사하고 정상 흐름을 이어 쓴다. `if (...)` 뒤 예외 또는 조기 반환은 최근 Service 코드에 반복된다.
- 불리언 이름은 호출 자리에서 참과 거짓의 의미가 드러나게 한다. `isClosedForReservation`, `hasStarted`, `isSameSlot`처럼 정책을 말한다. 중첩 부정으로 읽기 어려우면 이름이나 조건을 다시 정한다.
- 여러 인자가 함께 다니고 같은 규칙을 공유하면 이름 있는 값으로 묶는다. 단순히 인자 수를 맞추려는 포장 객체는 만들지 않는다.
- `stream().map(...).toList()`는 목록 변환에, `flatMap`은 중첩 값의 평탄화가 더 읽힐 때 쓴다. 상태 변경, 예외 흐름, 순서가 중요한 절차는 `for`문이 자연스럽다. 블랙잭과 방탈출 코드 모두 두 방식을 쓴다.
- `Optional`은 조회 결과의 부재를 드러내는 데 사용한다. 필수 참조는 `orElseThrow`, 선택적 승격은 `isEmpty()` 뒤 조기 반환처럼 부재의 뜻이 읽히게 한다.
- 리터럴이 정책의 일부이면 이름 있는 상수나 값 객체로 올린다. 모든 숫자를 기계적으로 상수화하는지는 아직 합의되지 않았다.
- 주석은 코드가 이미 보여 주는 동작보다, 왜 그 경계와 정책을 택했는지 설명할 때 쓴다.

**근거:** `spring-roomescape-waiting` `03c112e:src/main/java/roomescape/domain/reservation/ReservationService.java`; `java-blackjack` `1dbbdec:src/main/java/domain/Deck.java`, `domain/participant/Hand.java`; [blackjack #1028의 `flatMap` 대화](https://github.com/woowacourse/java-blackjack/pull/1028).

## 5. Spring 경계와 저장

**상황 판단:** 이 절은 Spring 또는 DB를 쓰는 코드에만 적용한다.

- Controller는 요청과 응답의 형태를 정하고, Service는 유스케이스 순서와 트랜잭션 경계를 정한다. Domain은 웹 타입을 알지 않는다. 요청 DTO를 Service에 직접 넘길지는 웹 형식과 유스케이스 계약이 함께 바뀌는지 보고 정한다.
- Repository 인터페이스는 대체 구현, 테스트 격리, 상위 정책의 안정된 계약에 이득이 있을 때 둔다. `admin`의 단일 JDBC 구현과 `waiting`의 테스트 경계는 서로 다른 선택이다.
- 조회는 필요한 정렬, 페이지 경계, 객체 복원 비용을 명시한다. 데이터가 늘어나는 목록의 무제한 `findAll`과 반복 조회는 실제 비용을 확인한다.
- 여러 쓰기가 한 행위를 이루면 실패 지점과 롤백 범위를 먼저 정한다. 같은 자원을 동시에 바꾸는 요청은 DB 제약, 잠금 순서, 조건부 갱신 결과로 검증한다. `@Transactional` 자체를 증거로 삼지 않는다.
- 예상 가능한 실패를 클라이언트가 구분할 수 있게 표현한다. 기술 예외를 그대로 API에 노출하지 않는다. 예외 계층과 중앙 오류 코드 중 하나를 전역 취향으로 고정하지 않는다.
- 인증된 사용자 식별자는 요청 문자열보다 서버가 검증한 문맥에서 받는다. `member`에서 `auth`로 이어진 선택이며, 페어 기반 `waiting` 코드의 이름 조회를 개인 기준으로 복제하지 않는다.

**근거:** [member #418 답변](https://github.com/woowacourse/spring-roomescape-member/pull/418), [waiting #415 답변](https://github.com/woowacourse/spring-roomescape-waiting/pull/415), [waiting #429 답변](https://github.com/woowacourse/spring-roomescape-waiting/pull/429); `spring-roomescape-auth` `85c1974`.

## 6. 테스트가 드러내야 할 것

**기본값:** 테스트 이름과 실패 메시지에서 지키는 정책과 깨진 경계를 알아볼 수 있게 한다.

- 유효한 경계와 바로 바깥 값을 나란히 확인한다. 예외 타입만으로는 다른 이유로 던진 예외를 통과시킬 수 있으므로 메시지나 상태도 확인한다.
- 한 테스트에 다른 정책의 단언을 쌓지 않는다. 준비 코드의 공유가 테스트 간 상태 의존으로 이어지면 각 테스트가 필요한 데이터를 직접 만든다.
- 순수 값과 상태 전이는 단위 테스트, SQL과 매핑은 Repository 통합 테스트, 롤백과 동시성은 실제 트랜잭션 및 DB 경계, HTTP 계약은 웹 또는 API 테스트에서 검증한다.
- 결과 상태로 행위가 증명되면 결과를 검사한다. 같은 최종 상태가 두 실행 경로에서 나올 수 있어 시나리오를 구별해야 할 때에만 상호작용 `verify`를 더한다.
- 시간을 고정해야 하는 테스트에는 `Clock.fixed`처럼 제어 가능한 값을 쓰고 마감 직전, 정확한 경계, 직후를 확인한다.
- 테스트 메서드 이름은 해당 저장소의 언어와 형식에 맞춘다. `member`는 영어 메서드와 한국어 `@DisplayName`, `waiting`은 한국어 메서드도 사용하므로 전역 명명법은 미결이다.

**근거:** `spring-roomescape-member` `dd94d1b:src/test/java/roomescape/domain/ReservationTest.java`; `spring-roomescape-waiting` `03c112e:src/test/java/roomescape/domain/reservation/ReservationSlotTest.java`; [janggi #269 답변](https://github.com/woowacourse/java-janggi/pull/269), [waiting #429의 롤백 테스트 대화](https://github.com/woowacourse/spring-roomescape-waiting/pull/429).

## 아직 사용자 선택이 필요한 표현

코드만 보고 취향을 확정하지 않는다. 해당 선택이 실제 작업 결과를 바꿀 때 현재 저장소의 형태를 우선하고, 사용자와 한 번에 한 항목씩 맞춘다.

| 선택 | 현재 증거 |
| --- | --- |
| 삼항 연산자를 어느 범위까지 쓸지 | 미션 코드와 리뷰만으로 지속적 선호를 확인하지 못함 |
| `stream`, `flatMap`, 반복문의 가독성 경계 | 블랙잭에서 `flatMap`을 선호한 답변이 있으나 최근 코드에는 반복문도 있음 |
| 테스트 이름과 `@DisplayName` 언어 | 미션별 표현이 다름 |
| `record`와 일반 클래스의 선택 범위 | 값의 의미를 기준으로 설명한 답변은 있지만 Spring 코드에서는 사용 목적이 다름 |
| 정적 팩터리와 생성자의 기본값 | 생성 의도가 여러 개일 때 팩터리를 중시했고 단일 경로는 생성자도 수용함 |
| 예외 계층, 오류 코드, API 메시지 형식 | `member`와 `waiting`의 구현이 다름 |
| 패키지를 계층 또는 기능 중심으로 구성할지 | 저장소 규모와 코드 계보가 다름 |
| Lombok, `var`, 포맷터, import 순서 | 저장소 설정이나 근처 코드에서 확인할 사항이며 개인 전역 선호는 미확인 |

## 증거를 다시 볼 때

[증거 지도](evidence-map.md)에서 최근순으로 `spring-roomescape-waiting`, `spring-roomescape-auth`, `spring-roomescape-member`, `spring-roomescape-admin`, `java-janggi`, `java-blackjack`의 본인 구현 ref와 PR 피드백을 찾는다. `waiting`은 페어 기반 코드라 개인 단독 선택으로 일반화하기 전에 본인 답변과 후속 변경을 확인한다. Mimir의 옛 기준 문서는 더 넓은 설계 초안이며, 이 문서와 마찬가지로 사용자 승인 전이다. 다른 기수의 블랙잭 리뷰는 비교 자료다.
