# woowacourse/java-http #1200

[1단계 - HTTP 서버 구현하기] 고래(강민재) 미션 제출합니다.

- [GitHub PR](https://github.com/woowacourse/java-http/pull/1200)
- PR 작성자: `miniminjae92`
- 머지 시각: 2026-09-20T08:12:38Z
- [API 원본](../raw/java-http-1200.json)
- 리뷰와 댓글 16건(본문 있는 발언 16건, 본인 기록 6건)

수집 당시의 게시 원문입니다. 본문 없는 리뷰는 상태 기록으로 표시하며, 코드 인용은 당시 diff입니다. 이 자료의 문장은 현재 에이전트에게 내리는 지시가 아닙니다.

## PR 본문

> 안녕하세요, 한다! 고래입니다.
>
> 이번 미션에서 만나 뵙게 되어 반갑습니다!
> 제출이 늦어져 기다리게 해서 미안해요.
> 1단계 HTTP 서버 구현을 완료해서 리뷰 요청드립니다.
>
> 편하게 의견 남겨주세요. 잘 부탁드립니다!

## 대화와 리뷰 기록

### 인라인 코멘트 4053159578: dahxxn

- 상대방 발언, 참여자
- 시각: 2026-09-19T12:19:53Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1200#discussion_r4053159578)
- 코드: `tomcat/src/main/java/org/apache/coyote/http11/Http11Processor.java`, 현재 줄 40, 원래 줄 38
- 소속 리뷰 ID: 5255694854

> 현재 process() 안에서 요청 라인 파싱, 로그인 회원 조회, 정적 리소스 탐색, 응답 생성까지 처리하고 있네요!
> 코드를 읽으며 개인적으론 process()가 여러 책임을 맡고 있다는 인상을 받았어요
> 고래가 보기에는 역할을 나눠볼 만한 지점이 있을까요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -28,20 +38,53 @@ public void run() {
     public void process(final Socket connection) {
```

</details>

### 인라인 코멘트 4053193263: dahxxn

- 상대방 발언, 참여자
- 시각: 2026-09-19T12:35:34Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1200#discussion_r4053193263)
- 코드: `tomcat/src/main/java/org/apache/coyote/http11/RequestTarget.java`, 현재 줄 7, 원래 줄 7
- 소속 리뷰 ID: 5255694854

> RequestTarget을 따로 두셨군요!
> 고래는 이 객체의 책임 범위를 어디까지로 생각하셨나요?
> 특히 경로 매핑도 RequestTarget의 역할로 둔 판단이 궁금하네요 👀

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,60 @@
+package org.apache.coyote.http11;
+
+import java.util.HashMap;
+import java.util.Map;
+import java.util.Optional;
+
+public class RequestTarget {
```

</details>

### 인라인 코멘트 4053398319: dahxxn

- 상대방 발언, 참여자
- 시각: 2026-09-19T14:06:00Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1200#discussion_r4053398319)
- 코드: `tomcat/src/test/java/org/apache/coyote/http11/Http11ProcessorTest.java`, 현재 줄 68, 원래 줄 68
- 소속 리뷰 ID: 5255694854

> 오 이번 요구사항에 해당하는 내용에 대해서 테스트 코드까지 잘 작성해 주셨네요 👍

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -58,4 +63,131 @@ void index() throws IOException {

         assertThat(socket.output()).isEqualTo(expected);
     }
+
+    @Test
+    void CSS_리소스_요청에_해당_파일의_내용으로_응답한다() throws IOException {
```

</details>

### 인라인 코멘트 4053859116: dahxxn

- 상대방 발언, 참여자
- 시각: 2026-09-19T16:45:59Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1200#discussion_r4053859116)
- 코드: `tomcat/src/main/java/org/apache/coyote/http11/Http11Processor.java`, 현재 줄 None, 원래 줄 68
- 소속 리뷰 ID: 5255694854

> 요청한 리소스를 찾지 못하는 경우 responseBody가 초기값인 Hello world! 로 남고
> 상태 코드도 200 이 되는 것 같은데
> 존재하지 않는 리소스 요청에서는 해당 응답이 적절하다고 판단하신 걸까요? 👀

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -28,20 +38,53 @@ public void run() {
     public void process(final Socket connection) {
         try (final var inputStream = connection.getInputStream();
              final var outputStream = connection.getOutputStream()) {
+            BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
+            String requestLine = reader.readLine();
+            if (requestLine == null) {
+                return;
+            }
+            String[] parts = requestLine.split(" ");

-            final var responseBody = "Hello world!";
+            RequestTarget requestTarget = new RequestTarget(parts[1]);
+            if (requestTarget.isLogin()) {
+                Optional<String> account = requestTarget.queryParameter("account");
+                if (account.isPresent()) {
+                    Optional<User> user = InMemoryUserRepository.findByAccount(account.get());
+                    user.ifPresent(value -> log.info("user : {}", value));
+                }
+            }
+
+            String resourcePath = requestTarget.resourcePath();
+
+            byte[] responseBody = ROOT_RESPONSE_BODY.getBytes();
+            if (!resourcePath.equals("/")) {
+                String fileName = STATIC_RESOURCE_PREFIX + resourcePath;
+                URL resource = getClass().getClassLoader().getResource(fileName);
+                if (resource != null) {
+                    Path path = Paths.get(resource.toURI());
+                    responseBody = Files.readAllBytes(path);
+                }
+            }
+            String contentType = contentTypeOf(requestTarget.extension());
```

</details>

### 인라인 코멘트 4053879674: dahxxn

- 상대방 발언, 참여자
- 시각: 2026-09-19T16:52:52Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1200#discussion_r4053879674)
- 코드: `tomcat/src/test/java/org/apache/coyote/http11/Http11ProcessorTest.java`, 현재 줄 None, 원래 줄 170
- 소속 리뷰 ID: 5255694854

> 현재 테스트 통과에는 문제가 없는 부분이지만,
> 로그인 파라미터화 테스트 케이스 하나가 HTTP/1.1이 끝에 들어가서
> 최종 요청에 버전이 2번 포함되는 것 같습니다!
> 한번 확인해 보면 좋을 것 같아용

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -58,4 +63,131 @@ void index() throws IOException {

         assertThat(socket.output()).isEqualTo(expected);
     }
+
+    @Test
+    void CSS_리소스_요청에_해당_파일의_내용으로_응답한다() throws IOException {
+        // given
+        final String httpRequest = String.join("\r\n",
+                "GET /css/styles.css HTTP/1.1 ",
+                "Host: localhost:8080 ",
+                "Accept: text/css,*/*;q=0.1 ",
+                "",
+                "");
+
+        final var socket = new StubSocket(httpRequest);
+        final var processor = new Http11Processor(socket);
+
+        // when
+        processor.process(socket);
+
+        // then
+        final URL resource = getClass().getClassLoader().getResource("static/css/styles.css");
+        final String expected = Files.readString(new File(resource.getFile()).toPath());
+
+        assertThat(socket.output()).endsWith("\r\n\r\n" + expected);
+    }
+
+    @Test
+    void CSS_리소스_요청에_text_css_Content_Type으로_응답한다() {
+        // given
+        final String httpRequest = String.join("\r\n",
+                "GET /css/styles.css HTTP/1.1 ",
+                "Host: localhost:8080 ",
+                "Accept: text/css,*/*;q=0.1 ",
+                "",
+                "");
+
+        final var socket = new StubSocket(httpRequest);
+        final var processor = new Http11Processor(socket);
+
+        // when
+        processor.process(socket);
+
+        // then
+        assertThat(socket.output()).contains("Content-Type: text/css;charset=utf-8");
+    }
+
+    @Test
+    void Query_String이_있는_로그인_요청에_로그인_페이지를_반환한다() throws IOException {
+        // given
+        final String httpRequest = String.join("\r\n",
+                "GET /login?account=gugu&password=password HTTP/1.1 ",
+                "Host: localhost:8080 ",
+                "Connection: keep-alive ",
+                "",
+                "");
+
+        final var socket = new StubSocket(httpRequest);
+        final var processor = new Http11Processor(socket);
+
+        // when
+        processor.process(socket);
+
+        // then
+        final URL resource = getClass().getClassLoader().getResource("static/login.html");
+        final String expected = Files.readString(new File(resource.getFile()).toPath());
+
+        assertThat(socket.output()).endsWith("\r\n\r\n" + expected);
+    }
+
+    @Test
+    void 전달된_계정_정보와_일치하는_회원_조회_결과를_로그로_남긴다() {
+        // given
+        final Logger logger = (Logger) LoggerFactory.getLogger(Http11Processor.class);
+        final var appender = new ListAppender<ILoggingEvent>();
+        appender.start();
+        logger.addAppender(appender);
+
+        final String httpRequest = String.join("\r\n",
+                "GET /login?account=gugu&password=password HTTP/1.1 ",
+                "Host: localhost:8080 ",
+                "Connection: keep-alive ",
+                "",
+                "");
+
+        final var socket = new StubSocket(httpRequest);
+        final var processor = new Http11Processor(socket);
+
+        try {
+            // when
+            processor.process(socket);
+
+            // then
+            assertThat(appender.list)
+                    .extracting(ILoggingEvent::getFormattedMessage)
+                    .contains("user : User{id=1, account='gugu', email='hkkang@woowahan.com', password='password'}");
+        } finally {
+            logger.detachAppender(appender);
+            appender.stop();
+        }
+    }
+
+    @ParameterizedTest
+    @CsvSource({
+            "/index.html, static/index.html",
+            "/css/styles.css, static/css/styles.css",
+            "/login, static/login.html",
+            "/login?account=gugu&password=password HTTP/1.1 , static/login.html"
```

</details>

### 리뷰 본문 5255694854: dahxxn

- 상대방 발언, 참여자
- 시각: 2026-09-19T17:07:24Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1200#pullrequestreview-5255694854)
- 리뷰 상태: `CHANGES_REQUESTED`

> 안녕하세요 고래~
> 반갑습니다 리뷰어 한다입니다
>
> 이번 1단계 구현 잘 봤어요! 테스트 코드까지 잘 작성해 주셨네요
> 몇 군데는 구현의 책임 범위와 판단 기준이 궁금해 코멘트 남겼습니다!
>
> 편하게 의견 남겨주시고, 추가적으로 리팩토링하실 부분 있으시면 반영해주셔도 됩니다
> 고생 많으셨고, 반영 마치시면 다시 리뷰 요청해 주세요 화이팅임다 🐳

### 인라인 코멘트 4056043365: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-09-20T03:56:45Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1200#discussion_r4056043365)
- 코드: `tomcat/src/main/java/org/apache/coyote/http11/Http11Processor.java`, 현재 줄 40, 원래 줄 38
- 답변 대상: [코멘트 4053159578](https://github.com/woowacourse/java-http/pull/1200#discussion_r4053159578)
- 소속 리뷰 ID: 5259437922

> 저도 process 메서드 안에서 요청 라인 파싱, 회원 조회, 정적 리소스 탐색, 응답 생성처럼 역할을 나눠볼 지점은 보인다고 생각했어요.
>
> 다만 1단계를 구현하는 동안에는 이 작업들이 하나의 요청 처리 흐름으로 함께 움직였고, 각각이 독립적으로 변경되면서 충돌하거나 코드를 읽고 테스트하는 데 불편을 주는 상황은 아직 경험하지 못했어요.
>
> 반면 요청 대상을 다루는 부분은 Query String 요구사항이 추가되면서 하나의 문자열에서 경로, 파라미터, 확장자를 반복해서 다뤄야 했고, 경로 분리와 리소스 매핑이 섞이면서 불편함을 느껴서 RequestTarget 객체로 분리했어요.
>
> 이번 미션에서는 분리할 수 있다는 이유만으로 미리 역할을 나누기보다, 이후 요구사항을 구현하며 각 규칙이 독립적으로 변경되어 실제로 불편해지는 등 필요하다고 느낀 시점에 분리해보려 합니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -28,20 +38,53 @@ public void run() {
     public void process(final Socket connection) {
```

</details>

### 인라인 코멘트 4056054148: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-09-20T04:02:53Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1200#discussion_r4056054148)
- 코드: `tomcat/src/main/java/org/apache/coyote/http11/RequestTarget.java`, 현재 줄 7, 원래 줄 7
- 답변 대상: [코멘트 4053193263](https://github.com/woowacourse/java-http/pull/1200#discussion_r4053193263)
- 소속 리뷰 ID: 5259437922

> 1단계 미션 요구사항을 진행하면서 요청 라인의 두 번째 인자에 대해서 변경이 잦아서, Request target 이라는 하나의 개념으로 보고, 관련된 상태와 행동을 한곳에 모으기 위해 RequestTarget 을 만들었어요.
>
> 리소스 매핑도 함께 넣었는데요. 한다가 짚어준 부분을 다시 살펴보니, 이 매핑은 요청 타겟 객체의 책임이 아니라 서버가 정한 외부의 규칙이라는 생각이 들어서 수정했어요. 체크해주셔서 고마워요!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,60 @@
+package org.apache.coyote.http11;
+
+import java.util.HashMap;
+import java.util.Map;
+import java.util.Optional;
+
+public class RequestTarget {
```

</details>

### 인라인 코멘트 4056056600: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-09-20T04:04:32Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1200#discussion_r4056056600)
- 코드: `tomcat/src/main/java/org/apache/coyote/http11/Http11Processor.java`, 현재 줄 None, 원래 줄 68
- 답변 대상: [코멘트 4053859116](https://github.com/woowacourse/java-http/pull/1200#discussion_r4053859116)
- 소속 리뷰 ID: 5259437922

> 적절한 응답이라고 판단한 것은 아니구요~ 구현하면서 존재하지 않는 리소스에는 기본값인 Hello world! 와 200 OK 가 반환된다는 점을 알고 있었어요.
>
> 다만 1단계에서는 요구사항에 나온 경로의 응답을 구현하는 데 범위를 두었고, 존재하지 않는 경로의 상태 코드와 응답 본문은 요구사항에 없어서 별도로 정의하지 않았어요. 이후 해당 동작이 요구될 때 , 테스트로 먼저 정한 뒤 구현하고 싶단 생각을 했어요.
>

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -28,20 +38,53 @@ public void run() {
     public void process(final Socket connection) {
         try (final var inputStream = connection.getInputStream();
              final var outputStream = connection.getOutputStream()) {
+            BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
+            String requestLine = reader.readLine();
+            if (requestLine == null) {
+                return;
+            }
+            String[] parts = requestLine.split(" ");

-            final var responseBody = "Hello world!";
+            RequestTarget requestTarget = new RequestTarget(parts[1]);
+            if (requestTarget.isLogin()) {
+                Optional<String> account = requestTarget.queryParameter("account");
+                if (account.isPresent()) {
+                    Optional<User> user = InMemoryUserRepository.findByAccount(account.get());
+                    user.ifPresent(value -> log.info("user : {}", value));
+                }
+            }
+
+            String resourcePath = requestTarget.resourcePath();
+
+            byte[] responseBody = ROOT_RESPONSE_BODY.getBytes();
+            if (!resourcePath.equals("/")) {
+                String fileName = STATIC_RESOURCE_PREFIX + resourcePath;
+                URL resource = getClass().getClassLoader().getResource(fileName);
+                if (resource != null) {
+                    Path path = Paths.get(resource.toURI());
+                    responseBody = Files.readAllBytes(path);
+                }
+            }
+            String contentType = contentTypeOf(requestTarget.extension());
```

</details>

### 인라인 코멘트 4056058971: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-09-20T04:05:57Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1200#discussion_r4056058971)
- 코드: `tomcat/src/test/java/org/apache/coyote/http11/Http11ProcessorTest.java`, 현재 줄 68, 원래 줄 68
- 답변 대상: [코멘트 4053398319](https://github.com/woowacourse/java-http/pull/1200#discussion_r4053398319)
- 소속 리뷰 ID: 5259437922

> 감사합니다 🙈

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -58,4 +63,131 @@ void index() throws IOException {

         assertThat(socket.output()).isEqualTo(expected);
     }
+
+    @Test
+    void CSS_리소스_요청에_해당_파일의_내용으로_응답한다() throws IOException {
```

</details>

### 인라인 코멘트 4056059524: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-09-20T04:06:21Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1200#discussion_r4056059524)
- 코드: `tomcat/src/test/java/org/apache/coyote/http11/Http11ProcessorTest.java`, 현재 줄 None, 원래 줄 170
- 답변 대상: [코멘트 4053879674](https://github.com/woowacourse/java-http/pull/1200#discussion_r4053879674)
- 소속 리뷰 ID: 5259437922

> 제가 놓친 부분이네요. 체크해 주셔서 감사해요! 수정할게요 😊

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -58,4 +63,131 @@ void index() throws IOException {

         assertThat(socket.output()).isEqualTo(expected);
     }
+
+    @Test
+    void CSS_리소스_요청에_해당_파일의_내용으로_응답한다() throws IOException {
+        // given
+        final String httpRequest = String.join("\r\n",
+                "GET /css/styles.css HTTP/1.1 ",
+                "Host: localhost:8080 ",
+                "Accept: text/css,*/*;q=0.1 ",
+                "",
+                "");
+
+        final var socket = new StubSocket(httpRequest);
+        final var processor = new Http11Processor(socket);
+
+        // when
+        processor.process(socket);
+
+        // then
+        final URL resource = getClass().getClassLoader().getResource("static/css/styles.css");
+        final String expected = Files.readString(new File(resource.getFile()).toPath());
+
+        assertThat(socket.output()).endsWith("\r\n\r\n" + expected);
+    }
+
+    @Test
+    void CSS_리소스_요청에_text_css_Content_Type으로_응답한다() {
+        // given
+        final String httpRequest = String.join("\r\n",
+                "GET /css/styles.css HTTP/1.1 ",
+                "Host: localhost:8080 ",
+                "Accept: text/css,*/*;q=0.1 ",
+                "",
+                "");
+
+        final var socket = new StubSocket(httpRequest);
+        final var processor = new Http11Processor(socket);
+
+        // when
+        processor.process(socket);
+
+        // then
+        assertThat(socket.output()).contains("Content-Type: text/css;charset=utf-8");
+    }
+
+    @Test
+    void Query_String이_있는_로그인_요청에_로그인_페이지를_반환한다() throws IOException {
+        // given
+        final String httpRequest = String.join("\r\n",
+                "GET /login?account=gugu&password=password HTTP/1.1 ",
+                "Host: localhost:8080 ",
+                "Connection: keep-alive ",
+                "",
+                "");
+
+        final var socket = new StubSocket(httpRequest);
+        final var processor = new Http11Processor(socket);
+
+        // when
+        processor.process(socket);
+
+        // then
+        final URL resource = getClass().getClassLoader().getResource("static/login.html");
+        final String expected = Files.readString(new File(resource.getFile()).toPath());
+
+        assertThat(socket.output()).endsWith("\r\n\r\n" + expected);
+    }
+
+    @Test
+    void 전달된_계정_정보와_일치하는_회원_조회_결과를_로그로_남긴다() {
+        // given
+        final Logger logger = (Logger) LoggerFactory.getLogger(Http11Processor.class);
+        final var appender = new ListAppender<ILoggingEvent>();
+        appender.start();
+        logger.addAppender(appender);
+
+        final String httpRequest = String.join("\r\n",
+                "GET /login?account=gugu&password=password HTTP/1.1 ",
+                "Host: localhost:8080 ",
+                "Connection: keep-alive ",
+                "",
+                "");
+
+        final var socket = new StubSocket(httpRequest);
+        final var processor = new Http11Processor(socket);
+
+        try {
+            // when
+            processor.process(socket);
+
+            // then
+            assertThat(appender.list)
+                    .extracting(ILoggingEvent::getFormattedMessage)
+                    .contains("user : User{id=1, account='gugu', email='hkkang@woowahan.com', password='password'}");
+        } finally {
+            logger.detachAppender(appender);
+            appender.stop();
+        }
+    }
+
+    @ParameterizedTest
+    @CsvSource({
+            "/index.html, static/index.html",
+            "/css/styles.css, static/css/styles.css",
+            "/login, static/login.html",
+            "/login?account=gugu&password=password HTTP/1.1 , static/login.html"
```

</details>

### 리뷰 본문 5259437922: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-09-20T04:18:24Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1200#pullrequestreview-5259437922)
- 리뷰 상태: `COMMENTED`

> 꼼꼼하게 리뷰해 주셔서 고마워요~~~
> 필요한 부분 수정했습니다.

### 인라인 코멘트 4056467885: dahxxn

- 상대방 발언, 참여자
- 시각: 2026-09-20T08:01:08Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1200#discussion_r4056467885)
- 코드: `tomcat/src/main/java/org/apache/coyote/http11/Http11Processor.java`, 현재 줄 40, 원래 줄 38
- 답변 대상: [코멘트 4053159578](https://github.com/woowacourse/java-http/pull/1200#discussion_r4053159578)
- 소속 리뷰 ID: 5260029149

> 좋습니다~
> 분리 가능성 보다 실제 변경이나 테스트의 불편을 기준으로 삼으셨군요!
> 고래가 어떤 기준으로 현재 구조를 선택했는지 잘 이해했습니다 👍

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -28,20 +38,53 @@ public void run() {
     public void process(final Socket connection) {
```

</details>

### 인라인 코멘트 4056469833: dahxxn

- 상대방 발언, 참여자
- 시각: 2026-09-20T08:02:18Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1200#discussion_r4056469833)
- 코드: `tomcat/src/main/java/org/apache/coyote/http11/RequestTarget.java`, 현재 줄 7, 원래 줄 7
- 답변 대상: [코멘트 4053193263](https://github.com/woowacourse/java-http/pull/1200#discussion_r4053193263)
- 소속 리뷰 ID: 5260029149

> 요청 대상이 가진 정보와 서버가 정한 매핑 규칙을 구분해 보셨군요
> 말씀해 주신 의도와 변경 내용 모두 확인했습니다!
>

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,60 @@
+package org.apache.coyote.http11;
+
+import java.util.HashMap;
+import java.util.Map;
+import java.util.Optional;
+
+public class RequestTarget {
```

</details>

### 인라인 코멘트 4056480646: dahxxn

- 상대방 발언, 참여자
- 시각: 2026-09-20T08:08:40Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1200#discussion_r4056480646)
- 코드: `tomcat/src/main/java/org/apache/coyote/http11/Http11Processor.java`, 현재 줄 None, 원래 줄 68
- 답변 대상: [코멘트 4053859116](https://github.com/woowacourse/java-http/pull/1200#discussion_r4053859116)
- 소속 리뷰 ID: 5260029149

> 오호 그렇군요
> 저는 이번 요구사항에서 존재하지 않는 경로의 응답까지 함께 고민해 볼 수 있다고 생각해서 코멘트를 남겼어요
> 고래는 명시된 요구사항까지만 범위로 두고, 나머지는 필요해지는 시점에 테스트로 정의하려고 하셨군요
>
> 작업 범위를 정하는 서로의 기준이 달랐다는 점도 흥미롭고,
> 이번 답변을 통해 고래의 구현 스타일을 조금 더 알게 된 것 같아요 👍

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -28,20 +38,53 @@ public void run() {
     public void process(final Socket connection) {
         try (final var inputStream = connection.getInputStream();
              final var outputStream = connection.getOutputStream()) {
+            BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
+            String requestLine = reader.readLine();
+            if (requestLine == null) {
+                return;
+            }
+            String[] parts = requestLine.split(" ");

-            final var responseBody = "Hello world!";
+            RequestTarget requestTarget = new RequestTarget(parts[1]);
+            if (requestTarget.isLogin()) {
+                Optional<String> account = requestTarget.queryParameter("account");
+                if (account.isPresent()) {
+                    Optional<User> user = InMemoryUserRepository.findByAccount(account.get());
+                    user.ifPresent(value -> log.info("user : {}", value));
+                }
+            }
+
+            String resourcePath = requestTarget.resourcePath();
+
+            byte[] responseBody = ROOT_RESPONSE_BODY.getBytes();
+            if (!resourcePath.equals("/")) {
+                String fileName = STATIC_RESOURCE_PREFIX + resourcePath;
+                URL resource = getClass().getClassLoader().getResource(fileName);
+                if (resource != null) {
+                    Path path = Paths.get(resource.toURI());
+                    responseBody = Files.readAllBytes(path);
+                }
+            }
+            String contentType = contentTypeOf(requestTarget.extension());
```

</details>

### 리뷰 본문 5260029149: dahxxn

- 상대방 발언, 참여자
- 시각: 2026-09-20T08:11:44Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1200#pullrequestreview-5260029149)
- 리뷰 상태: `APPROVED`

> 안녕하세요 고래~
> 주말인데도 아주 빠르게 리뷰 반영해주셨네요
> 단순히 코드를 분리하는 것보다 실제 변경과 불편을 기준으로 구조를 판단하는
> 고래의 스타일을 이해했어요
>
> 1단계는 여기서 마무리할게요!
> 고생 많으셨고 다음 단계도 화이팅입니다 🐳
