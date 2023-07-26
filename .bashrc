### EXPORT ###
# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_ Muy bueno -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
export EDITOR='code'  # Editor de código predeterminado
export VISUAL='nano'  # Editor de texto predeterminado
export HISTCONTROL=ignoreboth:erasedups # Controla el historial de comandos de bash. Los comandos duplicados no se guardaran en el historial ni los que comienzan con un espacio en blanco
export PAGER='most'

# Prompt
PS1='[\[\e[96m\]\u\[\e[0m\]@\h \w \[\e[96;1m\]$(git branch 2>/dev/null | colrm 1 2)\[\e[0m\]]\$ '

# Si el shell no se ejecuta de forma interactiva, no hace nada
[[ $- != *i* ]] && return

# Verifica que los directorios existan, de ser cierto, los agrega al inicio de la variable entorno PATH
# Esto permite que los ejecutables ubicados en esos directorios sean encontrados y ejecutados desde
# cualquier ubicación del sistema
if [ -d "$HOME/.bin" ] ;
  then PATH="$HOME/.bin:$PATH"
fi

if [ -d "$HOME/.local/bin" ] ;
  then PATH="$HOME/.local/bin:$PATH"
fi

# ignorar mayúsculas y minúsculas al completar un comando de shell bashh
bind "set completion-ignore-case on"

### ALIAS ###
#list
alias ls='ls --color=auto'
alias la='ls -a'
alias ll='ls -alFh'
alias l='ls'
alias l.="ls -A | grep -E '^\.'" # busca los archivos ocultos
alias listdir="ls -d */ > list"

#pacman -> Remplazar por gestor correspondiente
alias sps='sudo pacman -S'
alias spr='sudo pacman -R'
alias sprs='sudo pacman -Rs'
alias sprdd='sudo pacman -Rdd'
alias spqo='sudo pacman -Qo'
alias spsii='sudo pacman -Sii'
# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_ Hasta aquí -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

# muestra la lista de paquetes que necesitan este paquete - depende de mpv como ejemplo
function_depends()  {
    search=$(echo "$1")
    sudo pacman -Sii $search | grep "Required" | sed -e "s/Required By     : //g" | sed -e "s/  /\n/g"
  }

alias depends='function_depends'

# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_ Muy bueno -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
#corregir errores tipográficos obvios
alias cd..='cd ..'
alias pdw='pwd'
alias udpate='sudo pacman -Syyu'
alias upate='sudo pacman -Syyu'
alias updte='sudo pacman -Syyu'
alias updqte='sudo pacman -Syyu'
alias upqll='paru -Syu --noconfirm'
alias upal='paru -Syu --noconfirm'

# Coloree la salida del comando grep para facilitar su uso (bueno para archivos de registro)
alias grep='grep --color=auto'
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'

# Alias ​​para la gestión de software
alias update='sudo pacman -Syyu'
alias upd='sudo pacman -Syyu'
# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_ Hasta aquí -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
# continuar descarga
alias wget="wget -c"

# lista de usuarios
alias userlist="cut -d: -f1 /etc/passwd | sort"
# ps
alias psa="ps auxf"
# grub update
alias update-grub="sudo grub-mkconfig -o /boot/grub/grub.cfg"
alias grub-update="sudo grub-mkconfig -o /boot/grub/grub.cfg"

# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_ Muy bueno -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
# add new fonts trabajar esto para cada que agrego fuentes nuevas y ocupo fc-cache como newFonts ->
alias nfont='sudo fc-cache -fv'

# cambiar entre bash y zsh
alias tobash="sudo chsh $USER -s /bin/bash && echo 'Now log out.'"
alias tozsh="sudo chsh $USER -s /bin/zsh && echo 'Now log out.'"
alias tofish="sudo chsh $USER -s /bin/fish && echo 'Now log out.'"

# kill commands
# quickly kill conkies
alias kc='killall conky'
# quickly kill polybar
alias kp='killall polybar'
# quickly kill picom
alias kpi='killall picom'

#hardware info --short
alias hw="hwinfo --short"
# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_ Hasta aquí -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

# control de audio pulseaudio o pipewire
alias audio="pactl info | grep 'Server Name'"

# comprobar vulnerabilidades microcódigo
alias microcode='grep . /sys/devices/system/cpu/vulnerabilities/*'

# verifique la cpu
alias cpu="cpuid -i | grep uarch | head -n 1"

# obtenga los espejos más rápidos en su vecindario
alias mirror="sudo reflector -f 30 -l 30 --number 10 --verbose --save /etc/pacman.d/mirrorlist"
alias mirrord="sudo reflector --latest 30 --number 10 --sort delay --save /etc/pacman.d/mirrorlist"
alias mirrors="sudo reflector --latest 30 --number 10 --sort score --save /etc/pacman.d/mirrorlist"
alias mirrora="sudo reflector --latest 30 --number 10 --sort age --save /etc/pacman.d/mirrorlist"
# nuestro experimental - la mejor opción por el momento
alias mirrorx="sudo reflector --age 6 --latest 20  --fastest 20 --threads 5 --sort rate --protocol https --save /etc/pacman.d/mirrorlist"
alias mirrorxx="sudo reflector --age 6 --latest 20  --fastest 20 --threads 20 --sort rate --protocol https --save /etc/pacman.d/mirrorlist"
alias ram='rate-mirrors --allow-root --disable-comments arch | sudo tee /etc/pacman.d/mirrorlist'
alias rams='rate-mirrors --allow-root --disable-comments --protocol https arch  | sudo tee /etc/pacman.d/mirrorlist'

