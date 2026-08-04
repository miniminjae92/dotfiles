-- 자바 버퍼가 열릴 때마다 실행된다. 이 설정에서 가장 조심스러운 파일.
--
-- 왜 여기 있나: jdtls는 프로젝트마다 워크스페이스가 따로다. 이전 설정은 cwd 기준으로
-- 세션당 한 번만 기동해, 다른 프로젝트 파일을 열면 엉뚱한 워크스페이스에 붙었다.
-- 그래서 버퍼마다 루트를 다시 계산한다. vim.lsp.enable 목록에 jdtls가 없는 이유도 이것.

local ok, jdtls = pcall(require, "jdtls")
if not ok then
	return
end

local mason = vim.fn.stdpath("data") .. "/mason"
local jdtls_bin = mason .. "/bin/jdtls"
if vim.fn.executable(jdtls_bin) == 0 then
	vim.notify("jdtls가 설치돼 있지 않다. :Mason에서 설치할 것.", vim.log.levels.WARN)
	return
end

-- 루트 찾기는 단계적으로 한다. vim.fs.root은 "가장 가까운" 조상을 주기 때문에,
-- 멀티모듈에서 모듈 build.gradle을 먼저 보면 프로젝트가 쪼개진다.
-- 그래서 프로젝트 전체를 뜻하는 표식(settings·래퍼)을 1순위로 둔다.
local root = vim.fs.root(0, { "settings.gradle", "settings.gradle.kts", "gradlew", "mvnw" })
	or vim.fs.root(0, { "pom.xml", "build.gradle", "build.gradle.kts" })
	or vim.fs.root(0, { ".git" })
	-- 빌드 파일이 아예 없는 연습용 단일 파일이면 그 파일이 있는 폴더로 본다
	or vim.fn.expand("%:p:h")

-- 루트 경로를 이름에 그대로 녹여 워크스페이스 충돌을 없앤다(같은 이름의 프로젝트가 여럿이어도 안전).
local workspace = vim.fn.stdpath("cache") .. "/jdtls-workspaces/" .. (root:gsub("[/\\:]", "_"))

local packages = mason .. "/packages"

-- 번들: 디버그 어댑터 + 테스트 러너.
-- java-test의 두 jar는 넣으면 안 된다고 공식 README가 못박고 있다(러너 셰이딩 jar와 커버리지 에이전트).
local bundles =
	vim.fn.glob(packages .. "/java-debug-adapter/extension/server/com.microsoft.java.debug.plugin-*.jar", true, true)
