-- package.json·tsconfig·docker-compose 같은 파일에서 키 이름을 완성하고 오타를 잡는다.
-- 스키마 목록은 SchemaStore(공개 JSON 스키마 모음)에서 통째로 받아온다.
return {
	settings = {
		json = {
			schemas = require("schemastore").json.schemas(),
			validate = { enable = true },
		},
	},
}