# montando la carpeta Public para intercambio entre anfitrión e invitado en virtualbox
alias vbm="sudo /usr/local/bin/arcolinux-vbox-share"

# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_ Muy bueno -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
#shopt
shopt -s autocd # permite ingresar a directorios sin usar cd
shopt -s cdspell # corrige errores tipográficos en los nombres de directorios al usar cd
shopt -s cmdhist # habilita la característica de historial de comandos mejorada
shopt -s dotglob # el patrón * en nombres de archivos coincidrá también con archivos ocultos
shopt -s histappend # asegura que el historias de commandos se añada aun archivo existente en vez de sobreescribir
shopt -s expand_aliases # permite la expación de alias en la línea de comando-------------------------
# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_ Hasta aquí -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
# descarga de youtube
alias yta-aac="yt-dlp --extract-audio --audio-format aac "
alias yta-best="yt-dlp --extract-audio --audio-format best "
alias yta-flac="yt-dlp --extract-audio --audio-format flac "
alias yta-mp3="yt-dlp --extract-audio --audio-format mp3 "
alias ytv-best="yt-dlp -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio' --merge-output-format mp4 "

# Paquetes instalados recientemente
alias rip="expac --timefmt='%Y-%m-%d %T' '%l\t%n %v' | sort | tail -200 | nl"
alias riplong="expac --timefmt='%Y-%m-%d %T' '%l\t%n %v' | sort | tail -3000 | nl"

# iso y versión utilizada para instalar ArcoLinux
alias iso="cat /etc/dev-rel | awk -F '=' '/ISO/ {print $2}'"
alias isoo="cat /etc/dev-rel"
#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_ Muy bueno -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
# vscode para archivos de configuración importantes
alias vf="$EDITOR ~/.config/fish/config.fish"
alias vz="$EDITOR ~/.zshrc"
alias bh="$EDITOR ~/.bashrc"
#alias nneofetch="$EDITOR ~/.config/neofetch/config.conf"

#shutdown or reboot
alias ssn="sudo shutdown now"
alias sr="reboot"

# actualizar mejores imágenes de pantalla de bloqueo
alias bls="betterlockscreen -u /usr/share/backgrounds/arcolinux/"

# proporcione la lista de todos los escritorios instalados - escritorios xsessions
alias xd="ls /usr/share/xsessions"
alias xdw="ls /usr/share/wayland-sessions"

# # ex = Extractor para todo tipo de archivos.
# # uso: ex <archivo>
ex ()
{
  if [ -f $1 ] ; then
    case $1 in
      *.tar.bz2)   tar xjf $1   ;;
      *.tar.gz)    tar xzf $1   ;;
      *.bz2)       bunzip2 $1   ;;
      *.rar)       unrar x $1   ;;
      *.gz)        gunzip $1    ;;
      *.tar)       tar xf $1    ;;
      *.tbz2)      tar xjf $1   ;;
      *.tgz)       tar xzf $1   ;;
      *.zip)       unzip $1     ;;
      *.Z)         uncompress $1;;
      *.7z)        7z x $1      ;;
      *.deb)       ar x $1      ;;
      *.tar.xz)    tar xf $1    ;;
      *.tar.zst)   tar xf $1    ;;
      *)           echo "'$1' no se puede extraer via ex()" ;;
    esac
  else
    echo "'$1' no es un archivo valido"
  fi
}

co ()
{
  elemento=$1
  tipo_compresion=$2
  archivo=""
  # echo $elemento
  if [[ $elemento ]]; then
      archivo="$(echo "$elemento" | cut -d'.' -f1 | cut -d'/' -f1)"
  fi


  case $tipo_compresion in
      zip) zip -r "${archivo:-$elemento}.zip" "$elemento"    ;;
      rar) rar a "${archivo:-$elemento}.rar" "$elemento"    ;;
      tar)       tar cf $elemento.tar $elemento    ;;
      bz2)       bzip2 -k $elemento   ;;
      gz)        gzip -k $elemento    ;;
      Z)         compress -k $elemento;;
      7z)        7z a $elemento.7z $elemento      ;;
      deb)       ar r $elemento.deb $elemento      ;;
      tar.bz2 | tbz2)   tar cjf $elemento.tar.bz2 $elemento   ;;
      tar.gz | tgz)    tar czf $elemento.tar.gz $elemento   ;;
      tar.xz | tar.zst)    tar cJf $elemento.tar.xz $elemento    ;;
      *)         echo "Tipo de compresión no válido" ;;
  esac

  if [ ! $elemento ] ; then
      echo "'$archivo' no es un archivo válido"
  fi
}

# vim
alias vi="nvim"

#git
alias gs="git status"
alias ga="git add ."
alias gc="git commit"
alias gr="git remote add origin"
alias gp="git push origin main"
alias clone="git clone"
alias rmgitcache="rm -r ~/.cache/git"
alias grh="git reset --hard"

#create a file called .bashrc-personal and put all your personal aliases
#in there. They will not be overwritten by skel.

[[ -f ~/.bashrc-personal ]] && . ~/.bashrc-personal

# neofetch

#####################################
#     COMANDOS PERSONALIZADOS       #
#####################################

PATH="$PATH:/home/brian/comandos"

eval "$(starship init bash)"
# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_ Hasta aquí -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
