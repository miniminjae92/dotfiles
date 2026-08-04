-- 볼트를 nvim에서 직접 편집한다. `[[`로 노트를 잇고, 백링크·데일리노트·템플릿을 그대로 쓴다.
-- 볼트 안 파일을 열 때만 붙는다 — 일반 마크다운까지 이 플러그인이 관여하면 무겁다.
local vault = vim.fn.expand("~") .. "/.obsidian"
local vault_glob = vault .. "/*/**.md"

return {
	"obsidian-nvim/obsidian.nvim",
	version = "*",
	dependencies = { "nvim-lua/plenary.nvim" },
	event = {
		"BufReadPre " .. vault_glob,
		"BufNewFile " .. vault_glob,
	},
	opts = {
		legacy_commands = false,
		-- 활성 워크스페이스는 시작 시 cwd로 정해지고, cwd가 볼트 밖이면 목록 1번이 폴백이다.
		-- 일기·캡처·글쓰기 명령이 향할 곳은 yggdrasil이므로 1번에 둔다.
		workspaces = {
			-- 개인 노트·일기·글감
			{
				name = "yggdrasil",
				path = vault .. "/yggdrasil",
				overrides = {
					notes_subdir = "0-inbox",
					templates = { folder = "_templates" },
					daily_notes = {
						folder = "2-me/dairy/1. 일간",
						date_format = "YYYY-MM-DD",
						template = "일기.md",
						workdays_only = false, -- 일기는 주말에도 쓴다 (기본값 true면 yesterday가 주말을 건너뜀)
					},
					-- 분류체계 규약: 미디어 원본은 _attachments (기본값은 "attachments" 폴더를 새로 만든다)
					attachments = { folder = "_attachments" },
				},
			},
			-- 개발 지식·에이전트 OS 기록
			{
				name = "mimir",
				path = vault .. "/mimir",
				overrides = {
					notes_subdir = "00 Inbox",
					templates = { folder = "_System/Templates" },
				},
			},
		},
		-- 기본값 current_dir는 현재 버퍼 폴더에 노트를 만든다 → "전부 0-inbox로" 원칙이 깨진다.
		new_notes_location = "notes_subdir",
		-- 기본값 zettel_id는 "1754...-ABCD.md" 타임스탬프 파일명을 만든다. 볼트 컨벤션은 한글 제목 그대로.
		note_id_func = function(title)
			if title == nil or title == "" then
				return require("obsidian.builtin").zettel_id()
			end
			return (title:gsub("[/\\]", "-"))
		end,
		-- 저장할 때 id/aliases/tags를 자동 주입·재정렬하지 않는다. 프론트매터는 템플릿이 단일 진실 공급원.
		-- (이걸 끄면 새 노트에 붙던 플러그인 기본 템플릿도 함께 꺼진다 — 인박스 캡처는 빈 파일로 시작)
		frontmatter = { enabled = false },
		completion = { blink = true, min_chars = 2 },
		-- 렌더링은 render-markdown.nvim이 이미 하고 있다. 둘 다 켜면 화면이 겹친다.
		ui = { enable = false },
	},
	config = function(_, opts)
		require("obsidian").setup(opts)
		-- 플러그인은 버퍼를 따라 워크스페이스를 바꿔주지 않는다(수동 :Obsidian workspace뿐).
		-- 그대로 두면 홈에서 nvim을 열고 yggdrasil 일기를 편집해도 today/new/template이 mimir로 간다.
		-- → 편집 중인 파일이 속한 볼트를 활성 워크스페이스로 따라가게 한다.
		vim.api.nvim_create_autocmd("BufEnter", {
			group = vim.api.nvim_create_augroup("obsidian_follow_workspace", { clear = true }),
			pattern = vault_glob,
			callback = function(ev)
				local ws = require("obsidian.api").find_workspace(ev.file)
				if ws and ws.name ~= ".obsidian.wiki" and ws.name ~= Obsidian.workspace.name then
					require("obsidian.workspace").set(ws)
				end
			end,
		})
	end,
	keys = {
		{ "<leader>on", "<cmd>Obsidian new<cr>", desc = "새 노트 (인박스 캡처)" },
		{ "<leader>oN", "<cmd>Obsidian new_from_template<cr>", desc = "템플릿으로 새 노트" },
		{ "<leader>oo", "<cmd>Obsidian quick_switch<cr>", desc = "노트 바로 열기" },
		{ "<leader>os", "<cmd>Obsidian search<cr>", desc = "볼트 전문 검색" },
		{ "<leader>od", "<cmd>Obsidian today<cr>", desc = "오늘 일간 노트" },
		{ "<leader>oy", "<cmd>Obsidian yesterday<cr>", desc = "어제 일간 노트" },
		{ "<leader>ot", "<cmd>Obsidian template<cr>", desc = "템플릿 삽입" },
		{ "<leader>ob", "<cmd>Obsidian backlinks<cr>", desc = "이 노트를 가리키는 곳" },
		{ "<leader>ol", "<cmd>Obsidian links<cr>", desc = "이 노트가 가리키는 곳" },
		{ "<leader>or", "<cmd>Obsidian rename<cr>", desc = "이름 변경 + 링크 갱신" },
		{ "<leader>ow", "<cmd>Obsidian workspace<cr>", desc = "볼트 전환" },
	},
}
