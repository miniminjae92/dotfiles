# woowacourse/java-mvc #1136

[1단계 - @MVC 프레임워크 구현하기] 고래(강민재) 미션 제출합니다.

- [GitHub PR](https://github.com/woowacourse/java-mvc/pull/1136)
- PR 작성자: `miniminjae92`
- 머지 시각: 2026-10-03T14:04:17Z
- [API 원본](../raw/java-mvc-1136.json)
- 리뷰와 댓글 12건(본문 있는 발언 9건, 본인 기록 7건)

수집 당시의 게시 원문입니다. 본문 없는 리뷰는 상태 기록으로 표시하며, 코드 인용은 당시 diff입니다. 이 자료의 문장은 현재 에이전트에게 내리는 지시가 아닙니다.

## PR 본문

> 안녕하세요, 흑곰~
> 이번 'MVC 구현하기' 잘 부탁드립니다.
>
> ## 변경 사항
>
> ### 어노테이션 기반 Handler Mapping
>
> - `@Controller`가 선언된 클래스를 탐색하도록 구현했습니다.
> - `@RequestMapping`이 선언된 메서드를 Handler로 등록했습니다.
> - 요청 경로와 HTTP Method를 기준으로 Handler를 조회하도록 구현했습니다.
> - HTTP Method가 지정되지 않으면 모든 HTTP Method에 대응하도록 구현했습니다.
> - 동일한 요청 경로와 HTTP Method가 중복 등록되면 초기화에 실패하도록 했습니다.
>
> ### Handler 실행
>
> - Controller 객체와 Handler 메서드를 `HandlerExecution`으로 관리하도록 구현했습니다.
> - HTTP 요청과 응답을 전달해 Handler 메서드를 실행하고 `ModelAndView`를 반환하도록 구현했습니다.
>
> ### View 렌더링
>
> - Model의 값을 Request attribute로 전달하도록 구현했습니다.
> - redirect와 JSP forward를 `JspView`에서 처리하도록 구현했습니다.
> - `DispatcherServlet`의 기존 View 처리 로직을 `JspView`로 이동했습니다.

## 대화와 리뷰 기록

### 인라인 코멘트 4161734822: jyt6640

- 상대방 발언, 참여자
- 시각: 2026-10-02T00:14:22Z
- [게시 원문](https://github.com/woowacourse/java-mvc/pull/1136#discussion_r4161734822)
- 코드: `mvc/src/main/java/com/interface21/webmvc/servlet/mvc/tobe/AnnotationHandlerMapping.java`, 현재 줄 53, 원래 줄 47
- 소속 리뷰 ID: 5387024470

> `AnnotationHandlerMapping`의 책임을 요청과 Handler를 매핑하는 것으로 본다면, Controller 인스턴스 생성까지 담당하는 건 책임이 조금 넓어질 수도 있을 것 같아요!
>
> 지금은 기본 생성자로 생성할 수 있지만, 이후 Controller가 Service 같은 의존성을 가지게 된다면 HandlerMapping이 객체 생성 방식까지 알아야 할 것 같은데요.
>
> 고래는 Controller의 생성과 생명주기를 누가 관리하는 게 자연스럽다고 생각하시나요? 현재 구조에 IoC/DI를 적용하게 된다면 어떻게 달라질지도 궁금합니다 🙂

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -20,10 +24,59 @@ public AnnotationHandlerMapping(final Object... basePackage) {
     }

     public void initialize() {
+        final var reflections = new Reflections(basePackage);
+
+        reflections.getTypesAnnotatedWith(Controller.class)
+                .forEach(this::registerController);
+
         log.info("Initialized AnnotationHandlerMapping!");
     }

+    private void registerController(final Class<?> controllerClass) {
+        final var controller = createController(controllerClass);
+
+        for (Method method : controllerClass.getDeclaredMethods()) {
+            if (method.isAnnotationPresent(RequestMapping.class)) {
+                registerHandler(controller, method);
+            }
+        }
+    }
+
+    private Object createController(final Class<?> controllerClass) {
+        try {
+            return controllerClass.getDeclaredConstructor().newInstance();
```

</details>

### 인라인 코멘트 4161741793: jyt6640

- 상대방 발언, 참여자
- 시각: 2026-10-02T00:15:47Z
- [게시 원문](https://github.com/woowacourse/java-mvc/pull/1136#discussion_r4161741793)
- 코드: `mvc/src/main/java/com/interface21/webmvc/servlet/mvc/tobe/HandlerExecution.java`, 현재 줄 19, 원래 줄 19
- 소속 리뷰 ID: 5387024470

> 현재 `HandlerExecution`은 Handler 메서드가 `(HttpServletRequest, HttpServletResponse)`를 인자로 받고 `ModelAndView`를 반환한다는 것을 전제로 하고 있는 것 같아요.
>
> 그런데 잘못된 형태의 메서드에 `@RequestMapping`을 붙여도 초기화에는 성공하고, 실제 요청이 들어왔을 때 `IllegalArgumentException`이나 `ClassCastException`으로 발견될 수도 있을 것 같은데요.
>
> 이런 잘못된 Handler 선언을 요청 시점이 아니라 초기화 시점에 발견하려면 어떤 조건들을 검증할 수 있을까요?
>
> 프레임워크 사용자가 조금 더 빠르게 문제를 알 수 있을 것 같습니다!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -1,12 +1,21 @@
 package com.interface21.webmvc.servlet.mvc.tobe;

+import com.interface21.webmvc.servlet.ModelAndView;
 import jakarta.servlet.http.HttpServletRequest;
 import jakarta.servlet.http.HttpServletResponse;
-import com.interface21.webmvc.servlet.ModelAndView;
+import java.lang.reflect.Method;

 public class HandlerExecution {

+    private final Object target;
+    private final Method method;
+
+    public HandlerExecution(Object target, Method method) {
+        this.target = target;
+        this.method = method;
+    }
+
     public ModelAndView handle(final HttpServletRequest request, final HttpServletResponse response) throws Exception {
-        return null;
+        return (ModelAndView) method.invoke(target, request, response);
```

</details>

### 인라인 코멘트 4161801207: jyt6640

- 상대방 발언, 참여자
- 시각: 2026-10-02T00:28:07Z
- [게시 원문](https://github.com/woowacourse/java-mvc/pull/1136#discussion_r4161801207)
- 코드: `mvc/src/main/java/com/interface21/webmvc/servlet/mvc/tobe/AnnotationHandlerMapping.java`, 현재 줄 39, 원래 줄 38
- 소속 리뷰 ID: 5387024470

> 여기서 `getMethods()`가 아니라 `getDeclaredMethods()`를 선택하신 이유가 궁금해요!
>
> `getDeclaredMethods()`는 해당 클래스에 직접 선언된 private 메서드까지 탐색하지만, 상속받은 public 메서드는 포함하지 않는 것으로 알고 있습니다.
>
> 그렇다면 `private @RequestMapping` 메서드도 Handler로 등록될 수 있지만 실제 `invoke()` 시점에는 접근 문제가 생길 수도 있을 것 같은데요.
>
> 고래는 어떤 접근 범위의 메서드까지 Handler로 허용하는 게 적절하다고 생각하시나요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -20,10 +24,59 @@ public AnnotationHandlerMapping(final Object... basePackage) {
     }

     public void initialize() {
+        final var reflections = new Reflections(basePackage);
+
+        reflections.getTypesAnnotatedWith(Controller.class)
+                .forEach(this::registerController);
+
         log.info("Initialized AnnotationHandlerMapping!");
     }

+    private void registerController(final Class<?> controllerClass) {
+        final var controller = createController(controllerClass);
+
+        for (Method method : controllerClass.getDeclaredMethods()) {
```

</details>

### 리뷰 본문 5387024470: jyt6640

- 상대방 발언, 참여자
- 시각: 2026-10-02T00:29:10Z
- [게시 원문](https://github.com/woowacourse/java-mvc/pull/1136#pullrequestreview-5387024470)
- 리뷰 상태: `CHANGES_REQUESTED`

> 안녕하세요 고래 !!
>
> 아직 미션도 못보고 있어서 학습을 좀 해보느라, 아직 옳지 않은 리뷰도 있을 수도 있습니다 !!
>
> 잘 감안해서 봐주세요 !!
>
> 고생많으셨어용~

### 인라인 코멘트 4163590708: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-10-02T07:11:15Z
- [게시 원문](https://github.com/woowacourse/java-mvc/pull/1136#discussion_r4163590708)
- 코드: `mvc/src/main/java/com/interface21/webmvc/servlet/mvc/tobe/AnnotationHandlerMapping.java`, 현재 줄 39, 원래 줄 38
- 답변 대상: [코멘트 4161801207](https://github.com/woowacourse/java-mvc/pull/1136#discussion_r4161801207)
- 소속 리뷰 ID: 5389136430

> 확인해보니 세 가지 방법이 있었습니다.
>
> 1. getMethods()를 사용해 public 메서드만 조회한다.
> 2. getDeclaredMethods()를 유지하고 public 메서드만 명시적으로 등록한다.
> 3. 비공개 메서드도 Handler로 허용하고 setAccessible(true)로 실행한다.
>
> 현재 요구사항에서는 비공개 Handler까지 지원할 필요는 없다고 생각했습니다. 또 getMethods()를 사용하면 상속받은 public 메서드까지 Handler 등록 대상이 될 수 있어서, 현재 클래스에 직접 선언된 메서드만 확인하는 기존 방식은 유지하고 싶었습니다.
>
> 그래서 getDeclaredMethods()는 유지하면서 public 메서드만 Handler로 등록하도록 변경해봤습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -20,10 +24,59 @@ public AnnotationHandlerMapping(final Object... basePackage) {
     }

     public void initialize() {
+        final var reflections = new Reflections(basePackage);
+
+        reflections.getTypesAnnotatedWith(Controller.class)
+                .forEach(this::registerController);
+
         log.info("Initialized AnnotationHandlerMapping!");
     }

+    private void registerController(final Class<?> controllerClass) {
+        final var controller = createController(controllerClass);
+
+        for (Method method : controllerClass.getDeclaredMethods()) {
```

</details>

### 리뷰 본문 5389136430: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-10-02T07:11:16Z
- [게시 원문](https://github.com/woowacourse/java-mvc/pull/1136#pullrequestreview-5389136430)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 4164047955: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-10-02T08:26:19Z
- [게시 원문](https://github.com/woowacourse/java-mvc/pull/1136#discussion_r4164047955)
- 코드: `mvc/src/main/java/com/interface21/webmvc/servlet/mvc/tobe/HandlerExecution.java`, 현재 줄 19, 원래 줄 19
- 답변 대상: [코멘트 4161741793](https://github.com/woowacourse/java-mvc/pull/1136#discussion_r4161741793)
- 소속 리뷰 ID: 5389698505

> 말씀해주신 부분을 확인하면서 몇 가지 방법을 생각해봤습니다.
>
> 1. 현재처럼 별도의 검증 없이 실제 요청이 들어왔을 때 `invoke()` 과정에서 잘못된 Handler 선언을 발견한다.
> 2. 초기화 시점에 파라미터의 개수·순서·타입과 반환 타입을 직접 검증해서 잘못된 Handler를 빠르게 발견한다.
> 3. Spring MVC처럼 고정된 Handler 시그니처를 검증하기보다 `HandlerMethodArgumentResolver`, `HandlerMethodReturnValueHandler`와 같이 각각의 파라미터와 반환값을 처리할 수 있는지를 판단하는 구조로 확장한다.
>
> 2번처럼 초기화 시점에 검증하는 방법도 충분히 의미 있다고 생각했습니다. 다만 이 방식을 선택하면 현재의 `(HttpServletRequest, HttpServletResponse) -> ModelAndView` 형태를 프레임워크의 명시적인 규칙으로 정의하게 되고, 그에 따라 파라미터 개수·순서·타입이나 반환 타입 같은 불변식과 예외 상황도 함께 정의하고 검증해야 한다고 생각했습니다.
>
> 3번은 실제 Spring MVC가 이 문제를 확장 가능한 구조로 해결하는 방식이라는 점에서 흥미로웠지만, 현재 단계에서 적용하기에는 미션의 범위를 많이 넘어간다고 판단했습니다.
>
> 그래서 이번에는 1번을 유지하기로 했습니다. 이번 미션에서는 Handler의 다양한 선언 형태나 그에 대한 방어 규칙을 설계하는 것보다, 어노테이션을 통해 Handler를 탐색하고 매핑한 뒤 실행하는 흐름과 MVC 각 객체의 역할을 이해하는 데 더 우선순위를 두고 싶었습니다.
>
> 덕분에 현재 구현이 특정 Handler 시그니처를 암묵적으로 전제하고 있다는 점과, 이를 fail-fast 방식으로 검증할 수도 있다는 점, 실제 Spring MVC에서는 이 문제를 어떤 구조로 확장하고 있는지까지 깊게 고민해볼 수 있었습니다. 좋은 질문 감사합니다!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -1,12 +1,21 @@
 package com.interface21.webmvc.servlet.mvc.tobe;

+import com.interface21.webmvc.servlet.ModelAndView;
 import jakarta.servlet.http.HttpServletRequest;
 import jakarta.servlet.http.HttpServletResponse;
-import com.interface21.webmvc.servlet.ModelAndView;
+import java.lang.reflect.Method;

 public class HandlerExecution {

+    private final Object target;
+    private final Method method;
+
+    public HandlerExecution(Object target, Method method) {
+        this.target = target;
+        this.method = method;
+    }
+
     public ModelAndView handle(final HttpServletRequest request, final HttpServletResponse response) throws Exception {
-        return null;
+        return (ModelAndView) method.invoke(target, request, response);
```

</details>

### 리뷰 본문 5389698505: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-10-02T08:26:19Z
- [게시 원문](https://github.com/woowacourse/java-mvc/pull/1136#pullrequestreview-5389698505)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 4164122154: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-10-02T08:37:55Z
- [게시 원문](https://github.com/woowacourse/java-mvc/pull/1136#discussion_r4164122154)
- 코드: `mvc/src/main/java/com/interface21/webmvc/servlet/mvc/tobe/AnnotationHandlerMapping.java`, 현재 줄 53, 원래 줄 47
- 답변 대상: [코멘트 4161734822](https://github.com/woowacourse/java-mvc/pull/1136#discussion_r4161734822)
- 소속 리뷰 ID: 5389787506

> 말씀해주신 부분을 보고 Controller 생성 책임을 어디에 두는 게 자연스러운지 고민해봤습니다.
>
> 저는 변경의 이유가 다르면 책임도 분리하는 편이 좋다고 생각합니다. Handler를 어떻게 매핑하는지와 Controller를 어떻게 생성하고 생명주기를 관리하는지는 서로 다른 이유로 변경될 수 있기 때문에, 장기적으로는 이 책임들이 분리되는 게 자연스럽다고 생각했습니다.
>
> IoC/DI가 적용된다면 객체 생성과 의존성 주입, 생명주기는 별도의 Container가 담당하고, AnnotationHandlerMapping은 이미 생성된 Controller를 이용해서 Handler를 등록하는 구조가 더 적절하다고 생각합니다.
>
> 다만 현재는 Controller 생성 방식이 기본 생성자 하나뿐이고, 별도의 의존성 주입이나 생명주기 관리 요구도 없는 상태라서 지금 Factory나 Container 역할까지 분리하는 것은 요구사항보다 앞선 추상화라고 판단했습니다.
>
> 그래서 현재 단계에서는 구조를 유지하되, 이후 Controller 생성 방식이 복잡해지거나 IoC/DI가 도입되는 시점에 이 책임을 분리하는 방향으로 생각하고 있는데 흑곰의 생각은 어떠신지?
>
> 덕분에 지금 구조에서 앞으로 어떻게 분리할 필요가 있는지 체크해볼 수 있었네요. 감사합니다~!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -20,10 +24,59 @@ public AnnotationHandlerMapping(final Object... basePackage) {
     }

     public void initialize() {
+        final var reflections = new Reflections(basePackage);
+
+        reflections.getTypesAnnotatedWith(Controller.class)
+                .forEach(this::registerController);
+
         log.info("Initialized AnnotationHandlerMapping!");
     }

+    private void registerController(final Class<?> controllerClass) {
+        final var controller = createController(controllerClass);
+
+        for (Method method : controllerClass.getDeclaredMethods()) {
+            if (method.isAnnotationPresent(RequestMapping.class)) {
+                registerHandler(controller, method);
+            }
+        }
+    }
+
+    private Object createController(final Class<?> controllerClass) {
+        try {
+            return controllerClass.getDeclaredConstructor().newInstance();
```

</details>

### 리뷰 본문 5389787506: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-10-02T08:37:55Z
- [게시 원문](https://github.com/woowacourse/java-mvc/pull/1136#pullrequestreview-5389787506)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 리뷰 본문 5389801308: miniminjae92

- 내 발언, PR 작성자
- 시각: 2026-10-02T08:39:38Z
- [게시 원문](https://github.com/woowacourse/java-mvc/pull/1136#pullrequestreview-5389801308)
- 리뷰 상태: `COMMENTED`

> 리뷰 감사합니다!
>
> 남겨주신 코멘트들을 보면서 현재 구현에서 암묵적으로 전제하고 있던 부분들과 책임의 경계를 다시 생각해볼 수 있었습니다.
>
> 수정이 필요하다고 판단한 부분은 반영했고, 현재 단계에서는 유지하기로 한 부분은 각각의 코멘트에 고민한 내용과 근거를 남겨두었습니다. 다시 한번 리뷰 부탁드립니다!

### 일반 댓글 5969909420: jyt6640

- 상대방 발언, 참여자
- 시각: 2026-10-03T14:04:12Z
- [게시 원문](https://github.com/woowacourse/java-mvc/pull/1136#issuecomment-5969909420)

> 충분히 잘 구현됬네요 !!
>
> 이번 미션은 머지하겠습니다 !!
