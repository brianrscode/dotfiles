#!/usr/bin/env bash

# Si no es shell interactiva, salir.
[[ $- != *i* ]] && return

### Entorno
export EDITOR="${EDITOR:-nvim}"
export VISUAL="${VISUAL:-nvim}"
export PAGER="${PAGER:-less}"
export HISTCONTROL=ignoreboth:erasedups
export HISTSIZE=10000
export HISTFILESIZE=20000

# Locale: intenta es_MX, con fallback seguro.
export LANG="${LANG:-es_MX.UTF-8}"
export LANGUAGE="${LANGUAGE:-es_MX:es}"
if locale -a 2>/dev/null | grep -qi '^es_MX\.utf8$'; then
    export LC_ALL="es_MX.UTF-8"
elif locale -a 2>/dev/null | grep -qi '^en_US\.utf8$'; then
    export LC_ALL="en_US.UTF-8"
else
    export LC_ALL="C.UTF-8"
fi

### PATH
for dir in "$HOME/.local/bin" "$HOME/.bin" "$HOME/.programas" "$HOME/comandos" "$HOME/.opencode/bin"; do
    [ -d "$dir" ] && PATH="$dir:$PATH"
done
export PATH

### Opciones de shell
shopt -s autocd
shopt -s cdspell
shopt -s cmdhist
shopt -s histappend
bind "set completion-ignore-case on"

### Alias base
alias ls="ls --color=auto"
alias l="ls --color=auto"
alias ll="ls -alFh"
alias la="ls -a"
alias l.="ls -A | grep -E '^\\.'"

alias ..="cd .."
alias ...="cd ../.."
alias cd..="cd .."
alias pdw="pwd"

alias vi="nvim"
alias vim="nvim"
alias pfre="pip freeze > requirements.txt"
alias wget="wget -c"
alias userlist="cut -d: -f1 /etc/passwd | sort"
alias psa="ps auxf"
alias apaga="shutdown now"
alias ssn="sudo shutdown now"
alias sr="reboot"

alias \
    clar="clear" \
    claer="clear" \
    lear="clear" \
    clea="clear" \
    cear="clear" \
    cler="clear" \
    clera="clear" \
    celar="clear" \
    cearl="clear"

### Alias de Git
alias gi="git init"
alias gs="git status"
alias gaa="git add"
alias ga="git add ."
alias gc="git commit"
alias gcm="git commit -m"
alias gr="git remote add origin"
alias gd="git diff"
alias gsw="git switch"
alias gswc="git switch -c"
alias clone="git clone"
alias gt="git log --graph --oneline --decorate --all"

gp() {
    local branch
    branch="$(git branch --show-current 2>/dev/null)"
    if [ -z "$branch" ]; then
        echo "No se detecto una rama actual."
        return 1
    fi
    git push -u origin "$branch"
}

gpu() {
    local branch
    branch="$(git branch --show-current 2>/dev/null)"
    if [ -z "$branch" ]; then
        echo "No se detecto una rama actual."
        return 1
    fi
    git pull --rebase origin "$branch"
}

### Alias de uv
alias uvi="uv init"
alias uva="uv add"
alias uvre="uv remove"
alias uvs="uv sync"
alias uvl="uv lock"
alias uvr="uv run"

### Utilidades
crear_env() {
    if [ -f .env ]; then
        echo ".env ya existe. No se sobreescribe."
        return 0
    fi

    cat > .env <<'EOF'
SECRET_KEY=
DEBUG=True
# ALLOWED_HOSTS=#dominio.com
DATABASE_URL=
NAME_DB=
USER_DB=
PASSWORD_DB=
HOST_DB=
PORT_DB=
# CSRF_TRUSTED_ORIGINS=#https://ejemplo.com
EOF
}

activar() {
    local venv_dir="venv"

    if [ -f "$venv_dir/bin/activate" ]; then
        echo -e "\e[1;34mActivando entorno virtual...\e[0m"
        # shellcheck disable=SC1091
        source "$venv_dir/bin/activate"
        echo -e "\e[1;32mEntorno virtual activado\e[0m"
    elif [ -f "$venv_dir/Scripts/activate" ]; then
        echo -e "\e[1;34mActivando entorno virtual...\e[0m"
        # shellcheck disable=SC1091
        source "$venv_dir/Scripts/activate"
        echo -e "\e[1;32mEntorno virtual activado\e[0m"
    else
        echo -e "\e[1;31mNo se pudo activar el entorno virtual. Ruta desconocida.\e[0m"
        return 1
    fi
}

