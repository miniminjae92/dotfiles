# woowacourse/java-blackjack #1028

[🚀 사이클1 - 미션 (블랙잭 게임 실행)] 고래 미션 제출합니다.

- [GitHub PR](https://github.com/woowacourse/java-blackjack/pull/1028)
- PR 작성자: `miniminjae92`
- 머지 시각: 2026-03-11T13:58:24Z
- [API 원본](../raw/java-blackjack-1028.json)
- 리뷰와 댓글 42건(본문 있는 발언 40건, 본인 기록 16건)

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
>
> ## 체크 리스트
>
> - [x] 미션의 필수 요구사항을 모두 구현했나요?
> - [x] Gradle `test`를 실행했을 때, 모든 테스트가 정상적으로 통과했나요?
> - [x] 애플리케이션이 정상적으로 실행되나요?
>
> ## 어떤 부분에 집중하여 리뷰해야 할까요?
>
> <!-- 리뷰어가 효과적으로 피드백할 수 있도록 중점적으로 피드백받고 싶은 내용을 공유해주세요.
> 예를 들어, 가장 고민했던 점이나 여전히 어려운 부분, 그리고 이에 대한 생각을 적을 수 있습니다. -->
>
> 가독성이 중요하다고 생각합니다, 부족한 부분이 많은데 가독성이 부족한 부분들에 대해서 알고싶습니다.
>
> 낮은 결합도와 높은 응집도를 가지고 싶은데 구체적인 방법과 경험을 많이 쌓고싶습니다.
>
> 일급 컬렉션을 순회할 수 있도록 이터러블을 구현하면 안되는 것인지 궁금합니다.
>
> Enum 작성을 할 때에 필드로 뷰에서 사용하기 위한 String을 가져도 되는지 궁금합니다.
> `Enum객체.name`으로 `equals`를 이용해야하는 것인지 사용해도 괜찮은지에 대한 판단이 헷갈립니다.
>
> 상속을 처음 사용해봤습니다. 핸드와 같은 상태를 공유하기 위해서 인터페이스보다 추상클래스를 사용해야한다고 생각했습니다. 다만 페어의 의견인 필드를 private로 하는 것을 지향해야한다는 얘기를 듣고 생각을 해보니 의존성을 위해서는 그것이 좋겠다고 느꼈습니다. 하지만 player, dealer를 다룰 때 hand를 마음껏 다룰 수 없음에 불편했고 접근제어자를 protected으로 사용하면 안되는지가 궁금했습니다. 메서드를 protected으로 Participant에 구현하면서 상태는 private로 유지하도록 최대한 노력하는 것이 맞는지 궁금합니다.
>
> 이름을 짓는 것이 너무 어려운데 좋은 방법은 많은 코드를 보는 것이라 생각하는데 다른 좋은 방법이 있다면 알고 싶습니다.
>
> 이번에 생성한 클래스가 많다고 느껴졌는데 어떤 식으로 분류를 하는 것이 좋을지 고민을 했는데 어려웠습니다. 관례가 있을까요?
>
> 단위테스트만 작성한 경험이 있는데 애플리케이션 단위에서 진행하는 것이 통합테스트라고 볼 수 있을까요? 맞다면 애플리케이션 단위에서의 테스트가 필수적인지 궁금합니다.
>
> 처음에 요구사항을 받았을 때 핵심 요구사항에서 도출되는 기능목록과 시나리오처럼 입출력 예시에서 나오는 순서를 기반으로한 기능목록이 함께 도출됐을 때 어떻게 정리를 하고 어디까지 설계를 하고 구현에 무엇부터 들어가야하는지에 대해서 실전에서 고민이 될 때가 많아 도움을 받을 수 있다면 받고 싶습니다.
>

## 대화와 리뷰 기록

### 인라인 코멘트 2911055280: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-10T11:21:37Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911055280)
- 코드: `.github/pull_request_template.md`, 현재 줄 16, 원래 줄 16
- 소속 리뷰 ID: 3921642743

> `pull_request_template.md`는 어떤 역할의 파일인가요?? 역할에 맞는 내용을 기입 하였다고 볼 수 있을까요??

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -9,29 +9,30 @@

 ## 체크 리스트

-- [ ] 미션의 필수 요구사항을 모두 구현했나요?
-- [ ] Gradle `test`를 실행했을 때, 모든 테스트가 정상적으로 통과했나요?
-- [ ] 애플리케이션이 정상적으로 실행되나요?
-- [ ] [프롤로그](https://prolog.techcourse.co.kr)에 셀프 체크를 작성했나요?
-  - <!-- 작성한 셀프 체크의 링크를 남겨주세요. -->
+- [x] 미션의 필수 요구사항을 모두 구현했나요?
+- [x] Gradle `test`를 실행했을 때, 모든 테스트가 정상적으로 통과했나요?
+- [x] 애플리케이션이 정상적으로 실행되나요?

+## 어떤 부분에 집중하여 리뷰해야 할까요?
```

</details>

### 인라인 코멘트 2911065029: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-10T11:23:44Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911065029)
- 코드: `src/main/java/domain/card/CardDto.java`, 현재 줄 None, 원래 줄 21
- 소속 리뷰 ID: 3921642743

> 고래가 생각하는 dto는 무엇이며 어떠한 목적으로 활용하면 좋을까요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,21 @@
+package domain.card;
+
+import java.util.ArrayList;
+import java.util.List;
+
+public record CardDto(List<Card> cards) {
+
+    public String getFormattedCards() {
+        List<String> cardsResult = new ArrayList<>();
+        for (Card card : cards) {
+            String suit = card.suitValue();
+            String rank = card.symbol();
+            cardsResult.add(rank + suit);
+        }
+        return String.join(", ", cardsResult);
+    }
+
+    public int size() {
+        return cards().size();
+    }
+}
```

</details>

### 인라인 코멘트 2911066626: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-10T11:24:06Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911066626)
- 코드: `src/main/java/domain/card/Card.java`, 현재 줄 None, 원래 줄 16
- 소속 리뷰 ID: 3921642743

> record를 활용하였네요! 어떠한 특성 때문에 활용하였을까요??

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,16 @@
+package domain.card;
+
+public record Card(Suit suit, Rank cardNumber) {
+    public boolean isAce() {
+        return this.cardNumber == Rank.ACE;
+    }
+
+    public String suitValue() {
+        return this.suit.getValue();
+    }
+
+    public String symbol() {
+        return this.cardNumber.getSymbol();
+    }
+
+}
```

</details>

### 인라인 코멘트 2911083181: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-10T11:27:41Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911083181)
- 코드: `src/main/java/domain/participant/Players.java`, 현재 줄 8, 원래 줄 8
- 소속 리뷰 ID: 3921642743

> > 일급 컬렉션을 순회할 수 있도록 이터러블을 구현하면 안되는 것인지 궁금합니다.
>
> 먼저 고래의 의도를 들어보고 판단해봐도 좋을 것 같아요 ㅎㅎ
>
> 1.  고래가 생각하는 일급컬렉션은 무엇이며 왜 필요할까요?
> 2. Iterable과 같은 인터페이스를 구현하고자 한 판단 기준은 무엇인가요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,51 @@
+package domain.participant;
+
+import java.util.HashSet;
+import java.util.Iterator;
+import java.util.List;
+import java.util.Set;
+
+public class Players implements Iterable<Player> {
```

</details>

### 인라인 코멘트 2911086373: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-10T11:28:22Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911086373)
- 코드: `src/main/java/domain/participant/Players.java`, 현재 줄 None, 원래 줄 16
- 소속 리뷰 ID: 3921642743

> copyOf를 사용하였네요! 어떤 이점이 있었나요??

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,51 @@
+package domain.participant;
+
+import java.util.HashSet;
+import java.util.Iterator;
+import java.util.List;
+import java.util.Set;
+
+public class Players implements Iterable<Player> {
+    private static final String ERROR_DUPLICATE_NAME = "플레이어 이름은 중복될 수 없습니다.";
+    private static final String ERROR_PLAYER_COUNT = "참가할 플레이어의 수는 최대 7명입니다.";
+    private static final int MAX_PLAYER_COUNT = 7;
+    private final List<Player> players;
+
+    private Players(List<Player> players) {
+        this.players = List.copyOf(players);
+    }
```

</details>

### 인라인 코멘트 2911089231: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-10T11:28:57Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911089231)
- 코드: `src/main/java/domain/participant/Players.java`, 현재 줄 None, 원래 줄 21
- 소속 리뷰 ID: 3921642743

> static 메서드를 활용하여 생성자를 구성한 이유가 무엇인가요??

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,51 @@
+package domain.participant;
+
+import java.util.HashSet;
+import java.util.Iterator;
+import java.util.List;
+import java.util.Set;
+
+public class Players implements Iterable<Player> {
+    private static final String ERROR_DUPLICATE_NAME = "플레이어 이름은 중복될 수 없습니다.";
+    private static final String ERROR_PLAYER_COUNT = "참가할 플레이어의 수는 최대 7명입니다.";
+    private static final int MAX_PLAYER_COUNT = 7;
+    private final List<Player> players;
+
+    private Players(List<Player> players) {
+        this.players = List.copyOf(players);
+    }
+
+    public static Players of(List<Player> players) {
+        validate(players);
+        return new Players(players);
+    }
```

</details>

### 인라인 코멘트 2911098115: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-10T11:30:44Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911098115)
- 코드: `src/main/java/domain/card/Rank.java`, 현재 줄 None, 원래 줄 16
- 소속 리뷰 ID: 3921642743

> > Enum 작성을 할 때에 필드로 뷰에서 사용하기 위한 String을 가져도 되는지 궁금합니다.
> > Enum객체.name으로 equals를 이용해야하는 것인지 사용해도 괜찮은지에 대한 판단이 헷갈립니다.
>
> Enum으로 구성한 객체가 우리가 잘 관리해야 하는 도메인 객체인지 아닌지에 따라 판단 기준이 달라질 것 같아요. 도메인 로직 내에서 View 관련 의존성이 들어 있을 때 어떤 장단점이 있을까요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,34 @@
+package domain.card;
+
+public enum Rank {
+    TWO(2, "2"),
+    THREE(3, "3"),
+    FOUR(4, "4"),
+    FIVE(5, "5"),
+    SIX(6, "6"),
+    SEVEN(7, "7"),
+    EIGHT(8, "8"),
+    NINE(9, "9"),
+    TEN(10, "10"),
+    JACK(10, "J"),
+    QUEEN(10, "Q"),
+    KING(10, "K"),
+    ACE(11, "A"),
```

</details>

### 인라인 코멘트 2911111982: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-10T11:33:25Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911111982)
- 코드: `src/main/java/domain/participant/Participant.java`, 현재 줄 15, 원래 줄 14
- 소속 리뷰 ID: 3921642743

> > 상속을 처음 사용해봤습니다. 핸드와 같은 상태를 공유하기 위해서 인터페이스보다 추상클래스를 사용해야한다고 생각했습니다.
>
> 좋은 접근이네요!
>
> > 다만 페어의 의견인 필드를 private로 하는 것을 지향해야한다는 얘기를 듣고 생각을 해보니 의존성을 위해서는 그것이 좋겠다고 느꼈습니다. 하지만 player, dealer를 다룰 때 hand를 마음껏 다룰 수 없음에 불편했고 접근제어자를 protected으로 사용하면 안되는지가 궁금했습니다. 메서드를 protected으로 Participant에 구현하면서 상태는 private로 유지하도록 최대한 노력하는 것이 맞는지 궁금합니다.
>
> private을 지향하는 목적과 어디까지 노출되지 말아야 한다고 생각하시나요? protected로는 원하는 가시성을 얻지 못하나요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,47 @@
+package domain.participant;
+
+import domain.card.Card;
+import domain.card.CardDto;
+import java.util.Objects;
+
+public abstract class Participant {
+    private final Name name;
+    private final Hand hand;
+
+    protected Participant(Name name) {
+        this.hand = new Hand();
+        this.name = name;
+    }
```

</details>

### 인라인 코멘트 2911126767: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-10T11:36:28Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911126767)
- 코드: `src/test/java/domain/participant/HandTest.java`, 현재 줄 15, 원래 줄 15
- 소속 리뷰 ID: 3921642743

> > 단위테스트만 작성한 경험이 있는데 애플리케이션 단위에서 진행하는 것이 통합테스트라고 볼 수 있을까요? 맞다면 애플리케이션 단위에서의 테스트가 필수적인지 궁금합니다.
>
> 먼저 답변드리기 전에 생각을 좀 더 들어보고 싶어요.
>  1. 고래가 생각하는 애플리케이션 단위는 무엇을 말씀하시는 건가요??
>  2. 단위테스트, 통합테스트는 무엇을 목적으로 테스트하는 걸까요? 그 밖에 또 어떤 테스트를 고려할 수 있을까요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,115 @@
+package domain.participant;
+
+import static org.assertj.core.api.Assertions.assertThat;
+
+import domain.card.Card;
+import domain.card.Rank;
+import domain.card.Suit;
+import java.util.List;
+import java.util.stream.Stream;
+import org.junit.jupiter.api.Test;
+import org.junit.jupiter.params.ParameterizedTest;
+import org.junit.jupiter.params.provider.Arguments;
+import org.junit.jupiter.params.provider.MethodSource;
+
+public class HandTest {
```

</details>

### 인라인 코멘트 2911168886: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-10T11:44:01Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911168886)
- 코드: `README.md`, 현재 줄 5, 원래 줄 5
- 소속 리뷰 ID: 3921642743

> > 처음에 요구사항을 받았을 때 핵심 요구사항에서 도출되는 기능목록과 시나리오처럼 입출력 예시에서 나오는 순서를 기반으로한 기능목록이 함께 도출됐을 때 어떻게 정리를 하고 어디까지 설계를 하고 구현에 무엇부터 들어가야하는지에 대해서 실전에서 고민이 될 때가 많아 도움을 받을 수 있다면 받고 싶습니다.
>
> 먼저 한 가지 일을 처리할 수 있는 가장 `작은 단위의 시나리오`를 생각해보면 어떻까요? 이번 미션처럼 블랙잭 게임으로 가정해볼게요.
>
>  - [  ] 카드 합계를 계산할 수 있다.
>      - [  ] ACE가 존재하지 않는 경우 전체 카드 점수를 합산한다.
>      - [  ] ACE를 11로 계산했을 때 합계가 21을 초과하면 해당 ACE는 1로 계산한다.
>      - [  ] ACE를 11로 계산했을 때 합계가 21 이하이면 해당 ACE는 11로 계산한다.
>  - [  ] 카드 뭉치가 비어 있는 경우 점수를 계산할 수 없다.
>  - [  ] ...
>
> 이러한 시나리오는 결국 특정한 한 가지 상황에 집중하기 때문에 TDD 사이클을 진행하는 데 무리 없이 활용할 수 있을 것 같아요. 또한 각각의 시나리오를 해결하다보면 이 문제를 해결할 객체를 떠올리게 되는데요, 이러한 것들이 모여 결국 Card, Deck과 같은 객체와 책임이 구성될 수 있다고 생각합니다.
>
> 물론 이러한 흐름이 단 번에 진행되는 것은 아니지만 한 가지 기능을 처리할 수 있는 여러 시나리오를 고민해보고 비슷한 성격을 카테고리로 묶어 하나씩 체크하다보면 자연스럽게 역할과 책임을 찾아갈 수 있을 것 같아요.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -1,3 +1,241 @@
 # java-blackjack

 블랙잭 미션 저장소
+
+## 기능 요구 사항
```

</details>

### 인라인 코멘트 2911182157: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-10T11:46:26Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911182157)
- 코드: `src/main/java/domain/Deck.java`, 현재 줄 26, 원래 줄 27
- 소속 리뷰 ID: 3921642743

> 프로그래밍 요구사항에 맞춰 뎁스를 줄여볼까요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,43 @@
+package domain;
+
+import domain.card.Card;
+import domain.card.Rank;
+import domain.card.Suit;
+import java.util.ArrayList;
+import java.util.Collections;
+import java.util.List;
+
+public class Deck {
+    private final List<Card> cards;
+
+    private Deck(List<Card> cards) {
+        this.cards = cards;
+    }
+
+    public static Deck create() {
+        List<Card> cards = new ArrayList<>();
+
+        for (Suit suit : Suit.values()) {
+            for (Rank cardNumber : Rank.values()) {
+                cards.add(new Card(suit, cardNumber));
+            }
+        }
+
+        return new Deck(cards);
+    }
```

</details>

### 인라인 코멘트 2911184616: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-10T11:46:52Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911184616)
- 코드: `src/main/java/domain/Deck.java`, 현재 줄 None, 원래 줄 38
- 소속 리뷰 ID: 3921642743

> `shuffle`과 같이 제어할 순 없는 영역은 어떻게 검증할 수 있을까요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,43 @@
+package domain;
+
+import domain.card.Card;
+import domain.card.Rank;
+import domain.card.Suit;
+import java.util.ArrayList;
+import java.util.Collections;
+import java.util.List;
+
+public class Deck {
+    private final List<Card> cards;
+
+    private Deck(List<Card> cards) {
+        this.cards = cards;
+    }
+
+    public static Deck create() {
+        List<Card> cards = new ArrayList<>();
+
+        for (Suit suit : Suit.values()) {
+            for (Rank cardNumber : Rank.values()) {
+                cards.add(new Card(suit, cardNumber));
+            }
+        }
+
+        return new Deck(cards);
+    }
+
+    public Card pop() {
+        Card card = cards.getLast();
+        cards.removeLast();
+
+        return card;
+    }
+
+    public void shuffle() {
+        Collections.shuffle(this.cards);
+    }
```

</details>

### 인라인 코멘트 2911193229: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-10T11:48:26Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911193229)
- 코드: `src/main/java/domain/participant/Participant.java`, 현재 줄 55, 원래 줄 46
- 소속 리뷰 ID: 3921642743

> Equals, HashCode를 재정의하였네요! 어떠한 경우 활용하게 되나요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,47 @@
+package domain.participant;
+
+import domain.card.Card;
+import domain.card.CardDto;
+import java.util.Objects;
+
+public abstract class Participant {
+    private final Name name;
+    private final Hand hand;
+
+    protected Participant(Name name) {
+        this.hand = new Hand();
+        this.name = name;
+    }
+
+    public void addCard(Card card) {
+        hand.add(card);
+    }
+
+    public CardDto handInfo() {
+        return hand.snapshot();
+    }
+
+    public String getName() {
+        return name.value();
+    }
+
+    public int getScore() {
+        return hand.calculateScore();
+    }
+
+    public abstract boolean canReceive();
+
+    @Override
+    public boolean equals(Object o) {
+        if (o == null || getClass() != o.getClass()) {
+            return false;
+        }
+        Participant participant = (Participant) o;
+        return Objects.equals(name, participant.name);
+    }
+
+    @Override
+    public int hashCode() {
+        return Objects.hash(name);
+    }
```

</details>

### 인라인 코멘트 2911202329: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-10T11:49:51Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911202329)
- 코드: `README.md`, 현재 줄 192, 원래 줄 192
- 소속 리뷰 ID: 3921642743

> 이러한 기준을 통해 생성자를 사용하거나 정적 메서드를 사용하는 방향으로 정해지나요?

<details>
<summary>당시 코드 문맥</summary>

````diff
@@ -1,3 +1,241 @@
 # java-blackjack

 블랙잭 미션 저장소
+
+## 기능 요구 사항
+
+#### 플레이어 이름 입력 기능
+
+- [x] 안내 메세지 출력 후 참여할 플레이어 이름들을 입력을 받는다
+    - [x] 널값이나 빈 공백 예외처리
+    - [x] 쉼표 기준으로 입력 분리
+
+- Player
+  - Name
+    - [x] 이름이 공백이면 예외처리
+    - [x] 이름이 10글자 이상이면 예외처리
+  - Hand
+    - [x] 보유한 카드의 점수 총합을 계산한다.
+      - [x] 카드의 숫자 계산은 카드 숫자를 기본으로 한다.
+      - [x] Ace는 1 또는 11로 계산한다.
+      - [x] J, Q, K는 각각 10으로 계산한다.
+
+- Players
+  - [x] 중복된 닉네임은 예외처리
+  - [x] 플레이어 이름이 7개 초과시 예외처리
+
+- Dealer
+  - [x] 딜러의 닉네임은 "딜러"를 사용한다.
+
+- GameManager
+    - [x] 딜러와 각 플레이어에게 두 장씩 카드를 지급한다.
+      - [x] 딜러에게 2장 나눠준다
+      - [x] 전체 플레이어에게 2장 나눠준다
+        - [x] 플레이어에게 2장 나눠준다
+
+#### 게임 진행
+
+- [x] 게임 시작 준비
+    - [x] 카드 덱을 만든다.
+        - [x] 카드덱은 52개의 카드로 구성된다.
+    - [x] 카드덱은 무작위의 순서를 가진다.
+    - [x] 딜러와 각 플레이어는 두 장의 카드를 지급받는다.
+    - [x] 카드 배정 결과 출력
+
+- [x] 참가자는 추가 카드 지급을 결정한다.
+- [x] 모든 플레이어 턴 진행
+  - [x] 플레이어의 핸드가 버스트인지 검사한다.
+  - 버스트가 아니라면
+    - [x] 카드를 추가로 지급받을지 안내메세지를 추력하고 y/n 입력
+      - [x] y이면 카드를 추가로 제공하고 결과를 출력한다
+      - [x] n이면 플레이어 턴을 종료하고 다음 플레이어 턴을 진행한다
+  - 버스트라면
+    - [x] 다음 플레이어 턴을 진행한다.
+
+- [x] 딜러 턴 진행
+  - [x] 딜러의 핸드가 16점 초과인지 검사한다.
+  - 16점을 넘지 않는다면
+    - [x] 딜러에게 카드 한장을 지급한다.
+
+- [x] 딜러 차례
+    - [x] 딜러 핸즈 총합이 16이하일 때
+        - [x] 딜러에게 카드 한 장 deal
+- [x] 게임 결과 출력 기능
+- [x] 결과 판정
+  - [x] 플레이어의 점수가 21점이 넘으면 패배, 심판 승리
+  - [x] 플레이어의 점수가 21점이 넘지 않는다.
+    - [x] 딜러의 점수가 21점이 넘는다 -> 플레이어 승리, 딜러 패배
+    - [x] 딜러의 점수가 21점이하이다
+      - [x] 21점과의 차이값을 서로 비교 판정
+- [x] 최종 승패 출력 기능
+
+```
+실행 결과
+게임에 참여할 사람의 이름을 입력하세요.(쉼표 기준으로 분리)
+pobi,jason
+
+딜러와 pobi, jason에게 2장을 나누었습니다.
+딜러카드: 3다이아몬드
+pobi카드: 2하트, 8스페이드
+jason카드: 7클로버, K스페이드
+
+pobi는 한장의 카드를 더 받겠습니까?(예는 y, 아니오는 n)
+y
+pobi카드: 2하트, 8스페이드, A클로버
+pobi는 한장의 카드를 더 받겠습니까?(예는 y, 아니오는 n)
+n
+jason는 한장의 카드를 더 받겠습니까?(예는 y, 아니오는 n)
+n
+jason카드: 7클로버, K스페이드
+
+딜러는 16이하라 한장의 카드를 더 받았습니다.
+
+딜러카드: 3다이아몬드, 9클로버, 8다이아몬드 - 결과: 20
+pobi카드: 2하트, 8스페이드, A클로버 - 결과: 21
+jason카드: 7클로버, K스페이드 - 결과: 17
+
+## 최종 승패
+딜러: 1승 1패
+pobi: 승
+jason: 패
+```
+## 미션 중 기록
+
+### 규칙을 적용해서 변경한 코드 1곳 이상
+
+적용한 규칙: 테스트 단위 기준 규칙
+- If-Then
+  - 비즈니스 요구사항에 따라 도메인의 행위(Behavior)가 정의되면, 해당 행위의 완결성을 기준으로 테스트 단위를 작성한다.
+- 테스트 작성 순서
+  1. **Red:** 구현 코드 없이, 오직 요구사항(행위)을 검증하는 **실패하는 테스트**를 먼저 작성한다.
+  2. **Green:** 테스트를 통과시키기 위해 **가장 빠르고 단순하게** 코드를 구현한다.
+  3. **Refactor:** 테스트가 성공한 상태를 유지하면서, **중복을 제거하고 가독성을 높이는** 리팩터링을 진행한다.
+- 금지
+  - DB나 네트워크 같은 외부 환경에 직접 연결하지 않는다.
+
+
+- Name
+  - [x] 이름이 공백이면 예외처리
+  - [x] 이름이 10글자 이상이면 예외처리
+
+- Hand
+  - [x] 보유한 카드의 점수 총합을 계산한다.
+  - [x] 카드의 숫자 계산은 카드 숫자를 기본으로 한다.
+  - [x] Ace는 1 또는 11로 계산한다.
+  - [x] J, Q, K는 각각 10으로 계산한다.
+
+- Players
+  - [x] 중복된 닉네임은 예외처리
+  - [x] 플레이어 이름이 7개 초과시 예외처리
+
+- Deck
+  - [x] 카드덱은 52개의 카드로 구성된다
+  - [x] 카드덱은 무작위의 순서를 가진다
+
+- GameManager
+  - [x] 딜러와 각 플레이어에게 두 장씩 카드를 지급한다.
+    - [x] 딜러에게 2장 나눠준다
+    - [x] 전체 플레이어에게 2장 나눠준다
+      - [x] 플레이어에게 2장 나눠준다
+- Participant
+  - [x] 추가 카드 지급 여부를 결정한다
+
+초기에 입출력 결과를 보면서 시나리오 순서대로 기능 목록을 작성을 했습니다.
+해당 기능 목록을 테스트를 먼저 작성을 했습니다.
+그 과정에서 새롭게 도출되는 도메인과 기능들이 보였습니다.
+그런 경우 리드미에 정리를 하고 TDD, 레드->그린->리팩터링을 진행했습니다.
+규칙을 진행해보면서 핵심 도메인 객체들을 협력관계를 도출해보고 작은 책임부터 TDD하면 좋겠다는 깨달음을 얻었습니다.
+### 테스트 작성이 어려웠던 코드 1곳 이상
+
+#### 카드덱은 무작위의 순서를 가진다
+
+카드의 일급컬렉션인 Deck에서 getter 사용 없이 가지고 있는 `List<Card>`에 대해서 테스트하고 싶었는데 방법이 떠오르지 않아 `unmodifiableList`를 이용했습니다.
+
+#### 딜러와 각 플레이어에게 두 장씩 카드를 지급한다.
+
+카드를 지급을 하는 것과 받는 것에서의 고민이 있었고 초기에 2장씩 분배하는 것과 이후에 추가 카드 지급과 함께 생각을 하면서 고민이 깊어졌습니다.
+
+2장을 받았는지 확인하는 테스트를 작성할 때도 두 가지 경우로 고민을 했습니다.
+덱에서 카드를 뽑았을 때 리턴 값이 널이 아닌지 확인하고 정상적으로 덱의 사이즈가 줄었는지 확인하는 식으로 테스트를 작성하고 싶었습니다.
+다른 방법으로는 참가자의 핸드에 가지고 있는 카드들의 숫자를 체크하는 의견이 나왔고 해당 방법으로 진행하게 되면서 도메인에서 불필요한 책임이 섞이게 됐다는 생각을 하게 됐습니다.
+
+#### 추가 카드 지급 여부를 결정한다
+
+참가자에서 추상 메서드 `canReceive()`를 작성하고 상속받는 서브클래스인 Player, Dealer에서 구현을 진행했습니다.
+게임매니저가 덱을 가지고 카드를 지급하도록 진행했었습니다.
+또한 핸드는 플레이어 생성 시 비어있도록 했습니다.
+덱에서 랜덤한 결과가 나와서 어떻게 진행할까 하는 와중에 우선 셔플 기능을 분리했었었고 그로 인해 예측할 수 있는 순서로 Deck을 다룰 수 있어서 그것을 기반으로 `canReceive()` 메서드를 테스트할 수 있었지만 원하는대로 카드를 뽑을 수 있도록 하는 것이 더 좋은 방법이라고 생각이 들었습니다.
+
+### 막힌 순간 1회 이상
+
+#### 기능 목록 작성 과정
+
+기능 목록을 처음에 작성하는 과정에서 구체적인 사항을 드러나지 않도록 작성하는 것이 좋겠다고 생각했고 그렇게 접근했다가 설계가 부족한 부분이 많은 것을 느끼게 되면서 막히는 경험을 했습니다.
+
+핵심 도메인 규칙이라고 생각되면 테스트해서 규칙을 보장해야한다고 생각했습니다.
+라이브러리의 `shuffle`과 같은 메서드 사용 시 테스트를 작성할 필요가 없다는 주장을 만났습니다.
+그 과정에서 고민이 있었고 `shuffle`과 같은 구현은 바뀔 수 있다고 판단했습니다.
+하지만 핵심 도메인 규칙은 항상 지켜져야 된다고 생각했고 결과적으로 카드덱은 무작위 순서를 가진다를 테스트해야한다고 강하게 주장하게 됐습니다.
+
+이처럼 테스트를 해야하는 것과 하지말 것에 대해서 결정에 혼란이 있었고 그 과정에서 기능 목록 작성이 힘들었습니다.
+또한 블랙잭 도메인에 대한 이해가 부족한 상태도 문제였던 것 같습니다.
+차라리 충분한 시간을 게임을 직접해보고 인터넷이나 동료 등 충분한 조사를 하고 해당 도메인에 대한 이해를 높이고 진행했으면 네이밍이나 도메인 도출 등 수월했겠다고 느꼈습니다.
+
+#### 정적 메서드 사용
+
+정적 메서드 사용에 대해서 다른 의견을 경험하면서 막히는 경험을 했습니다.
+정적 메서드를 사용한다면 사용하는 근거가 무엇인지 페어의 질문에서 당황을 했습니다.
+그러면서 생각을 정리했습니다.
+1. 메서드명으로 의도를 표현할 수 있다.
+2. 상수를 이용하는 등 캐싱으로 효율을 증가시킬 수 있다.
+3. 서브 타입, 다양한 구현체를 반환할 수 있다.
+   세가지로 정리를 했고 세가지 이유에 속하지 않는 경우에는 정적메서드보다 생성자를 사용하고싶다는 생각이 커졌습니다.
````

</details>

### 리뷰 본문 3921642743: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-10T11:56:38Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#pullrequestreview-3921642743)
- 리뷰 상태: `CHANGES_REQUESTED`

> 안녕하세요 고래~ 블랙잭 리뷰를 맡은 매트입니다!
>
> 질문 주신 부분을 포함하여 간단히 코멘트 남겼습니다. 확인해주시고 놓친 부분 있다면 편하게 디엠 혹은 코멘트 남겨주세요!
>
> ---
>
> 아래는 코드 레벨에서 남기기 어려운 부분이라 따로 정리하였어요.
>
> > 가독성이 중요하다고 생각합니다, 부족한 부분이 많은데 가독성이 부족한 부분들에 대해서 알고싶습니다.
>
> > 이름을 짓는 것이 너무 어려운데 좋은 방법은 많은 코드를 보는 것이라 생각하는데 다른 좋은 방법이 있다면 알고 싶습니다.
>
> 가독성이 좋다는 건 결국 누구나 읽기 쉽고 해석하기 용이한 형태를 말하는 거겠죠? 가장 기본적으로 고려해볼 수 있는 건 이미 수년 동안 특정 언어를 여러 사람이 사용해오며 정리된 컨벤션을 따르는 것 같아요. 이를 통해 축적된 노하우를 배울 수 있을 뿐만 아니라 코드의 일관성 자체를 달성할 수 있으니까요. 그 밖에는 다른 사람이 작성한 코드를 직접 읽어보며 잘 읽히는 코드나 패턴을 기억해두는 등 여러 방식을 통해 보완할 수 있을 것 같아요!
>
> 이름 짓는 것 또한 비슷한 맥락으로 통할 것 같아요. 저는 보통 프레임워크나 여러 사람이 기여한 라이브러리를 살펴보며 적절한 네이밍 방식을 참고하기도 합니다.
>
> > 낮은 결합도와 높은 응집도를 가지고 싶은데 구체적인 방법과 경험을 많이 쌓고싶습니다.
>
> 왜 낮은 결합도와 높은 응집도가 필요할까요? 먼저 고래가 이러한 방법과 경험을 가지고 싶다고 했는데 달성하지 못했을 때 어떤 단점을 느끼셨나요?

### 인라인 코멘트 2916540457: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-03-11T07:50:57Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2916540457)
- 코드: `.github/pull_request_template.md`, 현재 줄 16, 원래 줄 16
- 답변 대상: [코멘트 2911055280](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911055280)
- 소속 리뷰 ID: 3927582328

> `pull_request_template.md`의 존재 이유를 깊이 고민해보지 못했습니다.
> 위 파일 자체에 제 개인적인 질문을 담는 것이 파일의 목적(양식 제공)에 어긋난다는 점을 깨달았습니다.
>
> 또한 이 PR 본문은 제 코드를 마주할 리뷰어에 대한 '배려를 담는 그릇'이라는 점을 깨달았습니다.
>
> 단순한 기록을 넘어, 이번 작업의 핵심 요약과 구체적인 변경 사항, 그리고 제가 중요하게 고민했던 설계 포인트를 명확히 전달하여 리뷰어의 시간을 아끼고 깊이 있는 소통을 하기 위한 도구임을 배웠습니다.
>
> 앞으로는 작성해주신 템플릿의 의도를 정확히 파악하여, 제 고민의 궤적을 쉽게 따라오실 수 있도록 작성하겠습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -9,29 +9,30 @@

 ## 체크 리스트

-- [ ] 미션의 필수 요구사항을 모두 구현했나요?
-- [ ] Gradle `test`를 실행했을 때, 모든 테스트가 정상적으로 통과했나요?
-- [ ] 애플리케이션이 정상적으로 실행되나요?
-- [ ] [프롤로그](https://prolog.techcourse.co.kr)에 셀프 체크를 작성했나요?
-  - <!-- 작성한 셀프 체크의 링크를 남겨주세요. -->
+- [x] 미션의 필수 요구사항을 모두 구현했나요?
+- [x] Gradle `test`를 실행했을 때, 모든 테스트가 정상적으로 통과했나요?
+- [x] 애플리케이션이 정상적으로 실행되나요?

+## 어떤 부분에 집중하여 리뷰해야 할까요?
```

</details>

### 인라인 코멘트 2916592862: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-03-11T08:02:46Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2916592862)
- 코드: `src/main/java/domain/card/Card.java`, 현재 줄 None, 원래 줄 16
- 답변 대상: [코멘트 2911066626](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911066626)
- 소속 리뷰 ID: 3927582328

> 저는 record를 사용할 때 가지고 있는 값 자체가 그 객체를 표현하는가에 대해서 생각을 해봅니다.
> '같은 무늬, 같은 숫자를 가지고 있을 때 같은 카드인가?'에 대해서 생각해봤고 그런 경우에 같은 카드가 맞다라는 판단이 들었기 때문에 record를 사용했습니다.
>
> 제가 알고 있었던 record의 특성은 아래와 같습니다.
> 가지고 있는 상태를 변경 불가능한 불변 객체입니다. 그 이유는 필드가 암시적으로 `final`로 선언되기 때문입니다.
> 가지고 있는 필드에 대한 행동을 가질 수 있습니다. 그로 인해 유효성을 보장하는 등 활용을 할 수 있습니다.
> 보일러플레이트 제거 효과로 코드의 간결성을 가질 수 있습니다. `equals, hashcode, getter, toString`을 컴파일러가 필드 기반으로 자동으로 생성해줍니다.
>
> 추가적으로 공부를 하면서 알게 된 점이 있습니다. 저는 컬렉션은 필드로 가지지 못하는 줄 알았습니다. 하지만 그저 얕은 불변성만 제공하는 것을 알게 되었습니다.
> 그렇기 때문에 record에서 컬렉션을 안전하게 다루려면 아래의 코드처럼 처리 해야 한다는 점을 알게 되었습니다.
>
> ```
> public record Hand(List<Card> cards) {
>     public Hand {
>         // 생성 시점에 읽기 전용 리스트로 변환하여 저장
>         cards = List.copyOf(cards);
>     }
> }
> ```
>
> 또한 record에서 사용하는 정확한 용어에 대해서도 추가적으로 알게 됐습니다.
> - Getter -> Accessor
> - 상태 -> 컴포넌트
> - 생성자 -> 컴팩트 생성^[자

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,16 @@
+package domain.card;
+
+public record Card(Suit suit, Rank cardNumber) {
+    public boolean isAce() {
+        return this.cardNumber == Rank.ACE;
+    }
+
+    public String suitValue() {
+        return this.suit.getValue();
+    }
+
+    public String symbol() {
+        return this.cardNumber.getSymbol();
+    }
+
+}
```

</details>

### 인라인 코멘트 2916597417: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-03-11T08:03:50Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2916597417)
- 코드: `src/main/java/domain/card/CardDto.java`, 현재 줄 None, 원래 줄 21
- 답변 대상: [코멘트 2911065029](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911065029)
- 소속 리뷰 ID: 3927582328

> 제가 생각하는 dto는 순수한 데이터 전달 객체라고 생각합니다.
> 목적은 핵심 객체가 자율적으로 존재할 수 있도록 캡슐화를 지켜주어 변경이 생겼을 때 정보를 제공한 객체와의 의존성이 생기지 않도록 하는 것이 목적이라고 생각합니다.
> 그렇기 때문에 필드로는 원시타입 사용을 지향하며 로직을 가지지 않는 순수한 데이터 전달에 집중해야 한다고 생각합니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,21 @@
+package domain.card;
+
+import java.util.ArrayList;
+import java.util.List;
+
+public record CardDto(List<Card> cards) {
+
+    public String getFormattedCards() {
+        List<String> cardsResult = new ArrayList<>();
+        for (Card card : cards) {
+            String suit = card.suitValue();
+            String rank = card.symbol();
+            cardsResult.add(rank + suit);
+        }
+        return String.join(", ", cardsResult);
+    }
+
+    public int size() {
+        return cards().size();
+    }
+}
```

</details>

### 인라인 코멘트 2916607225: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-03-11T08:05:49Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2916607225)
- 코드: `src/main/java/domain/card/Rank.java`, 현재 줄 None, 원래 줄 16
- 답변 대상: [코멘트 2911098115](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911098115)
- 소속 리뷰 ID: 3927582328

> 장점으로는 빠른 구현이 편리하다는 점인 것 같습니다.
> 이번 블랙잭 미션을 하면서 해당 도메인이 어디에 있는지 세부사항들을 알고 있어 바로바로 고치고 추가하는 것이 편한 것 같은데 시스템이 커지거나 세부사항을 모르는 경우에는 뷰에 변경이 있을 때 뷰를 먼저 들여다 볼 것으로 예상되는데 그러한 경우에서 도메인까지 수정이 필요하다면 불편할 것 같습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,34 @@
+package domain.card;
+
+public enum Rank {
+    TWO(2, "2"),
+    THREE(3, "3"),
+    FOUR(4, "4"),
+    FIVE(5, "5"),
+    SIX(6, "6"),
+    SEVEN(7, "7"),
+    EIGHT(8, "8"),
+    NINE(9, "9"),
+    TEN(10, "10"),
+    JACK(10, "J"),
+    QUEEN(10, "Q"),
+    KING(10, "K"),
+    ACE(11, "A"),
```

</details>

### 인라인 코멘트 2916671036: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-03-11T08:19:39Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2916671036)
- 코드: `src/main/java/domain/participant/Participant.java`, 현재 줄 15, 원래 줄 14
- 답변 대상: [코멘트 2911111982](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911111982)
- 소속 리뷰 ID: 3927582328

> `private`가 지향하는 목적은 내부 구현의 은닉이라고 생각합니다.
> 상태는 숨기고 행위를 보여주면서 How를 숨기고 What에 집중할 수 있게 하여 구현의 변경이 자유로워지는 장점이 있다고 생각합니다.
> 노출에 관해서는 어떤 자료구조를 사용하는가에 대해서도 모르는 것이 좋다고 느꼈습니다.
> 가지고 있는 상태의 자료구조도 변할 수 있기 때문입니다.
> `protected`를 사용하게 되면 직접 슈퍼클래스의 상태를 다룰 수 있게 되면서 구현에 대한 강한 결합이 생길 것으로 예상되어 원하는 가시성을 얻기 힘들다고 생각합니다.
> 그렇기 때문에 서브 클래스가 원하는 것이 있을 때 행위인 메서드를 통해서 얻도록 하는 것이 좋다고 생각하게 됐습니다.
>

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,47 @@
+package domain.participant;
+
+import domain.card.Card;
+import domain.card.CardDto;
+import java.util.Objects;
+
+public abstract class Participant {
+    private final Name name;
+    private final Hand hand;
+
+    protected Participant(Name name) {
+        this.hand = new Hand();
+        this.name = name;
+    }
```

</details>

### 인라인 코멘트 2916738213: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-03-11T08:33:55Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2916738213)
- 코드: `src/main/java/domain/participant/Participant.java`, 현재 줄 55, 원래 줄 46
- 답변 대상: [코멘트 2911193229](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911193229)
- 소속 리뷰 ID: 3927582328

> 동일한 이름을 가진 플레이어가 중복으로 존재하지 않도록 하기 위해 재정의했습니다.
>
> `equals`를 통해 객체의 주소값이 다르더라도 이름이 같다면 논리적으로 같은 객체임을 정의했고, 이와 쌍을 이루는 `hashCode`를 함께 수정하여 해시 기반 컬렉션에서도 이 동등성이 유지되도록 했습니다.
>
> 이를 활용하면 `HashSet`이나 `HashMap` 같은 자료구조를 사용할 때 의도한 대로 중복을 자동으로 걸러낼 수 있습니다. 또한 단위 테스트에서 `isEqualTo`를 사용할 때 객체의 내부 필드를 하나하나 비교하지 않고도 객체 자체로 동등성을 검증할 수 있습니다.
>

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,47 @@
+package domain.participant;
+
+import domain.card.Card;
+import domain.card.CardDto;
+import java.util.Objects;
+
+public abstract class Participant {
+    private final Name name;
+    private final Hand hand;
+
+    protected Participant(Name name) {
+        this.hand = new Hand();
+        this.name = name;
+    }
+
+    public void addCard(Card card) {
+        hand.add(card);
+    }
+
+    public CardDto handInfo() {
+        return hand.snapshot();
+    }
+
+    public String getName() {
+        return name.value();
+    }
+
+    public int getScore() {
+        return hand.calculateScore();
+    }
+
+    public abstract boolean canReceive();
+
+    @Override
+    public boolean equals(Object o) {
+        if (o == null || getClass() != o.getClass()) {
+            return false;
+        }
+        Participant participant = (Participant) o;
+        return Objects.equals(name, participant.name);
+    }
+
+    @Override
+    public int hashCode() {
+        return Objects.hash(name);
+    }
```

</details>

### 인라인 코멘트 2916822886: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-03-11T08:51:10Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2916822886)
- 코드: `src/main/java/domain/participant/Players.java`, 현재 줄 8, 원래 줄 8
- 답변 대상: [코멘트 2911083181](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911083181)
- 소속 리뷰 ID: 3927582328

> 제가 생각하는 일급컬렉션은 동일한 객체들의 모은 컬렉션과 관련된 비즈니스 로직을 응집도 있게 모아주고 캡슐화를 해주기 때문에 필요하다고 생각합니다.
>
> `Iterable` 인터페이스를 구현하고자 판단한 기준은 각 플레이어마다 사용자 입력을 받은 후 그 입력에 따른 처리를 해야하는데 일급컬렉션에게 위임을 하면 일급컬렉션 내에서 뷰와의 의존이 생길 것으로 생각해서 밖에서 순회할 수 있도록 했습니다.
>
> 대답을 하면서 든 생각은 노출된 `player`를 통해서 의도치 않은 동작이 발생할 수 없도록 할 수 있다면 `Iterable`을 사용해도 괜찮을 것 같다는 생각이 들었습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,51 @@
+package domain.participant;
+
+import java.util.HashSet;
+import java.util.Iterator;
+import java.util.List;
+import java.util.Set;
+
+public class Players implements Iterable<Player> {
```

</details>

### 인라인 코멘트 2916936299: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-03-11T09:13:00Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2916936299)
- 코드: `src/main/java/domain/participant/Players.java`, 현재 줄 None, 원래 줄 16
- 답변 대상: [코멘트 2911086373](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911086373)
- 소속 리뷰 ID: 3927582328

> `final`만으로는 참조에 대한 불변만 보장되는데 만약에 `copyOf` 없이 생성자를 통해 받을 수 있다면 외부의 `players` 인스턴스에 참조로 인해 내부가 의도치 않은 변경이 있을 수 있다고 생각합니다.
> 그리고 `copyOf`를 사용하게 되면 컬렉션의 구조에 대해서도 불변이 보장 되어서 내/외부의 의도치 않은 조작으로부터 예방할 수 있다고 생각합니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,51 @@
+package domain.participant;
+
+import java.util.HashSet;
+import java.util.Iterator;
+import java.util.List;
+import java.util.Set;
+
+public class Players implements Iterable<Player> {
+    private static final String ERROR_DUPLICATE_NAME = "플레이어 이름은 중복될 수 없습니다.";
+    private static final String ERROR_PLAYER_COUNT = "참가할 플레이어의 수는 최대 7명입니다.";
+    private static final int MAX_PLAYER_COUNT = 7;
+    private final List<Player> players;
+
+    private Players(List<Player> players) {
+        this.players = List.copyOf(players);
+    }
```

</details>

### 인라인 코멘트 2916979814: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-03-11T09:20:05Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2916979814)
- 코드: `src/main/java/domain/participant/Players.java`, 현재 줄 None, 원래 줄 21
- 답변 대상: [코멘트 2911089231](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911089231)
- 소속 리뷰 ID: 3927582328

> 객체의 생성 의도를 표현할 수 있다고 생각합니다. 다만 저는 여러 파라미터에서 Players가 생성되는 경우에 사용하려 했을 것 같습니다. 이 경우에는 생성자로 생성하는 것이 괜찮다고 생각합니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,51 @@
+package domain.participant;
+
+import java.util.HashSet;
+import java.util.Iterator;
+import java.util.List;
+import java.util.Set;
+
+public class Players implements Iterable<Player> {
+    private static final String ERROR_DUPLICATE_NAME = "플레이어 이름은 중복될 수 없습니다.";
+    private static final String ERROR_PLAYER_COUNT = "참가할 플레이어의 수는 최대 7명입니다.";
+    private static final int MAX_PLAYER_COUNT = 7;
+    private final List<Player> players;
+
+    private Players(List<Player> players) {
+        this.players = List.copyOf(players);
+    }
+
+    public static Players of(List<Player> players) {
+        validate(players);
+        return new Players(players);
+    }
```

</details>

### 인라인 코멘트 2917194226: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-03-11T09:53:47Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2917194226)
- 코드: `src/main/java/domain/Deck.java`, 현재 줄 None, 원래 줄 38
- 답변 대상: [코멘트 2911184616](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911184616)
- 소속 리뷰 ID: 3927582328

> 전략 패턴과 함수형 인터페이스를 활용해 셔플 로직을 외부에서 주입받도록 개선했습니다. 이를 통해 무작위성이라는 제어할 수 없는 영역을 통제하여, 테스트 환경에서 원하는 시나리오를 자유롭게 재현하고 검증할 수 있게 되었습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,43 @@
+package domain;
+
+import domain.card.Card;
+import domain.card.Rank;
+import domain.card.Suit;
+import java.util.ArrayList;
+import java.util.Collections;
+import java.util.List;
+
+public class Deck {
+    private final List<Card> cards;
+
+    private Deck(List<Card> cards) {
+        this.cards = cards;
+    }
+
+    public static Deck create() {
+        List<Card> cards = new ArrayList<>();
+
+        for (Suit suit : Suit.values()) {
+            for (Rank cardNumber : Rank.values()) {
+                cards.add(new Card(suit, cardNumber));
+            }
+        }
+
+        return new Deck(cards);
+    }
+
+    public Card pop() {
+        Card card = cards.getLast();
+        cards.removeLast();
+
+        return card;
+    }
+
+    public void shuffle() {
+        Collections.shuffle(this.cards);
+    }
```

</details>

### 인라인 코멘트 2917262543: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-03-11T10:05:16Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2917262543)
- 코드: `src/test/java/domain/participant/HandTest.java`, 현재 줄 15, 원래 줄 15
- 답변 대상: [코멘트 2911126767](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911126767)
- 소속 리뷰 ID: 3927582328

> 제가 생각한 애플리케이션 단위는 입출력예시, 하나의 유스케이스라고 볼 수 있을 것 같습니다.
> 다시 말해 절차적인 제공한 입출력 예시, 다르게 표현하자면 유스케이스를 테스트하고 싶었습니다.
> 사용자의 입력 -> 처리 -> 출력을 제어해서 런타임환경에서 시나리오대로 입력하는 것이 아닌 테스트 코드로 검증하고 싶었습니다.
>
> 단일 책임에서 도출된 객체간의 협력 메시지, 퍼블릭 인터페이스를 테스트하는 것이 단위테스트라고 생각됩니다.
> 즉, 외부 의존성을 제거한 Tell, Don't Ask에서 말하는 Tell을 테스트하는 것이 아닐까 싶습니다.
>
> 통합테스트는 현재 프로그램, 프로세스 이외의 다른 프로세스와의 협력까지 함께 테스트하는 것으로 생각합니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,115 @@
+package domain.participant;
+
+import static org.assertj.core.api.Assertions.assertThat;
+
+import domain.card.Card;
+import domain.card.Rank;
+import domain.card.Suit;
+import java.util.List;
+import java.util.stream.Stream;
+import org.junit.jupiter.api.Test;
+import org.junit.jupiter.params.ParameterizedTest;
+import org.junit.jupiter.params.provider.Arguments;
+import org.junit.jupiter.params.provider.MethodSource;
+
+public class HandTest {
```

</details>

### 인라인 코멘트 2917269709: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-03-11T10:06:42Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2917269709)
- 코드: `README.md`, 현재 줄 5, 원래 줄 5
- 답변 대상: [코멘트 2911168886](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911168886)
- 소속 리뷰 ID: 3927582328

> 감사합니다. 작은 단위의 시나리오를 생각하고 의존성이 가장 없어 보이는 작은 객체부터 TDD 해보자는 생각을 덕분에 할 수 있게 된 것 같습니다!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -1,3 +1,241 @@
 # java-blackjack

 블랙잭 미션 저장소
+
+## 기능 요구 사항
```

</details>

### 인라인 코멘트 2917295057: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-03-11T10:11:35Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2917295057)
- 코드: `README.md`, 현재 줄 192, 원래 줄 192
- 답변 대상: [코멘트 2911202329](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911202329)
- 소속 리뷰 ID: 3927582328

> 네 이러한 기준으로 적용을 고려하기로 개인적으로 생각을 정리했습니다.
> 특히 현재는 1번에서 말한 생성의 의도를 표현에 대해서 가장 큰 비중을 가지고 있습니다.
> 2, 3번은 현재까지 경험을 해본 적이 없는데 이번 페어의 질문을 통해 검색을 통해 알게 됐는데 적절한 상황을 인지할 수 있는지는 아직 큰 자신은 없습니다 🥹

<details>
<summary>당시 코드 문맥</summary>

````diff
@@ -1,3 +1,241 @@
 # java-blackjack

 블랙잭 미션 저장소
+
+## 기능 요구 사항
+
+#### 플레이어 이름 입력 기능
+
+- [x] 안내 메세지 출력 후 참여할 플레이어 이름들을 입력을 받는다
+    - [x] 널값이나 빈 공백 예외처리
+    - [x] 쉼표 기준으로 입력 분리
+
+- Player
+  - Name
+    - [x] 이름이 공백이면 예외처리
+    - [x] 이름이 10글자 이상이면 예외처리
+  - Hand
+    - [x] 보유한 카드의 점수 총합을 계산한다.
+      - [x] 카드의 숫자 계산은 카드 숫자를 기본으로 한다.
+      - [x] Ace는 1 또는 11로 계산한다.
+      - [x] J, Q, K는 각각 10으로 계산한다.
+
+- Players
+  - [x] 중복된 닉네임은 예외처리
+  - [x] 플레이어 이름이 7개 초과시 예외처리
+
+- Dealer
+  - [x] 딜러의 닉네임은 "딜러"를 사용한다.
+
+- GameManager
+    - [x] 딜러와 각 플레이어에게 두 장씩 카드를 지급한다.
+      - [x] 딜러에게 2장 나눠준다
+      - [x] 전체 플레이어에게 2장 나눠준다
+        - [x] 플레이어에게 2장 나눠준다
+
+#### 게임 진행
+
+- [x] 게임 시작 준비
+    - [x] 카드 덱을 만든다.
+        - [x] 카드덱은 52개의 카드로 구성된다.
+    - [x] 카드덱은 무작위의 순서를 가진다.
+    - [x] 딜러와 각 플레이어는 두 장의 카드를 지급받는다.
+    - [x] 카드 배정 결과 출력
+
+- [x] 참가자는 추가 카드 지급을 결정한다.
+- [x] 모든 플레이어 턴 진행
+  - [x] 플레이어의 핸드가 버스트인지 검사한다.
+  - 버스트가 아니라면
+    - [x] 카드를 추가로 지급받을지 안내메세지를 추력하고 y/n 입력
+      - [x] y이면 카드를 추가로 제공하고 결과를 출력한다
+      - [x] n이면 플레이어 턴을 종료하고 다음 플레이어 턴을 진행한다
+  - 버스트라면
+    - [x] 다음 플레이어 턴을 진행한다.
+
+- [x] 딜러 턴 진행
+  - [x] 딜러의 핸드가 16점 초과인지 검사한다.
+  - 16점을 넘지 않는다면
+    - [x] 딜러에게 카드 한장을 지급한다.
+
+- [x] 딜러 차례
+    - [x] 딜러 핸즈 총합이 16이하일 때
+        - [x] 딜러에게 카드 한 장 deal
+- [x] 게임 결과 출력 기능
+- [x] 결과 판정
+  - [x] 플레이어의 점수가 21점이 넘으면 패배, 심판 승리
+  - [x] 플레이어의 점수가 21점이 넘지 않는다.
+    - [x] 딜러의 점수가 21점이 넘는다 -> 플레이어 승리, 딜러 패배
+    - [x] 딜러의 점수가 21점이하이다
+      - [x] 21점과의 차이값을 서로 비교 판정
+- [x] 최종 승패 출력 기능
+
+```
+실행 결과
+게임에 참여할 사람의 이름을 입력하세요.(쉼표 기준으로 분리)
+pobi,jason
+
+딜러와 pobi, jason에게 2장을 나누었습니다.
+딜러카드: 3다이아몬드
+pobi카드: 2하트, 8스페이드
+jason카드: 7클로버, K스페이드
+
+pobi는 한장의 카드를 더 받겠습니까?(예는 y, 아니오는 n)
+y
+pobi카드: 2하트, 8스페이드, A클로버
+pobi는 한장의 카드를 더 받겠습니까?(예는 y, 아니오는 n)
+n
+jason는 한장의 카드를 더 받겠습니까?(예는 y, 아니오는 n)
+n
+jason카드: 7클로버, K스페이드
+
+딜러는 16이하라 한장의 카드를 더 받았습니다.
+
+딜러카드: 3다이아몬드, 9클로버, 8다이아몬드 - 결과: 20
+pobi카드: 2하트, 8스페이드, A클로버 - 결과: 21
+jason카드: 7클로버, K스페이드 - 결과: 17
+
+## 최종 승패
+딜러: 1승 1패
+pobi: 승
+jason: 패
+```
+## 미션 중 기록
+
+### 규칙을 적용해서 변경한 코드 1곳 이상
+
+적용한 규칙: 테스트 단위 기준 규칙
+- If-Then
+  - 비즈니스 요구사항에 따라 도메인의 행위(Behavior)가 정의되면, 해당 행위의 완결성을 기준으로 테스트 단위를 작성한다.
+- 테스트 작성 순서
+  1. **Red:** 구현 코드 없이, 오직 요구사항(행위)을 검증하는 **실패하는 테스트**를 먼저 작성한다.
+  2. **Green:** 테스트를 통과시키기 위해 **가장 빠르고 단순하게** 코드를 구현한다.
+  3. **Refactor:** 테스트가 성공한 상태를 유지하면서, **중복을 제거하고 가독성을 높이는** 리팩터링을 진행한다.
+- 금지
+  - DB나 네트워크 같은 외부 환경에 직접 연결하지 않는다.
+
+
+- Name
+  - [x] 이름이 공백이면 예외처리
+  - [x] 이름이 10글자 이상이면 예외처리
+
+- Hand
+  - [x] 보유한 카드의 점수 총합을 계산한다.
+  - [x] 카드의 숫자 계산은 카드 숫자를 기본으로 한다.
+  - [x] Ace는 1 또는 11로 계산한다.
+  - [x] J, Q, K는 각각 10으로 계산한다.
+
+- Players
+  - [x] 중복된 닉네임은 예외처리
+  - [x] 플레이어 이름이 7개 초과시 예외처리
+
+- Deck
+  - [x] 카드덱은 52개의 카드로 구성된다
+  - [x] 카드덱은 무작위의 순서를 가진다
+
+- GameManager
+  - [x] 딜러와 각 플레이어에게 두 장씩 카드를 지급한다.
+    - [x] 딜러에게 2장 나눠준다
+    - [x] 전체 플레이어에게 2장 나눠준다
+      - [x] 플레이어에게 2장 나눠준다
+- Participant
+  - [x] 추가 카드 지급 여부를 결정한다
+
+초기에 입출력 결과를 보면서 시나리오 순서대로 기능 목록을 작성을 했습니다.
+해당 기능 목록을 테스트를 먼저 작성을 했습니다.
+그 과정에서 새롭게 도출되는 도메인과 기능들이 보였습니다.
+그런 경우 리드미에 정리를 하고 TDD, 레드->그린->리팩터링을 진행했습니다.
+규칙을 진행해보면서 핵심 도메인 객체들을 협력관계를 도출해보고 작은 책임부터 TDD하면 좋겠다는 깨달음을 얻었습니다.
+### 테스트 작성이 어려웠던 코드 1곳 이상
+
+#### 카드덱은 무작위의 순서를 가진다
+
+카드의 일급컬렉션인 Deck에서 getter 사용 없이 가지고 있는 `List<Card>`에 대해서 테스트하고 싶었는데 방법이 떠오르지 않아 `unmodifiableList`를 이용했습니다.
+
+#### 딜러와 각 플레이어에게 두 장씩 카드를 지급한다.
+
+카드를 지급을 하는 것과 받는 것에서의 고민이 있었고 초기에 2장씩 분배하는 것과 이후에 추가 카드 지급과 함께 생각을 하면서 고민이 깊어졌습니다.
+
+2장을 받았는지 확인하는 테스트를 작성할 때도 두 가지 경우로 고민을 했습니다.
+덱에서 카드를 뽑았을 때 리턴 값이 널이 아닌지 확인하고 정상적으로 덱의 사이즈가 줄었는지 확인하는 식으로 테스트를 작성하고 싶었습니다.
+다른 방법으로는 참가자의 핸드에 가지고 있는 카드들의 숫자를 체크하는 의견이 나왔고 해당 방법으로 진행하게 되면서 도메인에서 불필요한 책임이 섞이게 됐다는 생각을 하게 됐습니다.
+
+#### 추가 카드 지급 여부를 결정한다
+
+참가자에서 추상 메서드 `canReceive()`를 작성하고 상속받는 서브클래스인 Player, Dealer에서 구현을 진행했습니다.
+게임매니저가 덱을 가지고 카드를 지급하도록 진행했었습니다.
+또한 핸드는 플레이어 생성 시 비어있도록 했습니다.
+덱에서 랜덤한 결과가 나와서 어떻게 진행할까 하는 와중에 우선 셔플 기능을 분리했었었고 그로 인해 예측할 수 있는 순서로 Deck을 다룰 수 있어서 그것을 기반으로 `canReceive()` 메서드를 테스트할 수 있었지만 원하는대로 카드를 뽑을 수 있도록 하는 것이 더 좋은 방법이라고 생각이 들었습니다.
+
+### 막힌 순간 1회 이상
+
+#### 기능 목록 작성 과정
+
+기능 목록을 처음에 작성하는 과정에서 구체적인 사항을 드러나지 않도록 작성하는 것이 좋겠다고 생각했고 그렇게 접근했다가 설계가 부족한 부분이 많은 것을 느끼게 되면서 막히는 경험을 했습니다.
+
+핵심 도메인 규칙이라고 생각되면 테스트해서 규칙을 보장해야한다고 생각했습니다.
+라이브러리의 `shuffle`과 같은 메서드 사용 시 테스트를 작성할 필요가 없다는 주장을 만났습니다.
+그 과정에서 고민이 있었고 `shuffle`과 같은 구현은 바뀔 수 있다고 판단했습니다.
+하지만 핵심 도메인 규칙은 항상 지켜져야 된다고 생각했고 결과적으로 카드덱은 무작위 순서를 가진다를 테스트해야한다고 강하게 주장하게 됐습니다.
+
+이처럼 테스트를 해야하는 것과 하지말 것에 대해서 결정에 혼란이 있었고 그 과정에서 기능 목록 작성이 힘들었습니다.
+또한 블랙잭 도메인에 대한 이해가 부족한 상태도 문제였던 것 같습니다.
+차라리 충분한 시간을 게임을 직접해보고 인터넷이나 동료 등 충분한 조사를 하고 해당 도메인에 대한 이해를 높이고 진행했으면 네이밍이나 도메인 도출 등 수월했겠다고 느꼈습니다.
+
+#### 정적 메서드 사용
+
+정적 메서드 사용에 대해서 다른 의견을 경험하면서 막히는 경험을 했습니다.
+정적 메서드를 사용한다면 사용하는 근거가 무엇인지 페어의 질문에서 당황을 했습니다.
+그러면서 생각을 정리했습니다.
+1. 메서드명으로 의도를 표현할 수 있다.
+2. 상수를 이용하는 등 캐싱으로 효율을 증가시킬 수 있다.
+3. 서브 타입, 다양한 구현체를 반환할 수 있다.
+   세가지로 정리를 했고 세가지 이유에 속하지 않는 경우에는 정적메서드보다 생성자를 사용하고싶다는 생각이 커졌습니다.
````

</details>

### 인라인 코멘트 2917322962: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-03-11T10:16:46Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2917322962)
- 코드: `src/main/java/domain/Deck.java`, 현재 줄 26, 원래 줄 27
- 답변 대상: [코멘트 2911182157](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911182157)
- 소속 리뷰 ID: 3927582328

> 처음에는 이중 for문이 가독성이 좋다고 생각을 했는데 제 개인적인 주관이 많이 들어간 것이라 매트의 의견도 궁금합니다.
>
> 요구 사항을 지킬 때 두 가지 방법이 떠올랐습니다.
> 위 처럼 스트림을 이용하는 것과 중첩된 for 문만 메서드 분리하는 것이었습니다.
> flatMap을 이용한 이중 스트림이 한눈에 들어와서 더 가독성이 낫다고 느꼈는데 괜찮을까요?
>
>

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,43 @@
+package domain;
+
+import domain.card.Card;
+import domain.card.Rank;
+import domain.card.Suit;
+import java.util.ArrayList;
+import java.util.Collections;
+import java.util.List;
+
+public class Deck {
+    private final List<Card> cards;
+
+    private Deck(List<Card> cards) {
+        this.cards = cards;
+    }
+
+    public static Deck create() {
+        List<Card> cards = new ArrayList<>();
+
+        for (Suit suit : Suit.values()) {
+            for (Rank cardNumber : Rank.values()) {
+                cards.add(new Card(suit, cardNumber));
+            }
+        }
+
+        return new Deck(cards);
+    }
```

</details>

### 인라인 코멘트 2917344215: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-03-11T10:20:32Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2917344215)
- 코드: `.github/pull_request_template.md`, 현재 줄 16, 원래 줄 16
- 답변 대상: [코멘트 2911055280](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911055280)
- 소속 리뷰 ID: 3927582328

> 한 가지 궁금한 점이 있습니다 매트!
>
> 새롭게 풀리퀘스트를 보냈을 때 PR 본문을 새롭게 수정해도 되는지, 좋은 방법인건지 궁금합니다.
>
> 만약 새롭게 본문을 수정하는 것이 맞는거라면 이번에 변경사항들에 대해서 핵심 요약을 하고 그것들에 대한 근거들을 작성하는 정도면 괜찮을까요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -9,29 +9,30 @@

 ## 체크 리스트

-- [ ] 미션의 필수 요구사항을 모두 구현했나요?
-- [ ] Gradle `test`를 실행했을 때, 모든 테스트가 정상적으로 통과했나요?
-- [ ] 애플리케이션이 정상적으로 실행되나요?
-- [ ] [프롤로그](https://prolog.techcourse.co.kr)에 셀프 체크를 작성했나요?
-  - <!-- 작성한 셀프 체크의 링크를 남겨주세요. -->
+- [x] 미션의 필수 요구사항을 모두 구현했나요?
+- [x] Gradle `test`를 실행했을 때, 모든 테스트가 정상적으로 통과했나요?
+- [x] 애플리케이션이 정상적으로 실행되나요?

+## 어떤 부분에 집중하여 리뷰해야 할까요?
```

</details>

### 리뷰 본문 3927582328: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-03-11T10:31:34Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#pullrequestreview-3927582328)
- 리뷰 상태: `COMMENTED`

> 매트 Summit을 해야한다는 사실을 몰랐습니다.
> 이번에 또 배웠네요, 이곳에 새로 보낼 PR에 대한 내용을 적으면 좋겠다고 판단이 들었습니다!
>
> 이번에 피드백 주신 부분들을 적용하면서 가장 크게 변경된 부분은 dto를 생각해보면서 도메인과 뷰의 의존성을 없애야겠다고 결정한 것입니다.
>
> `Enum` 도메인의 뷰에서 사용하기 위한 필드들을 모두 정리했습니다.
> 사용자 입출력이 변경이 있을 때 `View`를 먼저 확인할 것으로 생각해서 해당 패키지에 `Enum`으로 출력 문자열 연결을 했습니다.
>
> 도메인에서 사용하는 `snapShot()`이나 `toDto()` 등을 제거했습니다.
> 그 이유는 절차적인 비즈니스 로직, 유스케이스가 변경될 때 도메인 외부에서 유스케이스에 따른 데이터 가공을 주도하고 싶다고 생각이 들었기 때문입니다.
> 그래서 `Getter`를 하는데에 있어 불변성을 지킬려고 노력했습니다.
>
> 변수, 메서드명의 가독성을 향상 시키기 위한 변경을 시도했습니다.

### 인라인 코멘트 2918248363: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-11T13:05:50Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2918248363)
- 코드: `src/main/java/domain/card/Card.java`, 현재 줄 None, 원래 줄 16
- 답변 대상: [코멘트 2911066626](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911066626)
- 소속 리뷰 ID: 3929467222

> 제가 생각한 것 보다 더 꼼꼼하게 학습하였네요 👍

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,16 @@
+package domain.card;
+
+public record Card(Suit suit, Rank cardNumber) {
+    public boolean isAce() {
+        return this.cardNumber == Rank.ACE;
+    }
+
+    public String suitValue() {
+        return this.suit.getValue();
+    }
+
+    public String symbol() {
+        return this.cardNumber.getSymbol();
+    }
+
+}
```

</details>

### 리뷰 본문 3929467222: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-11T13:05:50Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#pullrequestreview-3929467222)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 2918254729: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-11T13:07:00Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2918254729)
- 코드: `src/main/java/domain/card/Rank.java`, 현재 줄 None, 원래 줄 16
- 답변 대상: [코멘트 2911098115](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911098115)
- 소속 리뷰 ID: 3929473818

> 넵 두 방향 모두 장단점이 있으니 상황에 맞춰 적절히 선택하면 좋을 것 같아요 ㅎㅎ

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,34 @@
+package domain.card;
+
+public enum Rank {
+    TWO(2, "2"),
+    THREE(3, "3"),
+    FOUR(4, "4"),
+    FIVE(5, "5"),
+    SIX(6, "6"),
+    SEVEN(7, "7"),
+    EIGHT(8, "8"),
+    NINE(9, "9"),
+    TEN(10, "10"),
+    JACK(10, "J"),
+    QUEEN(10, "Q"),
+    KING(10, "K"),
+    ACE(11, "A"),
```

</details>

### 리뷰 본문 3929473818: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-11T13:07:01Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#pullrequestreview-3929473818)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 2918268638: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-11T13:09:38Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2918268638)
- 코드: `.github/pull_request_template.md`, 현재 줄 16, 원래 줄 16
- 답변 대상: [코멘트 2911055280](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911055280)
- 소속 리뷰 ID: 3929489824

> PR  템플릿은 그냥 단순히 가이드를 제공 해줄뿐입니다 ㅎㅎ 고래가 생각 했을 때 추가적인 내용이 필요하다 판단하면 자유롭게 작성해도 괜찮아요.
>
> 다만 코드 관련 질문이라면 코드 베이스에 코멘트를 통해 전달 주시는게 전체적인 맥락을 파악하는데 더 용이할 것 같아요.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -9,29 +9,30 @@

 ## 체크 리스트

-- [ ] 미션의 필수 요구사항을 모두 구현했나요?
-- [ ] Gradle `test`를 실행했을 때, 모든 테스트가 정상적으로 통과했나요?
-- [ ] 애플리케이션이 정상적으로 실행되나요?
-- [ ] [프롤로그](https://prolog.techcourse.co.kr)에 셀프 체크를 작성했나요?
-  - <!-- 작성한 셀프 체크의 링크를 남겨주세요. -->
+- [x] 미션의 필수 요구사항을 모두 구현했나요?
+- [x] Gradle `test`를 실행했을 때, 모든 테스트가 정상적으로 통과했나요?
+- [x] 애플리케이션이 정상적으로 실행되나요?

+## 어떤 부분에 집중하여 리뷰해야 할까요?
```

</details>

### 인라인 코멘트 2918283667: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-11T13:12:24Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2918283667)
- 코드: `src/main/java/domain/participant/Participant.java`, 현재 줄 15, 원래 줄 14
- 답변 대상: [코멘트 2911111982](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911111982)
- 소속 리뷰 ID: 3929489824

> protected는 말씀 주신 것 처럼 강한 결합이 생기는 듯 보이기도 하지만 그렇다고 상속을 완전히 배제할 필욘 없다고 생각해요. 상속이던 조합이던 각각의 맞는 상황에 충분히 활용할 수 있기에 완전 배제하기 보단 직접 사용해보며 느낀 장단점을 기반으로 앞으로의 선택을 진행할 때 양분으로 삼아보면 좋을 것 같아요 ㅎㅎ

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,47 @@
+package domain.participant;
+
+import domain.card.Card;
+import domain.card.CardDto;
+import java.util.Objects;
+
+public abstract class Participant {
+    private final Name name;
+    private final Hand hand;
+
+    protected Participant(Name name) {
+        this.hand = new Hand();
+        this.name = name;
+    }
```

</details>

### 인라인 코멘트 2918335615: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-11T13:21:35Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2918335615)
- 코드: `src/main/java/domain/participant/Players.java`, 현재 줄 8, 원래 줄 8
- 답변 대상: [코멘트 2911083181](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911083181)
- 소속 리뷰 ID: 3929489824

> 네 좋습니다. Iterable 내에서 제공하는 스펙이 필요하다면 사용해도 좋을 것 같아요. 다만 한 가지 추가적으로 고려해야 할 부분은 인터페이스를 구현한다는 건 해당 인터페이스에서 명시한 스펙을 따라야 한다는 것을 의미하기도 해요. 가령 Iterable을 메서드 파라미터로 사용하는 메서드가 있다고 가정해볼게요. 만약 고래가 override한 함수가 의도와 다르게 구현되었다면 파라미터로 전달된 메서드는 정상적으로 처리가 되었음을 보장할 수 있을까요? 이런 부분들을 까지 잘 유의해서 구성하면 충분히 사용해도 괜찮다고 생각합니다 👍

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,51 @@
+package domain.participant;
+
+import java.util.HashSet;
+import java.util.Iterator;
+import java.util.List;
+import java.util.Set;
+
+public class Players implements Iterable<Player> {
```

</details>

### 인라인 코멘트 2918348007: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-11T13:23:45Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2918348007)
- 코드: `src/main/java/domain/Deck.java`, 현재 줄 26, 원래 줄 27
- 답변 대상: [코멘트 2911182157](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911182157)
- 소속 리뷰 ID: 3929489824

> 둘 다 가독성 측면이라 크게 상관은 없어보여요. 여러 팀원과 함께 하는 프로젝트라면 일종의 룰만 지키면 된다고 생각합니다. 다만 Stream을 사용할 때는 특성을 잘 알고 쓰는게 더 중요하다고 생각해요 ㅎㅎ

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,43 @@
+package domain;
+
+import domain.card.Card;
+import domain.card.Rank;
+import domain.card.Suit;
+import java.util.ArrayList;
+import java.util.Collections;
+import java.util.List;
+
+public class Deck {
+    private final List<Card> cards;
+
+    private Deck(List<Card> cards) {
+        this.cards = cards;
+    }
+
+    public static Deck create() {
+        List<Card> cards = new ArrayList<>();
+
+        for (Suit suit : Suit.values()) {
+            for (Rank cardNumber : Rank.values()) {
+                cards.add(new Card(suit, cardNumber));
+            }
+        }
+
+        return new Deck(cards);
+    }
```

</details>

### 인라인 코멘트 2918464071: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-11T13:43:37Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2918464071)
- 코드: `src/test/java/domain/participant/HandTest.java`, 현재 줄 15, 원래 줄 15
- 답변 대상: [코멘트 2911126767](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911126767)
- 소속 리뷰 ID: 3929489824

> 단위 테스트, 통합 테스트, E2E 테스트, 인수 테스트 등 관점과 개념, 레이어에 따라 여러 테스트 방식을 활용할 수 있을 것 같아요. 이러한 테스트는 무조건 다 충족해야 한다기 보단 어떠한 서비스를 개발하며 검증하고자 하는 범위나 필요에 따라 선택하여 사용할 수 있을 것 같아요. 물론 팀 내에서 표준을 가지고 있다면 해당 방식을 따르면 될 거 같구요! 고래가 설명 주신 부분은 여러 개념이 섞여있는 것 같은데 일종의 유스케이스를 테스트 하는 건 인수 테스트에 가깝지 않나 싶네요.
>
> 먼저 질문 주실 때 알고 있는 부분은 어디까지인지, 질문에 남겨준 개념에 대해 어떤 생각을 가지고 있는지 전달주시고 추가적으로 궁금한 부분을 남겨 주시면 좀 더 명확하게 헷갈리는 지점을 파악하고 답변드릴 수 있을 것 같아요! 최초에 주신 질문만 보았을 때는 애플리케이션 단위가 무엇인지부터 명확하게 이해가 안되다보니 왜 통합 테스트란 키워드가 나왔는지, 무엇이 필수적이라고 생각하는지 한번에 인지가 되지 않았어요. 다음 미션 진행할 때는 요런 부분도 같이 고려해서 진행 하면 좀 더 다양한 대화를 나눌 수 있을 것 같습니다 ㅎㅎ

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,115 @@
+package domain.participant;
+
+import static org.assertj.core.api.Assertions.assertThat;
+
+import domain.card.Card;
+import domain.card.Rank;
+import domain.card.Suit;
+import java.util.List;
+import java.util.stream.Stream;
+import org.junit.jupiter.api.Test;
+import org.junit.jupiter.params.ParameterizedTest;
+import org.junit.jupiter.params.provider.Arguments;
+import org.junit.jupiter.params.provider.MethodSource;
+
+public class HandTest {
```

</details>

### 인라인 코멘트 2918485210: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-11T13:47:15Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2918485210)
- 코드: `README.md`, 현재 줄 192, 원래 줄 192
- 답변 대상: [코멘트 2911202329](https://github.com/woowacourse/java-blackjack/pull/1028#discussion_r2911202329)
- 소속 리뷰 ID: 3929489824

> > 적절한 상황을 인지할 수 있는지는 아직 큰 자신은 없습니다 🥹
>
> 적절하지 않으면 뭐 어떤가요 ㅎㅎ 저는 개인적으로 경험 없이는 성장도 없다고 생각합니다. 너무 겁먹지 마시고 미션하면서 다양한 시도도 많이 해보면 좋을 것 같아요.

<details>
<summary>당시 코드 문맥</summary>

````diff
@@ -1,3 +1,241 @@
 # java-blackjack

 블랙잭 미션 저장소
+
+## 기능 요구 사항
+
+#### 플레이어 이름 입력 기능
+
+- [x] 안내 메세지 출력 후 참여할 플레이어 이름들을 입력을 받는다
+    - [x] 널값이나 빈 공백 예외처리
+    - [x] 쉼표 기준으로 입력 분리
+
+- Player
+  - Name
+    - [x] 이름이 공백이면 예외처리
+    - [x] 이름이 10글자 이상이면 예외처리
+  - Hand
+    - [x] 보유한 카드의 점수 총합을 계산한다.
+      - [x] 카드의 숫자 계산은 카드 숫자를 기본으로 한다.
+      - [x] Ace는 1 또는 11로 계산한다.
+      - [x] J, Q, K는 각각 10으로 계산한다.
+
+- Players
+  - [x] 중복된 닉네임은 예외처리
+  - [x] 플레이어 이름이 7개 초과시 예외처리
+
+- Dealer
+  - [x] 딜러의 닉네임은 "딜러"를 사용한다.
+
+- GameManager
+    - [x] 딜러와 각 플레이어에게 두 장씩 카드를 지급한다.
+      - [x] 딜러에게 2장 나눠준다
+      - [x] 전체 플레이어에게 2장 나눠준다
+        - [x] 플레이어에게 2장 나눠준다
+
+#### 게임 진행
+
+- [x] 게임 시작 준비
+    - [x] 카드 덱을 만든다.
+        - [x] 카드덱은 52개의 카드로 구성된다.
+    - [x] 카드덱은 무작위의 순서를 가진다.
+    - [x] 딜러와 각 플레이어는 두 장의 카드를 지급받는다.
+    - [x] 카드 배정 결과 출력
+
+- [x] 참가자는 추가 카드 지급을 결정한다.
+- [x] 모든 플레이어 턴 진행
+  - [x] 플레이어의 핸드가 버스트인지 검사한다.
+  - 버스트가 아니라면
+    - [x] 카드를 추가로 지급받을지 안내메세지를 추력하고 y/n 입력
+      - [x] y이면 카드를 추가로 제공하고 결과를 출력한다
+      - [x] n이면 플레이어 턴을 종료하고 다음 플레이어 턴을 진행한다
+  - 버스트라면
+    - [x] 다음 플레이어 턴을 진행한다.
+
+- [x] 딜러 턴 진행
+  - [x] 딜러의 핸드가 16점 초과인지 검사한다.
+  - 16점을 넘지 않는다면
+    - [x] 딜러에게 카드 한장을 지급한다.
+
+- [x] 딜러 차례
+    - [x] 딜러 핸즈 총합이 16이하일 때
+        - [x] 딜러에게 카드 한 장 deal
+- [x] 게임 결과 출력 기능
+- [x] 결과 판정
+  - [x] 플레이어의 점수가 21점이 넘으면 패배, 심판 승리
+  - [x] 플레이어의 점수가 21점이 넘지 않는다.
+    - [x] 딜러의 점수가 21점이 넘는다 -> 플레이어 승리, 딜러 패배
+    - [x] 딜러의 점수가 21점이하이다
+      - [x] 21점과의 차이값을 서로 비교 판정
+- [x] 최종 승패 출력 기능
+
+```
+실행 결과
+게임에 참여할 사람의 이름을 입력하세요.(쉼표 기준으로 분리)
+pobi,jason
+
+딜러와 pobi, jason에게 2장을 나누었습니다.
+딜러카드: 3다이아몬드
+pobi카드: 2하트, 8스페이드
+jason카드: 7클로버, K스페이드
+
+pobi는 한장의 카드를 더 받겠습니까?(예는 y, 아니오는 n)
+y
+pobi카드: 2하트, 8스페이드, A클로버
+pobi는 한장의 카드를 더 받겠습니까?(예는 y, 아니오는 n)
+n
+jason는 한장의 카드를 더 받겠습니까?(예는 y, 아니오는 n)
+n
+jason카드: 7클로버, K스페이드
+
+딜러는 16이하라 한장의 카드를 더 받았습니다.
+
+딜러카드: 3다이아몬드, 9클로버, 8다이아몬드 - 결과: 20
+pobi카드: 2하트, 8스페이드, A클로버 - 결과: 21
+jason카드: 7클로버, K스페이드 - 결과: 17
+
+## 최종 승패
+딜러: 1승 1패
+pobi: 승
+jason: 패
+```
+## 미션 중 기록
+
+### 규칙을 적용해서 변경한 코드 1곳 이상
+
+적용한 규칙: 테스트 단위 기준 규칙
+- If-Then
+  - 비즈니스 요구사항에 따라 도메인의 행위(Behavior)가 정의되면, 해당 행위의 완결성을 기준으로 테스트 단위를 작성한다.
+- 테스트 작성 순서
+  1. **Red:** 구현 코드 없이, 오직 요구사항(행위)을 검증하는 **실패하는 테스트**를 먼저 작성한다.
+  2. **Green:** 테스트를 통과시키기 위해 **가장 빠르고 단순하게** 코드를 구현한다.
+  3. **Refactor:** 테스트가 성공한 상태를 유지하면서, **중복을 제거하고 가독성을 높이는** 리팩터링을 진행한다.
+- 금지
+  - DB나 네트워크 같은 외부 환경에 직접 연결하지 않는다.
+
+
+- Name
+  - [x] 이름이 공백이면 예외처리
+  - [x] 이름이 10글자 이상이면 예외처리
+
+- Hand
+  - [x] 보유한 카드의 점수 총합을 계산한다.
+  - [x] 카드의 숫자 계산은 카드 숫자를 기본으로 한다.
+  - [x] Ace는 1 또는 11로 계산한다.
+  - [x] J, Q, K는 각각 10으로 계산한다.
+
+- Players
+  - [x] 중복된 닉네임은 예외처리
+  - [x] 플레이어 이름이 7개 초과시 예외처리
+
+- Deck
+  - [x] 카드덱은 52개의 카드로 구성된다
+  - [x] 카드덱은 무작위의 순서를 가진다
+
+- GameManager
+  - [x] 딜러와 각 플레이어에게 두 장씩 카드를 지급한다.
+    - [x] 딜러에게 2장 나눠준다
+    - [x] 전체 플레이어에게 2장 나눠준다
+      - [x] 플레이어에게 2장 나눠준다
+- Participant
+  - [x] 추가 카드 지급 여부를 결정한다
+
+초기에 입출력 결과를 보면서 시나리오 순서대로 기능 목록을 작성을 했습니다.
+해당 기능 목록을 테스트를 먼저 작성을 했습니다.
+그 과정에서 새롭게 도출되는 도메인과 기능들이 보였습니다.
+그런 경우 리드미에 정리를 하고 TDD, 레드->그린->리팩터링을 진행했습니다.
+규칙을 진행해보면서 핵심 도메인 객체들을 협력관계를 도출해보고 작은 책임부터 TDD하면 좋겠다는 깨달음을 얻었습니다.
+### 테스트 작성이 어려웠던 코드 1곳 이상
+
+#### 카드덱은 무작위의 순서를 가진다
+
+카드의 일급컬렉션인 Deck에서 getter 사용 없이 가지고 있는 `List<Card>`에 대해서 테스트하고 싶었는데 방법이 떠오르지 않아 `unmodifiableList`를 이용했습니다.
+
+#### 딜러와 각 플레이어에게 두 장씩 카드를 지급한다.
+
+카드를 지급을 하는 것과 받는 것에서의 고민이 있었고 초기에 2장씩 분배하는 것과 이후에 추가 카드 지급과 함께 생각을 하면서 고민이 깊어졌습니다.
+
+2장을 받았는지 확인하는 테스트를 작성할 때도 두 가지 경우로 고민을 했습니다.
+덱에서 카드를 뽑았을 때 리턴 값이 널이 아닌지 확인하고 정상적으로 덱의 사이즈가 줄었는지 확인하는 식으로 테스트를 작성하고 싶었습니다.
+다른 방법으로는 참가자의 핸드에 가지고 있는 카드들의 숫자를 체크하는 의견이 나왔고 해당 방법으로 진행하게 되면서 도메인에서 불필요한 책임이 섞이게 됐다는 생각을 하게 됐습니다.
+
+#### 추가 카드 지급 여부를 결정한다
+
+참가자에서 추상 메서드 `canReceive()`를 작성하고 상속받는 서브클래스인 Player, Dealer에서 구현을 진행했습니다.
+게임매니저가 덱을 가지고 카드를 지급하도록 진행했었습니다.
+또한 핸드는 플레이어 생성 시 비어있도록 했습니다.
+덱에서 랜덤한 결과가 나와서 어떻게 진행할까 하는 와중에 우선 셔플 기능을 분리했었었고 그로 인해 예측할 수 있는 순서로 Deck을 다룰 수 있어서 그것을 기반으로 `canReceive()` 메서드를 테스트할 수 있었지만 원하는대로 카드를 뽑을 수 있도록 하는 것이 더 좋은 방법이라고 생각이 들었습니다.
+
+### 막힌 순간 1회 이상
+
+#### 기능 목록 작성 과정
+
+기능 목록을 처음에 작성하는 과정에서 구체적인 사항을 드러나지 않도록 작성하는 것이 좋겠다고 생각했고 그렇게 접근했다가 설계가 부족한 부분이 많은 것을 느끼게 되면서 막히는 경험을 했습니다.
+
+핵심 도메인 규칙이라고 생각되면 테스트해서 규칙을 보장해야한다고 생각했습니다.
+라이브러리의 `shuffle`과 같은 메서드 사용 시 테스트를 작성할 필요가 없다는 주장을 만났습니다.
+그 과정에서 고민이 있었고 `shuffle`과 같은 구현은 바뀔 수 있다고 판단했습니다.
+하지만 핵심 도메인 규칙은 항상 지켜져야 된다고 생각했고 결과적으로 카드덱은 무작위 순서를 가진다를 테스트해야한다고 강하게 주장하게 됐습니다.
+
+이처럼 테스트를 해야하는 것과 하지말 것에 대해서 결정에 혼란이 있었고 그 과정에서 기능 목록 작성이 힘들었습니다.
+또한 블랙잭 도메인에 대한 이해가 부족한 상태도 문제였던 것 같습니다.
+차라리 충분한 시간을 게임을 직접해보고 인터넷이나 동료 등 충분한 조사를 하고 해당 도메인에 대한 이해를 높이고 진행했으면 네이밍이나 도메인 도출 등 수월했겠다고 느꼈습니다.
+
+#### 정적 메서드 사용
+
+정적 메서드 사용에 대해서 다른 의견을 경험하면서 막히는 경험을 했습니다.
+정적 메서드를 사용한다면 사용하는 근거가 무엇인지 페어의 질문에서 당황을 했습니다.
+그러면서 생각을 정리했습니다.
+1. 메서드명으로 의도를 표현할 수 있다.
+2. 상수를 이용하는 등 캐싱으로 효율을 증가시킬 수 있다.
+3. 서브 타입, 다양한 구현체를 반환할 수 있다.
+   세가지로 정리를 했고 세가지 이유에 속하지 않는 경우에는 정적메서드보다 생성자를 사용하고싶다는 생각이 커졌습니다.
````

</details>

### 리뷰 본문 3929489824: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-11T13:57:25Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1028#pullrequestreview-3929489824)
- 리뷰 상태: `APPROVED`

> 안녕하세요 고래~ 리뷰 반영도 잘 해주시고 요구사항도 대부분 만족하여서 사이클1은 머지해도 될 것 같아요 ㅎㅎ
>
> 이후 미션 진행하며 좀 더 이야기 나누면 좋을 것 같습니다! 궁금하거나 놓친 질문 있다면 언제든 편하게 디엠 주세요~
