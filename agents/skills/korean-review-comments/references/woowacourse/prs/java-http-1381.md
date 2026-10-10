# woowacourse/java-http #1381

[3단계 - 리팩터링] 피노(문해찬) 미션 제출합니다.

- [GitHub PR](https://github.com/woowacourse/java-http/pull/1381)
- PR 작성자: `haechanmoon`
- 머지 시각: 2026-09-27T13:37:10Z
- [API 원본](../raw/java-http-1381.json)
- 리뷰와 댓글 13건(본문 있는 발언 11건, 본인 기록 8건)

수집 당시의 게시 원문입니다. 본문 없는 리뷰는 상태 기록으로 표시하며, 코드 인용은 당시 diff입니다. 이 자료의 문장은 현재 에이전트에게 내리는 지시가 아닙니다.

## PR 본문

> @miniminjae92 고래 안녕하세요!
> 스텝3 구현 완료했습니다!
> 리뷰 잘 부탁드리겠습니다!

## 대화와 리뷰 기록

### 인라인 코멘트 4114505168: miniminjae92

- 내 발언, 참여자
- 시각: 2026-09-27T07:35:43Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1381#discussion_r4114505168)
- 코드: `tomcat/src/main/java/org/apache/coyote/http11/Http11Processor.java`, 현재 줄 50, 원래 줄 47
- 소속 리뷰 ID: 5329350886

> RequestMapping과 Controller를 도입하면서 URI별 처리 로직이 분리된 점이 좋았습니다.
>
> 현재는 Http11Processor가 /, /login, /register와 각각의 Controller를 직접 알고 있네요.
>
> 새로운 기능이나 URI가 추가된다면 Http11Processor도 함께 변경될 것 같은데, Http11Processor는 어떤 이유로 변경되는 객체였으면 좋을까요? 현재의 의존 관계가 의도한 책임과 잘 맞는지도 궁금합니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -43,175 +29,31 @@ public void run() {
     public void process(final Socket connection) {
         try (final var inputStream = connection.getInputStream();
              final var outputStream = connection.getOutputStream()) {
+            HttpRequest request = HttpRequest.parse(inputStream);

-            final var bufferedReader = new BufferedReader(
-                    new InputStreamReader(inputStream, StandardCharsets.UTF_8));
-            final String requestLine = bufferedReader.readLine();
-            if (requestLine == null) {
-                return;
-            }
-
-            final String method = requestLine.split(" ")[0];
-            final String requestUri = requestLine.split(" ")[1];
-            final String requestPath = requestPath(requestUri);
-
-            final Map<String, String> headers = new HashMap<>();
-            String headerLine;
-            while ((headerLine = bufferedReader.readLine()) != null && !headerLine.isEmpty()) {
-                final int colonIndex = headerLine.indexOf(":");
-                if (colonIndex > 0) {
-                    headers.put(headerLine.substring(0, colonIndex).toLowerCase(),
-                            headerLine.substring(colonIndex + 1).trim());
-                }
+            SessionManager sessionManager = SessionManager.getInstance();
+            String sessionId = new HttpCookie(request.headers().get("cookie")).getValue("JSESSIONID");
+            Session session = null;
+            if (sessionId != null) {
+                session = sessionManager.findSession(sessionId);
             }
-
-            final SessionManager sessionManager = SessionManager.getInstance();
-            final String sessionId = new HttpCookie(headers.get("cookie")).getValue("JSESSIONID");
-            Session session = sessionId == null ? null : sessionManager.findSession(sessionId);
             String setCookie = null;
             if (session == null) {
                 session = new Session(UUID.randomUUID().toString());
                 sessionManager.add(session);
                 setCookie = "JSESSIONID=" + session.getId() + "; Path=/; HttpOnly";
             }

-            String requestBody = "";
-            if ("POST".equals(method)) {
-                final int contentLength = Integer.parseInt(headers.getOrDefault("content-length", "0"));
-                final char[] buffer = new char[contentLength];
-                int readCount = 0;
-                while (readCount < contentLength) {
-                    final int count = bufferedReader.read(buffer, readCount, contentLength - readCount);
-                    if (count == -1) {
-                        throw new IOException("Request body ended early");
-                    }
-                    readCount += count;
-                }
-                requestBody = new String(buffer);
-            }
-
-            if ("POST".equals(method) && "/register".equals(requestPath)) {
-                final Map<String, String> parameters = queryParameters(requestBody);
-                final String account = parameters.get("account");
-                final String password = parameters.get("password");
-                final String email = parameters.get("email");
-                if (account == null || password == null || email == null) {
-                    final String response = "HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\n"
-                            + cookieHeader(setCookie) + "\r\n";
-                    outputStream.write(response.getBytes(StandardCharsets.UTF_8));
-                    return;
-                }
-                InMemoryUserRepository.save(new User(account, password, email));
-                sendRedirect(outputStream, "/index.html", setCookie);
-                return;
-            }
-
-            if ("GET".equals(method) && "/login".equals(requestPath)
-                    && session.getAttribute("user") != null) {
-                sendRedirect(outputStream, "/index.html", setCookie);
-                return;
-            }
-
-            if ("POST".equals(method) && "/login".equals(requestPath)) {
-                final Map<String, String> loginParameters = queryParameters(requestBody);
-                final boolean logInIsSuccess = logIn(loginParameters);
-                if (logInIsSuccess) {
-                    session.setAttribute("user", InMemoryUserRepository
-                            .findByAccount(loginParameters.get("account")).orElseThrow());
-                }
-                final String location = logInIsSuccess ? "/index.html" : "/401.html";
-                sendRedirect(outputStream, location, setCookie);
-                return;
-            }
-
-            final String responseBody = responseBody(requestPath);
-            final String contentType = contentType(requestPath);
-
-            final String response = "HTTP/1.1 200 OK \r\n"
-                    + "Content-Type: " + contentType + " \r\n"
-                    + "Content-Length: " + responseBody.getBytes(StandardCharsets.UTF_8).length + " \r\n"
-                    + cookieHeader(setCookie) + "\r\n" + responseBody;
-
-            outputStream.write(response.getBytes(StandardCharsets.UTF_8));
-            outputStream.flush();
-        } catch (IOException | UncheckedServletException e) {
+            HttpResponse response = new HttpResponse(outputStream, setCookie);
```

</details>

### 인라인 코멘트 4114539115: miniminjae92

- 내 발언, 참여자
- 시각: 2026-09-27T07:48:34Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1381#discussion_r4114539115)
- 코드: `tomcat/src/main/java/org/apache/coyote/http11/HttpResponse.java`, 현재 줄 None, 원래 줄 15
- 소속 리뷰 ID: 5329350886

> 응답을 만드는 책임이 `HttpResponse`로 이동하면서 Controller가 HTTP 응답 문자열을 직접 다루지 않게 된 점이 좋았습니다.
>
> 현재는 `send()`, `sendRedirect()`, `sendBadRequest()`, `sendNotFound()` 각각에서 필요한 상태 라인과 헤더를 구성하고 있네요.
>
> 앞으로 새로운 상태 코드나 헤더 조합이 필요해진다면 `HttpResponse`는 어떤 모습으로 확장될까요?
>
> 지금의 구조를 선택했을 때 얻을 수 있는 장점과, 요구사항이 늘어났을 때 생길 수 있는 변화도 함께 궁금합니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,56 @@
+package org.apache.coyote.http11;
+
+import java.io.IOException;
+import java.io.OutputStream;
+import java.nio.charset.StandardCharsets;
+
+public record HttpResponse(OutputStream output, String setCookie) {
+
+    public HttpResponse(OutputStream output) {
+        this(output, null);
+    }
+
+    public void send(String contentType, String body) throws IOException {
+        byte[] bodyBytes = body.getBytes(StandardCharsets.UTF_8);
+        String headers = "HTTP/1.1 200 OK\r\n"
```

</details>

### 리뷰 본문 5329350886: miniminjae92

- 내 발언, 참여자
- 시각: 2026-09-27T08:03:44Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1381#pullrequestreview-5329350886)
- 리뷰 상태: `CHANGES_REQUESTED`

(본문 없는 리뷰 상태 기록)

### 일반 댓글 5854064042: miniminjae92

- 내 발언, 참여자
- 시각: 2026-09-27T08:06:02Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1381#issuecomment-5854064042)

> 안녕하세요 피노~
> 휴일이 끝나가네요, 즐거운 명절이 되셨길 바랍니다!
> Step 3에서 역할을 나누면서 이전보다 각 객체의 책임이 훨씬 잘 드러난 것 같아요.
>
> 한번 더 고민해보면 좋을 것 같은 지점을 중심으로 코멘트 남겼습니다.
>
> 추가로 Session에서 현재 사용되지 않는 메서드가 존재하던데, 따로 남겨둔 이유가 있을까요?
> 미리 API를 열어두는 것에 대해서 어떻게 생각하시는 지 궁금합니다.
>
> 리뷰 한 번 확인해보시고 재요청주세요~!

### 인라인 코멘트 4114717959: haechanmoon

- 상대방 발언, PR 작성자
- 시각: 2026-09-27T08:54:56Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1381#discussion_r4114717959)
- 코드: `tomcat/src/main/java/org/apache/coyote/http11/Http11Processor.java`, 현재 줄 50, 원래 줄 47
- 답변 대상: [코멘트 4114505168](https://github.com/woowacourse/java-http/pull/1381#discussion_r4114505168)
- 소속 리뷰 ID: 5329599704

> 말씀해주신 대로 URI가 추가될 때마다 Http11Processor도 수정해야 했어요~
> Controller 등록을 RequestMapping.forSession()으로 옮겨서 Processor는 요청을 읽고 세션을 준비한 뒤 매핑된 Controller를 호출하도록 바꿨습니다!
> 로그인 Controller에 필요한 Session은 매핑을 만들 때 전달해요.
> 이제 경로가 추가돼도 Processor는 수정하지 않아도 되도록 했습니다!
> 감사합니다~~

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -43,175 +29,31 @@ public void run() {
     public void process(final Socket connection) {
         try (final var inputStream = connection.getInputStream();
              final var outputStream = connection.getOutputStream()) {
+            HttpRequest request = HttpRequest.parse(inputStream);

-            final var bufferedReader = new BufferedReader(
-                    new InputStreamReader(inputStream, StandardCharsets.UTF_8));
-            final String requestLine = bufferedReader.readLine();
-            if (requestLine == null) {
-                return;
-            }
-
-            final String method = requestLine.split(" ")[0];
-            final String requestUri = requestLine.split(" ")[1];
-            final String requestPath = requestPath(requestUri);
-
-            final Map<String, String> headers = new HashMap<>();
-            String headerLine;
-            while ((headerLine = bufferedReader.readLine()) != null && !headerLine.isEmpty()) {
-                final int colonIndex = headerLine.indexOf(":");
-                if (colonIndex > 0) {
-                    headers.put(headerLine.substring(0, colonIndex).toLowerCase(),
-                            headerLine.substring(colonIndex + 1).trim());
-                }
+            SessionManager sessionManager = SessionManager.getInstance();
+            String sessionId = new HttpCookie(request.headers().get("cookie")).getValue("JSESSIONID");
+            Session session = null;
+            if (sessionId != null) {
+                session = sessionManager.findSession(sessionId);
             }
-
-            final SessionManager sessionManager = SessionManager.getInstance();
-            final String sessionId = new HttpCookie(headers.get("cookie")).getValue("JSESSIONID");
-            Session session = sessionId == null ? null : sessionManager.findSession(sessionId);
             String setCookie = null;
             if (session == null) {
                 session = new Session(UUID.randomUUID().toString());
                 sessionManager.add(session);
                 setCookie = "JSESSIONID=" + session.getId() + "; Path=/; HttpOnly";
             }

-            String requestBody = "";
-            if ("POST".equals(method)) {
-                final int contentLength = Integer.parseInt(headers.getOrDefault("content-length", "0"));
-                final char[] buffer = new char[contentLength];
-                int readCount = 0;
-                while (readCount < contentLength) {
-                    final int count = bufferedReader.read(buffer, readCount, contentLength - readCount);
-                    if (count == -1) {
-                        throw new IOException("Request body ended early");
-                    }
-                    readCount += count;
-                }
-                requestBody = new String(buffer);
-            }
-
-            if ("POST".equals(method) && "/register".equals(requestPath)) {
-                final Map<String, String> parameters = queryParameters(requestBody);
-                final String account = parameters.get("account");
-                final String password = parameters.get("password");
-                final String email = parameters.get("email");
-                if (account == null || password == null || email == null) {
-                    final String response = "HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\n"
-                            + cookieHeader(setCookie) + "\r\n";
-                    outputStream.write(response.getBytes(StandardCharsets.UTF_8));
-                    return;
-                }
-                InMemoryUserRepository.save(new User(account, password, email));
-                sendRedirect(outputStream, "/index.html", setCookie);
-                return;
-            }
-
-            if ("GET".equals(method) && "/login".equals(requestPath)
-                    && session.getAttribute("user") != null) {
-                sendRedirect(outputStream, "/index.html", setCookie);
-                return;
-            }
-
-            if ("POST".equals(method) && "/login".equals(requestPath)) {
-                final Map<String, String> loginParameters = queryParameters(requestBody);
-                final boolean logInIsSuccess = logIn(loginParameters);
-                if (logInIsSuccess) {
-                    session.setAttribute("user", InMemoryUserRepository
-                            .findByAccount(loginParameters.get("account")).orElseThrow());
-                }
-                final String location = logInIsSuccess ? "/index.html" : "/401.html";
-                sendRedirect(outputStream, location, setCookie);
-                return;
-            }
-
-            final String responseBody = responseBody(requestPath);
-            final String contentType = contentType(requestPath);
-
-            final String response = "HTTP/1.1 200 OK \r\n"
-                    + "Content-Type: " + contentType + " \r\n"
-                    + "Content-Length: " + responseBody.getBytes(StandardCharsets.UTF_8).length + " \r\n"
-                    + cookieHeader(setCookie) + "\r\n" + responseBody;
-
-            outputStream.write(response.getBytes(StandardCharsets.UTF_8));
-            outputStream.flush();
-        } catch (IOException | UncheckedServletException e) {
+            HttpResponse response = new HttpResponse(outputStream, setCookie);
```

</details>

### 인라인 코멘트 4114718319: haechanmoon

- 상대방 발언, PR 작성자
- 시각: 2026-09-27T08:55:03Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1381#discussion_r4114718319)
- 코드: `tomcat/src/main/java/org/apache/coyote/http11/HttpResponse.java`, 현재 줄 None, 원래 줄 15
- 답변 대상: [코멘트 4114539115](https://github.com/woowacourse/java-http/pull/1381#discussion_r4114539115)
- 소속 리뷰 ID: 5329599704

> 지금 필요한 응답은 200, 302, 400, 404라서 상태별 메서드에서 응답 의도가 바로 보이는 단순함을 선택했어요! 다만 `Content-Length`와 `Set-Cookie` 작성이 실제로 반복되고 있더라고요. 그래서 상태별 메서드는 유지하고, 공통으로 헤더와 본문을 출력하는 `writeResponse()`를 추출했습니다. 새로운 상태 코드나 헤더가 필요하면 해당 메서드에서 필요한 값을 전달하고 공통 출력 부분을 재사용할 수 있을 것 같아요. 감사합니다!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,56 @@
+package org.apache.coyote.http11;
+
+import java.io.IOException;
+import java.io.OutputStream;
+import java.nio.charset.StandardCharsets;
+
+public record HttpResponse(OutputStream output, String setCookie) {
+
+    public HttpResponse(OutputStream output) {
+        this(output, null);
+    }
+
+    public void send(String contentType, String body) throws IOException {
+        byte[] bodyBytes = body.getBytes(StandardCharsets.UTF_8);
+        String headers = "HTTP/1.1 200 OK\r\n"
```

</details>

### 리뷰 본문 5329599704: haechanmoon

- 상대방 발언, PR 작성자
- 시각: 2026-09-27T09:10:04Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1381#pullrequestreview-5329599704)
- 리뷰 상태: `COMMENTED`

> 안녕하세요 고래
> 빠른 리뷰 감사드립니다!
> 말씀해주신 내용을 보고 URI 등록을 RequestMapping으로 옮기고,
> HttpResponse에서 반복되던 응답 출력 부분을 묶었어요.
> Session의 사용하지 않는 메서드도 제거했어요!
>
> 감사합니다!

### 인라인 코멘트 4115301340: miniminjae92

- 내 발언, 참여자
- 시각: 2026-09-27T12:15:57Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1381#discussion_r4115301340)
- 코드: `tomcat/src/main/java/org/apache/coyote/http11/Http11Processor.java`, 현재 줄 50, 원래 줄 47
- 답변 대상: [코멘트 4114505168](https://github.com/woowacourse/java-http/pull/1381#discussion_r4114505168)
- 소속 리뷰 ID: 5330251243

> 이전 피드백 이후 Http11Processor에서는 애플리케이션의 URI와 Controller를 직접 알지 않게 되었네요.
> 다만 현재는 해당 구성이 RequestMapping.forSession()으로 이동한 것으로 보여요.
> 이번 단계에서는 WAS 기능과 HTTP 요청/응답 처리 기능이 애플리케이션 개발자의 구현과 분리되어 재사용 가능한 구조가 되는 것을 목표로 하고 있는데요. 새로운 애플리케이션 경로나 Controller가 추가될 때 여전히 org.apache.coyote.http11 영역이 변경되어야 하는 현재 구조가 이 목표에 충분히 부합하는지 한 번 더 고민해보면 좋을 것 같습니다.
> 특히 RequestMapping의 책임이 등록된 매핑을 조회하는 것인지, 애플리케이션의 URI와 Controller를 구성하는 것까지 포함하는지도 함께 고민해보면 좋을 것 같아요.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -43,175 +29,31 @@ public void run() {
     public void process(final Socket connection) {
         try (final var inputStream = connection.getInputStream();
              final var outputStream = connection.getOutputStream()) {
+            HttpRequest request = HttpRequest.parse(inputStream);

-            final var bufferedReader = new BufferedReader(
-                    new InputStreamReader(inputStream, StandardCharsets.UTF_8));
-            final String requestLine = bufferedReader.readLine();
-            if (requestLine == null) {
-                return;
-            }
-
-            final String method = requestLine.split(" ")[0];
-            final String requestUri = requestLine.split(" ")[1];
-            final String requestPath = requestPath(requestUri);
-
-            final Map<String, String> headers = new HashMap<>();
-            String headerLine;
-            while ((headerLine = bufferedReader.readLine()) != null && !headerLine.isEmpty()) {
-                final int colonIndex = headerLine.indexOf(":");
-                if (colonIndex > 0) {
-                    headers.put(headerLine.substring(0, colonIndex).toLowerCase(),
-                            headerLine.substring(colonIndex + 1).trim());
-                }
+            SessionManager sessionManager = SessionManager.getInstance();
+            String sessionId = new HttpCookie(request.headers().get("cookie")).getValue("JSESSIONID");
+            Session session = null;
+            if (sessionId != null) {
+                session = sessionManager.findSession(sessionId);
             }
-
-            final SessionManager sessionManager = SessionManager.getInstance();
-            final String sessionId = new HttpCookie(headers.get("cookie")).getValue("JSESSIONID");
-            Session session = sessionId == null ? null : sessionManager.findSession(sessionId);
             String setCookie = null;
             if (session == null) {
                 session = new Session(UUID.randomUUID().toString());
                 sessionManager.add(session);
                 setCookie = "JSESSIONID=" + session.getId() + "; Path=/; HttpOnly";
             }

-            String requestBody = "";
-            if ("POST".equals(method)) {
-                final int contentLength = Integer.parseInt(headers.getOrDefault("content-length", "0"));
-                final char[] buffer = new char[contentLength];
-                int readCount = 0;
-                while (readCount < contentLength) {
-                    final int count = bufferedReader.read(buffer, readCount, contentLength - readCount);
-                    if (count == -1) {
-                        throw new IOException("Request body ended early");
-                    }
-                    readCount += count;
-                }
-                requestBody = new String(buffer);
-            }
-
-            if ("POST".equals(method) && "/register".equals(requestPath)) {
-                final Map<String, String> parameters = queryParameters(requestBody);
-                final String account = parameters.get("account");
-                final String password = parameters.get("password");
-                final String email = parameters.get("email");
-                if (account == null || password == null || email == null) {
-                    final String response = "HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\n"
-                            + cookieHeader(setCookie) + "\r\n";
-                    outputStream.write(response.getBytes(StandardCharsets.UTF_8));
-                    return;
-                }
-                InMemoryUserRepository.save(new User(account, password, email));
-                sendRedirect(outputStream, "/index.html", setCookie);
-                return;
-            }
-
-            if ("GET".equals(method) && "/login".equals(requestPath)
-                    && session.getAttribute("user") != null) {
-                sendRedirect(outputStream, "/index.html", setCookie);
-                return;
-            }
-
-            if ("POST".equals(method) && "/login".equals(requestPath)) {
-                final Map<String, String> loginParameters = queryParameters(requestBody);
-                final boolean logInIsSuccess = logIn(loginParameters);
-                if (logInIsSuccess) {
-                    session.setAttribute("user", InMemoryUserRepository
-                            .findByAccount(loginParameters.get("account")).orElseThrow());
-                }
-                final String location = logInIsSuccess ? "/index.html" : "/401.html";
-                sendRedirect(outputStream, location, setCookie);
-                return;
-            }
-
-            final String responseBody = responseBody(requestPath);
-            final String contentType = contentType(requestPath);
-
-            final String response = "HTTP/1.1 200 OK \r\n"
-                    + "Content-Type: " + contentType + " \r\n"
-                    + "Content-Length: " + responseBody.getBytes(StandardCharsets.UTF_8).length + " \r\n"
-                    + cookieHeader(setCookie) + "\r\n" + responseBody;
-
-            outputStream.write(response.getBytes(StandardCharsets.UTF_8));
-            outputStream.flush();
-        } catch (IOException | UncheckedServletException e) {
+            HttpResponse response = new HttpResponse(outputStream, setCookie);
```

</details>

### 리뷰 본문 5330251243: miniminjae92

- 내 발언, 참여자
- 시각: 2026-09-27T12:15:58Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1381#pullrequestreview-5330251243)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 리뷰 본문 5330255182: miniminjae92

- 내 발언, 참여자
- 시각: 2026-09-27T12:17:35Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1381#pullrequestreview-5330255182)
- 리뷰 상태: `CHANGES_REQUESTED`

> 피드백 반영해주신 부분들 확인했습니다! 전반적으로 많이 정리된 것 같아요!
> 다만 이전 피드백에서 이야기했던 WAS와 애플리케이션의 책임 분리 관점에서 더 확인하면 좋을 것 같다고 생각되어서 RC로 남깁니다. 코멘트 확인 부탁드려요!

### 인라인 코멘트 4115385719: haechanmoon

- 상대방 발언, PR 작성자
- 시각: 2026-09-27T12:47:26Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1381#discussion_r4115385719)
- 코드: `tomcat/src/main/java/org/apache/coyote/http11/Http11Processor.java`, 현재 줄 50, 원래 줄 47
- 답변 대상: [코멘트 4114505168](https://github.com/woowacourse/java-http/pull/1381#discussion_r4114505168)
- 소속 리뷰 ID: 5330332222

> 맞아요!
> 첫 수정에서는 Processor에서 경로 등록을 옮긴 것만 보고, WAS 패키지의 `RequestMapping`에 앱의 URI와 Controller 생성이 남아 있는 걸 놓쳤어요.
> 이번에는 `RequestMapping`을 전달받은 매핑의 조회만 맡도록 바꾸고, `/`, `/login`, `/register` 구성과 앱 Controller는 `com.techcourse`로 옮겼어요!
> `Application`에서 요청별 `Session`으로 매핑을 만드는 함수를 서버에 전달하고, `Tomcat`과 `Connector`를 거쳐 Processor가 사용해요. 이제 앱 경로를 추가할 때 WAS 코드는 수정하지 않아도 되게 됐습니다!
> 이 방향이 말씀하신 책임 분리가 맞을까요??

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -43,175 +29,31 @@ public void run() {
     public void process(final Socket connection) {
         try (final var inputStream = connection.getInputStream();
              final var outputStream = connection.getOutputStream()) {
+            HttpRequest request = HttpRequest.parse(inputStream);

-            final var bufferedReader = new BufferedReader(
-                    new InputStreamReader(inputStream, StandardCharsets.UTF_8));
-            final String requestLine = bufferedReader.readLine();
-            if (requestLine == null) {
-                return;
-            }
-
-            final String method = requestLine.split(" ")[0];
-            final String requestUri = requestLine.split(" ")[1];
-            final String requestPath = requestPath(requestUri);
-
-            final Map<String, String> headers = new HashMap<>();
-            String headerLine;
-            while ((headerLine = bufferedReader.readLine()) != null && !headerLine.isEmpty()) {
-                final int colonIndex = headerLine.indexOf(":");
-                if (colonIndex > 0) {
-                    headers.put(headerLine.substring(0, colonIndex).toLowerCase(),
-                            headerLine.substring(colonIndex + 1).trim());
-                }
+            SessionManager sessionManager = SessionManager.getInstance();
+            String sessionId = new HttpCookie(request.headers().get("cookie")).getValue("JSESSIONID");
+            Session session = null;
+            if (sessionId != null) {
+                session = sessionManager.findSession(sessionId);
             }
-
-            final SessionManager sessionManager = SessionManager.getInstance();
-            final String sessionId = new HttpCookie(headers.get("cookie")).getValue("JSESSIONID");
-            Session session = sessionId == null ? null : sessionManager.findSession(sessionId);
             String setCookie = null;
             if (session == null) {
                 session = new Session(UUID.randomUUID().toString());
                 sessionManager.add(session);
                 setCookie = "JSESSIONID=" + session.getId() + "; Path=/; HttpOnly";
             }

-            String requestBody = "";
-            if ("POST".equals(method)) {
-                final int contentLength = Integer.parseInt(headers.getOrDefault("content-length", "0"));
-                final char[] buffer = new char[contentLength];
-                int readCount = 0;
-                while (readCount < contentLength) {
-                    final int count = bufferedReader.read(buffer, readCount, contentLength - readCount);
-                    if (count == -1) {
-                        throw new IOException("Request body ended early");
-                    }
-                    readCount += count;
-                }
-                requestBody = new String(buffer);
-            }
-
-            if ("POST".equals(method) && "/register".equals(requestPath)) {
-                final Map<String, String> parameters = queryParameters(requestBody);
-                final String account = parameters.get("account");
-                final String password = parameters.get("password");
-                final String email = parameters.get("email");
-                if (account == null || password == null || email == null) {
-                    final String response = "HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\n"
-                            + cookieHeader(setCookie) + "\r\n";
-                    outputStream.write(response.getBytes(StandardCharsets.UTF_8));
-                    return;
-                }
-                InMemoryUserRepository.save(new User(account, password, email));
-                sendRedirect(outputStream, "/index.html", setCookie);
-                return;
-            }
-
-            if ("GET".equals(method) && "/login".equals(requestPath)
-                    && session.getAttribute("user") != null) {
-                sendRedirect(outputStream, "/index.html", setCookie);
-                return;
-            }
-
-            if ("POST".equals(method) && "/login".equals(requestPath)) {
-                final Map<String, String> loginParameters = queryParameters(requestBody);
-                final boolean logInIsSuccess = logIn(loginParameters);
-                if (logInIsSuccess) {
-                    session.setAttribute("user", InMemoryUserRepository
-                            .findByAccount(loginParameters.get("account")).orElseThrow());
-                }
-                final String location = logInIsSuccess ? "/index.html" : "/401.html";
-                sendRedirect(outputStream, location, setCookie);
-                return;
-            }
-
-            final String responseBody = responseBody(requestPath);
-            final String contentType = contentType(requestPath);
-
-            final String response = "HTTP/1.1 200 OK \r\n"
-                    + "Content-Type: " + contentType + " \r\n"
-                    + "Content-Length: " + responseBody.getBytes(StandardCharsets.UTF_8).length + " \r\n"
-                    + cookieHeader(setCookie) + "\r\n" + responseBody;
-
-            outputStream.write(response.getBytes(StandardCharsets.UTF_8));
-            outputStream.flush();
-        } catch (IOException | UncheckedServletException e) {
+            HttpResponse response = new HttpResponse(outputStream, setCookie);
```

</details>

### 리뷰 본문 5330332222: haechanmoon

- 상대방 발언, PR 작성자
- 시각: 2026-09-27T13:06:19Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1381#pullrequestreview-5330332222)
- 리뷰 상태: `COMMENTED`

> 꼼꼼히 리뷰 봐주셔서 감사해요!
> 코멘트 남겼어요! 확인 부탁드릴게요!

### 리뷰 본문 5330463499: miniminjae92

- 내 발언, 참여자
- 시각: 2026-09-27T13:24:41Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1381#pullrequestreview-5330463499)
- 리뷰 상태: `APPROVED`

> 피드백 의도까지 잘 반영해주신 것 확인했습니다!
> 여러 번 수정하시느라 정말 고생 많으셨어요.
> 이번 단계는 Approve 하겠습니다!
