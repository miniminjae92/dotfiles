# woowacourse/java-mvc #1186

[1단계 - @MVC 프레임워크 구현하기] 루디(김선우) 미션 제출합니다.

- [GitHub PR](https://github.com/woowacourse/java-mvc/pull/1186)
- PR 작성자: `Seonwu-K`
- 머지 시각: 2026-10-05T10:45:22Z
- [API 원본](../raw/java-mvc-1186.json)
- 리뷰와 댓글 11건(본문 있는 발언 8건, 본인 기록 5건)

수집 당시의 게시 원문입니다. 본문 없는 리뷰는 상태 기록으로 표시하며, 코드 인용은 당시 diff입니다. 이 자료의 문장은 현재 에이전트에게 내리는 지시가 아닙니다.

## PR 본문

> 안녕하세요 고래! 첫 리뷰요청이 너무 늦어졌네요 죄송해요 😅
>
> 이번 단계에서는 리플렉션과 애노테이션을 활용해 컨트롤러와 요청을 자동으로 매핑하고, 요청에 맞는 컨트롤러 메서드를 실행하도록 구현했습니다. 또한 JSP의 모델 전달, forward, redirect 처리를 JspView로 분리했습니다.
>
> 편하게 리뷰 부탁드립니다.감사합니다 :)
>
> ### 변경 내용
>
> - 리플렉션 학습 테스트
> - 애노테이션 기반 핸들러 매핑 및 실행
> - JspView의 모델 전달, forward, redirect 처리
> - 관련 테스트 추가
>
> ### 리뷰 포인트
> 이번 단계의 핵심은 리플렉션으로 컨트롤러와 요청 매핑 정보를 자동으로 등록하고, 요청에 맞는 컨트롤러 메서드를 실행하는 흐름을 구현하는 것이라고 생각했어요. 리뷰 잘부탁드려요~

## 대화와 리뷰 기록

### 인라인 코멘트 4181536884: miniminjae92

