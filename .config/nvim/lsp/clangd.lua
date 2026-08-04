-- background-index를 켜야 처음 여는 파일에서도 정의로 점프가 된다.
return {
	cmd = { "clangd", "--background-index" },
	filetypes = { "c", "cpp", "objc", "objcpp", "cuda" },
}
