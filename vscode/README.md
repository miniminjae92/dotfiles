📁 dotfiles 예시 디렉터리 구조

~/.dotfiles/vscode/
├── settings.json
├── keybindings.json
└── snippets/

🔗 심볼릭 링크로 연결 (macOS 기준)

'''zsh

ln -sf ~/.dotfiles/vscode/settings.json \
 ~/Library/Application\ Support/Code/User/settings.json

ln -sf ~/.dotfiles/vscode/keybindings.json \
 ~/Library/Application\ Support/Code/User/keybindings.json

ln -sf ~/.dotfiles/vscode/snippets \
 ~/Library/Application\ Support/Code/User/snippets

code --list-extensions > ~/.dotfiles/vscode/extensions.txt

'''