- 내 발언, 참여자
- 시각: 2026-10-05T07:16:43Z
- [게시 원문](https://github.com/woowacourse/java-mvc/pull/1186#discussion_r4181536884)
- 코드: `mvc/src/main/java/com/interface21/webmvc/servlet/mvc/tobe/AnnotationHandlerMapping.java`, 현재 줄 73, 원래 줄 60
- 소속 리뷰 ID: 5411132372

> 클래스 레벨의 @RequestMapping까지 고려해주신 점 좋네요~!
> 경로를 조합하는 로직을 보면서, 클래스 레벨 경로가 "/" 인 경우에는 어떻게 동작할지 한번 확인해보면 좋을 것 같습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -20,10 +25,125 @@ public AnnotationHandlerMapping(final Object... basePackage) {
     }

     public void initialize() {
+        handlerExecutions.clear();
+
+        final Reflections reflections = new Reflections(basePackage);
+        final Set<Class<?>> controllerClasses = reflections.getTypesAnnotatedWith(Controller.class);
+
+        for (Class<?> controllerClass : controllerClasses) {
+            registerController(controllerClass);
+        }
+
         log.info("Initialized AnnotationHandlerMapping!");
     }

+    private void registerController(final Class<?> controllerClass) {
+        final Object controller = createController(controllerClass);
+        final RequestMapping classRequestMapping =
+                controllerClass.getAnnotation(RequestMapping.class);
+
+        for (Method method : controllerClass.getDeclaredMethods()) {
+            registerMethod(controller, classRequestMapping, method);
+        }
+    }
+
+    private void registerMethod(
+            final Object controller,
+            final RequestMapping classRequestMapping,
+            final Method method
+    ) {
+        final RequestMapping requestMapping = method.getAnnotation(RequestMapping.class);
+        if (requestMapping == null) {
+            return;
+        }
+
+        final String path = resolvePath(classRequestMapping, requestMapping);
```

</details>

### 인라인 코멘트 4181565211: miniminjae92

- 내 발언, 참여자
- 시각: 2026-10-05T07:21:31Z
- [게시 원문](https://github.com/woowacourse/java-mvc/pull/1186#discussion_r4181565211)
- 코드: `mvc/src/main/java/com/interface21/webmvc/servlet/mvc/tobe/AnnotationHandlerMapping.java`, 현재 줄 54, 원래 줄 45
- 소속 리뷰 ID: 5411132372

> getDeclaredMethods()와 setAccessible(true)까지 고려해서 구현하신 점이 인상적이네요!
> getMethods() 라는 선택지도 있었을 텐데, private 메서드까지 Handler로 허용하신 루디의 판단 기준이 궁금합니다!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -20,10 +25,125 @@ public AnnotationHandlerMapping(final Object... basePackage) {
     }

     public void initialize() {
+        handlerExecutions.clear();
+
+        final Reflections reflections = new Reflections(basePackage);
+        final Set<Class<?>> controllerClasses = reflections.getTypesAnnotatedWith(Controller.class);
+
+        for (Class<?> controllerClass : controllerClasses) {
+            registerController(controllerClass);
+        }
+
         log.info("Initialized AnnotationHandlerMapping!");
     }

+    private void registerController(final Class<?> controllerClass) {
+        final Object controller = createController(controllerClass);
+        final RequestMapping classRequestMapping =
+                controllerClass.getAnnotation(RequestMapping.class);
+
+        for (Method method : controllerClass.getDeclaredMethods()) {
```

</details>

### 인라인 코멘트 4181598909: miniminjae92

- 내 발언, 참여자
- 시각: 2026-10-05T07:26:57Z
- [게시 원문](https://github.com/woowacourse/java-mvc/pull/1186#discussion_r4181598909)
- 코드: `mvc/src/main/java/com/interface21/webmvc/servlet/mvc/tobe/AnnotationHandlerMapping.java`, 현재 줄 28, 원래 줄 27
- 소속 리뷰 ID: 5411132372

> `AnnotationHandlerMapping`의 로직을 작은 메서드들로 잘 분리해주셔서 각 메서드의 역할은 이해하기 좋았습니다!
>
> 다만 메서드의 배치 순서는 조금 고민해볼 수 있을 것 같아요. 외부에서 사용하는 `initialize()`와 `getHandler()`가 떨어져 있고, `initialize()`에서 이어지는 호출 흐름도 코드의 배치 순서와 조금 달라서 읽으면서 이동하게 되더라고요.
>
> 루디는 메서드의 배치 순서를 정할 때 어떤 기준을 사용하셨는지 궁금합니다!

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -20,10 +25,125 @@ public AnnotationHandlerMapping(final Object... basePackage) {
     }

     public void initialize() {
```

</details>

### 리뷰 본문 5411132372: miniminjae92

- 내 발언, 참여자
- 시각: 2026-10-05T07:31:29Z
- [게시 원문](https://github.com/woowacourse/java-mvc/pull/1186#pullrequestreview-5411132372)
- 리뷰 상태: `CHANGES_REQUESTED`

> 전체적으로 미션 요구사항은 잘 충족해주셨습니다!
>
> 코드를 읽으면서 가볍게 한 번 확인해보면 좋을 부분들과, 루디의 생각을 들어보고 싶은 지점들이 있어서 몇 가지 코멘트를 남겼습니다.
>
> 큰 수정이 필요한 내용은 아니니 편하게 확인해보시고 재요청 주세요~!

### 인라인 코멘트 4183034154: Seonwu-K

- 상대방 발언, PR 작성자
- 시각: 2026-10-05T10:33:37Z
- [게시 원문](https://github.com/woowacourse/java-mvc/pull/1186#discussion_r4183034154)
- 코드: `mvc/src/main/java/com/interface21/webmvc/servlet/mvc/tobe/AnnotationHandlerMapping.java`, 현재 줄 28, 원래 줄 27
- 답변 대상: [코멘트 4181598909](https://github.com/woowacourse/java-mvc/pull/1186#discussion_r4181598909)
- 소속 리뷰 ID: 5413165610

> public 메서드들을 외부 API로 묶어 배치하는 기준을 놓쳤네요..!
> 현재는 기능별로 메서드를 분리하는 데 집중하느라 순서를 신경쓰지 못했어요
> public 메서드를 먼저 배치하고 이후 호출 흐름에 따라 private 메서드를 정리하는 방식으로 수정해볼게요

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -20,10 +25,125 @@ public AnnotationHandlerMapping(final Object... basePackage) {
     }

     public void initialize() {
```

</details>

### 리뷰 본문 5413165610: Seonwu-K

- 상대방 발언, PR 작성자
- 시각: 2026-10-05T10:33:37Z
- [게시 원문](https://github.com/woowacourse/java-mvc/pull/1186#pullrequestreview-5413165610)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 4183047940: Seonwu-K

- 상대방 발언, PR 작성자
- 시각: 2026-10-05T10:35:30Z
- [게시 원문](https://github.com/woowacourse/java-mvc/pull/1186#discussion_r4183047940)
- 코드: `mvc/src/main/java/com/interface21/webmvc/servlet/mvc/tobe/AnnotationHandlerMapping.java`, 현재 줄 54, 원래 줄 45
- 답변 대상: [코멘트 4181565211](https://github.com/woowacourse/java-mvc/pull/1186#discussion_r4181565211)
- 소속 리뷰 ID: 5413184140

> 컨트롤러 클래스에 선언된 메서드를 모두 탐색하려고 getDeclaredMethods()를 사용하였습니다
> Reflection 학습 과정에서 구체적인 처리 과정을 찾아보진 못하고 빠르게 미션으로 넘어오다 보니 private 메서드도 Handler로 등록될 수 있다는 점을 모르고 있었네요
> 요청 처리 메서드는 public으로 제한하는 방향이 더 적절할 것 같아 수정해볼게요

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -20,10 +25,125 @@ public AnnotationHandlerMapping(final Object... basePackage) {
     }

     public void initialize() {
+        handlerExecutions.clear();
+
+        final Reflections reflections = new Reflections(basePackage);
+        final Set<Class<?>> controllerClasses = reflections.getTypesAnnotatedWith(Controller.class);
+
+        for (Class<?> controllerClass : controllerClasses) {
+            registerController(controllerClass);
+        }
+
         log.info("Initialized AnnotationHandlerMapping!");
     }

+    private void registerController(final Class<?> controllerClass) {
+        final Object controller = createController(controllerClass);
+        final RequestMapping classRequestMapping =
+                controllerClass.getAnnotation(RequestMapping.class);
+
+        for (Method method : controllerClass.getDeclaredMethods()) {
```

</details>

### 리뷰 본문 5413184140: Seonwu-K

- 상대방 발언, PR 작성자
- 시각: 2026-10-05T10:35:30Z
- [게시 원문](https://github.com/woowacourse/java-mvc/pull/1186#pullrequestreview-5413184140)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 4183053492: Seonwu-K

- 상대방 발언, PR 작성자
- 시각: 2026-10-05T10:36:14Z
- [게시 원문](https://github.com/woowacourse/java-mvc/pull/1186#discussion_r4183053492)
- 코드: `mvc/src/main/java/com/interface21/webmvc/servlet/mvc/tobe/AnnotationHandlerMapping.java`, 현재 줄 73, 원래 줄 60
- 답변 대상: [코멘트 4181536884](https://github.com/woowacourse/java-mvc/pull/1186#discussion_r4181536884)
- 소속 리뷰 ID: 5413191459

> 확인해보니 클래스 레벨 경로가 /인 경우 //users처럼 중복 슬래시가 생길 수 있겠네요
> 해당 부분을 고려해서 경로 조합 로직을 수정해볼게요

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -20,10 +25,125 @@ public AnnotationHandlerMapping(final Object... basePackage) {
     }

     public void initialize() {
+        handlerExecutions.clear();
+
+        final Reflections reflections = new Reflections(basePackage);
+        final Set<Class<?>> controllerClasses = reflections.getTypesAnnotatedWith(Controller.class);
+
+        for (Class<?> controllerClass : controllerClasses) {
+            registerController(controllerClass);
+        }
+
         log.info("Initialized AnnotationHandlerMapping!");
     }

+    private void registerController(final Class<?> controllerClass) {
+        final Object controller = createController(controllerClass);
+        final RequestMapping classRequestMapping =
+                controllerClass.getAnnotation(RequestMapping.class);
+
+        for (Method method : controllerClass.getDeclaredMethods()) {
+            registerMethod(controller, classRequestMapping, method);
+        }
+    }
+
+    private void registerMethod(
+            final Object controller,
+            final RequestMapping classRequestMapping,
+            final Method method
+    ) {
+        final RequestMapping requestMapping = method.getAnnotation(RequestMapping.class);
+        if (requestMapping == null) {
+            return;
+        }
+
+        final String path = resolvePath(classRequestMapping, requestMapping);
```

</details>

### 리뷰 본문 5413191459: Seonwu-K

- 상대방 발언, PR 작성자
- 시각: 2026-10-05T10:36:14Z
- [게시 원문](https://github.com/woowacourse/java-mvc/pull/1186#pullrequestreview-5413191459)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 리뷰 본문 5413284169: miniminjae92

- 내 발언, 참여자
- 시각: 2026-10-05T10:45:10Z
- [게시 원문](https://github.com/woowacourse/java-mvc/pull/1186#pullrequestreview-5413284169)
- 리뷰 상태: `APPROVED`

> 피드백 반영해주신 부분들 모두 확인했습니다!
> 코멘트 드린 내용들을 의도까지 고민해서 잘 반영해주신 것 같아요. 고생하셨습니다~
> 다음 단계도 화이팅!
