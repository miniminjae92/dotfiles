-- OpenAPI 명세·GitHub Actions·docker-compose를 스키마로 검증한다.
-- 내장 schemaStore는 끄고 SchemaStore 플러그인 목록만 쓴다(같은 스키마를 두 번 받지 않도록).
return {
	settings = {
		yaml = {
			schemaStore = { enable = false, url = "" },
			schemas = require("schemastore").yaml.schemas(),
		},
	},
}
