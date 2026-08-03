-- core 층 로드 순서: 옵션 → 키맵 → 자동명령. 셋 다 플러그인에 의존하지 않는다.
require("miniminjae.core.options")
require("miniminjae.core.keymaps")
require("miniminjae.core.autocmds")
