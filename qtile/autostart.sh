#!/bin/bash

# Verifica si un proceso con el mismo nombre del comando pasado como argumento está en ejecución
# Si no se encuentra coincidencia con otro comando, se ejecuta en segundo plano
# Esto puede usarse para evitar ejecución duplicada de un comando o proceso específico
function run {
    if ! pgrep -x $(basename $1 | head -c 15) 1>/dev/null; then
        $@ &
    fi
}

# ESTE AUTOSTART ES SOLO PARA INICIAR COSAS DENTRO DE QTILE

# Establezca su resolución nativa SI no existe en xrandr

# Averigüe el nombre de su monitor con xrandr o arandr (guarde y obtendrá esta línea)
#autorandr horizontal

# Resolucion dinamica - detecta el monitor principal automaticamente
PRIMARY=$(xrandr | grep -E "^[a-zA-Z0-9-]+ connected primary" | awk '{print $1}')
if [ -z "$PRIMARY" ]; then
    PRIMARY=$(xrandr | grep -E "^[a-zA-Z0-9-]+ connected" | head -1 | awk '{print $1}')
fi

if [ -n "$PRIMARY" ]; then
    xrandr --output "$PRIMARY" --primary --auto
    # Detectar y configurar segundo monitor si existe
    SECONDARY=$(xrandr | grep -E "^[a-zA-Z0-9-]+ connected" | grep -v "$PRIMARY" | awk '{print $1}')
    if [ -n "$SECONDARY" ]; then
        xrandr --output "$SECONDARY" --right-of "$PRIMARY" --auto
    fi
fi

# cambia tu teclado si lo necesitas
# setxkbmap es -----------------------------------------------------------------------

# inicie sxhkd para reemplazar las combinaciones de teclas nativas de Qtile
run sxhkd -c ~/.config/qtile/sxhkd/sxhkdrc &
xrandr --output Virtual-1 --primary --mode 1680x1050 --pos 0x0 --rotate normal --output Virtual-2 --off --output Virtual-3 --off --output Virtual-4 --off --output Virtual-5 --off --output Virtual-6 --off --output Virtual-7 --off --output Virtual-8 --off
picom --config $HOME/.config/qtile/scripts/picom.conf &

# Poder ver las conexiones a internet
# run cbatticon &
run nm-applet &
run pamac-tray &
# run flameshot &
# run volumeicon &
# run udiskie -t & # Sirve para ver los usb conectados udisks2
run xfce4-power-manager &
numlockx on &
# blueberry-tray &

# recupera el fondo de pantalla seteado
# nitrogen --restore &
feh --bg-scale ~/wallpapers/0anime10.png
notify-send "Config lista" "Todo bien"
#feh --auto-reload
#run caffeine -a &
#run vivaldi-stable &
# run firefox &
# run thunar &
#run dropbox &
#run insync start &
#run spotify &
#run atom &
#run telegram-desktop &
