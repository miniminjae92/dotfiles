MacOS

rm .gitconfig .vimrc .zshrc
rm -rf ~/.config/nvim ~/.local/share/nvim ~/.local/state/nvim
git clone https://github.com/miniminjae92/dotfiles.git .dotfiles
ln -s ~/.dotfiles/.gitconfig ~/.gitconfig
ln -s ~/.dotfiles/.vimrc ~/.vimrc
ln -s ~/.dotfiles/.zshrc ~/.zshrc
ln -s ~/.dotfiles/.config/nvim ~/.config/nvim
