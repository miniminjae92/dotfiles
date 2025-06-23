MacOS

rm .gitconfig .vimrc .zshrc

rm -rf ~/.config/nvim ~/.local/share/nvim ~/.local/state/nvim

git clone https://github.com/miniminjae92/dotfiles.git .dotfiles

ln -s ~/.dotfiles/.gitconfig ~/.gitconfig;

ln -s ~/.dotfiles/.gitignore ~/.gitignore;

ln -s ~/.dotfiles/.vimrc ~/.vimrc;

ln -s ~/.dotfiles/.zshrc ~/.zshrc;

ln -s ~/.dotfiles/.config/nvim ~/.config/nvim;

ln -s ~/.dotfiles/.tmux.conf ~/.tmux.conf;

ln -sf ~/.dotfiles/.gitignore ~/.gitignore_global

git config --global core.excludesFile ~/.gitignore_global
