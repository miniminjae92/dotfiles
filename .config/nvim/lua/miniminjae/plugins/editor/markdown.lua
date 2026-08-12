-- 마크다운을 "읽기 좋게" 만드는 네 가지: 버퍼 안 렌더, 브라우저 미리보기, 이미지 붙여넣기, 표 정렬.
local mdview_job
local intentionally_stopped_jobs = {}

local function mdview_is_running()
	if not mdview_job then
		return false
	end

	if vim.fn.jobwait({ mdview_job }, 0)[1] == -1 then
		return true
	end

	mdview_job = nil
	return false
end

local function stop_mdview(options)
	options = options or {}
	if not mdview_is_running() then
		if options.notify ~= false then
			vim.notify("실행 중인 mdview가 없습니다", vim.log.levels.INFO)
		end
		return false
	end

	local job_id = mdview_job
	mdview_job = nil
	intentionally_stopped_jobs[job_id] = true
	vim.fn.jobstop(job_id)

	if options.notify ~= false then
		vim.notify("mdview를 종료했습니다", vim.log.levels.INFO)
	end
	return true
end

local function start_mdview()
	if vim.bo.filetype ~= "markdown" and vim.bo.filetype ~= "mdx" then
		vim.notify("마크다운 버퍼에서만 mdview를 열 수 있습니다", vim.log.levels.WARN)
		return
	end

	local path = vim.api.nvim_buf_get_name(0)
	if path == "" or vim.fn.filereadable(path) == 0 then
		vim.notify("먼저 마크다운 파일을 저장해 주세요", vim.log.levels.WARN)
		return
	end

	local executable = vim.fn.exepath("mdview")
	if executable == "" then
		vim.notify("mdview를 찾을 수 없습니다. install.sh 링크를 확인해 주세요", vim.log.levels.ERROR)
		return
	end

	if mdview_is_running() then
		stop_mdview({ notify = false })
	end

	local stderr = {}
	local job_id = vim.fn.jobstart({ executable, path }, {
		on_stderr = function(_, data)
			for _, line in ipairs(data or {}) do
				if line ~= "" then
					table.insert(stderr, line)
				end
			end
		end,
		on_exit = function(exited_job_id, exit_code)
			local intentionally_stopped = intentionally_stopped_jobs[exited_job_id]
			intentionally_stopped_jobs[exited_job_id] = nil
			if mdview_job == exited_job_id then
				mdview_job = nil
			end

			if not intentionally_stopped and exit_code ~= 0 then
				vim.schedule(function()
					local detail = stderr[#stderr] and (": " .. stderr[#stderr]) or ""
					vim.notify("mdview가 비정상 종료했습니다" .. detail, vim.log.levels.ERROR)
				end)
			end
		end,
	})

	if job_id <= 0 then
		vim.notify("mdview를 시작하지 못했습니다", vim.log.levels.ERROR)
		return
	end

	mdview_job = job_id
	local modified_note = vim.bo.modified and " (저장된 내용 기준, :w 후 자동 갱신)" or ""
	vim.notify("mdview 시작: " .. vim.fn.fnamemodify(path, ":t") .. modified_note, vim.log.levels.INFO)
end

local function toggle_mdview()
	if mdview_is_running() then
		stop_mdview()
	else
		start_mdview()
	end
end

return {
	-- 편집 중인 버퍼에서 헤딩·코드블록·표를 바로 렌더한다
	{
		"MeanderingProgrammer/render-markdown.nvim",
		ft = { "markdown", "mdx" },
		keys = {
			{ "<leader>mp", start_mdview, desc = "mdview 시작" },
			{ "<leader>ms", stop_mdview, desc = "mdview 중지" },
			{ "<leader>mt", toggle_mdview, desc = "mdview 토글" },
		},
		opts = {
			file_types = { "markdown", "mdx" },
			code = { sign = false, width = "block", right_pad = 1 },
			heading = { sign = false, icons = {} },
		},
	},

	-- 클립보드 이미지를 파일로 저장하고 링크까지 써 넣는다
	{
		"HakonHarnes/img-clip.nvim",
		event = "VeryLazy",
		opts = {
			default = {
				dir_path = ".",
				file_name = "%Y-%m-%d-%H-%M-%S",
				use_absolute_path = false,
				relative_to_current_file = true,
			},
		},
		keys = {
			{ "<leader>p", "<cmd>PasteImage<cr>", desc = "클립보드 이미지 붙여넣기" },
		},
	},

	-- 표 칸 맞추기 (gqip로 문단 전체 정렬)
	{
		"dhruvasagar/vim-table-mode",
		cmd = "TableModeToggle",
		init = function()
			vim.g.table_mode_corner = "|"
			vim.g.table_mode_separator = "|"
			vim.g.table_mode_fillchar = "-"
			vim.g.table_mode_auto_choose_table_mode = 1
			vim.g.table_mode_default_style = "markdown"
			vim.g.table_mode_auto_align = 1
		end,
		keys = {
			{ "<leader>tm", "<cmd>TableModeToggle<CR>", desc = "표 모드 토글" },
		},
	},
}