entorno() {
    local venv_dir="venv"

    if [ "$1" = "-h" ]; then
        echo "-h    Muestra esta ayuda"
        echo "-r    Instala dependencias desde requirements.txt"
        echo "-un   Desinstala dependencias desde requirements.txt"
        echo "-v    Instala dependencias para vision por computadora"
        echo "-d    Instala dependencias para Django y crea proyecto"
        echo "-drf  Instala dependencias para Django REST Framework y crea proyecto"
        return
    fi

    if [ ! -d "$venv_dir" ]; then
        echo -e "\e[1;34mCreando entorno virtual...\e[0m"
        python -m venv "$venv_dir"
        echo -e "\e[1;32mEntorno virtual creado en $venv_dir\e[0m"
    fi

    activar || return 1

    echo -e "\e[1;34mActualizando pip...\e[0m"
    python -m pip install --upgrade pip
    echo -e "\e[1;32mpip actualizado en el entorno virtual\e[0m"

    case "$1" in
        -r)
            echo -e "\e[1;34mInstalando dependencias desde requirements.txt...\e[0m"
            pip install -r requirements.txt
            echo -e "\e[1;32mDependencias instaladas\e[0m"
            ;;
        -un)
            echo -e "\e[1;34mDesinstalando dependencias desde requirements.txt...\e[0m"
            pip uninstall -y -r requirements.txt
            echo -e "\e[1;32mDependencias desinstaladas\e[0m"
            ;;
        -v)
            echo -e "\e[1;34mInstalando dependencias para vision por computadora...\e[0m"
            pip install opencv-contrib-python
            pfre
            echo -e "\e[1;32mDependencias instaladas y requirements.txt generado\e[0m"
            ;;
        -d)
            local project_name="${2:-core}"
            echo -e "\e[1;34mInstalando dependencias para Django...\e[0m"
            pip install django
            pfre
            echo -e "\e[1;34mCreando proyecto...\e[0m"
            django-admin startproject "$project_name" .
            echo "LOGIN_REDIRECT_URL = '/'" >> "$project_name/settings.py"
            echo "LOGOUT_REDIRECT_URL = '/'" >> "$project_name/settings.py"
            crear_env
            echo -e "\e[1;32mProyecto creado -> $project_name\e[0m"
            ;;
        -drf)
            local project_name="${2:-core}"
            echo -e "\e[1;34mInstalando dependencias para Django REST Framework...\e[0m"
            pip install django djangorestframework
            pfre
            django-admin startproject "$project_name" .
            crear_env
            echo -e "\e[1;32mProyecto creado -> $project_name\e[0m"
            ;;
    esac
}

run() {
    if [ ! -f manage.py ]; then
        echo -e "\e[1;31mNo se encontro manage.py en el directorio actual.\e[0m"
        return 1
    fi

    if [ -z "$1" ]; then
        echo -e "\e[1;34mEjecutando el servidor de desarrollo de Django...\e[0m"
        python manage.py runserver
    else
        echo -e "\e[1;34mEjecutando el servidor de desarrollo de Django en '$1'...\e[0m"
        python manage.py runserver "$1"
    fi
}

ex() {
    if [ -z "$1" ] || [ ! -f "$1" ]; then
        echo "'$1' no es un archivo valido"
        return 1
    fi

    case "$1" in
        *.rar) unrar x "$1" ;;
        *.gz) gunzip "$1" ;;
        *.tar) tar xf "$1" ;;
        *.tbz2) tar xjf "$1" ;;
        *.tgz) tar xzf "$1" ;;
        *.zip) unzip "$1" ;;
        *.Z) uncompress "$1" ;;
        *.7z) 7z x "$1" ;;
        *.tar.xz) tar xf "$1" ;;
        *.tar.zst) tar xf "$1" ;;
        *)
            echo "'$1' no se puede extraer via ex()"
            return 1
            ;;
    esac
}

### Integraciones opcionales
if command -v starship >/dev/null 2>&1; then
    eval "$(starship init bash)"
fi

if command -v zoxide >/dev/null 2>&1; then
    eval "$(zoxide init bash)"
fi

if command -v uv >/dev/null 2>&1; then
    eval "$(uv generate-shell-completion bash)"
fi

alias bh="$EDITOR ~/.bashrc"
alias vf="$EDITOR ~/.config/fish/config.fish"
alias vz="$EDITOR ~/.zshrc"

# Carga aliases/funciones locales que no quieras versionar.
[[ -f ~/.bashrc-personal ]] && . ~/.bashrc-personal
