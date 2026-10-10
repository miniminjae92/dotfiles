# woowacourse/java-mvc #1171

[2단계 - 점진적인 리팩터링] 고래(강민재) 미션 제출합니다.

- [GitHub PR](https://github.com/woowacourse/java-mvc/pull/1171)
- PR 작성자: `miniminjae92`
- 머지 시각: 2026-10-08T00:15:38Z
- [API 원본](../raw/java-mvc-1171.json)
- 리뷰와 댓글 6건(본문 있는 발언 5건, 본인 기록 1건)

수집 당시의 게시 원문입니다. 본문 없는 리뷰는 상태 기록으로 표시하며, 코드 인용은 당시 diff입니다. 이 자료의 문장은 현재 에이전트에게 내리는 지시가 아닙니다.

## PR 본문

> 안녕하세요 흑곰~
> 이번 2단계 리뷰도 잘 부탁드립니다.
>
> 이번 미션에서는 `점진적 리팩터링`을 기존 구조를 한 번에 교체하는 것이 아니라,
> 기존 방식이 동작하는 상태를 유지하면서 새로운 구조를 추가하고,
> 두 방식을 공존시킨 뒤 조금씩 이전해가는 과정이라고 생각했습니다.
>
> 그래서 Legacy MVC를 바로 제거하지 않고,
> `HandlerMapping`, `HandlerAdapter` 같은 공통 인터페이스를 두어
> 기존 `Controller` 방식과 Annotation 기반 MVC가 하나의 흐름 안에서 함께 동작하도록 확장했습니다.
>
> 이후 일부 Controller만 Annotation 기반으로 전환해,
> 기존 동작을 유지하면서 새로운 방식으로 점진적으로 이동할 수 있는 구조를 만들어보았습니다.
>
> ## 변경 사항
>
> ### Legacy MVC와 Annotation MVC 통합
> - `HandlerMapping`을 통해 요청에 대응하는 Handler를 찾도록 변경했습니다.
> - `HandlerAdapter`를 통해 Handler 종류에 맞는 실행 방식을 선택하도록 변경했습니다.
> - Legacy `Controller`와 Annotation 기반 `HandlerExecution`을 각각 처리하는 Adapter를 구현했습니다.
>
> ### Annotation MVC 구조 개선
> - `@Controller` 탐색 및 인스턴스 생성 책임을 `ControllerScanner`로 분리했습니다.
> - `AnnotationHandlerMapping`은 전달받은 Controller를 기반으로 `@RequestMapping` 메서드를 등록하고 조회하도록 구성했습니다.
>
> ### 점진적 마이그레이션
> - `RegisterController`, `RegisterViewController`를 Annotation 기반 Controller로 전환했습니다.
> - 등록 관련 요청은 `AnnotationHandlerMapping`에서 처리하고, 기존 로그인/로그아웃 요청은 Legacy MVC가 계속 처리하도록 유지했습니다.
>
> ### 테스트
> - `HandlerAdapter` 구현체의 지원 여부와 실행 결과를 검증했습니다.
> - `DispatcherServletTest`를 추가해 Legacy MVC와 Annotation MVC가 같은 애플리케이션에서 함께 동작하는 것을 검증했습니다.

## 대화와 리뷰 기록

### 리뷰 본문 5437681959: miniminjae92

- 내 발언, PR 작성자
- 시각:
- [게시 원문](https://github.com/woowacourse/java-mvc/pull/1171#pullrequestreview-5437681959)
- 리뷰 상태: `PENDING`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 4190572231: jyt6640

- 상대방 발언, 참여자
- 시각: 2026-10-06T01:16:40Z
- [게시 원문](https://github.com/woowacourse/java-mvc/pull/1171#discussion_r4190572231)
- 코드: `app/src/main/java/com/techcourse/DispatcherServlet.java`, 현재 줄 None, 원래 줄 70
- 소속 리뷰 ID: 5422703793

> 현재 `getHandler()`와 `getHandlerAdapter()`에서 적절한 대상을 찾지 못하면 `null`을 반환하고 있네요!
>
> 이 경우 등록되지 않은 요청이 들어오거나, 어떤 Adapter도 지원하지 않는 Handler가 반환되면 실제 원인과는 조금 떨어진 `NullPointerException`이 발생할 것 같아요.
>
> 미션 힌트에서도 지원할 수 없는 Handler의 경우 예외를 발생시키는 흐름을 보여주고 있는데요. Handler 또는 HandlerAdapter를 찾지 못한 상황을 조금 더 명시적인 예외로 표현해보는 것은 어떨까요?
>
> 또 이런 실패를 판단하고 예외를 발생시키는 책임은 어느 객체가 가지는 게 자연스러울지도 궁금합니다 🙂

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -31,13 +49,36 @@ protected void service(final HttpServletRequest request, final HttpServletRespon
         log.debug("Method : {}, Request URI : {}", request.getMethod(), requestURI);

         try {
-            final var controller = manualHandlerMapping.getHandler(requestURI);
-            final var viewName = controller.execute(request, response);
-            final var jspView = new JspView(viewName);
-            jspView.render(Map.of(), request, response);
+
+            final var handler = getHandler(request);
+            final var handlerAdapter = getHandlerAdapter(handler);
+            final var modelAndView = handlerAdapter.handle(request, response, handler);
+            modelAndView.getView().render(modelAndView.getModel(), request, response);
         } catch (Throwable e) {
             log.error("Exception : {}", e.getMessage(), e);
             throw new ServletException(e.getMessage());
         }
     }
+
+    private HandlerAdapter getHandlerAdapter(final Object handler) {
+        for (HandlerAdapter handlerAdapter : handlerAdapters) {
+            if (handlerAdapter.supports(handler)) {
+                return handlerAdapter;
+            }
+        }
+
+        return null;
```

</details>

### 인라인 코멘트 4190575112: jyt6640

- 상대방 발언, 참여자
- 시각: 2026-10-06T01:17:14Z
- [게시 원문](https://github.com/woowacourse/java-mvc/pull/1171#discussion_r4190575112)
- 코드: `app/src/main/java/com/techcourse/DispatcherServlet.java`, 현재 줄 65, 원래 줄 80
- 소속 리뷰 ID: 5422703793

> 여러 `HandlerMapping`을 순회하면서 처음 발견한 Handler를 반환하고 있네요!
>
> 현재는 `ManualHandlerMapping`이 먼저 등록되어 있기 때문에 동일한 요청이 레거시 MVC와 Annotation MVC 양쪽에 등록되어 있다면 Legacy Handler가 항상 선택될 것 같아요.
>
> 점진적으로 Controller를 마이그레이션하다 보면 두 방식에 동일한 요청이 잠시 공존하는 상황도 생길 수 있을 것 같은데요. 이런 충돌 상황에서는 어떤 Handler를 선택해야 할지 정책을 정해두는 것도 필요하지 않을까요?
>
> 현재처럼 등록 순서 자체를 우선순위로 사용하는 것도 하나의 방법일 것 같은데, 고래는 이런 경우를 어떻게 처리하는 게 좋다고 생각하시나요?

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -31,13 +49,36 @@ protected void service(final HttpServletRequest request, final HttpServletRespon
         log.debug("Method : {}, Request URI : {}", request.getMethod(), requestURI);

         try {
-            final var controller = manualHandlerMapping.getHandler(requestURI);
-            final var viewName = controller.execute(request, response);
-            final var jspView = new JspView(viewName);
-            jspView.render(Map.of(), request, response);
+
+            final var handler = getHandler(request);
+            final var handlerAdapter = getHandlerAdapter(handler);
+            final var modelAndView = handlerAdapter.handle(request, response, handler);
+            modelAndView.getView().render(modelAndView.getModel(), request, response);
         } catch (Throwable e) {
             log.error("Exception : {}", e.getMessage(), e);
             throw new ServletException(e.getMessage());
         }
     }
+
+    private HandlerAdapter getHandlerAdapter(final Object handler) {
+        for (HandlerAdapter handlerAdapter : handlerAdapters) {
+            if (handlerAdapter.supports(handler)) {
+                return handlerAdapter;
+            }
+        }
+
+        return null;
+    }
+
+    private Object getHandler(final HttpServletRequest request) {
+        for (HandlerMapping handlerMapping : handlerMappings) {
+            final var handler = handlerMapping.getHandler(request);
+
+            if (handler != null) {
+                return handler;
+            }
+        }
```

</details>

### 인라인 코멘트 4190596692: jyt6640

- 상대방 발언, 참여자
- 시각: 2026-10-06T01:20:46Z
- [게시 원문](https://github.com/woowacourse/java-mvc/pull/1171#discussion_r4190596692)
- 코드: `mvc/src/main/java/com/interface21/webmvc/servlet/mvc/tobe/AnnotationHandlerMapping.java`, 현재 줄 None, 원래 줄 37
- 소속 리뷰 ID: 5422703793

> 1단계에서 `getDeclaredMethods()`를 유지한 이유로 현재 Controller에 직접 선언된 Handler만 등록하고 싶다고 말씀해주셨던 게 기억나는데요!
>
> 이번 미션에서는 `ReflectionUtils.getAllMethods(..., withAnnotation(RequestMapping.class))`를 이용해서 Handler 메서드를 탐색하는 방법을 제시하고 있네요.
>
> 현재 구현에서는 부모 클래스로부터 상속받은 `@RequestMapping` 메서드는 여전히 등록되지 않을 것 같은데, 이번에도 상속된 Handler를 지원하지 않는 것을 의도하신 걸까요?
>
> 미션에서 `getAllMethods()`를 제시한 이유와 현재 선택을 한번 비교해봐도 좋을 것 같습니다 🙂

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -1,40 +1,38 @@
 package com.interface21.webmvc.servlet.mvc.tobe;

-import com.interface21.context.stereotype.Controller;
 import com.interface21.web.bind.annotation.RequestMapping;
 import com.interface21.web.bind.annotation.RequestMethod;
+import com.interface21.webmvc.servlet.mvc.HandlerMapping;
 import jakarta.servlet.http.HttpServletRequest;
 import java.lang.reflect.Method;
 import java.lang.reflect.Modifier;
 import java.util.HashMap;
 import java.util.Map;
-import org.reflections.Reflections;
 import org.slf4j.Logger;
 import org.slf4j.LoggerFactory;

-public class AnnotationHandlerMapping {
+public class AnnotationHandlerMapping implements HandlerMapping {

     private static final Logger log = LoggerFactory.getLogger(AnnotationHandlerMapping.class);

-    private final Object[] basePackage;
+    private final ControllerScanner controllerScanner;
     private final Map<HandlerKey, HandlerExecution> handlerExecutions;

-    public AnnotationHandlerMapping(final Object... basePackage) {
-        this.basePackage = basePackage;
+    public AnnotationHandlerMapping(final ControllerScanner controllerScanner) {
+        this.controllerScanner = controllerScanner;
         this.handlerExecutions = new HashMap<>();
     }

-    public void initialize() {
-        final var reflections = new Reflections(basePackage);

-        reflections.getTypesAnnotatedWith(Controller.class)
+    public void initialize() {
+        controllerScanner.scan()
                 .forEach(this::registerController);

         log.info("Initialized AnnotationHandlerMapping!");
     }

-    private void registerController(final Class<?> controllerClass) {
-        final var controller = createController(controllerClass);
+    private void registerController(final Object controller) {
+        final var controllerClass = controller.getClass();

         for (Method method : controllerClass.getDeclaredMethods()) {
```

</details>

### 리뷰 본문 5422703793: jyt6640

- 상대방 발언, 참여자
- 시각: 2026-10-06T01:21:35Z
- [게시 원문](https://github.com/woowacourse/java-mvc/pull/1171#pullrequestreview-5422703793)
- 리뷰 상태: `CHANGES_REQUESTED`

> 안녕하세요 고래 !
>
> 휴일간 일정이 바쁘게 있어서 리뷰가 늦었네요 ㅠㅠ
>
> 그래도 코멘트 남겼는데 확인부탁합니다 !

### 리뷰 본문 5449920204: jyt6640

- 상대방 발언, 참여자
- 시각: 2026-10-08T00:15:24Z
- [게시 원문](https://github.com/woowacourse/java-mvc/pull/1171#pullrequestreview-5449920204)
- 리뷰 상태: `APPROVED`

> 일단 커밋 내역을 확인했을 떄 반영한 것으로 보이니 미션 종료하겠습니다 !
>
> 고생하셨습니다 !
