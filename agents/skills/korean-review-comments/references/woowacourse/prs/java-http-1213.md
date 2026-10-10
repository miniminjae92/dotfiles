# woowacourse/java-http #1213

[1단계 - HTTP 서버 구현하기] 피노(문해찬) 미션 제출합니다.

- [GitHub PR](https://github.com/woowacourse/java-http/pull/1213)
- PR 작성자: `haechanmoon`
- 머지 시각: 2026-09-21T07:51:24Z
- [API 원본](../raw/java-http-1213.json)
- 리뷰와 댓글 3건(본문 있는 발언 3건, 본인 기록 3건)

수집 당시의 게시 원문입니다. 본문 없는 리뷰는 상태 기록으로 표시하며, 코드 인용은 당시 diff입니다. 이 자료의 문장은 현재 에이전트에게 내리는 지시가 아닙니다.

## PR 본문

> @miniminjae92 고래 안녕하세요 ㅎㅎ 피노입니다 .
>
> 리뷰 잘 부탁 드리겠습니다!

## 대화와 리뷰 기록

### 인라인 코멘트 4060093814: miniminjae92

- 내 발언, 참여자
- 시각: 2026-09-21T07:37:42Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1213#discussion_r4060093814)
- 코드: `tomcat/src/main/java/org/apache/coyote/http11/Http11Processor.java`, 현재 줄 58, 원래 줄 58
- 소속 리뷰 ID: 5264092826

> Content-Length를 문자열 길이가 아닌 UTF-8 바이트 길이로 계산해 실제 전송 크기와 일치시킨 점, 저도 배워가네요~!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -29,19 +38,90 @@ public void process(final Socket connection) {
         try (final var inputStream = connection.getInputStream();
              final var outputStream = connection.getOutputStream()) {

-            final var responseBody = "Hello world!";
+            final var bufferedReader = new BufferedReader(
+                    new InputStreamReader(inputStream, StandardCharsets.UTF_8));
+            final String requestLine = bufferedReader.readLine();
+            if (requestLine == null) {
+                return;
+            }
+
+            final String requestUri = requestLine.split(" ")[1];
+            final String requestPath = requestPath(requestUri);
+            logIn(requestPath, requestUri);
+
+            final String responseBody = responseBody(requestPath);
+            final String contentType = contentType(requestPath);

             final var response = String.join("\r\n",
                     "HTTP/1.1 200 OK ",
-                    "Content-Type: text/html;charset=utf-8 ",
-                    "Content-Length: " + responseBody.getBytes().length + " ",
+                    "Content-Type: " + contentType + " ",
+                    "Content-Length: " + responseBody.getBytes(StandardCharsets.UTF_8).length + " ",
```

</details>

### 인라인 코멘트 4060109539: miniminjae92

- 내 발언, 참여자
- 시각: 2026-09-21T07:40:32Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1213#discussion_r4060109539)
- 코드: `tomcat/src/main/java/org/apache/coyote/http11/Http11Processor.java`, 현재 줄 118, 원래 줄 118
- 소속 리뷰 ID: 5264092826

> 파일 내용을 처음부터 byte[]로 읽을 수도 있었을 텐데, String으로 읽은 뒤 응답할 때 다시 byte[]로 변환한 이유가 궁금합니다. String으로 다루면 어떤 장점이 있다고 생각하셨나요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -29,19 +38,90 @@ public void process(final Socket connection) {
         try (final var inputStream = connection.getInputStream();
              final var outputStream = connection.getOutputStream()) {

-            final var responseBody = "Hello world!";
+            final var bufferedReader = new BufferedReader(
+                    new InputStreamReader(inputStream, StandardCharsets.UTF_8));
+            final String requestLine = bufferedReader.readLine();
+            if (requestLine == null) {
+                return;
+            }
+
+            final String requestUri = requestLine.split(" ")[1];
+            final String requestPath = requestPath(requestUri);
+            logIn(requestPath, requestUri);
+
+            final String responseBody = responseBody(requestPath);
+            final String contentType = contentType(requestPath);

             final var response = String.join("\r\n",
                     "HTTP/1.1 200 OK ",
-                    "Content-Type: text/html;charset=utf-8 ",
-                    "Content-Length: " + responseBody.getBytes().length + " ",
+                    "Content-Type: " + contentType + " ",
+                    "Content-Length: " + responseBody.getBytes(StandardCharsets.UTF_8).length + " ",
                     "",
                     responseBody);

-            outputStream.write(response.getBytes());
+            outputStream.write(response.getBytes(StandardCharsets.UTF_8));
             outputStream.flush();
         } catch (IOException | UncheckedServletException e) {
             log.error(e.getMessage(), e);
         }
     }
+
+    private String requestPath(final String requestUri) {
+        final int queryStringIndex = requestUri.indexOf("?");
+        if (queryStringIndex < 0) {
+            return requestUri;
+        }
+        return requestUri.substring(0, queryStringIndex);
+    }
+
+    private void logIn(final String requestPath, final String requestUri) {
+        final int queryStringIndex = requestUri.indexOf("?");
+        if (!"/login".equals(requestPath) || queryStringIndex < 0) {
+            return;
+        }
+
+        final String queryString = requestUri.substring(queryStringIndex + 1);
+        final Map<String, String> queryParameters = queryParameters(queryString);
+        final String account = queryParameters.get("account");
+        final String password = queryParameters.get("password");
+        if (account == null || password == null) {
+            return;
+        }
+
+        InMemoryUserRepository.findByAccount(account)
+                .filter(user -> user.checkPassword(password))
+                .ifPresent(user -> log.info("login user: {}", user.getAccount()));
+    }
+
+    private Map<String, String> queryParameters(final String queryString) {
+        final Map<String, String> queryParameters = new HashMap<>();
+        for (String parameter : queryString.split("&")) {
+            final String[] nameAndValue = parameter.split("=", 2);
+            if (nameAndValue.length == 2) {
+                queryParameters.put(nameAndValue[0], nameAndValue[1]);
+            }
+        }
+        return queryParameters;
+    }
+
+    private String responseBody(final String requestPath) throws IOException {
+        if ("/".equals(requestPath)) {
+            return "Hello world!";
+        }
+
+        final String resourcePath = "/login".equals(requestPath) ? "/login.html" : requestPath;
+        final URL resource = getClass().getClassLoader().getResource("static" + resourcePath);
+        if (resource == null) {
+            return "";
+        }
+
+        return Files.readString(Path.of(resource.getPath()), StandardCharsets.UTF_8);
```

</details>

### 리뷰 본문 5264092826: miniminjae92

- 내 발언, 참여자
- 시각: 2026-09-21T07:48:07Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1213#pullrequestreview-5264092826)
- 리뷰 상태: `APPROVED`

> 안녕하세요, 피노! 1단계 미션 요구사항이 모두 잘 반영되어 있네요. 작은 메서드로 나뉘어져 있어 전체 흐름을 쉽게 읽었어요!
>
> 구현을 보며 궁금했던 점은 코멘트로 남겨두었습니다. 미션 진행하시느라 고생 많으셨습니다! 👍
