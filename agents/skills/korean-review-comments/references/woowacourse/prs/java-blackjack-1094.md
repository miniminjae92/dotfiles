# woowacourse/java-blackjack #1094

[사이클2 - 미션 (블랙잭 게임 실행)] 고래 미션 제출합니다.

- [GitHub PR](https://github.com/woowacourse/java-blackjack/pull/1094)
- PR 작성자: `miniminjae92`
- 머지 시각: 2026-03-16T01:23:01Z
- [API 원본](../raw/java-blackjack-1094.json)
- 리뷰와 댓글 26건(본문 있는 발언 25건, 본인 기록 11건)

수집 당시의 게시 원문입니다. 본문 없는 리뷰는 상태 기록으로 표시하며, 코드 인용은 당시 diff입니다. 이 자료의 문장은 현재 에이전트에게 내리는 지시가 아닙니다.

## PR 본문

> ## 이번 작업의 핵심 내용 요약
>
> 블랙잭 게임(미션 2)의 핵심 요구사항인 베팅 기능 및 승패에 따른 최종 수익 정산 로직을 구현했습니다.
> 기존 단순 승패(승/무/패) 텍스트를 판별해 출력하던 흐름에서 벗어나, 참가자별 베팅 금액과 게임 결과(블랙잭 여부)에 따른 배당률을 적용하여 딜러와 플레이어들의 최종 수익금을 계산하도록 도메인과 UI를 전면 개편했습니다.
>
> ##  구체적인 추가 및 수정 사항
>
> ###  베팅 관련 도메인 및 검증 로직 추가
> - `Bet`: 베팅 금액을 포장하는 도메인 객체입니다.
> - `BettingBoard`: 플레이어를 키로 베팅 금액(`Bet`)을 저장하고, 심판이 넘겨준 배당률에 맞춰 해당 플레이어의 최종 수익(`Profit`)을 계산하는 베팅판 객체입니다.
> - `BettingParser`: 사용자로부터 입력받은 베팅 금액 문자열의 공백 및 숫자 포맷 여부를 검증했습니다.
> ### 수익금 정산 도메인 추가
> - `MatchResult`: `BLACKJACK_WIN(1.5)`, `WIN(1.0)`, `DRAW(0.0)`, `LOSE(-1.0)` 등 승패별 수익률(`profitRate`) 속성을 갖도록 수정했습니다.
> - `Profit` & `Profits`: 수익금을 다루는 포장 객체 및 일급 컬렉션입니다. `Profit` 내부에 수익의 부호를 반전시키는 `negate()` 메서드를 두어, "딜러 수익 = 플레이어 총수익 * -1"이라는 규칙을 처리했습니다.
> - `Participant` & `Hand`: 객체가 스스로 자신의 카드 상태를 확인해 블랙잭 여부를 판단할 수 있도록 `isBlackjack()` 메서드 추가했습니다.
> ###  Referee(심판) 핵심 비즈니스 로직 변경
> - 단순히 승패 목록을 담은 DTO를 만들던 `evaluateMatch` 메서드를 삭제했습니다.
> - `BettingBoard`를 매개변수로 받아, 플레이어별 승패 결과를 도출한 뒤 수익금을 계산하고, 마지막에 딜러 수익까지 합산하여 최종 `Profits` 일급 컬렉션을 반환하는 `calculateProfits`로 책임을 재정의 했습니다.
> ### UI 흐름 및 DTO 교체
> - `GameController`: 게임 시작 직전 루프를 돌며 플레이어별 베팅 금액을 입력받아 `BettingBoard`에 세팅하는 흐름 추가했습니다.
> - `InputView`: `readBettingAmount` 추가했습니다.
> - `OutputView`: 기존의 승무패(`MatchResultView`) 출력 로직을 모두 걷어내고, 새롭게 만든 `ProfitsResultResponse` DTO를 받아 참가자들의 최종 수익을 출력하도록 변경했습니다.
> - 불필요한 코드 제거: 출력 방식이 바뀌면서 더 이상 쓰이지 않는 `MatchResultView`, `GameResultResponse`, `PlayerMatchResult` 등의 클래스를 일괄 삭제했습니다.
>
> ## 리뷰어에게
>
> 매트! 항상 고생이 많으십니다, 이번 미션 2 리뷰도 잘 부탁드립니다!
> 이번 미션을 진행하면서 깊게 고민했던 부분들을 말해볼게요!
>
> 처음에 베팅 금액을 플레이어가 가지면 되겠다고 생각했습니다.
> 하지만 아래의 요구 사항으로부터 고민이 생겼어요.
> - 3개 이상의 인스턴스 변수를 가진 클래스를 쓰지 않는다.
> 슈퍼클래스인 `Participant`가 가지고 있는 private 필드에 Player가 접근은 못하지만 인스턴스 객체로 생성될 때 모든 슈퍼클래스가 생성되는 것으로 알고 있습니다.
> 플레이어와 딜러가 슈퍼클래스의 인스턴스 변수를 가지고 있는 건 맞잖아?라고 생각이 들었고, 다만 클래스라고 명시가 되어있어 기준을 클래스로만 잡으면 해당 클래스 파일에는 필드가 명시 되진 않았잖아?라는 점이 서로 부딪히며 시작부터 깊은 고민을 했습니다.
> 그 과정에서 베팅 금액을 분리하는 방법은 없을까 생각을 시도해 보게 됐습니다.
> 요구사항이 없었다면 이런 생각을 해봤을까?라고 돌이켜보면 No라고 예상되는데요, 이러한 제약된 요구사항들이 새로운 시도를 하게 해주는 것 같습니다.
> 그렇게 해서 플레이어별 베팅금액으로 관리하고 승패에 따른 수익률을 계산하면 좋겠다고 접근할 아이디어가 떠올랐고 해당 방식으로 진행하게 됐습니다.
>
> 이번에는 아래의 지시사항을 지켜보고 싶었습니다.
> 이번 미션2에서도 설계를 하다가 또 너무 여러가지를 오랫동안 생각하게 되면서 구현 원칙을 못 지킬뻔 했는데요.
> 의식적으로 생각을 한 덕분에 "우선 동작하게 만들어보자" 생각하며, 급할 땐 `Setter`도 만들어서 사용하고 제거하는 등 새로운 방법을 시도해봤는데요, 매번 시작을 어려워하던 저에게 가슴이 뻥 뚫리는 느낌을 받기도 했네요
> 매트는 설계와 구현의 비중을 어떻게 두시는지, 궁금합니다! 우테코 과정을 진행하면서 매트도 변화가 많이 있었나요?
> ```
> 구현 원칙
> 빠르게 구현하고, 빠르게 PR을 보내라.
>
> 완벽한 코드가 아니라 피드백을 받을 수 있는 코드가 목표다.
>
> 동작하는 코드가 되면 바로 PR을 보낸다
> 부족한 부분은 숨기지 말고, 인식하고 공유한다
> PR이 빠를수록 리뷰에서 더 많이 배운다
> ```
>

## 대화와 리뷰 기록

### 인라인 코멘트 2931019566: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-13T12:52:13Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1094#discussion_r2931019566)
- 코드: `src/main/java/domain/Bet.java`, 현재 줄 None, 원래 줄 15
- 소속 리뷰 ID: 3943833165

> 금액을 다루는 경우 int 범위로 설정할 때 어떤 문제가 발생할 수 있나요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,15 @@
+package domain;
+
+public record Bet(int amount) {
+    private static final int MINIMUM_BETTING_AMOUNT = 1;
+
+    public Bet {
+        validate(amount);
+    }
+
+    private void validate(int amount) {
+        if (amount < MINIMUM_BETTING_AMOUNT) {
+            throw new IllegalArgumentException("베팅 금액은 최소 1원 이상이어야 합니다.");
+        }
+    }
+}
```

</details>

### 인라인 코멘트 2931020949: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-13T12:52:32Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1094#discussion_r2931020949)
- 코드: `src/main/java/domain/BettingBoard.java`, 현재 줄 23, 원래 줄 22
- 소속 리뷰 ID: 3943833165

> 배팅 머니를 별도 관리하는 이유는 무엇인가요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,22 @@
+package domain;
+
+import domain.participant.Player;
+import java.util.HashMap;
+import java.util.Map;
+
+public class BettingBoard {
+    private final Map<Player, Bet> betsByPlayer = new HashMap<>();
+
+    public void addBetting(Player player, Bet bet) {
+        betsByPlayer.put(player, bet);
+    }
+
+    public Profit calculateProfit(Player player, double profitRate) {
+        Bet originalBet = betsByPlayer.get(player);
+        return new Profit(originalBet.amount() * profitRate);
+    }
+
+    public Bet getBet(Player player) {
+        return betsByPlayer.get(player);
+    }
+}
```

</details>

### 인라인 코멘트 2931023387: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-13T12:53:03Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1094#discussion_r2931023387)
- 코드: `src/main/java/domain/BettingParser.java`, 현재 줄 None, 원래 줄 27
- 소속 리뷰 ID: 3943833165

> 별도로 파서를 구성한 이유는 무엇인가요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,27 @@
+package domain;
+
+public class BettingParser {
+
+    public static Bet parse(String input) {
+        validate(input);
+        return new Bet(parseInt(input));
+    }
+
+    private static void validate(String input) {
+        validateNotBlank(input);
+    }
+
+    private static void validateNotBlank(String rawPlayerName) {
+        if (rawPlayerName == null || rawPlayerName.isBlank()) {
+            throw new IllegalArgumentException("베팅 금액이 비어 있습니다.");
+        }
+    }
+
+    private static int parseInt(String input) {
+        try {
+            return Integer.parseInt(input);
+        } catch (NumberFormatException e) {
+            throw new IllegalArgumentException("숫자만 입력해 주세요.");
+        }
+    }
+}
```

</details>

### 인라인 코멘트 2931026950: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-13T12:53:48Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1094#discussion_r2931026950)
- 코드: `src/main/java/domain/Referee.java`, 현재 줄 None, 원래 줄 62
- 소속 리뷰 ID: 3943833165

> 반복된 if를 어떻게 줄일 수 있을까요?

### 인라인 코멘트 2931032670: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-13T12:55:02Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1094#discussion_r2931032670)
- 코드: `README.md`, 현재 줄 None, 원래 줄 248
- 소속 리뷰 ID: 3943833165

> 실제 동작과 요구사항이 다른 것 같아요!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -239,3 +239,19 @@ DTO 객체의 생성 책임은 컨트롤러나 서비스 레이어에 있는 것
 DTO는 원시타입만 들어가도록 해야하는가?, Enum 객체도 안되는 것인가?
 두 가지 고민사항으로 데이터 전달에도 고민을 했습니다.
 그 과정에서 뷰와 관련된 부분에서 문제가 생겨서 수정을 할 때를 생각해봤고 그런 경우 뷰를 수정할 것 같다는 생각과 의문들이 해소가 된 것 같습니다.
+
+### 미션 2 기능 요구 사항
+
+- [x] 플레이어는 게임을 시작할 때 배팅 금액을 정해야 한다.
+  - [x] 베팅 금액
+    - [x] 베팅 금액의 최소 단위는 10000이다.
+    - [x] 베팅 금액은 음수를 가질 수 있다.
```

</details>

### 인라인 코멘트 2931043209: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-13T12:57:13Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1094#discussion_r2931043209)
- 코드: `src/main/java/domain/Referee.java`, 현재 줄 None, 원래 줄 33
- 소속 리뷰 ID: 3943833165

> double의 합 연산은 안전할까요? java에서 부동소수점에 대한 연산은 어떻게 이뤄지나요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -1,42 +1,57 @@
 package domain;

-import domain.dto.GameResultResponse;
-import domain.dto.PlayerMatchResult;
 import domain.participant.Dealer;
+import domain.participant.Participant;
 import domain.participant.Participants;
 import domain.participant.Player;
-import java.util.ArrayList;
-import java.util.EnumMap;
-import java.util.List;
+import domain.participant.Players;
+import java.util.LinkedHashMap;
+import java.util.Map;

 public class Referee {

-    public GameResultResponse evaluateMatch(Participants participants) {
-        List<PlayerMatchResult> playerResults = calculatePlayerResults(participants);
-        EnumMap<MatchResult, Integer> dealerResults = calculateDealerResults(playerResults);
+    public Profits calculateProfits(Participants participants, BettingBoard bettingBoard) {
+        Dealer dealer = participants.getDealer();
+        Map<Participant, Profit> playerProfits = calculatePlayerProfits(participants.getPlayers(), dealer, bettingBoard);
+        Profit dealerProfit = calculateDealerProfit(playerProfits);
+        return assembleFinalProfits(dealer, dealerProfit, playerProfits);
+    }

-        return new GameResultResponse(dealerResults, playerResults);
+    private Map<Participant, Profit> calculatePlayerProfits(Players players, Dealer dealer, BettingBoard bettingBoard) {
+        Map<Participant, Profit> playerProfits = new LinkedHashMap<>();
+        for (Player player : players) {
+            MatchResult result = judge(dealer, player);
+            Profit profit = bettingBoard.calculateProfit(player, result.getProfitRate());
+            playerProfits.put(player, profit);
+        }
+        return playerProfits;
     }

-    private List<PlayerMatchResult> calculatePlayerResults(Participants participants) {
-        List<PlayerMatchResult> results = new ArrayList<>();
-        Dealer dealer = participants.getDealer();
+    private Profit calculateDealerProfit(Map<Participant, Profit> playerProfits) {
+        double totalPlayerProfit = playerProfits.values().stream()
+                .mapToDouble(Profit::value)
+                .sum();
```

</details>

### 리뷰 본문 3943833165: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-13T13:09:41Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1094#pullrequestreview-3943833165)
- 리뷰 상태: `CHANGES_REQUESTED`

> 안녕하세요 고래~ 이전에 구조를 어느정도 잡은 덕분에 수정이 크지 않아 빠르게 훓어보았습니다 ㅎㅎ
>
> 간단히 코멘트 남겼으니 확인해주시고 답변 남겨주세요!
>
> >의식적으로 생각을 한 덕분에 "우선 동작하게 만들어보자" 생각하며, 급할 땐 Setter도 만들어서 사용하고 제거하는 등 새로운 방법을 시도해봤는데요, 매번 시작을 어려워하던 저에게 가슴이 뻥 뚫리는 느낌을 받기도 했네요
> 매트는 설계와 구현의 비중을 어떻게 두시는지, 궁금합니다! 우테코 과정을 진행하면서 매트도 변화가 많이 있었나요?
>
> 저 또한 우테코를 진행하며 고래와 비슷한 고민을 하였는데요! 저는 대략적인 구현을 진행하며 설계를 그려가야 머릿속에 전체적인 그림이 그려지더라구요 ㅎㅎ 너무 설계에만 몰두하게 되면 실제 구현할 때 발목을 잡는 부분도 생기기도 하고 구현에 또 치중하면 추후 유연한 설계에 대비하지 못하기도 했던 것 같아요. 결국 두 지점을 적절히 조율하며 진행하는게 노하우이지 않을까 생각이 되어요.
>
> 그럼에도 가장 중요한 건 역시 마감 기한 이겠죠! 해당 기한 안에 설계와 구현을 모두 마무리해야 하기 때문에 좋은 설계를 위해 많은 시간을 투자하는 것도 중요하겠지만 대략적인 일정을 산정하는 역량 또한 매우 중요하다고 생각해요 ㅎㅎ

### 인라인 코멘트 2934730956: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-03-14T05:24:12Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1094#discussion_r2934730956)
- 코드: `src/main/java/domain/Bet.java`, 현재 줄 None, 원래 줄 15
- 답변 대상: [코멘트 2931019566](https://github.com/woowacourse/java-blackjack/pull/1094#discussion_r2931019566)
- 소속 리뷰 ID: 3948167324

> 두 가지 문제를 떠올릴 수 있었습니다.
> Overflow
> $2^{31} - 1$을 넘어가면 최솟값인 `-2147483648`로 순환하는 오버플로우 문제가 발생할 수 있습니다.
> Precision
> 다른 나라의 화폐나 소수점 단위를 표현해야 할 때, `int`는 정수만 처리할 수 있어 소수점 이하 데이터가 강제로 절사되는 문제가 발생할 수 있습니다.
> ### 발견한 해결책과 결정 근거
>
> 먼저 `long` 또는 `BigDecimal`을 떠올릴 수 있었습니다.
> `BigDecimal`에 대해서 모르기 때문에 공부를 해보고 각각을 사용할 때의 장단점에 대해서 생각해봤습니다.
>
> - `long` 사용 시: 소수점 표현이 필요 없는 환경에서는 오버플로우 범위가 훨씬 넓고($2^{63}-1$, 약 922경) 연산 성능이 빠릅니다. 하지만 수익률 계산 시 `double`과 곱셈 연산이 일어나는 순간, 부동소수점 특유의 미세한 오차가 발생하여 정밀도가 깨질 수 있습니다.
> - `BigDecimal` 사용 시: 객체 생성 비용으로 인해 성능은 상대적으로 낮지만, 메모리가 허용하는 한 무한한 자릿수와 소수점 연산을 오차 없이 10진수 기반으로 정확하게 처리할 수 있습니다.
>
> #### 최종 결정
> - 수익률(1.5배 등)과 연산할 때 어차피 오차 방지를 위해 `double`을 `BigDecimal`로 변환해야 하므로, 데이터의 일관성과 무결성을 위해 금액 관련 모든 필드에 `BigDecimal`을 표준으로 사용하기로 했습니다.
> - 주의 사항: `double`을 `BigDecimal`로 변환할 때는 반드시 문자열(`String`) 생성자나 `valueOf()` 메서드를 사용해야합니다. 그 이유는 `double`이 이미 가지고 있는 근사치 오차가 유입되는 것을 방지할 수 있기 때문입니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,15 @@
+package domain;
+
+public record Bet(int amount) {
+    private static final int MINIMUM_BETTING_AMOUNT = 1;
+
+    public Bet {
+        validate(amount);
+    }
+
+    private void validate(int amount) {
+        if (amount < MINIMUM_BETTING_AMOUNT) {
+            throw new IllegalArgumentException("베팅 금액은 최소 1원 이상이어야 합니다.");
+        }
+    }
+}
```

</details>

### 인라인 코멘트 2934753873: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-03-14T05:40:25Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1094#discussion_r2934753873)
- 코드: `src/main/java/domain/BettingBoard.java`, 현재 줄 23, 원래 줄 22
- 답변 대상: [코멘트 2931020949](https://github.com/woowacourse/java-blackjack/pull/1094#discussion_r2931020949)
- 소속 리뷰 ID: 3948167324

> "3개 이상의 인스턴스 변수를 가진 클래스를 쓰지 않는다. "라는 프로그래밍 요구사항을 지키려는 시도에서 생각하게 됐습니다.
>
> 그러한 시도 중에서 생각을 해봤을 때 참가자 객체가 직접 돈을 가지고 베팅하게 된다면 Knowing인 베팅 금액과 관련된 Doing, 행동의 예로 계산하는 책임까지 가지게 되는 것은 어울리지 않는다고 생각하게 됐습니다.
> 그리고 참가자와 베팅 금액은 생명주기가 다르다고 생각했습니다. 참가자는 게임의 시작과 종료까지 유지된다고 생각되는데 베팅 금액은 특정 라운드에 유효하다고 생각됐기 때문입니다.
> 그리고 딜러의 수익을 어떻게 계산할까를 계산하다가 플레이어들의 수익을 합한 뒤 마이너스를 곱하니깐 딱 떨어지는 것을 확인하고 딜러의 수익 계산을 위해서도 이러한 설계가 편리하겠다고 생각한 것도 이유가 됐습니다.
>

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,22 @@
+package domain;
+
+import domain.participant.Player;
+import java.util.HashMap;
+import java.util.Map;
+
+public class BettingBoard {
+    private final Map<Player, Bet> betsByPlayer = new HashMap<>();
+
+    public void addBetting(Player player, Bet bet) {
+        betsByPlayer.put(player, bet);
+    }
+
+    public Profit calculateProfit(Player player, double profitRate) {
+        Bet originalBet = betsByPlayer.get(player);
+        return new Profit(originalBet.amount() * profitRate);
+    }
+
+    public Bet getBet(Player player) {
+        return betsByPlayer.get(player);
+    }
+}
```

</details>

### 인라인 코멘트 2934771854: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-03-14T05:52:25Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1094#discussion_r2934771854)
- 코드: `src/main/java/domain/BettingParser.java`, 현재 줄 None, 원래 줄 27
- 답변 대상: [코멘트 2931023387](https://github.com/woowacourse/java-blackjack/pull/1094#discussion_r2931023387)
- 소속 리뷰 ID: 3948167324

> 사용자 입력은 언제든 변할 수 있는 불안정한 값이라고 생각합니다. 이를 도메인 내부로 직접 들여보내지 않고 즉시 검증하고 VO로 변환하기 위해 파서를 분리했습니다. 이를 통해 도메인 객체(`Bet`)는 문자열 파싱과 같은 로직에서 벗어나 비즈니스 규칙에만 집중할 수 있다고 생각됩니다.
>
> 이번 질문을 통해서 생각하게 된 부분이 있는데 공통된 유틸적인 부분이 반복될 것으로 판단이 됐습니다.
> 현재는 도메인별로 파서가 나뉘어 있지만, 추가 입력 요구 사항이 생길 때마다 반복적인 요소가 있을 것으로 생각되어서 상위 계층 인터페이스를 하나를 두어 입력 소스에 유연하게 대응하는 구조로 발전시키면 어떨까라고 생각하게 됐습니다.
>

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,27 @@
+package domain;
+
+public class BettingParser {
+
+    public static Bet parse(String input) {
+        validate(input);
+        return new Bet(parseInt(input));
+    }
+
+    private static void validate(String input) {
+        validateNotBlank(input);
+    }
+
+    private static void validateNotBlank(String rawPlayerName) {
+        if (rawPlayerName == null || rawPlayerName.isBlank()) {
+            throw new IllegalArgumentException("베팅 금액이 비어 있습니다.");
+        }
+    }
+
+    private static int parseInt(String input) {
+        try {
+            return Integer.parseInt(input);
+        } catch (NumberFormatException e) {
+            throw new IllegalArgumentException("숫자만 입력해 주세요.");
+        }
+    }
+}
```

</details>

### 인라인 코멘트 2934850613: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-03-14T07:03:13Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1094#discussion_r2934850613)
- 코드: `src/main/java/domain/Referee.java`, 현재 줄 None, 원래 줄 33
- 답변 대상: [코멘트 2931043209](https://github.com/woowacourse/java-blackjack/pull/1094#discussion_r2931043209)
- 소속 리뷰 ID: 3948167324

> 금융 데이터는 단 1원의 오차도 허용되지 않는 것이 중요한 부분이라고 생각됩니다.
>
> Java에서 부동소수점에 대한 연산에 대해서 알아봤습니다.
> 숫자를 이진수 형태의 지수와 가수로 나누어 저장을 하고 저희가 사용하는 10진수 소수 중 상당수가 2진수로 변환했을 때 무한 소수가 되는 것을 확인했습니다. 예를 들어 `0.1`의 경우도 2진수로 `0.0001100110011...`와 같이 무한히 반복되는데 컴퓨터는 메모리의 한계로 인해 무한한 숫자를 특정 지점에서 반올림하여 근사치로 저장하는 것을 알게 됐습니다.
>
> 이러한 근사치 오차들이 `stream().sum()`과 같이 합산하는 과정에서 누적되기 때문에 `double`의 합 연산은 금융 데이터를 다룰 때 안전하지 않다고 판단 됐습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -1,42 +1,57 @@
 package domain;

-import domain.dto.GameResultResponse;
-import domain.dto.PlayerMatchResult;
 import domain.participant.Dealer;
+import domain.participant.Participant;
 import domain.participant.Participants;
 import domain.participant.Player;
-import java.util.ArrayList;
-import java.util.EnumMap;
-import java.util.List;
+import domain.participant.Players;
+import java.util.LinkedHashMap;
+import java.util.Map;

 public class Referee {

-    public GameResultResponse evaluateMatch(Participants participants) {
-        List<PlayerMatchResult> playerResults = calculatePlayerResults(participants);
-        EnumMap<MatchResult, Integer> dealerResults = calculateDealerResults(playerResults);
+    public Profits calculateProfits(Participants participants, BettingBoard bettingBoard) {
+        Dealer dealer = participants.getDealer();
+        Map<Participant, Profit> playerProfits = calculatePlayerProfits(participants.getPlayers(), dealer, bettingBoard);
+        Profit dealerProfit = calculateDealerProfit(playerProfits);
+        return assembleFinalProfits(dealer, dealerProfit, playerProfits);
+    }

-        return new GameResultResponse(dealerResults, playerResults);
+    private Map<Participant, Profit> calculatePlayerProfits(Players players, Dealer dealer, BettingBoard bettingBoard) {
+        Map<Participant, Profit> playerProfits = new LinkedHashMap<>();
+        for (Player player : players) {
+            MatchResult result = judge(dealer, player);
+            Profit profit = bettingBoard.calculateProfit(player, result.getProfitRate());
+            playerProfits.put(player, profit);
+        }
+        return playerProfits;
     }

-    private List<PlayerMatchResult> calculatePlayerResults(Participants participants) {
-        List<PlayerMatchResult> results = new ArrayList<>();
-        Dealer dealer = participants.getDealer();
+    private Profit calculateDealerProfit(Map<Participant, Profit> playerProfits) {
+        double totalPlayerProfit = playerProfits.values().stream()
+                .mapToDouble(Profit::value)
+                .sum();
```

</details>

### 인라인 코멘트 2935053153: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-03-14T09:50:36Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1094#discussion_r2935053153)
- 코드: `README.md`, 현재 줄 None, 원래 줄 248
- 답변 대상: [코멘트 2931032670](https://github.com/woowacourse/java-blackjack/pull/1094#discussion_r2931032670)
- 소속 리뷰 ID: 3948167324

> 지적해 주신 대로 초기 요구사항 정의와 실제 구현 사이에 차이가 발생했습니다. 개발 과정에서 배당률 계산 시 발생하는 소수점 처리 문제와 현실적인 화폐 단위를 고려하여 아래와 같이 범위를 다시 설정하게 되었습니다.
>
> 블랙잭의 특수 규칙인 1.5배 배당(Natural Blackjack)을 적용할 때 화폐의 최소 단위가 중요함을 깨달았습니다.
> 1.5를 곱해도 원화 단위로 존재하는 100원을 하한선으로 재설정했습니다.
>
> 최대 금액(10억 원): 도메인의 안정성을 위해 무제한 베팅을 막고자 했으며, 시스템의 정수 오버플로우 방지 및 현실적인 카지노의 맥스 베팅 금액을 참고하여 임의의 상한선을 두었습니다.
>
> 음수 베팅 금액에 대한 정정 요구사항 체크리스트에 "음수를 가질 수 있다"라고 잘못 기재된 부분은 제 실수입니다. 베팅금액과 수익을 분리하는 설계를 하게 되면서 리드미도 함께 변경했어야 했는데 놓쳤네요! 체크해주셔서 감사합니다!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -239,3 +239,19 @@ DTO 객체의 생성 책임은 컨트롤러나 서비스 레이어에 있는 것
 DTO는 원시타입만 들어가도록 해야하는가?, Enum 객체도 안되는 것인가?
 두 가지 고민사항으로 데이터 전달에도 고민을 했습니다.
 그 과정에서 뷰와 관련된 부분에서 문제가 생겨서 수정을 할 때를 생각해봤고 그런 경우 뷰를 수정할 것 같다는 생각과 의문들이 해소가 된 것 같습니다.
+
+### 미션 2 기능 요구 사항
+
+- [x] 플레이어는 게임을 시작할 때 배팅 금액을 정해야 한다.
+  - [x] 베팅 금액
+    - [x] 베팅 금액의 최소 단위는 10000이다.
+    - [x] 베팅 금액은 음수를 가질 수 있다.
```

</details>

### 인라인 코멘트 2935053322: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-03-14T09:50:50Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1094#discussion_r2935053322)
- 코드: `src/main/java/domain/Referee.java`, 현재 줄 None, 원래 줄 62
- 답변 대상: [코멘트 2931026950](https://github.com/woowacourse/java-blackjack/pull/1094#discussion_r2931026950)
- 소속 리뷰 ID: 3948167324

> 처음에는 접근을 어떻게 다른 곳으로 옮길까에 대해서 고민했습니다.
> 아래의 코드처럼 분리해서 if를 줄일 생각을 했었습니다.
> ```
> public static MatchResult of(Dealer dealer, Player player) {
>     if (dealer.isBlackjack() || player.isBlackjack()) {
>         return judgeBlackjack(dealer, player);
>     }
>     if (dealer.isBust() || player.isBust()) {
>         return judgeBust(dealer, player);
>     }
>     return determineByScore(dealer.getScore(), player.getScore());
> }
>
> private static MatchResult judgeBlackjack(Dealer dealer, Player player) {
>     if (player.isBlackjack() && dealer.isBlackjack()) return DRAW;
>     if (player.isBlackjack()) return BLACKJACK_WIN;
>     return LOSE; // Dealer is Blackjack
> }
>
> private static MatchResult judgeBust(Dealer dealer, Player player) {
>     if (player.isBust()) return LOSE;
>     return WIN; // Dealer is Bust
> }
> ```
>
> 하지만 내츄럴 블랙잭 이외의 다른 규칙이 추가될 때마다 MatchResult가 무거워 질 것으로 판단도 되어서 이번 기회에 새로운 시도를 해보고 싶었습니다.
> "다형성을 이용해 조건문 줄이기" 라는 블랙잭 미션 글을 읽고 영감을 받았습니다.
> 객체가 행동 후 새로운 상태 객체를 반환하여 스스로 전이하도록 함으로써, 각 상태가 자신의 룰을 가장 잘 알고 행동하는 전문가가 되도록 설계해봤습니다.

### 리뷰 본문 3948167324: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-03-14T10:20:05Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1094#pullrequestreview-3948167324)
- 리뷰 상태: `COMMENTED`

> ## 주요 변경 사항
>
> - `int, double` 등 도메인 금액 관련 자료형들을 `BigDecimal` 객체로 변경
> - `Referee judge()` 메서드에서 블랙잭 규칙으로 증가되는 if 조건문을 `State` 객체를 통한 조건문 제거 리팩토링
> - 변경 사항에 대해 테스트 코드 리팩터링
>
> ## 리뷰어에게
>
> 상태를 다루면서 제가 구현을 하면서도 이해 못하는 곳에서 테스트 코드가 터지는 경험을 하게 됐습니다.
> 테스트 코드 덕분에 문제점을 알아차리며 리팩터링을 진행할 수 있어서 테스트의 소중함을 느낄 수 있었어요!
> 좋은 주말 보내시고 이번에도 리뷰 잘 부탁드리겠습니다 ☺️

### 인라인 코멘트 2936412083: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-15T07:58:35Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1094#discussion_r2936412083)
- 코드: `src/main/java/domain/state/State.java`, 현재 줄 22, 원래 줄 17
- 소속 리뷰 ID: 3949854008

> 상태 패턴을 도입하였네요! 고래는 개선하며 어떤 이점을 느끼셨나요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,17 @@
+package domain.state;
+
+import domain.Score;
+import domain.card.Card;
+import java.math.BigDecimal;
+import java.util.List;
+
+public interface State {
+    State draw(Card card);
+    State stay();
+    boolean isFinished();
+    boolean isBust();
+    boolean isBlackjack();
+    List<Card> cards();
+    Score getScore();
+    BigDecimal calculateProfitRate(State dealerState);
+}
```

</details>

### 인라인 코멘트 2936413364: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-15T08:00:08Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1094#discussion_r2936413364)
- 코드: `src/main/java/domain/state/Stay.java`, 현재 줄 20, 원래 줄 19
- 소속 리뷰 ID: 3949854008

> `new BigDecimal("-1.0")`은 재사용 가능하지 않을까 싶네요. BigDecimal은 어떤 특성을 가지고 있나요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,22 @@
+package domain.state;
+
+import domain.participant.Hand;
+import java.math.BigDecimal;
+
+public class Stay extends Finished {
+    public Stay(Hand hand) { super(hand); }
+
+    @Override
+    public BigDecimal calculateProfitRate(State dealerState) {
+        if (dealerState.isBust()) return BigDecimal.ONE;
+
+        int compare = this.getScore().compareTo(dealerState.getScore());
+        if (compare > 0) {
+            return BigDecimal.ONE;
+        }
+        if (compare < 0) {
+            return new BigDecimal("-1.0");
+        }
```

</details>

### 인라인 코멘트 2936416639: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-15T08:03:57Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1094#discussion_r2936416639)
- 코드: `src/main/java/domain/BettingBoard.java`, 현재 줄 23, 원래 줄 22
- 답변 대상: [코멘트 2931020949](https://github.com/woowacourse/java-blackjack/pull/1094#discussion_r2931020949)
- 소속 리뷰 ID: 3949854008

> 좋은 접근 인 것 같아요 😃 말씀 하신 관점으로 생각해보니 서로 다른 생명주기로 바라볼 수도 있겠네요! 각각의 책임이 명확해지니 테스트 하기 용이해질 것 같습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,22 @@
+package domain;
+
+import domain.participant.Player;
+import java.util.HashMap;
+import java.util.Map;
+
+public class BettingBoard {
+    private final Map<Player, Bet> betsByPlayer = new HashMap<>();
+
+    public void addBetting(Player player, Bet bet) {
+        betsByPlayer.put(player, bet);
+    }
+
+    public Profit calculateProfit(Player player, double profitRate) {
+        Bet originalBet = betsByPlayer.get(player);
+        return new Profit(originalBet.amount() * profitRate);
+    }
+
+    public Bet getBet(Player player) {
+        return betsByPlayer.get(player);
+    }
+}
```

</details>

### 인라인 코멘트 2936417411: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-15T08:04:47Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1094#discussion_r2936417411)
- 코드: `src/main/java/domain/Profit.java`, 현재 줄 23, 원래 줄 24
- 소속 리뷰 ID: 3949854008

> 금액 제한에 대한 검증을 잘 처리하였네요 👍

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,29 @@
+package domain;
+
+import java.math.BigDecimal;
+
+public record Profit(BigDecimal value) {
+    private static final BigDecimal MAX_PROFIT_LIMIT = new BigDecimal("100000000000000");
+
+    public Profit {
+        validateNull(value);
+        validateLimit(value);
+    }
+
+    private void validateNull(BigDecimal value) {
+        if (value == null) {
+            throw new IllegalArgumentException("수익 금액은 필수입니다.");
+        }
+    }
+
+    private void validateLimit(BigDecimal value) {
+        // 수익은 음수일 수 있으므로 절대값(abs)으로 상한선 검증 (신뢰도: 100%)
+        if (value.abs().compareTo(MAX_PROFIT_LIMIT) > 0) {
+            throw new IllegalArgumentException("수익 금액이 시스템 허용 범위를 초과했습니다.");
+        }
+    }
```

</details>

### 리뷰 본문 3949854008: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-15T08:07:01Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1094#pullrequestreview-3949854008)
- 리뷰 상태: `CHANGES_REQUESTED`

> 안녕하세요 고래! 상태 패턴을 도입하며 코드가 점점 간결해지고 책임이 명확하게 인지 된 것 같아요 ㅎㅎ 코드의 수정보다 리팩토링을 진행하며 어떤 과정을 거쳤는지 궁금하여 간단히 코멘트 남겼으니 확인해주세요!

### 인라인 코멘트 2936487341: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-03-15T09:13:25Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1094#discussion_r2936487341)
- 코드: `src/main/java/domain/state/State.java`, 현재 줄 22, 원래 줄 17
- 답변 대상: [코멘트 2936412083](https://github.com/woowacourse/java-blackjack/pull/1094#discussion_r2936412083)
- 소속 리뷰 ID: 3949953941

> ## 1. 복잡한 조건 분기 로직의 제거
>
> 이전에는 플레이어의 현재 점수나 상태를 확인하기 위해 많은 if-else 문을 사용해야 했습니다. 하지만 상태 패턴을 도입하면서 상태 전이 로직이 각 상태 객체 내부로 캡슐화되었습니다. 결과적으로 외부 제어 로직의 복잡성이 낮아졌고, 코드의 가독성이 좋아지는 이점을 얻었습니다.
>
> ## 2. 수정과 확장에 유리한 구조 (OCP)
>
> 새로운 블랙잭 규칙이 추가되는 상황을 가정했을 때, 이전에는 심판(Judge) 클래스의 제어문 전체를 분석하고 수정해야 하는 부담이 있었습니다. 하지만 상태 패턴을 적용한 후에는 새로운 규칙을 담은 상태 객체만 정의하면 되므로, 기존 코드에 영향을 주지 않고도 기능을 확장할 수 있어 유지보수 면에서 큰 이점을 느꼈습니다.
>
> ## 3. 객체의 자율성 및 캡슐화 강화
>
> 기존에는 외부에서 참가자의 점수를 묻고 그 값을 기반으로 승패를 판정하는 방식이었습니다. 이제는 참가자가 자신의 상태를 바탕으로 스스로 승패를 판단하게 함으로써, 객체를 더 자율적인 존재로 만들 수 있었습니다. 이는 내부 로직을 감추고 메시지를 통해 소통하는 캡슐화의 원칙을 더욱 강화하는 계기가 되었습니다.
>

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,17 @@
+package domain.state;
+
+import domain.Score;
+import domain.card.Card;
+import java.math.BigDecimal;
+import java.util.List;
+
+public interface State {
+    State draw(Card card);
+    State stay();
+    boolean isFinished();
+    boolean isBust();
+    boolean isBlackjack();
+    List<Card> cards();
+    Score getScore();
+    BigDecimal calculateProfitRate(State dealerState);
+}
```

</details>

### 인라인 코멘트 2936504769: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-03-15T09:30:45Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1094#discussion_r2936504769)
- 코드: `src/main/java/domain/state/Stay.java`, 현재 줄 20, 원래 줄 19
- 답변 대상: [코멘트 2936413364](https://github.com/woowacourse/java-blackjack/pull/1094#discussion_r2936413364)
- 소속 리뷰 ID: 3949953941

> 찾아보니 불변성이라는 특성때문에 얘기해주셨다고 생각이 되는데요?!
> 같은 값을 가진다면 new로 같은 객체를 생성하기 보다는 상수로 한번만 생성해서 재사용하는 것이 메모리 측면에서 유리할 것으로 생각되네요!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,22 @@
+package domain.state;
+
+import domain.participant.Hand;
+import java.math.BigDecimal;
+
+public class Stay extends Finished {
+    public Stay(Hand hand) { super(hand); }
+
+    @Override
+    public BigDecimal calculateProfitRate(State dealerState) {
+        if (dealerState.isBust()) return BigDecimal.ONE;
+
+        int compare = this.getScore().compareTo(dealerState.getScore());
+        if (compare > 0) {
+            return BigDecimal.ONE;
+        }
+        if (compare < 0) {
+            return new BigDecimal("-1.0");
+        }
```

</details>

### 인라인 코멘트 2936517578: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-03-15T09:44:24Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1094#discussion_r2936517578)
- 코드: `src/main/java/domain/BettingBoard.java`, 현재 줄 23, 원래 줄 22
- 답변 대상: [코멘트 2931020949](https://github.com/woowacourse/java-blackjack/pull/1094#discussion_r2931020949)
- 소속 리뷰 ID: 3949953941

> 네, 베팅 책임을 분리하니 플레이어나 딜러의 상태를 일일이 세팅하지 않고도 수익률에 따른 정산 로직만 독립적으로 검증할 수 있어서 편리했습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,22 @@
+package domain;
+
+import domain.participant.Player;
+import java.util.HashMap;
+import java.util.Map;
+
+public class BettingBoard {
+    private final Map<Player, Bet> betsByPlayer = new HashMap<>();
+
+    public void addBetting(Player player, Bet bet) {
+        betsByPlayer.put(player, bet);
+    }
+
+    public Profit calculateProfit(Player player, double profitRate) {
+        Bet originalBet = betsByPlayer.get(player);
+        return new Profit(originalBet.amount() * profitRate);
+    }
+
+    public Bet getBet(Player player) {
+        return betsByPlayer.get(player);
+    }
+}
```

</details>

### 리뷰 본문 3949953941: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-03-15T09:55:15Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1094#pullrequestreview-3949953941)
- 리뷰 상태: `COMMENTED`

> 상태 패턴 사용에 대한 이점을 한 번 더 생각해보면서 이번 시도에 대한 이해가 올라갈 수 있어 좋았습니다!
> `BigDecimal` 객체에 대해서 지적해주셔서 무의미한 재 생성 및 사용에 대해서도 경각심을 가지게 됐습니다!
>
> 매트! 주말인데 리뷰를 해주셔서 감사합니다~
> 좋은 주말 보내세요!

### 인라인 코멘트 2937719296: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-16T01:19:40Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1094#discussion_r2937719296)
- 코드: `src/main/java/domain/state/Stay.java`, 현재 줄 20, 원래 줄 19
- 답변 대상: [코멘트 2936413364](https://github.com/woowacourse/java-blackjack/pull/1094#discussion_r2936413364)
- 소속 리뷰 ID: 3951018996

> 넵 맞습니다 ㅎㅎ 불변 객체와 특성에 대해 잘 알아두면 멀티 스레드 개념이 필요할 때도 다방면으로 활용 할 수 있으니 잘 알아두면 좋을 것 같아요!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,22 @@
+package domain.state;
+
+import domain.participant.Hand;
+import java.math.BigDecimal;
+
+public class Stay extends Finished {
+    public Stay(Hand hand) { super(hand); }
+
+    @Override
+    public BigDecimal calculateProfitRate(State dealerState) {
+        if (dealerState.isBust()) return BigDecimal.ONE;
+
+        int compare = this.getScore().compareTo(dealerState.getScore());
+        if (compare > 0) {
+            return BigDecimal.ONE;
+        }
+        if (compare < 0) {
+            return new BigDecimal("-1.0");
+        }
```

</details>

### 리뷰 본문 3951018996: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-16T01:19:40Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1094#pullrequestreview-3951018996)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 리뷰 본문 3951024173: hyeonic

- 상대방 발언, 참여자
- 시각: 2026-03-16T01:22:45Z
- [게시 원문](https://github.com/woowacourse/java-blackjack/pull/1094#pullrequestreview-3951024173)
- 리뷰 상태: `APPROVED`

> 안녕하세요 고래! 사이클 2 너무 고생하셨어요 ㅎㅎ 대부분 다 잘 반영해주시고 고래의 근거와 생각도 알 수 있게 되어서 빠르게 확인 할 수 있었습니다.
>
> 남은 우테코 생활도 화이팅 하시고 이후 미션 진행하며 여러 견해가 필요하다면 언제든 편하게 디엠 요청 주셔도 좋으니 편하게 남겨주세요 🙂
