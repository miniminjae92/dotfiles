# iOS·iPadOS 적용 기준

## 먼저 확인할 정본

1. 프로젝트 생성 설정과 `IPHONEOS_DEPLOYMENT_TARGET`
2. `TARGETED_DEVICE_FAMILY`, orientation, required capabilities와 entitlement
3. 설치된 Xcode·SDK·Simulator runtime과 Apple의 현재 지원표
4. 앱의 실제 역할별 hardware·background·network 요구

배포 타깃, Xcode가 연결할 수 있는 OS, 설치한 Simulator runtime, Apple이 최신 OS를 제공하는 기기 목록은 서로 다른 계약이다.

## 화면과 접근성

- 고정 픽셀이나 특정 모델 이름으로 layout을 분기하지 않는다. safe area, size class와 실제 container 크기에 반응한다.
- iPhone의 작은 portrait·landscape와 iPad의 full screen·분할/최소 창을 별도 anchor로 둔다.
- Dynamic Type은 작은·기본·큰·최대 접근성 크기에서 확인하고, 핵심 과업이 잘리거나 겹치지 않게 한다.
- VoiceOver label·trait·순서·adjustable action, 44×44pt hit region, 대비와 색 이외 상태 신호를 확인한다.
- 가능하면 `XCUIApplication.performAccessibilityAudit`로 label, hit region, contrast, clipped text와 Dynamic Type을 자동 점검하고 실기기 VoiceOver 과업으로 마무리한다.

## 수명주기·권한·미디어

- 카메라·마이크·로컬 네트워크 권한의 `notDetermined`·허용·거부·제한과 설정 복귀를 분리한다.
- foreground, background, 잠금, interruption, route change, 전화, 다른 앱의 미디어 선점을 검증한다.
- peer 연결, capture freshness, receive/decode freshness와 render freshness를 별도 신호로 본다.
- background mode나 entitlement 존재를 실제 지속 동작 증거로 간주하지 않는다.
- 장시간 카메라·audio·network 기능은 실제 기기의 thermal state, 배터리와 메모리 압박을 측정한다.

## 출시

- Xcode가 지원하는 deployment target과 실제 연결/Simulator 가능 OS를 Apple 표에서 재확인한다.
- Debug 실기기 검증 뒤 동일 시나리오를 Release/TestFlight 빌드에서 반복한다.
- signing, entitlement, privacy manifest, 사용 목적 문구, 수출 규정과 third-party SDK를 archive에서 확인한다.
- iPhone·iPad 앱의 Apple Silicon Mac 및 Vision Pro 호환 제공 여부를 App Store Connect에서 명시적으로 결정한다.
- 공개 지원·개인정보·심사 문구가 현재 구현과 Release 실기기 증거를 넘지 않는지 대조한다.
- 최소 지원 OS 또는 기기를 낮추거나 올리면 새 설치뿐 아니라 기존 데이터 upgrade·복구와 지원 문구를 함께 갱신한다.

### TestFlight 외부 테스트 심사

외부 테스트가 다음 단계라면 사용자에게 제출 여부를 묻기 전에
[`../assets/testflight-external-review-template.md`](../assets/testflight-external-review-template.md)로 초안을 만든다.

- **앱 단위·테스터용:** `Beta App Description`, `Feedback Email`, 초대 화면의 승인된 앱 정보 표시 여부
- **빌드 단위·테스터용:** `What to Test`; 이번 빌드의 검증 목표, 재현 단계, 기대 결과와 피드백 초점을 쓴다.
- **심사자용:** 담당자 이름·이메일·전화번호, 로그인 필요 여부와 데모 계정, Review Notes; 권한, 하드웨어, 위치, 네트워크, 구독·결제 등 심사자가 전체 기능에 접근하는 절차를 쓴다.

기능 설명과 테스트 절차는 코드, 릴리스 노트, 지원 계약과 Release/TestFlight 검증 증거에서 도출한다. 확인되지 않은 연락처나 계정 값은 `사용자 확인 필요`로 남기고 추측하지 않는다. 비밀번호·인증 코드 같은 비밀은 저장소 파일에 쓰지 말고 App Store Connect 직접 입력 항목으로 표시한다. 한국어를 기본으로 하되 실제 테스터 지역과 앱 지원 언어에 필요한 localization만 만든다.

초안 생성과 App Store Connect 반영·심사 제출을 분리한다. 초안은 자동 생성하되, 계정 상태를 바꾸는 반영이나 제출은 사용자가 명시적으로 요청한 뒤에만 수행한다.

## 공식 자료

아래 주소와 모델 목록은 시간에 따라 바뀐다. 작업 시점에 다시 확인하고 확인일을 프로젝트 지원 계약에 기록한다.

- [Xcode SDK 및 시스템 요구사항](https://developer.apple.com/xcode/system-requirements)
- [iOS 16·iPadOS 16 호환 기기](https://support.apple.com/103267)
- [iOS 26 호환 iPhone](https://support.apple.com/guide/iphone/iphone-models-compatible-with-ios-26-iphe3fa5df43/26)
- [iPadOS 26 호환 iPad](https://support.apple.com/guide/ipad/ipad213a25b2/ipados)
- [Apple HIG Layout](https://developer.apple.com/design/human-interface-guidelines/layout)
- [Apple HIG Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)
- [앱 접근성 audit 수행](https://developer.apple.com/documentation/accessibility/performing-accessibility-audits-for-your-app)
- [앱 성능 개선](https://developer.apple.com/documentation/xcode/improving-your-app-s-performance)
- [TestFlight 테스트 정보 제공](https://developer.apple.com/help/app-store-connect/test-a-beta-version/provide-test-information)
- [TestFlight 외부 테스터 초대](https://developer.apple.com/help/app-store-connect/test-a-beta-version/invite-external-testers)
