return {
	"dhruvasagar/vim-table-mode",
	cmd = "TableModeToggle",
	init = function()
		-- Markdown 테이블 모드 강제 고정
		vim.g.table_mode_corner = "|"
		vim.g.table_mode_separator = "|"
		vim.g.table_mode_fillchar = "-"

		-- 파일 형식 자동 감지 (Markdown이면 Markdown 테이블 사용)
		vim.g.table_mode_auto_choose_table_mode = 1
		vim.g.table_mode_default_style = "markdown" -- 핵심

		-- gq 정렬 자동 활성화
		vim.g.table_mode_auto_align = 1
	end,
	keys = {
		{ "<leader>tm", ":TableModeToggle<CR>", desc = "Toggle table mode" },
	},
}

-- gqip      (현재 paragraph 정렬)
-- gqq       (한 줄 정렬)
--:TableModeToggle    ← 테이블 모드 켜기/끄기
-- gqip                ← 테이블 전체 정렬
-- <leader>ta          ← 열 추가
-- <leader>td          ← 열 삭제
-- <Leader>tA ← 행 추가
-- <Leader>tD ← 행 삭제