local excluded = {
	["com.microsoft.java.test.runner-jar-with-dependencies.jar"] = true,
	["jacocoagent.jar"] = true,
}
for _, jar in ipairs(vim.fn.glob(packages .. "/java-test/extension/server/*.jar", true, true)) do
	if not excluded[vim.fn.fnamemodify(jar, ":t")] then
		bundles[#bundles + 1] = jar
	end
end

-- 완성 목록에서 클래스를 고르면 import가 자동으로 붙게 하는 스위치.
local extended = vim.deepcopy(jdtls.extendedClientCapabilities)
extended.resolveAdditionalTextEditsSupport = true

-- 셸에 잡힌 JDK를 우선 쓰고, 없을 때만 설치 경로로 떨어진다(JDK를 올릴 때 이 폴백을 같이 고칠 것).
local java_home = vim.env.JAVA_HOME or vim.fn.expand("~/Library/Java/JavaVirtualMachines/temurin-21.0.9/Contents/Home")

local function on_attach(_, bufnr)
	local function map(mode, lhs, rhs, desc)
		vim.keymap.set(mode, lhs, rhs, { buffer = bufnr, desc = desc })
	end

	-- IntelliJ의 Extract 리팩터링 자리
	map("n", "crV", jdtls.extract_variable, "변수로 추출")
	map("n", "crC", jdtls.extract_constant, "상수로 추출")
	map("x", "crM", function()
		jdtls.extract_method(true)
	end, "메서드로 추출")

	map("n", "<leader>co", jdtls.organize_imports, "import 정리")

	-- 자바는 타입 이름이 길어 인레이 힌트 이득이 크다. 기본으로 켜고, 끄는 건 공통 <leader>ch.
	vim.lsp.inlay_hint.enable(true, { bufnr = bufnr })

	-- neotest가 구조를 못 읽는 프로젝트를 위한 jdtls 자체 실행기(폴백)
	map("n", "<leader>TN", jdtls.test_nearest_method, "근처 테스트 실행 (jdtls)")
	map("n", "<leader>TC", jdtls.test_class, "클래스 테스트 실행 (jdtls)")

	-- 서버가 프로젝트를 다 읽은 뒤라야 main 클래스를 찾을 수 있다
	vim.schedule(function()
		pcall(function()
			require("jdtls.dap").setup_dap_main_class_configs()
		end)
	end)

	-- 빌드 없이 파일 하나만 돌려보기 (JEP 330: java Foo.java)
	map("n", "<leader>jr", function()
		require("snacks").terminal.open({ "java", vim.fn.expand("%:p") }, {
			cwd = vim.fn.expand("%:p:h"),
			interactive = true,
		})
	end, "이 파일만 실행 (JEP 330)")

	map("n", "<leader>jb", function()
		if vim.fn.executable(root .. "/gradlew") == 0 then
			vim.notify("gradlew가 없다: " .. root, vim.log.levels.WARN)
			return
		end
		require("snacks").terminal.open({ "./gradlew", "build" }, { cwd = root, interactive = true })
	end, "gradlew build")
end

jdtls.start_or_attach({
	-- mason 래퍼가 OS별 config 폴더와 launcher jar를 알아서 고른다.
	cmd = {
		jdtls_bin,
		"--jvm-arg=-javaagent:" .. packages .. "/jdtls/lombok.jar",
		"-data",
		workspace,
	},
	cmd_env = { JAVA_HOME = java_home },
	root_dir = root,
	-- 이 서버는 vim.lsp.enable를 안 거치므로 '*' 설정이 닿지 않는다. 완성 기능을 직접 알려준다.
	capabilities = require("blink.cmp").get_lsp_capabilities(nil, true),
	on_attach = on_attach,
	settings = {
		java = {
			configuration = {
				runtimes = { { name = "JavaSE-21", path = java_home, default = true } },
			},
			signatureHelp = { enabled = true },
			-- .class만 있는 라이브러리를 열면 디컴파일해 보여준다
			contentProvider = { preferred = "fernflower" },
			eclipse = { downloadSources = true },
			maven = { downloadSources = true },
			references = { includeDecompiledSources = true },
			implementationsCodeLens = { enabled = false },
			referencesCodeLens = { enabled = false },
			completion = {
				-- 테스트에서 자주 쓰는 정적 임포트를 완성 후보 위로 올린다
				favoriteStaticMembers = {
					"org.junit.jupiter.api.Assertions.*",
					"org.junit.jupiter.api.Assumptions.*",
					"org.junit.jupiter.api.DynamicTest.*",
					"org.assertj.core.api.Assertions.*",
					"org.mockito.Mockito.*",
					"org.mockito.ArgumentMatchers.*",
					"java.util.Objects.requireNonNull",
					"java.util.Objects.requireNonNullElse",
				},
				importOrder = { "java", "javax", "com", "org" },
			},
			sources = {
				-- import를 `*`로 접지 않는다. 무엇을 쓰는지 파일만 보고 알 수 있게.
				organizeImports = { starThreshold = 9999, staticStarThreshold = 9999 },
			},
			inlayHints = { parameterNames = { enabled = "all" } },
			-- 포맷은 conform(google-java-format)이 전담한다. 여기서 켜면 저장할 때 규칙이 충돌한다.
			format = { enabled = false },
		},
	},
	init_options = {
		bundles = bundles,
		extendedClientCapabilities = extended,
	},
}, {
	-- 디버그 세션 중 코드를 고치면 다시 띄우지 않고 반영한다
	dap = { hotcodereplace = "auto" },
})
