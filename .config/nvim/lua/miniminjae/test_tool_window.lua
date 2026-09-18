local M = {}

local function output_panel()
	return require("neotest").output_panel
end

local function output_buffer()
	return output_panel().buffer()
end

local function find_window()
	local bufnr = output_buffer()
	for _, winid in ipairs(vim.api.nvim_list_wins()) do
		if vim.api.nvim_win_is_valid(winid) and vim.api.nvim_win_get_buf(winid) == bufnr then
			return winid
		end
	end
end

local function window_config()
	local horizontal_margin = math.max(2, math.floor(vim.o.columns * 0.04))
	local vertical_margin = math.max(1, math.floor(vim.o.lines * 0.04))
	local width = math.max(1, vim.o.columns - horizontal_margin * 2 - 2)
	local height = math.max(1, vim.o.lines - vertical_margin * 2 - vim.o.cmdheight - 2)

	return {
		relative = "editor",
		row = vertical_margin,
		col = horizontal_margin,
		width = width,
		height = height,
		style = "minimal",
		border = "rounded",
		title = " Test Output ",
		title_pos = "center",
		footer = " <leader>Ty: 결과 복사  <leader>To: 열기/숨기기  q: 숨기기 ",
		footer_pos = "center",
		zindex = 60,
	}
end

local function resolved_highlight(name)
	return vim.api.nvim_get_hl(0, { name = name, link = false })
end

local function configure_highlights()
	local normal = resolved_highlight("Normal")
	local float = resolved_highlight("NormalFloat")
	local border = resolved_highlight("FloatBorder")
	local title = resolved_highlight("FloatTitle")
	local footer = resolved_highlight("Comment")
	local selection = resolved_highlight("CursorLine")

	if vim.g.colors_name == "solarized-osaka" then
		vim.api.nvim_set_hl(0, "MiniminjaeTestOutput", { fg = 0x9EABAC, bg = 0x001419 })
		vim.api.nvim_set_hl(0, "MiniminjaeTestOutputBorder", { fg = 0x576D74, bg = 0x001419 })
		vim.api.nvim_set_hl(0, "MiniminjaeTestOutputTitle", { fg = 0x29A298, bg = 0x001419, bold = true })
		vim.api.nvim_set_hl(0, "MiniminjaeTestOutputFooter", { fg = 0x576D74, bg = 0x001419 })
		vim.api.nvim_set_hl(0, "MiniminjaeTestOutputCursorLine", { bg = 0x063540 })
		vim.api.nvim_set_hl(0, "MiniminjaeTestOutputError", { fg = 0xDB302D, bg = 0x001419, bold = true })
		return
	end

	local background = float.bg or 0x1D2224
	vim.api.nvim_set_hl(0, "MiniminjaeTestOutput", { fg = float.fg or normal.fg, bg = background })
	vim.api.nvim_set_hl(0, "MiniminjaeTestOutputBorder", { fg = border.fg or normal.fg, bg = background })
	vim.api.nvim_set_hl(0, "MiniminjaeTestOutputTitle", { fg = title.fg or normal.fg, bg = background, bold = true })
	vim.api.nvim_set_hl(0, "MiniminjaeTestOutputFooter", { fg = footer.fg or border.fg, bg = background })
	vim.api.nvim_set_hl(0, "MiniminjaeTestOutputCursorLine", { bg = selection.bg or background })
	vim.api.nvim_set_hl(0, "MiniminjaeTestOutputError", { fg = resolved_highlight("DiagnosticError").fg, bg = background, bold = true })
end

function M.hide()
	output_panel().close()
end

function M.copy_all()
	local lines = vim.api.nvim_buf_get_lines(output_buffer(), 0, -1, false)
	while #lines > 0 and lines[1]:match("^%s*$") do
		table.remove(lines, 1)
	end
	while #lines > 0 and lines[#lines]:match("^%s*$") do
		table.remove(lines)
	end

	if #lines == 0 then
		vim.notify("복사할 테스트 결과가 없습니다", vim.log.levels.WARN)
		return
	end

	vim.fn.setreg("+", table.concat(lines, "\n"), "c")
	vim.notify(("테스트 결과 %d줄을 복사했습니다"):format(#lines))
end

local function configure_buffer(bufnr)
	if vim.b[bufnr].miniminjae_test_output_mapped then
		return
	end

	vim.b[bufnr].miniminjae_test_output_mapped = true
	vim.keymap.set("n", "q", M.hide, { buffer = bufnr, silent = true, desc = "테스트 결과 숨기기" })
	vim.keymap.set("n", "<Esc>", M.hide, { buffer = bufnr, silent = true, desc = "테스트 결과 숨기기" })
	vim.keymap.set("n", "<leader>Ty", M.copy_all, { buffer = bufnr, silent = true, desc = "테스트 결과 복사" })
	vim.keymap.set("t", "<Esc>", function()
		vim.schedule(M.hide)
	end, { buffer = bufnr, silent = true, desc = "테스트 결과 숨기기" })
end

function M.create_window()
	configure_highlights()
	local bufnr = output_buffer()
	configure_buffer(bufnr)

	local winid = vim.api.nvim_open_win(bufnr, false, window_config())
	vim.api.nvim_set_option_value("wrap", false, { win = winid })
	vim.api.nvim_set_option_value("cursorline", true, { win = winid })
	vim.api.nvim_set_option_value(
		"winhighlight",
		"Normal:MiniminjaeTestOutput,NormalNC:MiniminjaeTestOutput,FloatBorder:MiniminjaeTestOutputBorder,FloatTitle:MiniminjaeTestOutputTitle,FloatFooter:MiniminjaeTestOutputFooter,CursorLine:MiniminjaeTestOutputCursorLine",
		{ win = winid }
	)
	vim.fn.matchadd("MiniminjaeTestOutputError", [[\v(FAILED|AssertionError)]], 10, -1, { window = winid })
	return winid
end

function M.open(opts)
	opts = opts or {}
	output_panel().open()

	local winid = find_window()
	if not winid then
		return
	end

	vim.api.nvim_win_set_config(winid, window_config())
	if opts.enter then
		vim.api.nvim_set_current_win(winid)
	end
	return winid
end

function M.toggle()
	local winid = find_window()
	if not winid then
		M.open({ enter = true })
	else
		M.hide()
	end
end

function M.run(args)
	output_panel().clear()
	M.open({ enter = true })
	if args == nil then
		require("neotest").run.run()
	else
		require("neotest").run.run(args)
	end
end

function M.setup()
	local namespace = vim.api.nvim_create_namespace("neotest")
	vim.diagnostic.config({ virtual_text = false, virtual_lines = false }, namespace)

	vim.api.nvim_create_autocmd("VimResized", {
		group = vim.api.nvim_create_augroup("miniminjae_test_tool_window", { clear = true }),
		callback = function()
			local winid = find_window()
			if winid then
				vim.api.nvim_win_set_config(winid, window_config())
			end
		end,
	})
end

return M
