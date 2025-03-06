local keyMapper = require("utils.keyMapper").mapKey

return {
  {
    "williamboman/mason.nvim",
    config = function()
      require("mason").setup()
    end,
  },
  {
    "williamboman/mason-lspconfig.nvim",
    config = function()
      require("mason-lspconfig").setup({
        ensure_installed = { "lua_ls", "clangd" },
      })
    end,
  },
  {
    "neovim/nvim-lspconfig",
    config = function()
      local lspconfig = require("lspconfig")
      lspconfig.lua_ls.setup({})
      lspconfig.clangd.setup({})

      -- LSP 관련 키맵
      keyMapper("K", vim.lsp.buf.hover)
      keyMapper("gd", vim.lsp.buf.definition)
      keyMapper("<leader>ca", vim.lsp.buf.code_action)
    end,
  },
  {
    "mfussenegger/nvim-dap",
    dependencies = { "rcarriga/nvim-dap-ui", "nvim-neotest/nvim-nio" },
    config = function()
      local dap = require("dap")
      local dapui = require("dapui")

      -- 🔹 dap-ui 설정 추가
      dapui.setup({
        controls = { -- 🔹 오류 방지를 위해 controls 명시적 활성화
          enabled = true,
        },
      })
      -- dap-ui 자동 실행 설정
      dap.listeners.after.event_initialized["dapui_config"] = function()
        dapui.open()
      end
      dap.listeners.before.event_terminated["dapui_config"] = function()
        dapui.close()
      end
      dap.listeners.before.event_exited["dapui_config"] = function()
        dapui.close()
      end

      -- C, C++ 디버깅을 위한 codelldb 설정
      dap.adapters.codelldb = {
        type = "executable",
        command = vim.fn.stdpath("data") .. "/mason/bin/codelldb",
      }

      dap.configurations.cpp = {
        {
          type = "codelldb",
          request = "launch",
          program = function()
            return vim.fn.input("Path to executable: ", vim.fn.getcwd() .. "/", "file")
          end,
          cwd = "${workspaceFolder}",
          stopOnEntry = false,
          args = {},
        },
      }
      dap.configurations.c = dap.configurations.cpp

      -- 🔹 디버깅 키맵
      keyMapper("<F5>", dap.continue) -- 실행 (Continue)
      keyMapper("<F9>", dap.run_last) -- 마지막 실행
      keyMapper("<F10>", dap.step_over) -- 현재 함수 건너뛰기 (Step Over)
      keyMapper("<F11>", dap.step_into) -- 현재 함수 내부로 이동 (Step Into)
      keyMapper("<F12>", dap.step_out) -- 현재 함수 빠져나오기 (Step Out)

      -- 🔹 브레이크포인트 관련
      keyMapper("<leader>db", dap.toggle_breakpoint) -- b (Toggle Breakpoint)
      keyMapper("<leader>dB", function()
        dap.set_breakpoint(vim.fn.input("Breakpoint condition: "))
      end)

      -- 🔹 변수 값 확인 (p, display 역할)
      keyMapper("<leader>dp", function()
        require("dap.ui.widgets").hover()
      end)

      -- 🔹 실시간 변수 감시 (Scopes 창)
      keyMapper("<leader>ds", function()
        require("dap.ui.widgets").centered_float(require("dap.ui.widgets").scopes)
      end)

      -- 디버깅 종료
      keyMapper("<leader>de", dap.terminate)

      -- UI 토글
      keyMapper("<leader>du", dapui.toggle)

      -- 🔹 C++ 컴파일 & 실행 (터미널 출력)
      keyMapper("<leader>cc", function()
        local base_dir = vim.fn.getcwd()
        local target_dir = vim.fn.input("Enter directory: ", base_dir .. "/", "dir")
        if target_dir == "" then
          print("🚨 No directory specified!")
          return
        end
        local files = vim.fn.glob(target_dir .. "/*.cpp", false, true)
        if #files == 0 then
          print("🚨 No .cpp files found in " .. target_dir)
          return
        end
        local compile_cmd = "clang++ -std=c++20 -g " .. table.concat(files, " ") .. " -o a.out 2>&1"

        -- Quickfix 창에 컴파일 로그 출력
        vim.cmd("cexpr system('" .. compile_cmd .. "')")

        if vim.v.shell_error ~= 0 then
          print("❌ Compilation failed! Check quickfix window.")
          vim.cmd("copen") -- Quickfix 창 열기
          return
        end
        print("✅ Compilation successful! Running...")
        vim.cmd("belowright 10split | terminal ./a.out")
      end)
    end,
  },
}
