-- 자바가 들어오는 입구. 여기서는 "무엇을 설치할지"만 선언하고,
-- 실제 서버 기동은 ftplugin/java.lua가 버퍼마다 한다(프로젝트 루트를 그때그때 계산해야 하므로).
return {
	{
		"mfussenegger/nvim-jdtls",
		ft = "java",
	},

	-- 테스트 어댑터를 공통 neotest에 꽂는다. 키맵(<leader>T*)은 이미 공통층에 있다.
	{
		"nvim-neotest/neotest",
		optional = true,
		dependencies = { "rcasia/neotest-java" },
		opts = { adapters = { ["neotest-java"] = {} } },
	},
}
