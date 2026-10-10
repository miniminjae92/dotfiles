# woowacourse/java-janggi #269

[ 사이클1 - 미션 (보드 초기화 + 기물 이동)] 고래 미션 제출합니다.

- [GitHub PR](https://github.com/woowacourse/java-janggi/pull/269)
- PR 작성자: `miniminjae92`
- 머지 시각: 2026-04-05T12:25:19Z
- [API 원본](../raw/java-janggi-269.json)
- 리뷰와 댓글 67건(본문 있는 발언 60건, 본인 기록 28건)

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
> - [ ] 미션의 필수 요구사항을 모두 구현했나요?
> - [x] Gradle `test`를 실행했을 때, 모든 테스트가 정상적으로 통과했나요?
> - [x] 애플리케이션이 정상적으로 실행되나요?
>
>
> ## 어떤 부분에 집중하여 리뷰해야 할까요?
>
> 안녕하세요 웨지!
> 많이 늦었죠? 이번 리뷰 잘 부탁드립니다!
>
> 설계상 어려웠던 부분들을 지금 다시 떠올려보자면,
>
> ### 입출력 흐름
> 페어와 얘기를 하면서 기물을 선택하고 갈 수 있는 지점을 나타내주면 좋겠다고 의견을 나눴습니다.
> 실제 게임에서 기물을 클릭하면 이동 가능 경로가 보이고 이동할 곳을 클릭하는 것을 상상했고 진행했습니다.
> 이 과정에서 출발점, 도착점을 한 번에 진행할 로직을 분리해서 진행하다 보니 재시도 부분과 예외 처리들에서 고민되는 부분들이 많았던 것 같습니다.
>
> ### 게임 초기화
> 게임 초기화 관련해서 고민을 꽤 했었습니다.
> 처음에는 ' 게임 시작 시 장기판과 전체 기물을 올바른 위치에 초기화한다.'를 테스트를 해야 하는가에 대해서 고민했습니다.
> 올바른 위치에 초기화되는 것은 꼭 보장되어야 하는 도메인 규칙이라고 느껴졌고, 테스트를 해야 한다고 판단했습니다.
> 그 후에 테스트를 어떻게 진행할지, 초기화를 어떻게 할지에 대해서 오래 고민했습니다.
> 고민을 오래 했지만, 결과적으로는 구현은 하드코딩, 테스트는 Mock으로 해보려 도전했다가 실패, 테스트를 위한 getter 사용을 고려하다가 좋은 방법이 떠오르지 않아서 패스했습니다.
> 결국은 페어가 팩토리를 만들자는 의견을 해서 하드 코딩 부분들을 하나의 팩토리에 응집시킬 수 있었습니다.
>
> ### 보드
> 저는 사전미션에서 위치가 총 90개밖에 안 되기 때문에 모든 위치를 가지고 빈 기물 객체를 가지는 방법을 떠올렸습니다. 그룹별로 토론을 진행했고, 대화를 나누면서 존재하는 기물에 대해서만 데이터로 보관하는 방법이 더 구현이 쉽게 떠올라서 해당 방법으로 진행했습니다.
> 그 후 보드와 기물 간에 협력을 어떻게 진행할지에 대해서 고민했습니다.
> 페어와 그림을 그리면서 얘기를 하면서 보드는 기물에게 위치를 주면, 기물은 해당 위치로부터의 모든 이동 가능한 위치들을 반환하고 보드는 그 위치들을 순회하면서 기물이 존재하는 것만 위치별 기물 `Map`에 담아서 다시 기물로 보내고 기물을 해당 데이터들을 이용해서 최종 목적지를 담아서 보드로 보내고 보드는 바깥으로 응답하는 식으로 설계했습니다.
> 추후 계속해서 구현하다가 실제로 Map이라는 자료구조를 기물이 알게 되는 것도 강한 의존성이라고 느껴져서 BoardReader라는 인터페이스 사용을 떠올렸고, 적용을 해봤습니다.
> 이 과정에서 순환 참조를 생각해 봤고, 어디서 처리하는 게 좋은가? 고민을 해보게 됐습니다.
> 저는 결과적으로 잘 변하지 않는 기물의 공통된 이동 전략을 추상화하고 게임 진행 시 계속 바뀌는 진영, 턴에 대해서는 상태 패턴을 적용해 봤습니다.
>
> ### 불변
> 직관적으로는 불변이 좋다고만 생각하지, 아직 제대로 경험을 해본 적이 없는 것 같습니다.
> 멀티 스레드 환경이나 많은 동료와 협업 등 여러 변수가 생겨야 느낄 수 있을까요?
> 불변성을 잘 지키면 예상치 못하는 동작을 방지하고 동시성에 대해서 에너지 소모를 아낄 수 있고, 부수 효과를 방지할 수 있다고 들었습니다. 다만 제가 시작부터 불변성을 유지하려 노력해서인지 현실적인 체감을 못 했는데 실무에서는 많이 다른지 궁금합니다.
> 이번 보드(장기판)가 가지고 있는 필드인 맵에 대해서 상태가 가변이었는데 보기가 불편하고, 위에 설명한 이유들을 익히 들어와서 불변성을 지니도록 보드를 설계해서 결국 보드를 가지고 있는 게임에서 final 할당 방지를 제거하게 됐는데 이 부분에서도 근거와 직접 느껴보는 경험?이 부족하다 보니 필요한 일이었는지 궁금합니다.
>
> ### 정적 메서드
> 언제 한 번 재활용 가능한, 캐싱을 사용할 수 있을 때 정적 팩토리 메서드를 사용해 보고 싶었는데 이번 장기에서 고정된 위치와 기물들을 초기에 생성하기 때문에 활용해 봤습니다.
>
> 이번 미션에서 페어는 AI 활용을 자제하는 것으로 알고 저도 노력을 해봤습니다.
> 어떠한 글을 작성하거나 예를 들어서 피드백을 받았을 때 먼저 내 생각을 적어 보고 AI와 문답을 해보고 답변을 가다듬는 것과 그러지 않고 순수한 제 생각을 작성하는 것 중 무엇이 지금 우테코를 할 때 좋을지 고민입니다.
> 과하지 않게 적당히 잘 활용하는 것이 좋다는 판단이 있을 수 있을 텐데 이번 미션에서 아예 금지를 해두고 진행해 보니 생각보다 강한 의존성이 생겼다는 것을 느꼈습니다.
> 웨지의 AI 활용에 대한 의견이 궁금하네요, 더 고생한 만큼 기억에 강하게 남는 것처럼 최대한 사용을 자제하는 것과 어느 정도 고민을 하고 시간을 무리하게 지체되지 않도록 인터넷 서칭, AI, 동료와의 토론을 적극 활용하는 것이 더 추천될까요?
>
> 마지막으로 아래 요구 사항들을 지키는 것이 어려웠습니다.
>
> for문 안에서 발생하는 if 조건문들을 depth를 위해서 줄이는 과정
> 모든 기능을 TDD로 구현한다. << 모든 public method를 테스트한다고 받아들이면 될까요? (getter, UI 제외)
> 모든 원시값을 포장하고 일급컬렉션을 사용한다.
> 디미터의 법칙
> 게터를 사용하지 않는다
>
> 이 부분들에 대해서는 아직 부족한 부분이 많지만 시간을 너무 소모하기엔 늦은 것 같아 부족하지만 PR 보냅니다, 잘 부탁드립니다.
>
> <!-- 리뷰어가 효과적으로 피드백할 수 있도록 중점적으로 피드백받고 싶은 내용을 공유해주세요.
> 예를 들어, 가장 고민했던 점이나 여전히 어려운 부분, 그리고 이에 대한 생각을 적을 수 있습니다. -->
>

## 대화와 리뷰 기록

### 일반 댓글 4176253287: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-02T10:32:24Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#issuecomment-4176253287)

> ai 활용에 대해 고민해주신것 보았는데요
> Ai도 하나의 툴이니까 잘 활용하면 좋을것 같아요
> 여기서 잘 이라는게 어렵긴한데요
> Ai 에게 0부터 100까지 다 물어보는것은 지양하시고 고래의 생각을 잘 정리한다음 확인을 하거나 놓치는 부분이 있을지 물어보고
> 답변에 대해 비판적인 시각으로 바라보며 검토를 하시는것이 도움이 되지 않을까 싶어요
> 도구를 잘 쓰는 개발자가 되어야지 도구 없이 개발을 못하지 않도록 하시는게 좋을것 같습니다
>
> 저희팀에서는 개발자간에 토론을 할 때 사용하기도 하는데요
> 여러가지 의견을 내고 이야기를 하다가 놓친부분이 있을지 체크리스트로 검수할 사항을 도출하는등의 행위를 할 때 사용하기도 합니다

### 일반 댓글 4176254583: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-02T10:32:41Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#issuecomment-4176254583)

> 불변은 모든 상황에서 다 좋지만은 않았던것 같아요
> 상태 관리를 하는게 오히려 더 직관적인 경우도 있었던것 같구요
> 우리는 실용적인 코드를 작성해서 읽기 쉽고 유지보수하기 좋은 산출물을 만들어내는거지 예술작품을 만들어내는게 아니니까요
>
> 값이 동시에 여러 스레드에 공유되는 경우가 아니면 저도 그렇게 큰 장점을 느끼며 개발한 기억은 없는것 같네요
> 그래도 잘못된 값 변화를 막기 위해 가능한 경우 불변으로 설계하는 편 이긴 해요
>
>  지금은 교육기간이니 도전해보고 싶은 부분을 몸으로 체감해보셔도 좋을것 같아요

### 인라인 코멘트 3027259174: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-02T10:36:41Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027259174)
- 코드: `src/main/java/controller/JanggiConsoleController.java`, 현재 줄 17, 원래 줄 14
- 소속 리뷰 ID: 4049806238

> `GameManager`가 `domain` 패키지에 위치하면서 `view.InputParser`, `view.InputView`, `view.OutputView`를 직접 의존하고 있는데요, 도메인 객체가 뷰 계층을 알고 있는 구조가 되어버립니다. 개선이 필요해보여요

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,89 @@
+package domain;
+
+import domain.board.Board;
+import domain.board.BoardFactory;
+import domain.board.Formation;
+import domain.board.FormationCommand;
+import domain.player.Name;
+import domain.player.Players;
+import java.util.List;
+import java.util.function.Supplier;
+import view.InputParser;
+import view.InputView;
+import view.OutputView;
+
```

</details>

### 인라인 코멘트 3027259859: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-02T10:36:49Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027259859)
- 코드: `src/main/java/domain/Game.java`, 현재 줄 35, 원래 줄 45
- 소속 리뷰 ID: 4049806238

> `getBoard()`가 `Map<Position, Piece>`를 그대로 반환하고 있는데요. 사용하는 곳은 view로 보이네요. 불변한 컬렉션을 반환해보면 어떨까요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,53 @@
+package domain;
+
+import domain.board.Board;
+import domain.piece.Piece;
+import domain.player.Players;
+import java.util.Map;
+
+public class Game {
+    private Board board;
+    private final Players players;
+
+    public Game(Board board, Players players) {
+        this.board = board;
+        this.players = players;
+    }
+
+    public Side getCurrentSide() {
+        return players.getCurrentSide();
+    }
+
+    public Destinations selectSource(Position position) {
+        Piece piece = board.getPiece(position);
+        players.getCurrentPlayer().validateAlly(piece);
+        return findDestinations(position);
+    }
+
+    public void move(Position source, Position target) {
+        Destinations destinations = selectSource(source);
+        destinations.validateDestinations(target);
+        movePiece(source, target);
+        players.switchPlayer();
+    }
+
+    private Destinations findDestinations(Position position) {
+        return board.findDestinations(position);
+    }
+
+    private void movePiece(Position source, Position target) {
+        this.board = board.movePiece(source, target);
+    }
+
+    public Map<Position, Piece> getBoard() {
+        return board.getBoard();
+    }
+
```

</details>

### 인라인 코멘트 3027260900: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-02T10:37:03Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027260900)
- 코드: `src/main/java/domain/Position.java`, 현재 줄 65, 원래 줄 68
- 소속 리뷰 ID: 4049806238

> Position이 캐싱을 통해 동일 좌표에 대해 같은 인스턴스를 반환하고 있는데, `equals()`와 `hashCode()`를 별도로 오버라이드하고 계시네요. 캐싱 덕분에 `==` 비교만으로도 동등성이 보장되는 상황에서 필요한 이유가 있나요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,91 @@
+package domain;
+
+import domain.strategy.Direction;
+import java.util.HashMap;
+import java.util.List;
+import java.util.Map;
+import java.util.Objects;
+
+public class Position {
+    private static final Map<Integer, Position> CACHE = new HashMap<>();
+
+    public static final int MIN = 0;
+    public static final int MAX_X = 8;
+    public static final int MAX_Y = 9;
+
+    private final int x;
+    private final int y;
+
+    static {
+        for (int x = MIN; x <= MAX_X; x++) {
+            for (int y = MIN; y <= MAX_Y; y++) {
+                CACHE.put(generateKey(x, y), new Position(x, y));
+            }
+        }
+    }
+
+    private Position(int x, int y) {
+        this.x = x;
+        this.y = y;
+    }
+
+    public static Position of(int x, int y) {
+        validateRange(x, y);
+        return CACHE.get(generateKey(x, y));
+    }
+
+    private static void validateRange(int x, int y) {
+        if (!isWithinRange(x, y)) {
+            throw new IllegalArgumentException(String.format("범위를 벗어난 좌표입니다: (%d, %d)", x, y));
+        }
+    }
+
+    public boolean canMove(Direction direction) {
+        return isWithinRange(this.x + direction.getDx(), this.y + direction.getDy());
+    }
+
+    public boolean canMove(List<Direction> sequence) {
+        if (sequence.isEmpty()) {
+            return true;
+        }
+
+        Direction direction = sequence.getFirst();
+        if (!canMove(direction)) {
+            return false;
+        }
+
+        return move(direction).canMove(sequence.subList(1, sequence.size()));
+    }
+
+    public Position move(Direction direction) {
+        return Position.of(this.x + direction.getDx(), this.y + direction.getDy());
+    }
+
+    public static boolean isWithinRange(int x, int y) {
+        return x >= MIN && x <= MAX_X && y >= MIN && y <= MAX_Y;
+    }
+
+    private static int generateKey(int x, int y) {
```

</details>

### 인라인 코멘트 3027261312: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-02T10:37:09Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027261312)
- 코드: `src/main/java/domain/Side.java`, 현재 줄 12, 원래 줄 63
- 소속 리뷰 ID: 4049806238

> `Side` enum에 `baseY()`, `generalY()`, `cannonY()`, `soldierY()`, `formationX()` 같은 배치 좌표 정보가 들어있는데요, 진영(Side)이라는 개념이 "초/한 구분"이라는 본래 역할 외에 "보드 배치 좌표"라는 책임까지 가진것 같네요.
>
> SRP를 위반한 것 아닌가요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,78 @@
+package domain;
+
+import java.util.List;
+
+public enum Side {
+    CHO("초") {
+        @Override
+        public int baseY() {
+            return 0;
+        }
+
+        @Override
+        public int generalY() {
+            return 1;
+        }
+
+        @Override
+        public int cannonY() {
+            return 2;
+        }
+
+        @Override
+        public int soldierY() {
+            return 3;
+        }
+
+        @Override
+        public List<Integer> formationX() {
+            return List.of(1, 2, 6, 7);
+        }
+    },
+    HAN("한") {
+        @Override
+        public int baseY() {
+            return 9;
+        }
+
+        @Override
+        public int generalY() {
+            return 8;
+        }
+
+        @Override
+        public int cannonY() {
+            return 7;
+        }
+
+        @Override
+        public int soldierY() {
+            return 6;
+        }
+
+        @Override
+        public List<Integer> formationX() {
+            return List.of(7, 6, 2, 1);
+        }
+    };
+
+    private final String name;
+
+    Side(String name) {
+        this.name = name;
+    }
```

</details>

### 인라인 코멘트 3027261952: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-02T10:37:19Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027261952)
- 코드: `src/main/java/domain/state/ActiveTurn.java`, 현재 줄 13, 원래 줄 9
- 소속 리뷰 ID: 4049806238

> 상태 패턴을 적용해서 턴을 관리하신 의도는 좋은데요, `next()`가 호출될 때마다 새로운 객체를 생성해야만 하나요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,14 @@
+package domain.state;
+
+public class ActiveTurn implements TurnState {
+
+    @Override
+    public boolean isCurrent() {
+        return true;
+    }
+
```

</details>

### 인라인 코멘트 3027262625: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-02T10:37:29Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027262625)
- 코드: `src/test/java/domain/player/PlayersTest.java`, 현재 줄 None, 원래 줄 12
- 소속 리뷰 ID: 4049806238

> 예외 테스트에서 `isInstanceOf(IllegalArgumentException.class)`만 검증하고 있는데요, 이 프로젝트에서 `IllegalArgumentException`을 던지는 곳이 상당히 많아요. [거짓 음성](https://bottom-to-top.tistory.com/97)을 주의해보면 좋을것 같습니다.
>
>

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,14 @@
+package domain.player;
+
+import static org.assertj.core.api.Assertions.assertThatThrownBy;
+
+import org.junit.jupiter.api.Test;
+
+class PlayersTest {
+
+    @Test
+    void 초기_플레이어_생성_시_두_플레이어의_이름이_같으면_예외가_발생한다() {
+        assertThatThrownBy(() -> Players.createInitial(new Name("whale"), new Name("whale")))
+                .isInstanceOf(IllegalArgumentException.class);
```

</details>

### 인라인 코멘트 3027264005: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-02T10:37:48Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027264005)
- 코드: `src/main/java/domain/piece/Piece.java`, 현재 줄 None, 원래 줄 49
- 소속 리뷰 ID: 4049806238

> is특정타입 형태의 메서드는 피해볼까요? 하위 구현체에 맞춰 계속해서 추가될 수 있어 추상화가 깨질 우려가 있습니다.
>
> 특정 타입인지를 묻기보다, 특정 행위를 할 수 있는지에 초점을 맞추어 표현해보면 좋을것 같아요.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,55 @@
+package domain.piece;
+
+import domain.Destinations;
+import domain.Position;
+import domain.Side;
+import domain.board.BoardReader;
+import domain.strategy.MovementStrategy;
+import domain.strategy.Path;
+import java.util.List;
+
+public abstract class Piece {
+    private final Side side;
+    private final MovementStrategy movementStrategy;
+
+    protected Piece(Side side, MovementStrategy movementStrategy) {
+        this.side = side;
+        this.movementStrategy = movementStrategy;
+    }
+
+    public Destinations findDestinations(Position current, BoardReader board) {
+        List<Path> paths = movementStrategy.generatePaths(current);
+        List<Position> validDestinations = filterValidPositions(current, paths, board);
+        return new Destinations(validDestinations);
+    }
+
+    protected abstract List<Position> filterValidPositions(Position current, List<Path> paths, BoardReader board);
+
+    protected List<Position> filterStandardPaths(List<Path> paths, BoardReader board) {
+        return paths.stream()
+                .filter(path -> !path.isBlocked(board))
+                .map(Path::getDestination)
+                .filter(dest -> isCatchableOrEmpty(dest, board))
+                .toList();
+    }
+
+    protected boolean isCatchableOrEmpty(Position destination, BoardReader board) {
+        return board.isEmpty(destination) || !board.isAlly(destination, side);
+    }
+
+    public boolean isAlly(Side other) {
+        return this.side.isAlly(other);
+    }
+
+    public boolean isGeneral() {
+        return false;
+    }
+
+    public boolean isCannon() {
+        return false;
```

</details>

### 인라인 코멘트 3027357721: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-02T10:58:21Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027357721)
- 코드: `src/test/java/domain/PositionTest.java`, 현재 줄 9, 원래 줄 9
- 소속 리뷰 ID: 4049806238

> 경계값만 테스트해주면 충분할것 같아보여요

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,45 @@
+package domain;
+
+import static org.assertj.core.api.Assertions.assertThatCode;
+import static org.assertj.core.api.Assertions.assertThatThrownBy;
+
+import org.junit.jupiter.params.ParameterizedTest;
+import org.junit.jupiter.params.provider.ValueSource;
+
+class PositionTest {
```

</details>

### 인라인 코멘트 3027370924: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-02T11:01:30Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027370924)
- 코드: `src/main/java/domain/strategy/ContinuousStrategy.java`, 현재 줄 None, 원래 줄 5
- 소속 리뷰 ID: 4049806238

> 사용하지 않는 import는 제거해주세요.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,33 @@
+package domain.strategy;
+
+import domain.Position;
+import java.util.ArrayList;
+import java.util.List;
```

</details>

### 인라인 코멘트 3027371282: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-02T11:01:34Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027371282)
- 코드: `src/main/java/domain/strategy/Direction.java`, 현재 줄 15, 원래 줄 48
- 소속 리뷰 ID: 4049806238

> `Direction`이 `horseSequences()`, `elephantSequences()`, `choSoldier()`, `hanSoldier()` 같은 특정 기물의 이동 조합을 직접 알고 있어야 하나요? SRP 위반 아닐까요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,60 @@
+package domain.strategy;
+
+import java.util.List;
+
+public enum Direction {
+    N(0, 1),
+    S(0, -1),
+    E(1, 0),
+    W(-1, 0),
+    NE(1, 1),
+    NW(-1, 1),
+    SE(1, -1),
+    SW(-1, -1);
+
+    private final int dx;
+    private final int dy;
+
+    Direction(int dx, int dy) {
+        this.dx = dx;
+        this.dy = dy;
+    }
+
+    public static List<Direction> linear() {
+        return List.of(N, S, E, W);
+    }
+
+    public static List<List<Direction>> horseSequences() {
+        return List.of(
+                List.of(N, NW), List.of(N, NE),
+                List.of(S, SW), List.of(S, SE),
+                List.of(E, NE), List.of(E, SE),
+                List.of(W, NW), List.of(W, SW)
+        );
+    }
+
+    public static List<List<Direction>> elephantSequences() {
+        return List.of(
+                List.of(N, NW, NW), List.of(N, NE, NE),
+                List.of(S, SW, SW), List.of(S, SE, SE),
+                List.of(E, NE, NE), List.of(E, SE, SE),
+                List.of(W, NW, NW), List.of(W, SW, SW)
+        );
+    }
+
+    public static List<Direction> choSoldier() {
+        return List.of(N, E, W);
+    }
+
```

</details>

### 인라인 코멘트 3027372378: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-02T11:01:51Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027372378)
- 코드: `src/main/java/domain/Game.java`, 현재 줄 24, 원래 줄 25
- 소속 리뷰 ID: 4049806238

> `players.getCurrentPlayer().validateAlly(piece);`를 `Players`에게 위임할 수 없나요?
>
>

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,53 @@
+package domain;
+
+import domain.board.Board;
+import domain.piece.Piece;
+import domain.player.Players;
+import java.util.Map;
+
+public class Game {
+    private Board board;
+    private final Players players;
+
+    public Game(Board board, Players players) {
+        this.board = board;
+        this.players = players;
+    }
+
+    public Side getCurrentSide() {
+        return players.getCurrentSide();
+    }
+
+    public Destinations selectSource(Position position) {
+        Piece piece = board.getPiece(position);
+        players.getCurrentPlayer().validateAlly(piece);
+        return findDestinations(position);
+    }
```

</details>

### 인라인 코멘트 3027430061: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-02T11:14:33Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027430061)
- 코드: `src/main/java/domain/Game.java`, 현재 줄 43, 원래 줄 52
- 소속 리뷰 ID: 4049806238

> `winner`를 찾기위해 대기중인 플레이어의 이름을 가져오는게 직관적으로 의도에 맞는 네이밍으로 보이지는 않는것 같아요.
>
> 다른 네이밍은 없을까요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,53 @@
+package domain;
+
+import domain.board.Board;
+import domain.piece.Piece;
+import domain.player.Players;
+import java.util.Map;
+
+public class Game {
+    private Board board;
+    private final Players players;
+
+    public Game(Board board, Players players) {
+        this.board = board;
+        this.players = players;
+    }
+
+    public Side getCurrentSide() {
+        return players.getCurrentSide();
+    }
+
+    public Destinations selectSource(Position position) {
+        Piece piece = board.getPiece(position);
+        players.getCurrentPlayer().validateAlly(piece);
+        return findDestinations(position);
+    }
+
+    public void move(Position source, Position target) {
+        Destinations destinations = selectSource(source);
+        destinations.validateDestinations(target);
+        movePiece(source, target);
+        players.switchPlayer();
+    }
+
+    private Destinations findDestinations(Position position) {
+        return board.findDestinations(position);
+    }
+
+    private void movePiece(Position source, Position target) {
+        this.board = board.movePiece(source, target);
+    }
+
+    public Map<Position, Piece> getBoard() {
+        return board.getBoard();
+    }
+
+    public boolean isOver() {
+        return board.isGameOver();
+    }
+
+    public String getWinner() {
+        return players.getWaitingPlayerName();
+    }
```

</details>

### 인라인 코멘트 3027500300: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-02T11:31:21Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027500300)
- 코드: `src/test/java/domain/piece/SoldierTest.java`, 현재 줄 None, 원래 줄 14
- 소속 리뷰 ID: 4049806238

> 초나라 졸과 한나라 졸의 이동 방향을 하나의 테스트에서 함께 검증하고 있는데요, 이 둘은 서로 다른 정책(전진 방향이 반대)을 검증하는 것이라 별도 테스트로 분리하는 게 각 케이스의 의도가 더 명확해질 것 같아요.
>
> [테스트도 SRP를 지켜주세요](https://bottom-to-top.tistory.com/99)

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,30 @@
+package domain.piece;
+
+import static org.assertj.core.api.Assertions.assertThat;
+
+import domain.Position;
+import domain.Side;
+import domain.board.Board;
+import java.util.Map;
+import org.junit.jupiter.api.DisplayName;
+import org.junit.jupiter.api.Test;
+
+class SoldierTest {
+    @Test
+    @DisplayName("초나라 졸은 상/좌/우 이동이 가능하고 한나라 졸은 하/좌/우 이동이 가능하다")
```

</details>

### 인라인 코멘트 3027500547: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-02T11:31:24Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027500547)
- 코드: `src/test/java/domain/player/PlayerTest.java`, 현재 줄 45, 원래 줄 44
- 소속 리뷰 ID: 4049806238

> `choPlayer.validateAlly(choPiece)`만 호출하고 별도의 단언이 없네요

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,53 @@
+package domain.player;
+
+import static org.assertj.core.api.Assertions.assertThat;
+import static org.assertj.core.api.Assertions.assertThatThrownBy;
+
+import domain.Side;
+import domain.piece.Piece;
+import domain.piece.PieceFactory;
+import domain.state.ActiveTurn;
+import org.junit.jupiter.api.Test;
+
+class PlayerTest {
+
+    @Test
+    void 턴_상태를_토글하면_현재_턴_여부가_반전된다() {
+        // Given: 초나라 플레이어가 자신의 턴(ActiveTurn)인 상태로 생성
+        Player player = new Player(new Name("cho"), Side.CHO, new ActiveTurn());
+
+        // When: 턴을 한 번 토글 (Active -> Waiting)
+        player.toggleTurn();
+        // Then
+        assertThat(player.isCurrentTurn()).isFalse();
+
+        // When: 턴을 다시 토글 (Waiting -> Active)
+        player.toggleTurn();
+        // Then
+        assertThat(player.isCurrentTurn()).isTrue();
+    }
+
+    @Test
+    void 플레이어는_자신의_기물이_아닌_상대방의_기물을_검증하면_예외가_발생한다() {
+        // Given: 초나라 플레이어와 한나라 졸(Soldier)
+        Player choPlayer = new Player(new Name("cho"), Side.CHO, new ActiveTurn());
+
+        // PieceFactory를 사용하여 실제 도메인과 동일한 기물 생성 (전략 주입 포함)
+        Piece hanPiece = PieceFactory.createSoldier(Side.HAN);
+
+        // When & Then: 초나라 플레이어가 한나라 기물을 validateAlly 할 때 예외 발생
+        assertThatThrownBy(() -> choPlayer.validateAlly(hanPiece))
+                .isInstanceOf(IllegalArgumentException.class)
+                .hasMessageContaining("상대방의 기물은 움직일 수 없습니다.");
+    }
+
+    @Test
```

</details>

### 인라인 코멘트 3027501449: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-02T11:31:38Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027501449)
- 코드: `src/test/java/domain/board/FormationCommandTest.java`, 현재 줄 None, 원래 줄 11
- 소속 리뷰 ID: 4049806238

> 하나의 테스트에서 4개의 입력에 대해 각각 단언하고 있는데요 간결하게 표현해주세요
>
> `ParameterizedTest` 를 사용하시면 될 것 같네요.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,26 @@
+package domain.board;
+
+import static org.assertj.core.api.Assertions.assertThat;
+import static org.assertj.core.api.Assertions.assertThatThrownBy;
+
+import org.junit.jupiter.api.Test;
+
+class FormationCommandTest {
+
+    @Test
+    void 포메이션_입력이_1_2_3_4_일때_정상_동작한다() {
```

</details>

### 인라인 코멘트 3027518593: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-02T11:35:43Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027518593)
- 코드: `src/main/java/domain/strategy/Direction.java`, 현재 줄 None, 원래 줄 21
- 소속 리뷰 ID: 4049806238

> 축약하지 말아주세요.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,60 @@
+package domain.strategy;
+
+import java.util.List;
+
+public enum Direction {
+    N(0, 1),
+    S(0, -1),
+    E(1, 0),
+    W(-1, 0),
+    NE(1, 1),
+    NW(-1, 1),
+    SE(1, -1),
+    SW(-1, -1);
+
+    private final int dx;
+    private final int dy;
+
+    Direction(int dx, int dy) {
+        this.dx = dx;
+        this.dy = dy;
+    }
```

</details>

### 인라인 코멘트 3027528117: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-02T11:37:54Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027528117)
- 코드: `src/main/java/domain/strategy/Path.java`, 현재 줄 None, 원래 줄 42
- 소속 리뷰 ID: 4049806238

> 상수로 표현할 수 없나요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,52 @@
+package domain.strategy;
+
+import domain.Position;
+import domain.board.BoardReader;
+import java.util.List;
+import java.util.Optional;
+import java.util.function.Predicate;
+
+public class Path {
+    private final List<Position> steps;
+
+    public Path(List<Position> steps) {
+        this.steps = List.copyOf(steps);
+    }
+
+    public Path takeWhile(Predicate<Position> condition) {
+        List<Position> result = steps.stream()
+                .takeWhile(condition)
+                .toList();
+        return new Path(result);
+    }
+
+    public Optional<Position> findFirst(Predicate<Position> condition) {
+        return steps.stream()
+                .filter(condition)
+                .findFirst();
+    }
+
+    public Path after(Position target) {
+        int index = steps.indexOf(target);
+        if (index == -1 || index == steps.size() - 1) {
+            return new Path(List.of());
+        }
+        return new Path(steps.subList(index + 1, steps.size()));
+    }
+
+    public boolean isBlocked(BoardReader board) {
+        if (steps.size() <= 1) {
+            return false;
+        }
+        return steps.subList(0, steps.size() - 1).stream()
+                .anyMatch(pos -> !board.isEmpty(pos));
```

</details>

### 인라인 코멘트 3027533161: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-02T11:38:57Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027533161)
- 코드: `src/main/java/domain/Destinations.java`, 현재 줄 27, 원래 줄 27
- 소속 리뷰 ID: 4049806238

> 이런 메서드는 절차적으로 호출하지 않으면 의도한대로 사용되지 않을 우려가 있어보이는데요.
>
> 구조적으로 안전하게 설계를 개선해보면 좋을것 같네요.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,28 @@
+package domain;
+
+import java.util.List;
+
+public class Destinations {
+    private final List<Position> positions;
+
+    public Destinations(List<Position> positions) {
+        validate(positions);
+        this.positions = List.copyOf(positions);
+    }
+
+    private void validate(List<Position> positions) {
+        if (positions.isEmpty()) {
+            throw new IllegalArgumentException("이동 가능한 목적지가 없습니다.");
+        }
+    }
+
+    public List<Position> getPositions() {
+        return positions;
+    }
+
+    public void validateDestinations(Position target) {
+        if (!positions.contains(target)) {
+            throw new IllegalArgumentException("이동할 수 없는 위치입니다.");
+        }
+    }
```

</details>

### 리뷰 본문 4049806238: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-02T11:42:03Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#pullrequestreview-4049806238)
- 리뷰 상태: `CHANGES_REQUESTED`

> 리뷰어가 중간에 바뀌면서 리뷰가 늦었네요. 질문에 대한 부분은 DM으로 이야기했었고 PR에 복사해서 답변해두었어요.
>
> 개선할 포인트들에 대해 리뷰를 남겨두었으니 확인해주세요.

### 인라인 코멘트 3031496622: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-03T05:25:37Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3031496622)
- 코드: `src/main/java/domain/piece/Piece.java`, 현재 줄 None, 원래 줄 49
- 답변 대상: [코멘트 3027264005](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027264005)
- 소속 리뷰 ID: 4054326506

> 피드백을 받고 다시 생각해보니, 상위 추상 클래스가 하위 구체 클래스(General, Cannon)의 구체적인 이름을 아는 것은 설계적 순환 참조이자 OCP 위반이라는 점에 공감을 했습니다.
>
> 처음에는 피드백을 전적으로 수용하여 이 메서드들을 아예 없애는 방향으로 리팩터링을 시도했습니다. 하지만 로직의 흐름상 기물의 특성을 확인하는 과정 자체는 필수적이었습니다. 애초에 이러한 조건문들을 없애기 위해서 설계한 방법이었기 때문입니다. 이를 대체하기 위해 `instanceof`를 사용하거나 `PieceType`, `Role` 같은 별도의 식별 필드를 도출하는 방법 외에는 떠오르는 것이 없었습니다. 이미 다형성으로 구조를 설계해둔 상태에서 식별용 타입을 추가하는 것은 중복된 설계이며, 객체지향적인 해결책이 아니라고 판단했습니다.
>
> 비밥이 질문해주신 의도는 외부에서 기물에게 질문을 던지는 행위 자체가 문제라기보다는 '추상 클래스에 하위 구체 클래스의 명칭(General, Cannon)이 그대로 노출되어 있는 것'이 문제의 핵심이라고 생각해봤습니다.
> 그렇다면 `isGeneral, isCannon`이 필요한 이유와 알맞도록 변경해봤습니다.
>
> `isGeneral -> isVital()`
> `isCannon -> canBridge & canBeCapturedByJump`

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,55 @@
+package domain.piece;
+
+import domain.Destinations;
+import domain.Position;
+import domain.Side;
+import domain.board.BoardReader;
+import domain.strategy.MovementStrategy;
+import domain.strategy.Path;
+import java.util.List;
+
+public abstract class Piece {
+    private final Side side;
+    private final MovementStrategy movementStrategy;
+
+    protected Piece(Side side, MovementStrategy movementStrategy) {
+        this.side = side;
+        this.movementStrategy = movementStrategy;
+    }
+
+    public Destinations findDestinations(Position current, BoardReader board) {
+        List<Path> paths = movementStrategy.generatePaths(current);
+        List<Position> validDestinations = filterValidPositions(current, paths, board);
+        return new Destinations(validDestinations);
+    }
+
+    protected abstract List<Position> filterValidPositions(Position current, List<Path> paths, BoardReader board);
+
+    protected List<Position> filterStandardPaths(List<Path> paths, BoardReader board) {
+        return paths.stream()
+                .filter(path -> !path.isBlocked(board))
+                .map(Path::getDestination)
+                .filter(dest -> isCatchableOrEmpty(dest, board))
+                .toList();
+    }
+
+    protected boolean isCatchableOrEmpty(Position destination, BoardReader board) {
+        return board.isEmpty(destination) || !board.isAlly(destination, side);
+    }
+
+    public boolean isAlly(Side other) {
+        return this.side.isAlly(other);
+    }
+
+    public boolean isGeneral() {
+        return false;
+    }
+
+    public boolean isCannon() {
+        return false;
```

</details>

### 리뷰 본문 4054326506: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-03T05:25:37Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#pullrequestreview-4054326506)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 3031611760: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-03T06:15:00Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3031611760)
- 코드: `src/main/java/domain/Side.java`, 현재 줄 12, 원래 줄 63
- 답변 대상: [코멘트 3027261312](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027261312)
- 소속 리뷰 ID: 4054443479

> Side가 진영 식별 외에 배치 규칙 정의 정보까지 가지고 있는 것은 SRP 위반이라고 저 또한 공감이 가서 변경을 해봤습니다.
> SideLayout 클래스를 새롭게 도출해서 책임을 분리했습니다.
> 수정을 하면서 Formation에 있던 조립을 하던 행위가 BoardFactory에 더 어울린다고 생각해서 함께 수정했습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,78 @@
+package domain;
+
+import java.util.List;
+
+public enum Side {
+    CHO("초") {
+        @Override
+        public int baseY() {
+            return 0;
+        }
+
+        @Override
+        public int generalY() {
+            return 1;
+        }
+
+        @Override
+        public int cannonY() {
+            return 2;
+        }
+
+        @Override
+        public int soldierY() {
+            return 3;
+        }
+
+        @Override
+        public List<Integer> formationX() {
+            return List.of(1, 2, 6, 7);
+        }
+    },
+    HAN("한") {
+        @Override
+        public int baseY() {
+            return 9;
+        }
+
+        @Override
+        public int generalY() {
+            return 8;
+        }
+
+        @Override
+        public int cannonY() {
+            return 7;
+        }
+
+        @Override
+        public int soldierY() {
+            return 6;
+        }
+
+        @Override
+        public List<Integer> formationX() {
+            return List.of(7, 6, 2, 1);
+        }
+    };
+
+    private final String name;
+
+    Side(String name) {
+        this.name = name;
+    }
```

</details>

### 인라인 코멘트 3031689162: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-03T06:46:26Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3031689162)
- 코드: `src/main/java/domain/Position.java`, 현재 줄 65, 원래 줄 68
- 답변 대상: [코멘트 3027260900](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027260900)
- 소속 리뷰 ID: 4054443479

> 네, 맞습니다.
> 같은 메모리 주소를 사용하는 것이므로 == 만으로도 동등성이 보장되기 때문에 필요없다고 판단네요.
> 좋은 지적 감사합니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,91 @@
+package domain;
+
+import domain.strategy.Direction;
+import java.util.HashMap;
+import java.util.List;
+import java.util.Map;
+import java.util.Objects;
+
+public class Position {
+    private static final Map<Integer, Position> CACHE = new HashMap<>();
+
+    public static final int MIN = 0;
+    public static final int MAX_X = 8;
+    public static final int MAX_Y = 9;
+
+    private final int x;
+    private final int y;
+
+    static {
+        for (int x = MIN; x <= MAX_X; x++) {
+            for (int y = MIN; y <= MAX_Y; y++) {
+                CACHE.put(generateKey(x, y), new Position(x, y));
+            }
+        }
+    }
+
+    private Position(int x, int y) {
+        this.x = x;
+        this.y = y;
+    }
+
+    public static Position of(int x, int y) {
+        validateRange(x, y);
+        return CACHE.get(generateKey(x, y));
+    }
+
+    private static void validateRange(int x, int y) {
+        if (!isWithinRange(x, y)) {
+            throw new IllegalArgumentException(String.format("범위를 벗어난 좌표입니다: (%d, %d)", x, y));
+        }
+    }
+
+    public boolean canMove(Direction direction) {
+        return isWithinRange(this.x + direction.getDx(), this.y + direction.getDy());
+    }
+
+    public boolean canMove(List<Direction> sequence) {
+        if (sequence.isEmpty()) {
+            return true;
+        }
+
+        Direction direction = sequence.getFirst();
+        if (!canMove(direction)) {
+            return false;
+        }
+
+        return move(direction).canMove(sequence.subList(1, sequence.size()));
+    }
+
+    public Position move(Direction direction) {
+        return Position.of(this.x + direction.getDx(), this.y + direction.getDy());
+    }
+
+    public static boolean isWithinRange(int x, int y) {
+        return x >= MIN && x <= MAX_X && y >= MIN && y <= MAX_Y;
+    }
+
+    private static int generateKey(int x, int y) {
```

</details>

### 인라인 코멘트 3031873154: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-03T07:50:59Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3031873154)
- 코드: `src/main/java/domain/strategy/Direction.java`, 현재 줄 15, 원래 줄 48
- 답변 대상: [코멘트 3027371282](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027371282)
- 소속 리뷰 ID: 4054443479

>
> 듣고보니 기물의 이동 조합은 게임의 룰이라고 보여집니다.
> Direction이 알고 있는 것은 좌표의 증감인데 방향 객체의 책임과 맞지 않다고 생각합니다.
> 축약을 제거하고, MovePattern에 이동 규칙을 응집시켜봤습니다.
>

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,60 @@
+package domain.strategy;
+
+import java.util.List;
+
+public enum Direction {
+    N(0, 1),
+    S(0, -1),
+    E(1, 0),
+    W(-1, 0),
+    NE(1, 1),
+    NW(-1, 1),
+    SE(1, -1),
+    SW(-1, -1);
+
+    private final int dx;
+    private final int dy;
+
+    Direction(int dx, int dy) {
+        this.dx = dx;
+        this.dy = dy;
+    }
+
+    public static List<Direction> linear() {
+        return List.of(N, S, E, W);
+    }
+
+    public static List<List<Direction>> horseSequences() {
+        return List.of(
+                List.of(N, NW), List.of(N, NE),
+                List.of(S, SW), List.of(S, SE),
+                List.of(E, NE), List.of(E, SE),
+                List.of(W, NW), List.of(W, SW)
+        );
+    }
+
+    public static List<List<Direction>> elephantSequences() {
+        return List.of(
+                List.of(N, NW, NW), List.of(N, NE, NE),
+                List.of(S, SW, SW), List.of(S, SE, SE),
+                List.of(E, NE, NE), List.of(E, SE, SE),
+                List.of(W, NW, NW), List.of(W, SW, SW)
+        );
+    }
+
+    public static List<Direction> choSoldier() {
+        return List.of(N, E, W);
+    }
+
```

</details>

### 인라인 코멘트 3031905947: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-03T08:02:01Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3031905947)
- 코드: `src/main/java/domain/strategy/Path.java`, 현재 줄 None, 원래 줄 42
- 답변 대상: [코멘트 3027528117](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027528117)
- 소속 리뷰 ID: 4054443479

> 상수로 표현을 해봤습니다.
> 다만 NOT_FOUND, SINGLE_STEP_SIZE 외에 다른 매직 넘버에 대해서도 지금처럼 상수화 하는 것이 좋은지 의견이 궁금합니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,52 @@
+package domain.strategy;
+
+import domain.Position;
+import domain.board.BoardReader;
+import java.util.List;
+import java.util.Optional;
+import java.util.function.Predicate;
+
+public class Path {
+    private final List<Position> steps;
+
+    public Path(List<Position> steps) {
+        this.steps = List.copyOf(steps);
+    }
+
+    public Path takeWhile(Predicate<Position> condition) {
+        List<Position> result = steps.stream()
+                .takeWhile(condition)
+                .toList();
+        return new Path(result);
+    }
+
+    public Optional<Position> findFirst(Predicate<Position> condition) {
+        return steps.stream()
+                .filter(condition)
+                .findFirst();
+    }
+
+    public Path after(Position target) {
+        int index = steps.indexOf(target);
+        if (index == -1 || index == steps.size() - 1) {
+            return new Path(List.of());
+        }
+        return new Path(steps.subList(index + 1, steps.size()));
+    }
+
+    public boolean isBlocked(BoardReader board) {
+        if (steps.size() <= 1) {
+            return false;
+        }
+        return steps.subList(0, steps.size() - 1).stream()
+                .anyMatch(pos -> !board.isEmpty(pos));
```

</details>

### 인라인 코멘트 3034905427: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-04T01:21:27Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3034905427)
- 코드: `src/main/java/domain/Game.java`, 현재 줄 24, 원래 줄 25
- 답변 대상: [코멘트 3027372378](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027372378)
- 소속 리뷰 ID: 4054443479

> 수정했습니다!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,53 @@
+package domain;
+
+import domain.board.Board;
+import domain.piece.Piece;
+import domain.player.Players;
+import java.util.Map;
+
+public class Game {
+    private Board board;
+    private final Players players;
+
+    public Game(Board board, Players players) {
+        this.board = board;
+        this.players = players;
+    }
+
+    public Side getCurrentSide() {
+        return players.getCurrentSide();
+    }
+
+    public Destinations selectSource(Position position) {
+        Piece piece = board.getPiece(position);
+        players.getCurrentPlayer().validateAlly(piece);
+        return findDestinations(position);
+    }
```

</details>

### 인라인 코멘트 3034945093: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-04T02:01:03Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3034945093)
- 코드: `src/main/java/domain/Game.java`, 현재 줄 43, 원래 줄 52
- 답변 대상: [코멘트 3027430061](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027430061)
- 소속 리뷰 ID: 4054443479

> 승자 진영을 이용해서 플레이어 이름을 반환하도록 수정해봤습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,53 @@
+package domain;
+
+import domain.board.Board;
+import domain.piece.Piece;
+import domain.player.Players;
+import java.util.Map;
+
+public class Game {
+    private Board board;
+    private final Players players;
+
+    public Game(Board board, Players players) {
+        this.board = board;
+        this.players = players;
+    }
+
+    public Side getCurrentSide() {
+        return players.getCurrentSide();
+    }
+
+    public Destinations selectSource(Position position) {
+        Piece piece = board.getPiece(position);
+        players.getCurrentPlayer().validateAlly(piece);
+        return findDestinations(position);
+    }
+
+    public void move(Position source, Position target) {
+        Destinations destinations = selectSource(source);
+        destinations.validateDestinations(target);
+        movePiece(source, target);
+        players.switchPlayer();
+    }
+
+    private Destinations findDestinations(Position position) {
+        return board.findDestinations(position);
+    }
+
+    private void movePiece(Position source, Position target) {
+        this.board = board.movePiece(source, target);
+    }
+
+    public Map<Position, Piece> getBoard() {
+        return board.getBoard();
+    }
+
+    public boolean isOver() {
+        return board.isGameOver();
+    }
+
+    public String getWinner() {
+        return players.getWaitingPlayerName();
+    }
```

</details>

### 인라인 코멘트 3034949112: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-04T02:05:20Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3034949112)
- 코드: `src/main/java/domain/Destinations.java`, 현재 줄 27, 원래 줄 27
- 답변 대상: [코멘트 3027533161](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027533161)
- 소속 리뷰 ID: 4054443479

> 출발지 위치와 해당 위치가 갈 수 있는 도착점들을 가지는 객체를 도출해서 해당 객체가 검증하도록 수정해봤습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,28 @@
+package domain;
+
+import java.util.List;
+
+public class Destinations {
+    private final List<Position> positions;
+
+    public Destinations(List<Position> positions) {
+        validate(positions);
+        this.positions = List.copyOf(positions);
+    }
+
+    private void validate(List<Position> positions) {
+        if (positions.isEmpty()) {
+            throw new IllegalArgumentException("이동 가능한 목적지가 없습니다.");
+        }
+    }
+
+    public List<Position> getPositions() {
+        return positions;
+    }
+
+    public void validateDestinations(Position target) {
+        if (!positions.contains(target)) {
+            throw new IllegalArgumentException("이동할 수 없는 위치입니다.");
+        }
+    }
```

</details>

### 인라인 코멘트 3034969423: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-04T02:22:01Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3034969423)
- 코드: `src/main/java/domain/state/ActiveTurn.java`, 현재 줄 13, 원래 줄 9
- 답변 대상: [코멘트 3027261952](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027261952)
- 소속 리뷰 ID: 4054443479

> 장기 게임 한판에 턴 변경이 많이 일어나고 단순하게 두 상태일 뿐인데 매번 새로운 객체를 호출하는 건 비효율적이라고 느껴져서 TurnState 인터페이스에 상수를 선언해서 사용하는 방법으로 개선해 봤습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,14 @@
+package domain.state;
+
+public class ActiveTurn implements TurnState {
+
+    @Override
+    public boolean isCurrent() {
+        return true;
+    }
+
```

</details>

### 인라인 코멘트 3034971819: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-04T02:24:23Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3034971819)
- 코드: `src/main/java/domain/strategy/Direction.java`, 현재 줄 None, 원래 줄 21
- 답변 대상: [코멘트 3027518593](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027518593)
- 소속 리뷰 ID: 4054443479

> 수정했습니다!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,60 @@
+package domain.strategy;
+
+import java.util.List;
+
+public enum Direction {
+    N(0, 1),
+    S(0, -1),
+    E(1, 0),
+    W(-1, 0),
+    NE(1, 1),
+    NW(-1, 1),
+    SE(1, -1),
+    SW(-1, -1);
+
+    private final int dx;
+    private final int dy;
+
+    Direction(int dx, int dy) {
+        this.dx = dx;
+        this.dy = dy;
+    }
```

</details>

### 인라인 코멘트 3034976747: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-04T02:29:41Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3034976747)
- 코드: `src/test/java/domain/board/FormationCommandTest.java`, 현재 줄 None, 원래 줄 11
- 답변 대상: [코멘트 3027501449](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027501449)
- 소속 리뷰 ID: 4054443479

> 수정했습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,26 @@
+package domain.board;
+
+import static org.assertj.core.api.Assertions.assertThat;
+import static org.assertj.core.api.Assertions.assertThatThrownBy;
+
+import org.junit.jupiter.api.Test;
+
+class FormationCommandTest {
+
+    @Test
+    void 포메이션_입력이_1_2_3_4_일때_정상_동작한다() {
```

</details>

### 인라인 코멘트 3034990364: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-04T02:43:06Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3034990364)
- 코드: `src/test/java/domain/piece/SoldierTest.java`, 현재 줄 None, 원래 줄 14
- 답변 대상: [코멘트 3027500300](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027500300)
- 소속 리뷰 ID: 4054443479

> 테스트도 SRP를 지켜야한다는 생각을 왜 못했을까요, 좋은 의견 감사합니다!
> 앞으로 더 신경쓰겠습니다~

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,30 @@
+package domain.piece;
+
+import static org.assertj.core.api.Assertions.assertThat;
+
+import domain.Position;
+import domain.Side;
+import domain.board.Board;
+import java.util.Map;
+import org.junit.jupiter.api.DisplayName;
+import org.junit.jupiter.api.Test;
+
+class SoldierTest {
+    @Test
+    @DisplayName("초나라 졸은 상/좌/우 이동이 가능하고 한나라 졸은 하/좌/우 이동이 가능하다")
```

</details>

### 인라인 코멘트 3035002262: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-04T02:49:38Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3035002262)
- 코드: `src/test/java/domain/player/PlayersTest.java`, 현재 줄 None, 원래 줄 12
- 답변 대상: [코멘트 3027262625](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027262625)
- 소속 리뷰 ID: 4054443479

> 실제로 서비스 운영 시 개발하는 입장에서 원인을 찾는데 아주 도움이 될 정보라고 생각되네요, 수정했습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,14 @@
+package domain.player;
+
+import static org.assertj.core.api.Assertions.assertThatThrownBy;
+
+import org.junit.jupiter.api.Test;
+
+class PlayersTest {
+
+    @Test
+    void 초기_플레이어_생성_시_두_플레이어의_이름이_같으면_예외가_발생한다() {
+        assertThatThrownBy(() -> Players.createInitial(new Name("whale"), new Name("whale")))
+                .isInstanceOf(IllegalArgumentException.class);
```

</details>

### 인라인 코멘트 3035003393: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-04T02:51:01Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3035003393)
- 코드: `src/test/java/domain/player/PlayerTest.java`, 현재 줄 45, 원래 줄 44
- 답변 대상: [코멘트 3027500547](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027500547)
- 소속 리뷰 ID: 4054443479

> 수정했습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,53 @@
+package domain.player;
+
+import static org.assertj.core.api.Assertions.assertThat;
+import static org.assertj.core.api.Assertions.assertThatThrownBy;
+
+import domain.Side;
+import domain.piece.Piece;
+import domain.piece.PieceFactory;
+import domain.state.ActiveTurn;
+import org.junit.jupiter.api.Test;
+
+class PlayerTest {
+
+    @Test
+    void 턴_상태를_토글하면_현재_턴_여부가_반전된다() {
+        // Given: 초나라 플레이어가 자신의 턴(ActiveTurn)인 상태로 생성
+        Player player = new Player(new Name("cho"), Side.CHO, new ActiveTurn());
+
+        // When: 턴을 한 번 토글 (Active -> Waiting)
+        player.toggleTurn();
+        // Then
+        assertThat(player.isCurrentTurn()).isFalse();
+
+        // When: 턴을 다시 토글 (Waiting -> Active)
+        player.toggleTurn();
+        // Then
+        assertThat(player.isCurrentTurn()).isTrue();
+    }
+
+    @Test
+    void 플레이어는_자신의_기물이_아닌_상대방의_기물을_검증하면_예외가_발생한다() {
+        // Given: 초나라 플레이어와 한나라 졸(Soldier)
+        Player choPlayer = new Player(new Name("cho"), Side.CHO, new ActiveTurn());
+
+        // PieceFactory를 사용하여 실제 도메인과 동일한 기물 생성 (전략 주입 포함)
+        Piece hanPiece = PieceFactory.createSoldier(Side.HAN);
+
+        // When & Then: 초나라 플레이어가 한나라 기물을 validateAlly 할 때 예외 발생
+        assertThatThrownBy(() -> choPlayer.validateAlly(hanPiece))
+                .isInstanceOf(IllegalArgumentException.class)
+                .hasMessageContaining("상대방의 기물은 움직일 수 없습니다.");
+    }
+
+    @Test
```

</details>

### 인라인 코멘트 3035011005: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-04T02:58:43Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3035011005)
- 코드: `src/test/java/domain/PositionTest.java`, 현재 줄 9, 원래 줄 9
- 답변 대상: [코멘트 3027357721](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027357721)
- 소속 리뷰 ID: 4054443479

> 이러한 테스트를 진행할 때마다 고민이 있었는데 범위 검사인 경우에 경계값만 테스트하는 것이 중복 제거와 테스트 의도를 명확하게 전달할 수 있는 이점이 있다고 생각되네요, 수정했습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,45 @@
+package domain;
+
+import static org.assertj.core.api.Assertions.assertThatCode;
+import static org.assertj.core.api.Assertions.assertThatThrownBy;
+
+import org.junit.jupiter.params.ParameterizedTest;
+import org.junit.jupiter.params.provider.ValueSource;
+
+class PositionTest {
```

</details>

### 인라인 코멘트 3035078715: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-04T04:00:04Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3035078715)
- 코드: `src/main/java/controller/JanggiConsoleController.java`, 현재 줄 17, 원래 줄 14
- 답변 대상: [코멘트 3027259174](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027259174)
- 소속 리뷰 ID: 4054443479

> 도메인과 뷰의 의존성 제거를 하기 위해 중간 계층을 도입했습니다.
> 이름을 고민했지만 콘솔 환경의 입출력 흐름을 제어하는 의미로 JanggiConsoleController라고 지어봤습니다.
> 도메인에 있던 toString or String 필드들을 삭제하고 DTO 객체를 활용해봤습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,89 @@
+package domain;
+
+import domain.board.Board;
+import domain.board.BoardFactory;
+import domain.board.Formation;
+import domain.board.FormationCommand;
+import domain.player.Name;
+import domain.player.Players;
+import java.util.List;
+import java.util.function.Supplier;
+import view.InputParser;
+import view.InputView;
+import view.OutputView;
+
```

</details>

### 인라인 코멘트 3035082036: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-04T04:03:35Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3035082036)
- 코드: `src/main/java/domain/Game.java`, 현재 줄 35, 원래 줄 45
- 답변 대상: [코멘트 3027259859](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027259859)
- 소속 리뷰 ID: 4054443479

> Board가 생성시에 Map.copyOf()를 수행해서 불변이 보장 되어있습니다.
> view로 바로 전달하지 않고 DTO 객체에서 변환하여 Map 구조에 대한 노출을 줄이고 데이터만 전송하는 식으로 시도해봤습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,53 @@
+package domain;
+
+import domain.board.Board;
+import domain.piece.Piece;
+import domain.player.Players;
+import java.util.Map;
+
+public class Game {
+    private Board board;
+    private final Players players;
+
+    public Game(Board board, Players players) {
+        this.board = board;
+        this.players = players;
+    }
+
+    public Side getCurrentSide() {
+        return players.getCurrentSide();
+    }
+
+    public Destinations selectSource(Position position) {
+        Piece piece = board.getPiece(position);
+        players.getCurrentPlayer().validateAlly(piece);
+        return findDestinations(position);
+    }
+
+    public void move(Position source, Position target) {
+        Destinations destinations = selectSource(source);
+        destinations.validateDestinations(target);
+        movePiece(source, target);
+        players.switchPlayer();
+    }
+
+    private Destinations findDestinations(Position position) {
+        return board.findDestinations(position);
+    }
+
+    private void movePiece(Position source, Position target) {
+        this.board = board.movePiece(source, target);
+    }
+
+    public Map<Position, Piece> getBoard() {
+        return board.getBoard();
+    }
+
```

</details>

### 리뷰 본문 4054443479: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-04T04:04:09Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#pullrequestreview-4054443479)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 3035601915: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-04T13:47:21Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3035601915)
- 코드: `src/main/java/domain/state/ActiveTurn.java`, 현재 줄 13, 원래 줄 9
- 답변 대상: [코멘트 3027261952](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027261952)
- 소속 리뷰 ID: 4058526185

> 상수선언하신것은 좋은데요
>
> 하위 구현체를 상위 구현체에서 참조하게 되어서 추상화가 깨지게되는것 같네요 상수 선언위치를 변경해보는건 어떨까요

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,14 @@
+package domain.state;
+
+public class ActiveTurn implements TurnState {
+
+    @Override
+    public boolean isCurrent() {
+        return true;
+    }
+
```

</details>

### 리뷰 본문 4058526185: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-04T13:47:21Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#pullrequestreview-4058526185)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 3035620029: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-04T14:05:36Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3035620029)
- 코드: `src/main/java/domain/strategy/Path.java`, 현재 줄 None, 원래 줄 42
- 답변 대상: [코멘트 3027528117](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027528117)
- 소속 리뷰 ID: 4058538593

> 모든 경우에 대해 상수로 표현하는것은 그렇게 좋지는 않다고 생각하는 편이긴한데요.
>
> 의미를 상수로 표현하는것과 그렇지 않은 경우를 구분하는 경우가 있는것 같네요.
>
> 가령 에러 메세지같은 경우에는 상수로 추출하는걸 별로 선호하지 않는편 같습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,52 @@
+package domain.strategy;
+
+import domain.Position;
+import domain.board.BoardReader;
+import java.util.List;
+import java.util.Optional;
+import java.util.function.Predicate;
+
+public class Path {
+    private final List<Position> steps;
+
+    public Path(List<Position> steps) {
+        this.steps = List.copyOf(steps);
+    }
+
+    public Path takeWhile(Predicate<Position> condition) {
+        List<Position> result = steps.stream()
+                .takeWhile(condition)
+                .toList();
+        return new Path(result);
+    }
+
+    public Optional<Position> findFirst(Predicate<Position> condition) {
+        return steps.stream()
+                .filter(condition)
+                .findFirst();
+    }
+
+    public Path after(Position target) {
+        int index = steps.indexOf(target);
+        if (index == -1 || index == steps.size() - 1) {
+            return new Path(List.of());
+        }
+        return new Path(steps.subList(index + 1, steps.size()));
+    }
+
+    public boolean isBlocked(BoardReader board) {
+        if (steps.size() <= 1) {
+            return false;
+        }
+        return steps.subList(0, steps.size() - 1).stream()
+                .anyMatch(pos -> !board.isEmpty(pos));
```

</details>

### 리뷰 본문 4058538593: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-04T14:05:36Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#pullrequestreview-4058538593)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 3035621656: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-04T14:07:27Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3035621656)
- 코드: `src/main/java/domain/board/Board.java`, 현재 줄 None, 원래 줄 34
- 소속 리뷰 ID: 4058539769

> 이 메서드의 경우 프로덕션 코드에서 부정표현을 위해 `!`를 사용하고 있는데요. 처음부터 부정표현을 담은 이름을 짓는게 낫지 않을까요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,76 @@
+package domain.board;
+
+import domain.Destinations;
+import domain.Position;
+import domain.Side;
+import domain.piece.Piece;
+import java.util.HashMap;
+import java.util.List;
+import java.util.Map;
+
+public class Board implements BoardReader{
+    public static final int MINIMUM_VITAL_PIECES_COUNT = 2;
+    private final Map<Position, Piece> board;
+
+    public Board(Map<Position, Piece> board) {
+        this.board = Map.copyOf(board);
+    }
+
+    public Destinations findDestinations(Position position) {
+        Piece piece = getPiece(position);
+        return piece.findDestinations(position, this);
+    }
+
+    public Board movePiece(Position source, Position target) {
+        Map<Position, Piece> nextBoardMap = new HashMap<>(this.board);
+        Piece movingPiece = nextBoardMap.remove(source);
+        if (movingPiece == null) {
+            throw new IllegalArgumentException("출발지에 기물이 존재하지 않습니다.");
+        }
+        nextBoardMap.put(target, movingPiece);
+        return new Board(nextBoardMap);
+    }
+
+    public boolean isGameOver() {
```

</details>

### 인라인 코멘트 3035626140: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-04T14:12:16Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3035626140)
- 코드: `src/main/java/domain/Game.java`, 현재 줄 None, 원래 줄 36
- 소속 리뷰 ID: 4058539769

> 혹시 이 private 메서드는 어떤 이유로 만드신걸까요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,54 @@
+package domain;
+
+import domain.board.Board;
+import domain.piece.Piece;
+import domain.player.Players;
+import java.util.Map;
+
+public class Game {
+    private Board board;
+    private final Players players;
+
+    public Game(Board board, Players players) {
+        this.board = board;
+        this.players = players;
+    }
+
+    public Side getCurrentSide() {
+        return players.getCurrentSide();
+    }
+
+    public MoveCandidate selectSource(Position source) {
+        Piece selectedPiece = board.getPiece(source);
+        players.validateAlly(selectedPiece);
+        Destinations destinations = findDestinations(source);
+        return new MoveCandidate(source, destinations);
+    }
+
+    public void move(MoveCandidate moveCandidate, Position target) {
+        moveCandidate.validate(target);
+        movePiece(moveCandidate.source(), target);
+        players.switchPlayer();
+    }
+
+    private Destinations findDestinations(Position position) {
+        return board.findDestinations(position);
+    }
```

</details>

### 인라인 코멘트 3035627287: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-04T14:13:18Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3035627287)
- 코드: `src/main/java/domain/board/Board.java`, 현재 줄 21, 원래 줄 21
- 소속 리뷰 ID: 4058539769

> 양방향 의존성이 생긴것 같네요.
>
> 이 부분은 해결할 수 없을까요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,76 @@
+package domain.board;
+
+import domain.Destinations;
+import domain.Position;
+import domain.Side;
+import domain.piece.Piece;
+import java.util.HashMap;
+import java.util.List;
+import java.util.Map;
+
+public class Board implements BoardReader{
+    public static final int MINIMUM_VITAL_PIECES_COUNT = 2;
+    private final Map<Position, Piece> board;
+
+    public Board(Map<Position, Piece> board) {
+        this.board = Map.copyOf(board);
+    }
+
+    public Destinations findDestinations(Position position) {
+        Piece piece = getPiece(position);
+        return piece.findDestinations(position, this);
```

</details>

### 인라인 코멘트 3035628965: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-04T14:15:10Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3035628965)
- 코드: `src/main/java/domain/strategy/MovementStrategy.java`, 현재 줄 None, 원래 줄 13
- 소속 리뷰 ID: 4058539769

> 인터페이스에서 디폴트 메서드를 사용하는 경우는 기존 인터페이스의 구현체가 존재하는 상황에서 새로운 스펙을 제공할때 안정적으로 하위 구현체의 호환성을 깨지 않게하기 위함인데요. 지금 그 의도로 사용하신게 맞을까요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,22 @@
+package domain.strategy;
+
+import domain.Position;
+import domain.Side;
+import domain.board.BoardReader;
+import java.util.ArrayList;
+import java.util.List;
+
+public interface MovementStrategy {
+    List<Path> generatePaths(Position current);
+    List<Position> getMovablePositions(Position current, BoardReader board, Side side);
+
+    default Path createPath(Position current, Direction direction) {
```

</details>

### 인라인 코멘트 3035630526: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-04T14:16:54Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3035630526)
- 코드: `src/main/java/domain/piece/Piece.java`, 현재 줄 None, 원래 줄 21
- 소속 리뷰 ID: 4058539769

> 메서드의 파라미터가 3개네요!
>
> 단순히 객체를 랩핑해서 줄이는게 아닌 다른방식을 이용해 2개 이하로 줄일수 있는 방법이 없을까요?
>
>

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,43 @@
+package domain.piece;
+
+import domain.Destinations;
+import domain.Position;
+import domain.Side;
+import domain.board.BoardReader;
+import domain.strategy.MovementStrategy;
+
+public abstract class Piece {
+    private final Side side;
+    private final MovementStrategy movementStrategy;
+
+    protected Piece(Side side, MovementStrategy movementStrategy) {
+        this.side = side;
+        this.movementStrategy = movementStrategy;
+    }
+
+    public abstract PieceType getType();
+
+    public Destinations findDestinations(Position current, BoardReader board) {
+        return new Destinations(movementStrategy.getMovablePositions(current, board, side));
```

</details>

### 인라인 코멘트 3035646961: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-04T14:34:44Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3035646961)
- 코드: `src/main/java/domain/piece/Piece.java`, 현재 줄 None, 원래 줄 21
- 답변 대상: [코멘트 3035630526](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3035630526)
- 소속 리뷰 ID: 4058539769

> 이 부분 말고도 다른 부분에도 3개인 부분이 간혹 보이는데요
>
> 이미 만들어진 객체에게 책임을 부여하거나, 구조를 변경해서 파라미터 갯수를 줄이도록 시도해보시면 좋을것 같습니다

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,43 @@
+package domain.piece;
+
+import domain.Destinations;
+import domain.Position;
+import domain.Side;
+import domain.board.BoardReader;
+import domain.strategy.MovementStrategy;
+
+public abstract class Piece {
+    private final Side side;
+    private final MovementStrategy movementStrategy;
+
+    protected Piece(Side side, MovementStrategy movementStrategy) {
+        this.side = side;
+        this.movementStrategy = movementStrategy;
+    }
+
+    public abstract PieceType getType();
+
+    public Destinations findDestinations(Position current, BoardReader board) {
+        return new Destinations(movementStrategy.getMovablePositions(current, board, side));
```

</details>

### 인라인 코멘트 3035647418: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-04T14:35:11Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3035647418)
- 코드: `src/main/java/domain/strategy/JumpStrategy.java`, 현재 줄 None, 원래 줄 34
- 소속 리뷰 ID: 4058539769

> `pos`도 축약이네요~

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,54 @@
+package domain.strategy;
+
+import domain.Position;
+import domain.Side;
+import domain.board.BoardReader;
+import domain.piece.Piece;
+import java.util.ArrayList;
+import java.util.List;
+import java.util.Optional;
+
+public class JumpStrategy implements MovementStrategy {
+    private final List<Direction> defaultDirections;
+
+    public JumpStrategy(List<Direction> defaultDirections) {
+        this.defaultDirections = defaultDirections;
+    }
+
+    @Override
+    public List<Path> generatePaths(Position current) {
+        return defaultDirections.stream()
+                .filter(current::canMove)
+                .map(direction -> createPath(current, direction))
+                .toList();
+    }
+
+    @Override
+    public List<Position> getMovablePositions(Position current, BoardReader board, Side side) {
+        return generatePaths(current).stream()
+                .flatMap(path -> getReachablePositions(path, board, side).stream())
+                .toList();
+    }
+
+    private List<Position> getReachablePositions(Path path, BoardReader board, Side side) {
+        return path.findFirst(pos -> !board.isEmpty(pos))
```

</details>

### 인라인 코멘트 3035653562: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-04T14:41:27Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3035653562)
- 코드: `src/main/java/domain/board/Board.java`, 현재 줄 24, 원래 줄 24
- 소속 리뷰 ID: 4058539769

> 이 메서드 아무런 방어로직과 검증이 거치지 않은상태에서도 기물의 움직임이 가능해보이네요. 절차적인 호출로만 올바른 도메인 로직이 동작할것 같습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,76 @@
+package domain.board;
+
+import domain.Destinations;
+import domain.Position;
+import domain.Side;
+import domain.piece.Piece;
+import java.util.HashMap;
+import java.util.List;
+import java.util.Map;
+
+public class Board implements BoardReader{
+    public static final int MINIMUM_VITAL_PIECES_COUNT = 2;
+    private final Map<Position, Piece> board;
+
+    public Board(Map<Position, Piece> board) {
+        this.board = Map.copyOf(board);
+    }
+
+    public Destinations findDestinations(Position position) {
+        Piece piece = getPiece(position);
+        return piece.findDestinations(position, this);
+    }
+
+    public Board movePiece(Position source, Position target) {
```

</details>

### 리뷰 본문 4058539769: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-04T14:43:30Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#pullrequestreview-4058539769)
- 리뷰 상태: `CHANGES_REQUESTED`

> 조금 더 개선해보면 좋을 부분에 리뷰를 남겨두었으니 확인해주세요

### 인라인 코멘트 3036286271: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-05T02:00:50Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3036286271)
- 코드: `src/main/java/domain/strategy/JumpStrategy.java`, 현재 줄 None, 원래 줄 34
- 답변 대상: [코멘트 3035647418](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3035647418)
- 소속 리뷰 ID: 4059018354

> 수정했습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,54 @@
+package domain.strategy;
+
+import domain.Position;
+import domain.Side;
+import domain.board.BoardReader;
+import domain.piece.Piece;
+import java.util.ArrayList;
+import java.util.List;
+import java.util.Optional;
+
+public class JumpStrategy implements MovementStrategy {
+    private final List<Direction> defaultDirections;
+
+    public JumpStrategy(List<Direction> defaultDirections) {
+        this.defaultDirections = defaultDirections;
+    }
+
+    @Override
+    public List<Path> generatePaths(Position current) {
+        return defaultDirections.stream()
+                .filter(current::canMove)
+                .map(direction -> createPath(current, direction))
+                .toList();
+    }
+
+    @Override
+    public List<Position> getMovablePositions(Position current, BoardReader board, Side side) {
+        return generatePaths(current).stream()
+                .flatMap(path -> getReachablePositions(path, board, side).stream())
+                .toList();
+    }
+
+    private List<Position> getReachablePositions(Path path, BoardReader board, Side side) {
+        return path.findFirst(pos -> !board.isEmpty(pos))
```

</details>

### 인라인 코멘트 3036301843: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-05T02:23:24Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3036301843)
- 코드: `src/main/java/domain/state/ActiveTurn.java`, 현재 줄 13, 원래 줄 9
- 답변 대상: [코멘트 3027261952](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3027261952)
- 소속 리뷰 ID: 4059018354

> 인터페이스가 구체 클래스를 의존하여 추상화가 깨지는 문제를 해결하기 위해 두 가지 대안을 고민했습니다.
>
> 1. 구체 클래스 간 직접 참조 (현재 구조 유지)
> 2. Enum으로의 전환
>
> 장기 도메인 특성상 턴의 종류가 늘어날 확률은 낮아 2번도 타당한 선택지라고 생각했습니다.
> 하지만 추후 각 턴 객체에 고유한 비즈니스 로직이나 제약 조건이 추가될 수 있는 확장성을 열어두고 싶었고, 기존의 클래스 구조를 Enum으로 전면 재작성하는 비용 대비 얻는 이득이 크지 않다고 판단하여 1번 방식을 선택했습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,14 @@
+package domain.state;
+
+public class ActiveTurn implements TurnState {
+
+    @Override
+    public boolean isCurrent() {
+        return true;
+    }
+
```

</details>

### 인라인 코멘트 3036315780: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-05T02:43:26Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3036315780)
- 코드: `src/main/java/domain/strategy/MovementStrategy.java`, 현재 줄 None, 원래 줄 13
- 답변 대상: [코멘트 3035628965](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3035628965)
- 소속 리뷰 ID: 4059018354

> 공통적으로 재사용 중복이 발생한 이유로 사용을 했는데 인터페이스와 구현의 분리를 위배하게 된 것 같습니다.
> 다시 보니 Path 생성 책임으로 보여 Path에 있는 것이 적절하다고 판단되어서 옮겨봤습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,22 @@
+package domain.strategy;
+
+import domain.Position;
+import domain.Side;
+import domain.board.BoardReader;
+import java.util.ArrayList;
+import java.util.List;
+
+public interface MovementStrategy {
+    List<Path> generatePaths(Position current);
+    List<Position> getMovablePositions(Position current, BoardReader board, Side side);
+
+    default Path createPath(Position current, Direction direction) {
```

</details>

### 인라인 코멘트 3036443554: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-05T05:37:58Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3036443554)
- 코드: `src/main/java/domain/Game.java`, 현재 줄 None, 원래 줄 36
- 답변 대상: [코멘트 3035626140](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3035626140)
- 소속 리뷰 ID: 4059018354

> board 인스턴스로 바로 접근이 가능해서 필요없다고 여겨지네요, 실수한 것 같아요.
> 삭제했습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,54 @@
+package domain;
+
+import domain.board.Board;
+import domain.piece.Piece;
+import domain.player.Players;
+import java.util.Map;
+
+public class Game {
+    private Board board;
+    private final Players players;
+
+    public Game(Board board, Players players) {
+        this.board = board;
+        this.players = players;
+    }
+
+    public Side getCurrentSide() {
+        return players.getCurrentSide();
+    }
+
+    public MoveCandidate selectSource(Position source) {
+        Piece selectedPiece = board.getPiece(source);
+        players.validateAlly(selectedPiece);
+        Destinations destinations = findDestinations(source);
+        return new MoveCandidate(source, destinations);
+    }
+
+    public void move(MoveCandidate moveCandidate, Position target) {
+        moveCandidate.validate(target);
+        movePiece(moveCandidate.source(), target);
+        players.switchPlayer();
+    }
+
+    private Destinations findDestinations(Position position) {
+        return board.findDestinations(position);
+    }
```

</details>

### 인라인 코멘트 3036455878: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-05T05:54:30Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3036455878)
- 코드: `src/main/java/domain/board/Board.java`, 현재 줄 None, 원래 줄 34
- 답변 대상: [코멘트 3035621656](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3035621656)
- 소속 리뷰 ID: 4059018354

> 부정 연산자를 재해석을 안해도 되니깐 좋은 것 같네요, 좋은 지적 감사합니다!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,76 @@
+package domain.board;
+
+import domain.Destinations;
+import domain.Position;
+import domain.Side;
+import domain.piece.Piece;
+import java.util.HashMap;
+import java.util.List;
+import java.util.Map;
+
+public class Board implements BoardReader{
+    public static final int MINIMUM_VITAL_PIECES_COUNT = 2;
+    private final Map<Position, Piece> board;
+
+    public Board(Map<Position, Piece> board) {
+        this.board = Map.copyOf(board);
+    }
+
+    public Destinations findDestinations(Position position) {
+        Piece piece = getPiece(position);
+        return piece.findDestinations(position, this);
+    }
+
+    public Board movePiece(Position source, Position target) {
+        Map<Position, Piece> nextBoardMap = new HashMap<>(this.board);
+        Piece movingPiece = nextBoardMap.remove(source);
+        if (movingPiece == null) {
+            throw new IllegalArgumentException("출발지에 기물이 존재하지 않습니다.");
+        }
+        nextBoardMap.put(target, movingPiece);
+        return new Board(nextBoardMap);
+    }
+
+    public boolean isGameOver() {
```

</details>

### 인라인 코멘트 3036481822: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-05T06:25:49Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3036481822)
- 코드: `src/main/java/domain/board/Board.java`, 현재 줄 24, 원래 줄 24
- 답변 대상: [코멘트 3035653562](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3035653562)
- 소속 리뷰 ID: 4059018354

> 정확한 지적 감사합니다.
> 기존 코드는 외부(Controller나 Game)에서 사전에 검증을 완벽하게 마쳤을 것이라고 맹신하는 '절차지향적'인 느낌이 있었습니다. 말씀해주신 대로 도메인 객체가 자신의 상태 무결성을 책임지도록 설계해야한다는 것을 다시 깨달았습니다.
> Game에서 보장해줘야할 부분, Board에서 보장해줘야할 부분들에 고민하면서 코드 수정을 해봤습니다.
>

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,76 @@
+package domain.board;
+
+import domain.Destinations;
+import domain.Position;
+import domain.Side;
+import domain.piece.Piece;
+import java.util.HashMap;
+import java.util.List;
+import java.util.Map;
+
+public class Board implements BoardReader{
+    public static final int MINIMUM_VITAL_PIECES_COUNT = 2;
+    private final Map<Position, Piece> board;
+
+    public Board(Map<Position, Piece> board) {
+        this.board = Map.copyOf(board);
+    }
+
+    public Destinations findDestinations(Position position) {
+        Piece piece = getPiece(position);
+        return piece.findDestinations(position, this);
+    }
+
+    public Board movePiece(Position source, Position target) {
```

</details>

### 인라인 코멘트 3036495936: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-05T06:42:41Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3036495936)
- 코드: `src/main/java/domain/board/Board.java`, 현재 줄 21, 원래 줄 21
- 답변 대상: [코멘트 3035627287](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3035627287)
- 소속 리뷰 ID: 4059018354

> 지적해 주신 부분에 대해 고민해 보았습니다.
> 하지만 현재 설계는 구체 클래스 간의 양방향 의존성이 아닌, 추상화를 통해 의존성 사이클을 끊어낸 단방향 구조로 판단했습니다.
> 왜냐하면 `Board`는 `Piece`를 의존하지만, `Piece`는 `Board`를 모르고, `BoardReader`라는 추상화된 인터페이스만 알고 있다고 판단했습니다.
> 만약에 Piece에게 할당한 책임들을 분리한다면, `Board`나 새로운 외부 객체의 협력이 필요해질 것으로 보입니다.
> 이동 조건을 무시한 위치에 따른 경로를 응답, 응답을 기물의 타입을 체크해서 최종 경로 선택이 필요해질 것으로 생각이 드는데 기물의 종류를 체크해야한다는 점에서 해당 설계가 하기 싫다고 느껴졌었습니다.
> 다른 좋은 방법이 있을까요?
>

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,76 @@
+package domain.board;
+
+import domain.Destinations;
+import domain.Position;
+import domain.Side;
+import domain.piece.Piece;
+import java.util.HashMap;
+import java.util.List;
+import java.util.Map;
+
+public class Board implements BoardReader{
+    public static final int MINIMUM_VITAL_PIECES_COUNT = 2;
+    private final Map<Position, Piece> board;
+
+    public Board(Map<Position, Piece> board) {
+        this.board = Map.copyOf(board);
+    }
+
+    public Destinations findDestinations(Position position) {
+        Piece piece = getPiece(position);
+        return piece.findDestinations(position, this);
```

</details>

### 인라인 코멘트 3036510054: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-05T06:59:35Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3036510054)
- 코드: `src/main/java/domain/piece/Piece.java`, 현재 줄 None, 원래 줄 21
- 답변 대상: [코멘트 3035630526](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3035630526)
- 소속 리뷰 ID: 4059018354

> Piece가 가지고 있는 진영(Side) 상태에 대한 검증을 이동전략 객체에 위임을 해버렸었네요, 그 부분을 Piece에서 책임지도록 했더니 side 파라미터를 제거할 수 있었습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,43 @@
+package domain.piece;
+
+import domain.Destinations;
+import domain.Position;
+import domain.Side;
+import domain.board.BoardReader;
+import domain.strategy.MovementStrategy;
+
+public abstract class Piece {
+    private final Side side;
+    private final MovementStrategy movementStrategy;
+
+    protected Piece(Side side, MovementStrategy movementStrategy) {
+        this.side = side;
+        this.movementStrategy = movementStrategy;
+    }
+
+    public abstract PieceType getType();
+
+    public Destinations findDestinations(Position current, BoardReader board) {
+        return new Destinations(movementStrategy.getMovablePositions(current, board, side));
```

</details>

### 리뷰 본문 4059018354: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-05T07:19:20Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#pullrequestreview-4059018354)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 3036798042: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-05T12:20:45Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3036798042)
- 코드: `src/main/java/domain/board/Board.java`, 현재 줄 21, 원래 줄 21
- 답변 대상: [코멘트 3035627287](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3035627287)
- 소속 리뷰 ID: 4059428099

> 앗 인터페이스가 있었군요 의존성 사이클은 끊어져있었네요

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,76 @@
+package domain.board;
+
+import domain.Destinations;
+import domain.Position;
+import domain.Side;
+import domain.piece.Piece;
+import java.util.HashMap;
+import java.util.List;
+import java.util.Map;
+
+public class Board implements BoardReader{
+    public static final int MINIMUM_VITAL_PIECES_COUNT = 2;
+    private final Map<Position, Piece> board;
+
+    public Board(Map<Position, Piece> board) {
+        this.board = Map.copyOf(board);
+    }
+
+    public Destinations findDestinations(Position position) {
+        Piece piece = getPiece(position);
+        return piece.findDestinations(position, this);
```

</details>

### 리뷰 본문 4059428099: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-05T12:20:45Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#pullrequestreview-4059428099)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 3036799020: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-05T12:21:49Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3036799020)
- 코드: `src/main/java/domain/board/Board.java`, 현재 줄 21, 원래 줄 21
- 답변 대상: [코멘트 3035627287](https://github.com/woowacourse/java-janggi/pull/269#discussion_r3035627287)
- 소속 리뷰 ID: 4059428892

> 제가 놓쳤었네요~ 넘어가주세요

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,76 @@
+package domain.board;
+
+import domain.Destinations;
+import domain.Position;
+import domain.Side;
+import domain.piece.Piece;
+import java.util.HashMap;
+import java.util.List;
+import java.util.Map;
+
+public class Board implements BoardReader{
+    public static final int MINIMUM_VITAL_PIECES_COUNT = 2;
+    private final Map<Position, Piece> board;
+
+    public Board(Map<Position, Piece> board) {
+        this.board = Map.copyOf(board);
+    }
+
+    public Destinations findDestinations(Position position) {
+        Piece piece = getPiece(position);
+        return piece.findDestinations(position, this);
```

</details>

### 리뷰 본문 4059428892: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-05T12:21:49Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#pullrequestreview-4059428892)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 리뷰 본문 4059431240: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-05T12:25:09Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/269#pullrequestreview-4059431240)
- 리뷰 상태: `APPROVED`

> 이번 사이클은 여기서 마무리해도 좋을것 같습니다~
>
> 고생 많으셨습니다
>
> merge하겠습니다. 🚀
