-- 버퍼의 텍스트를 골라 번역한다. .ideavimrc의 Translation 플러그인 자리를 대신한다.
-- 주 용도는 "읽기": 영문 주석·에러 메시지·라이브러리 문서를 긁어 한글 뜻만 확인하는 것이라
-- 기본을 hover로 둔다. 원문을 건드리지 않고 떠 있는 창에만 번역을 띄운다.
--
-- 엔진은 키가 필요 없는 구글 웹 번역(fallback)이다. 품질이 아쉬워지면 DeepL로 갈아타면 되는데,
-- 그쪽은 무료 플랜도 카드 등록을 요구한다.

-- motion_translate는 expr 키맵이다. 반환한 문자열이 다시 눌린 것처럼 동작해 모션을 기다린다.
-- 그래서 rhs를 함수로 주고 opts에 expr = true가 반드시 있어야 한다.
local function translate(mode)
	return function()
		return require("pantran").motion_translate({ mode = mode })
	end
end

return {
	"potamides/pantran.nvim",
	cmd = "Pantran",
	keys = {
		-- n모드에서는 모션을 받는다: `<leader>trip`(문단), `<leader>tr_`(현재 줄), `3<leader>tr_`(3줄).
		{ "<leader>tr", translate("hover"), mode = { "n", "x" }, expr = true, desc = "번역해서 띄우기" },
		{ "<leader>tR", translate("replace"), mode = { "n", "x" }, expr = true, desc = "번역문으로 바꾸기" },
		{ "<leader>ti", translate("interactive"), mode = { "n", "x" }, expr = true, desc = "번역 창 열기 (고치며)" },
	},
	opts = {
		default_engine = "google",
		engines = {
			google = {
				-- 이 둘이 하나라도 truthy면 pantran은 유료 Cloud Translation API로 붙는다.
				-- GOOGLE_API_KEY는 ~/.gemini.env가 Gemini용으로 이미 export하고 있어서,
				-- 끄지 않으면 엉뚱한 키로 번역 API를 두드리다 인증 실패한다. nil이 아니라 false여야 한다.
				api_key = false,
				bearer_token = false,
				-- 키 없는 웹 엔드포인트 쪽 설정은 이 하위 테이블이 따로 받는다.
				fallback = { default_target = "ko" },
			},
		},
		window = { window_config = { border = "rounded" } },
	},
	config = function(_, opts)
		require("pantran").setup(opts)
	end,
}
