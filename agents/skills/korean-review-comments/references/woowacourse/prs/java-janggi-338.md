# woowacourse/java-janggi #338

[🚀 사이클2 - 미션 (기물 확장 + DB 적용)] 고래 미션 제출합니다.

- [GitHub PR](https://github.com/woowacourse/java-janggi/pull/338)
- PR 작성자: `miniminjae92`
- 머지 시각: 2026-04-11T01:59:44Z
- [API 원본](../raw/java-janggi-338.json)
- 리뷰와 댓글 27건(본문 있는 발언 23건, 본인 기록 8건)

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
> <!-- 리뷰어가 효과적으로 피드백할 수 있도록 중점적으로 피드백받고 싶은 내용을 공유해주세요.
> 예를 들어, 가장 고민했던 점이나 여전히 어려운 부분, 그리고 이에 대한 생각을 적을 수 있습니다. -->
>
> 안녕하세요 비밥!
> 리뷰 신청이 많이 늦었네요, DB를 사용해보는 게 처음이라 낯선 개념들이 많아 시간이 걸린 것 같습니다.
>
> 지금 생각나는 추가적인 궁금한 사항들을 작성해보자면,
>
> 2단계 영속성에 들어갈 때쯤 느낀 것이 궁, 사, 쫄을 하나의 원스텝 이동전략으로 최대한 다룰려고 했는데 궁성 내 병/쫄의 이동 부분에서 결국 Soldier 클래스에 Overriding을 했습니다. 그러면서 전진만하는전략을 하나 더 만들어서 사용하는 게 더 좋았을 것 같다고 느끼는데 비밥의 의견
> 이 궁금합니다.
>
> 턴 객체를 플레이어에게 둔 것에 대해서 뒤늦게 이것이 괜찮은 판단이었는지 고민을 해봤습니다.
> 블랙잭에서 draw 행동과 상태패턴 활용한 것처럼 game에서 move라는 행동을 할 때 상태패턴처럼 활용하는 게 더 좋은 선택이었을까? 하는 생각이 들었는데 비밥의 의견이 궁금합니다!
>
> 사용자 입력을 받는 경우, 예를 들면 1,2,3,4와 같이 각각의 선택에 따라서 다른 비즈니스로직이 돌아가는 기능 목록 커맨드라고 가정할 때, if-else 조건문, switch-case, Enum 활용, Map 자료구조 활용 등 어떤 선택을 할지 매번 고민을 하는 것 같은데 좋은 인사이트를 얻을 수 있을까요?
>
> 테이블 설계를 하려고 할 때 단순하게 이 프로그램이 꺼지고 다시 시작될 때를 상상하면서 필요한 데이터들을 생각해봤습니다.
> 제가 설계한 도메인 아키텍처대로, 예를 들면 게임에 Players, board 상태가 있습니다.
> 각각의 객체에 또 객체들이 있는데요, 이러한 사고로 테이블을 설계하는 것이 아닌 것 같다고 느꼈는데 명시적인 근거를 잡는데 어려움을 느끼고 있습니다. 좋은 인사이트를 얻을 수 있을까요?
>
> 비밥, 항상 고생 많으십니다!
> 부족한 부분이 많지만 이번 리뷰도 잘 부탁드립니다~
>
>
>
>

## 대화와 리뷰 기록

### 일반 댓글 4212599926: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-09T08:04:02Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/338#issuecomment-4212599926)

> > 2단계 영속성에 들어갈 때쯤 느낀 것이 궁, 사, 쫄을 하나의 원스텝 이동전략으로 최대한 다룰려고 했는데 궁성 내 병/쫄의 이동 부분에서 결국 Soldier 클래스에 Overriding을 했습니다. 그러면서 전진만하는전략을 하나 더 만들어서 사용하는 게 더 좋았을 것 같다고 느끼는데 비밥의 의견
> 이 궁금합니다.
>
> 별도로 만드는게 더 좋아보여요~ 지금 구현상 filter가 외부로 노출되면서 책임이 분산된 느낌이 있는것 같네요.

### 일반 댓글 4212624974: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-09T08:08:29Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/338#issuecomment-4212624974)

> >턴 객체를 플레이어에게 둔 것에 대해서 뒤늦게 이것이 괜찮은 판단이었는지 고민을 해봤습니다.
> 블랙잭에서 draw 행동과 상태패턴 활용한 것처럼 game에서 move라는 행동을 할 때 상태패턴처럼 활용하는 게 더 좋은 선택이었을까? 하는 생각이 들었는데 비밥의 의견이 궁금합니다!
>
> 저라면 `player`가 알고 있게 하지는 않았을것 같습니다. 먼저 두명의 `player`의 상태를 동기적으로 맞추어 주어야 한다는 보장도 해주어야 하는점이 부담이 되는것 같아요. 그리고 `player`에서 반드시 관리를 해야만 하는가? 라는 질문에 명확한 답변이 생각나지 않는것 같아요. 다른 멤버변수와 응집도가 있는가? 에 대한 답도 생각나지 않는것 같구요. 말씀하신것처럼 `game` 에서 관리하는게 더 깔끔한 방향이지 않을까란 생각이 드네요.

### 일반 댓글 4212663583: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-09T08:15:21Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/338#issuecomment-4212663583)

> >사용자 입력을 받는 경우, 예를 들면 1,2,3,4와 같이 각각의 선택에 따라서 다른 비즈니스로직이 돌아가는 기능 목록 커맨드라고 가정할 때, if-else 조건문, switch-case, Enum 활용, Map 자료구조 활용 등 어떤 선택을 할지 매번 고민을 하는 것 같은데 좋은 인사이트를 얻을 수 있을까요?
>
> 좋은 고민이네요. 저는 보통 확장성을 고려하게되는것 같습니다. 지금 구현한 상태에서 새로운 커맨드가 추가된다고했을때 최소한의 공수가 들어가고, 최대한 빈틈이 없게 자동적으로 반영이 되려면 어떻게 구조를 작성해야하는가? 라는 생각을 하는것 같아요.
>
> 그래서 보통 테스트 코드에서 새로운 커멘드가 추가되었는데 반드시 반영해야하는 부분에 반영을 하지 않아
> 런타임에서 오류가 날수 있는 부분이 있다면 해당 부분을 검증할 수 있는 테스트 코드를 작성해두는것 같아요.
>
> 이렇게 방어적인 로직만 잘 작성되어있다면 메인코드는 어떻게 해도 큰 문제는 없다고 생각하나, 코드를 읽고 새로운 커맨드를 추가하는 입장이라고 한다면 `if-else` 구조는 눈치채기 쉽지 않은것 같습니다.
>
> 그런 면에서 enum은 `EnumSource` 라는 테스트 도구를 활용할 수 있어서 빈틈없이 로직을 작성하는데 좋은것 같아 선호하는편인것 같아요.

### 일반 댓글 4212669977: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-09T08:16:22Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/338#issuecomment-4212669977)

> >테이블 설계를 하려고 할 때 단순하게 이 프로그램이 꺼지고 다시 시작될 때를 상상하면서 필요한 데이터들을 생각해봤습니다.
> 제가 설계한 도메인 아키텍처대로, 예를 들면 게임에 Players, board 상태가 있습니다.
> 각각의 객체에 또 객체들이 있는데요, 이러한 사고로 테이블을 설계하는 것이 아닌 것 같다고 느꼈는데 명시적인 근거를 잡는데 어려움을 느끼고 있습니다. 좋은 인사이트를 얻을 수 있을까요?
>
> 질문이 잘 이해가 되지 않는데요. 조금 더 자세하게 설명해주실수있나요? 댓글로 달아주시고 dm 주시면 확인하고 다시 답변드릴게요~

### 인라인 코멘트 3056431064: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-09T08:19:45Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/338#discussion_r3056431064)
- 코드: `src/main/java/janggi/service/GameService.java`, 현재 줄 23, 원래 줄 22
- 소속 리뷰 ID: 4080778401

> `GameService`가 `currentGameId`와 `game`을 인스턴스 변수로 들고 있는데요, 이렇게 되면 `GameService`가 상태를 가진(stateful) 객체가 됩니다. 만약 나중에 여러 게임을 동시에 관리하거나, 서비스 객체를 싱글톤으로 사용하게 되면 문제가 생길 수 있어요.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,68 @@
+package janggi.service;
+
+import janggi.domain.Game;
+import janggi.domain.Side;
+import janggi.domain.board.Board;
+import janggi.domain.board.BoardFactory;
+import janggi.domain.board.Formation;
+import janggi.domain.player.Name;
+import janggi.domain.player.Players;
+import janggi.domain.repository.GameRepository;
+import janggi.domain.space.Position;
+import janggi.dto.BoardDto;
+import janggi.dto.DestinationDto;
+import janggi.dto.GameDto;
+import janggi.dto.WinnerDto;
+import java.util.List;
+
+public class GameService {
+    private final GameRepository gameRepository;
+    private Long currentGameId;
+    private Game game;
+
```

</details>

### 인라인 코멘트 3056431797: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-09T08:19:54Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/338#discussion_r3056431797)
- 코드: `src/main/java/janggi/infrastructure/dao/PieceDao.java`, 현재 줄 None, 원래 줄 37
- 소속 리뷰 ID: 4080778401

> `PieceDao`의 `findAllByGameId`와 `deleteAllByGameId` 메서드를 보면, `insertPieces`는 외부에서 `Connection`을 주입받는데 `findAllByGameId`는 내부에서 `DatabaseConnection.getConnection()`을 직접 호출하네요. 같은 DAO 안에서 커넥션 관리 방식이 일관되지 않은것 같아요

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,70 @@
+package janggi.infrastructure.dao;
+
+import janggi.domain.piece.Piece;
+import janggi.domain.space.Position;
+import janggi.infrastructure.dao.dto.PieceEntity;
+import janggi.infrastructure.db.DatabaseConnection;
+import java.sql.Connection;
+import java.sql.PreparedStatement;
+import java.sql.ResultSet;
+import java.sql.SQLException;
+import java.util.ArrayList;
+import java.util.List;
+import java.util.Map;
+
+public class PieceDao {
+
+    public void insertPieces(Connection connection, Long gameId, Map<Position, Piece> board) throws SQLException {
+        String sql = "INSERT INTO piece (game_id, x, y, side, piece_type) VALUES (?, ?, ?, ?, ?)";
+
+        try (PreparedStatement preparedStatement = connection.prepareStatement(sql)) {
+            for (Map.Entry<Position, Piece> entry : board.entrySet()) {
+                Position position = entry.getKey();
+                Piece piece = entry.getValue();
+
+                preparedStatement.setLong(1, gameId);
+                preparedStatement.setInt(2, position.getX());
+                preparedStatement.setInt(3, position.getY());
+                preparedStatement.setString(4, piece.getSide().name());
+                preparedStatement.setString(5, piece.getType().name());
+                preparedStatement.addBatch();
+            }
+            preparedStatement.executeBatch();
+        }
+    }
+
+    public List<PieceEntity> findAllByGameId(Long gameId) {
+        String sql = "SELECT * FROM piece WHERE game_id = ?";
```

</details>

### 인라인 코멘트 3056434326: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-09T08:20:25Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/338#discussion_r3056434326)
- 코드: `src/main/java/janggi/domain/repository/GameRepository.java`, 현재 줄 None, 원래 줄 12
- 소속 리뷰 ID: 4080778401

> `GameRepository`는 domain인데 `GameDto`는 domain 계층이 아닌것 같아요 도메인 계층이 다른 계층을 의존하지 않도록 하는게 변경에 취약하지 않은 구조를 만드는데 좋을것 같습니다

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,17 @@
+package janggi.domain.repository;
+
+import janggi.domain.Game;
+import janggi.dto.GameDto;
+import java.util.List;
+import java.util.Optional;
+
+public interface GameRepository {
+
+    Long save(Game game);
+
+    void update(Long id, Game game);
```

</details>

### 인라인 코멘트 3056434394: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-09T08:20:26Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/338#discussion_r3056434394)
- 코드: `src/test/java/janggi/infrastructure/repository/JdbcGameRepositoryTest.java`, 현재 줄 None, 원래 줄 28
- 소속 리뷰 ID: 4080778401

> `JdbcGameRepositoryTest`에서 `@BeforeEach`마다 schema.sql을 통째로 실행하고 있는데요, `PieceDaoTest`에서는 `@BeforeAll`로 스키마를 한 번만 생성하고 `@BeforeEach`에서 DELETE만 하는 방식을 쓰고 계시죠.
> 테스트 셋업을 위한 전략이 통일되면 좋을것 같아요

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,70 @@
+package janggi.infrastructure.repository;
+
+import static org.assertj.core.api.Assertions.assertThat;
+
+import janggi.domain.Game;
+import janggi.domain.Side;
+import janggi.domain.board.Board;
+import janggi.domain.board.BoardFactory;
+import janggi.domain.board.Formation;
+import janggi.domain.piece.Piece;
+import janggi.domain.player.Name;
+import janggi.domain.player.Players;
+import janggi.domain.space.Position;
+import janggi.infrastructure.dao.GameDao;
+import janggi.infrastructure.dao.PieceDao;
+import janggi.infrastructure.db.DatabaseConnection;
+import java.io.InputStream;
+import java.nio.charset.StandardCharsets;
+import java.sql.Connection;
+import java.sql.Statement;
+import java.util.Map;
+import org.junit.jupiter.api.BeforeEach;
+import org.junit.jupiter.api.Test;
+
+class JdbcGameRepositoryTest {
+    private JdbcGameRepository gameRepository;
+
+    @BeforeEach
```

</details>

### 인라인 코멘트 3056434395: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-09T08:20:26Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/338#discussion_r3056434395)
- 코드: `src/main/java/janggi/domain/Game.java`, 현재 줄 None, 원래 줄 62
- 소속 리뷰 ID: 4080778401

> `Game.getBoard()`가 `Map<Position, Piece>`를 직접 반환하고 있는데요, 이 메서드가 서비스에서 DTO 변환용으로도 쓰이고, `JdbcGameRepository`에서 DB 저장용으로도 쓰이고 있습니다.
>
> 도메인 객체의 내부 자료구조가 외부에 그대로 노출되면, `Board`의 내부 구현이 바뀔 때 영향 범위가 넓어지게 됩니다. `Board`가 필요한 정보를 제공하는 메서드를 별도로 두는 방식도 고려해보시면 어떨까요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -14,31 +17,49 @@ public Game(Board board, Players players) {
         this.players = players;
     }

-    public Side getCurrentSide() {
-        return players.getCurrentSide();
-    }
-
     public Destinations selectSource(Position source) {
         players.validateAlly(board.getPiece(source));
         return board.findDestinations(source);
     }

     public void move(Position source, Position target) {
+        validateGamePlaying();
         players.validateAlly(board.getPiece(source));
         this.board = board.movePiece(source, target);
         players.switchPlayer();
     }

-    public Map<Position, Piece> getBoard() {
-        return board.getBoard();
+    private void validateGamePlaying() {
+        if (!isPlaying()) {
+            throw new IllegalArgumentException("게임이 이미 종료되었습니다.");
+        }
     }

     public boolean isPlaying() {
         return board.isPlaying();
     }

-    public String getWinner() {
+    public Score calculateScore(Side side) {
+        if (side == Side.HAN) {
+            return board.calculateScore(side).plus(new Score(1.5));
+        }
+        return board.calculateScore(side);
+    }
+
+    public Name getWinner() {
         Side winnerSide = board.getWinnerSide();
         return players.getPlayerNameBySide(winnerSide);
     }
+
+    public Side getCurrentSide() {
+        return players.getCurrentSide();
+    }
+
+    public Name getPlayerNameBySide(Side side) {
+        return players.getPlayerNameBySide(side);
+    }
+
+    public Map<Position, Piece> getBoard() {
```

</details>

### 인라인 코멘트 3056540570: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-09T08:40:53Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/338#discussion_r3056540570)
- 코드: `src/main/java/janggi/infrastructure/repository/JdbcGameRepository.java`, 현재 줄 None, 원래 줄 65
- 소속 리뷰 ID: 4080778401

> 한번의 이동이 발생할때마다 매번 많은 양의 데이터가 insert 되는것으로 보여요. 꼭 모든 기물의 위치를 저장해야할까요? 이력(ex. history)을 이용하여 동일한 효과를 발생시킬수 있지 않을까요? 효율적인 데이터 저장 구조에 대해 고민해보시면 좋을것 같아요 조회를 비롯해서 고민해보세요~

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,115 @@
+package janggi.infrastructure.repository;
+
+import janggi.domain.Game;
+import janggi.domain.Side;
+import janggi.domain.board.Board;
+import janggi.domain.piece.Piece;
+import janggi.domain.piece.PieceFactory;
+import janggi.domain.piece.PieceType;
+import janggi.domain.player.Name;
+import janggi.domain.player.Players;
+import janggi.domain.repository.GameRepository;
+import janggi.domain.space.Position;
+import janggi.dto.GameDto;
+import janggi.infrastructure.dao.GameDao;
+import janggi.infrastructure.dao.PieceDao;
+import janggi.infrastructure.dao.dto.GameEntity;
+import janggi.infrastructure.dao.dto.PieceEntity;
+import janggi.infrastructure.db.DatabaseConnection;
+import java.sql.Connection;
+import java.sql.SQLException;
+import java.util.List;
+import java.util.Map;
+import java.util.Optional;
+import java.util.stream.Collectors;
+
+public class JdbcGameRepository implements GameRepository {
+    private final GameDao gameDao;
+    private final PieceDao pieceDao;
+
+    public JdbcGameRepository(GameDao gameDao, PieceDao pieceDao) {
+        this.gameDao = gameDao;
+        this.pieceDao = pieceDao;
+    }
+
+    @Override
+    public Long save(Game game) {
+        try (Connection connection = DatabaseConnection.getConnection()) {
+            connection.setAutoCommit(false);
+            try {
+                String choName = game.getPlayerNameBySide(Side.CHO).name();
+                String hanName = game.getPlayerNameBySide(Side.HAN).name();
+                String currentTurn = game.getCurrentSide().name();
+
+                Long gameId = gameDao.insertGame(connection, choName, hanName, currentTurn);
+                pieceDao.insertPieces(connection, gameId, game.getBoard());
+
+                connection.commit();
+                return gameId;
+            } catch (Exception e) {
+                connection.rollback();
+                throw new RuntimeException("새 게임 저장 중 롤백 발생", e);
+            }
+        } catch (SQLException e) {
+            throw new RuntimeException("DB 커넥션 오류", e);
+        }
+    }
+
+    @Override
+    public void update(Long id, Game game) {
+        try (Connection connection = DatabaseConnection.getConnection()) {
+            connection.setAutoCommit(false);
+            try {
+                gameDao.updateGame(connection, id, game.getCurrentSide().name(), game.isPlaying());
+                pieceDao.deleteAllByGameId(connection, id);
+                pieceDao.insertPieces(connection, id, game.getBoard());
```

</details>

### 리뷰 본문 4080778401: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-09T08:41:23Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/338#pullrequestreview-4080778401)
- 리뷰 상태: `CHANGES_REQUESTED`

> 고민을 많이한 흔적이 보이네요 👍
> 조금 더 개선해보면 좋을 부분에 리뷰를 남겨두었으니 확인해주세요

### 일반 댓글 4225453451: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-10T17:09:15Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/338#issuecomment-4225453451)

> > > 테이블 설계를 하려고 할 때 단순하게 이 프로그램이 꺼지고 다시 시작될 때를 상상하면서 필요한 데이터들을 생각해봤습니다.
> > > 제가 설계한 도메인 아키텍처대로, 예를 들면 게임에 Players, board 상태가 있습니다.
> > > 각각의 객체에 또 객체들이 있는데요, 이러한 사고로 테이블을 설계하는 것이 아닌 것 같다고 느꼈는데 명시적인 근거를 잡는데 어려움을 느끼고 있습니다. 좋은 인사이트를 얻을 수 있을까요?
> >
> > 질문이 잘 이해가 되지 않는데요. 조금 더 자세하게 설명해주실수있나요? 댓글로 달아주시고 dm 주시면 확인하고 다시 답변드릴게요~
>
> 도메인 객체 구조를 그대로 테이블 설계에 반영하다 보니, 독자적인 생명주기가 없는 작은 객체들(값 객체)까지 전부 테이블로 만들게 되어 구조가 너무 파편화되는 것 같습니다. 보통 Game처럼 중심이 되는 엔티티와 그에 종속된 하위 객체들을 DB에 저장할 때, 하나의 테이블에 밀어 넣는 기준과 테이블을 쪼개는 기준을 어떻게 잡으시는지 경험이 궁금합니다.

### 인라인 코멘트 3065815784: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-10T17:33:16Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/338#discussion_r3065815784)
- 코드: `src/main/java/janggi/domain/repository/GameRepository.java`, 현재 줄 None, 원래 줄 12
- 답변 대상: [코멘트 3056434326](https://github.com/woowacourse/java-janggi/pull/338#discussion_r3056434326)
- 소속 리뷰 ID: 4091420472

> 말씀하신 대로 도메인 계층인 GameRepository가 외부 UI 계층의 GameDto에 의존하는 것은 구조상 변경에 취약해진다고 판단했습니다.
>
> 도메인 패키지 내부에 목록 조회용 데이터 객체인 GameInfo를 추가해 Repository가 이를 반환하도록 수정하고, GameDto로의 변환 책임은 GameService로 옮겨 도메인의 순수성을 유지하도록 개선해봤습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,17 @@
+package janggi.domain.repository;
+
+import janggi.domain.Game;
+import janggi.dto.GameDto;
+import java.util.List;
+import java.util.Optional;
+
+public interface GameRepository {
+
+    Long save(Game game);
+
+    void update(Long id, Game game);
```

</details>

### 인라인 코멘트 3065840323: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-10T17:38:11Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/338#discussion_r3065840323)
- 코드: `src/main/java/janggi/domain/Game.java`, 현재 줄 None, 원래 줄 62
- 답변 대상: [코멘트 3056434395](https://github.com/woowacourse/java-janggi/pull/338#discussion_r3056434395)
- 소속 리뷰 ID: 4091420472

> 내부 자료구조 노출을 지양하고 캡슐화하는 부분을 자꾸 놓치네요! 감사합니다.
>
> 콜백 패턴이라는 것을 시도해봤습니다.
>
> 이 방식을 통해 Board의 내부 구현(Map 등)이 변경되더라도 외부 계층(DTO, Repository)이 영향받지 않도록 해봤는데, 혹시 현재 적용된 콜백 패턴 외에 내부 정보를 안전하게 제공할 수 있는 더 나은 방식이 있는지 비밥의 의견이 궁금합니다!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -14,31 +17,49 @@ public Game(Board board, Players players) {
         this.players = players;
     }

-    public Side getCurrentSide() {
-        return players.getCurrentSide();
-    }
-
     public Destinations selectSource(Position source) {
         players.validateAlly(board.getPiece(source));
         return board.findDestinations(source);
     }

     public void move(Position source, Position target) {
+        validateGamePlaying();
         players.validateAlly(board.getPiece(source));
         this.board = board.movePiece(source, target);
         players.switchPlayer();
     }

-    public Map<Position, Piece> getBoard() {
-        return board.getBoard();
+    private void validateGamePlaying() {
+        if (!isPlaying()) {
+            throw new IllegalArgumentException("게임이 이미 종료되었습니다.");
+        }
     }

     public boolean isPlaying() {
         return board.isPlaying();
     }

-    public String getWinner() {
+    public Score calculateScore(Side side) {
+        if (side == Side.HAN) {
+            return board.calculateScore(side).plus(new Score(1.5));
+        }
+        return board.calculateScore(side);
+    }
+
+    public Name getWinner() {
         Side winnerSide = board.getWinnerSide();
         return players.getPlayerNameBySide(winnerSide);
     }
+
+    public Side getCurrentSide() {
+        return players.getCurrentSide();
+    }
+
+    public Name getPlayerNameBySide(Side side) {
+        return players.getPlayerNameBySide(side);
+    }
+
+    public Map<Position, Piece> getBoard() {
```

</details>

### 인라인 코멘트 3065888228: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-10T17:48:26Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/338#discussion_r3065888228)
- 코드: `src/main/java/janggi/infrastructure/dao/PieceDao.java`, 현재 줄 None, 원래 줄 37
- 답변 대상: [코멘트 3056431797](https://github.com/woowacourse/java-janggi/pull/338#discussion_r3056431797)
- 소속 리뷰 ID: 4091420472

> Connection 획득 방식이 파편화된 점을 인지하고 애플리케이션, 컨트롤러, 서비스, 레포지토리, DAO 등 전체적으로 어느 곳에서 Connection을 일관되게 주입을 할까 고민을 했습니다.
>
> 저는 서비스레이어의 행동의 단위를 트랜잭션으로 봤기 때문에 서비스레이어가 좋겠다고 생각했습니다.
> 다만 서비스에 JDBC 의존성이 생기는 것을 피하고 싶어서 다른 방법들을 찾아보며 고민해봤습니다.
>
> 결정은 ConnectionContext(ThreadLocal)를 도입해 Service 계층에서 트랜잭션 경계를 설정하고, 모든 DAO는 ConnectionContext.get()을 통해 일관되게 동일한 커넥션을 사용하는 방법을 시도해봤는데 괜찮은가요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,70 @@
+package janggi.infrastructure.dao;
+
+import janggi.domain.piece.Piece;
+import janggi.domain.space.Position;
+import janggi.infrastructure.dao.dto.PieceEntity;
+import janggi.infrastructure.db.DatabaseConnection;
+import java.sql.Connection;
+import java.sql.PreparedStatement;
+import java.sql.ResultSet;
+import java.sql.SQLException;
+import java.util.ArrayList;
+import java.util.List;
+import java.util.Map;
+
+public class PieceDao {
+
+    public void insertPieces(Connection connection, Long gameId, Map<Position, Piece> board) throws SQLException {
+        String sql = "INSERT INTO piece (game_id, x, y, side, piece_type) VALUES (?, ?, ?, ?, ?)";
+
+        try (PreparedStatement preparedStatement = connection.prepareStatement(sql)) {
+            for (Map.Entry<Position, Piece> entry : board.entrySet()) {
+                Position position = entry.getKey();
+                Piece piece = entry.getValue();
+
+                preparedStatement.setLong(1, gameId);
+                preparedStatement.setInt(2, position.getX());
+                preparedStatement.setInt(3, position.getY());
+                preparedStatement.setString(4, piece.getSide().name());
+                preparedStatement.setString(5, piece.getType().name());
+                preparedStatement.addBatch();
+            }
+            preparedStatement.executeBatch();
+        }
+    }
+
+    public List<PieceEntity> findAllByGameId(Long gameId) {
+        String sql = "SELECT * FROM piece WHERE game_id = ?";
```

</details>

### 인라인 코멘트 3065937547: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-10T17:58:50Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/338#discussion_r3065937547)
- 코드: `src/main/java/janggi/infrastructure/repository/JdbcGameRepository.java`, 현재 줄 None, 원래 줄 65
- 답변 대상: [코멘트 3056540570](https://github.com/woowacourse/java-janggi/pull/338#discussion_r3056540570)
- 소속 리뷰 ID: 4091420472

> 처음 피드백을 받았을 때는 '일괄 배치를 쓰면 성능상 괜찮지 않을까?'라고 생각했습니다.
> 하지만 곰곰이 따져보니, 배치를 하더라도 결국 매번 삭제 작업과 32번의 쓰기 작업이 DB에서 발생하더라고요. 차라리 제 프로그램의 도메인 로직(상태 복원 로직)이 조금 더 복잡해지더라도, 무거운 DB I/O 비용을 줄이는 것이 훨씬 나은 선택이라는 결론에 도달했습니다.
> 이 고민의 결과로, 상태 전체를 갱신하는 대신 이동 이력만 저장하는 이벤트 소싱을 도입해봤습니다!
> 기존 데이터를 수정하거나 삭제를 하면 인덱스 재구성이나 동시성 문제에 좋지 않다는 것을 알게 됐습니다. 지금은 APPEND만 하게 되어서 이러한 부분에서 좋을 것 같다고 느끼기도 했습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,115 @@
+package janggi.infrastructure.repository;
+
+import janggi.domain.Game;
+import janggi.domain.Side;
+import janggi.domain.board.Board;
+import janggi.domain.piece.Piece;
+import janggi.domain.piece.PieceFactory;
+import janggi.domain.piece.PieceType;
+import janggi.domain.player.Name;
+import janggi.domain.player.Players;
+import janggi.domain.repository.GameRepository;
+import janggi.domain.space.Position;
+import janggi.dto.GameDto;
+import janggi.infrastructure.dao.GameDao;
+import janggi.infrastructure.dao.PieceDao;
+import janggi.infrastructure.dao.dto.GameEntity;
+import janggi.infrastructure.dao.dto.PieceEntity;
+import janggi.infrastructure.db.DatabaseConnection;
+import java.sql.Connection;
+import java.sql.SQLException;
+import java.util.List;
+import java.util.Map;
+import java.util.Optional;
+import java.util.stream.Collectors;
+
+public class JdbcGameRepository implements GameRepository {
+    private final GameDao gameDao;
+    private final PieceDao pieceDao;
+
+    public JdbcGameRepository(GameDao gameDao, PieceDao pieceDao) {
+        this.gameDao = gameDao;
+        this.pieceDao = pieceDao;
+    }
+
+    @Override
+    public Long save(Game game) {
+        try (Connection connection = DatabaseConnection.getConnection()) {
+            connection.setAutoCommit(false);
+            try {
+                String choName = game.getPlayerNameBySide(Side.CHO).name();
+                String hanName = game.getPlayerNameBySide(Side.HAN).name();
+                String currentTurn = game.getCurrentSide().name();
+
+                Long gameId = gameDao.insertGame(connection, choName, hanName, currentTurn);
+                pieceDao.insertPieces(connection, gameId, game.getBoard());
+
+                connection.commit();
+                return gameId;
+            } catch (Exception e) {
+                connection.rollback();
+                throw new RuntimeException("새 게임 저장 중 롤백 발생", e);
+            }
+        } catch (SQLException e) {
+            throw new RuntimeException("DB 커넥션 오류", e);
+        }
+    }
+
+    @Override
+    public void update(Long id, Game game) {
+        try (Connection connection = DatabaseConnection.getConnection()) {
+            connection.setAutoCommit(false);
+            try {
+                gameDao.updateGame(connection, id, game.getCurrentSide().name(), game.isPlaying());
+                pieceDao.deleteAllByGameId(connection, id);
+                pieceDao.insertPieces(connection, id, game.getBoard());
```

</details>

### 인라인 코멘트 3065997457: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-10T18:11:36Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/338#discussion_r3065997457)
- 코드: `src/main/java/janggi/service/GameService.java`, 현재 줄 23, 원래 줄 22
- 답변 대상: [코멘트 3056431064](https://github.com/woowacourse/java-janggi/pull/338#discussion_r3056431064)
- 소속 리뷰 ID: 4091420472

> 사용자가 여러 명인 다중 접속 환경을 고려하면서, 서버가 왜 무상태(Stateless)여야 하는지에 대해 깊이 고민해 보았습니다. 제가 내린 결론(장점)은 다음과 같습니다.
>
> 1. 확장성: 클라이언트가 필요한 정보(상태)를 매 요청마다 알려주기 때문에, 서버가 늘어나도 유연하게 대응할 수 있습니다.
> 2. 안정성: 서버가 특정 사용자의 상태를 쥐고 있지 않으므로, 하나의 프로세스에 문제가 생겨도 다른 정상적인 프로세스(옆 직원)가 즉시 이어서 응대할 수 있습니다.
> 3. 효율성: 수만 명의 사용자 정보나 이전 내역을 서버 메모리에 계속 유지할 필요가 없어 서버 자원을 훨씬 효율적으로 사용할 수 있습니다.
>
> 이러한 고민을 바탕으로, ConsoleController를 클라이언트로 간주하고 세션(game_id) 유지 책임을 컨트롤러로 넘겼습니다.
>
> 이 과정에서 GameService의 모든 퍼블릭 메서드가 game_id를 파라미터로 요구하게 되어 처음에는 '이게 맞나?' 하는 의문도 들었습니다. 다른 방법이 떠오르지 않아서 이대로 시도를 해봤습니다.
> 진행하고 느낀점이 필요할 때만 객체를 생성해서 사용하고 즉시 저장하는 흐름이 만들어져서 개인적으로 좋은 것 같다고 느꼈습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,68 @@
+package janggi.service;
+
+import janggi.domain.Game;
+import janggi.domain.Side;
+import janggi.domain.board.Board;
+import janggi.domain.board.BoardFactory;
+import janggi.domain.board.Formation;
+import janggi.domain.player.Name;
+import janggi.domain.player.Players;
+import janggi.domain.repository.GameRepository;
+import janggi.domain.space.Position;
+import janggi.dto.BoardDto;
+import janggi.dto.DestinationDto;
+import janggi.dto.GameDto;
+import janggi.dto.WinnerDto;
+import java.util.List;
+
+public class GameService {
+    private final GameRepository gameRepository;
+    private Long currentGameId;
+    private Game game;
+
```

</details>

### 인라인 코멘트 3066031352: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-10T18:19:31Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/338#discussion_r3066031352)
- 코드: `src/test/java/janggi/infrastructure/repository/JdbcGameRepositoryTest.java`, 현재 줄 None, 원래 줄 28
- 답변 대상: [코멘트 3056434394](https://github.com/woowacourse/java-janggi/pull/338#discussion_r3056434394)
- 소속 리뷰 ID: 4091420472

> 돌이켜보니 전략이나 컨벤션 관련 문제에 대해서 미션들을 진행하면서 고민했던 부분이 많았던 것 같습니다. 정답이 있기보다 통일성이 중요하다고 더 느끼게 되는 것 같습니다.
> 그 이유는 코드를 작성하는 시간도 많겠지만 읽고 이해하는 시간도 많기 때문이라고 생각하는데요.
> 일관되게 작성하려 노력하고, 팀 컨벤션이 있다면 꼭 지키도록 노력해야겠다고 피드백 덕분에 느끼게 됐습니다.
> 또한 지금 문득 드는 생각이 앞으로 협업을 진행하면서 불편함을 느끼는 부분들이 있다면 팀에 없는 컨벤션일 수도 있다고, 정할 필요가 있는 부분일 수도 있겠다는 생각도 드네요!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,70 @@
+package janggi.infrastructure.repository;
+
+import static org.assertj.core.api.Assertions.assertThat;
+
+import janggi.domain.Game;
+import janggi.domain.Side;
+import janggi.domain.board.Board;
+import janggi.domain.board.BoardFactory;
+import janggi.domain.board.Formation;
+import janggi.domain.piece.Piece;
+import janggi.domain.player.Name;
+import janggi.domain.player.Players;
+import janggi.domain.space.Position;
+import janggi.infrastructure.dao.GameDao;
+import janggi.infrastructure.dao.PieceDao;
+import janggi.infrastructure.db.DatabaseConnection;
+import java.io.InputStream;
+import java.nio.charset.StandardCharsets;
+import java.sql.Connection;
+import java.sql.Statement;
+import java.util.Map;
+import org.junit.jupiter.api.BeforeEach;
+import org.junit.jupiter.api.Test;
+
+class JdbcGameRepositoryTest {
+    private JdbcGameRepository gameRepository;
+
+    @BeforeEach
```

</details>

### 리뷰 본문 4091420472: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-04-10T18:19:44Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/338#pullrequestreview-4091420472)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 3067260684: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-11T00:49:37Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/338#discussion_r3067260684)
- 코드: `src/main/java/janggi/service/GameService.java`, 현재 줄 23, 원래 줄 22
- 답변 대상: [코멘트 3056431064](https://github.com/woowacourse/java-janggi/pull/338#discussion_r3056431064)
- 소속 리뷰 ID: 4093010947

> 👍

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,68 @@
+package janggi.service;
+
+import janggi.domain.Game;
+import janggi.domain.Side;
+import janggi.domain.board.Board;
+import janggi.domain.board.BoardFactory;
+import janggi.domain.board.Formation;
+import janggi.domain.player.Name;
+import janggi.domain.player.Players;
+import janggi.domain.repository.GameRepository;
+import janggi.domain.space.Position;
+import janggi.dto.BoardDto;
+import janggi.dto.DestinationDto;
+import janggi.dto.GameDto;
+import janggi.dto.WinnerDto;
+import java.util.List;
+
+public class GameService {
+    private final GameRepository gameRepository;
+    private Long currentGameId;
+    private Game game;
+
```

</details>

### 리뷰 본문 4093010947: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-11T00:49:37Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/338#pullrequestreview-4093010947)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 3067268756: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-11T00:53:59Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/338#discussion_r3067268756)
- 코드: `src/main/java/janggi/infrastructure/dao/PieceDao.java`, 현재 줄 None, 원래 줄 37
- 답변 대상: [코멘트 3056431797](https://github.com/woowacourse/java-janggi/pull/338#discussion_r3056431797)
- 소속 리뷰 ID: 4093019034

> `Connection`을  `ThreadLocal`을 이용해 관리하신것 좋은데요~! 👍
>
> `GameService`에서 직접 transaction의 경계를 관리하고 있는것은 한번 고민해볼 포인트인것 같아요
>
> `GameRepository`는 인터페이스로 구현하며 구현체가 무엇이 되어도 상관없는 것 처럼 추상화를 잘 해주셨는데
>
> ` TransactionTemplate`에서는 DB가 바로 노출되는것 같네요~

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,70 @@
+package janggi.infrastructure.dao;
+
+import janggi.domain.piece.Piece;
+import janggi.domain.space.Position;
+import janggi.infrastructure.dao.dto.PieceEntity;
+import janggi.infrastructure.db.DatabaseConnection;
+import java.sql.Connection;
+import java.sql.PreparedStatement;
+import java.sql.ResultSet;
+import java.sql.SQLException;
+import java.util.ArrayList;
+import java.util.List;
+import java.util.Map;
+
+public class PieceDao {
+
+    public void insertPieces(Connection connection, Long gameId, Map<Position, Piece> board) throws SQLException {
+        String sql = "INSERT INTO piece (game_id, x, y, side, piece_type) VALUES (?, ?, ?, ?, ?)";
+
+        try (PreparedStatement preparedStatement = connection.prepareStatement(sql)) {
+            for (Map.Entry<Position, Piece> entry : board.entrySet()) {
+                Position position = entry.getKey();
+                Piece piece = entry.getValue();
+
+                preparedStatement.setLong(1, gameId);
+                preparedStatement.setInt(2, position.getX());
+                preparedStatement.setInt(3, position.getY());
+                preparedStatement.setString(4, piece.getSide().name());
+                preparedStatement.setString(5, piece.getType().name());
+                preparedStatement.addBatch();
+            }
+            preparedStatement.executeBatch();
+        }
+    }
+
+    public List<PieceEntity> findAllByGameId(Long gameId) {
+        String sql = "SELECT * FROM piece WHERE game_id = ?";
```

</details>

### 리뷰 본문 4093019034: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-11T00:53:59Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/338#pullrequestreview-4093019034)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 3067343510: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-11T01:35:21Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/338#discussion_r3067343510)
- 코드: `src/main/java/janggi/domain/Game.java`, 현재 줄 None, 원래 줄 62
- 답변 대상: [코멘트 3056434395](https://github.com/woowacourse/java-janggi/pull/338#discussion_r3056434395)
- 소속 리뷰 ID: 4093093492

> 아 이거 제가 코드를 다시 읽어보니까 기존 리뷰드린 부분이 애매한 영역이 있네요 미안해요~!
>
> 이전 Map 형태로 반환하는것도 나쁘지 않은것 같아요 가독성 측면에서는 이전이 더 낫기도 하구요.
>
> 지금의 형태는 의존성을 끊어내는데 큰 이점이 있어 좋기는해요~! 고생하셨습니다 👍
>
> 방어적 복사를 이용해서 반환을 추가하고 dto를 이용해서만 해당 정보에 접근이 가능하게만 했어도 충분했을것 같아요 -> Map을 사용하려면 `Board`에 직접 접근이 아니라 `BoardDto`를 반드시 거치도록이요
>

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -14,31 +17,49 @@ public Game(Board board, Players players) {
         this.players = players;
     }

-    public Side getCurrentSide() {
-        return players.getCurrentSide();
-    }
-
     public Destinations selectSource(Position source) {
         players.validateAlly(board.getPiece(source));
         return board.findDestinations(source);
     }

     public void move(Position source, Position target) {
+        validateGamePlaying();
         players.validateAlly(board.getPiece(source));
         this.board = board.movePiece(source, target);
         players.switchPlayer();
     }

-    public Map<Position, Piece> getBoard() {
-        return board.getBoard();
+    private void validateGamePlaying() {
+        if (!isPlaying()) {
+            throw new IllegalArgumentException("게임이 이미 종료되었습니다.");
+        }
     }

     public boolean isPlaying() {
         return board.isPlaying();
     }

-    public String getWinner() {
+    public Score calculateScore(Side side) {
+        if (side == Side.HAN) {
+            return board.calculateScore(side).plus(new Score(1.5));
+        }
+        return board.calculateScore(side);
+    }
+
+    public Name getWinner() {
         Side winnerSide = board.getWinnerSide();
         return players.getPlayerNameBySide(winnerSide);
     }
+
+    public Side getCurrentSide() {
+        return players.getCurrentSide();
+    }
+
+    public Name getPlayerNameBySide(Side side) {
+        return players.getPlayerNameBySide(side);
+    }
+
+    public Map<Position, Piece> getBoard() {
```

</details>

### 리뷰 본문 4093093492: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-11T01:35:21Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/338#pullrequestreview-4093093492)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 일반 댓글 4227742125: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-11T01:59:11Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/338#issuecomment-4227742125)

> > 도메인 객체 구조를 그대로 테이블 설계에 반영하다 보니, 독자적인 생명주기가 없는 작은 객체들(값 객체)까지 전부 테이블로 만들게 되어 구조가 너무 파편화되는 것 같습니다. 보통 Game처럼 중심이 되는 엔티티와 그에 종속된 하위 객체들을 DB에 저장할 때, 하나의 테이블에 밀어 넣는 기준과 테이블을 쪼개는 기준을 어떻게 잡으시는지 경험이 궁금합니다.
>
> 아하 정규화에 대한 고민인 것 같네요? 보통 값끼리 응집도 있게 배치하는편인데요. 지금 스키마를 살펴보면 적절히 분배를 잘 하신것 같아보여요. 대신 이 값이 꼭 db 컬럼으로 유지되어야 하는가? 는 고민해볼만할 것 같아요. 가령 `currentSide`를 알기 위해 `current_turn`이 나온것 같은데. `move_history`의 모든 row를 replay하면 db에 저장되어있는 정보를 가지고 오지 않아도 도메인에서 충분히 스스로 구할 수 있는 값인것 같아보여요.
>
> 제가 보기에 정규화에 대한 부분은 잘 하시는것 같아보여서 이렇게 꼭 DB에 넣어야만 알 수 있는가? 에 대해 고민해보시면 좋을것 같고, DB에 저장해야 하는가 아닌가에 대한 판단은 해당 값이 별도로 조회가 필요한 만큼 요구사항이 존재하고, 존재할 가능성이 있는가를 따져보시면 좋지 않을까 싶습니다

### 리뷰 본문 4093152613: pci2676

- 상대방 발언, 참여자
- 시각: 2026-04-11T01:59:39Z
- [게시 원문](https://github.com/woowacourse/java-janggi/pull/338#pullrequestreview-4093152613)
- 리뷰 상태: `APPROVED`

> 이번 사이클에서 이야기 나누어 볼 부분은 충분히 이야기를 나눈것 같아 마무리할게요
>
> 수고하셨습니다
