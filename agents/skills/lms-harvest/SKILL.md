---
name: lms-harvest
description: 우테코 LMS+ 미션의 전체 스텝을 마크다운으로 일괄 수확해 지정 디렉터리에 저장한다. 브라우저의 로그인 세션을 그대로 타며, 본문 데이터는 로컬 수신 서버로 직송해 토큰을 거의 쓰지 않는다.
---

# LMS Harvest — 미션 스텝 일괄 md 수확

LMS+(`techcourse-lms-plus-web.woowahan.com`)의 미션 페이지에서 사이드바 전체 스텝을
순회하며 본문을 마크다운으로 변환해 파일로 저장하는 워크플로.

핵심 설계: **본문 데이터는 모델 컨텍스트를 거치지 않는다.**
페이지 안에서 md로 변환 → 로컬 1회용 수신 서버로 POST → 디스크. 도구 출력에는 스텝별
길이 요약만 흐른다. 20스텝(약 80KB) 기준 실측 토큰 비용은 오케스트레이션 호출 십수 회분이 전부.

## 입력

- 미션 URL 또는 "지금 열린 미션" (예: `/missions/31`)
- 저장 위치 (디렉터리). 미지정 시 사용자에게 확인.

## 절차

1. **브라우저 도구 로드** (한 번의 ToolSearch로):
   `tabs_context_mcp, tabs_create_mcp, navigate, javascript_tool, browser_batch`
2. **탭 준비**: 새 탭 생성 → 미션 URL로 이동. 로그인은 크롬 세션에 이미 있어야 한다
   (없으면 사용자에게 로그인 요청하고 중단. 로그인 대행 금지).
3. **수신 서버 기동** (Bash, `run_in_background: true`):
   `node <이 스킬 디렉터리>/receiver.js <scratchpad>/lms-harvest.json 4199`
   1회 수신 후 자동 종료, 5분 무수신 시 타임아웃.
4. **수확기 주입**: `harvester.js` 파일 내용을 Read로 읽어 `javascript_tool`로 실행
   (SPA 로딩 완료 후. 필요하면 2초 대기 선행).
5. **수확 실행**: `await window.__lmsHarvest.run('http://127.0.0.1:4199/save')`
   반환된 status에서 스텝 수·오류 확인. `error: 'sidebar item not found'`가 있으면
   해당 섹션이 사이드바에서 접혀 있는 것 — 펼친 뒤 재실행.
6. **파일 분할**: `node <이 스킬 디렉터리>/split.js <scratchpad>/lms-harvest.json <저장디렉터리> <오늘날짜>`
   → 섹션별 하위 디렉터리 + 스텝별 md(frontmatter: source/section/step_id/harvested) + README 인덱스.
7. **검증**: 파일 수 = status의 스텝 수인지 확인하고 결과를 보고.

## 선택 후속: 착수 가이드 종합

수확본이 크면 원문을 메인 컨텍스트로 읽지 말고, 섹션별 병렬 서브에이전트(스키마 강제)로
행동·제출물·마감·규칙만 추출한 뒤 종합 가이드 md를 작성한다.

## 주의·한계

- **읽기 전용**: 스텝 클릭(열람)만 한다. 제출·평가·설정 버튼은 절대 누르지 않는다.
- API 직접 호출(`techcourse-lms-plus-api...`)은 403 — 인증 토큰을 꺼내지 않는다(보안 경계).
  DOM/React fiber 경유가 정답.
- 원시 HTML을 도구 출력으로 반출하면 DLP 필터에 걸린다. 반드시 페이지 안에서 md 변환.
- LMS UI 개편 시 `harvester.js`의 `ITEM_SELECTOR`/`GROUP_SELECTOR`/fiber 키 순회가 깨질 수 있다
  — 그 지점만 고치면 된다.
- 수확물은 개인 학습용 사본이다. 외부 공개·재배포하지 않는다.
