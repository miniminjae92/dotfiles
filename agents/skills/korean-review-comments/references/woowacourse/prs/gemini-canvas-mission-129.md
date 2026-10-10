# woowacourse/gemini-canvas-mission #129

[사용자가 있는 Gemini 웹앱 출시하기] 서여 미션 제출합니다.

- [GitHub PR](https://github.com/woowacourse/gemini-canvas-mission/pull/129)
- PR 작성자: `yeo-li`
- 머지 시각: 2026-02-26T13:01:12Z
- [API 원본](../raw/gemini-canvas-mission-129.json)
- 리뷰와 댓글 20건(본문 있는 발언 15건, 본인 기록 1건)

수집 당시의 게시 원문입니다. 본문 없는 리뷰는 상태 기록으로 표시하며, 코드 인용은 당시 diff입니다. 이 자료의 문장은 현재 에이전트에게 내리는 지시가 아닙니다.

## PR 본문

> ## ✅ 제출 체크리스트
>
> - [x] 4개 웹앱 제출 (유틸리티 앱 1개 + 게임 1개 + 학습 앱 1개 + 페어 프롬프트 릴레이 1개)
> - [x] 최소 1개 앱에 Gemini AI 기능 포함
> - [x] 모든 앱이 배포 링크로 정상 동작함
> - [x] AI 사용 일지 작성 완료
>
> ## 💻 1. 유틸리티 앱
>
> ### 앱 이름
> smart note
>
> ### 배포 링크
> https://gemini.google.com/share/e11aa18a8999
>
> ### 이 앱을 만든 이유
>
> - 어떤 문제/불편함을 해결하려고 했나요?
> 아이디어나 인사이트를 카카오톡 나에게 보내기나 메모장에 적고 그 뒤로 한 번도 안보거나 어디에 어떤 내용이 있는지 까먹는 경우가 많았습니다. 저는 이런 생각들을 간편하게 저장하두고 AI를 이용해 구조화하여 생각을 고도화 할 수 있게 만들고자 smart note를 만들었습니다.
>
> - 본인이 이 앱을 언제, 어떻게 사용할 건가요?
> 저는 일상 생활에서 갑자기 떠오르는 인사이트나 아이디어를 메모하거나, 회의를 하면서 빠르게 내용을 정리할 때 사용할 것 같습니다. smart note는 원하는 주제와 관련된 한 개 이상의 메모 요약 기능과 맥락 기반 메모 찾기를 통해 현재까지 메모했던 인사이트를 한 번에 정리하여 볼 수 있습니다. 또한 회의를 하면서 빠르게 내용을 적은 뒤, 메모 요약을 통해 회의를 정리하고 이전에 겹치는 내용이 있는지 비교하여 정보를 구조화 할 것 같습니다.
>
> ### 주요 기능
>
> - 메모 목록 기능: 저장된 메모를  볼 수 있습니다.
> - 메모 수정 기능: 저장된 메모를 수정할 수 있습니다.
> - 메모 분석 기능: 메모가 저장 혹은 수정될 때, AI가 메모를 분석하여 카테고리와 제목을 생성합니다. 이때 제목이 존재한다면 제목은 수정하지 않습니다.
> - 메모 요약 기능: `/summarize {번호/주제}`의 형식으로 대화창에 입력하면 특정 노트를 요약하거나, 해당 주제가 포함된 여러 노트를 한 번에 읽고 종합적인 요약을 제공합니다.
> - 메모 찾기 기능: `/find {프롬프트}`의 형식으로 대화창에 입력하면 단순 검색을 넘어 AI가 맥락을 파악해 관련 노트를 목록으로 보여줍니다.
>
> ### AI 기능 (해당되는 경우)
>
> - 어떤 AI 기능을 추가했나요?
> AI를 이용해 메모를 분석하는 기능과, 메모를 요약 및 탐색하는 기능을 추가했습니다.
>
> - AI 기능이 앱에서 어떤 역할을 하나요?
> AI는 저장도니 메모를 분류 및 재가공하는 관리자의 역할을 합니다. 메모의 원본은 별도의 저장 장치에 저장되어 변형이 없지만, 메모 원본을 사용자가 원하는 형태로 맞게 정리하고 요약해주기 때문입니다.
>
> ## 🎮 2. 게임
>
> ### 앱 이름
> 혼자서도 즐기는 캐치마인드
>
> ### 배포 링크
> https://gemini.google.com/share/0b16993e298f
>
> ### 이 앱을 만든 이유
>
> - 어떤 문제/불편함을 해결하려고 했나요?
> 캐치마인드를 하려면 반드시 두 명 이상 있어야 한다는 치명적인 단점이 있었습니다. 저는 이런 문제를 해결하기 위해, AI가 문제를 내면 사용자가 맞출 수 있도록 해 혼자서도 캐치마인드를 즐길 수 있는 혼자서도 즐기는 캐치마인드 앱을 만들었습니다.
>
> - 본인이 이 앱을 언제, 어떻게 사용할 건가요?
> 저는 등하교때 통학 시간이 긴데, 이때 캐치마인드를 하며 시간을 보낼 것 같습니다.
>
> ### 주요 기능
>
> - 키워드 추출 기능: AI가 그림을 그릴 키워드를 추출합니다.
> - 키워드 그림 생성 기능: AI가 키워드와 관련된 그림을 그립니다. 이때, 키워드가 직접적으로 연상되지 않도록 생성을 강제합니다.
> - 사용자 입력값 비교 기능: 사용자가 그림을 보고 예상 정답을 입력하면, 정답과 비교하여 정답 유무를 출력합니다.
> - 힌트 보기 기능: AI가 키워드를 연상할 수 있는 간접적인 힌트 3개를 생성합니다.
>
> ### AI 기능 (해당되는 경우)
>
> - 어떤 AI 기능을 추가했나요?
> AI 그림 및 힌트 생성 기능을 추가했습니다.
>
> - AI 기능이 앱에서 어떤 역할을 하나요?
> AI는 문제 출제자 역할(게임 호스트)을 하고 있습니다.
>
> ## 📚 3. 학습 앱
>
> ### 앱 이름
> BFS 학습앱
>
> ### 배포 링크
> https://gemini.google.com/share/2a2237df4bc2
>
> ### 이 앱을 만든 이유
>
> - 어떤 문제/불편함을 해결하려고 했나요?
> 알고리즘에서 그래프를 처음 공부할 때, 머릿속으로만 상상하다보니 이해하기 어려웠습니다. 따라서 이를 시각화 하여 확인하고 그래프를 이해하기 위해 만들었습니다.
>
> - 본인이 이 앱을 언제, 어떻게 사용할 건가요?
> BFS에 대해 복습을 할 때 사용할 것 같습니다.
>
> ### 주요 기능
>
> - BFS 시각화 기능: BFS가 어떻게 진행되는지 시각화 하여 제시합니다.
> - BFS 관련 퀴즈 기능: BFS와 관련된 퀴즈를 제시합니다.
> - BFS 구현 코드 제공 기능: BFS를 구현한 코드를 제시합니다.
>
> ## 🤝 4. 페어 프롬프트 릴레이 앱
>
> ### 앱 이름
> Team Convention Master(이하 TCM)
>
> ### 페어
> @Chocoding1
>
> ### 배포 링크
> https://gemini.google.com/share/68c7b240fe86
>
> ### 이 앱을 만든 이유
>
> - 어떤 문제/불편함을 해결하려고 했나요?
> 팀 컨벤션 결정 후, 즉각적인 컨벤션 준수가 어려운 팀원들에게 도움을 주기 위해 만들었습니다.
> 또한 팀 컨벤션을 최초에 정할 때, 회의를 하며 정리한 내용을 AI로 자동으로 정리해주어 컨벤션 문서 작성의 번거로움을 효과적으로 줄였습니다.
>
> - 본인이 이 앱을 언제, 어떻게 사용할 건가요?
> 우아한테크코스에서 페어 매칭을 하거나 팀 프로젝트를 진행할 때, TCM을 사용하여 초기 팀 컨벤션을 빠르게 문서화하여 시간 자원을 효율적으로 사용할 것입니다.
>
> ### 주요 기능
>
> - 팀 기술 스택 지정 기능: 팀 내에서 사용하는 IDE와 개발 언어를 선택할 수 있습니다.
> - 컨벤션 작성 기능: 팀 내의 컨벤션을 카테고리별로 작성할 수 있습니다.
> - AI 컨벤션 문서화 기능: 자연어로 도출된 컨벤션을 AI가 IDE 설정 파일과 문서로 생성해줍니다.
>
> ### AI 기능 (해당되는 경우)
>
> - 어떤 AI 기능을 추가했나요?
> 자연어로 도출된 컨벤션을 AI를 사용해 문서화 하는 기능을 추가했습니다.
>
> - AI 기능이 앱에서 어떤 역할을 하나요?
> 문서를 자동으로 생성해줌으로써, 시간 절약에 도움이 됩니다.
>
> ## 📝 AI 사용 일지
> - 본인 기준으로 가장 잘 만들어진 앱 1개를 골라주세요.
> - 아래 불릿 포인트는 예시입니다. 각 항목의 취지를 참고해 본인의 실제 경험을 중심으로 자유롭게 작성해 주세요.
>
> ### 대상 앱 이름
>
> ### 1. 초기 프롬프트
> ```text
> 팀 프로젝트를 할 때 정해진 팀 컨벤션을 자동으로 IDE에 적용되도록 하고 싶어. 그럴 수 있게 팀 컨벤션을 입력하면 그에 맞는 xml 파일을 생성하는 앱을 만들어줘.
> 이 앱은 팀프로젝트를 진행하는 개발자들을 대상으로 하는 거고, 카테고리별로 정해진 컨벤션들을 리스트로 입력할 수 있도록 해줘.
> 기술 스택은 html, css, js만 사용해서 만들어줘.
> ```
>
> 처음 Gemini에게 입력한 프롬프트를 그대로 적어주세요.
>
> ### 2. 프롬프트 개선 과정
>
> - 처음 결과물의 문제점은 무엇이었나요?
> 저는 컨벤션을 자연어로 작성하고 이를 AI를 이용해 IDE 전용 설정 파일을 만들고 싶었습니다. 하지만 결과는 지정된 템플릿에 변수를 입력 받으면 단순히 그 자리에 값만 변경되는 형식으로 개발되어 의도와는 다르게 결과물이 도출되는 문제가 있었습니다.
>
> - 어떤 식으로 프롬프트를 수정했나요?
> AI가 코드를 수정할 때, 코드를 부분만 수정하는 것이 아니라, 전면 수정하여 변경을 원하지 않는 부분도 변경되는 문제가 있었습니다. 따라서 이런 문제를 해결하기 위해 프롬프트 입력 마다 `기존의 코드를 절대 변경하지 말라` 라는 프롬프트를 추가하여 변경에 제약사항을 주었습니다.
>
> - 몇 번의 반복을 거쳤나요?
> 총 14번 반복했습니다.
>
> ### 3. 효과적이었던 프롬프팅 전략
>
> 우선 효과에 대해 간단히 정의하겠습니다. 바이브 코딩에서의 좋은 효과는 개발자가 가지고 있는 느낌 또는 수준을 AI를 통해 코드로 도출해 내는 것이라고 생각합니다. 이 정의를 바탕으로 효과적이거나 효과가 없었던 사례를 제시하겠습니다.
>
> - 어떤 방식으로 요청했을 때 원하는 결과가 나왔나요?
> 1. 코드를 절대 변경하지 말라고 이야기 하라 : gemini를 이용해 기능을 개선하다보면, 변경을 원하지 않는 코드까지 변경되는 문제가 있었습니다. 이를 해결하기 위해 프롬프트마다 코드를 절대 변경하지말거나 최소한의 변경만 하라는 명령어를 추가하면 의도대로 생성될 확률이 올라가 더 효과적인 개발을 할 수 있었습니다.
>
> 2. AI와 소통할 문서를 만들어라 : 기능은 자연어를 통해 고도화 할 수 있었지만, 화면 ui를 개선하고 싶을때는 이를 정확히 짚기 어려웠습니다. 저는 이런 문제를 해결하기 위해 AI에게 화면의 모든 요소에 라벨링을 하여 문서를 생성하도록 하여 기능이나 디자인을 변경할 때, 이 문서를 기반으로 위치를 AI에게 전달하여 더 정확하고 빠른 결과 도출을 할 수 있었습니다.
>
> - 반대로 효과가 없었던 방식은 어떤게 있었나요?
> 잘 못하거나 지식이 전무한 분야의 요구사항을 구체적으로 작성하니 오히려 원하는 결과가 나오지 않았습니다. 이번 미션에서는 AI에게 구체적으로 제시를 하기 위해 의도적으로 노력했습니다. 그렇기에 디자인을 잘하진 못하지만 구체적으로 제시하여 개발을 진행했습니다. 하지만 결과는 원하는 디자인 퀄리티로 나오지 않았습니다. 그리고 비교를 위해 다른 주제의 미션에서는 기능만 구체적으로 명시하고 디자인을 강제하지 않았더니 더 만족할만한 결과물이 나왔습니다.
>
> ### 4. 배운 점
>
> - Gemini Canvas를 효과적으로 사용하기 위한 나만의 팁이 있다면?
>
> 1. 마음가짐 팁
> - Gemini Canvas는 프로토타입을 빠르게 만들어준다는 것을 분명히 인지하고 사용하면 더 좋은 효과를 얻을 수 있을 것 같습니다. 이 목적을 분명히 하면, 추상적인 아이디어를 시각화 하여 기존의 아이디어를 개선하거나 부족한 부분을 확인하는데 사용할 수 있습니다. 하지만 프로토타입을 넘어서는 완전한 프로덕트를 Gemini Canvas를 이용해 만들고자 하는 목적을 가진다면, 시간이 오래걸리거나 목적 달성에 실패할 것 같습니다.
>
> 2. 프롬프트 팁(3번 문항 재사용)
> - 코드를 절대 변경하지 말라고 이야기 하라 : gemini를 이용해 기능을 개선하다보면, 변경을 원하지 않는 코드까지 변경되는 문제가 있었습니다. 이를 해결하기 위해 프롬프트마다 코드를 절대 변경하지말거나 최소한의 변경만 하라는 명령어를 추가하면 의도대로 생성될 확률이 올라가 더 효과적인 개발을 할 수 있었습니다.
>
> - AI와 소통할 문서를 만들어라 : 기능은 자연어를 통해 고도화 할 수 있었지만, 화면 ui를 개선하고 싶을때는 이를 정확히 짚기 어려웠습니다. 저는 이런 문제를 해결하기 위해 AI에게 화면의 모든 요소에 라벨링을 하여 문서를 생성하도록 하여 기능이나 디자인을 변경할 때, 이 문서를 기반으로 위치를 AI에게 전달하여 더 정확하고 빠른 결과 도출을 할 수 있었습니다.
>
> ### 5. 리뷰어에게 피드백 받고 싶은 포인트
> AI를 사용한 방법과 결과물에 대한 피드백을 받고싶습니다!

## 대화와 리뷰 기록

### 인라인 코멘트 2858693854: echo724

- 상대방 발언, 참여자
- 시각: 2026-02-26T12:14:40Z
- [게시 원문](https://github.com/woowacourse/gemini-canvas-mission/pull/129#discussion_r2858693854)
- 코드: `smart_note.html`, 현재 줄 1, 원래 줄 1
- 소속 리뷰 ID: 3860547767

> <img width="1356" height="545" alt="Image" src="https://github.com/user-attachments/assets/0ace830c-ade0-4f71-ada2-7400c6024982" />
>
> - 위의 스크린샷과 같이 `/find {검색어}`나 `/summarize {키워드}`를 입력할 경우, 알파벳으로 입력할 경우에는 괜찮지만 한글로 입력할 경우, 마지막 글자가 다시 입력되고 입력된 글자로 노트가 생성되는 버그가 있습니다. 왜 이런 버그가 일어났나요?
>
> <img width="947" height="181" alt="Image" src="https://github.com/user-attachments/assets/d950342d-93ba-4252-be3f-fbe433048482" />
> - 입력칸이 `메모` 아니면 `명령어`를 받는 형태인데, `무엇을 도와드릴까요?`라는 placeholder text가 ai에게 프롬프트를 입력해야하는 것처럼 보이게 만들어서 이 부분 text가 노트 생성 이나 명령어 입력 등 좀 더 명확하면 좋을 것 같아요!
> - 시험삼아 프롬프트 해킹도 시도해보려고 했는데 안되더라구요 ㅎㅎ,, 잘 구현하신 것 같습니다. 따로 프롬프트 validation이나 sanitisation 하신 부분이 있을까요?

### 인라인 코멘트 2858733962: echo724

- 상대방 발언, 참여자
- 시각: 2026-02-26T12:24:15Z
- [게시 원문](https://github.com/woowacourse/gemini-canvas-mission/pull/129#discussion_r2858733962)
- 코드: `혼자서도_즐기는_캐치마인드.html`, 현재 줄 1, 원래 줄 1
- 소속 리뷰 ID: 3860547767

> 이 게임 하다가 시간 가는줄 모르고 했습니다.. 이미지와 힌트가 AI가 만들었음에도 창의적인 것 같아서 좋은 활용 예시인 것 같습니다! 가능하면 이걸로 서비스도 내보시거나 해보세요 인기가 좀 있을듯 합니다 ㅎㅎ

### 인라인 코멘트 2858774613: echo724

- 상대방 발언, 참여자
- 시각: 2026-02-26T12:33:31Z
- [게시 원문](https://github.com/woowacourse/gemini-canvas-mission/pull/129#discussion_r2858774613)
- 코드: `혼자서도_즐기는_캐치마인드.html`, 현재 줄 135, 원래 줄 135
- 소속 리뷰 ID: 3860547767

> 제안: 이 부분 명시를 하셨는데도 이미지에서 의미없는 알파벳이 몇 번 뜨더라구요. 아무래도 심볼로서 알파벳이 사용된 것 같은데 이부분도 막아야할 것 같습니다.

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,374 @@
+import React, { useState, useEffect, useCallback, useRef } from 'react';
+import { Palette, Lightbulb, Send, RefreshCw, Trophy, AlertCircle, Loader2, Heart, HeartOff, Brain, HelpCircle } from 'lucide-react';
+
+const apiKey = ""; // 환경 제공 키 사용
+
+const API_TEXT_URL = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=${apiKey}`;
+const API_IMAGE_URL = `https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key=${apiKey}`;
+
+// 카테고리별 단어 풀
+const WORDS_DATABASE = [
+  { word: "비행기", category: "교통수단" }, { word: "피아노", category: "악기" }, { word: "북극곰", category: "동물" },
+  { word: "무지개", category: "자연" }, { word: "자전거", category: "교통수단" }, { word: "여권", category: "여행" },
+  { word: "시간", category: "추상어" }, { word: "우정", category: "추상어" }, { word: "스마트폰", category: "기계" },
+  { word: "도서관", category: "장소" }, { word: "지구", category: "자연" }, { word: "선인장", category: "식물" },
+  { word: "망원경", category: "도구" }, { word: "카메라", category: "도구" }, { word: "돋보기", category: "도구" },
+  { word: "잠수함", category: "교통수단" }, { word: "등대", category: "건물" }, { word: "열기구", category: "교통수단" },
+  { word: "나침반", category: "도구" }, { word: "우주선", category: "교통수단" }, { word: "화산", category: "자연" },
+  { word: "폭포", category: "자연" }, { word: "눈사람", category: "겨울" }, { word: "모래시계", category: "도구" },
+  { word: "편지", category: "통신" }, { word: "향수", category: "미용" }, { word: "보물상자", category: "물건" },
+  { word: "성", category: "건물" }, { word: "열쇠", category: "물건" }, { word: "안경", category: "물건" },
+  { word: "신발", category: "의류" }, { word: "우산", category: "물건" }, { word: "촛불", category: "물건" },
+  { word: "거울", category: "물건" }, { word: "시계", category: "물건" }, { word: "지도", category: "여행" },
+  { word: "기타", category: "악기" }, { word: "드럼", category: "악기" }, { word: "바이올린", category: "악기" },
+  { word: "축구공", category: "스포츠" }, { word: "연필", category: "문구" }, { word: "지갑", category: "물건" },
+  { word: "청소기", category: "가전" }, { word: "냉장고", category: "가전" }, { word: "선풍기", category: "가전" },
+  { word: "에어컨", category: "가전" }, { word: "텔레비전", category: "가전" }, { word: "컴퓨터", category: "가전" },
+  { word: "마우스", category: "가전" }, { word: "키보드", category: "가전" }, { word: "칫솔", category: "위생" },
+  { word: "비누", category: "위생" }, { word: "수건", category: "위생" }, { word: "침대", category: "가구" },
+  { word: "베개", category: "가구" }, { word: "거실", category: "장소" }, { word: "부엌", category: "장소" },
+  { word: "화장실", category: "장소" }, { word: "지하실", category: "장소" }, { word: "계단", category: "구조물" },
+  { word: "사탕", category: "음식" }, { word: "초콜릿", category: "음식" }, { word: "아이스크림", category: "음식" },
+  { word: "햄버거", category: "음식" }, { word: "피자", category: "음식" }, { word: "김밥", category: "음식" },
+  { word: "떡볶이", category: "음식" }, { word: "라면", category: "음식" }, { word: "커피", category: "음식" },
+  { word: "우유", category: "음식" }, { word: "사과", category: "과일" }, { word: "바나나", category: "과일" },
+  { word: "포도", category: "과일" }, { word: "수박", category: "과일" }, { word: "딸기", category: "과일" },
+  { word: "오렌지", category: "과일" }, { word: "복숭아", category: "과일" }, { word: "파인애플", category: "과일" },
+  { word: "망고", category: "과일" }, { word: "키위", category: "과일" }, { word: "호랑이", category: "동물" },
+  { word: "사자", category: "동물" }, { word: "코끼리", category: "동물" }, { word: "기린", category: "동물" },
+  { word: "얼룩말", category: "동물" }, { word: "원숭이", category: "동물" }, { word: "토끼", category: "동물" },
+  { word: "강아지", category: "동물" }, { word: "고양이", category: "동물" }, { word: "햄스터", category: "동물" },
+  { word: "고래", category: "동물" }, { word: "상어", category: "동물" }, { word: "문어", category: "동물" },
+  { word: "오징어", category: "동물" }, { word: "게", category: "동물" }, { word: "조개", category: "동물" },
+  { word: "불가사리", category: "동물" }, { word: "해파리", category: "동물" }, { word: "물고기", category: "동물" },
+  { word: "거북이", category: "동물" }
+];
+
+const App = () => {
+  const [usedWords, setUsedWords] = useState([]);
+  const [currentProblem, setCurrentProblem] = useState(null);
+  const [image, setImage] = useState(null);
+  const [userInput, setUserInput] = useState("");
+  const [gameState, setGameState] = useState('idle'); // idle, loading, playing, won, lost
+  const [visibleHintCount, setVisibleHintCount] = useState(0);
+  const [loadingStep, setLoadingStep] = useState("");
+  const [score, setScore] = useState(0);
+  const [wrongCount, setWrongCount] = useState(0);
+  const [error, setError] = useState(null);
+  const [isShaking, setIsShaking] = useState(false);
+
+  const MAX_ATTEMPTS = 5;
+
+  const fetchWithRetry = async (url, options, retries = 5, backoff = 1000) => {
+    try {
+      const response = await fetch(url, options);
+      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
+      return await response.json();
+    } catch (err) {
+      if (retries > 0) {
+        await new Promise(resolve => setTimeout(resolve, backoff));
+        return fetchWithRetry(url, options, retries - 1, backoff * 2);
+      }
+      throw err;
+    }
+  };
+
+  const startNewGame = useCallback(async () => {
+    setGameState('loading');
+    setError(null);
+    setVisibleHintCount(0);
+    setUserInput("");
+    setImage(null);
+    setWrongCount(0);
+
+    try {
+      let available = WORDS_DATABASE.filter(item => !usedWords.includes(item.word));
+      if (available.length === 0) {
+        available = [...WORDS_DATABASE];
+        setUsedWords([]);
+      }
+      const picked = available[Math.floor(Math.random() * available.length)];
+      setCurrentProblem(picked);
+      setUsedWords(prev => [...prev, picked.word]);
+
+      setLoadingStep(`${picked.category} 분야의 문제를 준비하는 중...`);
+
+      // 힌트 및 리버스(캐치마인드) 전략 수립
+      const brainResponse = await fetchWithRetry(API_TEXT_URL, {
+        method: 'POST',
+        headers: { 'Content-Type': 'application/json' },
+        body: JSON.stringify({
+          contents: [{
+            parts: [{
+              text: `단어: '${picked.word}'. 카테고리: '${picked.category}'.
+              이 단어를 시각적 넌센스(리버스) 캐치마인드 퀴즈로 만들기 위한 2~3개의 상징물 조합을 제안하고, 힌트 3개를 작성해줘.
+
+              [중요 규칙]
+              1. 모든 힌트는 반드시 '한글'로 작성할 것.
+              2. 힌트에서 정답 단어를 직접적으로 묘사하거나 언급하지 말 것.
+              3. 대신 그림 속 상징물들이 무엇을 의미하는지나, 단어의 음절을 비유적으로 표현할 것.
+
+              Respond strictly in JSON format:
+              {
+                "visual_strategy": "Detailed English description of symbols for image generator. NO TEXT.",
+                "hints": ["첫 번째 상징에 대한 비유적 힌트", "두 번째 상징 또는 단어 구성에 대한 은유적 힌트", "정답을 연상시키는 결정적인 넌센스 힌트"]
+              }`
+            }]
+          }],
+          generationConfig: { responseMimeType: "application/json" },
+          systemInstruction: {
+            parts: [{ text: "당신은 기발한 캐치마인드 퀴즈 마스터입니다. 사용자가 머리를 써서 정답을 유추할 수 있도록 은유적이고 기발한 힌트를 제공하세요. 모든 힌트는 한글이어야 합니다." }]
+          }
+        })
+      });
+
+      const data = JSON.parse(brainResponse.candidates[0].content.parts[0].text);
+      setCurrentProblem(prev => ({ ...prev, hints: data.hints }));
+
+      // 이미지 생성
+      setLoadingStep("AI가 캔버스에 캐치마인드 그림을 그리는 중...");
+      const finalImagePrompt = `A 2 or 3 panel rebus puzzle for '${picked.word}'.
+        Visual strategy: ${data.visual_strategy}.
+        Style: Simple child drawing, 10 years old artist, vibrant crayons.
+        Colors: Red, Blue, Yellow, Green, Black only.
+        Background: Clean white paper.
+        CRITICAL: NO LETTERS, NO NUMBERS, NO CHARACTERS. Use only icons and symbols.`;
```

</details>

### 인라인 코멘트 2858801188: echo724

- 상대방 발언, 참여자
- 시각: 2026-02-26T12:38:56Z
- [게시 원문](https://github.com/woowacourse/gemini-canvas-mission/pull/129#discussion_r2858801188)
- 코드: `BFS_시각화_학습_도구_앱.html`, 현재 줄 1, 원래 줄 1
- 소속 리뷰 ID: 3860547767

> <img width="704" height="488" alt="Image" src="https://github.com/user-attachments/assets/b56afc01-c22f-4743-bc99-8563e247321a" />
>
> - 제안: `탐색시작`을 누른뒤, `구조 재설정`을 하면 탐색이 초기화 되지 않고 변경된 구조에서 탐색을 이어서 하더라구요. 이 부분 구조 재설정을 탐색 중에는 못하게 하던가 아니면 탐색을 새로 하는 방법으로 변경이 필요해 보입니다!

### 인라인 코멘트 2858834139: echo724

- 상대방 발언, 참여자
- 시각: 2026-02-26T12:45:23Z
- [게시 원문](https://github.com/woowacourse/gemini-canvas-mission/pull/129#discussion_r2858834139)
- 코드: `team_convention_master.html`, 현재 줄 1, 원래 줄 1
- 소속 리뷰 ID: 3860547767

> 실제로 협업하는데 있어서 도움이 되는 툴 만드셨네요! 이거 코드 컨벤션 설정하는 것도 일인데 자연어 → 설정으로 인해 직관적으로 설정할 수 도 있고, 다운로드, 공유도 쉬워서 도움이 실제로 될 것 같습니다! 하나 생각난 아이디어는 `설정` → `자연어` 방식도 지원해보면 어떨까요? 내가 가지고 있는 설정을 upload하면 자연어로 어떤 설정 항목이 있는지도 보여주고 거기서 추가/삭제 등의 재가공을 지원하는 것도 유용할 것 같아요!
>
> 개선할 점은 아래 스크린샷 처럼 팀가이드 markdown 코드 블럭 부분이 깨집니다.
> <img width="686" height="170" alt="Image" src="https://github.com/user-attachments/assets/8fa3b195-ec3c-4860-bdab-2c289cd75a31" />
>
>

### 리뷰 본문 3860547767: echo724

- 상대방 발언, 참여자
- 시각: 2026-02-26T13:00:59Z
- [게시 원문](https://github.com/woowacourse/gemini-canvas-mission/pull/129#pullrequestreview-3860547767)
- 리뷰 상태: `APPROVED`

> 안녕하세요 @yeo-li
> 전반적으로 AI를 활용해서 유용하고 재미있는 앱들 만드셨네요! 게임은 시간 가는줄 모르고 몇 번 했습니다 ㅋㅋ ㅜ
> 프롬프트 개선 과정과 전략 읽어봤는데 저와 비슷한 AI 개발 경험을 하셨더라구요. 저도 클로드 설정 UI 툴을 AI로 만들었었는데, 설정 파일 특성상 정확한 값을 요구하는 경우가 많지만 AI가 임의로 변경하거나 만드는 경우가 있더라구요. 저는 설정 가능한 값을 설명한 공식문서를 context에 넣어줘서 해결한 경험이 있습니다. 그래서 AI가 변경/수정 가능한 범위를 지정해주는 것도 방법이지 않을까 합니다!
>
> 질문 주신 부분에 대해서는 AI 기능을 각 앱의 특성에 맞게 적절히 사용하신 것 같아 크게 피드백 드릴 부분은 없습니다. 다만 한 가지 떠오른 건, AI 기능을 사용할 경우, 아웃풋이 일정하지 않고 아웃풋 만드는데 걸리는 시간이 있어서 이 두가지 경우는 미리 AI asset을 만들어두고 만들어진 asset으로 불러오는 것도 좋은 방법인 것 같습니다. 예를 들어서 AI 캐치마인드 같은 경우에도 사실 유저 인풋이 없기 때문에 미리 Asset을 생성해서 유저에게 랜덤하게 보여주면 같은 경험으로 더 좋은 유저 경험을 줄 수 있다고 생각합니다!
>
> 전반적으로 AI 기능을 적절하게 활용하시고 전체적인 기능과 만들고자 했던 앱이 완성된 것 같아 바로 머지 하도록 하겠습니다! 개선 제안 커멘트를 몇 개 남기긴 했는데 참고해보세요~ 수고 많으셨습니다

### 일반 댓글 3970162380: Chocoding1

- 상대방 발언, 참여자
- 시각: 2026-02-27T01:16:22Z
- [게시 원문](https://github.com/woowacourse/gemini-canvas-mission/pull/129#issuecomment-3970162380)

> [캐치마인드]
> 열린 힌트 개수에 따라 점수가 감소하는 기능도 있으면 좋겠습니다!
>
> [BFS 학습앱]
> 추후에 BFS 뿐만 아니라 다른 알고리즘들도 추가해주시면 도움이 많이 될 거 같습니다!

### 일반 댓글 3970173949: miniminjae92

- 내 발언, 참여자
- 시각: 2026-02-27T01:21:05Z
- [게시 원문](https://github.com/woowacourse/gemini-canvas-mission/pull/129#issuecomment-3970173949)

> [smart note]
> 이전 다른 메모를 파일 넣기로 추가할 수 있으면 좋을 것 같습니다.
>
> [캐치마인드]
> 홈으로 가거나 다시 시작 기능이 있어도 좋을 것 같습니다.

### 일반 댓글 3970209150: e9ua1

- 상대방 발언, 참여자
- 시각: 2026-02-27T01:33:14Z
- [게시 원문](https://github.com/woowacourse/gemini-canvas-mission/pull/129#issuecomment-3970209150)

> [smart note]
> 의 명령어 셋이 더 많으면 좋을 거 같아요. 예를 들어 여러 요약을 통합한다던지 하는?

### 일반 댓글 3970479461: yeo-li

- 상대방 발언, PR 작성자
- 시각: 2026-02-27T03:12:40Z
- [게시 원문](https://github.com/woowacourse/gemini-canvas-mission/pull/129#issuecomment-3970479461)

> ## 이번 주 인상 깊었던 순간
>
> 연극 준비를 했던 순간이었습니다. 저는 태어나서 한 번도 사람들 앞에서 연극을 해본적이 없어 솔직히 하기 싫은 마음이 있었습니다. 하지만 연극조 분들과 연극을 준비하면서, 한 번도 마주해보지 못한 것에 도전하여 잘 못하고 부끄러울지라도 우선 부딪혀보아야겠단 생각으로 바뀌었습니다. 하기 싫고 회피하고 싶은 것도 마주치기 위해 노력하면 마음가짐도 바뀔 수 있다는 것을 알게되어, 저는 연극 준비를 했던 순간이 가장 인상 깊었던 순간이었습니다. 마음이 무겁지만, 그래도 해보겠습니다!
>
> ## 다음에 도전하고 싶은 것
>
> 이번 주 온보딩 미션을 하면서 시간 관리를 잘 하지 못했습니다. 첫 날에는 환경에 적응하느라 하지 못했고, 두 번째 날은 과제의 양을 과소평가 하고 느슨하게 하여 오후 시간과 저녁 시간 안에 오늘 목표치를 완료하지 못했습니다. 이렇게 해내거나 못한 일에는 이유(핑계)가 있습니다. 다음 도전은 핑계 없이 완료한 한 주를 보내고 싶습니다.

### 인라인 코멘트 2863937551: yeo-li

- 상대방 발언, PR 작성자
- 시각: 2026-02-27T11:43:56Z
- [게시 원문](https://github.com/woowacourse/gemini-canvas-mission/pull/129#discussion_r2863937551)
- 코드: `smart_note.html`, 현재 줄 1, 원래 줄 1
- 답변 대상: [코멘트 2858693854](https://github.com/woowacourse/gemini-canvas-mission/pull/129#discussion_r2858693854)
- 소속 리뷰 ID: 3866507137

> 피드백 정말 감사합니다!
>
> 저도 확인해보니 동일한 문제가 발생하여 관련 문제를 찾아보았습니다. 그리고 이 문제는 IME 합성 과정에서 발생하는 문제임을 확인했습니다.
>
> 관련 문제를 해결하기 위해 브라우저에서 제공하는 `isComposing` 속성을 이용했습니다. 사용자가 `Enter`를 눌렀을 때 `isComposing`이 `true`라면 아무것도 하지 않고 종료하고, `false`라면 AI에게 명령 프롬프트가 전달되도록 변경했습니다. 관련 로직을 추가하니 한글 입력시에도 입력이 두 번 되는 문제가 해결됨을 확인할 수 있었습니다!
>
> 그리고 두 번째 개선사항도 모두 반영하여 다시 앱을 만들어보았습니다!
>
> > 피드백 반영된 smart note 링크
> > https://gemini.google.com/share/d6a51d64b055
>
> 마지막으로  프롬프트 해킹을 시도하셨다고 해서 깜짝 놀랐습니다ㅋㅋ큐ㅠ 따로 validation이나 sanitisation한 부분은 없었습니다..! 그래서 제가 gemini에게 역으로 질문해보니, 사용자의 입력값을 특정 맥락 안에 포함시키도록 하는 contextual wrapping과 명령어의 응답을 json 형식으로 반환하도록 강제하는 방식을 사용했다고 했습니다!

### 리뷰 본문 3866507137: yeo-li

- 상대방 발언, PR 작성자
- 시각: 2026-02-27T11:43:57Z
- [게시 원문](https://github.com/woowacourse/gemini-canvas-mission/pull/129#pullrequestreview-3866507137)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 2867308902: yeo-li

- 상대방 발언, PR 작성자
- 시각: 2026-02-28T10:00:39Z
- [게시 원문](https://github.com/woowacourse/gemini-canvas-mission/pull/129#discussion_r2867308902)
- 코드: `혼자서도_즐기는_캐치마인드.html`, 현재 줄 1, 원래 줄 1
- 답변 대상: [코멘트 2858733962](https://github.com/woowacourse/gemini-canvas-mission/pull/129#discussion_r2858733962)
- 소속 리뷰 ID: 3870306836

> ㅋㅋㅋㅋ큐ㅠ 감사합니다!

### 리뷰 본문 3870306836: yeo-li

- 상대방 발언, PR 작성자
- 시각: 2026-02-28T10:00:39Z
- [게시 원문](https://github.com/woowacourse/gemini-canvas-mission/pull/129#pullrequestreview-3870306836)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 2867358451: yeo-li

- 상대방 발언, PR 작성자
- 시각: 2026-02-28T10:44:06Z
- [게시 원문](https://github.com/woowacourse/gemini-canvas-mission/pull/129#discussion_r2867358451)
- 코드: `혼자서도_즐기는_캐치마인드.html`, 현재 줄 135, 원래 줄 135
- 답변 대상: [코멘트 2858774613](https://github.com/woowacourse/gemini-canvas-mission/pull/129#discussion_r2858774613)
- 소속 리뷰 ID: 3870362441

> 제안 감사합니다! 심볼에 알파벳과 같은 언어적 요소도 금지하니 확실히 글자가 나오는 빈도가 많이 줄었습니다. 그리고 생성된 그림을 피드백하고 재생성하는 과정을 더해 그림 생성의 안정성을 높여보았습니다. 하지만 이렇게 해도 가끔 글자가 떠서 많이 아쉽긴 한 것 같습니다ㅠㅠ 아래 개선 해본 캐치마인드 링크 첨부하겠습니다!
>
> > 피드백 반영된 캐치마인드 링크
> > https://gemini.google.com/share/72deb08c5d1f

<details>
<summary>당시 코드 문맥</summary>

```diff
@@ -0,0 +1,374 @@
+import React, { useState, useEffect, useCallback, useRef } from 'react';
+import { Palette, Lightbulb, Send, RefreshCw, Trophy, AlertCircle, Loader2, Heart, HeartOff, Brain, HelpCircle } from 'lucide-react';
+
+const apiKey = ""; // 환경 제공 키 사용
+
+const API_TEXT_URL = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=${apiKey}`;
+const API_IMAGE_URL = `https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key=${apiKey}`;
+
+// 카테고리별 단어 풀
+const WORDS_DATABASE = [
+  { word: "비행기", category: "교통수단" }, { word: "피아노", category: "악기" }, { word: "북극곰", category: "동물" },
+  { word: "무지개", category: "자연" }, { word: "자전거", category: "교통수단" }, { word: "여권", category: "여행" },
+  { word: "시간", category: "추상어" }, { word: "우정", category: "추상어" }, { word: "스마트폰", category: "기계" },
+  { word: "도서관", category: "장소" }, { word: "지구", category: "자연" }, { word: "선인장", category: "식물" },
+  { word: "망원경", category: "도구" }, { word: "카메라", category: "도구" }, { word: "돋보기", category: "도구" },
+  { word: "잠수함", category: "교통수단" }, { word: "등대", category: "건물" }, { word: "열기구", category: "교통수단" },
+  { word: "나침반", category: "도구" }, { word: "우주선", category: "교통수단" }, { word: "화산", category: "자연" },
+  { word: "폭포", category: "자연" }, { word: "눈사람", category: "겨울" }, { word: "모래시계", category: "도구" },
+  { word: "편지", category: "통신" }, { word: "향수", category: "미용" }, { word: "보물상자", category: "물건" },
+  { word: "성", category: "건물" }, { word: "열쇠", category: "물건" }, { word: "안경", category: "물건" },
+  { word: "신발", category: "의류" }, { word: "우산", category: "물건" }, { word: "촛불", category: "물건" },
+  { word: "거울", category: "물건" }, { word: "시계", category: "물건" }, { word: "지도", category: "여행" },
+  { word: "기타", category: "악기" }, { word: "드럼", category: "악기" }, { word: "바이올린", category: "악기" },
+  { word: "축구공", category: "스포츠" }, { word: "연필", category: "문구" }, { word: "지갑", category: "물건" },
+  { word: "청소기", category: "가전" }, { word: "냉장고", category: "가전" }, { word: "선풍기", category: "가전" },
+  { word: "에어컨", category: "가전" }, { word: "텔레비전", category: "가전" }, { word: "컴퓨터", category: "가전" },
+  { word: "마우스", category: "가전" }, { word: "키보드", category: "가전" }, { word: "칫솔", category: "위생" },
+  { word: "비누", category: "위생" }, { word: "수건", category: "위생" }, { word: "침대", category: "가구" },
+  { word: "베개", category: "가구" }, { word: "거실", category: "장소" }, { word: "부엌", category: "장소" },
+  { word: "화장실", category: "장소" }, { word: "지하실", category: "장소" }, { word: "계단", category: "구조물" },
+  { word: "사탕", category: "음식" }, { word: "초콜릿", category: "음식" }, { word: "아이스크림", category: "음식" },
+  { word: "햄버거", category: "음식" }, { word: "피자", category: "음식" }, { word: "김밥", category: "음식" },
+  { word: "떡볶이", category: "음식" }, { word: "라면", category: "음식" }, { word: "커피", category: "음식" },
+  { word: "우유", category: "음식" }, { word: "사과", category: "과일" }, { word: "바나나", category: "과일" },
+  { word: "포도", category: "과일" }, { word: "수박", category: "과일" }, { word: "딸기", category: "과일" },
+  { word: "오렌지", category: "과일" }, { word: "복숭아", category: "과일" }, { word: "파인애플", category: "과일" },
+  { word: "망고", category: "과일" }, { word: "키위", category: "과일" }, { word: "호랑이", category: "동물" },
+  { word: "사자", category: "동물" }, { word: "코끼리", category: "동물" }, { word: "기린", category: "동물" },
+  { word: "얼룩말", category: "동물" }, { word: "원숭이", category: "동물" }, { word: "토끼", category: "동물" },
+  { word: "강아지", category: "동물" }, { word: "고양이", category: "동물" }, { word: "햄스터", category: "동물" },
+  { word: "고래", category: "동물" }, { word: "상어", category: "동물" }, { word: "문어", category: "동물" },
+  { word: "오징어", category: "동물" }, { word: "게", category: "동물" }, { word: "조개", category: "동물" },
+  { word: "불가사리", category: "동물" }, { word: "해파리", category: "동물" }, { word: "물고기", category: "동물" },
+  { word: "거북이", category: "동물" }
+];
+
+const App = () => {
+  const [usedWords, setUsedWords] = useState([]);
+  const [currentProblem, setCurrentProblem] = useState(null);
+  const [image, setImage] = useState(null);
+  const [userInput, setUserInput] = useState("");
+  const [gameState, setGameState] = useState('idle'); // idle, loading, playing, won, lost
+  const [visibleHintCount, setVisibleHintCount] = useState(0);
+  const [loadingStep, setLoadingStep] = useState("");
+  const [score, setScore] = useState(0);
+  const [wrongCount, setWrongCount] = useState(0);
+  const [error, setError] = useState(null);
+  const [isShaking, setIsShaking] = useState(false);
+
+  const MAX_ATTEMPTS = 5;
+
+  const fetchWithRetry = async (url, options, retries = 5, backoff = 1000) => {
+    try {
+      const response = await fetch(url, options);
+      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
+      return await response.json();
+    } catch (err) {
+      if (retries > 0) {
+        await new Promise(resolve => setTimeout(resolve, backoff));
+        return fetchWithRetry(url, options, retries - 1, backoff * 2);
+      }
+      throw err;
+    }
+  };
+
+  const startNewGame = useCallback(async () => {
+    setGameState('loading');
+    setError(null);
+    setVisibleHintCount(0);
+    setUserInput("");
+    setImage(null);
+    setWrongCount(0);
+
+    try {
+      let available = WORDS_DATABASE.filter(item => !usedWords.includes(item.word));
+      if (available.length === 0) {
+        available = [...WORDS_DATABASE];
+        setUsedWords([]);
+      }
+      const picked = available[Math.floor(Math.random() * available.length)];
+      setCurrentProblem(picked);
+      setUsedWords(prev => [...prev, picked.word]);
+
+      setLoadingStep(`${picked.category} 분야의 문제를 준비하는 중...`);
+
+      // 힌트 및 리버스(캐치마인드) 전략 수립
+      const brainResponse = await fetchWithRetry(API_TEXT_URL, {
+        method: 'POST',
+        headers: { 'Content-Type': 'application/json' },
+        body: JSON.stringify({
+          contents: [{
+            parts: [{
+              text: `단어: '${picked.word}'. 카테고리: '${picked.category}'.
+              이 단어를 시각적 넌센스(리버스) 캐치마인드 퀴즈로 만들기 위한 2~3개의 상징물 조합을 제안하고, 힌트 3개를 작성해줘.
+
+              [중요 규칙]
+              1. 모든 힌트는 반드시 '한글'로 작성할 것.
+              2. 힌트에서 정답 단어를 직접적으로 묘사하거나 언급하지 말 것.
+              3. 대신 그림 속 상징물들이 무엇을 의미하는지나, 단어의 음절을 비유적으로 표현할 것.
+
+              Respond strictly in JSON format:
+              {
+                "visual_strategy": "Detailed English description of symbols for image generator. NO TEXT.",
+                "hints": ["첫 번째 상징에 대한 비유적 힌트", "두 번째 상징 또는 단어 구성에 대한 은유적 힌트", "정답을 연상시키는 결정적인 넌센스 힌트"]
+              }`
+            }]
+          }],
+          generationConfig: { responseMimeType: "application/json" },
+          systemInstruction: {
+            parts: [{ text: "당신은 기발한 캐치마인드 퀴즈 마스터입니다. 사용자가 머리를 써서 정답을 유추할 수 있도록 은유적이고 기발한 힌트를 제공하세요. 모든 힌트는 한글이어야 합니다." }]
+          }
+        })
+      });
+
+      const data = JSON.parse(brainResponse.candidates[0].content.parts[0].text);
+      setCurrentProblem(prev => ({ ...prev, hints: data.hints }));
+
+      // 이미지 생성
+      setLoadingStep("AI가 캔버스에 캐치마인드 그림을 그리는 중...");
+      const finalImagePrompt = `A 2 or 3 panel rebus puzzle for '${picked.word}'.
+        Visual strategy: ${data.visual_strategy}.
+        Style: Simple child drawing, 10 years old artist, vibrant crayons.
+        Colors: Red, Blue, Yellow, Green, Black only.
+        Background: Clean white paper.
+        CRITICAL: NO LETTERS, NO NUMBERS, NO CHARACTERS. Use only icons and symbols.`;
```

</details>

### 리뷰 본문 3870362441: yeo-li

- 상대방 발언, PR 작성자
- 시각: 2026-02-28T10:44:07Z
- [게시 원문](https://github.com/woowacourse/gemini-canvas-mission/pull/129#pullrequestreview-3870362441)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 2867362426: yeo-li

- 상대방 발언, PR 작성자
- 시각: 2026-02-28T10:49:44Z
- [게시 원문](https://github.com/woowacourse/gemini-canvas-mission/pull/129#discussion_r2867362426)
- 코드: `BFS_시각화_학습_도구_앱.html`, 현재 줄 1, 원래 줄 1
- 답변 대상: [코멘트 2858801188](https://github.com/woowacourse/gemini-canvas-mission/pull/129#discussion_r2858801188)
- 소속 리뷰 ID: 3870365589

> 앗 이런 부분이 있었군요..! 말씀해 주신 부분을 수정하기 위해 탐색 중에 구조 `재설정 버튼`을 비활성화 하여 탐색 중 구조가 변경되는 것을 막았습니다! 피드백 감사합니다:)
>
> > 피드백 반영된 BFS 학습앱 링크
> > https://gemini.google.com/share/cfdb8c740faa

### 리뷰 본문 3870365589: yeo-li

- 상대방 발언, PR 작성자
- 시각: 2026-02-28T10:49:44Z
- [게시 원문](https://github.com/woowacourse/gemini-canvas-mission/pull/129#pullrequestreview-3870365589)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)

### 인라인 코멘트 2867378365: yeo-li

- 상대방 발언, PR 작성자
- 시각: 2026-02-28T11:13:07Z
- [게시 원문](https://github.com/woowacourse/gemini-canvas-mission/pull/129#discussion_r2867378365)
- 코드: `team_convention_master.html`, 현재 줄 1, 원래 줄 1
- 답변 대상: [코멘트 2858834139](https://github.com/woowacourse/gemini-canvas-mission/pull/129#discussion_r2858834139)
- 소속 리뷰 ID: 3870378800

> 말씀해주신 기능도 정말 좋은 기능인 것 같아 바로 추가해보았습니다ㅎㅎ 그리고 markdown 오류도 수정 완료했습니다! 피드백 정말 감사합니다☺️
>
> > 피드백 반영된 TCM 링크
> > https://gemini.google.com/share/f3eb91fb57f2

### 리뷰 본문 3870378800: yeo-li

- 상대방 발언, PR 작성자
- 시각: 2026-02-28T11:13:07Z
- [게시 원문](https://github.com/woowacourse/gemini-canvas-mission/pull/129#pullrequestreview-3870378800)
- 리뷰 상태: `COMMENTED`

(본문 없는 리뷰 상태 기록)
