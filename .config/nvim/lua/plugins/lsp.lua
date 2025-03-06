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

      dapui.setup({
        controls = {
          enabled = true,
        },
      })

      dap.listeners.after.event_initialized["dapui_config"] = function()
        dapui.open()
      end
      dap.listeners.before.event_terminated["dapui_config"] = function()
        dapui.close()
      end
      dap.listeners.before.event_exited["dapui_config"] = function()
        dapui.close()
      end

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

      keyMapper("<F5>", function()
        local dir = vim.fn.expand("%:h")
        if dir ~= "" then
          vim.cmd("lcd " .. dir)
        end
        local files = vim.fn.glob("*.cpp", false, true)
        if #files == 0 then
          print("🚨 No .cpp files found in " .. dir)
          return
        end
        local compile_cmd = "clang++ -std=c++20 -g " .. table.concat(files, " ") .. " -o a.out 2>&1"
        vim.cmd("cexpr system('" .. compile_cmd .. "')")
        if vim.v.shell_error ~= 0 then
          print("❌ Compilation failed! Check quickfix window.")
          vim.cmd("copen")
          return
        end
        print("✅ Compilation successful! Starting debug...")
        dap.continue()
      end)
      keyMapper("<F9>", dap.run_last)
      keyMapper("<F10>", dap.step_over)
      keyMapper("<F11>", dap.step_into)
      keyMapper("<F12>", dap.step_out)
      keyMapper("<leader>db", dap.toggle_breakpoint)
      keyMapper("<leader>dB", function()
        dap.set_breakpoint(vim.fn.input("Breakpoint condition: "))
      end)
      keyMapper("<leader>dp", function()
        require("dap.ui.widgets").hover()
      end)
      keyMapper("<leader>ds", function()
        require("dap.ui.widgets").centered_float(require("dap.ui.widgets").scopes)
      end)
      keyMapper("<leader>de", dap.terminate)
      keyMapper("<leader>du", dapui.toggle)
    end,
  },
}
