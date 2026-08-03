-- DB 콘솔. :DBUI로 접속을 고르고 SQL 버퍼에서 바로 질의한다(PostgreSQL 학습용 슬롯).
-- 접속하려면 클라이언트 바이너리가 필요하다: PostgreSQL은 `psql`(brew install libpq).
return {
	"tpope/vim-dadbod",
	dependencies = {
		"kristijanhusak/vim-dadbod-ui",
		"kristijanhusak/vim-dadbod-completion",
	},
	cmd = { "DB", "DBUI", "DBUIToggle", "DBUIAddConnection", "DBUIFindBuffer" },
	init = function()
		vim.g.db_ui_use_nerd_fonts = 1
		vim.g.db_ui_show_database_icon = 1
		-- 접속 정보와 저장한 질의는 설정 저장소가 아니라 데이터 디렉터리에 둔다
		vim.g.db_ui_save_location = vim.fn.stdpath("data") .. "/db_ui"
	end,
}
