# 실기기 함정 (실측으로 굳은 것만)

## iOS

- **WDA는 사람이 한 번 허용해야 뜬다.** `devcap wda up`을 돌리면 폰에 "'XCTest' 앱 사용 암호 입력 / Enable UI Automation" 창이 뜨고 60초 안에 눌러야 8100이 열린다. 안 누르면 러너는 살아 있고 포트만 영영 안 열린다. devcap이 로그에서 실패를 감지해 알려 준다. 재시도는 `devcap wda up` 다시.
- **WDA 없이도 되는 것**: 한 장 캡처, 수동 롱스크롤(`m`), 스킴 딥링크(`open yogiyolink://…`, devicectl이 번들을 받아 연다), 앱 목록. 안 되는 것: 자동 스크롤, 탭, 접근성 트리, 번들을 모르는 https 링크 열기.
- **접근성 트리는 느리다**(`pymobiledevice3 accessibility` 2분, WDA `/source` 웹뷰에서 1분). 기본은 OCR이고 `--tree`는 좌표가 꼭 필요할 때만.
- **스와이프는 떼기 전에 멈춘다.** devcap의 W3C 동작에 pause가 들어 있어 이동량이 결정론적이다(폭 6px). 직접 WDA를 부를 일이 있으면 `dragfromtoforduration`은 쓰지 않는다(46~1376px로 널뛴다).
- **세션은 bundleId 없이 만든다.** bundleId를 주면 그 앱이 재시작돼 사람이 옮겨 둔 화면이 날아간다. devcap은 빈 세션을 만들고, 생성 전후 앞 앱의 pid를 비교해 바뀌면 경고한다(재시작됐다는 뜻이니 화면을 다시 만든다).
- **좌표계가 둘이다.** 트리와 터치는 포인트, 스크린샷은 픽셀(iPhone 12 Pro Max는 3배). devcap 바깥은 전부 픽셀이다.
- **딥링크 스킴은 앱이 선언한 값을 쓴다.** `devcap apps --grep <앱>`. 요기요는 `yogiyo://`가 아니라 `yogiyolink://`와 `yogiyoapp://`이고, 같은 스킴이라도 경로마다 열리는 것이 다르다(`push.page/franchise`는 `yogiyolink`만).
- **게이트웨이 페이지는 스토어 폴백 타이머를 쏜다.** Safari 경유 링크에서 확인창을 늦게 누르면 앱스토어가 찍힌다. 앱스토어 화면이 나오면 링크가 죽은 게 아니라 내가 늦은 것부터 의심한다. 이 기기 확인창 오른쪽 버튼은 포인트 (373, 460) = 픽셀 (1119, 1380).
- **폰이 잠기면 전부 죽는다.** 설정 > 디스플레이 > 자동 잠금 '안 함'.
- **WDA 없는 입력 경로는 없다.** `pymobiledevice3 developer core-device universal-hid-service`(HID 터치)와 `core-device screen-capture`는 iOS 26.6에서 "Failed to start service"로 시작 자체가 안 된다(2026-08-21 실측). 시간을 쓰지 않는다.
- `xcodebuild`의 "The device is passcode protected"는 오진일 때가 있다. devcap은 xcodebuild를 안 쓰고 `pymobiledevice3 developer dvt xcuitest`로 러너를 띄운다.

## Android

- **adb가 기기를 못 보면 폰 쪽이다.** 개발자 옵션 > USB 디버깅, USB 모드 파일 전송(MTP), RSA 허용 팝업. `devcap doctor`가 USB에 물린 기기 이름까지 알려 준다.
- **콜드 스타트 모달이 고정 좌표 탭을 깨뜨린다.** 진입은 딥링크(`devcap open`)를 우선하고, 탭이 필요하면 `--tree`로 텍스트를 찾아 그 좌표를 누른다.
- **브라우저에 머문 화면을 앱 화면으로 읽는 사고.** `summary.json`의 `front_app`(현재 액티비티)이 대상 패키지인지 본다.
- **발열.** 연속 수집 시 앱이 죽는다. `devcap temps`로 배터리/최고 온도를 보고 50도 넘으면 쉰다. 화면을 끄지 말고(잠김) 조작만 멈춘다.
- 화면 꺼짐 방지: `devcap awake on`.

## 공통

- 스크롤 바닥은 픽셀로 판정한다(직전 프레임과 같으면 끝). 트리는 화면보다 늦다.
- 겹침 실측이 실패한 프레임은 경고와 함께 겹침 0으로 잇는다. `warnings`가 비어 있지 않으면 `text.txt`에 중복 줄이 있을 수 있다.
