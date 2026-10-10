# woowacourse/java-http #1292

[2단계 - 로그인 구현하기] 고래(강민재) 미션 제출합니다.

- [GitHub PR](https://github.com/woowacourse/java-http/pull/1292)
- PR 작성자: `miniminjae92`
- 머지 시각: 2026-09-25T15:58:06Z
- [API 원본](../raw/java-http-1292.json)
- 리뷰와 댓글 12건(본문 있는 발언 10건, 본인 기록 5건)

수집 당시의 게시 원문입니다. 본문 없는 리뷰는 상태 기록으로 표시하며, 코드 인용은 당시 diff입니다. 이 자료의 문장은 현재 에이전트에게 내리는 지시가 아닙니다.

## PR 본문

> 안녕하세요, 한다! 고래입니다. 2단계 리뷰 부탁드립니다.
>
> ## Context
>
> 요구사항을 진행하며 요청을 읽는 코드를 여러 번 수정했고, 200 응답과 302 리다이렉트를 만들 때 응답 구성 규칙도 중복됐습니다. 요청의 메서드, 대상, 헤더, 본문은 `HttpRequest`가 다루고, HTTP 응답을 조립하는 일은 `HttpResponse`가 맡도록 나눴습니다.
>
> 세션은 로그인 성공 시에만 만들지, 로그인 전에도 만들지 고민했습니다. 비회원 장바구니처럼 로그인 전부터 세션을 사용하는 흐름을 직접 경험해 보고 싶어, 유효한 세션이 없는 요청에는 빈 세션을 만들고 로그인에 성공하면 그 세션에 `User`를 저장했습니다.
>
> ## Notes for reviewers
>
> - `HttpRequest`, `HttpResponse`와 `Http11Processor` 사이의 책임 경계가 자연스러운지 궁금합니다.
> - 로그인 전에도 세션을 만드는 선택에 대해서도 의견을 듣고 싶습니다.
>

## 대화와 리뷰 기록

### 인라인 코멘트 4100608385: dahxxn

- 상대방 발언, 참여자
- 시각: 2026-09-25T02:58:43Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1292#discussion_r4100608385)
- 코드: `tomcat/src/main/java/org/apache/coyote/http11/Http11Processor.java`, 현재 줄 55, 원래 줄 55
- 소속 리뷰 ID: 5312787420

> 비회원 장바구니 흐름을 경험하기 위해 로그인 전부터 세션을 만든 의도는 잘 이해했어요 👍
>
> 다만 현재는 로그인에 성공해 권한 상태가 달라져도 기존 세션에 User만 추가하고 같은 ID를 계속 사용하고 있네요
> ```java
>         session.setAttribute("user", authenticatedUser.get());
> ```
> 만약 누군가 로그인 전 세션 ID를 미리 알고 있거나 사용자에게 해당 ID를 사용하게 만들었다면,
> 사용자가 로그인한 이후에도 같은 ID로 인증 상태에 접근할 수 있을 것 같아요
> 일반적으로 이런 상황을 세션 고정(Session Fixation)이라고 하는데요
>
> 테스트에서도 로그인 전후 ID가 같음을 보장하고 있는데,
> 비회원 상태는 유지하면서 인증 경계에서는 세션 ID를 갱신하는 방식에 대해 어떻게 생각하시나요? 👀

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -40,54 +41,95 @@ public void run() {
     public void process(final Socket connection) {
         try (final var inputStream = connection.getInputStream();
              final var outputStream = connection.getOutputStream()) {
-            BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
-            String requestLine = reader.readLine();
-            if (requestLine == null) {
+            HttpRequest request = HttpRequest.readFrom(inputStream);
+            if (request == null) {
                 return;
             }
-            String[] parts = requestLine.split(" ");
-
-            RequestTarget requestTarget = new RequestTarget(parts[1]);
-            if (requestTarget.hasPath(LOGIN_PATH)) {
-                Optional<String> account = requestTarget.queryParameter("account");
-                if (account.isPresent()) {
-                    Optional<User> user = InMemoryUserRepository.findByAccount(account.get());
-                    user.ifPresent(value -> log.info("user : {}", value));
-                }
+            SessionManager sessionManager = new SessionManager();
+            Optional<Session> existingSession = request.findCookie("JSESSIONID")
+                    .flatMap(sessionManager::findSession);
+            Session session = existingSession.orElseGet(() -> {
+                Session newSession = new Session(UUID.randomUUID().toString());
+                sessionManager.add(newSession);
+                return newSession;
+            });
```

</details>

### 인라인 코멘트 4100716932: dahxxn

- 상대방 발언, 참여자
- 시각: 2026-09-25T03:21:22Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1292#discussion_r4100716932)
- 코드: `tomcat/src/main/java/org/apache/coyote/http11/HttpRequest.java`, 현재 줄 15, 원래 줄 15
- 소속 리뷰 ID: 5312787420

> 지난 단계에서 규칙이 독립적으로 변경되거나 코드를 읽고 테스트하는 데
> 불편함이 생겼을 때 책임을 나눠보고 싶다고 말씀해 주셨는데요.
> 이번 단계에서는 요청 파싱의 잦은 변경과 응답 생성의 중복을 기준으로 HttpRequest와 HttpResponse를 분리하셨네요.
> 요청을 해석하는 일과 응답을 조립하는 일이 각 객체에 모여 있어 전체 흐름을 따라가기 편했고,
> 이전에 이야기해 주신 기준도 잘 반영된 것 같아 좋았습니다 👍

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,102 @@
+package org.apache.coyote.http11;
+
+import java.io.BufferedInputStream;
+import java.io.ByteArrayOutputStream;
+import java.io.EOFException;
+import java.io.IOException;
+import java.io.InputStream;
+import java.net.URLDecoder;
+import java.nio.charset.StandardCharsets;
+import java.util.HashMap;
+import java.util.Locale;
+import java.util.Map;
+import java.util.Optional;
+
+public final class HttpRequest {
```

</details>

### 인라인 코멘트 4100773801: dahxxn

- 상대방 발언, 참여자
- 시각: 2026-09-25T03:34:34Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1292#discussion_r4100773801)
- 코드: `tomcat/src/main/java/org/apache/coyote/http11/Http11Processor.java`, 현재 줄 88, 원래 줄 87
- 소속 리뷰 ID: 5312787420

> 중복 계정의 회원가입을 어떻게 처리할지는 정책의 영역이지만
> 현재 save()는 account를 키로 사용하고 있어 이미 가입된 계정으로 다시 회원가입하면
> 저장소에 있던 기존 회원 정보가 새로운 정보로 덮어써지는 것 같아요~

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -40,54 +41,95 @@ public void run() {
     public void process(final Socket connection) {
         try (final var inputStream = connection.getInputStream();
              final var outputStream = connection.getOutputStream()) {
-            BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
-            String requestLine = reader.readLine();
-            if (requestLine == null) {
+            HttpRequest request = HttpRequest.readFrom(inputStream);
+            if (request == null) {
                 return;
             }
-            String[] parts = requestLine.split(" ");
-
-            RequestTarget requestTarget = new RequestTarget(parts[1]);
-            if (requestTarget.hasPath(LOGIN_PATH)) {
-                Optional<String> account = requestTarget.queryParameter("account");
-                if (account.isPresent()) {
-                    Optional<User> user = InMemoryUserRepository.findByAccount(account.get());
-                    user.ifPresent(value -> log.info("user : {}", value));
-                }
+            SessionManager sessionManager = new SessionManager();
+            Optional<Session> existingSession = request.findCookie("JSESSIONID")
+                    .flatMap(sessionManager::findSession);
+            Session session = existingSession.orElseGet(() -> {
+                Session newSession = new Session(UUID.randomUUID().toString());
+                sessionManager.add(newSession);
+                return newSession;
+            });
+            HttpResponse response = route(request, session);
+            if (existingSession.isEmpty() && !response.hasHeader("Set-Cookie")) {
+                response.addHeader("Set-Cookie", "JSESSIONID=" + session.getId());
             }
+            outputStream.write(response.toByteArray());
+            outputStream.flush();
+        } catch (IOException | UncheckedServletException | URISyntaxException e) {
+            log.error(e.getMessage(), e);
+        }
+    }

-            String resourcePath = resolveResourcePath(requestTarget);
+    private HttpResponse route(HttpRequest request, Session session) throws IOException, URISyntaxException {
+        if (request.matches("POST", LOGIN_PATH)) {
+            return login(request, session);
+        }
+        if (request.matches("POST", "/register")) {
+            return register(request);
+        }
+        if (request.matches("GET", LOGIN_PATH) && session.getAttribute("user") instanceof User) {
+            return HttpResponse.redirectTo("/index.html");
+        }
+        return handleResourceRequest(request);
+    }

-            byte[] responseBody = ROOT_RESPONSE_BODY.getBytes();
-            if (!resourcePath.equals("/")) {
-                String fileName = STATIC_RESOURCE_PREFIX + resourcePath;
-                URL resource = getClass().getClassLoader().getResource(fileName);
-                if (resource != null) {
-                    Path path = Paths.get(resource.toURI());
-                    responseBody = Files.readAllBytes(path);
-                }
-            }
-            String contentType = contentTypeOf(requestTarget.getExtension());
+    private HttpResponse register(HttpRequest request) {
+        String account = request.findFormParameter("account")
+                .orElseThrow(() -> new IllegalArgumentException("필수 입력값 누락: account"));
+        String password = request.findFormParameter("password")
+                .orElseThrow(() -> new IllegalArgumentException("필수 입력값 누락: password"));
+        String email = request.findFormParameter("email")
+                .orElseThrow(() -> new IllegalArgumentException("필수 입력값 누락: email"));
+        InMemoryUserRepository.save(new User(account, password, email));
```

</details>

### 리뷰 본문 5312787420: dahxxn

- 상대방 발언, 참여자
- 시각: 2026-09-25T03:40:21Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1292#pullrequestreview-5312787420)
- 리뷰 상태: `CHANGES_REQUESTED`

> 안녕하세요 고래~
> 이번 단계에서 로그인할 때만 세션을 만드는 데 그치지 않고,
> 비회원 흐름까지 경험해 보기 위해 미리 세션을 생성하신 점이 인상 깊었어요 👍
> 관련해 인증 전후의 세션 처리와 중복 회원가입의 동작에서 궁금한 점이 있어 코멘트 남겼습니다!
> 남긴 코멘트에 의견 주시고 개선하고 싶으신 부분 있다면 반영한 뒤 다시 리뷰 요청해 주세요!!
> 화이팅입니다~!! 🐳

### 인라인 코멘트 4102152526: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-09-25T07:19:57Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1292#discussion_r4102152526)
- 코드: `tomcat/src/main/java/org/apache/coyote/http11/Http11Processor.java`, 현재 줄 88, 원래 줄 87
- 답변 대상: [코멘트 4100773801](https://github.com/woowacourse/java-http/pull/1292#discussion_r4100773801)
- 소속 리뷰 ID: 5314762572

> 짚어주셔서 고마워요.
> 중복 계정에 대한 생각을 하긴 했었는데 이번 미션 요구사항에는 벗어난다고 여겨져서 고려하진 않았었어요.
> 임시 방편으로 해당 부분만 수정이 가능하긴 한데,  추후 회원 식별 방식과 중복 가입 요구사항을 함께 살펴볼 기회가 생기면 그 때 자세하게 이 부분을 다뤄보고 싶은데 괜찮을까요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -40,54 +41,95 @@ public void run() {
     public void process(final Socket connection) {
         try (final var inputStream = connection.getInputStream();
              final var outputStream = connection.getOutputStream()) {
-            BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
-            String requestLine = reader.readLine();
-            if (requestLine == null) {
+            HttpRequest request = HttpRequest.readFrom(inputStream);
+            if (request == null) {
                 return;
             }
-            String[] parts = requestLine.split(" ");
-
-            RequestTarget requestTarget = new RequestTarget(parts[1]);
-            if (requestTarget.hasPath(LOGIN_PATH)) {
-                Optional<String> account = requestTarget.queryParameter("account");
-                if (account.isPresent()) {
-                    Optional<User> user = InMemoryUserRepository.findByAccount(account.get());
-                    user.ifPresent(value -> log.info("user : {}", value));
-                }
+            SessionManager sessionManager = new SessionManager();
+            Optional<Session> existingSession = request.findCookie("JSESSIONID")
+                    .flatMap(sessionManager::findSession);
+            Session session = existingSession.orElseGet(() -> {
+                Session newSession = new Session(UUID.randomUUID().toString());
+                sessionManager.add(newSession);
+                return newSession;
+            });
+            HttpResponse response = route(request, session);
+            if (existingSession.isEmpty() && !response.hasHeader("Set-Cookie")) {
+                response.addHeader("Set-Cookie", "JSESSIONID=" + session.getId());
             }
+            outputStream.write(response.toByteArray());
+            outputStream.flush();
+        } catch (IOException | UncheckedServletException | URISyntaxException e) {
+            log.error(e.getMessage(), e);
+        }
+    }

-            String resourcePath = resolveResourcePath(requestTarget);
+    private HttpResponse route(HttpRequest request, Session session) throws IOException, URISyntaxException {
+        if (request.matches("POST", LOGIN_PATH)) {
+            return login(request, session);
+        }
+        if (request.matches("POST", "/register")) {
+            return register(request);
+        }
+        if (request.matches("GET", LOGIN_PATH) && session.getAttribute("user") instanceof User) {
+            return HttpResponse.redirectTo("/index.html");
+        }
+        return handleResourceRequest(request);
+    }

-            byte[] responseBody = ROOT_RESPONSE_BODY.getBytes();
-            if (!resourcePath.equals("/")) {
-                String fileName = STATIC_RESOURCE_PREFIX + resourcePath;
-                URL resource = getClass().getClassLoader().getResource(fileName);
-                if (resource != null) {
-                    Path path = Paths.get(resource.toURI());
-                    responseBody = Files.readAllBytes(path);
-                }
-            }
-            String contentType = contentTypeOf(requestTarget.getExtension());
+    private HttpResponse register(HttpRequest request) {
+        String account = request.findFormParameter("account")
+                .orElseThrow(() -> new IllegalArgumentException("필수 입력값 누락: account"));
+        String password = request.findFormParameter("password")
+                .orElseThrow(() -> new IllegalArgumentException("필수 입력값 누락: password"));
+        String email = request.findFormParameter("email")
+                .orElseThrow(() -> new IllegalArgumentException("필수 입력값 누락: email"));
+        InMemoryUserRepository.save(new User(account, password, email));
```

</details>

### 리뷰 본문 5314762572: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-09-25T07:19:57Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1292#pullrequestreview-5314762572)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 4102240594: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-09-25T07:31:39Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1292#discussion_r4102240594)
- 코드: `tomcat/src/main/java/org/apache/coyote/http11/Http11Processor.java`, 현재 줄 55, 원래 줄 55
- 답변 대상: [코멘트 4100608385](https://github.com/woowacourse/java-http/pull/1292#discussion_r4100608385)
- 소속 리뷰 ID: 5314869566

> 이번 미션에서는 로그인 전 상태를 옮겨야 하는 기능이 없어 구현 범위를 넓히지 않았는데 재밌어보여서 변경해봤어요
> 다만 이번 미션에는 로그인 전 상태로 유지할 데이터나 정책은 없어 새 세션에는 인증 정보만 담았고, 이후 비회원 상태를 유지해야 하는 기능이 생기면 어떤 데이터를 옮길지 정해서 다뤄보겠습니다~!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -40,54 +41,95 @@ public void run() {
     public void process(final Socket connection) {
         try (final var inputStream = connection.getInputStream();
              final var outputStream = connection.getOutputStream()) {
-            BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
-            String requestLine = reader.readLine();
-            if (requestLine == null) {
+            HttpRequest request = HttpRequest.readFrom(inputStream);
+            if (request == null) {
                 return;
             }
-            String[] parts = requestLine.split(" ");
-
-            RequestTarget requestTarget = new RequestTarget(parts[1]);
-            if (requestTarget.hasPath(LOGIN_PATH)) {
-                Optional<String> account = requestTarget.queryParameter("account");
-                if (account.isPresent()) {
-                    Optional<User> user = InMemoryUserRepository.findByAccount(account.get());
-                    user.ifPresent(value -> log.info("user : {}", value));
-                }
+            SessionManager sessionManager = new SessionManager();
+            Optional<Session> existingSession = request.findCookie("JSESSIONID")
+                    .flatMap(sessionManager::findSession);
+            Session session = existingSession.orElseGet(() -> {
+                Session newSession = new Session(UUID.randomUUID().toString());
+                sessionManager.add(newSession);
+                return newSession;
+            });
```

</details>

### 리뷰 본문 5314869566: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-09-25T07:31:39Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1292#pullrequestreview-5314869566)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 리뷰 본문 5314922131: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-09-25T07:37:20Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1292#pullrequestreview-5314922131)
- 리뷰 상태: `COMMENTED`

> 자세한 부분들을 캐치해서 던져주셔서 많은 생각을 할 수 있었어요.
> 도움이 많이 됐습니다. 감사합니다.

### 인라인 코멘트 4106244308: dahxxn

- 상대방 발언, 참여자
- 시각: 2026-09-25T15:52:35Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1292#discussion_r4106244308)
- 코드: `tomcat/src/main/java/org/apache/coyote/http11/Http11Processor.java`, 현재 줄 55, 원래 줄 55
- 답변 대상: [코멘트 4100608385](https://github.com/woowacourse/java-http/pull/1292#discussion_r4100608385)
- 소속 리뷰 ID: 5319742067

> 바로 반영해주셨네요!
> 로그인 시점에 새 ID로 교체하고 이전 세션까지 제거해서, 로그인 전 ID로는 더 이상 인증 상태에 접근할 수 없게 되었네요.
> 테스트에서도 이전 ID가 조회되지 않는 것까지 확인했습니다!
> 지금은 옮길 비회원 데이터가 없으니 인증 정보만 담는 판단도 자연스럽다고 생각합니다 🙂

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -40,54 +41,95 @@ public void run() {
     public void process(final Socket connection) {
         try (final var inputStream = connection.getInputStream();
              final var outputStream = connection.getOutputStream()) {
-            BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
-            String requestLine = reader.readLine();
-            if (requestLine == null) {
+            HttpRequest request = HttpRequest.readFrom(inputStream);
+            if (request == null) {
                 return;
             }
-            String[] parts = requestLine.split(" ");
-
-            RequestTarget requestTarget = new RequestTarget(parts[1]);
-            if (requestTarget.hasPath(LOGIN_PATH)) {
-                Optional<String> account = requestTarget.queryParameter("account");
-                if (account.isPresent()) {
-                    Optional<User> user = InMemoryUserRepository.findByAccount(account.get());
-                    user.ifPresent(value -> log.info("user : {}", value));
-                }
+            SessionManager sessionManager = new SessionManager();
+            Optional<Session> existingSession = request.findCookie("JSESSIONID")
+                    .flatMap(sessionManager::findSession);
+            Session session = existingSession.orElseGet(() -> {
+                Session newSession = new Session(UUID.randomUUID().toString());
+                sessionManager.add(newSession);
+                return newSession;
+            });
```

</details>

### 인라인 코멘트 4106247104: dahxxn

- 상대방 발언, 참여자
- 시각: 2026-09-25T15:52:55Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1292#discussion_r4106247104)
- 코드: `tomcat/src/main/java/org/apache/coyote/http11/Http11Processor.java`, 현재 줄 88, 원래 줄 87
- 답변 대상: [코멘트 4100773801](https://github.com/woowacourse/java-http/pull/1292#discussion_r4100773801)
- 소속 리뷰 ID: 5319742067

> 좋습니다~
> 말씀하신 것처럼 중복 가입을 어떻게 처리할지는 정책의 영역이라,
> 회원 식별 방식과 함께 고민할 때 다루는 게 더 자연스러울 것 같아요.
> 이미 인지하고 계셨다니 충분합니다 👍

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -40,54 +41,95 @@ public void run() {
     public void process(final Socket connection) {
         try (final var inputStream = connection.getInputStream();
              final var outputStream = connection.getOutputStream()) {
-            BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
-            String requestLine = reader.readLine();
-            if (requestLine == null) {
+            HttpRequest request = HttpRequest.readFrom(inputStream);
+            if (request == null) {
                 return;
             }
-            String[] parts = requestLine.split(" ");
-
-            RequestTarget requestTarget = new RequestTarget(parts[1]);
-            if (requestTarget.hasPath(LOGIN_PATH)) {
-                Optional<String> account = requestTarget.queryParameter("account");
-                if (account.isPresent()) {
-                    Optional<User> user = InMemoryUserRepository.findByAccount(account.get());
-                    user.ifPresent(value -> log.info("user : {}", value));
-                }
+            SessionManager sessionManager = new SessionManager();
+            Optional<Session> existingSession = request.findCookie("JSESSIONID")
+                    .flatMap(sessionManager::findSession);
+            Session session = existingSession.orElseGet(() -> {
+                Session newSession = new Session(UUID.randomUUID().toString());
+                sessionManager.add(newSession);
+                return newSession;
+            });
+            HttpResponse response = route(request, session);
+            if (existingSession.isEmpty() && !response.hasHeader("Set-Cookie")) {
+                response.addHeader("Set-Cookie", "JSESSIONID=" + session.getId());
             }
+            outputStream.write(response.toByteArray());
+            outputStream.flush();
+        } catch (IOException | UncheckedServletException | URISyntaxException e) {
+            log.error(e.getMessage(), e);
+        }
+    }

-            String resourcePath = resolveResourcePath(requestTarget);
+    private HttpResponse route(HttpRequest request, Session session) throws IOException, URISyntaxException {
+        if (request.matches("POST", LOGIN_PATH)) {
+            return login(request, session);
+        }
+        if (request.matches("POST", "/register")) {
+            return register(request);
+        }
+        if (request.matches("GET", LOGIN_PATH) && session.getAttribute("user") instanceof User) {
+            return HttpResponse.redirectTo("/index.html");
+        }
+        return handleResourceRequest(request);
+    }

-            byte[] responseBody = ROOT_RESPONSE_BODY.getBytes();
-            if (!resourcePath.equals("/")) {
-                String fileName = STATIC_RESOURCE_PREFIX + resourcePath;
-                URL resource = getClass().getClassLoader().getResource(fileName);
-                if (resource != null) {
-                    Path path = Paths.get(resource.toURI());
-                    responseBody = Files.readAllBytes(path);
-                }
-            }
-            String contentType = contentTypeOf(requestTarget.getExtension());
+    private HttpResponse register(HttpRequest request) {
+        String account = request.findFormParameter("account")
+                .orElseThrow(() -> new IllegalArgumentException("필수 입력값 누락: account"));
+        String password = request.findFormParameter("password")
+                .orElseThrow(() -> new IllegalArgumentException("필수 입력값 누락: password"));
+        String email = request.findFormParameter("email")
+                .orElseThrow(() -> new IllegalArgumentException("필수 입력값 누락: email"));
+        InMemoryUserRepository.save(new User(account, password, email));
```

</details>

### 리뷰 본문 5319742067: dahxxn

- 상대방 발언, 참여자
- 시각: 2026-09-25T15:57:42Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1292#pullrequestreview-5319742067)
- 리뷰 상태: `APPROVED`

> 안녕하세요 고래!
> 세션 재발급까지 테스트로 확인해주셔서 인증 전후 흐름이 훨씬 명확해진 것 같습니다 ㅎㅎ
> 저도 리뷰하는 과정에서 궁금한 부분 찾다보니 덕분에 많이 배우는 것 같아요
> 2단계는 여기서 머지하겠습니다! 3단계도 화이팅입니다~
