-- 검색 담당. telescope 자리를 대신하며, LSP 결과 목록(gd·gR·gi·gt)도 이 피커로 뜬다.
-- 후보 이동 <C-j>/<C-k>와 <C-q>(선택분을 quickfix로)는 fzf 기본 동작이라 따로 설정하지 않는다.
return {
	"ibhagwan/fzf-lua",
	cmd = "FzfLua",
	opts = {
		-- 파일명을 먼저 보여준다. 경로가 긴 프로젝트에서 무엇을 고르는지 바로 읽힌다.
		files = { formatter = "path.filename_first" },
		grep = { formatter = "path.filename_first" },
	},
	keys = {
		{ "<leader>ff", "<cmd>FzfLua files<cr>", desc = "파일 찾기" },
		{ "<leader>fr", "<cmd>FzfLua oldfiles<cr>", desc = "최근 파일" },
		{ "<leader>fs", "<cmd>FzfLua live_grep<cr>", desc = "프로젝트에서 문자열 찾기" },
		{ "<leader>fc", "<cmd>FzfLua grep_cword<cr>", desc = "커서 아래 단어 찾기" },
		{ "<leader>fb", "<cmd>FzfLua buffers<cr>", desc = "열린 버퍼" },
		{ "<leader>fk", "<cmd>FzfLua keymaps<cr>", desc = "키맵 찾기" },
		{ "<leader>fh", "<cmd>FzfLua helptags<cr>", desc = "도움말 찾기" },
		{ "<leader>fg", "<cmd>FzfLua git_status<cr>", desc = "변경된 파일" },
		{ "<leader>ft", "<cmd>TodoFzfLua<cr>", desc = "TODO/FIXME 찾기" },
	},
}
