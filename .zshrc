# ~.zshrc
export ZSH=~/.oh-my-zsh

# disable oh-my-zsh themes for pure prompt
ZSH_THEME=""

source $ZSH/oh-my-zsh.sh
export ZPLUG_HOME=/opt/homebrew/opt/zplug
source $ZPLUG_HOME/init.zsh

zplug "mafredri/zsh-async", from:github
zplug "sindresorhus/pure", use:pure.zsh, from:github, as:theme
zplug "zsh-users/zsh-autosuggestions", as:plugin, defer:2

zplug load
# Install plugins if there are plugins that have not been installed
if ! zplug check --verbose; then
    printf "Install? [y/N]: "
    if read -q; then
        echo; zplug install
    fi
fi

#C++ compile and run
my_cc()
{
	clang++ -std=c++20 -g "$@" && ./a.out
}

alias cc='my_cc'
