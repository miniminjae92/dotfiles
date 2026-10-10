# woowacourse/java-http #1355

[3단계 - 리팩터링] 고래(강민재) 미션 제출합니다.

- [GitHub PR](https://github.com/woowacourse/java-http/pull/1355)
- PR 작성자: `miniminjae92`
- 머지 시각: 2026-09-27T07:10:33Z
- [API 원본](../raw/java-http-1355.json)
- 리뷰와 댓글 14건(본문 있는 발언 13건, 본인 기록 4건)

수집 당시의 게시 원문입니다. 본문 없는 리뷰는 상태 기록으로 표시하며, 코드 인용은 당시 diff입니다. 이 자료의 문장은 현재 에이전트에게 내리는 지시가 아닙니다.

## PR 본문

> 한다, 명절에도 리뷰해 주시느라 고생 많으십니다!
>
> 기존 2단계 제출 당시 문서, 테스트, 초기 구조에서 마음에 들지 않았던 부분들을 먼저 정리하고 시작했어요.
>
> 2단계에서 정했던 세션 관련 규칙도 다시 고민해봤습니다. 톰캣을 구현하면서 로그인과 같은 애플리케이션 정책과 세션 자체를 관리하는 책임은 분리하는 게 맞아 보이더라구요.
>
> 다만 `HttpServletRequest`에서도 `getSession()`을 통해 세션을 제공하는 점을 참고해서, WAS에서 세션을 준비한 뒤 `HttpRequest`를 통해 Controller에서 사용할 수 있도록 구현해봤어요.
>
> 편하게 리뷰 부탁드려요~!
>
> ## 변경 사항
>
> ### HTTP 요청과 응답 책임 분리
>
> - Request Line을 `RequestLine`, `HttpMethod`, `HttpVersion`, `RequestTarget`으로 분리했습니다.
> - `HttpRequest`가 HTTP 요청을 해석하고 필요한 요청 정보를 제공하도록 정리했습니다.
> - `StatusLine`, `HttpStatus`를 도입해 HTTP 응답 상태 표현 책임을 분리했습니다.
> - `HttpResponse`가 상태, 헤더, 본문을 작성하고 HTTP 응답 메시지로 직렬화하도록 변경했습니다.
>
> ### Controller 도입
>
> - `Controller` 인터페이스를 추가했습니다.
> - `AbstractController`에서 HTTP Method에 따라 GET, POST 처리를 분기하도록 했습니다.
> - `RequestMapping`에서 요청 경로에 대응하는 Controller를 선택하도록 했습니다.
>
> ### 애플리케이션 처리 분리
>
> - 정적 리소스 처리를 `StaticResourceController`로 이동했습니다.
> - 회원가입 처리를 `RegisterController`로 이동했습니다.
> - 로그인 처리를 `LoginController`로 이동했습니다.
> - `Http11Processor`가 로그인, 회원가입과 같은 애플리케이션 로직을 직접 처리하지 않도록 변경했습니다.

## 대화와 리뷰 기록

### 인라인 코멘트 4112202396: dahxxn

- 상대방 발언, 참여자
- 시각: 2026-09-26T17:46:57Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1355#discussion_r4112202396)
- 코드: `tomcat/src/main/java/org/apache/catalina/startup/Tomcat.java`, 현재 줄 None, 원래 줄 31
- 소속 리뷰 ID: 5326783453

> Processor에서 로그인/회원가입 처리가 분리돼서 흐름이 훨씬 잘 보이네요~
>
> 다만 지금은 경로와 컨트롤러를 Tomcat에서 등록하고 있어서,
> 애플리케이션에 기능이 추가될 때마다 Tomcat도 함께 수정해야 할 것 같아요!
> 컨트롤러들도 org.apache.coyote.http11 패키지에 있으면서 User, InMemoryUserRepository를 사용하고 있는데,
> WAS를 다른 애플리케이션에서도 재사용한다는 관점에서 보면 이 부분들은 어느 쪽에 있는 게 자연스럽다고 생각하시는지 궁금합니다~!!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -11,7 +18,20 @@ public class Tomcat {
     private static final Logger log = LoggerFactory.getLogger(Tomcat.class);

     public void start() {
-        var connector = new Connector();
+        Manager sessionManager = new SessionManager();
+        Controller staticResourceController = new StaticResourceController();
+        RequestMapping requestMapping = new RequestMapping(staticResourceController);
+        requestMapping.register(
+                "/register",
+                new RegisterController(staticResourceController)
+        );
+        requestMapping.register(
+                "/login",
+                new LoginController(sessionManager, staticResourceController)
+        );
```

</details>

### 인라인 코멘트 4112277125: dahxxn

- 상대방 발언, 참여자
- 시각: 2026-09-26T18:13:14Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1355#discussion_r4112277125)
- 코드: `tomcat/src/main/java/org/apache/coyote/http11/StaticResourceController.java`, 현재 줄 None, 원래 줄 45
- 소속 리뷰 ID: 5326783453

> 로그인/회원가입 컨트롤러를 분리했지만,
> 해당 경로에서 어떤 페이지를 보여줄지는 StaticResourceController가 담당하고 있네요
>
> 이렇게 되면 경로에 대한 책임이 RequestMapping과 StaticResourceController 모두에 존재하게 되는데,
> 경로가 만약 바뀌게 되면 두 곳 모두 수정해야 되지 않을까요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,60 @@
+package org.apache.coyote.http11;
+
+import java.io.IOException;
+import java.net.URISyntaxException;
+import java.net.URL;
+import java.nio.file.Files;
+import java.nio.file.Path;
+import java.nio.file.Paths;
+
+public class StaticResourceController extends AbstractController {
+    private static final String STATIC_RESOURCE_PREFIX = "static";
+    private static final String ROOT_RESPONSE_BODY = "Hello world!";
+    private static final String LOGIN_PATH = "/login";
+    private static final String LOGIN_RESOURCE_PATH = "/login.html";
+
+    @Override
+    protected void doGet(
+            final HttpRequest request,
+            final HttpResponse response
+    ) throws IOException, URISyntaxException {
+        String resourcePath = resolveResourcePath(request.path());
+
+        byte[] responseBody = ROOT_RESPONSE_BODY.getBytes();
+
+        if (!resourcePath.equals("/")) {
+            String fileName = STATIC_RESOURCE_PREFIX + resourcePath;
+            URL resource = getClass()
+                    .getClassLoader()
+                    .getResource(fileName);
+
+            if (resource != null) {
+                Path path = Paths.get(resource.toURI());
+                responseBody = Files.readAllBytes(path);
+            }
+        }
+
+        response.setStatus(HttpStatus.OK);
+        response.addHeader(
+                "Content-Type",
+                contentTypeOf(request.extension())
+        );
+        response.setBody(responseBody);
+    }
+
+    private String resolveResourcePath(String requestPath) {
```

</details>

### 인라인 코멘트 4112286945: dahxxn

- 상대방 발언, 참여자
- 시각: 2026-09-26T18:16:32Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1355#discussion_r4112286945)
- 코드: `tomcat/src/main/java/org/apache/coyote/http11/RequestMapping.java`, 현재 줄 None, 원래 줄 22
- 소속 리뷰 ID: 5326783453

> 간단한 부분이긴 한데, HttpReqeust 객체를 직접 넘겨받기 보다는, path 경로만 넘겨받으면
> 의존성도 제거되고 테스트에서도 매핑 규칙을 HTTP 파서와 독립적으로 테스트 할 수 있을 것 같습니다!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,28 @@
+package org.apache.coyote.http11;
+
+import java.util.HashMap;
+import java.util.Map;
+
+public class RequestMapping {
+
+    private final Map<String, Controller> controllers = new HashMap<>();
+    private final Controller defaultController;
+
+    public RequestMapping(final Controller defaultController) {
+        this.defaultController = defaultController;
+    }
+
+    public void register(
+            final String path,
+            final Controller controller
+    ) {
+        controllers.put(path, controller);
+    }
+
+    public Controller getController(final HttpRequest request) {
```

</details>

### 인라인 코멘트 4112482089: dahxxn

- 상대방 발언, 참여자
- 시각: 2026-09-26T19:23:05Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1355#discussion_r4112482089)
- 코드: `tomcat/src/main/java/org/apache/coyote/http11/Http11Processor.java`, 현재 줄 None, 원래 줄 56
- 소속 리뷰 ID: 5326783453

> PR 본문에서 애플리케이션 정책과 세션 관리 책임을 분리하려고
> getSession()처럼 WAS에서 세션을 준비하도록 하셨다고 해서 인상 깊게 봤습니다!
>
> 다만 세션 준비는 WAS가 맡고 있는데,
> 로그인 시 세션 갱신은 LoginController가 Manager를 직접 받아서 처리하고 새 JSESSIONID 쿠키도 직접 만들고 있는 것 같아요.
> 그래서 쿠키 발급이 처음 세션을 만들 때는 Processor, 갱신할 때는 LoginController로 나뉘게 된 것 같고요!
> 로그인이 인증 경계라는 걸 아는 건 애플리케이션이라 "언제 갱신할지"는 컨트롤러가 정할 수밖에 없는데,
> `"어떻게 갱신하고 쿠키로 전달할지"`까지 컨트롤러가 알아야 할까 하는 생각이 드네용 🤔
>
> 세션 갱신 후 쿠키를 내려주는 일도 WAS가 맡도록 하는 것에 대해 고래는 어떻게 생각하시나요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -45,101 +43,32 @@ public void process(final Socket connection) {
             if (request == null) {
                 return;
             }
-            SessionManager sessionManager = new SessionManager();
+
             Optional<Session> existingSession = request.findCookie("JSESSIONID")
                     .flatMap(sessionManager::findSession);
-            Session session = existingSession.orElseGet(() -> {
-                Session newSession = new Session(UUID.randomUUID().toString());
-                sessionManager.add(newSession);
-                return newSession;
-            });
-            HttpResponse response = route(request, session, sessionManager);
+
+            Session session = existingSession.orElseGet(sessionManager::createSession);
+            request.attachSession(session);
+
+            HttpResponse response = route(request);
+
             if (existingSession.isEmpty() && !response.hasHeader("Set-Cookie")) {
                 response.addHeader("Set-Cookie", "JSESSIONID=" + session.getId());
```

</details>

### 리뷰 본문 5326783453: dahxxn

- 상대방 발언, 참여자
- 시각: 2026-09-26T19:42:17Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1355#pullrequestreview-5326783453)
- 리뷰 상태: `CHANGES_REQUESTED`

> 안녕하세요 고래~
> PR 본문에서 세션 관리 책임을 어떻게 나눌지 고민하신 과정이 보여서 리뷰하기 더 수월했어요 👍
> 이번 단계 목표인 WAS와 애플리케이션 역할 분리 관점에서 궁금한 점들을 코멘트로 남겼습니다.
> 편하게 의견 주시고, 개선하고 싶은 부분 있다면 반영한 뒤 다시 리뷰 요청해주셔요!
> 이번 단계도 화이팅입니다 🙌

### 인라인 코멘트 4113547463: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-09-27T00:41:14Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1355#discussion_r4113547463)
- 코드: `tomcat/src/main/java/org/apache/catalina/startup/Tomcat.java`, 현재 줄 None, 원래 줄 31
- 답변 대상: [코멘트 4112202396](https://github.com/woowacourse/java-http/pull/1355#discussion_r4112202396)
- 소속 리뷰 ID: 5328277898

> 말씀해주신 부분을 보고 다시 보니 Processor에서 애플리케이션 로직을 분리하는 데만 집중하고, 실제 조립은 여전히 Tomcat이 알고 있었네요. 예시 설명을 보니 위치도 부자연스럽다고 생각되네요.
>
> 컨트롤러들을 애플리케이션 패키지로 옮기고, `Application`에서 경로와 Controller를 구성한 `RequestMapping`을 Tomcat에 전달하도록 변경했습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -11,7 +18,20 @@ public class Tomcat {
     private static final Logger log = LoggerFactory.getLogger(Tomcat.class);

     public void start() {
-        var connector = new Connector();
+        Manager sessionManager = new SessionManager();
+        Controller staticResourceController = new StaticResourceController();
+        RequestMapping requestMapping = new RequestMapping(staticResourceController);
+        requestMapping.register(
+                "/register",
+                new RegisterController(staticResourceController)
+        );
+        requestMapping.register(
+                "/login",
+                new LoginController(sessionManager, staticResourceController)
+        );
```

</details>

### 인라인 코멘트 4113559315: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-09-27T00:46:01Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1355#discussion_r4113559315)
- 코드: `tomcat/src/main/java/org/apache/coyote/http11/RequestMapping.java`, 현재 줄 None, 원래 줄 22
- 답변 대상: [코멘트 4112286945](https://github.com/woowacourse/java-http/pull/1355#discussion_r4112286945)
- 소속 리뷰 ID: 5328277898

> 이 부분은 미션 힌트의 `getController(HttpRequest request)` 형태를 그대로 따라가면서 시작했어요.
>
> 다시 보니 현재 `RequestMapping`이 실제로 사용하는 정보는 `path` 하나뿐이고, 말씀해주신 것처럼 `HttpRequest` 전체에 의존할 이유는 없겠더라고요.
>
> 그래서 `getController(String path)`로 변경하고 호출하는 쪽에서 `request.path()`만 전달하도록 수정했습니다. 매핑 테스트도 HTTP 요청 파싱과 독립적으로 볼 수 있게 되서 편하더라구요!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,28 @@
+package org.apache.coyote.http11;
+
+import java.util.HashMap;
+import java.util.Map;
+
+public class RequestMapping {
+
+    private final Map<String, Controller> controllers = new HashMap<>();
+    private final Controller defaultController;
+
+    public RequestMapping(final Controller defaultController) {
+        this.defaultController = defaultController;
+    }
+
+    public void register(
+            final String path,
+            final Controller controller
+    ) {
+        controllers.put(path, controller);
+    }
+
+    public Controller getController(final HttpRequest request) {
```

</details>

### 인라인 코멘트 4113561617: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-09-27T00:47:08Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1355#discussion_r4113561617)
- 코드: `tomcat/src/main/java/org/apache/coyote/http11/Http11Processor.java`, 현재 줄 None, 원래 줄 56
- 답변 대상: [코멘트 4112482089](https://github.com/woowacourse/java-http/pull/1355#discussion_r4112482089)
- 소속 리뷰 ID: 5328277898

> 이 부분은 말씀해주신 `언제 갱신할지`와 `어떻게 갱신할지`의 구분이 이해하는 데 도움이 많이 됐습니다.
>
> 로그인 성공을 아는 `LoginController`는 이제 `request.renewSession()`으로 갱신 시점만 결정하고, `Manager`를 직접 사용하거나 `JSESSIONID` 쿠키를 작성하지 않도록 변경했습니다.
>
> `HttpRequest`가 연결된 Manager를 통해 세션을 갱신하고 자신의 현재 세션도 새 세션으로 교체하도록 했고, Processor에서는 요청으로 들어온 세션 ID와 처리 후 최종 세션 ID가 달라졌을 때 새로운 `JSESSIONID`를 응답하도록 변경했습니다.
>
> 이렇게 해서 애플리케이션은 세션을 언제 갱신할지만 결정하고, 실제 세션 교체와 클라이언트에 전달하는 방법은 WAS 쪽에서 담당하도록 정리해봤습니다!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -45,101 +43,32 @@ public void process(final Socket connection) {
             if (request == null) {
                 return;
             }
-            SessionManager sessionManager = new SessionManager();
+
             Optional<Session> existingSession = request.findCookie("JSESSIONID")
                     .flatMap(sessionManager::findSession);
-            Session session = existingSession.orElseGet(() -> {
-                Session newSession = new Session(UUID.randomUUID().toString());
-                sessionManager.add(newSession);
-                return newSession;
-            });
-            HttpResponse response = route(request, session, sessionManager);
+
+            Session session = existingSession.orElseGet(sessionManager::createSession);
+            request.attachSession(session);
+
+            HttpResponse response = route(request);
+
             if (existingSession.isEmpty() && !response.hasHeader("Set-Cookie")) {
                 response.addHeader("Set-Cookie", "JSESSIONID=" + session.getId());
```

</details>

### 리뷰 본문 5328277898: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-09-27T00:53:19Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1355#pullrequestreview-5328277898)
- 리뷰 상태: `COMMENTED`

> 한다, 리뷰 반영해서 다시 올렸습니다!
>
> 이번 리뷰를 보면서 WAS와 애플리케이션의 경계에 대해서 덕분에 생각해보게 됐어요.
>
> 각 코멘트에도 변경한 내용과 생각을 남겨두었습니다.
> 다시 한번 리뷰 부탁드릴게요!

### 인라인 코멘트 4114431124: dahxxn

- 상대방 발언, 참여자
- 시각: 2026-09-27T07:04:31Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1355#discussion_r4114431124)
- 코드: `tomcat/src/main/java/org/apache/catalina/startup/Tomcat.java`, 현재 줄 None, 원래 줄 31
- 답변 대상: [코멘트 4112202396](https://github.com/woowacourse/java-http/pull/1355#discussion_r4112202396)
- 소속 리뷰 ID: 5329245002

> 좋습니다~
> 컨트롤러가 애플리케이션 패키지로 옮겨지고 Application에서 조립하게 되니, 이제 Tomcat은 어떤 애플리케이션이 올라오는지 몰라도 되겠네요 👍

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -11,7 +18,20 @@ public class Tomcat {
     private static final Logger log = LoggerFactory.getLogger(Tomcat.class);

     public void start() {
-        var connector = new Connector();
+        Manager sessionManager = new SessionManager();
+        Controller staticResourceController = new StaticResourceController();
+        RequestMapping requestMapping = new RequestMapping(staticResourceController);
+        requestMapping.register(
+                "/register",
+                new RegisterController(staticResourceController)
+        );
+        requestMapping.register(
+                "/login",
+                new LoginController(sessionManager, staticResourceController)
+        );
```

</details>

### 리뷰 본문 5329245002: dahxxn

- 상대방 발언, 참여자
- 시각: 2026-09-27T07:04:31Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1355#pullrequestreview-5329245002)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 4114439037: dahxxn

- 상대방 발언, 참여자
- 시각: 2026-09-27T07:07:57Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1355#discussion_r4114439037)
- 코드: `tomcat/src/main/java/org/apache/coyote/http11/Http11Processor.java`, 현재 줄 54, 원래 줄 54
- 소속 리뷰 ID: 5329252767

> 들어온 세션 ID와 처리 후 세션 ID를 비교하니
> 새로만든 경우와 갱신한 경우 모두 여기서 한번에 쿠키가 발급되네요!
> 컨트롤러는 renewSession()으로 갱신 시점만 정하게 돼서 말씀하신 경계가 잘 드러나는 것 같습니당
>

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -45,101 +40,37 @@ public void process(final Socket connection) {
             if (request == null) {
                 return;
             }
-            SessionManager sessionManager = new SessionManager();
-            Optional<Session> existingSession = request.findCookie("JSESSIONID")
+
+            Optional<String> requestedSessionId = request.findCookie("JSESSIONID");
+            Optional<Session> existingSession = requestedSessionId
                     .flatMap(sessionManager::findSession);
-            Session session = existingSession.orElseGet(() -> {
-                Session newSession = new Session(UUID.randomUUID().toString());
-                sessionManager.add(newSession);
-                return newSession;
-            });
-            HttpResponse response = route(request, session, sessionManager);
-            if (existingSession.isEmpty() && !response.hasHeader("Set-Cookie")) {
-                response.addHeader("Set-Cookie", "JSESSIONID=" + session.getId());
+
+            Session session = existingSession.orElseGet(sessionManager::createSession);
+            request.attachSession(session, sessionManager);
+
+            HttpResponse response = route(request);
+
+            Session currentSession = request.session();
+            if (requestedSessionId.filter(currentSession.getId()::equals).isEmpty()) {
```

</details>

### 인라인 코멘트 4114442538: dahxxn

- 상대방 발언, 참여자
- 시각: 2026-09-27T07:09:34Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1355#discussion_r4114442538)
- 코드: `tomcat/src/main/java/com/techcourse/controller/LoginController.java`, 현재 줄 32, 원래 줄 32
- 소속 리뷰 ID: 5329252767

> 파일 응답 기능은 StaticResourceRenderer로 분리되고, 보여줄 페이지는 각 컨트롤러가 직접 정하게 됐네요!
> 경로 책임이 한 곳에 모여서 흐름이 훨씬 자연스러워진 것 같아요 👍

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,58 @@
+package com.techcourse.controller;
+
+import com.techcourse.db.InMemoryUserRepository;
+import com.techcourse.model.User;
+import java.util.Optional;
+import org.apache.catalina.Session;
+import org.apache.coyote.http11.AbstractController;
+import org.apache.coyote.http11.HttpRequest;
+import org.apache.coyote.http11.HttpResponse;
+import org.apache.coyote.http11.StaticResourceRenderer;
+
+public class LoginController extends AbstractController {
+
+    private static final String LOGIN_PAGE = "/login.html";
+
+    private final StaticResourceRenderer resourceRenderer;
+
+    public LoginController(final StaticResourceRenderer resourceRenderer) {
+        this.resourceRenderer = resourceRenderer;
+    }
+
+    @Override
+    protected void doGet(
+            final HttpRequest request,
+            final HttpResponse response
+    ) throws Exception {
+        if (request.session().getAttribute("user") instanceof User) {
+            response.sendRedirect("/index.html");
+            return;
+        }
+
+        resourceRenderer.writeResource(LOGIN_PAGE, response);
```

</details>

### 리뷰 본문 5329252767: dahxxn

- 상대방 발언, 참여자
- 시각: 2026-09-27T07:10:18Z
- [게시 원문](https://github.com/woowacourse/java-http/pull/1355#pullrequestreview-5329252767)
- 리뷰 상태: `APPROVED`

> 안녕하세요 고래~
> 정말 빠르게 반영해주셨군요
> WAS와 애플리케이션 경계가 코드에서 훨씬 선명하게 보여서 좋았습니다
> 3단계는 이만 머지하겠습니다~ 마지막 4단계도 화이팅~!!
