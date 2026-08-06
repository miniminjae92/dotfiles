---
name: mobile-engineering
description: Apply senior mobile engineering gates to non-trivial iOS, iPadOS, or Android planning, implementation, debugging, QA, and release work. Use when a change touches mobile UI, device or OS support, permissions, sensors, camera or audio, networking, app lifecycle, background execution, storage, performance, accessibility, signing, TestFlight or store delivery; define a support contract and verify simulator, physical-device, and Release-build evidence before claiming support.
---

# Mobile Engineering

모바일을 작은 데스크톱 앱으로 취급하지 않는다. 코드가 맞는지뿐 아니라 OS, 기기, 권한, 수명주기, 실제 환경, 배포 빌드의 조합에서 사용자가 과업을 끝낼 수 있는지를 검증한다.

## 1. 지원 계약부터 확인

코드를 바꾸기 전에 저장소에서 지원 계약을 찾는다. 없으면
[`references/support-contract-template.md`](references/support-contract-template.md)를 프로젝트 문서 체계에 맞춰 만든다.

다음을 서로 다른 값으로 기록한다.

- **설치 가능 범위:** 배포 타깃과 스토어 설정상 설치되는 OS, 기기
- **지원 범위:** 제품이 정상 동작을 약속하는 OS, 기기, 모드
- **검증 범위:** 이번 릴리스에서 실제 증거를 확보한 조합

최소 OS만으로 최소 기종을 대신하지 않는다. 화면이 가장 작은 기기, 성능, 메모리 기준 기기, 최신 OS 기기와 특수 capability 기기는 서로 다를 수 있다. 검증할 수 없는 설치 가능 범위를 지원 완료로 쓰지 않는다.

## 2. 변경의 모바일 위험을 분류

각 변경에서 해당하는 축만 고르고, 축마다 실패 상태, 관찰 신호, 복구, 검증 층을 정한다.

- **OS, 기기:** 최소/최신 OS, CPU, 메모리, thermal state, 저장 공간, 센서, codec, radio capability
- **화면, 입력:** 최소/최대 창, 회전, safe area, 키보드, Dynamic Type, VoiceOver, 색 이외 신호, locale
- **권한, 개인정보:** 미결정, 허용, 거부, 제한, 설정 변경 뒤 복귀, 수집, 로그, 백업 경계
- **수명주기:** cold/warm launch, foreground/background, 잠금, 종료, process eviction, 복원
- **하드웨어, 미디어:** 카메라, 마이크, Bluetooth, 오디오 route, interruption, 통화, 다른 앱과의 자원 경합
- **네트워크:** offline, 느림, 손실, Wi-Fi↔cellular 전환, captive/guest/AP-isolated 망, 재연결, 중복, 순서 역전
- **성능, 전력:** 시작 시간, main-thread stall, 메모리 압박, 장시간 발열, 배터리, 저전력 모드
- **저장, 업데이트:** 빈 공간, 파일 보호, schema migration, 이전 버전 upgrade, 삭제, 재설치, 복원
- **배포:** Debug/Release 차이, signing, entitlement, privacy manifest, 난독화, 최적화, TestFlight/store 설치, 태블릿 앱의 Mac, Vision Pro 제공 여부

위험이 카메라, 마이크, 백그라운드, radio, thermal, 스토어 정책처럼 플랫폼이 소유한 동작이면, UI나 추상화보다 작은 실기기 spike를 먼저 실행한다.

## 3. 최소 기기 매트릭스를 고른다

모델을 많이 나열하지 말고 위험을 대표하는 anchor를 고른다. 한 기기가 여러 축을 덮어도 된다.

1. **floor-performance:** 지원 범위에서 가장 느리거나 메모리가 적은 기기
2. **small-layout:** 지원 범위에서 실제 사용 창이 가장 작은 기기
3. **large/adaptive:** 가장 큰 화면과 태블릿의 최소, 분할, 최대 창
4. **current:** 최신 OS, SDK, 대표 최신 하드웨어
5. **capability:** 카메라, NFC, BLE, PiP처럼 기능 분기가 생기는 경계 기기

기기가 없으면 조용히 생략하지 않는다. 테스트 기기 확보, TestFlight 사용자 모집, 기기 팜, 지원 범위 축소 중 하나를 선택하고 담당자와 시점을 남긴다.

## 4. 검증 층을 분리

- **순수 테스트:** 상태 머신, 정책, codec, migration, timeout, retry, 범위 제한
- **플랫폼 통합:** permission mapping, lifecycle orchestration, 저장소, 네트워크, 미디어 adapter
- **UI 자동화:** 핵심 과업, 빈/오류/복구 상태, 접근성 audit, 최소 창, 최대 글자 크기
- **Simulator/Emulator:** OS, 화면 조합, 회전, locale, appearance, 제한된 환경 주입
- **실기기:** 센서, 카메라, 마이크, radio, 백그라운드, interruption, 발열, 배터리, 실제 성능
- **Release/TestFlight:** 최적화, 서명, entitlement가 적용된 실제 설치본과 upgrade 경로

Simulator 성공을 실기기 성공으로, Debug 성공을 Release 성공으로, 연결 성공을 데이터 freshness 성공으로 바꾸어 말하지 않는다.

## 5. 작업 게이트

### 설계 전

- 지원 계약과 변경 위험 축을 식별한다.
- 사용자에게 보일 실패, 제한, 복구를 먼저 정한다.
- 플랫폼 불확실성은 공식 문서와 최소 spike로 줄인다.

### 구현 중

- 상태와 실패를 관찰 가능하게 만들되 개인정보, 미디어, 비밀을 로그에 남기지 않는다.
- 플랫폼 경계 밖 순수 정책을 행위 테스트로 고정한다.
- 지원하지 않는 capability에는 숨은 실패 대신 명시적 fallback을 둔다.

### 완료 전

- 변경 위험에 해당하는 최소 자동 검증과 기기 anchor를 통과한다.
- OS, 모델, 앱 버전/빌드, 환경, 시간, 결과를 증거에 남긴다.
- 실행하지 않은 조합은 `unverified`, 실패는 `failed`, 의도적 비지원은 `unsupported`로 구분한다.
- 지원 범위나 중요한 tradeoff가 바뀌면 프로젝트 결정 정본을 갱신한다.
- 지원, 개인정보, 스토어 문구가 실제 구현과 검증 범위를 넘지 않는지 대조한다.
- iOS, iPadOS 작업의 다음 단계가 TestFlight 외부 테스트이면, 제출 여부를 묻기 전에 [`assets/testflight-external-review-template.md`](assets/testflight-external-review-template.md)로 심사 초안을 만든다. 확인되지 않은 계정 정보는 표시만 하고 추측하지 않는다.
- 현재 작업 정본에 마지막 검증과 다음 한 단계를 갱신한다.

## 6. 플랫폼별 적용

- iOS, iPadOS 작업은 [`references/ios-ipados.md`](references/ios-ipados.md)를 읽고 현재 Xcode, SDK, Apple 지원표를 다시 확인한다.
- Android 작업은 Gradle 설정, `minSdk`·`targetSdk`, ABI, 폼팩터와 Play 정책을 공식 Android 문서에서 현재 값으로 확인한다. Android 프로젝트가 생기기 전에는 특정 API 수준이나 제조사 매트릭스를 전역 기본값으로 고정하지 않는다.

공식 문서는 가능성을 설명한다. 프로젝트의 지원 약속은 제품 맥락, 실제 사용자 기기와 검증 비용을 함께 보고 결정한다.
