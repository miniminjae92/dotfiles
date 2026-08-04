-- 내장 옵션만 다룬다. 플러그인이 없어도 편집이 되는 최소 조건.

-- 파일 탐색은 oil(`-`)과 snacks.explorer가 전담하므로 netrw는 끈다.
vim.g.loaded_netrw = 1
vim.g.loaded_netrwPlugin = 1

local opt = vim.opt

-- 줄 번호: 상대 + 커서줄만 절대
opt.relativenumber = true
opt.number = true

-- 탭·들여쓰기 (prettier 기본값에 맞춘 2칸)
opt.tabstop = 2
opt.shiftwidth = 2
opt.expandtab = true
opt.autoindent = true

-- 줄바꿈: 단어 단위로 접고 접힌 줄임을 표시
opt.wrap = true
opt.linebreak = true
opt.showbreak = "↪ "

-- 검색: 소문자만 쓰면 대소문자 무시, 대문자를 섞으면 구분
opt.ignorecase = true
opt.smartcase = true

opt.cursorline = true
opt.cmdheight = 1

-- 트루컬러 터미널 전제(Ghostty). 사인 칸을 항상 띄워 진단 표시 때 본문이 밀리지 않게 한다.
opt.termguicolors = true
opt.background = "dark"
opt.signcolumn = "yes"

opt.backspace = "indent,eol,start"

-- 시스템 클립보드 공용
opt.clipboard:append("unnamedplus")

-- 분할은 오른쪽·아래로 (읽는 방향과 일치)
opt.splitright = true
opt.splitbelow = true

opt.swapfile = false
opt.encoding = "UTF-8"
opt.scrolloff = 10

-- 키 연속 입력 대기시간. `jk` 탈출과 which-key 팝업이 뜨는 시점을 함께 좌우한다.
opt.timeout = true
opt.timeoutlen = 500

-- mdx는 nvim이 모르는 확장자라 직접 등록하고, 하이라이팅은 markdown 파서를 빌려 쓴다.
vim.filetype.add({
	extension = {
		mdx = "mdx",
	},
})
vim.treesitter.language.register("markdown", "mdx")
